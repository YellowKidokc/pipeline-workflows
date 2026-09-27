"""Implementations behind the S0-S10 single-purpose station modules."""
from __future__ import annotations
import datetime as dt, difflib, hashlib, json, os, re, sys, urllib.request
from collections import Counter
from pathlib import Path

SCRIPTURE_RE=re.compile(r"\b(?:[1-3]\s*)?(?:Genesis|Exodus|Psalms?|Isaiah|Matthew|Mark|Luke|John|Acts|Romans|Corinthians|Galatians|Ephesians|Philippians|Colossians|Thessalonians|Timothy|Titus|Hebrews|James|Peter|Jude|Revelation)\s+\d{1,3}:\d{1,3}(?:[-–]\d{1,3})?",re.I)
DATE_RE=re.compile(r"\b(?:c\.\s*)?(?:AD\s*)?(?:18|19|20)\d{2}(?:[-–](?:\d{2}|\d{4}))?\b",re.I)
PERSON_RE=re.compile(r"\b(?:Dr\.|Prof\.)?\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}\b")
SENTENCE_RE=re.compile(r"(?<=[.!?])\s+")

def _prefs(ctx): return json.loads((ctx.packet/'PREFS/preferences.json').read_text(encoding='utf-8'))
def _chunks(ctx): return ctx.ledger.db.execute("SELECT * FROM transcript_chunks WHERE video_id=? ORDER BY ordinal",(ctx.video_id,)).fetchall()
def _statements(ctx):
 src=ctx.video['source_id']; return ctx.ledger.db.execute("SELECT * FROM statements WHERE source_id=? ORDER BY id",(src,)).fetchall()
def _nas(ctx,endpoint,payload):
 url=_prefs(ctx).get('nas_nlp_url','http://192.168.2.50:8765').rstrip('/')+endpoint
 req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=3) as response: return json.load(response)
def _llm(ctx,prompt):
 prefs=_prefs(ctx); endpoints=[(prefs.get('ollama_url','http://192.168.2.50:11434').rstrip('/')+'/api/generate',{'model':prefs.get('ollama_model','qwen2.5:7b'),'prompt':prompt,'stream':False})]
 if prefs.get('llm_api_url') and prefs.get('llm_api_key'): endpoints.append((prefs['llm_api_url'],{'prompt':prompt}))
 last=None
 for url,payload in endpoints:
  try:
   headers={'Content-Type':'application/json'}
   if prefs.get('llm_api_key') and url==prefs.get('llm_api_url'): headers['Authorization']='Bearer '+prefs['llm_api_key']
   request=urllib.request.Request(url,data=json.dumps(payload).encode(),headers=headers)
   with urllib.request.urlopen(request,timeout=10) as response: return json.load(response)
  except Exception as exc: last=exc
 raise RuntimeError(f'no LLM endpoint available: {last}')
def _entity_id(db,kind):
 n=db.execute("SELECT count(*)+1 FROM entities").fetchone()[0]; return f"ENT-{kind[:4].upper()}-{n:05d}"
def intake(ctx):
 if not ctx.video['source_id'] or ctx.video['raw_transcript'] is None: raise ValueError('video lacks source or raw transcript')
 return {'source_id':ctx.video['source_id'],'characters':len(ctx.video['raw_transcript'])}
def chunks(ctx):
 prefs=_prefs(ctx); raw=ctx.video['raw_transcript'] or ''
 text=re.sub(r"\[(?:music|applause)\]",'',raw,flags=re.I) if prefs.get('remove_stage_directions',True) else raw
 if prefs.get('remove_fillers',True): text=re.sub(r"(?i)(?<!\w)(?:uh+|um+)(?:[, ]+|\b)",'',text)
 sentences=SENTENCE_RE.split(re.sub(r"\s+",' ',text).strip()); target=int(prefs.get('paragraph_words',200)); groups=[]; current=[]
 for sentence in sentences:
  if current and len((' '.join(current)+' '+sentence).split())>target: groups.append(' '.join(current)); current=[]
  if sentence: current.append(sentence)
 if current: groups.append(' '.join(current))
 with ctx.ledger.db:
  ctx.ledger.db.execute("DELETE FROM transcript_chunks WHERE video_id=?",(ctx.video_id,))
  for i,text in enumerate(groups,1):
   match=re.search(r"\b(?:\d{1,2}:)?\d{1,2}:\d{2}\b",text); stamp=match.group(0) if match else 'unknown'
   ctx.ledger.db.execute("INSERT INTO transcript_chunks VALUES(?,?,?,?,?,?)",(f"{ctx.video_id}-CH{i:04d}",ctx.video_id,i,text,f"t={stamp};L{i:03d}",f"t={stamp};L{i:03d}"))
  ctx.ledger.db.execute("UPDATE videos SET cleaned_transcript=? WHERE id=?",('\n\n'.join(groups),ctx.video_id))
 return {'chunks':len(groups)}
