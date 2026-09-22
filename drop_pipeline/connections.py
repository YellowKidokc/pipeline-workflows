"""Local passage-backed similarities; these do not establish agreement."""
import json
import os
from uuid import uuid4
from pathlib import Path
from .paths import inside, relative

def write(path, text):
    temporary=path.with_name(path.name+"."+uuid4().hex+".tmp")
    temporary.write_text(text,encoding="utf-8")
    os.replace(temporary,path)


def rebuild(workspace):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    records=[json.loads(p.read_text(encoding='utf-8')) for p in sorted((workspace/'STATE'/'documents').glob('*.json'))]
    records=[r for r in records if inside(workspace,r['note']).is_file()]
    ready=workspace/'OBSIDIAN_READY';links=ready/'Links';links.mkdir(exist_ok=True)
    index=['# Research library','','Connections are lexical suggestions, not verified relationships.','']
    matrix=None
    if len(records)>1:
        try:
            vectorizer=TfidfVectorizer(stop_words='english',max_features=25000,ngram_range=(1,2))
            matrix=vectorizer.fit_transform([r['text'] for r in records])
        except ValueError:pass
    connections=[]
    for i,record in enumerate(records):
        note=Path(relative(record['note'])).stem
        index.append(f'- [[{note}|{record["title"]}]]')
        lines=['# Connections: '+record['title'],'',f'[[{note}|Return to source note]]',''];related=[]
        if matrix is not None:
            scores=cosine_similarity(matrix[i],matrix).ravel()
            for j in scores.argsort()[::-1]:
                if j==i or scores[j]<.08:continue
                other=records[j];passages=other['passages']
                if not passages:continue
                passage_scores=cosine_similarity(matrix[i],vectorizer.transform(passages)).ravel()
                passage=passages[int(passage_scores.argmax())]
                related.append({'target':other['id'],'score':round(float(scores[j]),4),'passage':passage,'source_sha256':other['source_sha256']})
                lines += [f'## [[{Path(relative(other["note"])).stem}|{other["title"]}]]','',f'Local TF-IDF similarity: {scores[j]:.3f}. Relationship requires review.','',
                          '> '+passage.replace('\n','\n> '),'',f'Source SHA-256: `{other["source_sha256"]}`','']
                if len(related)>=5:break
        if not related:lines+=['No related passages above the current threshold.']
        write(links/(record['id']+'.md'),'\n'.join(lines)+'\n')
        connections.append({'source':record['id'],'related':related})
    write(ready/'Library Index.md','\n'.join(index)+'\n')
    write(workspace/'STATE'/'connections.json',json.dumps(connections,indent=2,ensure_ascii=False))
    return {'documents':len(records),'connections':sum(len(r['related']) for r in connections)}
