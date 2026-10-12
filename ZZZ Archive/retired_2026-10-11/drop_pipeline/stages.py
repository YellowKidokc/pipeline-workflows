"""Explicit local stages. Add trusted stage functions here; workflows choose their order."""
import re
from .processing import analyze, CATEGORIES


def local_nlp(context):
    context['analysis']=analyze(context['video']['text'], context['categories'], context.get('category_patterns'))


def category_views(context):
    context['show_categories']=True


def reading_highlights(context):
    """Decorate copies of selected passages; leave source text untouched."""
    selected=context['analysis']['summary']
    lines=['> [!abstract] Suggested highlights',
           '> Selected by local text ranking for reading, not factual verification.', '']
    for passage in selected:
        # Do not create nested highlight delimiters from source Markdown.
        quote=passage.replace('==', '&#61;&#61;').replace('\n', '\n> ')
        lines.append('> =='+quote+'==\n')
    context['extras']['Reading highlights']=lines if selected else ['No passages selected.']


def research_signals(context):
    analysis=context['analysis']
    quotes=analysis['claim_signals'][:8]
    questions=analysis['questions'][:8]
    text=context['video']['text']
    refs=sorted(set(re.findall(r'\b(?:[1-3]\s+)?(?:Genesis|Exodus|Psalms?|Isaiah|Matthew|Mark|Luke|John|Romans|Corinthians|Revelation)\s+\d{1,3}:\d{1,3}(?:[-–]\d{1,3})?',text,re.I)))
    years=sorted(set(re.findall(r'\b(?:1[0-9]{3}|20[0-9]{2})\b',text)))
    context['signals']={'scripture_references':refs,'year_mentions':years,'claim_signal_count':len(analysis['claim_signals']),
                        'question_count':len(analysis['questions'])}
    context['extras']['Research signals']=['> [!note] Reading aids', '> These are lexical matches and quotations, not verified facts.', '',
        '**Scripture references:** '+(', '.join(refs) or 'None detected'),
        '**Year mentions:** '+(', '.join(years) or 'None detected'), '',
        '**Claim-bearing passages:**','']+['> '+s.replace('\n','\n> ')+'\n' for s in quotes]
    context['extras']['Questions raised']= ['> '+q.replace('\n','\n> ')+'\n' for q in questions] or ['No explicit questions detected.']


def prompt_structure(context):
    # Prompts are catalogued, never executed as instructions.
    text=context['video']['text']
    headings=re.findall(r'(?m)^#{1,6}\s+(.+)$',text)
    placeholders=sorted(set(re.findall(r'\{\{?([A-Za-z_][A-Za-z0-9_]*)\}?\}',text)))
    context['extras']['Prompt inventory']=['This prompt is stored for review; it has not been executed.', '',
        '**Sections:** '+(', '.join(headings) or 'None explicitly marked'),
        '**Placeholders:** '+(', '.join(placeholders) or 'None detected')]


STAGES={'local_nlp':local_nlp,'category_views':category_views,'reading_highlights':reading_highlights,'research_signals':research_signals,'prompt_structure':prompt_structure}
DEFAULT_STAGES=['normalize','local_nlp','category_views','reading_highlights','research_signals','obsidian_note']


def validate_stages(names):
    if not isinstance(names,list) or len(names)!=len(set(names)):
        raise ValueError('Stages must be a list without duplicates')
    if not names or names[0]!='normalize' or names[-1]!='obsidian_note' or 'local_nlp' not in names:
        raise ValueError('Workflow must start with normalize, include local_nlp and end with obsidian_note')
    if any(name not in STAGES and name not in {'normalize','obsidian_note'} for name in names):
        raise ValueError('Unknown workflow stage')
    if names.index('local_nlp')!=1:
        raise ValueError('local_nlp must follow normalize before other analysis stages')


def run_stages(video, categories, definition, config):
    names=definition['stages'];validate_stages(names)
    patterns=dict(CATEGORIES)
    for category,pattern in config.get('categories',{}).items():
        if not re.fullmatch(r'[a-z][a-z0-9_-]{0,40}',category):raise ValueError('Invalid category identifier')
        re.compile(pattern)
        patterns[category]=pattern
    context={'video':video,'categories':categories,'category_patterns':patterns,'extras':{},'show_categories':False}
    executed=[]
    for name in names[1:-1]:
        STAGES[name](context)
        executed.append(name)
    if not context['show_categories']:context['analysis']['categories']={}
    context['executed_stages']=['normalize',*executed,'obsidian_note']
    return context