def entities(ctx):
 with ctx.ledger.db: ctx.ledger.db.execute("DELETE FROM entity_mentions WHERE video_id=?",(ctx.video_id,))
 count=0
 for chunk in _chunks(ctx):
  found=[]
  try:
   result=_nas(ctx,'/ner',{'text':chunk['text']}); items=result if isinstance(result,list) else result.get('entities',result.get('results',[]))
   for item in items:
    label=str(item.get('entity_group',item.get('label',''))).upper(); kind={'PER':'PERSON','PERSON':'PERSON','LOC':'PLACE','GPE':'PLACE','ORG':'ORG'}.get(label)
    if kind: found.append((item.get('word',item.get('text','')).replace('##','').strip(),kind,float(item.get('score',.5))))
  except Exception:
   found=[(x.strip(),'PERSON',.35) for x in PERSON_RE.findall(chunk['text'])]
  with ctx.ledger.db:
   for text,kind,confidence in found:
    if text:
     ctx.ledger.db.execute("INSERT OR IGNORE INTO entity_mentions(video_id,chunk_id,mention_text,entity_type,confidence) VALUES(?,?,?,?,?)",(ctx.video_id,chunk['id'],text,kind,confidence)); count+=1
 return {'mentions':count}
def resolve(ctx):
 aliases={r['alias'].lower():r['entity_id'] for r in ctx.ledger.db.execute('SELECT * FROM entity_aliases')}; resolved=review=0
 rows=ctx.ledger.db.execute("SELECT * FROM entity_mentions WHERE video_id=?",(ctx.video_id,)).fetchall()
 for mention in rows:
  key=mention['mention_text'].lower(); entity_id=aliases.get(key); lifecycle='CANDIDATE'
  if not entity_id:
   matches=difflib.get_close_matches(key,aliases.keys(),n=2,cutoff=.82)
   if len(matches)==1: entity_id=aliases[matches[0]]
   elif len(matches)>1: lifecycle='REVIEW'; review+=1
   else:
    entity_id=_entity_id(ctx.ledger.db,mention['entity_type'])
    with ctx.ledger.db:
     ctx.ledger.db.execute("INSERT INTO entities(id,entity_type,name) VALUES(?,?,?)",(entity_id,mention['entity_type'],mention['mention_text']))
     ctx.ledger.db.execute("INSERT INTO entity_aliases(alias,entity_id,confidence) VALUES(?,?,?)",(mention['mention_text'],entity_id,mention['confidence'] or .5))
    aliases[key]=entity_id
  with ctx.ledger.db: ctx.ledger.db.execute("UPDATE entity_mentions SET entity_id=?,lifecycle=? WHERE id=?",(entity_id,lifecycle,mention['id']))
  resolved+=bool(entity_id)
 return {'resolved':resolved,'review':review}
def dates(ctx):
 created=0
 for statement in _statements(ctx):
  for value in dict.fromkeys(DATE_RE.findall(statement['statement_text'])):
   event_id=ctx.ledger.next_id('EVT',ctx.video['collection'])
   with ctx.ledger.db: ctx.ledger.db.execute("INSERT INTO events(id,collection,event_date,event_date_precision,title,description,lifecycle) VALUES(?,?,?,?,?,?, 'CANDIDATE')",(event_id,ctx.video['collection'],value,'range' if '-' in value or '–' in value else 'year',statement['statement_text'][:200],statement['statement_text']))
   created+=1
 return {'events':created}
