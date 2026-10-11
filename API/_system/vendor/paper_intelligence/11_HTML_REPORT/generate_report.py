"""
L11 — HTML REPORT GENERATOR
============================
Generates single-file HTML scorecards from pipeline JSON results.
Matches the Theophysics dark/gold aesthetic.
Each report is self-contained (inline CSS, inline Chart.js).

Usage:
  python generate_report.py --json results.json --output report_dir/
  python generate_report.py --json results.json --single   # one combined report
"""
import json, argparse, re
from pathlib import Path
from datetime import datetime


def _bar(val, max_val=1.0, color='#d4af37'):
    """Inline SVG bar."""
    pct = min((val or 0) / max_val * 100, 100)
    return f'<div style="display:flex;align-items:center;gap:8px"><div style="flex:1;height:8px;background:#1a1a1a;border-radius:4px;overflow:hidden"><div style="width:{pct}%;height:100%;background:{color};border-radius:4px"></div></div><span class="mono" style="font-size:0.75rem;color:#a0a0a0;min-width:45px;text-align:right">{val:.3f}</span></div>'


def _fruit_row(name, l6_val, l8_val, anti_val):
    """Row for fruits comparison table."""
    l6 = l6_val or 0
    l8 = l8_val or 0
    anti = anti_val or 0
    avg = (l6 + l8) / 2 if (l6 > 0 and l8 > 0) else max(l6, l8)
    return f'''<tr>
        <td style="font-weight:500;color:#e8e8e8">{name}</td>
        <td>{_bar(l6, 0.3, '#d4af37')}</td>
        <td>{_bar(l8, 1.0, '#22c55e')}</td>
        <td>{_bar(anti, 0.1, '#ef4444')}</td>
        <td class="mono" style="text-align:center;color:#d4af37">{avg:.3f}</td>
    </tr>'''


