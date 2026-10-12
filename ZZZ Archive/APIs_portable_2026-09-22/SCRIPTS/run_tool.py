"""Run a named supporting tool with this package's Python and local key settings."""
from pathlib import Path
import subprocess
import sys
from api_workbench import ROOT, environment, initialize

TOOLS = {
    "synthesize": ("EVIDENCE/SCRIPTS/series_grand_synthesizer.py", []),
    "database": ("EVIDENCE/SCRIPTS/sync_to_sqlite.py", []),
    "pair": ("EVIDENCE/SCRIPTS/theophysics_congruence_matrix.py", []),
    "pair-god-is": ("EVIDENCE/SCRIPTS/god_is_unproven_to_lean.py", []),
    "annotate": ("EVIDENCE/SCRIPTS/three_dials_annotate.py", []),
    "merge": ("EVIDENCE/SCRIPTS/api_original_merge.py", []),
    "best-arguments": ("EVIDENCE/SCRIPTS/best_arguments_and_weaknesses.py", []),
    "build-argument": ("EVIDENCE/SCRIPTS/argument_builder.py", []),
    "evaluate-series": ("EVIDENCE/SCRIPTS/series_evaluator.py", ["--all", "--provider", "deepseek", "--workers", "12"]),
    "one-page": ("EVIDENCE/SCRIPTS/axiom_one_page_transform.py", []),
    "sidecars": ("EVIDENCE/SCRIPTS/evidence_sidecars.py", []),
    "search-sidecars": ("EVIDENCE/SCRIPTS/evidence_sidecars.py", ["--search-prompt"]),
    "pull-papers": ("LEAN4/SCRIPTS/pull_papers.py", []),
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in TOOLS:
        print("Choose a tool:", ", ".join(TOOLS))
        return 1
    name = sys.argv[1]
    path, flags = TOOLS[name]
    flags = list(flags)
    extra = sys.argv[2:]
    if name == "synthesize" and not extra:
        series = input("Series folder name: ").strip()
        if not series:
            return 1
        flags += ["--series", series, "--provider", "deepseek"]
    if name == "build-argument" and not extra:
        term = input("Argument to build: ").strip()
        if not term:
            return 1
        flags += ["--find", term, "--name", term]
    if name == "annotate" and not extra:
        print("Drag an article onto this launcher, or pass its file path.")
        return 1
    initialize()
    return subprocess.call([sys.executable, "-u", str(ROOT / path), *flags, *extra],
                           cwd=ROOT, env=environment())


if __name__ == "__main__":
    raise SystemExit(main())
