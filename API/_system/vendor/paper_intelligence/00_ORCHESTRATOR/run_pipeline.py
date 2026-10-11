"""
MASTER ORCHESTRATOR
===================
Runs all 7 layers on a paper or series.
Outputs: Excel workbook + L4 7Q files into vault.

Usage:
  python run_pipeline.py --paper "path/to/paper.md"
  python run_pipeline.py --series "path/to/series/" --output "path/to/output/"
"""
import sys, json, re, argparse, hashlib
import os  # ONE_MENU
from pathlib import Path
from datetime import datetime

# Bump when scoring formulas, layer columns, or aggregation logic change.
# Lets you tell two runs apart even if file names match.
SCHEMA_VERSION = "2026.04.07-B"  # B: L6 upgraded to truth_coherence_scanner (fruits + anti-fruits + character)

# Add backend to path
BACKEND = Path(os.environ.get("ONE_MENU_PATH_PI_BACKEND") or Path(__file__).resolve().parent)  # ONE_MENU: was a fixed O: drive path
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(BACKEND / "analytics"))
sys.path.insert(0, str(BACKEND / "core"))

SUITE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(SUITE_DIR / "01_TEXT_ANALYTICS"))
sys.path.insert(0, str(SUITE_DIR / "02_ACADEMIC_STANDARD"))
sys.path.insert(0, str(SUITE_DIR / "03_THEOPHYSICS_METRICS"))
sys.path.insert(0, str(SUITE_DIR / "04_OPENAI_7Q"))
sys.path.insert(0, str(SUITE_DIR / "05_NLP_DEEP"))
sys.path.insert(0, str(SUITE_DIR / "06_TRUTH_ENGINE"))
sys.path.insert(0, str(SUITE_DIR / "07_KNOWLEDGE_GRAPHS"))
sys.path.insert(0, str(SUITE_DIR / "08_EMOTION_PROFILE"))
sys.path.insert(0, str(SUITE_DIR / "09_LINGUISTIC_DEPTH"))
sys.path.insert(0, str(SUITE_DIR / "10_IDEA_DENSITY"))

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    HAS_EXCEL = True
except ImportError:
    HAS_EXCEL = False
    print("WARNING: openpyxl not installed. Excel output disabled.")


def log_status(ok: bool, label: str, detail: str = ""):
    prefix = "[OK]" if ok else "[ERROR]"
    if detail:
        print(f"  {prefix} {label}: {detail}")
    else:
        print(f"  {prefix} {label}")


def run_layer(name, fn, *args, **kwargs):
    try:
        result = fn(*args, **kwargs)
        log_status(True, name)
        return result
    except Exception as e:
        log_status(False, name, str(e))
        return {}


def _check_layer_result(name: str, result: dict) -> bool:
    """Detect silent layer failures: a layer returning a dict with an *_error
    field is broken, even if no exception was raised. Returns True if healthy."""
    if not isinstance(result, dict):
        return True
    err_keys = [k for k in result.keys() if k.endswith("_error") or k == "error"]
    if err_keys:
        msgs = "; ".join(f"{k}={result[k]}" for k in err_keys)
        log_status(False, name, msgs)
        return False
    return True


def _stable_paper_id(paper: Path) -> str:
    """Hash the resolved path so the same paper gets the same ID across runs,
    even when re-run from a different cwd."""
    h = hashlib.sha1(str(paper.resolve()).lower().encode("utf-8")).hexdigest()
    return f"P-{h[:12]}"


