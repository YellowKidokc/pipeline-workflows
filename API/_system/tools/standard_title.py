"""Standard title for every source in the corpus (runs FIRST, before any CKG):

    <Author code> <YYYY-MM-DD> · <Title> · <Keyword>, <Keyword>[, <Keyword>] · <Move>
    e.g.  GHabermas 2026-08-15 · Critical Scholars Date These Creeds to the 30s AD · Resurrection, Early Creeds, Pre-Pauline Tradition · Evidence

- author code: first initial + surname for a person ("Gary Habermas" -> "GHabermas"); overrides in author_codes.json
- date: YouTube upload date (yt-dlp, no API cost; stored in the note as upload_date) instead of a chapter number;
  papers use their own date field
- title: the video/paper title without the channel name, @handles and "(Audio Only)"-style noise
- keywords: 2-3 specific search topics, broadest first (never generic fields like Theology or Apologetics), reusing the
  corpus vocabulary in keyword_vocab.json so the same topic is always spelled the same
- move: what the source mainly does, one of MOVES (the classification the topics don't give)
Keywords and move come from one small DeepSeek call on the title and the opening of the source.

The note gets YAML fields std_title, author_code, upload_date, keywords, move, original_file. With --apply the file is
renamed and [[links]] to it in the same folder (the channel index) are updated. Without --apply it only prints.

    python tools/standard_title.py <note.md or folder> [...] [--apply]
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys
from pathlib import Path

API_HOME = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(API_HOME))
from engine import llm, pick                                      # noqa: E402
from engine.paths import configured, external                     # noqa: E402

MOVES = ["Evidence", "Argument", "Objection-reply", "Scholarly-survey", "Method", "Application", "Testimony", "Debate"]
GENERIC = {"theology", "apologetics", "christianity", "religion", "philosophy", "faith", "bible", "christian apologetics"}
HERE = Path(__file__).resolve().parent
CODES = HERE / "author_codes.json"
TAXONOMY = HERE / "taxonomy.json"             # master record of every classification used (source of truth)
VAULT = external("vault_root", required=False) if configured("vault_root") else None      # paths.json
MASTER_MD = VAULT / "00_CLASSIFICATION_MASTER.md" if VAULT else None                        # readable copy in the vault
NAME_KEYWORDS = 2                            # the most SPECIFIC keywords go in the file name; all of them go into the YAML
YT_PY = (external("yt_downloader") / "venv" / "Scripts" / "python.exe") if configured("yt_downloader") else Path(sys.executable)
MAX_NAME = 140                               # Windows paths stop at 260 characters; vault folders take ~110


def field(text, key):
    m = re.search(rf'^{key}:\s*"?(.*?)"?\s*$', text[:4000], re.M)
    if m:
        return m.group(1).strip()
    # Raw YouTube downloader notes use bold Markdown metadata rather than YAML,
    # for example ``**Video ID:** `abc123``` and ``**Captured:** 2026-09-27``.
    label = key.replace("_", " ")
    m = re.search(rf'^\*\*{re.escape(label)}:\*\*\s*`?(.+?)`?\s*$', text[:4000], re.M | re.I)
    return m.group(1).strip().strip("`") if m else ""


def previous_names(text) -> list[str]:
    """The note's earlier names, a JSON list (names contain commas, so never split on them)."""
    m = re.search(r"^previous_names:\s*(\[.*\])\s*$", text[:6000], re.M)
    try:
        return [str(x) for x in json.loads(m.group(1))] if m else []
    except ValueError:
        return []


def listfield(text, key):
    return [x.strip() for x in field(text, key).strip("[]").replace('"', "").split(",") if x.strip()]


def author_code(name: str) -> str:
    codes = json.loads(CODES.read_text(encoding="utf-8")) if CODES.exists() else {}
    if name in codes: return codes[name]
    words = re.findall(r"[A-Za-z][\w'-]*", name)
    if len(words) == 2 and all(w[0].isupper() for w in words): return words[0][0] + words[1]          # a person
    return "".join(w[0].upper() + w[1:] for w in words)[:16] or "Unknown"                            # a channel


