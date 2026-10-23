"""NABLA address: deterministic half (spec v6 sec.14). The AI proposes; this code validates and builds."""
import re
ORDER = "GMESTKRQFC"
TIE = "ECGKMTRFSQ"
DOMAINS = {"THEOPHYSICS","SCIENCE","PHYSICS","BIOLOGY","CHEMISTRY","MATHEMATICS","LOGIC","LAW","MEDICINE","FINANCE",
           "PERSONAL","TECH","EDUCATION","GOVERNANCE","ART","BUSINESS","RELIGION","HISTORY","PSYCHOLOGY","SOCIOLOGY",
           "INFORMATION","PHILOSOPHY","UNKNOWN"}
VERS = set("DWFPAX"); USES = set("IBTR"); RISKS = {"R0","R1","R2","R3","R4"}
AUD = {"SELF","INTERNAL","TEAM","AI_RESEARCH","PUBLIC","PUBLIC_RESEARCH","ACADEMIC","CLIENT","RESTRICTED","LEGAL","UNKNOWN"}

def vector_str(v): return "".join(f"{k}{v[k]}" for k in ORDER)

def semantic_hash(v):
    rank = sorted(ORDER, key=lambda k: (-v[k], TIE.index(k)))
    return "".join(f"[{rank[i]}·{rank[9-i]}]" for i in range(5))

def validate(filing, v):
    errs = []
    if set(v) != set(ORDER): errs.append("vector must have exactly G M E S T K R Q F C")
    if any(x not in (0, 3) for x in v.values()): errs.append("vector scores must be 0 or 3")
    if filing.get("D") not in DOMAINS: errs.append(f"bad domain {filing.get('D')}")
    if not re.fullmatch(r"[A-Z0-9_]+", str(filing.get("N",""))): errs.append("entity must be UPPER_SNAKE")
    if filing.get("V") not in VERS: errs.append("bad version")
    if filing.get("A") not in AUD: errs.append("bad audience")
    if filing.get("U") not in USES: errs.append("bad use")
    if filing.get("R") not in RISKS: errs.append("bad risk")
    return errs

def address(filing, v):
    f = filing
    return f"{f['D']}/{f['N']}/{f['V']}/{f['A']}/{f['U']}/{f['R']} :: {vector_str(v)} :: {semantic_hash(v)}"

ENCODER_PROMPT = """NABLA ENCODER v6
Classify the artifact by what it structurally IS, not just its topic. Do not judge truth.
Return ONLY JSON: {"filing":{"D":..,"N":..,"V":..,"A":..,"U":..,"R":..},
 "vector":{"G":0|3,"M":..,"E":..,"S":..,"T":..,"K":..,"R":..,"Q":..,"F":..,"C":..},
 "confidence":{"G":0-1,...}, "review_flags":[..], "minimal_decode":"one sentence",
 "truth_modes":[..], "operators":[..]}
G=authority/ground; M=mechanism/action; E=disorder IN THE ARTIFACT; S=identity/self; T=time/sequence;
K=knowledge/info; R=relation/bond; Q=experience/felt; F=faith/trust; C=explicit synthesis/unity.
E3 only for artifact corruption/fragmentation/contradiction/redaction. C3 only when integration is a dominant function.
Filing: D domain (THEOPHYSICS SCIENCE PHYSICS MATHEMATICS LOGIC PHILOSOPHY RELIGION HISTORY ... UNKNOWN),
N entity UPPER_SNAKE, V D/W/F/P/A/X, A audience (SELF INTERNAL TEAM AI_RESEARCH PUBLIC PUBLIC_RESEARCH ACADEMIC ...),
U I inform/B bind/T transform/R record, R risk R0-R4.
truth_modes from: AXIOM PRE_ASSUMPTION EMPIRICAL_EVENT HISTORICAL_RECORD MATHEMATICAL_PROOF FORMAL_DERIVATION
INTERPRETATION SYMBOLIC_TRUTH MORAL_CLAIM THEOLOGICAL_CLAIM EXPERIENTIAL_REPORT PREDICTION UNKNOWN.
operators: which of these the artifact instantiates as a dominant move: source distinction relation reception
orientation boundary cost record damage repair identity_preserving_transformation.
Confidence is separate from 0/3. If uncertain, add a review flag; do not manufacture certainty.
SCORING IS BINARY: every vector value is exactly 0 or 3. Never 1 or 2. There is no partial score; partial belongs in confidence.
3 means DOMINANT - one of the few signals that define what this artifact is. Most artifacts have 3 to 5 dominant variables.
If you mark more than 6 variables 3, you are describing the topic, not the artifact: drop the weakest back to 0 and flag it.
C3 requires that integration/unification is the artifact's main job, not that it is coherent or well organized."""
