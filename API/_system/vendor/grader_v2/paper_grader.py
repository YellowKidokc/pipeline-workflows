#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PAPER GRADER — CKG_EVIDENCE station
L15 Atom Analytics: text stream + CKG atom stream (spec: ANALYTICS_QUESTIONS.md)

Pure Python, standard library only. No API calls, no paid providers.

Drop papers (.md / .markdown / .txt) into
    STATIONS/PAPER_GRADER/INBOX/01_PRIORITY | 02_SERIES/<series name> | 03_GENERAL
00_WAITING_NOT_PROCESSED is skipped unless --include-waiting.

For each paper it writes a Markdown report and a JSON record into STATIONS/PAPER_GRADER/OUTBOX,
then rebuilds the master index and a corpus report across everything graded so far.
If the same paper has already been through CKG_EVIDENCE, its CKG v3.1 JSON record is read too.

Every number here measures structure, coverage and connection. None of it is a truth ruling.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import math
import re
import shutil
import sys
import traceback
import uuid
from collections import Counter, defaultdict
from pathlib import Path

GRADER_VERSION = "paper_grader 0.2.0"

# Same namespace and formula as the CKG runner (ckg.py: uid('paper-version:' + sha256)),
# so every station derives the identical paper UUID from the same source bytes.
CKG_NAMESPACE = uuid.UUID("8121b19c-b135-4b14-ae07-806757692169")


def paper_uuid_for(sha: str) -> str:
    return str(uuid.uuid5(CKG_NAMESPACE, "paper-version:" + sha))

SCRIPTS_DIR = Path(__file__).resolve().parent
MAIN_DIR = SCRIPTS_DIR.parents[1]          # SCRIPTS lives in MAIN\PYTHON
STATION_DIR = MAIN_DIR / "PYTHON"
BACK_DIR = MAIN_DIR / "_BACKSIDE" / "PYTHON"
CKG_RECORDS = MAIN_DIR / "_BACKSIDE" / "CKG_EVIDENCE" / "SYSTEM" / "RECORDS"
sys.path.insert(0, str(MAIN_DIR / "_BACKSIDE" / "SCRIPTS"))   # shared: uuid_registry
try:
    import uuid_registry  # the one place paper UUIDs are minted
except Exception:  # grader still runs without the registry; paper_uuid falls back to the version UUID
    uuid_registry = None

INBOX_LANES = ["00_WAITING_NOT_PROCESSED", "01_PRIORITY", "02_SERIES", "03_GENERAL", "04_DUPLICATES"]
ACTIVE_LANES = ["01_PRIORITY", "02_SERIES", "03_GENERAL"]
# PYTHON works piece by piece: one report per paper plus the corpus report — no classification views.
OUTBOX_LANES = ["01_ALL_PAPERS"]
PAPER_EXTS = {".md", ".markdown", ".txt"}
STATE_FILE = "00_GRADER_STATE.json"
INDEX_FILE = "00_MASTER_INDEX.csv"

BOUNDARY = ("Python-only structural analysis — no AI calls. Every number measures structure, "
            "coverage and connection; none is a truth ruling. Candidate outputs wait for a human ruling.")


# ───────────────────────────── basic utilities ─────────────────────────────

def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def safe_name(s: str, limit: int = 80) -> str:
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", s)
    s = re.sub(r"\s+", " ", s).strip(" ._")
    return (s[:limit].rstrip(" ._")) or "untitled"


def read_text(path: Path):
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig", errors="replace")
    return raw, text.replace("\r\n", "\n").replace("\r", "\n")


def snippet(s: str, n: int = 240) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def clean_inline(s: str) -> str:
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", lambda m: m.group(2) or m.group(1), s)
    s = re.sub(r"[*_`]+", "", s)
    return re.sub(r"\s+", " ", s).strip()


WORD_RE = re.compile(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'’\-]*|\d+(?:\.\d+)?")
SENT_SPLIT = re.compile(r"(?<=[.!?])[\"'”’)\]]*\s+(?=[\"'“‘(\[]?[A-Z0-9])")

STOPWORDS = set("""a about above after again against all also am an and any are as at be because been before being
below between both but by can cannot could did do does doing down during each few for from further had has have
having he her here hers herself him himself his how i if in into is it its itself just let me more most my myself no
nor not now of off on once only or other ought our ours ourselves out over own same she should so some such than that
the their theirs them themselves then there these they this those through to too under until up upon very was we were
what when where which while who whom why will with would you your yours yourself yourselves one two three also may
might must shall every each within without across among per via like just even still yet thus hence therefore however
into onto because since whether either neither though although rather quite much many more most less least well
""".split())


def sentences_of(block: str):
    return [x.strip() for x in SENT_SPLIT.split(block) if len(x.strip()) > 1]


def syllables(word: str) -> int:
    w = word.lower().strip("'’-")
    if not w or not w[0].isalpha():
        return 1
    if len(w) <= 3:
        return 1
    w = re.sub(r"(?:[^laeiouy]es|ed|[^laeiouy]e)$", "", w)
    w = re.sub(r"^y", "", w)
    return max(1, len(re.findall(r"[aeiouy]{1,2}", w)))


# ───────────────────────────── document parsing ─────────────────────────────

FM_RE = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.S)


def split_frontmatter(text: str):
    m = FM_RE.match(text)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def frontmatter_info(fm: str) -> dict:
    keys = re.findall(r"^([A-Za-z_][\w\-]*)[ \t]*:", fm, re.M)
    c = Counter(keys)
    vals = {}
    for k in ("title", "series", "domain", "domain_primary", "project", "register", "register_type",
              "type", "content_type"):
        m = re.search(rf"^{k}[ \t]*:[ \t]*(.+)$", fm, re.M)
        if m:
            v = m.group(1).split(" #")[0].strip().strip('"').strip("'")
            if v and v not in ("null", "~", "[]", "{}"):
                vals[k] = v
    return {"present": bool(fm), "keys": len(c),
            "duplicate_keys": sorted(k for k, n in c.items() if n > 1), "values": vals}


def extract_original(text: str):
    m = re.search(r"<!--\s*PAPER_SECTION:[^\n>]*?:ORIGINAL:BEGIN\s*-->\n?(.*?)"
                  r"<!--\s*PAPER_SECTION:[^\n>]*?:ORIGINAL:END\s*-->", text, re.S)
    if m:
        return m.group(1), "PAPER_SECTION ORIGINAL markers"
    m = re.search(r"<!--[^\n>]*ORIGINAL ARTICLE BELOW[^\n>]*-->\n?", text)
    if m:
        rest = text[m.end():]
        cut = re.search(r"\n#\s*▼\s*CLASSIFICATION LAYER", rest)
        if cut:
            rest = rest[:cut.start()]
        return rest, "ORIGINAL ARTICLE BELOW marker"
    return None, None


def strip_for_prose(body: str) -> str:
    t = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    t = re.sub(r"\$\$.*?\$\$", " ", t, flags=re.S)
    return t


def prose_blocks(body: str):
    """Prose paragraphs: blockquote/callout text kept, headings/tables/rules dropped."""
    t = strip_for_prose(body)
    blocks = []
    for blk in re.split(r"\n\s*\n", t):
        lines = []
        for ln in blk.split("\n"):
            s = re.sub(r"^(>\s*)+", "", ln.strip())
            if not s:
                continue
            if s.startswith("|") or re.match(r"^#{1,6}\s", s) or re.match(r"^\[!\w+\][-+]?\s*\S{0,60}$", s) \
                    or re.match(r"^[-*_]{3,}$", s):
                continue
            s = re.sub(r"^\[!\w+\][-+]?\s*", "", s)
            s = re.sub(r"^([-*+]|\d+[.)])\s+", "", s)
            lines.append(s)
        if lines:
            blocks.append(" ".join(lines))
    return blocks


def parse_tables(md: str):
    tables = []
    lines = md.split("\n")
    strip_q = lambda x: re.sub(r"^(>\s*)+", "", x.strip())
    i = 0
    while i < len(lines):
        ln = strip_q(lines[i])
        nxt = strip_q(lines[i + 1]) if i + 1 < len(lines) else ""
        if ln.startswith("|") and re.match(r"^\|?\s*:?-{3,}", nxt):
            headers = [c.strip() for c in ln.strip().strip("|").split("|")]
            rows, j = [], i + 2
            while j < len(lines):
                r = strip_q(lines[j])
                if not r.startswith("|"):
                    break
                rows.append([c.strip() for c in r.strip().strip("|").split("|")])
                j += 1
            tables.append({"headers": headers, "rows": rows, "line": i + 1})
            i = j
            continue
        i += 1
    return tables


def readability(blocks):
    words = sents = syl = 0
    for b in blocks:
        b2 = clean_inline(b)
        ss = sentences_of(b2) or [b2]
        sents += len(ss)
        ws = WORD_RE.findall(b2)
        words += len(ws)
        syl += sum(syllables(w) for w in ws if w[0].isalpha())
    if words == 0 or sents == 0:
        return None
    wps, spw = words / sents, syl / words
    return {"words": words, "sentences": sents, "avg_sentence_words": round(wps, 1),
            "flesch_kincaid_grade": round(0.39 * wps + 11.8 * spw - 15.59, 1),
            "flesch_reading_ease": round(206.835 - 1.015 * wps - 84.6 * spw, 1)}


