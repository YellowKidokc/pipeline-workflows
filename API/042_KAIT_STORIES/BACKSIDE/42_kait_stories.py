"""042_KAIT_STORIES: map a paper to Kait Willett moves.

ONE_MENU.bat 69

For each input paper, make one API call that returns three alternative spines,
each beat tagged with Kait move IDs, canonical-point carry, and a structural why.
Outputs a human-readable .md and a structured .json including an OpenWriter outline.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(next(p for p in Path(__file__).resolve().parents if (p / "_system").is_dir()) / "_system"))
from engine.output import markdown_to_html, page  # noqa: E402
from engine.station import Context, ItemResult, Station  # noqa: E402

LABEL = "042_KAIT_STORIES"
HERE = Path(__file__).resolve().parent
DEFAULT_MOVES_PATH = Path("C:/Users/David/Documents/faiththruphysics.com/Canon/WRITING_METHOD/KAIT_MOVES_LIBRARY.md")


def norm_loop_id(move_id: str) -> str:
    """Convert K01/K1 shorthand to the loops.json form kait_K01."""
    s = str(move_id).strip()
    if s.startswith("kait_"):
        return s
    m = re.match(r"K?(\d{1,2})$", s, re.IGNORECASE)
    if m:
        return f"kait_K{int(m.group(1)):02d}"
    return s


def load_moves(path: Path | None) -> str:
    p = Path(path) if path else DEFAULT_MOVES_PATH
    if p.is_file():
        return p.read_text(encoding="utf-8")
    # Fallback: look next to the script
    local = HERE / "KAIT_MOVES_LIBRARY.md"
    if local.is_file():
        return local.read_text(encoding="utf-8")
    return "# Kait moves library not found. The model should use the moves described in the prompt."


def render(item, data: dict) -> str:
    out = [f"# Kait spines: {item.title}", ""]
    out += [f"**Thesis:** {data.get('thesis', '')}", ""]
    if data.get("thesis_flag"):
        out += [f"> **Thesis flag:** {data['thesis_flag']}", ""]
    out += [f"**Carry question:** {data.get('carry_question', '')}", ""]
    out += ["---", ""]

    for v in data.get("variants", []):
        out += [f"## Variant {v.get('variant_id')} — {v.get('label', '')}", ""]
        for section in ("opening", "body", "closing"):
            out += [f"### {section.capitalize()}", ""]
            for beat in v.get(section, []):
                moves = ", ".join(beat.get("move_ids", []))
                out += [f"**{beat.get('beat', '')}**  *(moves: {moves})*", ""]
                out += [f"- Canonical point: {beat.get('canonical_point', '')}", ""]
                out += [f"- Fill: {beat.get('fill', '')}", ""]
                out += [f"- Why: {beat.get('why', '')}", ""]
                out += [""]

    if data.get("loops_used"):
        out += ["## Loops used", ""] + [f"- `{x}`" for x in data["loops_used"]] + [""]
    if data.get("loops_not_used_but_relevant"):
        out += ["## Relevant loops not chosen", ""] + [f"- `{x}`" for x in data["loops_not_used_but_relevant"]] + [""]

    if data.get("openwriter_outline"):
        out += ["## OpenWriter outline", "", "| beat | label | loops | canonical point |", "|---|---|---|---|"]
        for row in data["openwriter_outline"]:
            loops = ", ".join(row.get("loop_ids", []))
            out += [f"| {row.get('id', '')} | {row.get('label', '')} | {loops} | {row.get('canonical_point', '')} |"]
        out += [""]

    return "\n".join(out)


def main() -> int:
    station = Station(LABEL, prompt_files=["PROMPT.md"])
    items = station.items()
    if station.args.dry_run or not items:
        return station.run(lambda ctx: None, items)

    moves_library = load_moves(getattr(station.args, "kait_moves", None))
    prompt_template = (HERE / "PROMPT.md").read_text(encoding="utf-8")

    def _normalize(data: dict) -> dict:
        used: set[str] = set()
        for v in data.get("variants", []):
            for section in ("opening", "body", "closing"):
                for beat in v.get(section, []):
                    beat["move_ids"] = [norm_loop_id(m) for m in beat.get("move_ids", [])]
                    used.update(beat["move_ids"])
        for row in data.get("openwriter_outline", []):
            row["loop_ids"] = [norm_loop_id(m) for m in row.get("loop_ids", [])]
            used.update(row["loop_ids"])
        data["loops_used"] = sorted(used)
        not_used = [norm_loop_id(m) for m in data.get("loops_not_used_but_relevant", []) if norm_loop_id(m) not in used]
        data["loops_not_used_but_relevant"] = not_used
        return data

    def process(ctx: Context):
        text = ctx.text
        ctx.step(f"paper: {len(text):,} characters")
        prompt = prompt_template.replace("{KAIT_MOVES_LIBRARY}", moves_library).replace("{SOURCE_PAPER}", text)
        data = ctx.cached("kait_spine", lambda: ctx.call_json("kait_spine", prompt))
        if not isinstance(data, dict):
            ctx.errors.append("kait_spine returned no JSON")
            return None
        data = _normalize(data)
        ctx.step(f"returned {len(data.get('variants', []))} variant(s)")
        md = render(ctx.item, data)
        html = page(f"Kait spines: {ctx.item.title}", markdown_to_html(md))
        return ItemResult(data, html, None, md)

    return station.run(process, items)


if __name__ == "__main__":
    raise SystemExit(main())