def generate_paper_html(row: dict) -> str:
    fname = row.get('file', 'Unknown')
    title = fname.replace('.md', '').replace('_', ' ')
    analyzed = row.get('analyzed_at', '')[:19]

    # Collect key metrics
    chi = row.get('L3_chi_score', 0) or 0
    chi_status = row.get('L3_chi_status', '')
    ckg = row.get('L3_ckg_tier', 'N/A')
    truth = row.get('L6_truth_score', 0) or 0
    coherence = row.get('L6_coherence_score', 0) or 0
    combined = row.get('L6_combined_score', 0) or 0
    words = row.get('L1_word_count', 0) or 0
    grade = row.get('L2_academic_grade', 'N/A')
    reading_level = row.get('L1_text_standard', 'N/A')
    claims = row.get('L6_claim_count', 0) or 0
    contradictions = row.get('L6_contradiction_flags', 0) or 0
    evidence = row.get('L6_evidence_density', 0) or 0
    fruit_net = row.get('L8_fruit_emo_net', 0) or 0
    idea_density = row.get('L10_idea_density_mean', 0) or 0
    idea_level = row.get('L10_idea_density_level', 'N/A')
    mtld = row.get('L9_lr_mtld', 0) or 0
    nrc_top = row.get('L8_nrc_top_emotions', '')
    emo_dominant = row.get('L8_emo_dominant', '')
    emo_top5 = row.get('L8_emo_top_5', '')
    posture = row.get('L6_character_posture', '')
    integrity = row.get('L6_integrity_profiles', '')
    centrality = row.get('L7_centrality_within_series', '')
    cluster = row.get('L7_cluster', '')

    # Fruits data for radar chart
    fruits = ['love', 'joy', 'peace', 'patience', 'kindness',
              'goodness', 'faithfulness', 'gentleness', 'self_control']
    l6_fruits = [row.get(f'L6_fruit_{f}', 0) or 0 for f in fruits]
    l8_fruits = [row.get(f'L8_fruit_emo_{f}', 0) or 0 for f in fruits]
    fruit_labels = [f.replace('_', ' ').title() for f in fruits]

    # Anti-fruits (L8)
    anti_names = ['hatred', 'despair', 'conflict', 'impatience', 'cruelty',
                  'corruption', 'betrayal', 'harshness', 'indulgence']
    anti_vals = [row.get(f'L8_anti_emo_{a}', 0) or 0 for a in anti_names]

    # Master equation variables
    me_vars = ['G_gravity_belonging', 'M_mass_meaning', 'E_entropy_engagement',
               'S_spacetime_structure', 'T_time_eternity', 'K_knowledge_logos',
               'R_relationship', 'Q_quantum_observer', 'F_faith_coupling', 'C_christ_coherence']
    me_labels = [v.split('_', 1)[1].replace('_', ' ').title() for v in me_vars]
    me_values = [row.get(f'L3_me_{v}', 0) or 0 for v in me_vars]

    # GoEmotions 27 values for bar chart
    emo_labels_27 = ['admiration', 'amusement', 'anger', 'annoyance', 'approval', 'caring',
                     'confusion', 'curiosity', 'desire', 'disappointment', 'disapproval',
                     'disgust', 'embarrassment', 'excitement', 'fear', 'gratitude', 'grief',
                     'joy', 'love', 'nervousness', 'optimism', 'pride', 'realization',
                     'relief', 'remorse', 'sadness', 'surprise', 'neutral']
    emo_values_27 = [row.get(f'L8_emo_{e}', 0) or 0 for e in emo_labels_27]

    # NRC 8 emotions
    nrc_labels = ['joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust', 'anger', 'anticipation']
    nrc_values = [row.get(f'L8_nrc_{e}', 0) or 0 for e in nrc_labels]

    # Layer health
    status = row.get('_layer_status', {})
    layer_html = ''
    for layer in sorted(status.keys()):
        st = status[layer]
        color = '#22c55e' if st == 'ok' else ('#f59e0b' if st == 'skipped' else '#ef4444')
        icon = '&#10003;' if st == 'ok' else ('&#8644;' if st == 'skipped' else '&#10007;')
        layer_html += f'<span style="display:inline-flex;align-items:center;gap:4px;padding:2px 8px;background:rgba({",".join(str(int(color.lstrip("#")[i:i+2],16)) for i in (0,2,4))},0.15);border-radius:4px;font-size:0.7rem;color:{color}">{icon} {layer}</span> '

    # Claims breakdown
    anchored = row.get('L6_anchored_claims', 0) or 0
    under = row.get('L6_under_supported_claims', 0) or 0
    over = row.get('L6_overstated_claims', 0) or 0
    falsifiable = row.get('L6_falsifiable_claims', 0) or 0
    speculative = row.get('L6_speculative_claims', 0) or 0

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Paper Intelligence: {title}</title>
<link href="https://fonts.googleapis.com/css2?family=Crimson+Text:wght@400;600&family=Inter:wght@300;400;500;600&family=Oswald:wght@400;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
:root {{
    --bg: #0a0a0a; --surface: #0f0f0f; --surface2: #1a1a1a; --surface3: #222;
    --border: #2a2a2a; --gold: #d4af37; --gold-dim: rgba(212,175,55,0.1);
    --text: #e8e8e8; --text-dim: #a0a0a0; --text-muted: #666;
    --red: #ef4444; --blue: #4a9eff; --teal: #2dd4bf; --green: #22c55e; --orange: #f59e0b;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; font-size: 15px; }}
.serif {{ font-family: 'Crimson Text', serif; }}
.display {{ font-family: 'Oswald', sans-serif; }}
.mono {{ font-family: 'JetBrains Mono', monospace; }}
.main {{ max-width: 1000px; margin: 0 auto; padding: 2rem 1.5rem 4rem; }}
h1 {{ font-family: 'Oswald', sans-serif; font-size: 1.8rem; color: var(--gold); margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 2px; }}
h2 {{ font-family: 'Oswald', sans-serif; font-size: 1.2rem; color: var(--gold); margin: 2rem 0 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--border); text-transform: uppercase; letter-spacing: 1px; }}
h3 {{ font-size: 0.9rem; color: var(--text-dim); margin: 1.2rem 0 0.6rem; text-transform: uppercase; letter-spacing: 1px; }}
.meta {{ font-size: 0.8rem; color: var(--text-muted); margin-bottom: 1.5rem; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 1rem; margin: 1rem 0; }}
.card {{ background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; }}
.card-label {{ font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); margin-bottom: 0.3rem; }}
.card-value {{ font-family: 'Oswald', sans-serif; font-size: 1.6rem; color: var(--gold); }}
.card-sub {{ font-size: 0.75rem; color: var(--text-dim); margin-top: 0.2rem; }}
.chart-box {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; margin: 1rem 0; }}
table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
th {{ text-align: left; padding: 8px 10px; border-bottom: 2px solid var(--border); color: var(--text-muted); font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; }}
td {{ padding: 6px 10px; border-bottom: 1px solid var(--border); }}
.badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 600; }}
.badge-gold {{ background: rgba(212,175,55,0.15); color: var(--gold); }}
.badge-green {{ background: rgba(34,197,94,0.15); color: var(--green); }}
.badge-red {{ background: rgba(239,68,68,0.15); color: var(--red); }}
.badge-blue {{ background: rgba(74,158,255,0.15); color: var(--blue); }}
.two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; }}
@media (max-width: 700px) {{ .two-col {{ grid-template-columns: 1fr; }} .grid {{ grid-template-columns: 1fr 1fr; }} }}
.footer {{ text-align: center; margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--border); font-size: 0.75rem; color: var(--text-muted); }}
</style>
</head>
<body>
<div class="main">

