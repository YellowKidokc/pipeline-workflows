"""Paper identity. The ONE place paper UUIDs are minted (the missing uuid_registry).
paper_uuid  : minted once (uuid4), permanent, survives every edit.
version_uuid: uuid5(CKG_NAMESPACE, 'paper-version:' + sha256) - same formula every station already uses."""
import hashlib, json, os, uuid
from datetime import datetime, timezone
CKG_NAMESPACE = uuid.UUID("8121b19c-b135-4b14-ae07-806757692169")

def version_uuid(sha): return str(uuid.uuid5(CKG_NAMESPACE, "paper-version:" + sha))

class Registry:
    def __init__(self, path):
        self.path = path
        self.data = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {"papers": {}, "by_sha": {}, "by_stem": {}}
    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        tmp = self.path + ".tmp"
        json.dump(self.data, open(tmp, "w", encoding="utf-8"), indent=2); os.replace(tmp, self.path)
    def resolve(self, sha, stem, parent_uuid=None):
        """Same bytes -> same paper. Same stem or explicit parent -> new version of that paper. Else mint."""
        d = self.data
        if sha in d["by_sha"]: return d["by_sha"][sha], False
        pid = parent_uuid or d["by_stem"].get(stem) or str(uuid.uuid4())
        p = d["papers"].setdefault(pid, {"paper_uuid": pid, "first_seen": datetime.now(timezone.utc).isoformat(), "versions": []})
        prev = p["versions"][-1]["chain_hash"] if p["versions"] else "0" * 64
        v = {"n": len(p["versions"]) + 1, "sha256": sha, "version_uuid": version_uuid(sha), "file": stem,
             "at": datetime.now(timezone.utc).isoformat(), "prev": prev}
        v["chain_hash"] = hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest()
        p["versions"].append(v); d["by_sha"][sha] = pid; d["by_stem"][stem] = pid
        return pid, True