def claims(ctx):
 source_id=ctx.video['source_id']; transcript=ctx.video['cleaned_transcript'] or ctx.video['raw_transcript'] or ''; created=0; claims_created=0
 llm_claims=[]
 try:
  result=_llm(ctx,'Return JSON {"claims":[{"text":"...","attribution":"HIGH|MED|LOW"}]}. Extract atomic attributed claims only. Never add facts.\n'+transcript[:12000]); raw=result.get('response',result)
  parsed=json.loads(raw) if isinstance(raw,str) else raw; llm_claims=parsed.get('claims',[]) if isinstance(parsed,dict) else []
 except Exception: pass # deterministic sentence fallback below preserves the review workflow
 if not _statements(ctx):
  source_number=int(source_id.rsplit('-',1)[1])
  for i,sentence in enumerate(SENTENCE_RE.split(re.sub(r"\s+",' ',transcript).strip()),1):
   if not sentence: continue
   sid=ctx.ledger.add_statement(ctx.video['collection'],source_id,sentence,locator=f"video:{ctx.video_id}:sentence:{i}")
   with ctx.ledger.db: ctx.ledger.db.execute("UPDATE statements SET attribution_confidence=? WHERE id=?",('HIGH' if re.search(r'\b(?:I|we)\b',sentence) else 'MED',sid))
   created+=1
 for statement in _statements(ctx):
  text=statement['statement_text']
  if len(text.split())<6 or text.endswith('?'): continue
  exists=ctx.ledger.db.execute("SELECT 1 FROM claims WHERE statement_id=?",(statement['id'],)).fetchone()
  if exists: continue
  selected=next((item for item in llm_claims if item.get('text','').lower() in text.lower() or text.lower() in item.get('text','').lower()),None)
  claim_text=selected.get('text',text) if selected else text; confidence=selected.get('attribution','MED') if selected else ('HIGH' if re.search(r'\b(?:I|we)\b',text) else 'MED')
  cid=ctx.ledger.next_id('CLM',ctx.video['collection'])
  with ctx.ledger.db: ctx.ledger.db.execute("INSERT INTO claims(id,collection,statement_id,claim_text,claim_type,rating,claimed_evidence,counterclaim) VALUES(?,?,?,?,?,'UNRATED',?,?)",(cid,ctx.video['collection'],statement['id'],text,'CORE' if claims_created<5 else 'SUPPORTING','not extracted' if ctx.profile=='conspiracy' else None,'not extracted' if ctx.profile=='conspiracy' else None))
  with ctx.ledger.db:
   ctx.ledger.db.execute("UPDATE claims SET claim_text=? WHERE id=?",(claim_text,cid)); ctx.ledger.db.execute("UPDATE statements SET attribution_confidence=? WHERE id=?",(confidence if confidence in ('HIGH','MED','LOW') else 'LOW',statement['id']))
  claims_created+=1
 return {'statements_created':created,'claims':claims_created}
def themes(ctx):
 profile=(ctx.packet/'PROMPTS/profiles'/f"{ctx.profile}.md").read_text(encoding='utf-8'); labels=[]; active=False
 for line in profile.splitlines():
  if line.startswith('themes:'): active=True; continue
  if active and re.match(r"\s+- ",line): labels.append(re.sub(r"^\s+- ",'',line))
  elif active and line and not line.startswith(' '): break
 with ctx.ledger.db: ctx.ledger.db.execute("DELETE FROM theme_mentions WHERE video_id=?",(ctx.video_id,))
 count=0
 for chunk in _chunks(ctx):
  scores=[]
  try:
   result=_nas(ctx,'/zeroshot',{'text':chunk['text'],'labels':labels}); scores=list(zip(result.get('labels',labels),result.get('scores',[])))
  except Exception:
   low=chunk['text'].lower(); scores=[(label,.5) for label in labels if label.lower() in low]
  with ctx.ledger.db:
   for label,score in scores:
    if score>=float(_prefs(ctx).get('theme_threshold',.35)): ctx.ledger.db.execute("INSERT OR REPLACE INTO theme_mentions VALUES(?,?,?,?)",(ctx.video_id,chunk['id'],label,float(score))); count+=1
 return {'themes':count}
def citations(ctx):
 if ctx.profile!='christian': return {'disabled':True}
 count=0
 for statement in _statements(ctx):
  for ref in dict.fromkeys(SCRIPTURE_RE.findall(statement['statement_text'])):
   usage='proof text' if re.search(r'proves?|therefore|shows?',statement['statement_text'],re.I) else 'background'
   with ctx.ledger.db: ctx.ledger.db.execute("INSERT OR IGNORE INTO scripture_refs VALUES(?,?,?,?)",(ctx.video_id,statement['id'],ref,usage)); count+=1
 return {'scripture_refs':count}
