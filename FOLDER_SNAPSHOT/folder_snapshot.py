"""Folder Snapshot — drop a folder in, get one HTML page that shows what's in it.

Usage:
    python folder_snapshot.py "D:\\some\\folder"              # stats only, no API
    python folder_snapshot.py "D:\\some\\folder" --ai         # + DeepSeek summaries
    python folder_snapshot.py "D:\\some\\folder" -o out.html --max-files 2000

DeepSeek: set DEEPSEEK_API_KEY in your environment. Uses the OpenAI-compatible
endpoint https://api.deepseek.com/chat/completions (model deepseek-chat).
Stdlib only. Output is a single self-contained HTML file (opens offline).
"""
import argparse, collections, datetime as dt, html, json, math, os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

TEXT_EXT = {".md", ".txt", ".html", ".htm", ".py", ".json", ".csv", ".js", ".ts", ".lean", ".tex", ".yaml", ".yml"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".obsidian", ".venv", "venv", ".trash"}
STOP = set("""a about above after again against all also am an and any are as at be because been before being below
between both but by can could did do does doing down during each few for from further had has have having he her here
hers him his how i if in into is it its itself just me more most my no nor not now of off on once only or other our
ours out over own same she should so some such than that the their theirs them then there these they this those through
to too under until up very was we were what when where which while who whom why will with would you your yours one two
may might must shall us let like get got make made use used using also yet via per etc http https www com html div span
class style href src true false none null return def import self var const function new string data type value""".split())

# ---------- reading ----------
def read_text(p):
    try:
        with open(p, "rb") as f:
            raw = f.read(2_000_000)
    except OSError:
        return ""
    t = raw.decode("utf-8", "ignore")
    if p.lower().endswith((".html", ".htm")):
        t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
        t = re.sub(r"(?s)<[^>]+>", " ", t)
        t = html.unescape(t)
    return t

def title_of(p, raw):
    m = re.search(r"(?im)^#\s+(.+)$", raw) or re.search(r"(?is)<title>(.*?)</title>", raw)
    return (m.group(1).strip()[:120] if m else os.path.splitext(os.path.basename(p))[0])

def tokens(t):
    return [w for w in re.findall(r"[a-zA-Z][a-zA-Z\-]{2,}", t.lower()) if w not in STOP and len(w) < 30]

def scan(root, max_files):
    files = []
    for d, dirs, names in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not x.startswith(".")]
        for n in names:
            p = os.path.join(d, n)
            try:
                st = os.stat(p)
            except OSError:
                continue
            ext = os.path.splitext(n)[1].lower()
            rec = {"path": os.path.relpath(p, root), "name": n, "ext": ext or "(none)", "bytes": st.st_size,
                   "mtime": st.st_mtime, "folder": os.path.relpath(d, root).split(os.sep)[0] if d != root else "(top)",
                   "text": ext in TEXT_EXT}
            files.append(rec)
            if len(files) >= max_files:
                return files
    return files

# ---------- analysis ----------
def analyse(root, files):
    docs = [f for f in files if f["text"] and f["bytes"] > 0]
    df = collections.Counter()
    for f in docs:
        full = os.path.join(root, f["path"])
        with open(full, "rb") as fh:
            raw = fh.read(2_000_000).decode("utf-8", "ignore")
        txt = read_text(full)
        tk = tokens(txt)
        f["title"] = title_of(full, raw)
        f["words"] = len(re.findall(r"\S+", txt))
        f["headings"] = len(re.findall(r"(?m)^#{1,6}\s", raw)) + len(re.findall(r"(?i)<h[1-6]", raw))
        f["links"] = len(re.findall(r"\[\[[^\]]+\]\]", raw)) + len(re.findall(r"(?i)href=", raw))
        f["tf"] = collections.Counter(tk)
        f["snippet"] = re.sub(r"\s+", " ", txt).strip()[:400]
        df.update(set(tk))
    n = max(len(docs), 1)
    for f in docs:
        sc = {w: c * math.log(n / (1 + df[w])) for w, c in f["tf"].items() if df[w] < n * 0.6 or n < 4}
        f["keys"] = [w for w, _ in sorted(sc.items(), key=lambda x: -x[1])[:8]]
        f["kset"] = set(w for w, _ in sorted(sc.items(), key=lambda x: -x[1])[:40])
    # families: greedy by shared top keyword
    fam_count = collections.Counter(k for f in docs for k in f["keys"][:3])
    fams = [w for w, c in fam_count.most_common(8) if c >= 2]
    for f in docs:
        f["family"] = next((k for k in f["keys"][:5] if k in fams), "other")
    corpus = collections.Counter()
    for f in docs:
        corpus.update(f["tf"])
    return docs, fams, corpus