<h1>{title}</h1>
<div class="meta">
    Paper Intelligence Report &mdash; Schema {row.get('schema_version', '')} &mdash; {analyzed}<br/>
    {layer_html}
</div>

<!-- ══════════ KEY METRICS ══════════ -->
<div class="grid">
    <div class="card">
        <div class="card-label">CHI Score</div>
        <div class="card-value">{chi:.2f}</div>
        <div class="card-sub">{chi_status}</div>
    </div>
    <div class="card">
        <div class="card-label">Truth Score</div>
        <div class="card-value">{truth:.2f}</div>
        <div class="card-sub">Coherence: {coherence:.3f}</div>
    </div>
    <div class="card">
        <div class="card-label">Academic Grade</div>
        <div class="card-value">{grade}</div>
        <div class="card-sub">{reading_level}</div>
    </div>
    <div class="card">
        <div class="card-label">CKG Tier</div>
        <div class="card-value" style="font-size:1.2rem">{ckg}</div>
        <div class="card-sub">{words:,} words</div>
    </div>
    <div class="card">
        <div class="card-label">Idea Density</div>
        <div class="card-value">{idea_density:.3f}</div>
        <div class="card-sub">{idea_level}</div>
    </div>
    <div class="card">
        <div class="card-label">Fruit &minus; Anti</div>
        <div class="card-value" style="color:{'var(--green)' if fruit_net > 0 else 'var(--red)'}">{'+' if fruit_net > 0 else ''}{fruit_net:.3f}</div>
        <div class="card-sub">Emotion net score</div>
    </div>
    <div class="card">
        <div class="card-label">Vocab Diversity</div>
        <div class="card-value">{mtld:.0f}</div>
        <div class="card-sub">MTLD</div>
    </div>
    <div class="card">
        <div class="card-label">Claims Analyzed</div>
        <div class="card-value">{claims}</div>
        <div class="card-sub">{contradictions} contradictions</div>
    </div>
</div>

<!-- ══════════ FRUITS RADAR ══════════ -->
<h2>Fruits of the Spirit &mdash; Dual Channel</h2>
<div class="two-col">
    <div class="chart-box">
        <canvas id="fruitRadar" height="300"></canvas>
    </div>
    <div class="chart-box">
        <h3>Fruits Comparison Table</h3>
        <table>
            <tr><th>Fruit</th><th>L6 (Lexical)</th><th>L8 (Emotion)</th><th>Anti-Fruit</th><th>Avg</th></tr>
            {''.join(_fruit_row(
                fruit_labels[i],
                l6_fruits[i],
                l8_fruits[i],
                anti_vals[i] if i < len(anti_vals) else 0
            ) for i in range(9))}
        </table>
    </div>
</div>