# ───────────────────────────── vocabularies ─────────────────────────────
# (pattern, family, case_sensitive)
TERMS = {
    "χ (chi)": (r"χ|\bchi\b", "FRAMEWORK", False),
    "Master Equation": (r"\bmaster equation\b", "FRAMEWORK", False),
    "Logos": (r"\blogos\b", "FRAMEWORK", False),
    "coherence": (r"\bcoheren(?:ce|t)\b", "FRAMEWORK", False),
    "decoherence": (r"\bdecoheren(?:ce|t)\b", "FRAMEWORK", False),
    "Ten Laws": (r"\bten (?:universal )?laws\b", "FRAMEWORK", False),
    "Theophysics": (r"\btheophysic", "FRAMEWORK", False),
    "Fruits of the Spirit": (r"\bfruits? of the spirit\b", "FRAMEWORK", False),
    "moral conservation": (r"\bmoral conservation\b", "FRAMEWORK", False),
    "Principia Mathematica Moralia": (r"\bprincipia (?:mathematica )?moralia\b", "FRAMEWORK", False),
    "7-Question method": (r"\b(?:7|seven)[- ]?q(?:uestion)?s?\b", "FRAMEWORK", False),
    "BC1 (terminal observer)": (r"\bBC1\b", "FRAMEWORK", True),
    "God": (r"\bgod\b", "THEOLOGY", False),
    "Christ / Jesus": (r"\bchrist\b|\bjesus\b", "THEOLOGY", False),
    "Trinity": (r"\btrinit(?:y|arian)\b", "THEOLOGY", False),
    "grace": (r"\bgrace\b", "THEOLOGY", False),
    "sin": (r"\bsin(?:s|ful|ner|ners)?\b", "THEOLOGY", False),
    "faith": (r"\bfaith\b", "THEOLOGY", False),
    "love / agapē": (r"\bagap[eē]\b|\blove\b", "THEOLOGY", False),
    "atonement": (r"\batonement\b", "THEOLOGY", False),
    "resurrection": (r"\bresurrect", "THEOLOGY", False),
    "Holy Spirit": (r"\bholy spirit\b", "THEOLOGY", False),
    "creation": (r"\bcreation\b|\bcreator\b", "THEOLOGY", False),
    "covenant": (r"\bcovenant", "THEOLOGY", False),
    "incarnation": (r"\bincarnat", "THEOLOGY", False),
    "repentance": (r"\brepent", "THEOLOGY", False),
    "righteousness / justice": (r"\brighteous|\bjustice\b", "THEOLOGY", False),
    "mercy": (r"\bmercy\b", "THEOLOGY", False),
    "Scripture": (r"\bscriptur|\bbiblical\b|\bbible\b", "THEOLOGY", False),
    "entropy": (r"\bentrop", "PHYSICS", False),
    "quantum": (r"\bquantum\b", "PHYSICS", False),
    "superposition": (r"\bsuperposition", "PHYSICS", False),
    "entanglement": (r"\bentangle", "PHYSICS", False),
    "measurement": (r"\bmeasurement", "PHYSICS", False),
    "collapse": (r"\bcollapse", "PHYSICS", False),
    "gravity": (r"\bgravit", "PHYSICS", False),
    "relativity": (r"\brelativit", "PHYSICS", False),
    "thermodynamics": (r"\bthermodynamic", "PHYSICS", False),
    "electromagnetism": (r"\belectromagnet", "PHYSICS", False),
    "strong force": (r"\bstrong (?:nuclear )?force\b", "PHYSICS", False),
    "weak force": (r"\bweak (?:nuclear )?force\b", "PHYSICS", False),
    "Hamiltonian": (r"\bhamiltonian\b", "PHYSICS", False),
    "Lagrangian": (r"\blagrangian\b", "PHYSICS", False),
    "Noether": (r"\bnoether", "PHYSICS", False),
    "symmetry": (r"\bsymmetr", "PHYSICS", False),
    "spacetime": (r"\bspace-?time\b", "PHYSICS", False),
    "observer": (r"\bobserver", "PHYSICS", False),
    "Schrödinger": (r"\bschr[öo]e?dinger\b", "PHYSICS", False),
    "theorem": (r"\btheorem", "MATH_FORMAL", False),
    "proof": (r"\bproofs?\b|\bprove[sdn]?\b", "MATH_FORMAL", False),
    "axiom": (r"\baxiom", "MATH_FORMAL", False),
    "Lean": (r"\bLean\b", "MATH_FORMAL", True),
    "Gödel": (r"\bg[öo]del\b", "MATH_FORMAL", False),
    "isomorphism": (r"\bisomorph", "MATH_FORMAL", False),
    "operator": (r"\boperators?\b", "MATH_FORMAL", False),
    "Z3": (r"\bZ3\b", "MATH_FORMAL", True),
    "information": (r"\binformation\b", "INFORMATION", False),
    "Shannon": (r"\bshannon\b", "INFORMATION", False),
    "channel capacity": (r"\bchannel capacity\b", "INFORMATION", False),
    "integrated information (Φ)": (r"\bintegrated information\b|Φ", "INFORMATION", False),
}
TERM_RES = {k: re.compile(p, 0 if cs else re.I) for k, (p, fam, cs) in TERMS.items()}
TERM_FAMILY = {k: fam for k, (p, fam, cs) in TERMS.items()}

# Canonical law numbering — NT Spiritual Terms canonical reference (Apr 19, 2026).
# The law-ordering conflict (Weak Force at 4 vs 9) is still an open ruling; this table follows the Apr 19 sheet.
LAW_CANON = {
    1: ("Gravitation / GR", r"gravit|general relativity|\bGR\b"),
    2: ("Motion (F=ma)", r"\bmotion\b|F\s*=\s*ma|newton"),
    3: ("Electromagnetism", r"electromagnet|maxwell"),
    4: ("Strong Force", r"strong (?:nuclear )?force|yukawa"),
    5: ("Thermodynamics", r"thermodynamic|entrop"),
    6: ("Information / Shannon", r"\binformation\b|shannon"),
    7: ("Quantum", r"quantum"),
    8: ("Relativity", r"(?<!general )relativit|lorentz"),
    9: ("Weak Force", r"weak (?:nuclear )?force|noether|parity"),
    10: ("Coherence", r"\bcoheren"),
}
LAW_RES = {n: re.compile(p, re.I) for n, (name, p) in LAW_CANON.items()}
LAW_MENTION = re.compile(r"\bLaw\s*#?\s*(\d{1,2})\b")

BOOKS = [
    ("Genesis", ["Genesis", "Gen"]), ("Exodus", ["Exodus", "Exod", "Ex"]), ("Leviticus", ["Leviticus", "Lev"]),
    ("Numbers", ["Numbers", "Num"]), ("Deuteronomy", ["Deuteronomy", "Deut"]), ("Joshua", ["Joshua", "Josh"]),
    ("Judges", ["Judges", "Judg"]), ("Ruth", ["Ruth"]), ("Samuel", ["Samuel", "Sam"]), ("Kings", ["Kings", "Kgs"]),
    ("Chronicles", ["Chronicles", "Chron", "Chr"]), ("Ezra", ["Ezra"]), ("Nehemiah", ["Nehemiah", "Neh"]),
    ("Esther", ["Esther", "Esth"]), ("Job", ["Job"]), ("Psalms", ["Psalms", "Psalm", "Pss", "Ps"]),
    ("Proverbs", ["Proverbs", "Prov"]), ("Ecclesiastes", ["Ecclesiastes", "Eccles", "Eccl"]),
    ("Song of Songs", ["Song of Songs", "Song of Solomon"]), ("Isaiah", ["Isaiah", "Isa"]),
    ("Jeremiah", ["Jeremiah", "Jer"]), ("Lamentations", ["Lamentations", "Lam"]), ("Ezekiel", ["Ezekiel", "Ezek"]),
    ("Daniel", ["Daniel", "Dan"]), ("Hosea", ["Hosea", "Hos"]), ("Joel", ["Joel"]), ("Amos", ["Amos"]),
    ("Obadiah", ["Obadiah", "Obad"]), ("Jonah", ["Jonah"]), ("Micah", ["Micah", "Mic"]), ("Nahum", ["Nahum", "Nah"]),
    ("Habakkuk", ["Habakkuk", "Hab"]), ("Zephaniah", ["Zephaniah", "Zeph"]), ("Haggai", ["Haggai", "Hag"]),
    ("Zechariah", ["Zechariah", "Zech"]), ("Malachi", ["Malachi", "Mal"]), ("Matthew", ["Matthew", "Matt", "Mt"]),
    ("Mark", ["Mark", "Mk"]), ("Luke", ["Luke", "Lk"]), ("John", ["John", "Jn"]), ("Acts", ["Acts"]),
    ("Romans", ["Romans", "Rom"]), ("Corinthians", ["Corinthians", "Cor"]), ("Galatians", ["Galatians", "Gal"]),
    ("Ephesians", ["Ephesians", "Eph"]), ("Philippians", ["Philippians", "Phil"]),
    ("Colossians", ["Colossians", "Col"]), ("Thessalonians", ["Thessalonians", "Thess"]),
    ("Timothy", ["Timothy", "Tim"]), ("Titus", ["Titus"]), ("Philemon", ["Philemon", "Phlm"]),
    ("Hebrews", ["Hebrews", "Heb"]), ("James", ["James", "Jas"]), ("Peter", ["Peter", "Pet"]), ("Jude", ["Jude"]),
    ("Revelation", ["Revelation", "Rev"]),
]
BOOK_ALIAS = {a: canon for canon, aliases in BOOKS for a in aliases}
SCRIPTURE_RE = re.compile(
    r"\b(?:(?P<num>[123]|III|II|I)\s*)?(?P<book>"
    + "|".join(re.escape(a) for a in sorted(BOOK_ALIAS, key=len, reverse=True))
    + r")\.?\s+(?P<ch>\d{1,3}):(?P<v>\d{1,3})(?:\s*[–-]\s*(?P<v2>\d{1,3}))?")
ROMAN = {"I": "1", "II": "2", "III": "3"}

# (pattern, category) — case-sensitive
WITNESSES = {
    "Augustine": (r"\bAugustine\b", "historical witness"),
    "Aquinas": (r"\bAquinas\b", "historical witness"),
    "Boethius": (r"\bBoethius\b", "historical witness"),
    "Anselm": (r"\bAnselm\b", "historical witness"),
    "Athanasius": (r"\bAthanasius\b", "historical witness"),
    "Irenaeus": (r"\bIrenaeus\b", "historical witness"),
    "Origen": (r"\bOrigen\b", "historical witness"),
    "Tertullian": (r"\bTertullian\b", "historical witness"),
    "Gregory of Nyssa": (r"\bGregory of Nyssa\b", "historical witness"),
    "Basil": (r"\bBasil(?: the Great)?\b", "historical witness"),
    "Chrysostom": (r"\bChrysostom\b", "historical witness"),
    "Maximus the Confessor": (r"\bMaximus\b", "historical witness"),
    "Pseudo-Dionysius": (r"\bDionysius\b", "historical witness"),
    "Bonaventure": (r"\bBonaventure\b", "historical witness"),
    "Duns Scotus": (r"\bScotus\b", "historical witness"),
    "Pascal": (r"\bPascal\b", "historical witness"),
    "Calvin": (r"\bCalvin\b", "historical witness"),
    "Luther": (r"\bLuther\b", "historical witness"),
    "Kierkegaard": (r"\bKierkegaard\b", "historical witness"),
    "Jonathan Edwards": (r"\bJonathan Edwards\b", "historical witness"),
    "C. S. Lewis": (r"\bC\.\s?S\.\s?Lewis\b", "historical witness"),
    "Plato": (r"\bPlato\b", "philosophical witness"),
    "Aristotle": (r"\bAristotle\b", "philosophical witness"),
    "Plotinus": (r"\bPlotinus\b", "philosophical witness"),
    "Leibniz": (r"\bLeibniz\b", "philosophical witness"),
    "Descartes": (r"\bDescartes\b", "philosophical witness"),
    "Kant": (r"\bKant\b", "philosophical witness"),
    "Berkeley": (r"\bBerkeley\b", "philosophical witness"),
    "Newton": (r"\bNewton\b", "scientific / mathematical"),
    "Einstein": (r"\bEinstein\b", "scientific / mathematical"),
    "Bohr": (r"\bBohr\b", "scientific / mathematical"),
    "Heisenberg": (r"\bHeisenberg\b", "scientific / mathematical"),
    "Schrödinger": (r"\bSchr[öo]e?dinger\b", "scientific / mathematical"),
    "Dirac": (r"\bDirac\b", "scientific / mathematical"),
    "Bell": (r"\bBell(?:'s|’s|\s+(?:\(|19|20|test|inequalit|theorem))", "scientific / mathematical"),
    "Aspect": (r"\bAspect(?:'s|’s|\s+(?:et al|\(|19|20|and|experiment))", "scientific / mathematical"),
    "Wheeler": (r"\bWheeler\b", "scientific / mathematical"),
    "von Neumann": (r"\bvon Neumann\b", "scientific / mathematical"),
    "Gödel": (r"\bG[öo]del\b", "scientific / mathematical"),
    "Tarski": (r"\bTarski\b", "scientific / mathematical"),
    "Turing": (r"\bTuring\b", "scientific / mathematical"),
    "Shannon": (r"\bShannon\b", "scientific / mathematical"),
    "Noether": (r"\bNoether\b", "scientific / mathematical"),
    "Maxwell": (r"\bMaxwell\b", "scientific / mathematical"),
    "Boltzmann": (r"\bBoltzmann\b", "scientific / mathematical"),
    "Planck": (r"\bPlanck\b", "scientific / mathematical"),
    "Feynman": (r"\bFeynman\b", "scientific / mathematical"),
    "Hawking": (r"\bHawking\b", "scientific / mathematical"),
    "Penrose": (r"\bPenrose\b", "scientific / mathematical"),
    "Zurek": (r"\bZurek\b", "scientific / mathematical"),
    "Landauer": (r"\bLandauer\b", "scientific / mathematical"),
    "Lawvere": (r"\bLawvere\b", "scientific / mathematical"),
    "Cantor": (r"\bCantor\b", "scientific / mathematical"),
    "Hilbert": (r"\bHilbert\b", "scientific / mathematical"),
    "Wigner": (r"\bWigner\b", "scientific / mathematical"),
    "Tononi": (r"\bTononi\b", "scientific / mathematical"),
}
WITNESS_RES = {k: re.compile(p) for k, (p, c) in WITNESSES.items()}

