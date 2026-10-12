"""Small, dependency-free XLSX reader used by offline migration."""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

MAIN = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def read_workbook(path: str | Path) -> dict[str, list[dict[str, str]]]:
    result = {}
    with ZipFile(path) as archive:
        shared = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared = ["".join(t.text or "" for t in item.iter(MAIN + "t")) for item in root]
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        rel_root = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        rels = {item.attrib["Id"]: item.attrib["Target"] for item in rel_root}
        for sheet in workbook.find(MAIN + "sheets"):
            target = rels[sheet.attrib[RID]].lstrip("/")
            if not target.startswith("xl/"):
                target = "xl/" + target
            xml = ET.fromstring(archive.read(target))
            rows = []
            for row in xml.findall(".//" + MAIN + "sheetData/" + MAIN + "row"):
                values = {"_row": row.attrib["r"]}
                for cell in row.findall(MAIN + "c"):
                    column = re.match(r"[A-Z]+", cell.attrib["r"]).group()
                    node = cell.find(MAIN + "v")
                    value = "" if node is None else (node.text or "")
                    if cell.attrib.get("t") == "s" and value:
                        value = shared[int(value)]
                    elif cell.attrib.get("t") == "inlineStr":
                        value = "".join(t.text or "" for t in cell.iter(MAIN + "t"))
                    values[column] = value
                rows.append(values)
            result[sheet.attrib["name"]] = rows
    return result