<!-- ══════════ 27 EMOTIONS ══════════ -->
<h2>GoEmotions &mdash; 27 Fine-Grained Emotions</h2>
<div class="chart-box">
    <canvas id="emoBar" height="200"></canvas>
    <div style="margin-top:0.8rem;font-size:0.8rem;color:var(--text-dim)">
        <strong>Dominant:</strong> {emo_dominant} &nbsp;|&nbsp; <strong>Top 5:</strong> {emo_top5}
    </div>
</div>

<!-- ══════════ NRC PLUTCHIK ══════════ -->
<h2>NRC Plutchik Emotion Wheel</h2>
<div class="two-col">
    <div class="chart-box">
        <canvas id="nrcRadar" height="280"></canvas>
    </div>
    <div class="chart-box">
        <h3>NRC Top Emotions</h3>
        <div style="font-size:0.85rem;color:var(--text-dim);line-height:2">{nrc_top.replace(', ', '<br/>')}</div>
    </div>
</div>

<!-- ══════════ MASTER EQUATION ══════════ -->
<h2>Master Equation Variables</h2>
<div class="chart-box">
    <canvas id="meBar" height="200"></canvas>
</div>

<!-- ══════════ CLAIMS ══════════ -->
<h2>Claims Analysis</h2>
<div class="grid" style="grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));">
    <div class="card"><div class="card-label">Total Claims</div><div class="card-value">{claims}</div></div>
    <div class="card"><div class="card-label">Anchored</div><div class="card-value" style="color:var(--green)">{anchored}</div></div>
    <div class="card"><div class="card-label">Under-Supported</div><div class="card-value" style="color:var(--orange)">{under}</div></div>
    <div class="card"><div class="card-label">Overstated</div><div class="card-value" style="color:var(--red)">{over}</div></div>
    <div class="card"><div class="card-label">Falsifiable</div><div class="card-value" style="color:var(--blue)">{falsifiable}</div></div>
    <div class="card"><div class="card-label">Speculative</div><div class="card-value" style="color:var(--text-muted)">{speculative}</div></div>
</div>

<!-- ══════════ CHARACTER ══════════ -->
<h2>Character Profile</h2>
<div class="card" style="margin:1rem 0">
    <div style="margin-bottom:0.5rem"><span class="badge badge-gold">{posture}</span></div>
    <div style="font-size:0.85rem;color:var(--text-dim)">{integrity}</div>
</div>

<!-- ══════════ KEYWORDS ══════════ -->
<h2>Keywords &amp; Entities</h2>
<div class="two-col">
    <div class="card">
        <h3>KeyBERT Keywords</h3>
        <div style="font-size:0.8rem;color:var(--text-dim);line-height:1.8">
            {(row.get('L1_keybert_keywords', '') or '').replace(' | ', '<br/>')}
        </div>
    </div>
    <div class="card">
        <h3>NLP Entities</h3>
        <div style="font-size:0.8rem;color:var(--text-dim);line-height:1.8">
            <strong>People:</strong> {row.get('L5_entity_people', 'N/A')}<br/>
            <strong>Orgs:</strong> {row.get('L5_entity_orgs', 'N/A')}<br/>
            <strong>Count:</strong> {row.get('L5_entity_count', 0)} entities, {row.get('L5_entity_types_found', '')}
        </div>
    </div>
</div>

{'<h2>Knowledge Graph Position</h2><div class="card" style="margin:1rem 0"><div style="font-size:0.85rem;color:var(--text-dim)"><strong>Centrality:</strong> ' + str(centrality) + ' &nbsp;|&nbsp; <strong>Cluster:</strong> ' + str(cluster) + '</div></div>' if centrality else ''}

<div class="footer">
    Theophysics Paper Intelligence Pipeline v{row.get('schema_version', '2026')} &mdash; 10-Layer Analysis<br/>
    Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}
</div>

</div>