STRONG_RE = re.compile(
    r"\b(prove[sd]?|proven|proof that|necessitat\w*|definitively|conclusively|settled|undeniabl\w*|"
    r"irrefutabl\w*|unquestionabl\w*|beyond (?:any )?doubt|certainly|guarantee[sd]?|the only|"
    r"(?:lean|machine)[- ]verified|verified in lean|formally verified)\b", re.I)
HEDGE_RE = re.compile(
    r"\b(may|might|could|suggests?|appears?|likely|possibly|perhaps|proposed?|candidate|conjectur\w*|"
    r"hypothes\w*|tentative\w*|provisional\w*)\b", re.I)
VERIFY_CLAIM_RE = re.compile(
    r"(?i)((?:lean|machine)[- ]?(?:4 )?verified|verified in lean|formally verified|zero[- ]sorry|"
    r"compiles?\s+(?:clean|with zero)|lake build|z3[- ](?:verified|checked|proved))")
ARG_RE = re.compile(r"\b(therefore|thus|hence|it follows|consequently|because|since|so that|implies|entails)\b", re.I)
OBJECTION_RE = re.compile(
    r"(/EAST\b|\bobjection|\bobject that\b|\bcritics?\b|\brival\b|\bcounter-?argument|\bskeptic|"
    r"\bone might (?:say|object|argue)|\bopponents?\b)", re.I)
FALSIFY_RE = re.compile(
    r"(?i)\b(falsif\w*|refut\w*|kill condition|defeat condition|would (?:break|fail|be false|refute|falsify)|"
    r"breaks if|testable|we predict|predicts?|prediction\w*)\b")
BRIDGE_RE = re.compile(
    r"(?i)(\bmaps? (?:onto|to)\b|\bcorresponds? to\b|\bcorrespondence\b|\bisomorphi\w*|\bhomomorphi\w*|"
    r"\bstructural(?:ly)? (?:parallel|identical|same|isomorph\w*)|\bmirrors?\b|\banalog(?:y|ies|ous|ue)\b|"
    r"\bdual projection|\bsame (?:equation|structure|shape)\b|↔|⟷|<->)")
SIGMA_RE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:σ|sigma\b)", re.I)
PVAL_RE = re.compile(r"\bp\s*[<=≤]\s*0?\.\d+", re.I)
CITE_RES = [
    re.compile(r"\(([A-Z][A-Za-z'’\-]+(?:\s+et al\.?)?(?:\s*(?:&|and)\s*[A-Z][A-Za-z'’\-]+)?),?\s+"
               r"((?:1[5-9]|20)\d\d)[a-z]?\)"),
    re.compile(r"\b([A-Z][A-Za-z'’\-]+(?:\s+et al\.?)?)\s+\(((?:1[5-9]|20)\d\d)[a-z]?\)"),
    re.compile(r"\b([A-Z][A-Za-z'’\-]+\s+et al\.?),?\s+((?:1[5-9]|20)\d\d)\b"),
]
DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s)\]>]+")
URL_RE = re.compile(r"https?://[^\s)\]>]+")

GREEK = "αβγδεζηθικλμνξοπρστυφχψωΓΔΘΛΞΠΣΦΨΩℏ∂∇∫∑√∞"
LATEX_GREEK = {"alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ε", "zeta": "ζ", "eta": "η",
               "theta": "θ", "kappa": "κ", "lambda": "λ", "mu": "μ", "nu": "ν", "xi": "ξ", "pi": "π", "rho": "ρ",
               "sigma": "σ", "tau": "τ", "phi": "φ", "chi": "χ", "psi": "ψ", "omega": "ω", "Gamma": "Γ",
               "Delta": "Δ", "Theta": "Θ", "Lambda": "Λ", "Pi": "Π", "Sigma": "Σ", "Phi": "Φ", "Psi": "Ψ",
               "Omega": "Ω", "hbar": "ℏ", "partial": "∂", "nabla": "∇", "int": "∫", "sum": "∑", "infty": "∞"}
EQ_LABEL_RE = re.compile(r"\b(E\d+(?:\.\d+)*)\s*[:=]")
DEF_SECTION_RE = re.compile(r"(?i)definition|glossary|key terms|terms|vocabulary|symbols")
DEF_VERBAL = [
    re.compile(r"(?i)\b(?:we\s+)?define[sd]?\s+(?:the\s+)?([A-Za-z][\w\-\s'’]{1,40}?)\s+(?:as|to be)\s+([^\n.]{5,200})"),
    re.compile(r"(?i)\b(?:the\s+term\s+)?([A-Za-z][\w\-'’]*(?:\s+[\w\-'’]+){0,4}?)\s+(?:is defined as|is defined to be|"
               r"denotes|stands for)\s+([^\n.]{5,200})"),
    re.compile(r"(?<![=<>!])\b([^\s=|$]{1,20})\s*(?::=|≡)\s*([^\n|]{3,200})"),
]
DEF_STOP = {"this", "that", "it", "which", "what", "there", "here", "he", "she", "they", "we", "one", "the", "a"}


# ───────────────────────────── analyzers (text stream) ─────────────────────────────

def all_sentences(blocks):
    out = []
    for b in blocks:
        for s in sentences_of(clean_inline(b)):
            out.append(s)
    return out


def analyze_structure(body: str, blocks) -> dict:
    lines = body.split("\n")
    heads, in_code = [], False
    for i, ln in enumerate(lines, 1):
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", ln)
        if m:
            heads.append({"level": len(m.group(1)), "text": clean_inline(m.group(2)), "line": i})
    doubled = [b["text"] for a, b in zip(heads, heads[1:]) if a["text"] == b["text"] and a["level"] == b["level"]]
    r = readability(blocks) or {"words": 0, "sentences": 0}
    last = next((l.strip() for l in reversed(lines) if l.strip()), "")
    truncated = (len(last) > 40 and not re.search(r"[.!?:;)\]*_`>|\"'”’—…\-]$", last)
                 and not last.startswith(("#", "|", "---", "<!--")))
    return {
        "words": r.get("words", 0), "sentences": r.get("sentences", 0), "paragraphs": len(blocks),
        "headings": len(heads), "tables": len(re.findall(r"^\s*>?\s*\|?\s*:?-{3,}:?\s*\|", body, re.M)),
        "reading_time_min": round(r.get("words", 0) / 230, 1),
        "avg_sentence_words": r.get("avg_sentence_words"),
        "flesch_kincaid_grade": r.get("flesch_kincaid_grade"),
        "flesch_reading_ease": r.get("flesch_reading_ease"),
        "outline": [h for h in heads if h["level"] <= 3][:80],
        "doubled_headings": doubled,
        "truncation_suspected": truncated,
        "last_line": snippet(last, 160),
    }


def classify_source(full_text: str, fm: str, words: int) -> str:
    head = full_text[:4000]
    if re.search(r"record_version:\s*CKG_", fm + head) or "PAPER_SECTION:" in full_text:
        return "PIPELINE_ARTIFACT"
    if "Human routing question" in full_text or ("primarily become" in full_text and "- [ ]" in full_text):
        return "ROUTING_STUB"
    if words < 150:
        return "STUB"
    return "PAPER"


def analyze_terms(prose: str, body: str) -> dict:
    uses = {}
    for k, rx in TERM_RES.items():
        n = len(rx.findall(prose))
        if n:
            uses[k] = n
    fam = Counter()
    for k, n in uses.items():
        fam[TERM_FAMILY[k]] += n
    # definitions
    defs = []
    seen = set()

    def add(term, text, how):
        t = clean_inline(term).strip(" :-—–*").strip()
        if not t or t.lower() in DEF_STOP or len(t) > 60 or not re.search(r"[A-Za-zΑ-ω]", t):
            return
        key = (t.lower(), how)
        if key in seen:
            return
        seen.add(key)
        defs.append({"term": t, "definition": snippet(clean_inline(text), 220), "found_by": how})

    current, in_code = "", False
    for ln in body.split("\n"):
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r"^#{1,6}\s+(.+)", ln)
        if m:
            current = m.group(1)
            continue
        if current and DEF_SECTION_RE.search(current):
            s = re.sub(r"^(>\s*)+", "", ln.strip())
            m1 = re.match(r"^(?:[-*]\s+)?\*\*(.{2,60}?)\*\*\s*[:—–-]?\s*(.{5,})$", s)
            m2 = re.match(r"^[-*]\s+([^:]{2,50}):\s+(.{5,})$", s)
            if m1:
                add(m1.group(1), m1.group(2), "definitions section")
            elif m2:
                add(m2.group(1), m2.group(2), "definitions section")
    for tbl in parse_tables(body):
        hdr = [h.lower() for h in tbl["headers"]]
        if hdr and re.search(r"\bterm\b|\bsymbol\b|\bconcept\b", hdr[0]) and len(hdr) >= 2:
            for row in tbl["rows"]:
                if len(row) >= 2 and row[0] and not re.match(r"^:?-{3,}", row[0]):
                    add(row[0], row[1], "definitions table")
    for rx in DEF_VERBAL:
        for m in rx.finditer(strip_for_prose(body)):
            add(m.group(1), m.group(2), "definition wording")
    defined_lower = [d["term"].lower() for d in defs]

    def is_defined(name):
        key = name.split(" (")[0].split(" / ")[0].lower()
        return any(key in d or d in key for d in defined_lower if len(d) > 1)

    undefined = sorted(k for k in uses if TERM_FAMILY[k] == "FRAMEWORK" and not is_defined(k))
    # law references
    laws = []
    for m in LAW_MENTION.finditer(prose):
        n = int(m.group(1))
        if n not in LAW_CANON:
            continue
        win = prose[max(0, m.start() - 40): m.end() + 100]
        hits = [k for k, rx in LAW_RES.items() if rx.search(win)]
        status = "MATCH" if n in hits else ("POSSIBLE_MISMATCH" if hits else "UNLABELED")
        laws.append({"law": n, "canon_name": LAW_CANON[n][0], "status": status,
                     "nearby_law_keywords": [LAW_CANON[h][0] for h in hits if h != n],
                     "context": snippet(win, 160)})
    return {"term_uses": dict(sorted(uses.items(), key=lambda x: -x[1])),
            "family_totals": dict(fam.most_common()),
            "definitions": defs,
            "framework_terms_without_local_definition": undefined,
            "law_references": laws}


