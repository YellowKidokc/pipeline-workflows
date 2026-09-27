from pathlib import Path
import json, sys
p=Path(__file__).resolve().parents[1]
for d in "INPUT OUTPUT REVIEW ARCHIVE ERROR CONFIG PREFS PROMPTS SCRIPTS LOGS".split():
 print(("OK " if (p/d).is_dir() else "MISSING ")+d)
json.loads((p/"CONFIG/config.json").read_text())
print("Python",sys.version)
