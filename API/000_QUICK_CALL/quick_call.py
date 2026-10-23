"""000_QUICK_CALL - first station. Writes the sidecar YAML that heads every later API call.
Usage: python quick_call.py <file> [--series "Math Is Moral"] [--position 3] [--of 5] [--me-id ME-...] [--parent <paper_uuid>] [--no-ai]"""
import argparse, hashlib, json, os, shutil, sys, urllib.request
from datetime import datetime, timezone
import nabla, identity

def _central(key):
    """Read the ONE central config (API/_system/config/paths.json) - same as every other station."""
    try:
        cfg = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_system", "config", "paths.json"), encoding="utf-8"))
        return cfg.get(key) or None
    except Exception: return None

PIPE      = os.environ.get("API_PIPELINE") or _central("api_pipeline_out") or r"\\192.168.2.50\h_hp\Desktop\Youtube API CKG\API_PIPELINE"
ORIGINALS = os.environ.get("API_ORIGINALS") or _central("originals_root") or r"\\192.168.2.50\h_hp\Desktop\Youtube API CKG\ORIGINALS"
STATION   = os.path.join(PIPE, "000_QUICK_CALL")
REGISTRY  = os.path.join(STATION, "UUID_REGISTRY.json")

def ask_ai(text):
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key: raise RuntimeError("DEEPSEEK_API_KEY not set")
    url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com").rstrip("/") + "/chat/completions"
    body = {"model": "deepseek-chat", "response_format": {"type": "json_object"}, "temperature": 0,
            "messages": [{"role": "system", "content": nabla.ENCODER_PROMPT},
                         {"role": "user", "content": text[:60000]}]}
    req = urllib.request.Request(url, json.dumps(body).encode(), {"Content-Type": "application/json", "Authorization": "Bearer " + key})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(json.loads(r.read())["choices"][0]["message"]["content"])

def yaml_dump(o, ind=0):
    pad = "  " * ind; out = []
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, (dict, list)) and v: out.append(f"{pad}{k}:"); out.append(yaml_dump(v, ind + 1))
            else: out.append(f"{pad}{k}: {json.dumps(v, ensure_ascii=False) if v not in ({}, []) else ('{}' if v == {} else '[]')}")
    else:
        for v in o:
            if isinstance(v, (dict, list)): out.append(f"{pad}-"); out.append(yaml_dump(v, ind + 1))
            else: out.append(f"{pad}- {json.dumps(v, ensure_ascii=False)}")
    return "\n".join(out)

def run(path, series=None, position=None, of=None, me_id=None, parent=None, use_ai=True):
    raw = open(path, "rb").read(); sha = hashlib.sha256(raw).hexdigest()
    stem = os.path.splitext(os.path.basename(path))[0]
    reg = identity.Registry(REGISTRY); pid, new = reg.resolve(sha, stem, parent); reg.save()
    os.makedirs(ORIGINALS, exist_ok=True)
    orig = os.path.join(ORIGINALS, f"{stem}__{sha[:12]}{os.path.splitext(path)[1]}")
    if not os.path.exists(orig): shutil.copy2(path, orig)
    nab = {"status": "NOT_RUN"}
    if use_ai:
        try:
            p = ask_ai(raw.decode("utf-8", errors="replace"))
            v = {k: int(p["vector"][k]) for k in nabla.ORDER}; errs = nabla.validate(p["filing"], v)
            nab = {"status": "VALID" if not errs else "INVALID", "errors": errs,
                   "address": nabla.address(p["filing"], v) if not errs else None,
                   "filing": p["filing"], "vector": nabla.vector_str(v), "hash": nabla.semantic_hash(v),
                   "confidence": p.get("confidence", {}),
                   "review_flags": p.get("review_flags", []) + [f"low confidence {k}" for k, c in p.get("confidence", {}).items() if float(c) < .75],
                   "minimal_decode": p.get("minimal_decode"), "truth_modes": p.get("truth_modes", []),
                   "operators": p.get("operators", []), "proposed_by": "deepseek-chat (semantic, AI-proposed)", "validated_by": "nabla.py (deterministic)"}
        except Exception as e: nab = {"status": "FAILED", "error": str(e)}
    paper = reg.data["papers"][pid]
    side = {
      "record_type": "QUICK_CALL_HEADER", "schema": "000_QUICK_CALL v0.1",
      "created_at": datetime.now(timezone.utc).isoformat(),
      "identity": {"paper_uuid": pid, "version_uuid": identity.version_uuid(sha), "version_n": next(v["n"] for v in paper["versions"] if v["sha256"] == sha),
                   "source_sha256": sha, "source_file": os.path.basename(path), "original_copy": orig, "new_version": new},
      "branch": {"series": series, "position": position, "of": of},
      "master_equation_id": me_id,
      "nabla": nab,
      "knowledge_graph": {"node_type": None, "q7_dimension": None, "edge_types": [],
                          "note": "filled by CKG station; allowed values in stations.yaml"},
      "lifecycle": {"current_stage": "intake", "stations_done": ["000_QUICK_CALL"], "stations_skipped": []},
      "ladder": {"1_uuid": "which object", "2_nabla_title": "what kind / read it?", "3_lossless_summary": "1/20 compaction - pending", "4_paper": "source"},
    }
    os.makedirs(STATION, exist_ok=True)
    out = os.path.join(STATION, f"{stem}__{pid[:8]}.yaml")
    open(out, "w", encoding="utf-8").write("# Sidecar - tied to the paper, never inside it. Header for every API call.\n" + yaml_dump(side) + "\n")
    print(f"[{nab['status']}] {stem}  paper {pid[:8]}  v{side['identity']['version_n']}  -> {out}")
    if nab.get("address"): print("   " + nab["address"])
    return side

if __name__ == "__main__":
    a = argparse.ArgumentParser(); a.add_argument("file"); a.add_argument("--series"); a.add_argument("--position", type=int)
    a.add_argument("--of", type=int); a.add_argument("--me-id"); a.add_argument("--parent"); a.add_argument("--no-ai", action="store_true")
    x = a.parse_args(); run(x.file, x.series, x.position, x.of, x.me_id, x.parent, not x.no_ai)
