"""Actions: one small job per file, callable alone or strung together into a workflow.

    python act.py                                  list the actions and workflows, then ask what to run
    python act.py scripture <note|folder|@list>    one action
    python act.py scripture title <folder>         several, in that order, on each note
    python act.py new_video <folder>               a workflow (workflows/new_video.txt)

An action is actions/<name>.py with:
    ABOUT = "one line: what it gives you"
    API = False                                    True if it calls a model (costs money)
    SERIAL = False                                 True if notes must go one at a time (shared state, e.g. title)
    def run(note: Path, text: str) -> dict         returns {"yaml": {...}} to store on the note, and/or
                                                   {"note": new_path} if it renamed the note, {"say": "..."} to print
Folders obey their _PICK.md (engine/pick.py), like every station. Results go ON the note: small values into its
YAML front matter (engine/note.py). Actions that write sections (publish) do it themselves.
"""
from __future__ import annotations

import importlib.util
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "_system"))
from engine import note as N, pick                         # noqa: E402

ACTIONS, WORKFLOWS = HERE / "actions", HERE / "workflows"


def load(name: str):
    spec = importlib.util.spec_from_file_location(f"action_{name}", ACTIONS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def available() -> tuple[list[str], list[str]]:
    acts = sorted(p.stem for p in ACTIONS.glob("*.py") if not p.name.startswith("_"))
    flows = sorted(p.stem for p in WORKFLOWS.glob("*.txt"))
    return acts, flows


def expand(names: list[str]) -> list[str]:
    """Action and workflow names -> the actions to run, in order."""
    acts, flows = available()
    out = []
    for n in names:
        if n in acts:
            out.append(n)
        elif n in flows:
            out += [l.split("#")[0].strip() for l in (WORKFLOWS / f"{n}.txt").read_text(encoding="utf-8").splitlines()
                    if l.split("#")[0].strip()]
        else:
            raise SystemExit(f"No action or workflow called '{n}'. Run act.py with no arguments to see the list.")
    unknown = [a for a in out if a not in acts]
    if unknown:
        raise SystemExit(f"Workflow names unknown action(s): {', '.join(unknown)}")
    return out


def one(path: Path, steps: list) -> str:
    said = []
    for name, mod in steps:
        try:
            text = path.read_text(encoding="utf-8")
            result = mod.run(path, text) or {}
        except Exception as exc:                            # one bad note never stops the rest
            said.append(f"{name}: FAILED {type(exc).__name__}: {exc}")
            break
        if result.get("yaml"):
            path.write_text(N.set_fields(path.read_text(encoding="utf-8"), result["yaml"]), encoding="utf-8")
        if result.get("note"):
            path = Path(result["note"])
        said.append(f"{name}: {result.get('say', 'ok')}")
    return f"{path.name[:90]}\n    " + "\n    ".join(said)


def ask(question: str) -> str:
    try:
        return input(question).strip().strip('"')
    except EOFError:
        return ""


def main(argv: list[str]) -> int:
    yes = "--yes" in argv
    argv = [a for a in argv if a != "--yes"]
    acts, flows = available()
    names = [a for a in argv if not Path(a).exists() and not a.startswith("@")]
    items = [a for a in argv if a not in names]
    if not names:
        print("\nACTIONS")
        for a in acts:
            m = load(a)
            print(f"  {a:<14} {'API ' if getattr(m, 'API', False) else 'free'}  {getattr(m, 'ABOUT', '')}")
        print("\nWORKFLOWS")
        for f in flows:
            print(f"  {f:<14} {' -> '.join(expand([f]))}")
        names = ask("\nWhich action(s) or workflow? (names, in order) ").split()
        if not names:
            return 0
    if not items:
        items = [ask("Which note or folder? (drag it here) ")]
    order = expand(names)
    loaded = [(n, load(n)) for n in order]
    # folder actions (SCOPE = "folder", e.g. clean: raw transcripts -> Clean MD) run first, on the folders named;
    # the note actions then run on the notes those folders hold (after the pick list)
    folder_steps = [(n, m) for n, m in loaded if getattr(m, "SCOPE", "note") == "folder"]
    steps = [(n, m) for n, m in loaded if getattr(m, "SCOPE", "note") != "folder"]
    folders = list(dict.fromkeys(Path(i) if Path(i).is_dir() else Path(i).parent for i in items if not i.startswith("@")))
    for name, mod in folder_steps:
        paid = " (calls a model)" if getattr(mod, "API", False) else ""
        if not yes and ask(f"{name}{paid} on {', '.join(f.name for f in folders)}? [Y/n] ").lower() in ("n", "no"):
            return 1
        for f in folders:
            print(f"{name}: {f.name}: {(mod.run_folder(f) or {}).get('say', 'ok')}", flush=True)
    if not steps:
        return 0
    notes = pick.resolve(items)
    if not notes:
        print("Nothing to run (see the PICK line above if a pick list was written).")
        return 0
    paid = [n for n, m in steps if getattr(m, "API", False)]
    print(f"\n{len(notes)} note(s) · {' -> '.join(order)}" + (f" · calls a model: {', '.join(paid)}" if paid else " · no API"))
    if not yes and ask("Run? [Y/n] ").lower() in ("n", "no"):
        return 1
    serial = any(getattr(m, "SERIAL", False) for _, m in steps)     # e.g. title: shared vocabulary, one at a time
    with ThreadPoolExecutor(max_workers=1 if serial else 4 if paid else 8) as pool:
        for line in pool.map(lambda p: one(p, steps), notes):
            print(line, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