def overlap_matrix(docs, limit=24):
    top = sorted(docs, key=lambda f: -f["words"])[:limit]
    m = [[(len(a["kset"] & b["kset"]) / max(1, len(a["kset"] | b["kset"]))) for b in top] for a in top]
    return top, m

# ---------- DeepSeek ----------
def deepseek(prompt, key, max_tokens=300):
    body = json.dumps({"model": "deepseek-chat", "max_tokens": max_tokens, "temperature": 0.2,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request("https://api.deepseek.com/chat/completions", body,
                                 {"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.load(r)["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"(DeepSeek call failed: {e})"

def ai_pass(root, docs, fams, key, max_ai):
    targets = sorted(docs, key=lambda f: -f["words"])[:max_ai]
    def one(f):
        txt = read_text(os.path.join(root, f["path"]))[:6000]
        f["ai"] = deepseek("In 2 sentences, say what this document is and its main claim or purpose. "
                           f"Then on a new line give 'Status:' draft/spec/finished/notes/code.\n\nFILE: {f['name']}\n\n{txt}", key)
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(one, targets))
    digest = "\n".join(f"- {f['name']} [{f['family']}]: {f.get('ai') or f['snippet'][:200]}" for f in targets[:80])
    return deepseek("You are summarizing a research folder for its owner. Write a short overview (5-8 sentences): "
                    "what this folder is, the main threads, what looks finished vs unfinished, duplicates, and the "
                    f"3 files worth opening first. Families: {', '.join(fams)}\n\n{digest}", key, 700)

# ---------- HTML ----------
PALETTE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948", "#898781"]

def bubbles_svg(docs, famcol):
    top = sorted(docs, key=lambda f: -f["words"])[:120]
    W, H = 960, 520
    placed = []
    mx = max([f["words"] for f in top] + [1])
    out = []
    for i, f in enumerate(top):
        r = 6 + 44 * math.sqrt(f["words"] / mx)
        ang, rad = i * 2.399963, 0  # golden-angle spiral, push out until no collision
        while True:
            x, y = W / 2 + rad * math.cos(ang), H / 2 + rad * math.sin(ang) * 0.55
            if all((x - a) ** 2 + (y - b) ** 2 >= (r + c + 2) ** 2 for a, b, c in placed) or rad > 700:
                break
            rad += 3
        placed.append((x, y, r))
        lbl = html.escape(f["title"][:22]) if r > 22 else ""
        out.append(f'<g class="b" data-i="{docs.index(f)}"><circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{famcol[f["family"]]}" fill-opacity=".72"/>'
                   f'<text x="{x:.0f}" y="{y+4:.0f}" text-anchor="middle">{lbl}</text><title>{html.escape(f["title"])} — {f["words"]:,} words</title></g>')
    return f'<svg viewBox="0 0 {W} {H}" class="chart">{"".join(out)}</svg>'

def venn_svg(docs, fams, famcol):
    big = fams[:3]
    if len(big) < 2:
        return "<p class='muted'>Not enough families to overlap.</p>"
    sets = {k: set(f["path"] for f in docs if k in f["kset"]) for k in big}
    pos = [(330, 200), (530, 200), (430, 340)][:len(big)]
    mx = max(len(s) for s in sets.values()) or 1
    out = []
    for (x, y), k in zip(pos, big):
        r = 90 + 70 * math.sqrt(len(sets[k]) / mx)
        out.append(f'<circle cx="{x}" cy="{y}" r="{r:.0f}" fill="{famcol[k]}" fill-opacity=".28" stroke="{famcol[k]}" stroke-width="2"/>')
        out.append(f'<text x="{x}" y="{y - r + 26:.0f}" text-anchor="middle" class="vl">{html.escape(k)} · {len(sets[k])}</text>')
    a, b = big[0], big[1]
    out.append(f'<text x="430" y="205" text-anchor="middle" class="vn">{len(sets[a] & sets[b])}</text>')
    if len(big) == 3:
        c = big[2]
        out.append(f'<text x="430" y="265" text-anchor="middle" class="vn">{len(sets[a] & sets[b] & sets[c])}</text>')
        out.append(f'<text x="365" y="300" text-anchor="middle" class="vn">{len(sets[a] & sets[c])}</text>')
        out.append(f'<text x="495" y="300" text-anchor="middle" class="vn">{len(sets[b] & sets[c])}</text>')
    return f'<svg viewBox="0 0 860 520" class="chart">{"".join(out)}</svg>'

def heat_html(top, m):
    def cell(v):
        a = min(1, v * 2.2)
        return f'<td style="background:rgba(42,120,214,{a:.2f})" title="{v:.0%}">{"" if v >= .999 else f"{v*100:.0f}"}</td>'
    head = "".join(f'<th><span>{html.escape(f["title"][:26])}</span></th>' for f in top)
    rows = "".join(f'<tr><th class="rh">{html.escape(f["title"][:34])}</th>{"".join(cell(v) for v in row)}</tr>' for f, row in zip(top, m))
    return f'<div class="heatwrap"><table class="heat"><tr><th></th>{head}</tr>{rows}</table></div>'

def bars(counter, n=12, fmt="{:,}"):
    items = counter.most_common(n)
    mx = max([v for _, v in items] + [1])
    return "".join(f'<div class="bar"><span class="bl">{html.escape(str(k))}</span><span class="bt"><i style="width:{100*v/mx:.1f}%"></i></span><span class="bv">{fmt.format(v)}</span></div>' for k, v in items)

def timeline(files):
    days = collections.Counter(dt.date.fromtimestamp(f["mtime"]).strftime("%Y-%m") for f in files)
    return bars(collections.Counter(dict(sorted(days.items())[-18:])), 18)

def render(root, files, docs, fams, corpus, overview):
    famcol = {k: PALETTE[i % 8] for i, k in enumerate(fams)}; famcol["other"] = PALETTE[8]
    words = sum(f.get("words", 0) for f in docs)
    newest = max(files, key=lambda f: f["mtime"]) if files else None
    top, m = overlap_matrix(docs)
    dupes = collections.defaultdict(list)
    for f in files:
        dupes[(f["name"].lower(), f["bytes"])].append(f["path"])
    dupes = [v for v in dupes.values() if len(v) > 1]
    strip = [("Files", f"{len(files):,}"), ("Readable docs", f"{len(docs):,}"), ("Words", f"{words:,}"),
             ("Families", str(len(fams))), ("Possible duplicates", str(len(dupes))),
             ("Last change", dt.datetime.fromtimestamp(newest["mtime"]).strftime("%b %d, %Y") if newest else "—")]
    fammap = "".join(
        f'<div class="fam" style="--c:{famcol[k]}"><b>{html.escape(k)}</b><small>{sum(1 for f in docs if f["family"]==k)} files</small>'
        f'<ul>{"".join(f"<li>{html.escape(f["title"][:60])}</li>" for f in sorted([d for d in docs if d["family"]==k], key=lambda d:-d["words"])[:5])}</ul></div>'
        for k in fams + ["other"])
    rows = "".join(
        f'<tr data-fam="{html.escape(f["family"])}"><td><span class="dot" style="background:{famcol[f["family"]]}"></span>{html.escape(f["title"][:80])}'
        f'<div class="path">{html.escape(f["path"])}</div>{"<div class=ai>"+html.escape(f["ai"])+"</div>" if f.get("ai") else ""}</td>'
        f'<td>{f["ext"]}</td><td class="n">{f["words"]:,}</td><td class="n">{f["headings"]}</td><td class="n">{f["links"]}</td>'
        f'<td>{dt.date.fromtimestamp(f["mtime"])}</td><td class="k">{html.escape(", ".join(f["keys"][:5]))}</td></tr>'
        for f in sorted(docs, key=lambda d: -d["mtime"]))
    dupe_html = "".join(f"<li>{' · '.join(html.escape(p) for p in v[:4])}</li>" for v in dupes[:40]) or "<li class='muted'>None found.</li>"
    ov = f'<section class="card ov"><h2>What this folder is</h2><p>{html.escape(overview).replace(chr(10), "<br>")}</p></section>' if overview else ""
    legend = "".join(f'<button class="lg" data-f="{html.escape(k)}" style="--c:{famcol[k]}">{html.escape(k)}</button>' for k in fams + ["other"])
    return TEMPLATE.format(
        title=html.escape(os.path.basename(os.path.abspath(root)) or root), root=html.escape(os.path.abspath(root)),
        when=dt.datetime.now().strftime("%b %d, %Y %H:%M"), ov=ov,
        strip="".join(f'<div class="kpi"><b>{v}</b><span>{k}</span></div>' for k, v in strip),
        bubbles=bubbles_svg(docs, famcol), venn=venn_svg(docs, fams, famcol), heat=heat_html(top, m),
        fammap=fammap, terms=bars(collections.Counter({w: c for w, c in corpus.most_common(14)}), 14),
        types=bars(collections.Counter(f["ext"] for f in files), 10),
        folders=bars(collections.Counter(f["folder"] for f in files), 10),
        time=timeline(files), rows=rows, dupes=dupe_html, legend=legend)

TEMPLATE = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Snapshot · {title}</title><style>
:root{{--plane:#f5f5f2;--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--muted:#898781;--grid:#e1e0d9;--accent:#2a78d6}}
@media(prefers-color-scheme:dark){{:root{{--plane:#0e0e0d;--surface:#171716;--ink:#ecebe7;--ink2:#b4b2ab;--muted:#7d7b74;--grid:#2a2a27}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--plane);color:var(--ink);font:15px/1.5 system-ui,Segoe UI,sans-serif}}
main{{max-width:1240px;margin:0 auto;padding:28px 16px 80px}}h1{{font:600 34px/1.15 Georgia,serif;margin:0}}
h2{{font:600 20px Georgia,serif;margin:0 0 12px}}.sub{{color:var(--muted);font-size:13px;margin:6px 0 22px;word-break:break-all}}
.strip{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:0 0 18px}}
.kpi{{background:var(--surface);border:1px solid var(--grid);border-radius:10px;padding:14px}}.kpi b{{display:block;font:600 26px Georgia,serif}}.kpi span{{color:var(--muted);font-size:12.5px}}
.card{{background:var(--surface);border:1px solid var(--grid);border-radius:10px;padding:18px;margin:0 0 18px}}
.ov p{{font:17px/1.6 Georgia,serif;margin:0}}.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}.grid3{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
@media(max-width:860px){{.grid2,.grid3{{grid-template-columns:1fr}}}}
.chart{{width:100%;height:auto;display:block}}.chart text{{font-size:11px;fill:var(--ink);pointer-events:none}}.b{{cursor:pointer}}.b.dim{{opacity:.12}}
.vl{{font:600 14px system-ui!important}}.vn{{font:600 18px Georgia!important}}
.legend{{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}}.lg{{border:1px solid var(--c);color:var(--ink);background:transparent;border-radius:999px;padding:3px 10px;font-size:12.5px;cursor:pointer}}.lg.on{{background:var(--c);color:#fff}}
.fams{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}}.fam{{border-left:4px solid var(--c);padding:6px 10px;background:var(--plane);border-radius:6px}}.fam small{{color:var(--muted);margin-left:6px}}.fam ul{{margin:6px 0 0;padding-left:16px;font-size:13px;color:var(--ink2)}}
.bar{{display:grid;grid-template-columns:120px 1fr 60px;gap:8px;align-items:center;font-size:13px;margin:3px 0}}.bl{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}.bt{{background:var(--grid);height:9px;border-radius:5px;overflow:hidden}}.bt i{{display:block;height:100%;background:var(--accent)}}.bv{{text-align:right;color:var(--ink2)}}
.heatwrap{{overflow:auto;max-height:640px}}.heat{{border-collapse:collapse;font-size:10.5px}}.heat td{{width:26px;height:22px;text-align:center;border:1px solid var(--surface);color:var(--ink)}}
.heat th span{{writing-mode:vertical-rl;transform:rotate(180deg);display:inline-block;max-height:150px;overflow:hidden;font-weight:400;color:var(--ink2)}}.heat .rh{{text-align:right;font-weight:400;white-space:nowrap;padding-right:6px;color:var(--ink2)}}
input{{width:100%;padding:9px 12px;border:1px solid var(--grid);border-radius:8px;background:var(--plane);color:var(--ink);font:inherit;margin:0 0 10px}}
.tw{{overflow:auto;max-height:720px}}table.files{{width:100%;border-collapse:collapse;font-size:13px}}.files th{{position:sticky;top:0;background:var(--surface);text-align:left;color:var(--muted);font-weight:500;padding:8px;border-bottom:1px solid var(--grid)}}
.files td{{padding:8px;border-bottom:1px solid var(--grid);vertical-align:top}}.n{{text-align:right}}.k{{color:var(--ink2)}}.path{{color:var(--muted);font-size:11.5px}}.ai{{margin-top:4px;color:var(--ink2);font-style:italic}}
.dot{{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px}}.muted{{color:var(--muted)}}ul.d{{font-size:12.5px;color:var(--ink2)}}
</style></head><body><main>
<h1>{title}</h1><div class="sub">{root} · snapshot {when}</div>
<div class="strip">{strip}</div>{ov}
<section class="card"><h2>Every document, sized by length</h2><div class="legend">{legend}</div>{bubbles}</section>
<div class="grid2"><section class="card"><h2>How the biggest families overlap</h2>{venn}</section>
<section class="card"><h2>Family map</h2><div class="fams">{fammap}</div></section></div>
<section class="card"><h2>The matrix: which documents share vocabulary</h2><p class="muted" style="margin-top:-6px">The 24 longest documents. Darker = more shared key terms (%).</p>{heat}</section>
<div class="grid3"><section class="card"><h2>Recurring terms</h2>{terms}</section><section class="card"><h2>File types</h2>{types}</section><section class="card"><h2>Subfolders</h2>{folders}</section></div>
<div class="grid2"><section class="card"><h2>When it was written</h2>{time}</section><section class="card"><h2>Possible duplicates</h2><ul class="d">{dupes}</ul></section></div>
<section class="card"><h2>The wall: every document</h2><input id="q" placeholder="Filter by title, path, or term…"><div class="tw"><table class="files"><thead><tr><th>Document</th><th>Type</th><th>Words</th><th>Heads</th><th>Links</th><th>Changed</th><th>Key terms</th></tr></thead><tbody id="rows">{rows}</tbody></table></div></section>
</main><script>
const rows=[...document.querySelectorAll('#rows tr')];let fam=null;
function apply(){{const q=document.getElementById('q').value.toLowerCase();rows.forEach(r=>{{r.style.display=(!q||r.textContent.toLowerCase().includes(q))&&(!fam||r.dataset.fam===fam)?'':'none'}});
document.querySelectorAll('.lg').forEach(b=>b.classList.toggle('on',b.dataset.f===fam));}}
document.getElementById('q').oninput=apply;
document.querySelectorAll('.lg').forEach(b=>b.onclick=()=>{{fam=fam===b.dataset.f?null:b.dataset.f;apply();
document.querySelectorAll('.b').forEach(g=>{{const c=g.querySelector('circle').getAttribute('fill');g.classList.toggle('dim',!!fam&&c!==b.style.getPropertyValue('--c').trim())}})}});
</script></body></html>"""

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", nargs="?", help="omit to pick a folder in a dialog")
    ap.add_argument("-o", "--out")
    ap.add_argument("--ai", action="store_true", help="add DeepSeek summaries (needs DEEPSEEK_API_KEY)")
    ap.add_argument("--open", action="store_true", help="open the page when done")
    ap.add_argument("--max-files", type=int, default=5000)
    ap.add_argument("--max-ai", type=int, default=60, help="how many docs get an AI summary")
    a = ap.parse_args()
    root = a.folder
    if not root:
        import tkinter, tkinter.filedialog
        tkinter.Tk().withdraw()
        root = tkinter.filedialog.askdirectory(title="Pick a folder to snapshot")
        if not root:
            sys.exit("No folder picked.")
    if not os.path.isdir(root):
        sys.exit(f"Not a folder: {root}")
    print(f"Scanning {root} …")
    files = scan(root, a.max_files)
    docs, fams, corpus = analyse(root, files)
    overview = ""
    if a.ai:
        key = os.environ.get("DEEPSEEK_API_KEY")
        if not key:
            print("DEEPSEEK_API_KEY not set; skipping AI pass.")
        else:
            print(f"Asking DeepSeek about {min(len(docs), a.max_ai)} documents …")
            overview = ai_pass(root, docs, fams, key, a.max_ai)
    out = a.out or os.path.join(root, "_FOLDER_SNAPSHOT.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(render(root, files, docs, fams, corpus, overview))
    print(f"Done: {len(files)} files, {len(docs)} docs → {out}")
    if a.open:
        os.startfile(os.path.abspath(out))

if __name__ == "__main__":
    main()
