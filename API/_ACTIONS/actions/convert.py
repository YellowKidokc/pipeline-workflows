"""convert: every PDF, Word, HTML, spreadsheet or slide file in a folder -> markdown in <folder>/Converted MD/.

Calls ConversionStation (python -m theophysics_conversion.convert SRC --out ...) in its own .venv; nothing is
rewritten here. Files already converted (the .md exists) are skipped. Originals are never touched.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_system"))
from engine.paths import configured, external  # noqa: E402

ABOUT = "PDF / DOCX / HTML / XLSX / PPTX in a folder -> markdown in <folder>/Converted MD (ConversionStation)"
API = False
SCOPE = "folder"
EXTS = {".pdf", ".docx", ".doc", ".html", ".htm", ".xlsx", ".xls", ".pptx", ".epub", ".rtf", ".odt"}


def run_folder(folder: Path) -> dict:
    if not configured("conversion_station"):
        return {"say": "conversion_station is not set in _system/config/paths.json"}
    cs = external("conversion_station")
    py = cs / ".venv" / "Scripts" / "python.exe"
    out_dir = folder / "Converted MD"
    files = sorted(f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in EXTS)
    done = failed = skipped = 0
    for f in files:
        out = out_dir / f"{f.stem}.md"
        if out.exists():
            skipped += 1
            continue
        out_dir.mkdir(exist_ok=True)
        r = subprocess.run([str(py), "-m", "theophysics_conversion.convert", str(f), "--out", str(out)],
                           cwd=cs, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode == 0 and out.exists():
            done += 1
        else:
            failed += 1
            print(f"  convert FAILED {f.name}: {(r.stderr or r.stdout).strip().splitlines()[-1:] or ''}", flush=True)
    return {"say": f"{done} converted, {skipped} already done, {failed} failed ({len(files)} file(s)) -> {out_dir}"}