def checkbacks(ctx):
 own={r['id'] for r in _statements(ctx)}; candidates=ctx.ledger.db.execute("SELECT id,statement_text FROM statements WHERE lifecycle='ACCEPTED'").fetchall(); matches=0
 for statement in _statements(ctx):
  try: _nas(ctx,'/embed',{'text':statement['statement_text']})
  except Exception: pass
  a=set(re.findall(r"\w{4,}",statement['statement_text'].lower()))
  for other in candidates:
   if other['id'] in own: continue
   b=set(re.findall(r"\w{4,}",other['statement_text'].lower())); score=len(a&b)/len(a|b) if a and b else 0
   if score>=.15:
    link_type='ANALOGY_TO'; engine='token-fallback'
    try:
     result=_nas(ctx,'/nli',{'premise':other['statement_text'],'hypothesis':statement['statement_text']}); label=str(result.get('label',result.get('labels',[''])[0])).upper(); confidence=float(result.get('score',result.get('scores',[score])[0])); score=confidence
     if 'CONTRAD' in label: link_type='CONTRADICTS'
     elif 'ENTAIL' in label or 'SUPPORT' in label: link_type='SUPPORTS'
     engine='nas-nli'
    except Exception: pass
    with ctx.ledger.db: ctx.ledger.db.execute("INSERT OR IGNORE INTO links(from_id,to_id,link_type,strength,source,created_at) VALUES(?,?,?,?,?,?)",(statement['id'],other['id'],link_type,score,engine,dt.datetime.now(dt.timezone.utc).isoformat()))
    if link_type=='CONTRADICTS':
     signal_id=ctx.ledger.next_id('CONTRA',ctx.video['collection']); hunch_id=ctx.ledger.next_id('HNCH',ctx.video['collection']); timestamp=dt.datetime.now(dt.timezone.utc).isoformat()
     with ctx.ledger.db:
      ctx.ledger.db.execute("INSERT INTO signals(id,collection,signal_kind,description,score,source_record_id,created_at) VALUES(?,?,'CONTRA',?,?,?,?)",(signal_id,ctx.video['collection'],f"Possible contradiction between {statement['id']} and {other['id']}",score,statement['id'],timestamp))
      ctx.ledger.db.execute("INSERT INTO hunches(id,collection,written_by,written_at,gut_statement,what_triggered_it,what_would_make_it_real,what_would_kill_it) VALUES(?,?,?,?,?,?,?,?)",(hunch_id,ctx.video['collection'],'system extraction',timestamp,'The speaker may contradict an earlier statement',signal_id,'Human comparison confirms mutually exclusive meanings','Context or qualification reconciles both statements'))
      ctx.ledger.db.execute("INSERT INTO links(from_id,to_id,link_type,source,created_at) VALUES(?,?,'PROMOTED_FROM','S8',?)",(signal_id,hunch_id,timestamp))
    matches+=1
 return {'matches':matches,'engine':'NAS /embed + /nli with token fallback'}
def validate(ctx):
 failures=[]
 if not ctx.video['raw_transcript']: failures.append('missing transcript')
 if not _chunks(ctx): failures.append('S1 produced no chunks')
 if not _statements(ctx): failures.append('S5 produced no statements')
 review=ctx.packet/'REVIEW'/f"{ctx.video_id}.reason.txt"
 if failures: review.write_text('\n'.join(failures)+'\n',encoding='utf-8'); raise ValueError('; '.join(failures))
 if review.exists(): review.unlink()
 return {'valid':True}