def _slugify(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
    return s[:60] or "series"


def analyze_paper(paper_path, run_openai=False, vault_output=None,
                  series_id="", run_id=""):
    paper = Path(paper_path)
    print(f"\n{'='*60}")
    print(f"ANALYZING: {paper.name}")
    print(f"{'='*60}")

    row = {
        # ── Identity columns (stable across runs / reorderings) ──
        'paper_id':       _stable_paper_id(paper),
        'file':           paper.name,
        'series_id':      series_id,
        'run_id':         run_id,
        'schema_version': SCHEMA_VERSION,
        'source_path':    str(paper.resolve()),
        'analyzed_at':    datetime.now().isoformat(),
    }
    # Track per-layer health so we know which rows are trustworthy.
    row['_layer_status'] = {}

    def _record(layer_key, name, result):
        ok = _check_layer_result(name, result) if isinstance(result, dict) else False
        row['_layer_status'][layer_key] = "ok" if ok else "error"
        return ok

    # L1: Text Analytics
    try:
        import text_analyzer as L1
        r = L1.analyze(str(paper))
        r.pop('_keyword_list', None)
        r.pop('_bigram_list', None)
        row.update({f"L1_{k}": v for k, v in r.items() if k != 'file'})
        if _record("L1", "L1 Text Analytics", r):
            log_status(True, "L1 Text Analytics")
    except Exception as e:
        log_status(False, "L1 Text Analytics", str(e))
        row['_layer_status']['L1'] = "error"

    # L2: Academic Standard
    try:
        import academic_scorer as L2
        r = L2.analyze(str(paper))
        row.update({f"L2_{k}": v for k, v in r.items() if k != 'file'})
        if _record("L2", "L2 Academic Standard", r):
            log_status(True, "L2 Academic Standard")
    except Exception as e:
        log_status(False, "L2 Academic Standard", str(e))
        row['_layer_status']['L2'] = "error"

    # L3: Theophysics Metrics
    try:
        import theophysics_scorer as L3
        r = L3.analyze(str(paper))
        row.update({f"L3_{k}": v for k, v in r.items() if k != 'file'})
        if _record("L3", "L3 Theophysics Metrics", r):
            log_status(True, "L3 Theophysics Metrics")
    except Exception as e:
        log_status(False, "L3 Theophysics Metrics", str(e))
        row['_layer_status']['L3'] = "error"

    # L4: OpenAI 7Q (optional, costs money)
    if run_openai:
        try:
            import seven_q_runner as L4
            r = L4.run_paper(str(paper), vault_output)
            verdict = r.get('reverse_7q', {}).get('verdict', '')
            confidence = r.get('reverse_7q', {}).get('confidence_score', '')
            row['L4_7q_verdict'] = verdict
            row['L4_7q_confidence'] = confidence
            row['L4_7q_file'] = 'see vault _7Q_ANALYSIS folder'
            log_status(True, "L4 OpenAI 7Q")
            row['_layer_status']['L4'] = "ok"
        except Exception as e:
            log_status(False, "L4 OpenAI 7Q", str(e))
            row['_layer_status']['L4'] = "error"
    else:
        row['L4_7q_verdict'] = 'not run (use --openai flag)'
        row['_layer_status']['L4'] = "skipped"
        print(f"  - L4 OpenAI 7Q: skipped")

    # L5: NLP Deep
    try:
        import nlp_analyzer as L5
        r = L5.analyze(str(paper))
        row.update({f"L5_{k}": v for k, v in r.items() if k != 'file'})
        if _record("L5", "L5 NLP Deep", r):
            log_status(True, "L5 NLP Deep")
    except Exception as e:
        log_status(False, "L5 NLP Deep", str(e))
        row['_layer_status']['L5'] = "error"

    # L6: Truth Engine (requires sentence-transformers, slow first run)
    try:
        import truth_runner as L6
        r = L6.score_paper(str(paper))
        row.update({f"L6_{k}": v for k, v in r.items() if k != 'file'})
        if _record("L6", "L6 Truth Engine", r):
            log_status(True, "L6 Truth Engine")
    except Exception as e:
        log_status(False, "L6 Truth Engine", str(e))
        row['_layer_status']['L6'] = "error"

    # L8: Emotion Profile (NRCLex + GoEmotions 27-emotion → Fruits mapping)
    try:
        import emotion_analyzer as L8
        r = L8.analyze(str(paper))
        row.update({f"L8_{k}": v for k, v in r.items()})
        if _record("L8", "L8 Emotion Profile", r):
            log_status(True, "L8 Emotion Profile")
    except Exception as e:
        log_status(False, "L8 Emotion Profile", str(e))
        row['_layer_status']['L8'] = "error"

    # L9: Linguistic Depth (textdescriptives + lexicalrichness)
    try:
        import linguistic_analyzer as L9
        r = L9.analyze(str(paper))
        row.update({f"L9_{k}": v for k, v in r.items()})
        if _record("L9", "L9 Linguistic Depth", r):
            log_status(True, "L9 Linguistic Depth")
    except Exception as e:
        log_status(False, "L9 Linguistic Depth", str(e))
        row['_layer_status']['L9'] = "error"

    # L10: Idea Density (propositional density)
    try:
        import idea_density_analyzer as L10
        r = L10.analyze(str(paper))
        row.update({f"L10_{k}": v for k, v in r.items()})
        if _record("L10", "L10 Idea Density", r):
            log_status(True, "L10 Idea Density")
    except Exception as e:
        log_status(False, "L10 Idea Density", str(e))
        row['_layer_status']['L10'] = "error"

    return row


def analyze_series(series_path, output_path=None, run_openai=False):
    series = Path(series_path)
    papers = sorted([f for f in series.glob("*.md")
                     if (re.match(r'^\d{2}', f.name) or re.match(r'^GTQ_\d', f.name))
                     and not f.name.startswith('00')
                     and f.name not in ('README.md', '_CLAUDIAN_AUDIT.md', 'GTQ_00_INDEX.md')])

    if output_path:
        out_dir = Path(output_path)
    else:
        out_dir = series / "_PAPER_INTELLIGENCE"
    out_dir.mkdir(parents=True, exist_ok=True)

    series_slug = _slugify(series.name)
    run_id = datetime.now().strftime('%Y%m%d_%H%M%S')
    series_id = f"S-{hashlib.sha1(str(series.resolve()).lower().encode()).hexdigest()[:10]}"

    print(f"\nSeries: {series.name}")
    print(f"Papers: {len(papers)}")
    print(f"Output: {out_dir}")
    print(f"Run ID: {run_id}  Schema: {SCHEMA_VERSION}")

    all_rows = []
    for p in papers:
        vault_out = str(p.parent)
        row = analyze_paper(str(p), run_openai=run_openai, vault_output=vault_out,
                            series_id=series_id, run_id=run_id)
        all_rows.append(row)

    # Build Knowledge Graph
    try:
        import graph_builder as L7
        graph_result = L7.build_graph(all_rows, str(out_dir))
        for i, row in enumerate(all_rows):
            g = graph_result.get('node_data', {}).get(row['file'], {})
            row['L7_centrality_within_series'] = g.get('centrality', '')
            row['L7_cluster'] = g.get('cluster', '')
            row['_layer_status']['L7'] = "ok"
        print()
        log_status(True, "L7 Knowledge Graph built")
    except Exception as e:
        print()
        log_status(False, "L7 Knowledge Graph", str(e))
        for row in all_rows:
            row['_layer_status']['L7'] = "error"

    # Export to Excel
    excel_path = None
    if HAS_EXCEL and all_rows:
        excel_path = out_dir / f"{series_slug}_PAPER_INTELLIGENCE_{run_id}.xlsx"
        write_excel(all_rows, excel_path)
        print(f"\n  Excel: {excel_path.name}")

    # JSON backup
    json_path = out_dir / f"{series_slug}_pipeline_results_{run_id}.json"
    json_path.write_text(json.dumps(all_rows, indent=2, default=str), encoding='utf-8')
    print(f"  JSON:  {json_path.name}")

    # Run summary — one-glance health snapshot for this run
    summary = {
        "schema_version": SCHEMA_VERSION,
        "run_id":         run_id,
        "series_id":      series_id,
        "series_name":    series.name,
        "series_path":    str(series.resolve()),
        "output_dir":     str(out_dir.resolve()),
        "paper_count":    len(all_rows),
        "openai_enabled": bool(run_openai),
        "excel":          excel_path.name if excel_path else None,
        "layer_health":   _aggregate_layer_health(all_rows),
        "papers":         [{"paper_id": r.get("paper_id"),
                            "file":     r.get("file"),
                            "status":   r.get("_layer_status", {})}
                           for r in all_rows],
    }
    (out_dir / f"{series_slug}_run_summary_{run_id}.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    print(f"\n{'='*60}")
    print(f"COMPLETE — {len(all_rows)} papers analyzed")
    print(f"Layer health: {summary['layer_health']}")
    print(f"{'='*60}")
    return all_rows


def _aggregate_layer_health(rows):
    """Count ok/error/skipped per layer across all papers in this run."""
    counts = {}
    for r in rows:
        for layer, status in r.get("_layer_status", {}).items():
            counts.setdefault(layer, {"ok": 0, "error": 0, "skipped": 0})
            counts[layer][status] = counts[layer].get(status, 0) + 1
    return counts


LAYER_COLORS = {
    'L1_': 'D6E4F7',  # blue
    'L2_': 'D6F7D6',  # green
    'L3_': 'F7F0D6',  # gold
    'L4_': 'F7D6D6',  # red/pink
    'L5_': 'EBD6F7',  # purple
    'L6_': 'D6F7F0',  # teal
    'L7_': 'F7E6D6',  # orange
    'L8_': 'F7D6E8',  # pink (emotion)
    'L9_': 'D6E8F7',  # light steel blue (linguistic)
    'L10_': 'E8F7D6', # light lime (idea density)
}

def _flatten_for_excel(rows):
    """openpyxl can't write dicts. Flatten _layer_status into a single string col."""
    out = []
    for r in rows:
        r2 = dict(r)
        ls = r2.pop("_layer_status", None)
        if isinstance(ls, dict):
            r2["layer_status"] = ",".join(f"{k}:{v}" for k, v in sorted(ls.items()))
        out.append(r2)
    return out


def write_excel(rows, path):
    rows = _flatten_for_excel(rows)
    wb = openpyxl.Workbook()

    # SUMMARY SHEET — key metrics only
    ws = wb.active
    ws.title = "SUMMARY"
    summary_cols = [
        'paper_id', 'file', 'series_id', 'run_id', 'schema_version',
        'L1_word_count', 'L1_flesch_kincaid_grade', 'L1_reading_level',
        'L1_vocab_richness', 'L1_avg_sentence_length',
        'L2_citation_count', 'L2_external_theory_count', 'L2_academic_signal_score',
        'L3_chi_score', 'L3_wk_ratio', 'L3_fruits_composite',
        'L3_cross_domain_bridges', 'L3_ckg_tier',
        'L4_7q_verdict', 'L4_7q_confidence',
        'L5_topic_count', 'L5_entity_count', 'L5_key_sentence',
        # ── L6 Truth Engine RICH (truth_coherence_scanner) ──
        'L6_truth_score', 'L6_coherence_score', 'L6_combined_score',
        'L6_evidence_density', 'L6_falsifiability_density', 'L6_hedge_density',
        'L6_contradiction_flags', 'L6_absolute_pressure', 'L6_rhetorical_force',
        'L6_warmth_score', 'L6_discipline_score',
        'L6_fruit_integrity_score', 'L6_anti_fruit_pressure',
        # Fruits (9)
        'L6_fruit_love', 'L6_fruit_joy', 'L6_fruit_peace', 'L6_fruit_patience',
        'L6_fruit_kindness', 'L6_fruit_goodness', 'L6_fruit_faithfulness',
        'L6_fruit_gentleness', 'L6_fruit_self_control',
        # Anti-fruits (9)
        'L6_anti_love', 'L6_anti_joy', 'L6_anti_peace', 'L6_anti_patience',
        'L6_anti_kindness', 'L6_anti_goodness', 'L6_anti_faithfulness',
        'L6_anti_gentleness', 'L6_anti_self_control',
        # Claim breakdown
        'L6_claim_count', 'L6_anchored_claims', 'L6_under_supported_claims',
        'L6_overstated_claims', 'L6_speculative_claims', 'L6_contradictory_claims',
        'L6_falsifiable_claims',
        # Character profile rollup
        'L6_threat_score', 'L6_protection_score', 'L6_balance_score',
        'L6_primary_threats', 'L6_primary_protections',
        'L6_character_posture', 'L6_integrity_profiles',
        'L7_centrality_within_series', 'L7_cluster',
        # ── L8 Emotion Profile ──
        'L8_nrc_joy', 'L8_nrc_trust', 'L8_nrc_fear', 'L8_nrc_anger',
        'L8_nrc_sadness', 'L8_nrc_disgust', 'L8_nrc_surprise', 'L8_nrc_anticipation',
        'L8_nrc_positive', 'L8_nrc_negative', 'L8_nrc_top_emotions',
        'L8_emo_dominant', 'L8_emo_top_5',
        'L8_emo_admiration', 'L8_emo_amusement', 'L8_emo_anger', 'L8_emo_annoyance',
        'L8_emo_approval', 'L8_emo_caring', 'L8_emo_confusion', 'L8_emo_curiosity',
        'L8_emo_desire', 'L8_emo_disappointment', 'L8_emo_disapproval', 'L8_emo_disgust',
        'L8_emo_embarrassment', 'L8_emo_excitement', 'L8_emo_fear', 'L8_emo_gratitude',
        'L8_emo_grief', 'L8_emo_joy', 'L8_emo_love', 'L8_emo_nervousness',
        'L8_emo_optimism', 'L8_emo_pride', 'L8_emo_realization', 'L8_emo_relief',
        'L8_emo_remorse', 'L8_emo_sadness', 'L8_emo_surprise', 'L8_emo_neutral',
        # Fruits ← Emotions mapping
        'L8_fruit_emo_love', 'L8_fruit_emo_joy', 'L8_fruit_emo_peace',
        'L8_fruit_emo_patience', 'L8_fruit_emo_kindness', 'L8_fruit_emo_goodness',
        'L8_fruit_emo_faithfulness', 'L8_fruit_emo_gentleness', 'L8_fruit_emo_self_control',
        'L8_anti_emo_hatred', 'L8_anti_emo_despair', 'L8_anti_emo_conflict',
        'L8_anti_emo_impatience', 'L8_anti_emo_cruelty', 'L8_anti_emo_corruption',
        'L8_anti_emo_betrayal', 'L8_anti_emo_harshness', 'L8_anti_emo_indulgence',
        'L8_fruit_emo_composite', 'L8_anti_emo_composite', 'L8_fruit_emo_net',
        # ── L9 Linguistic Depth ──
        'L9_lr_ttr', 'L9_lr_rttr', 'L9_lr_cttr',
        'L9_lr_mtld', 'L9_lr_mattr', 'L9_lr_hdd',
        'L9_lr_words', 'L9_lr_terms',
        # ── L10 Idea Density ──
        'L10_idea_density_mean', 'L10_idea_density_min', 'L10_idea_density_max',
        'L10_idea_density_std', 'L10_idea_total_propositions',
        'L10_idea_paragraphs_analyzed', 'L10_idea_density_level',
    ]
    # Write header
    for col, key in enumerate(summary_cols, 1):
        cell = ws.cell(row=1, column=col, value=key.replace('_', ' ').replace('L1 ', '[L1] ').replace('L2 ', '[L2] ').replace('L3 ', '[L3] ').replace('L4 ', '[L4] ').replace('L5 ', '[L5] ').replace('L6 ', '[L6] ').replace('L7 ', '[L7] '))
        # Color by layer
        for prefix, color in LAYER_COLORS.items():
            if key.startswith(prefix):
                cell.fill = PatternFill(start_color=color, end_color=color, fill_type='solid')
        cell.font = Font(bold=True)

    for row_idx, row in enumerate(rows, 2):
        for col, key in enumerate(summary_cols, 1):
            val = row.get(key, '')
            if isinstance(val, float):
                val = round(val, 4)
            ws.cell(row=row_idx, column=col, value=val)

    ws.freeze_panes = 'B2'
    ws.auto_filter.ref = f"A1:{openpyxl.utils.get_column_letter(len(summary_cols))}1"

    # FULL DATA SHEET
    ws2 = wb.create_sheet("FULL_DATA")
    if rows:
        all_keys = list(rows[0].keys())
        for col, key in enumerate(all_keys, 1):
            cell = ws2.cell(row=1, column=col, value=key)
            cell.font = Font(bold=True)
            for prefix, color in LAYER_COLORS.items():
                if key.startswith(prefix):
                    cell.fill = PatternFill(start_color=color, end_color=color, fill_type='solid')
        for row_idx, row in enumerate(rows, 2):
            for col, key in enumerate(all_keys, 1):
                val = row.get(key, '')
                if isinstance(val, float):
                    val = round(val, 4)
                ws2.cell(row=row_idx, column=col, value=val)

    wb.save(str(path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Theophysics Paper Intelligence Pipeline")
    parser.add_argument('--paper', help='Single paper .md path')
    parser.add_argument('--series', help='Series folder path')
    parser.add_argument('--output', help='Output directory for Excel and JSON')
    parser.add_argument('--openai', action='store_true', help='Run OpenAI 7Q layer (costs ~$0.02/paper)')
    args = parser.parse_args()

    if args.paper:
        row = analyze_paper(args.paper, run_openai=args.openai)
        print(json.dumps({k: v for k, v in row.items()
                          if not k.startswith('_')}, indent=2, default=str))
    elif args.series:
        analyze_series(args.series, args.output, run_openai=args.openai)
    else:
        print("Usage:")
        print("  python run_pipeline.py --paper path/to/paper.md")
        print("  python run_pipeline.py --series path/to/series/ [--output path/] [--openai]")