def upload_date(video_id: str) -> str:
    if not video_id: return ""
    py = str(YT_PY) if YT_PY.exists() else sys.executable
    try:
        out = subprocess.run([py, "-m", "yt_dlp", "--skip-download", "--no-warnings", "--print", "upload_date",
                              f"https://www.youtube.com/watch?v={video_id}"], capture_output=True, text=True, timeout=90).stdout.strip().splitlines()
        d = out[-1] if out else ""
        return f"{d[:4]}-{d[4:6]}-{d[6:8]}" if re.fullmatch(r"\d{8}", d) else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def clean_title(title: str, author: str) -> str:
    t = re.sub(r"@[\w.-]+", "", title)
    t = re.sub(r"\((?:audio(?: only)?|official[^)]*|full[^)]*)\)", "", t, flags=re.I)
    for part in filter(None, [author, *author.split()]):
        if len(part) > 3:
            t = re.sub(rf"\s*[-–—|:]\s*(?:with\s+)?{re.escape(part)}\b.*$", "", t, flags=re.I)
            t = re.sub(rf"\s+(?:with|ft\.?|feat\.?|by)\s+{re.escape(part)}\b.*$", "", t, flags=re.I)    # "... with Gary Habermas"
    t = re.sub(r"\s+(?:with|ft\.?|feat\.?)\s*$", "", t, flags=re.I)
    t = re.sub(r"\s*:\s+", " – ", t)                                # "Title: Subtitle" keeps its break as a dash
    t = re.sub(r'[<>:"/\\|?*#^\[\]]', "", t)                     # not allowed in Windows file names or Obsidian links
    return re.sub(r"\s{2,}", " ", t).strip(" -–—·.")


def taxonomy() -> dict:
    t = json.loads(TAXONOMY.read_text(encoding="utf-8")) if TAXONOMY.exists() else {}
    for k in ("keywords", "moves", "authors"): t.setdefault(k, {})
    return t


def author_share(keyword: str, code: str, self_name: str = "") -> float:
    """Share of this author's titled notes that carry the keyword (0 until the author has 5), so a keyword on nearly
    every note of a channel (Resurrection, Minimal Facts Approach for Habermas) gives way in the file name."""
    t = taxonomy()
    mine = {n for names in t["moves"].values() for n in names if n.startswith(code + " ") and n != self_name}
    if len(mine) < 5: return 0.0
    hits = next((set(v) for k, v in t["keywords"].items() if k.lower() == keyword.lower()), set())
    return len(hits & mine) / len(mine)


def vocab() -> list[str]:
    return sorted(taxonomy()["keywords"])