def analyze_math(body: str, prose: str) -> dict:
    eqs, seen = [], set()

    def add(expr, where):
        e = re.sub(r"\s+", " ", expr).strip().strip("*`").strip()
        if len(e) < 3 or len(e) > 300:
            return
        k = re.sub(r"\s", "", e)
        if k in seen:
            return
        seen.add(k)
        lab = EQ_LABEL_RE.search(e)
        eqs.append({"expression": e, "label": lab.group(1) if lab else None, "found_in": where})

    for m in re.finditer(r"\$\$(.+?)\$\$", body, re.S):
        add(m.group(1), "display math")
    for m in re.finditer(r"(?<!\$)\$([^$\n]{2,200})\$(?!\$)", body):
        s = m.group(1)
        if "=" in s or "\\" in s or any(c in GREEK for c in s):
            add(s, "inline math")
    mathy = re.compile(r"[" + GREEK + r"]|\^|\bd[a-z]/d[a-z]\b|\\[a-zA-Z]+|⟨|⟩|\|[^|\s]+⟩")
    in_code = False
    for ln in body.split("\n"):
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        s = re.sub(r"^(>\s*)+", "", ln.strip())
        if re.match(r"^\|?\s*:?-{3,}", s):
            continue
        cells = [c for c in s.strip("|").split("|")] if s.startswith("|") else [s]
        for c in cells:
            c2 = re.sub(r"\$[^$]*\$", " ", c)
            if "=" in c2 and mathy.search(c2) and "http" not in c2:
                lab = EQ_LABEL_RE.search(c2)
                piece = c2[lab.start():] if lab else c2
                add(clean_inline(piece), "table cell" if s.startswith("|") else "text line")
    all_expr = " ".join(e["expression"] for e in eqs)
    for name, ch in LATEX_GREEK.items():
        all_expr = all_expr.replace("\\" + name, ch)
    syms = sorted({c for c in all_expr if c in GREEK and c not in "∫∑√∞ℏ∂∇"})  # standard operators need no definition
    sym_rows = []
    for s in syms:
        rx_def = re.compile(re.escape(s) + r"\s*(?:\(|is\b|=|denotes|represents|stands for|:)|where[^.\n]{0,80}"
                            + re.escape(s))
        sym_rows.append({"symbol": s, "defined_nearby": bool(rx_def.search(prose))})
    labels = [e["label"] for e in eqs if e["label"]]
    lean_mentions = len(re.findall(r"\bLean\s?4?\b", body))
    thm_names = sorted(set(re.findall(r"\b(?:theorem|lemma)\s+([A-Za-z_][\w.']*_[\w.']*|[A-Za-z_]+\.[\w.']+)", body)))
    verify_claims = []
    for s in all_sentences(prose_blocks(body)):
        if VERIFY_CLAIM_RE.search(s):
            verify_claims.append(snippet(s, 240))
    stats = []
    for rx, kind in ((SIGMA_RE, "sigma"), (PVAL_RE, "p-value")):
        for m in rx.finditer(prose):
            stats.append({"kind": kind, "value": m.group(0),
                          "context": snippet(prose[max(0, m.start() - 90): m.end() + 60], 200)})
    derivation_markers = len(re.findall(r"\b(?:therefore|thus|hence|it follows|we derive|substitut\w*|yields)\b|⇒|⟹|=>",
                                        prose, re.I))
    return {"equations": eqs, "equation_count": len(eqs), "labelled_equations": labels,
            "symbols": sym_rows, "derivation_markers": derivation_markers,
            "lean_mentions": lean_mentions, "lean_theorem_names": thm_names[:60],
            "sorry_mentions": len(re.findall(r"\bsorry\b", body)),
            "verification_claims": verify_claims[:40], "statistical_claims": stats[:40]}


def analyze_evidence(prose: str, body: str) -> dict:
    passages = Counter()
    first_ctx = {}
    for m in SCRIPTURE_RE.finditer(body):
        num = m.group("num")
        num = ROMAN.get(num, num) if num else ""
        book = BOOK_ALIAS[m.group("book")]
        ref = f"{(num + ' ') if num else ''}{book} {m.group('ch')}:{m.group('v')}"
        if m.group("v2"):
            ref += f"–{m.group('v2')}"
        passages[ref] += 1
        first_ctx.setdefault(ref, snippet(body[max(0, m.start() - 80): m.end() + 80], 200))
    books = Counter()
    for ref, n in passages.items():
        books[ref.rsplit(" ", 1)[0]] += n
    wit = []
    for name, rx in WITNESS_RES.items():
        ms = list(rx.finditer(prose))
        if ms:
            m0 = ms[0]
            wit.append({"name": name, "category": WITNESSES[name][1], "mentions": len(ms),
                        "first_mention": snippet(prose[max(0, m0.start() - 100): m0.end() + 120], 240)})
    wit.sort(key=lambda w: (w["category"], -w["mentions"]))
    cites = set()
    for rx in CITE_RES:
        for m in rx.finditer(prose):
            cites.add(f"{m.group(1)} {m.group(2)}")
    return {"scripture_passages": dict(passages.most_common()),
            "scripture_context": first_ctx,
            "scripture_books": dict(books.most_common()),
            "witnesses": wit,
            "citation_like_references": sorted(cites),
            "dois": sorted(set(DOI_RE.findall(body))),
            "urls": sorted(set(URL_RE.findall(body)))[:60]}


def analyze_argument(sents, prose: str, body: str) -> dict:
    strong, hedge = [], 0
    for s in sents:
        if STRONG_RE.search(s):
            strong.append(snippet(s, 240))
        if HEDGE_RE.search(s):
            hedge += 1
    words = max(1, len(WORD_RE.findall(prose)))
    obj_sents = [snippet(s, 200) for s in sents if OBJECTION_RE.search(s)]
    obj_heads = [h for h in re.findall(r"^#{1,6}\s+(.+)$", body, re.M)
                 if re.search(r"(?i)/EAST|objection|rival|respons|critic|counter", h)]
    return {"strong_language_sentences": strong, "strong_language_count": len(strong),
            "hedged_sentence_count": hedge,
            "argument_markers_per_1000_words": round(1000 * len(ARG_RE.findall(prose)) / words, 1),
            "objection_passages": obj_sents[:30], "objection_headings": [clean_inline(h) for h in obj_heads]}


def analyze_bridges(body: str, sents) -> dict:
    kinds = Counter()
    lines = []
    for s in sents:
        ms = BRIDGE_RE.findall(s)
        if ms:
            for m in ms:
                ml = m.lower()
                if "isomorph" in ml or "homomorph" in ml or "structural" in ml or "same" in ml:
                    kinds["structure wording"] += 1
                elif "analog" in ml or "mirror" in ml:
                    kinds["analogy wording"] += 1
                else:
                    kinds["mapping wording"] += 1
            lines.append(snippet(s, 220))
    phys = re.compile(r"(?i)quantum|physic|mechanic|math|equation|information|thermo|entropy|force|field|science")
    theo = re.compile(r"(?i)theolog|scriptur|spiritual|biblic|god|christ|moral|faith|grace|sin\b|gospel")
    btables = []
    for t in parse_tables(body):
        h = " ".join(t["headers"])
        if phys.search(h) and theo.search(h):
            btables.append({"headers": t["headers"], "rows": len(t["rows"]), "line": t["line"]})
    return {"mapping_language": dict(kinds), "mapping_sentences": lines[:40],
            "cross_domain_tables": btables,
            "cross_domain_rows": sum(t["rows"] for t in btables)}


def analyze_falsifiability(sents) -> dict:
    rows = []
    for s in sents:
        m = FALSIFY_RE.search(s)
        if m:
            w = m.group(1).lower()
            kind = "prediction" if w.startswith("predict") or "we predict" in w else "defeat / falsifiability"
            rows.append({"kind": kind, "sentence": snippet(s, 240)})
    return {"lines": rows[:50], "prediction_count": sum(r["kind"] == "prediction" for r in rows),
            "defeat_count": sum(r["kind"] != "prediction" for r in rows)}


def analyze_voice(blocks, fm_vals: dict, words: int, term_uses: dict) -> dict:
    tech = sum(n for k, n in term_uses.items() if TERM_FAMILY[k] in ("FRAMEWORK", "PHYSICS", "MATH_FORMAL",
                                                                   "INFORMATION"))
    scored = []
    for b in blocks:
        wc = len(WORD_RE.findall(b))
        if wc < 35:
            continue
        if not any(rx.search(b) for k, rx in TERM_RES.items() if TERM_FAMILY[k] != "MATH_FORMAL"):
            continue
        r = readability([b])
        if r:
            scored.append((r["flesch_kincaid_grade"], snippet(clean_inline(b), 320)))
    scored.sort(key=lambda x: x[0])
    reg = (fm_vals.get("register") or fm_vals.get("register_type") or "").upper()
    reg = "CANON" if "CANON" in reg else ("DECLARATION" if "DECL" in reg else "UNSPECIFIED")
    return {"register_type": reg,
            "technical_terms_per_100_words": round(100 * tech / max(1, words), 1),
            "clearest_passages": [{"grade": g, "passage": p} for g, p in scored[:3]],
            "most_demanding_passages": [{"grade": g, "passage": p} for g, p in scored[3:][::-1][:3]]}


def content_vector(prose: str, top: int = 300) -> dict:
    toks = [w.lower().strip("'’-") for w in WORD_RE.findall(prose)]
    c = Counter(w for w in toks if len(w) >= 4 and w not in STOPWORDS and not w[0].isdigit())
    return dict(c.most_common(top))


# ───────────────────────────── atom stream (CKG v3.1 records) ─────────────────────────────

PLACEHOLDER_RE = re.compile(r"^(?:U\d+|—|–|-|NOT_APPLICABLE|N/?A|unknown|none|\{\{.*\}\})\b", re.I)