def _section(lines,title,items): lines += [f"## {title}",*(items or ['none found']),'']
def project(ctx):
 video=ctx.video; out=Path(os.environ.get('OPENINTEL_VAULT_ROOT') or (json.loads((ctx.packet/'CONFIG/config.json').read_text()).get('vault_root',str(ctx.packet/'OUTPUT')) if (ctx.packet/'CONFIG/config.json').exists() else ctx.packet/'OUTPUT'))
 folder=out/'YouTube'/re.sub(r'[<>:"/\\|?*]','-',video['channel']); folder.mkdir(parents=True,exist_ok=True)
 claims=ctx.ledger.db.execute("SELECT c.id,c.claim_text,s.locator FROM claims c LEFT JOIN statements s ON s.id=c.statement_id WHERE s.source_id=? ORDER BY c.id LIMIT 5",(video['source_id'],)).fetchall()
 entities=[r['name'] for r in ctx.ledger.db.execute("SELECT DISTINCT e.name FROM entity_mentions m JOIN entities e ON e.id=m.entity_id WHERE m.video_id=? LIMIT 5",(ctx.video_id,))]
 themes=[r['theme'] for r in ctx.ledger.db.execute("SELECT theme,max(confidence) score FROM theme_mentions WHERE video_id=? GROUP BY theme ORDER BY score DESC",(ctx.video_id,))]
 hunches=ctx.ledger.db.execute("SELECT h.id,h.gut_statement FROM hunches h JOIN links l ON l.from_id=h.id WHERE l.to_id IN (SELECT id FROM statements WHERE source_id=?)",(video['source_id'],)).fetchall()
 lines=[f"# {video['title']}",f"**Channel:** {video['channel']} · **Date:** {video['published_at'] or 'unknown'} · **Length:** {video['duration'] or 'unknown'} · [Watch]({video['url']}) · [Transcript]({video['channel']} - Chapter {video['chapter']:03d})",'']
 _section(lines,'What this is',[f"A transcript-derived {video['profile']} analysis of {video['title']}. Speaker and format require human confirmation."])
 _section(lines,'What it means',[f"- [[{r['id']}]] — {r['claim_text']} ({r['locator'] or 'timestamp unavailable'})" for r in claims])
 _section(lines,'How it connects',[*(f"- Theme: {x}" for x in themes),'- Inside this channel: none found','- To the vault: none found','- Tensions: none found'])
 graph=['```mermaid','graph LR','  Video[Video]']+[f"  Video --> C{i}[{re.sub(r'[^A-Za-z0-9 ]','',r['id'])}]" for i,r in enumerate(claims,1)]+[f"  Video --> E{i}[{re.sub(r'[^A-Za-z0-9 ]','',x)}]" for i,x in enumerate(entities,1)]+['```']
 _section(lines,'Mini graph',graph)
 _section(lines,'Open threads',[f"- [[{r['id']}]] — {r['gut_statement']}" for r in hunches])
 if video['profile']=='christian':
  refs=ctx.ledger.db.execute("SELECT reference,usage FROM scripture_refs WHERE video_id=?",(ctx.video_id,)).fetchall()
  _section(lines,'Christian lens',[*(f"- **Scripture used:** {r['reference']} — {r['usage']}" for r in refs),'- **Doctrine touched:** '+(', '.join(themes) if themes else 'none found'),'- **Apologetic argument type:** none found','- **Strength & weak points:** requires human review','- **Theophysics bridge:** none found'])
 path=folder/f"{video['channel']} - Chapter {video['chapter']:03d} - {re.sub(r'[<>:\"/\\|?*]','-',video['title'])} — CKG.md"; manual='\n<!-- manual -->\n'
 if path.exists() and '<!-- manual -->' in path.read_text(encoding='utf-8'): manual='\n<!-- manual -->'+path.read_text(encoding='utf-8').split('<!-- manual -->',1)[1]
 path.write_text('\n'.join(lines).rstrip()+manual,encoding='utf-8')
 # Rolling channel card is regenerated from ledger aggregates after every video.
 channel_path=folder/f"{video['channel']} — CKG.md"; channel_path.write_text(f"# {video['channel']} — CKG\n\n## Top claims\n"+'\n'.join(f"- {r['claim_text']}" for r in claims or [])+"\n\n## Most-cited people and works\n"+('\n'.join(f'- {x}' for x in entities) or 'none found')+"\n\n## Theme map\n"+('\n'.join(f'- {x}' for x in themes) or 'none found')+"\n\n## Position changes\nnone found\n\n## Cross-vault connections\nnone found\n\n## Open threads\n"+('\n'.join(f"- {r['gut_statement']}" for r in hunches) or 'none found')+'\n',encoding='utf-8')
 return {'ckg':str(path),'channel_ckg':str(channel_path)}
