"""62_ATOM_BUILDER: claim atoms and axiom companions for each paper (ATOM BUILDER, Sep 2026).

Two passes per paper, papers in parallel, each pass the vendored ATOM BUILDER script unchanged
(vendor/atom_builder/scripts, from NAS Desktop/Folders/_____pipeline-workflows-main/.../ATOM BUILDER/scripts):

  atoms   process_atom_pipeline.py --file   CLAIM, EVIDENCE, PROOF, PROCESS + the 10-section Atom Meaning Block,
                                            and a nerve-draft JSON for 1-click import into the Claim Atom Builder
                                            (BACKSIDE/tools/atom-builder.html, "Import JSON"). Via OpenRouter.
  axioms  process_axiom_deepseek.py --file  the axiom companion: every axiom, theorem, definition or claim the
                                            paper states. DeepSeek direct.

Each pass runs in a private scratch folder, so the source note is never moved or archived.
Output, flat in the folder chosen at the button (default this OUTBOX):
  <note> · 62_ATOM_BUILDER.md      the meaning block(s), then the axiom companion
  _json/<note> · nerve-draft.json  the Claim Atom Builder import file
If one pass fails the other is kept and the failure is written at the top of the file.

No questions:  python BACKSIDE\\62_atom_builder.py <papers or folder> --outbox <folder> --workers 8
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRONT = HERE.parent
sys.path.insert(0, str(next(p for p in HERE.parents if (p / "_system").is_dir()) / "_system"))
from engine import pick  # noqa: E402
from engine.paths import inside  # noqa: E402

LABEL = "62_ATOM_BUILDER"
SCRIPTS = inside("vendor", "atom_builder", "scripts")
DEFAULT_MODEL = "deepseek/deepseek-v4-flash"  # vendored default is a free Nvidia model; deepseek-chat has no provider your OpenRouter account allows


def run(cmd: list[str], env: dict) -> str:
    r = subprocess.run([sys.executable, "-u", *cmd], env=env, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=1800)
    if r.returncode != 0:
        raise RuntimeError((r.stdout + r.stderr).strip()[-800:] or f"exit {r.returncode}")
    return r.stdout


def one(note: Path, out: Path, env: dict) -> bool:
    final = out / f"{note.stem} · {LABEL}.md"
    if final.exists() and not env.get("_REDO"):
        print(f"  SKIP {note.name} (already in {out})")
        return True
    failures, parts = [], [f"# Atoms: {note.stem}\n\nSource: `{note}`\n"]
    with tempfile.TemporaryDirectory(prefix="atom_") as tmp:
        work = Path(tmp)
        try:
            run([str(SCRIPTS / "process_atom_pipeline.py"), "--file", str(note), "--base", str(work / "atoms"), "--workers", "1"], env)
            blocks = sorted((work / "atoms" / "outbox").rglob("*_ATOM_MEANING_BLOCK.md"))
            parts += ["## Atom Meaning Block\n"] + [b.read_text(encoding="utf-8") for b in blocks]
            drafts = sorted((work / "atoms" / "outbox").rglob("nerve-draft*.json"))
            if drafts:
                (out / "_json").mkdir(parents=True, exist_ok=True)
                shutil.copy2(drafts[-1], out / "_json" / f"{note.stem} · nerve-draft.json")
        except Exception as exc:
            failures.append(f"atoms pass failed: {exc}")
        try:
            run([str(SCRIPTS / "process_axiom_deepseek.py"), "--file", str(note), "--out", str(work / "axioms"),
                 "--workers", "1", "--no-resume"], env)
            companions = sorted((work / "axioms").rglob("*_COMPANION.md"))
            parts += ["## Axiom companion\n"] + [c.read_text(encoding="utf-8") for c in companions]
        except Exception as exc:
            failures.append(f"axioms pass failed: {exc}")
    if len(failures) == 2:
        print(f"  FAILED {note.name}: {' | '.join(failures)}")
        return False
    head = "".join(f"> [!warning] {f}\n" for f in failures)
    final.write_text(head + "\n".join(parts) + "\n", encoding="utf-8")
    print(f"  OK   {note.name} -> {final.name}" + (f"  ({failures[0]})" if failures else ""))
    return not failures


def main() -> int:
    p = argparse.ArgumentParser(prog=LABEL, description=__doc__.splitlines()[0])
    p.add_argument("items", nargs="*", help="papers, folders of papers, or @list.txt (default: this INBOX)")
    p.add_argument("--outbox", "--out", dest="out", help=f"default {FRONT / 'OUTBOX'}")
    p.add_argument("--workers", type=int, default=8)
    p.add_argument("--limit", type=int)
    p.add_argument("--model", default=None, help=f"OpenRouter model for the atoms pass (default {DEFAULT_MODEL})")
    p.add_argument("--redo", action="store_true")
    p.add_argument("--dry-run", action="store_true", help="list the papers; no API")
    p.add_argument("--focus", action="append", default=[], help="accepted for the button; ATOM BUILDER prompts are fixed")
    a = p.parse_args()
    notes = [n for n in pick.resolve(a.items or [str(FRONT / "INBOX")]) if n.suffix.lower() in (".md", ".txt", ".lean")]
    notes = notes[:a.limit] if a.limit else notes
    if not notes:
        print(f"{LABEL}: no papers. Drop .md files into {FRONT / 'INBOX'} or pass them.")
        return 0
    if a.dry_run:
        for n in notes:
            print("PLAN", n)
        return 0
    out = Path(a.out) if a.out else FRONT / "OUTBOX"
    out.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, "PYTHONIOENCODING": "utf-8",
           "OPENROUTER_MODEL": a.model or os.environ.get("OPENROUTER_MODEL") or DEFAULT_MODEL}
    if a.redo:
        env["_REDO"] = "1"
    print(f"{LABEL}: {len(notes)} paper(s), {a.workers} at once, atoms model {env['OPENROUTER_MODEL']}, results -> {out}")
    with ThreadPoolExecutor(max_workers=max(1, min(a.workers, len(notes)))) as pool:
        results = list(pool.map(lambda n: one(n, out, env), notes))
    print(f"{LABEL}: done {sum(results)} of {len(notes)}")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