<script>
// Fruits Radar
new Chart(document.getElementById('fruitRadar'), {{
    type: 'radar',
    data: {{
        labels: {json.dumps(fruit_labels)},
        datasets: [
            {{ label: 'L6 Lexical', data: {json.dumps(l6_fruits)}, borderColor: '#d4af37', backgroundColor: 'rgba(212,175,55,0.1)', pointBackgroundColor: '#d4af37' }},
            {{ label: 'L8 Emotion', data: {json.dumps(l8_fruits)}, borderColor: '#22c55e', backgroundColor: 'rgba(34,197,94,0.1)', pointBackgroundColor: '#22c55e' }}
        ]
    }},
    options: {{
        responsive: true,
        scales: {{ r: {{ beginAtZero: true, grid: {{ color: '#2a2a2a' }}, ticks: {{ display: false }}, pointLabels: {{ color: '#a0a0a0', font: {{ size: 11 }} }} }} }},
        plugins: {{ legend: {{ labels: {{ color: '#a0a0a0' }} }} }}
    }}
}});

// GoEmotions Bar
new Chart(document.getElementById('emoBar'), {{
    type: 'bar',
    data: {{
        labels: {json.dumps([l.title() for l in emo_labels_27])},
        datasets: [{{ data: {json.dumps(emo_values_27)}, backgroundColor: {json.dumps(emo_values_27)}.map(v => v > 0.1 ? '#d4af37' : v > 0.01 ? 'rgba(212,175,55,0.5)' : 'rgba(212,175,55,0.15)') }}]
    }},
    options: {{
        responsive: true, indexAxis: 'y',
        scales: {{ x: {{ grid: {{ color: '#1a1a1a' }}, ticks: {{ color: '#666' }} }}, y: {{ ticks: {{ color: '#a0a0a0', font: {{ size: 10 }} }} }} }},
        plugins: {{ legend: {{ display: false }} }}
    }}
}});

// NRC Radar
new Chart(document.getElementById('nrcRadar'), {{
    type: 'radar',
    data: {{
        labels: {json.dumps([l.title() for l in nrc_labels])},
        datasets: [{{ label: 'NRC', data: {json.dumps(nrc_values)}, borderColor: '#4a9eff', backgroundColor: 'rgba(74,158,255,0.1)', pointBackgroundColor: '#4a9eff' }}]
    }},
    options: {{
        responsive: true,
        scales: {{ r: {{ beginAtZero: true, grid: {{ color: '#2a2a2a' }}, ticks: {{ display: false }}, pointLabels: {{ color: '#a0a0a0', font: {{ size: 11 }} }} }} }},
        plugins: {{ legend: {{ display: false }} }}
    }}
}});

// Master Equation Bar
new Chart(document.getElementById('meBar'), {{
    type: 'bar',
    data: {{
        labels: {json.dumps(me_labels)},
        datasets: [{{ data: {json.dumps(me_values)}, backgroundColor: '#d4af37' }}]
    }},
    options: {{
        responsive: true,
        scales: {{ x: {{ ticks: {{ color: '#a0a0a0', font: {{ size: 10 }} }} }}, y: {{ beginAtZero: true, grid: {{ color: '#1a1a1a' }}, ticks: {{ color: '#666' }} }} }},
        plugins: {{ legend: {{ display: false }} }}
    }}
}});
</script>
</body>
</html>'''
    return html


def main():
    parser = argparse.ArgumentParser(description="Generate HTML scorecards from pipeline JSON")
    parser.add_argument('--json', required=True, help='Path to pipeline results JSON')
    parser.add_argument('--output', default=None, help='Output directory (default: same as JSON)')
    parser.add_argument('--single', action='store_true', help='Generate one combined report')
    args = parser.parse_args()

    data = json.loads(Path(args.json).read_text(encoding='utf-8'))
    if not isinstance(data, list):
        data = [data]

    out_dir = Path(args.output) if args.output else Path(args.json).parent / "html_reports"
    out_dir.mkdir(parents=True, exist_ok=True)

    for row in data:
        fname = row.get('file', 'unknown').replace('.md', '')
        html = generate_paper_html(row)
        path = out_dir / f"PI_{fname}.html"
        path.write_text(html, encoding='utf-8')
        print(f"  Generated: {path.name}")

    print(f"\n{len(data)} HTML reports written to {out_dir}")


if __name__ == '__main__':
    main()
