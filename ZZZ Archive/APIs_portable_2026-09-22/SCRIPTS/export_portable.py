"""Export only explicitly listed program files, never private runtime content."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def export(destination, root=ROOT):
    entries = json.loads((root / "PACKAGE_FILES.json").read_text(encoding="utf-8"))["files"]
    data = []
    for name in entries:
        rel = Path(name)
        if rel.is_absolute() or ".." in rel.parts or name.endswith(".local.json") or rel.name.startswith(".env"):
            raise ValueError(f"Unsafe export entry: {name}")
        p = (root / rel).resolve()
        if not p.is_relative_to(root.resolve()) or not p.is_file():
            raise ValueError(f"Missing or external export entry: {name}")
        data.append((name, p.read_bytes()))
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "x", zipfile.ZIP_DEFLATED) as z:
        for name, content in data:
            z.writestr("APIs/" + name, content)
        z.writestr("APIs/EXPORT_HASHES.json", json.dumps({name: hashlib.sha256(content).hexdigest() for name, content in data}, indent=2))
    return destination


if __name__ == "__main__":
    from datetime import datetime
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / "outputs" / ("APIs-portable-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".zip")
    print(export(target))
