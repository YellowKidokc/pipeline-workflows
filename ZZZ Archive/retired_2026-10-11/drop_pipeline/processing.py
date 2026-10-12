"""Local NLP stages: extraction, classification lenses and Obsidian rendering."""
import hashlib
import json
import re
from pathlib import Path
from . import transcript_format as formatter

CATEGORIES = {
    "theology": r"\b(god|jesus|christ|scripture|bible|resurrection|grace|faith)\b",
    "science": r"\b(physics|quantum|energy|experiment|scientific|biology|entropy|measurement)\b",
    "history": r"\b(history|historical|ancient|archaeology|manuscript|century|dated)\b",
    "mathematics": r"\b(theorem|proof|lean\s*4|equation|axiom|mathematical|algebra)\b",
    "technology": r"\b(software|python|api|model|computer|algorithm|programming)\b",
}

def sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+|\n+', text.replace('>>', '\n')) if s.strip()]

def extract(source):
    raw = source.read_text(encoding='utf-8-sig', errors='strict')
    if source.suffix.lower() in {'.srt', '.vtt'}:
        # Existing caption parser, preserving raw originals separately.
        segments = formatter.parse_srt(str(source))
        if not segments:
            raise ValueError('No readable subtitle cues; review source format')
        return [{'title':source.stem, 'video_id':'', 'url':'', 'language':'',
                 'text':'\n'.join(s['text'] for s in segments), 'segments':segments}]
    if formatter.MD_SECTION.search(raw) and re.search(r'(?m)^### Transcript\s*$',raw):
        videos = formatter.split_combined_md(raw)
    elif '### Transcript' in raw:
        videos = formatter.parse_single_md(raw)
    else:
        heading=re.search(r'(?m)^#\s+(.+)$',raw)
        videos = [{'title':heading.group(1) if heading else source.stem,'video_id':'','url':'','language':'','body':raw}]
    result=[]
    for video in videos:
        body=video.pop('body', '')
        if not body.strip():
            raise ValueError('Missing transcript in collection: ' + video['title'])
        video.update(text=body,segments=formatter.parse_md_body(body))
        result.append(video)
    return result

def analyze(text, requested=(), category_patterns=None):
    from sklearn.feature_extraction.text import TfidfVectorizer
    chunks=sentences(text)
    usable=[(i,s) for i,s in enumerate(chunks) if len(s.split()) >= 6]
    summary=[]; keywords=[]
    if usable:
        try:
            vectorizer=TfidfVectorizer(stop_words='english',max_features=12000,ngram_range=(1,2))
            matrix=vectorizer.fit_transform([s for _,s in usable])
            weights=matrix.sum(axis=0).A1
            names=vectorizer.get_feature_names_out()
            keywords=[str(names[i]) for i in weights.argsort()[-12:][::-1]]
            scores=(matrix @ weights)
            chosen=sorted(scores.argsort()[-min(5,len(usable)):], key=lambda i:usable[i][0])
            summary=[usable[i][1] for i in chosen]
        except ValueError:
            pass
    categories={}
    for category,pattern in (category_patterns or CATEGORIES).items():
        matching=[s for s in chunks if re.search(pattern,s,re.I)]
        if matching or category in requested:
            categories[category]={'matching_passages':matching,'method':'lexical category lens; not factual verification'}
    return {'method':'local TF-IDF extractive NLP', 'summary':summary, 'keywords':keywords,
            'categories':categories, 'word_count':len(text.split()),
            'questions':[s for s in chunks if s.endswith('?')],
            'claim_signals':[s for s in chunks if re.search(r'\b(evidence|proves?|study|studies|according to|therefore)\b',s,re.I)]}

def readable(video):
    # Split explicit speaker markers before paragraphing; never invent speaker names.
    paragraphs=[]
    for turn in video['text'].split('>>'):
        for p in formatter.build_paragraphs(formatter.parse_md_body(turn)):
            paragraphs.append(p['text'])
    return '\n\n'.join(paragraphs)

def render(video, analysis, source_hash, route, extras=None):
    metadata={'type': 'youtube_transcript' if route=='youtube' else route,
              'title':video['title'], 'video_id':video.get('video_id',''), 'url':video.get('url',''),
              'language':video.get('language',''), 'source_sha256':source_hash,
              'status':'candidate', 'speaker_status':'unresolved',
              'tags':['source/'+route]+['topic/'+c for c in analysis['categories']],
              'keywords':analysis['keywords'], 'analysis_method':analysis['method']}
    # JSON scalars/lists are YAML-compatible; quoting prevents metadata injection.
    out=['---']+[f'{k}: {json.dumps(v,ensure_ascii=False)}' for k,v in metadata.items()]+['---','', '# '+video['title'],'',
         '> [!info] Source and analysis', '> Extractive summaries quote the supplied text. Topic matches do not verify claims. Speakers are not inferred.', '',
         '## Extractive overview','']
    out+=['> '+s.replace('\n','\n> ')+'\n' for s in analysis['summary']]
    out+=['## Topic views','']
    for category,data in analysis['categories'].items():
        out += ['### '+category.title(), '', f"{len(data['matching_passages'])} matching passages; full list in the analysis receipt.",'']
        out += ['> '+s.replace('\n','\n> ')+'\n' for s in data['matching_passages'][:3]]
    for heading, lines in (extras or {}).items():
        out += ['## '+heading, '', *lines, '']
    # Prose cleanup is for transcripts. Documents/prompts retain their Markdown
    # structure, including lists, code blocks and template line breaks.
    source_text=readable(video) if route=='youtube' else video['text']
    out+=['## Transcript' if route=='youtube' else '## Source text','',source_text,'']
    timed=[s for s in video['segments'] if s.get('start') is not None]
    if timed:
        out+=['## Timed source cues','']
        out += [f"[{formatter.fmt_stamp(s['start'])}] {s['text']}" for s in timed]
    return '\n'.join(out)