def build_ckg_index(ckg_dir: Path) -> dict:
    idx = {"sha": {}, "name": {}}
    if not ckg_dir or not ckg_dir.exists():
        return idx
    for jp in ckg_dir.rglob("*.json"):
        try:
            j = json.loads(jp.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(j, dict) or "paper_uuid" not in j:
            continue
        src = j.get("source") or {}
        for s in {src.get("sha256"), j.get("source_sha256")}:
            if s:
                idx["sha"][s] = jp
        for loc in [src.get("path")] + list(src.get("locations") or []):
            if loc:
                idx["name"].setdefault(Path(str(loc).replace("\\", "/")).name.lower(), jp)
    return idx


def substantive_rows(rows):
    out = []
    for r in rows:
        if not r or not r[0] or PLACEHOLDER_RE.match(r[0].strip()):
            continue
        unk = sum("unknown" in c.lower() for c in r)
        if unk >= max(2, len(r) // 2):
            continue
        out.append(r)
    return out


def atom_stream(sha: str, filename: str, ckg_index: dict) -> dict:
    jp = ckg_index["sha"].get(sha)
    how = "source SHA-256"
    if not jp:
        jp = ckg_index["name"].get(filename.lower())
        how = "source filename"
    if not jp:
        return {"status": "NOT_COMPUTED",
                "reason": "No CKG v3.1 record found for this source (matched by SHA-256, then filename). "
                          "Run the paper through CKG_EVIDENCE first to add claim, warrant and bridge-grade metrics."}
    try:
        j = json.loads(jp.read_text(encoding="utf-8"))
    except Exception as e:
        return {"status": "ERROR", "reason": f"Could not read CKG record {jp}: {e}"}
    objs = j.get("objects") or []
    secs = j.get("sections") or {}

    def tables_of(key):
        return parse_tables((secs.get(key) or {}).get("markdown", "") or "")

    def count_rows(key, header_rx):
        n = 0
        for t in tables_of(key):
            if re.search(header_rx, " ".join(t["headers"]), re.I):
                n += len(substantive_rows(t["rows"]))
        return n

    routing = any("- [ ]" in (o.get("quote") or "") for o in objs) or \
        "routing" in " ".join(j.get("keywords") or []).lower()
    return {
        "status": "FOUND", "matched_by": how, "record_path": str(jp),
        "record_version": j.get("record_version"), "paper_uuid": j.get("paper_uuid"),
        "review_status": j.get("review_status"), "classification": j.get("classification"),
        "overview_status": (j.get("overview") or {}).get("status"),
        "objects_total": len(objs),
        "objects_by_type": dict(Counter(o.get("type", "?") for o in objs)),
        "objects_by_register": dict(Counter(o.get("register", "?") for o in objs)),
        "objects": [{"key": o.get("key"), "type": o.get("type"), "register": o.get("register"),
                     "statement": snippet(o.get("statement") or "", 220), "uuid": o.get("uuid")} for o in objs],
        "section_status": {k: (v or {}).get("status") for k, v in secs.items()},
        "definition_rows": count_rows("S02", r"\bterm\b"),
        "math_rows": count_rows("S07", r"math id"),
        "bridge_rows": count_rows("S08", r"bridge id"),
        "defeat_condition_rows": count_rows("S09", r"negation|defeat"),
        "prediction_rows": count_rows("S09", r"prediction"),
        "unmapped_items": len(j.get("unmapped") or []),
        "grading_status": (j.get("grading") or {}).get("status"),
        "formal_build_status": j.get("formal_build_status"),
        "ckg_source_looks_like_routing_stub": routing,
    }


# ───────────────────────────── grading one paper ─────────────────────────────

NOT_COMPUTED = [
    ("l15.corpus.claim_clusters", "EMB", "Needs sentence embeddings over claim statements (next build step)."),
    ("l15.corpus.independent_arrival", "EMB", "Needs claim clusters plus run provenance dates."),
    ("l15.corpus.cross_domain_patterns", "EMB", "Needs anonymized invariant signatures from opened atoms."),
    ("l15.paper.definition_fit", "EMB", "Needs the canonical definitions library to compare against."),
    ("l15.paper.central_claim / load_bearers", "CKG", "Needs typed dependency edges (A4) in CKG records; "
                                                     "current records carry objects but not edges."),
    ("l15.paper.warrant_profile", "CKG", "Needs per-object axes (proof class, evidence edges) in CKG records."),
    ("l15.paper.ic_profile", "CKG", "Needs graded bridge records (S08 registry with IC grades)."),
    ("l15.time.*", "HISTORY", "Needs more than one graded version of the same paper."),
    ("l15.time.model_agreement", "AI", "Needs multi-model CKG runs of the same source."),
]


def grade_paper(path: Path, raw: bytes, text: str, sha: str, lane: str, series: str | None,
                ckg_index: dict, collection: str | None = None) -> dict:
    fm, body_all = split_frontmatter(text)
    fmi = frontmatter_info(fm)
    orig, orig_how = extract_original(text)
    analysed = orig if orig is not None else body_all
    blocks = prose_blocks(analysed)
    prose = "\n\n".join(blocks)
    sents = all_sentences(blocks)
    structure = analyze_structure(analysed, blocks)
    source_class = classify_source(text, fm, structure["words"])
    title = fmi["values"].get("title")
    if not title:
        m = re.search(r"^#\s+(.+)$", analysed, re.M)
        title = clean_inline(m.group(1)) if m else path.stem
    terms = analyze_terms(prose, analysed)
    math_ = analyze_math(analysed, prose)
    evid = analyze_evidence(prose, analysed)
    arg = analyze_argument(sents, prose, analysed)
    bridges = analyze_bridges(analysed, sents)
    fals = analyze_falsifiability(sents)
    voice = analyze_voice(blocks, fmi["values"], structure["words"], terms["term_uses"])
    atoms = atom_stream(sha, path.name, ckg_index)

    checks = [
        ("Source class", source_class, source_class == "PAPER"),
        ("Front matter keys unique", "yes" if not fmi["duplicate_keys"] else
         "duplicates: " + ", ".join(fmi["duplicate_keys"]), not fmi["duplicate_keys"]),
        ("No doubled headings", "yes" if not structure["doubled_headings"] else
         f"{len(structure['doubled_headings'])} doubled", not structure["doubled_headings"]),
        ("Not truncated", "yes" if not structure["truncation_suspected"] else
         "last line ends mid-sentence", not structure["truncation_suspected"]),
        ("CKG v3.1 record", atoms["status"], atoms["status"] == "FOUND"),
    ]
    if atoms.get("ckg_source_looks_like_routing_stub"):
        checks.append(("CKG record is a real review", "CKG record reviewed a routing stub, not this paper", False))
    hard_fail = source_class in ("ROUTING_STUB", "STUB")
    soft = [c for c in checks[1:] if not c[2] and c[0] != "CKG v3.1 record"]
    readiness = "NOT_READY" if hard_fail else ("PARTIAL" if soft or source_class != "PAPER" else "READY")

    strengths = []
    if evid["scripture_passages"]:
        strengths.append(f"Scripture: {len(evid['scripture_passages'])} passages across "
                         f"{len(evid['scripture_books'])} books ({', '.join(list(evid['scripture_books'])[:6])}).")
    hist = [w["name"] for w in evid["witnesses"] if w["category"] != "scientific / mathematical"]
    sci = [w["name"] for w in evid["witnesses"] if w["category"] == "scientific / mathematical"]
    if hist:
        strengths.append(f"Historical and philosophical witnesses beside the argument: {', '.join(hist)}.")
    if sci:
        strengths.append(f"Scientific and mathematical figures engaged: {', '.join(sci)}.")
    if math_["equation_count"]:
        strengths.append(f"{math_['equation_count']} mathematical expressions"
                         + (f", {len(math_['labelled_equations'])} labelled ({', '.join(math_['labelled_equations'][:6])})"
                            if math_["labelled_equations"] else "") + ".")
    if terms["definitions"]:
        strengths.append(f"{len(terms['definitions'])} explicit definitions.")
    if bridges["cross_domain_rows"]:
        strengths.append(f"{bridges['cross_domain_rows']} cross-domain mapping rows in "
                         f"{len(bridges['cross_domain_tables'])} table(s).")
    if arg["objection_passages"] or arg["objection_headings"]:
        strengths.append(f"Engages objections: {len(arg['objection_passages'])} passages"
                         + (f", headings: {', '.join(arg['objection_headings'][:4])}" if arg["objection_headings"] else "")
                         + ".")
    if fals["lines"]:
        strengths.append(f"Stays open to reality: {fals['defeat_count']} falsifiability/defeat lines, "
                         f"{fals['prediction_count']} prediction lines.")
    matched = [l for l in terms["law_references"] if l["status"] == "MATCH"]
    if matched:
        strengths.append(f"{len(matched)} Law references consistent with canonical numbering.")
    if voice["clearest_passages"]:
        strengths.append(f"Clearest passage reads at grade {voice['clearest_passages'][0]['grade']} — "
                         f"ready to reuse in plain-language pieces.")
    if evid["citation_like_references"]:
        strengths.append(f"{len(evid['citation_like_references'])} citation-style references.")

    look = []
    for name, result, ok in checks:
        if not ok and name != "CKG v3.1 record":
            look.append(f"(LOCAL) {name}: {result}.")
    mism = [l for l in terms["law_references"] if l["status"] == "POSSIBLE_MISMATCH"]
    if mism:
        look.append(f"(LOCAL) {len(mism)} Law reference(s) sit next to another law's keywords — check numbering "
                    f"against canon (ordering ruling still open).")
    if math_["verification_claims"]:
        look.append(f"(LOCAL) {len(math_['verification_claims'])} verification claim(s) — pair each with a receipt.")
    undefined_syms = [s["symbol"] for s in math_["symbols"] if not s["defined_nearby"]]
    if undefined_syms:
        look.append(f"(LOCAL) Symbols without a definition found nearby: {' '.join(undefined_syms)}.")
    if terms["framework_terms_without_local_definition"]:
        look.append("(INERT unless canon lacks them) Framework terms used without a local definition: "
                    + ", ".join(terms["framework_terms_without_local_definition"]) + ".")
    if arg["strong_language_count"]:
        look.append(f"(LOCAL) {arg['strong_language_count']} strong-wording sentence(s) — check each against "
                    f"the warrant it has.")

    registered = uuid_registry.paper_uuid_for_sha(sha) if uuid_registry else None
    return {
        "grader_version": GRADER_VERSION, "paper_uuid": registered or paper_uuid_for(sha),
        "version_uuid": paper_uuid_for(sha), "paper_id": sha[:12], "title": title, "collection": collection,
        "source_sha256": sha,
        "source": {"file": path.name, "path": str(path), "sha256": sha, "bytes": len(raw),
                   "analysed_part": orig_how or "whole document (front matter excluded)"},
        "lane": lane, "series": series, "analyzed_at": now_iso(),
        "front_matter": fmi, "source_class": source_class, "readiness": readiness,
        "readiness_checks": [{"check": c, "result": r, "ok": ok} for c, r, ok in checks],
        "strengths": strengths, "worth_a_look": look,
        "structure": structure, "claims_and_argument": arg, "definitions_and_terms": terms,
        "mathematics": math_, "evidence_witnesses_scripture": evid, "bridges": bridges,
        "falsifiability": fals, "voice_and_readers": voice, "atom_stream": atoms,
        "not_computed": [{"metric": m, "needs": n, "reason": r} for m, n, r in NOT_COMPUTED],
        "boundary": BOUNDARY,
        "_vector": content_vector(prose),
    }


# ───────────────────────────── Markdown rendering ─────────────────────────────

def md_table(headers, rows) -> str:
    esc = lambda x: str(x if x is not None else "").replace("|", "\\|").replace("\n", " ")
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def more_note(total: int, shown: int) -> str:
    return f"\n\n*…{total - shown} more in the JSON record.*" if total > shown else ""


def yaml_scalar(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    return json.dumps(str(v), ensure_ascii=False)


def render_paper_md(rec: dict, json_name: str) -> str:
    s, t, m, e = rec["structure"], rec["definitions_and_terms"], rec["mathematics"], rec["evidence_witnesses_scripture"]
    a, b, f, v, at = rec["claims_and_argument"], rec["bridges"], rec["falsifiability"], rec["voice_and_readers"], rec["atom_stream"]
    flat = {
        "record_type": "PAPER_GRADER_REPORT", "grader_version": rec["grader_version"],
        "paper_uuid": rec.get("paper_uuid"), "version_uuid": rec.get("version_uuid"), "paper_id": rec["paper_id"],
        "collection": rec.get("collection"),
        "title": rec["title"], "source_file": rec["source"]["file"], "source_sha256": rec["source"]["sha256"],
        "analyzed_at": rec["analyzed_at"], "lane": rec["lane"], "series": rec["series"],
        "source_class": rec["source_class"], "readiness": rec["readiness"],
        "ckg_record": at["status"], "words": s["words"], "fk_grade": s["flesch_kincaid_grade"],
        "equations": m["equation_count"], "labelled_equations": len(m["labelled_equations"]),
        "scripture_passages": len(e["scripture_passages"]), "witnesses": len(e["witnesses"]),
        "definitions": len(t["definitions"]), "law_references": len(t["law_references"]),
        "law_possible_mismatches": sum(1 for l in t["law_references"] if l["status"] == "POSSIBLE_MISMATCH"),
        "cross_domain_rows": b["cross_domain_rows"], "strong_language": a["strong_language_count"],
        "falsifiability_lines": len(f["lines"]), "verification_claims": len(m["verification_claims"]),
        "admission": "candidate", "human_ruling": "pending",
    }
    out = ["---"] + [f"{k}: {yaml_scalar(val)}" for k, val in flat.items()] + ["---", ""]
    out.append(f"# Paper Grader — {rec['title']}\n")
    out.append(f"**Source:** `{rec['source']['file']}` · **SHA-256:** `{rec['source']['sha256']}`  ")
    out.append(f"**Lane:** {rec['lane']} · **Series:** {rec['series'] or '—'} · **Graded:** {rec['analyzed_at']} · "
               f"**Grader:** {rec['grader_version']}  ")
    out.append(f"**Analysed:** {rec['source']['analysed_part']} · **Full data:** `{json_name}`\n")
    out.append(f"> [!note] What this is\n> {BOUNDARY}\n")

    out.append("## Readiness\n")
    out.append(f"**{rec['readiness']}** · source class **{rec['source_class']}**\n")
    out.append(md_table(["Check", "Result", "OK"], [(c["check"], c["result"], "✅" if c["ok"] else "⚠️")
                                                   for c in rec["readiness_checks"]]) + "\n")

    out.append("## Strengths at a glance\n")
    out.append("\n".join(f"- {x}" for x in rec["strengths"]) if rec["strengths"] else "- None detected by text analysis.")
    out.append("")
    out.append("## Worth a look\n")
    out.append("\n".join(f"- {x}" for x in rec["worth_a_look"]) if rec["worth_a_look"] else "- Nothing flagged.")
    out.append("")

    out.append("## A1 · Structure & argument\n")
    out.append(md_table(["Metric", "Value"], [
        ("Words / sentences / paragraphs", f"{s['words']} / {s['sentences']} / {s['paragraphs']}"),
        ("Headings / tables", f"{s['headings']} / {s['tables']}"),
        ("Reading time", f"{s['reading_time_min']} min"),
        ("Flesch–Kincaid grade / reading ease", f"{s['flesch_kincaid_grade']} / {s['flesch_reading_ease']}"),
        ("Average sentence length", f"{s['avg_sentence_words']} words"),
        ("Argument markers per 1,000 words", a["argument_markers_per_1000_words"]),
        ("Strong-wording sentences / hedged sentences", f"{a['strong_language_count']} / {a['hedged_sentence_count']}"),
        ("Objection passages", len(a["objection_passages"])),
    ]) + "\n")
    if s["outline"]:
        out.append("**Outline**\n")
        out.append("\n".join(f"{'  ' * (h['level'] - 1)}- {h['text']}" for h in s["outline"][:40]))
        out.append(more_note(len(s["outline"]), 40) + "\n")
    if a["strong_language_sentences"]:
        out.append("**Strong wording — pair each with its warrant**\n")
        shown = a["strong_language_sentences"][:15]
        out.append(md_table(["#", "Sentence"], [(i + 1, x) for i, x in enumerate(shown)]))
        out.append(more_note(len(a["strong_language_sentences"]), 15) + "\n")

    out.append("## A2 · Definitions & terms\n")
    tu = list(t["term_uses"].items())
    if tu:
        out.append(md_table(["Term", "Family", "Uses"], [(k, TERM_FAMILY[k], n) for k, n in tu[:25]]))
        out.append(more_note(len(tu), 25) + "\n")
    out.append("**Family totals:** " + (", ".join(f"{k} {n}" for k, n in t["family_totals"].items()) or "—") + "\n")
    if t["definitions"]:
        out.append("**Definitions found**\n")
        out.append(md_table(["Term", "Definition", "Found by"],
                            [(d["term"], d["definition"], d["found_by"]) for d in t["definitions"][:30]]))
        out.append(more_note(len(t["definitions"]), 30) + "\n")
    if t["framework_terms_without_local_definition"]:
        out.append("**Framework terms used without a local definition:** "
                   + ", ".join(t["framework_terms_without_local_definition"]) + "\n")
    if t["law_references"]:
        out.append("**Law references** (canonical numbering per the Apr 19 NT Spiritual Terms sheet)\n")
        out.append(md_table(["Law", "Canon name", "Status", "Context"],
                            [(l["law"], l["canon_name"], l["status"], l["context"]) for l in t["law_references"][:25]]))
        out.append(more_note(len(t["law_references"]), 25) + "\n")

    out.append("## A3 · Mathematics & formal work\n")
    out.append(md_table(["Metric", "Value"], [
        ("Mathematical expressions", m["equation_count"]),
        ("Labelled equations", ", ".join(m["labelled_equations"]) or "—"),
        ("Derivation markers", m["derivation_markers"]),
        ("Lean mentions / theorem names / 'sorry' mentions",
         f"{m['lean_mentions']} / {len(m['lean_theorem_names'])} / {m['sorry_mentions']}"),
        ("Verification claims", len(m["verification_claims"])),
        ("Statistical claims (σ, p)", len(m["statistical_claims"])),
    ]) + "\n")
    if m["equations"]:
        out.append(md_table(["Label", "Expression", "Found in"],
                            [(q["label"] or "—", q["expression"], q["found_in"]) for q in m["equations"][:30]]))
        out.append(more_note(len(m["equations"]), 30) + "\n")
    if m["symbols"]:
        out.append(md_table(["Symbol", "Definition found nearby"],
                            [(x["symbol"], "yes" if x["defined_nearby"] else "not found") for x in m["symbols"]]) + "\n")
    if m["lean_theorem_names"]:
        out.append("**Lean theorem / lemma names:** " + ", ".join(f"`{x}`" for x in m["lean_theorem_names"][:30]) + "\n")
    if m["verification_claims"]:
        out.append("**Verification claims — each needs a receipt**\n")
        out.append("\n".join(f"- {x}" for x in m["verification_claims"][:15]) + "\n")
    if m["statistical_claims"]:
        out.append(md_table(["Kind", "Value", "Context"],
                            [(x["kind"], x["value"], x["context"]) for x in m["statistical_claims"][:15]]) + "\n")

    out.append("## A4 · Evidence, witnesses & Scripture\n")
    if e["scripture_passages"]:
        out.append(md_table(["Passage", "Times", "First context"],
                            [(p, n, e["scripture_context"].get(p, "")) for p, n in list(e["scripture_passages"].items())[:40]]))
        out.append(more_note(len(e["scripture_passages"]), 40) + "\n")
        out.append("**Books:** " + ", ".join(f"{k} ({n})" for k, n in e["scripture_books"].items()) + "\n")
    else:
        out.append("No chapter:verse Scripture references detected.\n")
    if e["witnesses"]:
        out.append(md_table(["Name", "Category", "Mentions", "First mention"],
                            [(w["name"], w["category"], w["mentions"], w["first_mention"]) for w in e["witnesses"]]) + "\n")
    out.append(f"**Citation-style references:** {len(e['citation_like_references'])}"
               + (" — " + "; ".join(e["citation_like_references"][:20]) if e["citation_like_references"] else "")
               + f"  \n**DOIs:** {len(e['dois'])} · **URLs:** {len(e['urls'])}\n")

    out.append("## A5 · Bridges & cross-domain moves\n")
    out.append("**Mapping language:** " + (", ".join(f"{k} {n}" for k, n in b["mapping_language"].items()) or "none") + "\n")
    if b["cross_domain_tables"]:
        out.append(md_table(["Line", "Headers", "Rows"],
                            [(x["line"], " · ".join(x["headers"]), x["rows"]) for x in b["cross_domain_tables"]]) + "\n")
    if b["mapping_sentences"]:
        out.append("\n".join(f"- {x}" for x in b["mapping_sentences"][:12]) + more_note(len(b["mapping_sentences"]), 12) + "\n")

    out.append("## A6 · Falsifiability & predictions\n")
    if f["lines"]:
        out.append(md_table(["Kind", "Sentence"], [(x["kind"], x["sentence"]) for x in f["lines"][:20]]))
        out.append(more_note(len(f["lines"]), 20) + "\n")
    else:
        out.append("No falsifiability or prediction wording detected.\n")

    out.append("## A7 · Voice & readers\n")
    out.append(f"**Register:** {v['register_type']} · **Technical terms per 100 words:** "
               f"{v['technical_terms_per_100_words']}\n")
    if v["clearest_passages"]:
        out.append("**Clearest passages**\n")
        out.append("\n".join(f"- *(grade {p['grade']})* {p['passage']}" for p in v["clearest_passages"]) + "\n")
    if v["most_demanding_passages"]:
        out.append("**Most demanding passages — candidates for a plain-language companion**\n")
        out.append("\n".join(f"- *(grade {p['grade']})* {p['passage']}" for p in v["most_demanding_passages"]) + "\n")

    out.append("## Atom stream — CKG v3.1 record\n")
    if at["status"] == "FOUND":
        out.append(md_table(["Field", "Value"], [
            ("Record", at["record_path"]), ("Matched by", at["matched_by"]),
            ("Review status / overview", f"{at['review_status']} / {at['overview_status']}"),
            ("Objects", f"{at['objects_total']} — " + ", ".join(f"{k} {n}" for k, n in at["objects_by_type"].items())),
            ("Registers", ", ".join(f"{k} {n}" for k, n in at["objects_by_register"].items())),
            ("Substantive rows: definitions / math / bridges", f"{at['definition_rows']} / {at['math_rows']} / {at['bridge_rows']}"),
            ("Substantive rows: defeat conditions / predictions", f"{at['defeat_condition_rows']} / {at['prediction_rows']}"),
            ("Unmapped items", at["unmapped_items"]),
            ("Section status", ", ".join(f"{k} {v2}" for k, v2 in at["section_status"].items())),
        ]) + "\n")
    else:
        out.append(f"**{at['status']}** — {at['reason']}\n")

    out.append("## Not computed in this pass\n")
    out.append(md_table(["Metric", "Needs", "Reason"], [(x["metric"], x["needs"], x["reason"]) for x in rec["not_computed"]]))
    out.append(f"\n---\n*{BOUNDARY}*\n")
    return "\n".join(out)


def render_extract_md(rec: dict) -> str:
    t, m, e, f, at = (rec["definitions_and_terms"], rec["mathematics"], rec["evidence_witnesses_scripture"],
                      rec["falsifiability"], rec["atom_stream"])
    out = [f"# Knowledge extract — {rec['title']}\n", f"`{rec['source']['file']}` · `{rec['source']['sha256'][:12]}` · "
           f"{rec['analyzed_at']}\n", f"> {BOUNDARY}\n"]
    if at["status"] == "FOUND" and at["objects"]:
        out.append("## CKG objects\n")
        out.append(md_table(["Key", "Type", "Register", "Statement"],
                            [(o["key"], o["type"], o["register"], o["statement"]) for o in at["objects"]]) + "\n")
    if t["definitions"]:
        out.append("## Definitions\n")
        out.append(md_table(["Term", "Definition"], [(d["term"], d["definition"]) for d in t["definitions"]]) + "\n")
    if m["equations"]:
        out.append("## Equations\n")
        out.append(md_table(["Label", "Expression"], [(q["label"] or "—", q["expression"]) for q in m["equations"]]) + "\n")
    if e["scripture_passages"]:
        out.append("## Scripture\n")
        out.append(", ".join(e["scripture_passages"].keys()) + "\n")
    if e["witnesses"]:
        out.append("## Witnesses\n")
        out.append(", ".join(f"{w['name']} ({w['category']})" for w in e["witnesses"]) + "\n")
    if m["verification_claims"]:
        out.append("## Verification claims (pair with receipts)\n")
        out.append("\n".join(f"- {x}" for x in m["verification_claims"]) + "\n")
    if f["lines"]:
        out.append("## Falsifiability & predictions\n")
        out.append("\n".join(f"- *{x['kind']}* — {x['sentence']}" for x in f["lines"]) + "\n")
    return "\n".join(out)


# ───────────────────────────── writing outputs ─────────────────────────────

def write_outputs(rec: dict, path: Path, raw: bytes, outbox: Path) -> dict:
    # Same naming as the CKG runner: "<title> -- <version uuid>". Markdown + JSON side by side in 01_ALL_PAPERS.
    base = f"{safe_name(rec['title'], 90)} -- {rec['version_uuid']}"
    json_name, md_name = base + ".json", base + ".md"
    cls = (rec["atom_stream"].get("classification") or {}) if rec["atom_stream"]["status"] == "FOUND" else {}
    fmv = rec["front_matter"]["values"]
    pick = lambda a, b: a if a not in (None, "", "Unassigned") else b
    rec["views"] = {"collection": rec.get("collection"), "series": rec["series"],
                    "domain": pick(cls.get("domain"), fmv.get("domain") or fmv.get("domain_primary")),
                    "content_type": pick(cls.get("purpose"), fmv.get("content_type") or fmv.get("type")),
                    "laws": sorted({l["law"] for l in rec["definitions_and_terms"]["law_references"]})}
    rec["markdown"] = md_name
    rec["outputs"] = {"markdown": f"01_ALL_PAPERS/{md_name}", "json": f"01_ALL_PAPERS/{json_name}"}
    md = render_paper_md(rec, json_name)
    (outbox / "01_ALL_PAPERS" / json_name).write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
    (outbox / "01_ALL_PAPERS" / md_name).write_text(md, encoding="utf-8")
    orig_dir = BACK_DIR / "ORIGINALS"
    orig_dir.mkdir(parents=True, exist_ok=True)
    (orig_dir / (rec["version_uuid"] + path.suffix.lower())).write_bytes(raw)
    if rec["readiness"] != "READY":
        note = [f"# Needs attention — {rec['title']}\n", f"`{rec['source']['file']}` · readiness **{rec['readiness']}** "
                f"· source class **{rec['source_class']}**\n"]
        note += [f"- {c['check']}: {c['result']}" for c in rec["readiness_checks"] if not c["ok"]]
        note.append(f"\nFull report: `{rec['outputs']['markdown']}`\n")
        (BACK_DIR / "NEEDS_ATTENTION").mkdir(parents=True, exist_ok=True)
        (BACK_DIR / "NEEDS_ATTENTION" / md_name).write_text("\n".join(note), encoding="utf-8")
    return {"json": json_name, "markdown": md_name}


def write_failure(outbox: Path, path: Path, err: str):
    name = f"FAILED__{safe_name(path.stem)}.md"
    (BACK_DIR / "NEEDS_ATTENTION").mkdir(parents=True, exist_ok=True)
    (BACK_DIR / "NEEDS_ATTENTION" / name).write_text(
        f"# Grader failure — {path.name}\n\n`{path}`\n\n```\n{err}\n```\n", encoding="utf-8")


# ───────────────────────────── corpus ─────────────────────────────

def load_records(outbox: Path):
    recs = []
    for jp in sorted((outbox / "01_ALL_PAPERS").glob("*.json")):
        try:
            r = json.loads(jp.read_text(encoding="utf-8"))
            if r.get("grader_version", "").startswith("paper_grader"):
                recs.append(r)
        except Exception:
            continue
    return recs


def cosine(a: dict, b: dict, idf: dict) -> float:
    num = sum(a[k] * idf[k] * b[k] * idf[k] for k in a.keys() & b.keys())
    na = math.sqrt(sum((v * idf[k]) ** 2 for k, v in a.items()))
    nb = math.sqrt(sum((v * idf[k]) ** 2 for k, v in b.items()))
    return num / (na * nb) if na and nb else 0.0


def build_corpus(recs) -> dict:
    papers = [r for r in recs if r.get("source_class") in ("PAPER", "PIPELINE_ARTIFACT")]
    census = defaultdict(lambda: {"papers": 0, "uses": 0})
    defs = defaultdict(list)
    scripture = defaultdict(set)
    witnesses = defaultdict(set)
    labels = defaultdict(list)
    laws = defaultdict(lambda: {"MATCH": set(), "POSSIBLE_MISMATCH": set(), "UNLABELED": set()})
    verify = []
    grid = defaultdict(Counter)
    for r in recs:
        title = r["title"]
        t = r["definitions_and_terms"]
        for term, n in t["term_uses"].items():
            census[term]["papers"] += 1
            census[term]["uses"] += n
        for d in t["definitions"]:
            defs[d["term"].lower()].append({"paper": title, "term": d["term"], "definition": d["definition"]})
        for p in r["evidence_witnesses_scripture"]["scripture_passages"]:
            scripture[p].add(title)
        for w in r["evidence_witnesses_scripture"]["witnesses"]:
            witnesses[(w["name"], w["category"])].add(title)
        for q in r["mathematics"]["equations"]:
            if q["label"]:
                labels[q["label"]].append({"paper": title, "expression": q["expression"]})
        fam = t["family_totals"]
        dom_fam = max(fam, key=fam.get) if fam else "NONE"
        cited = set()
        for l in t["law_references"]:
            laws[l["law"]][l["status"]].add(title)
            cited.add(l["law"])
        for n in cited:
            grid[n][dom_fam] += 1
        for c in r["mathematics"]["verification_claims"]:
            verify.append({"paper": title, "claim": c})
    # vocabulary similarity (tf-idf cosine over content words)
    vecs = [(r["title"], r.get("_vector") or {}) for r in papers]
    df = Counter()
    for _, v in vecs:
        df.update(v.keys())
    N = max(1, len(vecs))
    idf = {k: math.log((N + 1) / (c + 1)) + 1 for k, c in df.items()}
    pairs = []
    for i in range(len(vecs)):
        for j in range(i + 1, len(vecs)):
            sim = cosine(vecs[i][1], vecs[j][1], idf)
            if sim >= 0.2:
                pairs.append((round(sim, 3), vecs[i][0], vecs[j][0]))
    pairs.sort(reverse=True)
    label_reuse = {k: v for k, v in labels.items()
                   if len({re.sub(r"\s", "", x["expression"]) for x in v}) > 1}
    return {
        "generated_at": now_iso(), "grader_version": GRADER_VERSION,
        "records": len(recs),
        "by_source_class": dict(Counter(r["source_class"] for r in recs)),
        "by_readiness": dict(Counter(r["readiness"] for r in recs)),
        "term_census": dict(sorted(census.items(), key=lambda x: (-x[1]["papers"], -x[1]["uses"]))),
        "definitions_library": {k: v for k, v in sorted(defs.items(), key=lambda x: -len(x[1]))},
        "terms_defined_in_multiple_papers": sorted(k for k, v in defs.items() if len({x["paper"] for x in v}) > 1),
        "scripture_index": {p: sorted(ts) for p, ts in sorted(scripture.items(), key=lambda x: -len(x[1]))},
        "witness_index": [{"name": n, "category": c, "papers": sorted(ts)}
                          for (n, c), ts in sorted(witnesses.items(), key=lambda x: -len(x[1]))],
        "equation_labels": {k: v for k, v in sorted(labels.items())},
        "equation_labels_with_different_expressions": sorted(label_reuse),
        "law_references": {n: {k: sorted(s) for k, s in d.items()} for n, d in sorted(laws.items())},
        "law_by_dominant_family": {n: dict(c) for n, c in sorted(grid.items())},
        "verification_claims": verify,
        "vocabulary_similar_pairs": [{"similarity": s, "a": a, "b": b} for s, a, b in pairs[:30]],
        "boundary": BOUNDARY + " Similarity here is shared vocabulary, not shared structure.",
    }


def render_corpus_md(c: dict) -> str:
    out = ["---", "record_type: PAPER_GRADER_CORPUS_REPORT", f"generated_at: {yaml_scalar(c['generated_at'])}",
           f"records: {c['records']}", "---", "", "# Paper Grader — Corpus Report\n", f"> [!note]\n> {c['boundary']}\n",
           "## The corpus\n",
           md_table(["Measure", "Value"], [
               ("Records graded", c["records"]),
               ("By source class", ", ".join(f"{k} {n}" for k, n in c["by_source_class"].items())),
               ("By readiness", ", ".join(f"{k} {n}" for k, n in c["by_readiness"].items())),
           ]) + "\n", "## B4 · Term census\n"]
    rows = [(k, TERM_FAMILY.get(k, "?"), v["papers"], v["uses"]) for k, v in list(c["term_census"].items())[:40]]
    out.append(md_table(["Term", "Family", "Papers", "Uses"], rows) + "\n")
    if c["terms_defined_in_multiple_papers"]:
        out.append("## B4 · Terms defined in more than one paper — compare the versions\n")
        for term in c["terms_defined_in_multiple_papers"][:25]:
            out.append(f"### {term}\n")
            out.append(md_table(["Paper", "Definition"],
                                [(x["paper"], x["definition"]) for x in c["definitions_library"][term]]) + "\n")
    out.append("## B5 · Scripture illuminated\n")
    sc = list(c["scripture_index"].items())
    out.append(md_table(["Passage", "Papers", "Which"], [(p, len(ts), "; ".join(ts[:5])) for p, ts in sc[:50]])
               if sc else "No Scripture references yet.")
    out.append("\n## B2 · Witnesses across the corpus\n")
    wi = c["witness_index"]
    out.append(md_table(["Witness", "Category", "Papers", "Which"],
                        [(w["name"], w["category"], len(w["papers"]), "; ".join(w["papers"][:5])) for w in wi[:40]])
               if wi else "No witnesses yet.")
    out.append("\n## B6 · Equation labels\n")
    el = list(c["equation_labels"].items())
    out.append(md_table(["Label", "Papers", "Expressions differ?"],
                        [(k, len(v), "yes" if k in c["equation_labels_with_different_expressions"] else "no")
                         for k, v in el]) if el else "No labelled equations yet.")
    out.append("\n## B7 · Law references across the corpus\n")
    lr = c["law_references"]
    if lr:
        out.append(md_table(["Law", "Canon name", "Match", "Possible mismatch", "Unlabeled", "Dominant families of citing papers"],
                            [(n, LAW_CANON[int(n)][0], len(d["MATCH"]), len(d["POSSIBLE_MISMATCH"]), len(d["UNLABELED"]),
                              ", ".join(f"{k} {v}" for k, v in c["law_by_dominant_family"].get(n, {}).items()))
                             for n, d in lr.items()]))
    else:
        out.append("No Law references yet.")
    out.append("\n## B6 · Verification claims (receipt ledger input)\n")
    vc = c["verification_claims"]
    out.append(md_table(["Paper", "Claim"], [(x["paper"], x["claim"]) for x in vc[:40]]) if vc else "None found.")
    out.append("\n## B3 · Papers that share the most vocabulary\n")
    vp = c["vocabulary_similar_pairs"]
    out.append(md_table(["Similarity", "Paper A", "Paper B"], [(x["similarity"], x["a"], x["b"]) for x in vp])
               if vp else "Needs at least two papers with overlapping vocabulary.")
    out.append("\n*Structural convergence (claim clusters, independent arrival) needs the embedding step — "
               "see 'Not computed' in each paper report.*\n")
    return "\n".join(out)


def write_master_index(recs, outbox: Path):
    cols = ["paper_uuid", "paper_id", "title", "source_file", "lane", "series", "source_class", "readiness", "ckg_record",
            "words", "fk_grade", "equations", "labelled_equations", "scripture_passages", "witnesses", "definitions",
            "law_references", "law_possible_mismatches", "cross_domain_rows", "strong_language",
            "falsifiability_lines", "verification_claims", "analyzed_at", "markdown", "json", "source_sha256"]
    BACK_DIR.mkdir(parents=True, exist_ok=True)
    with open(BACK_DIR / INDEX_FILE, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in recs:
            t, m, e = r["definitions_and_terms"], r["mathematics"], r["evidence_witnesses_scripture"]
            w.writerow([r.get("paper_uuid") or paper_uuid_for(r["source"]["sha256"]), r["paper_id"], r["title"],
                        r["source"]["file"], r["lane"], r["series"] or "",
                        r["source_class"], r["readiness"], r["atom_stream"]["status"], r["structure"]["words"],
                        r["structure"]["flesch_kincaid_grade"], m["equation_count"], len(m["labelled_equations"]),
                        len(e["scripture_passages"]), len(e["witnesses"]), len(t["definitions"]),
                        len(t["law_references"]),
                        sum(1 for l in t["law_references"] if l["status"] == "POSSIBLE_MISMATCH"),
                        r["bridges"]["cross_domain_rows"], r["claims_and_argument"]["strong_language_count"],
                        len(r["falsifiability"]["lines"]), len(m["verification_claims"]), r["analyzed_at"],
                        (r.get("outputs") or {}).get("markdown", ""), (r.get("outputs") or {}).get("json", ""),
                        r["source"]["sha256"]])


# ───────────────────────────── run ─────────────────────────────

def ensure_dirs(inbox: Path, outbox: Path):
    for lane in INBOX_LANES:
        (inbox / lane).mkdir(parents=True, exist_ok=True)
    for lane in OUTBOX_LANES:
        (outbox / lane).mkdir(parents=True, exist_ok=True)
    for d in ("ORIGINALS", "STATE", "NEEDS_ATTENTION", "CORPUS_REPORTS"):
        (BACK_DIR / d).mkdir(parents=True, exist_ok=True)


def discover(inbox: Path, include_waiting: bool):
    """(lane, series, collection, path). Your own folders under 03_GENERAL become the collection."""
    found = []
    lanes = (["00_WAITING_NOT_PROCESSED"] if include_waiting else []) + ACTIVE_LANES
    for lane in lanes:
        root = inbox / lane
        if not root.exists():
            continue
        for p in sorted(root.rglob("*")):
            if not p.is_file() or p.suffix.lower() not in PAPER_EXTS or p.name.startswith(("~$", ".")):
                continue
            rel = p.relative_to(root).parts
            series = rel[0] if lane == "02_SERIES" and len(rel) > 1 else None
            collection = " / ".join(rel[:-1]) if lane == "03_GENERAL" and len(rel) > 1 else None
            found.append((lane, series, collection, p))
    return found


def load_state(outbox: Path) -> dict:
    sp = BACK_DIR / "STATE" / STATE_FILE
    if sp.exists():
        try:
            return json.loads(sp.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_state(outbox: Path, state: dict):
    (BACK_DIR / "STATE").mkdir(parents=True, exist_ok=True)
    (BACK_DIR / "STATE" / STATE_FILE).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def rebuild_corpus(outbox: Path):
    recs = load_records(outbox)
    write_master_index(recs, outbox)
    corpus = build_corpus(recs)
    stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    md = render_corpus_md(corpus)
    js = json.dumps(corpus, ensure_ascii=False, indent=2, default=list)
    (outbox / "00_CORPUS_REPORT.md").write_text(md, encoding="utf-8")
    (outbox / "00_CORPUS_REPORT.json").write_text(js, encoding="utf-8")
    (BACK_DIR / "CORPUS_REPORTS" / f"CORPUS_REPORT_{stamp}.md").write_text(md, encoding="utf-8")
    return len(recs)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Paper Grader — L15 atom analytics (Python only, no API calls).")
    ap.add_argument("--inbox", help="Inbox folder (default: MAIN/PYTHON/INBOX)")
    ap.add_argument("--outbox", help="Outbox folder (default: MAIN/PYTHON/OUTBOX)")
    ap.add_argument("--ckg-json", help="CKG records folder (default: MAIN/_BACKSIDE/CKG_EVIDENCE/SYSTEM/RECORDS)")
    ap.add_argument("--force", action="store_true", help="Regrade papers already graded at this version")
    ap.add_argument("--include-waiting", action="store_true", help="Also grade INBOX/00_WAITING_NOT_PROCESSED")
    ap.add_argument("--inventory", action="store_true", help="Count what is waiting; grade nothing")
    ap.add_argument("--corpus-only", action="store_true", help="Rebuild the index and corpus report only")
    args = ap.parse_args(argv)

    inbox = Path(args.inbox) if args.inbox else STATION_DIR / "INBOX"
    outbox = Path(args.outbox) if args.outbox else STATION_DIR / "OUTBOX"
    ckg_json = Path(args.ckg_json) if args.ckg_json else CKG_RECORDS
    ensure_dirs(inbox, outbox)
    print(f"{GRADER_VERSION}\n  inbox : {inbox}\n  outbox: {outbox}\n  ckg   : {ckg_json}\n")

    if args.corpus_only:
        n = rebuild_corpus(outbox)
        print(f"Corpus report rebuilt from {n} record(s).")
        return 0

    files = discover(inbox, args.include_waiting)
    state = load_state(outbox)
    if args.inventory:
        lanes = Counter(l for l, s, c, p in files)
        new = 0
        for l, s, c, p in files:
            try:
                if sha256_bytes(p.read_bytes()) not in state:
                    new += 1
            except OSError:
                pass
        print(f"Papers found: {len(files)}  (not yet graded: {new})")
        for l, n in sorted(lanes.items()):
            print(f"  {l}: {n}")
        return 0

    ckg_index = build_ckg_index(ckg_json)
    print(f"CKG records indexed: {len(set(ckg_index['sha'].values()))}")
    done = skipped = failed = dups = 0
    seen_this_run = {}
    for lane, series, collection, p in files:
        try:
            raw, text = read_text(p)
            sha = sha256_bytes(raw)
            if sha in seen_this_run:  # exact copy of a file already in this inbox → 04_DUPLICATES
                dest = inbox / "04_DUPLICATES" / sha[:12]
                dest.mkdir(parents=True, exist_ok=True)
                shutil.move(str(p), str(dest / p.name))
                dups += 1
                print(f"  duplicate          {p.name}  (same bytes as {seen_this_run[sha]})")
                continue
            seen_this_run[sha] = p.name
            prev = state.get(sha)
            if prev and not args.force and prev.get("version") == GRADER_VERSION and \
                    (outbox / "01_ALL_PAPERS" / prev.get("json", "")).exists():
                skipped += 1
                continue
            rec = grade_paper(p, raw, text, sha, lane, series, ckg_index, collection)
            names = write_outputs(rec, p, raw, outbox)
            state[sha] = {"file": str(p), "version": GRADER_VERSION, "graded_at": rec["analyzed_at"], **names}
            done += 1
            print(f"  graded  {rec['readiness']:<9} {rec['source_class']:<17} {p.name}")
        except Exception:
            failed += 1
            err = traceback.format_exc()
            write_failure(outbox, p, err)
            print(f"  FAILED  {p.name}\n{err}")
    save_state(outbox, state)
    n = rebuild_corpus(outbox)
    print(f"\nDone. graded {done} · skipped (already graded) {skipped} · duplicates moved {dups} · "
          f"failed {failed} · corpus {n} record(s)")
    print(f"Reports: {outbox / '01_ALL_PAPERS'}\nCorpus:  {outbox / '00_CORPUS_REPORT.md'}")
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
