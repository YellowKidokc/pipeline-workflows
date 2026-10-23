"""Runner for split CKG variants. Used by serve_backside.py (/run, /progress).

A variant is a folder with ckg.json + calls/. This folder is variant "general";
more go in variants/<name>/ (copy this folder's ckg.json + calls/).

For each note: run every switched-on call in run_order, passing earlier answers along,
then write OUTBOX/<variant>/<note>.md with sections in page order.
Dry run (the default) builds every prompt and writes them out instead of calling a model.
"""
import json
import os
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EXTS = {".md", ".txt"}


def variants():
    found = {}
    for d in [ROOT] + sorted((ROOT / "variants").glob("*")):
        if (d / "ckg.json").exists():
            m = json.loads((d / "ckg.json").read_text(encoding="utf-8"))
            found[m.get("variant", d.name)] = d
    return found


def load_variant(d):
    m = json.loads((d / "ckg.json").read_text(encoding="utf-8"))
    for c in m["calls"]:
        f = d / c["folder"]
        c["prompt"] = (f / "prompt.md").read_text(encoding="utf-8") if (f / "prompt.md").exists() else ""
        c["template"] = (f / "output.md").read_text(encoding="utf-8") if (f / "output.md").exists() else ""
    return m


def prompt_text(c, source, prior):
    p = c["prompt"].split("\n---\n", 1)[-1]  # drop the human note above the first ---
    prior_txt = "\n\n".join(f"## {k}\n{v}" for k, v in prior.items()) or "(none yet)"
    return (p.replace("{{output_template}}", c["template"])
             .replace("{{prior_results}}", prior_txt)
             .replace("{{source}}", source))


def call_model(model, prompt):
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        raise RuntimeError("DEEPSEEK_API_KEY is not set")
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                       "response_format": {"type": "json_object"}}).encode()
    req = urllib.request.Request("https://api.deepseek.com/chat/completions", data=body,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        reply = json.loads(r.read())["choices"][0]["message"]["content"]
    data = json.loads(reply)
    return data.get("markdown") or json.dumps(data, ensure_ascii=False, indent=2)


class Job:
    def __init__(self, folder, names, mode, workers, dry_run):
        self.folder, self.dry, self.workers = Path(folder), dry_run, max(1, min(20, int(workers)))
        if not self.folder.is_dir():
            raise ValueError(f"folder not found: {folder}")
        vs = variants()
        missing = [n for n in names if n not in vs]
        if missing or not names:
            raise ValueError(f"unknown variants: {missing or 'none picked'}")
        self.vars = {n: load_variant(vs[n]) for n in names}
        notes = sorted(p for p in self.folder.rglob("*") if p.suffix.lower() in EXTS and p.is_file())
        if not notes:
            raise ValueError("no .md or .txt files in that folder")
        pairs = [(n, v) for n in notes for v in names] if mode == "per_note" else [(n, v) for v in names for n in notes]
        self.items = [{"note": str(n), "name": n.name, "variant": v, "state": "waiting", "step": "",
                       "done": 0, "total": sum(1 for c in self.vars[v]["calls"] if c["on"] and c.get("run_order")),
                       "error": ""} for n, v in pairs]
        self.started, self.stopped, self.lock = time.time(), False, threading.Lock()

    def run_item(self, it):
        if self.stopped:
            it["state"] = "stopped"
            return
        m, note = self.vars[it["variant"]], Path(it["note"])
        it["state"] = "running"
        try:
            source = note.read_text(encoding="utf-8")
            prior, outs = {}, {}
            for c in sorted((c for c in m["calls"] if c["on"] and c.get("run_order")), key=lambda c: c["run_order"]):
                if self.stopped:
                    raise RuntimeError("stopped")
                it["step"] = c["id"]
                p = prompt_text(c, source, prior)
                outs[c["id"]] = (f"<!-- DRY RUN: {c['id']} prompt, {len(p):,} chars -->\n" + p) if self.dry \
                    else call_model(m.get("model", "deepseek-chat"), p)
                prior[c["id"]] = outs[c["id"]] if not self.dry else "(dry run)"
                it["done"] += 1
            page = []
            for c in sorted((c for c in m["calls"] if c.get("page_order")), key=lambda c: c["page_order"]):
                if c["kind"] == "paste_source":
                    page.append("# ORIGINAL ARTICLE\n\n" + source + "\n")
                elif c["id"] in outs:
                    page.append(outs[c["id"]].rstrip() + "\n")
                elif c["kind"] == "layout":
                    page.append(c["template"])
            sub = "_DRY_RUN" if self.dry else ""
            out = ROOT / "OUTBOX" / f"{it['variant']}{sub}" / f"{note.stem} · CKG.md"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text("\n".join(page), encoding="utf-8")
            it["state"], it["out"] = "done", str(out)
        except Exception as e:
            it["state"], it["error"] = ("stopped" if self.stopped else "failed"), str(e)

    def start(self):
        def go():
            with ThreadPoolExecutor(self.workers) as ex:
                list(ex.map(self.run_item, self.items))
            self.finished = time.time()
        self.finished = None
        threading.Thread(target=go, daemon=True).start()

    def status(self):
        count = lambda s: sum(1 for i in self.items if i["state"] == s)
        return {"dry_run": self.dry, "workers": self.workers, "items": self.items,
                "done": count("done"), "failed": count("failed"), "running": count("running"),
                "total": len(self.items), "elapsed": round((self.finished or time.time()) - self.started),
                "finished": self.finished is not None}
