"""md2html: the note -> a styled .html beside it (the Reusable Tools convert_markdown_to_html plugin, called as is)."""
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir()) / "_system"))
from engine.paths import configured, external  # noqa: E402

ABOUT = "note -> .html beside it (github style), via the existing convert_markdown_to_html plugin"
API = False
PLUGIN = ("Reusable_Tools_From_Theophysics/Conversions_and_Data_Tools/01_ENGINE/01_ENGINE/scripts/python_pipeline/"
          "data_command_center/scripts/convert_markdown_to_html.py")


def run(note: Path, text: str) -> dict:
    if not configured("file_tools"):
        return {"say": "file_tools is not set in _system/config/paths.json"}
    spec = importlib.util.spec_from_file_location("md2html_plugin", external("file_tools") / PLUGIN)
    plugin = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(plugin)
    out = note.with_suffix(".html")
    plugin.run({"input_md_path": str(note), "output_html_path": str(out), "template": "github"})
    return {"say": f"-> {out.name}"}
