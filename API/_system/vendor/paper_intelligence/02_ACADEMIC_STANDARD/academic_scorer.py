"""
L2: ACADEMIC STANDARD SCORER
=============================
Citation detection, external theory references, academic structure,
and Semantic Scholar lookup for real citation data.
"""
import re
from pathlib import Path

try:
    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    HAS_SS = True
except Exception:
    HAS_SS = False
    sch = None

ACADEMIC_SIGNALS = [
    'hypothesis','hypothesize','demonstrate','evidence','empirical',
    'methodology','statistically','significant','correlation','causation',
    'peer-reviewed','journal','publication','citation','literature review',
    'theoretical framework','research question','findings','conclusion',
    'data analysis','quantitative','qualitative','sample size','p-value',
    'confidence interval','reproducible','falsifiable','control group',
]

THEORY_SIGNALS = [
    # Physics
    'general relativity','quantum mechanics','thermodynamics','entropy',
    'information theory','decoherence','superposition','wave function',
    # Philosophy / Logic
    'godel','tarski','church-turing','incompleteness','modal logic',
    'epistemology','ontology','phenomenology',
    # Consciousness
    'integrated information','global workspace','orchestrated reduction',
    'hard problem','qualia','neural correlates',
    # Information
    'shannon entropy','kolmogorov complexity','algorithmic information',
    'landauer principle','maxwells demon',
    # Biology / Systems
    'second law','complexity','emergence','self-organization','attractor',
]

CITATION_PATTERNS = [
    r'\([A-Z][a-zA-Z\s]+,\s*\d{4}\)',   # (Author, 2020)
    r'\[\d+\]',                           # [1]
    r'\[[\w,\s]+\d{4}[\w,\s]*\]',        # [Smith2020]
    r'et al\.',                           # et al.
    r'ibid\.',                            # ibid.
    r'\b(doi|DOI)[:\.]\s*\S+',           # DOI
    r'https?://\S+',                      # URLs as references
]

STRUCTURE_MARKERS = {
    'has_abstract': r'\babstract\b',
    'has_introduction': r'\b(introduction|overview)\b',
    'has_methodology': r'\b(method|methodology|approach)\b',
    'has_results': r'\b(results?|findings?|outcomes?)\b',
    'has_discussion': r'\b(discussion|analysis|implications)\b',
    'has_conclusion': r'\b(conclusion|summary|closing)\b',
    'has_references': r'\b(references?|bibliography|works cited)\b',
}


def semantic_scholar_lookup(title, max_results=5):
    if not HAS_SS or not title:
        return {}
    try:
        results = sch.search_paper(title, limit=max_results, fields=[
            'title','year','citationCount','referenceCount',
            'venue','authors','abstract','influentialCitationCount'
        ])
        if not results or len(results) == 0:
            return {'ss_found': False}
        top = results[0]
        return {
            'ss_found': True,
            'ss_title': top.title,
            'ss_year': top.year,
            'ss_citation_count': top.citationCount,
            'ss_reference_count': top.referenceCount,
            'ss_venue': top.venue,
            'ss_influential_citations': top.influentialCitationCount,
        }
    except Exception as e:
        return {'ss_found': False, 'ss_error': str(e)}


def analyze(path_or_text, is_path=True, run_ss_lookup=False):
    if is_path:
        text = Path(path_or_text).read_text(encoding='utf-8', errors='ignore')
        fname = Path(path_or_text).name
        # Extract title from first H1
        title_match = re.search(r'^#\s+(.+)', text, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else fname.replace('.md','')
    else:
        text = path_or_text
        fname = 'inline'
        title = ''

    tl = text.lower()

    # Citation patterns
    citation_hits = []
    total_citations = 0
    for p in CITATION_PATTERNS:
        hits = re.findall(p, text)
        total_citations += len(hits)
        citation_hits.extend(hits[:3])

    # Academic signal words
    academic_score = sum(1 for term in ACADEMIC_SIGNALS if term in tl)
    academic_density = round(academic_score / max(len(text.split()), 1) * 1000, 2)

    # External theory references
    theory_hits = [t for t in THEORY_SIGNALS if t in tl]
    theory_count = len(theory_hits)

    # Structure check
    structure = {k: bool(re.search(v, tl)) for k, v in STRUCTURE_MARKERS.items()}
    structure_score = sum(structure.values())

    # Footnote / endnote markers
    footnotes = len(re.findall(r'\[\^[\w\d]+\]', text))

    # URL references
    urls = len(re.findall(r'https?://\S+', text))

    # DOI references
    dois = len(re.findall(r'\b(doi|DOI)[:\.]\s*\S+', text))

    result = {
        'file': fname,
        'title_detected': title[:80],
        'citation_count': total_citations,
        'citation_density_per1k': round(total_citations / max(len(text.split()), 1) * 1000, 2),
        'external_theory_count': theory_count,
        'external_theories': ', '.join(theory_hits[:8]),
        'academic_signal_count': academic_score,
        'academic_signal_density': academic_density,
        'structure_score': f"{structure_score}/{len(STRUCTURE_MARKERS)}",
        'has_abstract': structure['has_abstract'],
        'has_introduction': structure['has_introduction'],
        'has_methodology': structure['has_methodology'],
        'has_results': structure['has_results'],
        'has_conclusion': structure['has_conclusion'],
        'has_references_section': structure['has_references'],
        'footnote_count': footnotes,
        'url_references': urls,
        'doi_references': dois,
    }

    # Optional: Semantic Scholar lookup
    if run_ss_lookup and title:
        result.update(semantic_scholar_lookup(title))

    # Academic grade
    total = total_citations + theory_count + academic_score
    if total >= 40: result['academic_grade'] = 'A (Publication Grade)'
    elif total >= 25: result['academic_grade'] = 'B (Strong)'
    elif total >= 15: result['academic_grade'] = 'C (Moderate)'
    elif total >= 5:  result['academic_grade'] = 'D (Light)'
    else:             result['academic_grade'] = 'F (Needs Citations)'

    return result


if __name__ == '__main__':
    import sys, json
    run_ss = '--ss' in sys.argv
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        r = analyze(sys.argv[1], run_ss_lookup=run_ss)
        print(json.dumps(r, indent=2))