def remember(name: str, keys: list[str], move: str, code: str, author: str, old: str = "") -> None:
    """Record every classification used, then rewrite the master record in the vault."""
    t = taxonomy()
    for bucket in ("keywords", "moves"):                    # a retitled note drops its previous entries first
        for term in list(t[bucket]):
            t[bucket][term] = [n for n in t[bucket][term] if n not in (name, old)]
            if not t[bucket][term]: del t[bucket][term]
    for bucket, terms in (("keywords", keys), ("moves", [move])):
        for term in terms:
            match = next((k for k in t[bucket] if k.lower() == term.lower()), term)
            t[bucket].setdefault(match, [])
            if name not in t[bucket][match]: t[bucket][match].append(name)
    t["authors"][code] = author
    TAXONOMY.write_text(json.dumps(t, indent=1, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    write_master(t)


def write_master(t: dict) -> None:
    link = lambda n: f"[[{n}\\|{' '.join(n.split(' ')[:2])}]]"        # shown as "GHabermas 2026-09-12"; \| because it sits in a table
    L = ["# Classification master record", "",
         "Every classification the corpus uses, rebuilt each time a source is titled (tools/standard_title.py; data: "
         "API_ALL/API_HOME/tools/taxonomy.json). The tagger is told to reuse these terms, so over time this becomes the "
         "fixed vocabulary the whole corpus works within.", "",
         "## Rules", "",
         "- File name: `<Author code> <YYYY-MM-DD> · <Title> · <Keyword>, <Keyword> · <Move>`; all keywords are in the note's YAML.",
         "- Keywords: specific search topics, broadest first, Title Case, 1-3 words. Never generic fields: " + ", ".join(sorted(GENERIC)) + ".",
         "- Move: what the source mainly does. One of: " + ", ".join(MOVES) + ".",
         "- Author code: first initial + surname for a person; overrides in tools/author_codes.json.", "",
         f"## Keywords ({len(t['keywords'])})", "", "| Keyword | Sources | Examples |", "|---|---:|---|"]
    for k, names in sorted(t["keywords"].items(), key=lambda kv: (-len(kv[1]), kv[0].lower())):
        L.append(f"| {k} | {len(names)} | {' · '.join(link(n) for n in names[:3])}{' …' if len(names) > 3 else ''} |")
    L += ["", f"## Moves ({len(t['moves'])} of {len(MOVES)} in use)", "", "| Move | Sources |", "|---|---:|"]
    for m in MOVES: L.append(f"| {m} | {len(t['moves'].get(m, []))} |")
    L += ["", "## Author codes", "", "| Code | Author / channel |", "|---|---|"]
    for c, a in sorted(t["authors"].items()): L.append(f"| {c} | {a} |")
    if not MASTER_MD: return print("  (master record not written: vault_root is not set in paths.json)")
    try: MASTER_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    except OSError as exc: print(f"  (master record not written: {exc})")


PROMPT = """Tag this source for search in a research corpus about Christianity, physics and philosophy.
KEYWORDS: 2 or 3 specific topics someone would actually search for, broadest first, most specific last
(e.g. Resurrection, Early Creeds, Pre-Pauline Tradition). Never use generic fields such as Theology, Apologetics,
Christianity, Religion or Philosophy, never the author's or channel's name, and never a metaphor or image the
speaker uses (a topic, not a figure of speech). Title Case, 1-3 words each.
Reuse a term from KNOWN KEYWORDS whenever one fits, spelled exactly as listed.
MOVE: exactly one of {moves}: what the source mainly DOES.
{extra}Return JSON only: {{"keywords": ["..."], "move": "..."{extra_json}}}

AUTHOR: {author}
KNOWN KEYWORDS: {known}
TITLE: {title}

OPENING OF THE SOURCE:
{opening}"""


SLUG = re.compile(r"[a-z0-9]+(?:[-_][a-z0-9]+)+")                 # a file name, not a title: bgl-02-who-did-jesus-save
SERIES = re.compile(r"^([a-z]{2,6})[-_](\d{1,3})[-_]", re.I)       # series code + part: bgl-02-...
ASK_TITLE = ("TITLE is a file name, not a title. Also return \"title\": a proper title for this piece in Title Case, "
             "taken from the source (its own heading or its main question), at most 10 words.\n")
ASK_SERIES = ("It is part {part} of a series with the code {code}. Also return \"series\": the series' full name in "
              "Title Case (usually the title of part 1).{known}\n")


def tag(title: str, body: str, author: str, want_title: bool = False, series: tuple | None = None) -> dict:
    """One small call: keywords and move, plus a proper title and the series name when the title is a file name."""
    extra, extra_json = "", ""
    if want_title:
        extra += ASK_TITLE; extra_json += ', "title": "..."'
    if series:
        code, part, known = series
        extra += ASK_SERIES.format(part=part, code=code, known=f" It is already known as: {known}." if known else "")
        extra_json += ', "series": "..."'
    prompt = PROMPT.format(moves=", ".join(MOVES), author=author, known=", ".join(vocab()) or "(none yet)",
                           title=title, opening=" ".join(body.split()[:1200]), extra=extra, extra_json=extra_json)
    r = llm.call([{"role": "user", "content": prompt}], json_mode=True, max_tokens=300, temperature=0.1)
    try:
        d = json.loads(r.text)
    except (ValueError, AttributeError):
        d = {}
    keys = [str(k).strip() for k in d.get("keywords", []) if str(k).strip() and str(k).strip().lower() not in GENERIC][:3]
    return {"keywords": keys, "move": d.get("move") if d.get("move") in MOVES else "Argument",
            "title": str(d.get("title") or "").strip(), "series": str(d.get("series") or "").strip()}


def keywords_and_move(title: str, body: str, author: str) -> tuple[list[str], str]:
    d = tag(title, body, author)
    return d["keywords"], d["move"]


def set_yaml(text: str, values: dict) -> str:
    if not text.startswith("---"): text = "---\n---\n" + text           # a paper with no front matter gets one
    end = text.index("\n---", 3)
    head, rest = text[:end], text[end:]
    for k, v in values.items():
        line = f"{k}: {json.dumps(v, ensure_ascii=False)}"
        if re.search(rf"^{k}:", head, re.M):
            head = re.sub(rf"^{k}:.*$", lambda _: line, head, count=1, flags=re.M)
        else:
            head += "\n" + line
    return head + rest


def process(note: Path, apply: bool) -> str:
    text = note.read_text(encoding="utf-8")
    author = (field(text, "author") or field(text, "channel") or field(text, "by")
              or (note.parent.name if field(text, "video_id") else "")
              or ("David Lowe" if re.search(r"David Lowe|POF 2828", text[:3000]) or not field(text, "video_id") else "Unknown"))
    # a source with no author and no video is one of David's own papers
    code = author_code(author)
    date = (field(text, "upload_date") or upload_date(field(text, "video_id"))
            or next((field(text, k)[:10] for k in ("date", "assembled", "published", "captured_at", "created", "downloaded")
                     if re.match(r"\d{4}-\d{2}-\d{2}", field(text, k))), "")
            or __import__("datetime").date.fromtimestamp(note.stat().st_mtime).isoformat())
    h1 = re.search(r"^#\s+(.+)$", text.split("\n---", 2)[-1] if text.startswith("---") else text, re.M)
    # the name the source came with; never the standard name we gave it (a rerun would title the title)
    raw = field(text, "title") or (h1.group(1) if h1 else "") or Path(field(text, "original_file") or note.name).stem
    title = field(text, "doc_title") or clean_title(raw, author)
    keys, move = listfield(text, "keywords"), field(text, "move")
    sm = SERIES.match(raw)
    series_code, part = (sm.group(1).upper(), int(sm.group(2))) if sm else ("", 0)
    series = field(text, "series") or (taxonomy().get("series", {}).get(series_code, "") if series_code else "")
    need_title = not field(text, "doc_title") and bool(SLUG.fullmatch(raw))
    if not keys or not move or need_title or (series_code and not series):
        body = text.split("## Transcript", 1)[-1] if "## Transcript" in text else text
        d = tag(title, body, author, want_title=need_title,
                series=(series_code, part, series) if series_code and not series else None)
        keys, move = (keys, move) if keys and move else (d["keywords"], d["move"])
        if need_title and d["title"]:
            title = clean_title(d["title"], author)
        series = series or d["series"]
    # the name shows keywords the title doesn't already say; the title wins the space, so drop to one keyword before cutting it
    shown = [k for k in keys if k.lower() not in title.lower()] or keys
    shown.sort(key=lambda k: author_share(k, code, field(text, "std_title")) >= 0.4)   # stable: rare-for-this-author first
    for n in range(NAME_KEYWORDS, 0, -1):
        tail = f" · {', '.join(shown[:n])} · {move}"
        room = MAX_NAME - len(f"{code} {date} · ") - len(tail) - 3
        if len(title) <= room: break
    short = title
    if len(title) > room:
        short = title[:room].rsplit(" ", 1)[0]
        if short.count("(") > short.count(")"): short = short[:short.rindex("(")]   # never leave "(Pt.…"
        short = short.rstrip(" -–—,:;") + "…"
    label = f"{series_code} {part:02d} · " if series_code else ""
    std = f"{code} {date} · {label}{short}{tail}"
    home = note.parent
    folder_name = re.sub(r'[<>:"/\\|?*]', "", series).strip() if series else ""
    if folder_name and home.name != folder_name:                     # a series gets its own folder (David)
        home = home / folder_name
    new = home / (std + ".md")
    if apply and new != note and new.exists():
        return f"CLASH {note.name} -> {new.name} (a note with that name exists; left as is)"
    if apply:
        remember(new.stem, keys, move, code, author, old=field(text, "std_title"))
        values = {"std_title": std, "doc_title": title, "author_code": code, "upload_date": date, "keywords": keys,
                  "move": move, "original_file": field(text, "original_file") or note.name}
        if new.stem != note.stem:                                     # results made under an earlier name stay findable
            values["previous_names"] = list(dict.fromkeys(previous_names(text) + [note.stem]))
        if series_code:
            values.update({"series": series, "series_code": series_code, "part": part})
            t = taxonomy(); t.setdefault("series", {}).setdefault(series_code, series)   # first name seen wins
            TAXONOMY.write_text(json.dumps(t, indent=1, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        text = set_yaml(text, values)
        note.write_text(text, encoding="utf-8")
        if new != note:
            new.parent.mkdir(exist_ok=True)
            note.rename(new)
            listing = pick.pick_file_for(new)                               # a channel's _PICK.md sits above Clean MD
            for other in [*note.parent.glob("*.md"), *([listing] if listing and listing.parent != note.parent else [])]:
                # keep [[links]] in the channel index and the pick list working
                t = other.read_text(encoding="utf-8")
                t2 = t.replace(f"[[{note.stem}|", f"[[{new.stem}|").replace(f"[[{note.stem}]]", f"[[{new.stem}]]")
                if t2 != t: other.write_text(t2, encoding="utf-8")
    return str(new.relative_to(note.parent)) if new.parent != note.parent else new.name


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("items", nargs="+"); p.add_argument("--apply", action="store_true")
    p.add_argument("--all", action="store_true", help="ignore _PICK.md and title every note in the folders (cheap: ~1.5k tokens each)")
    a = p.parse_args()
    if a.all:
        notes = [n for raw in a.items for n in (pick.notes(Path(raw)) if Path(raw).is_dir() else [Path(raw)])]
    else:
        notes = pick.resolve(a.items)               # folders obey their _PICK.md, like every API station
    llm.configure(1)                  # one at a time, so each note sees the keywords the previous one added
    clashes = 0
    for n in notes:
        r = process(n, a.apply); print(r, flush=True)
        clashes += r.startswith("CLASH")
    return 1 if clashes else 0


if __name__ == "__main__":
    raise SystemExit(main())
