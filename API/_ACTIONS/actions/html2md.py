"""html2md: every .html in a folder -> .md beside it (the Reusable Tools convert_html_to_markdown plugin, called as is)."""
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_system"))
from engine.paths import configured, external  # noqa: E402

ABOUT = "every .html in a folder -> .md beside it (skips ones already converted), via convert_html_to_markdown"
API = False
SCOPE = "folder"
PLUGIN = ("Reusable_Tools_From_Theophysics/Conversions_and_Data_Tools/01_ENGINE/01_ENGINE/scripts/python_pipeline/"
          "data_command_center/scripts/convert_html_to_markdown.py")


def run_folder(folder: Path) -> dict:
    if not configured("file_tools"):
        return {"say": "file_tools is not set in _system/config/paths.json"}
    spec = importlib.util.spec_from_file_location("html2md_plugin", external("file_tools") / PLUGIN)
    plugin = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plugin)
    done = skipped = 0
    for f in sorted(list(folder.glob("*.html")) + list(folder.glob("*.htm"))):
        out = f.with_suffix(".md")
        if out.exists():
            skipped += 1
            continue
        plugin.run({"input_html_path": str(f), "output_md_path": str(out)})
        done += 1
    return {"say": f"{done} converted, {skipped} already had a .md"}
