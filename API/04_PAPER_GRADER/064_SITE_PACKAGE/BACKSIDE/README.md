# 64_SITE_PACKAGE

The last step of `063_PAPER_AUDIT`: every audited paper gets a home, so a whole series can become pages on the website.
Each part of a series is audited on its own; each time a part comes through, its page is built (an earlier version moves to
`99_archive\superseded\<date>\`) and the series title page is rebuilt from every part it has.

```
<site_root>\
  00_ALL_SERIES_INDEX.md / .html / .csv
  01_<series>\
    00_manifest.md / .html             the series title page: every part in order, readiness, which stations ran
    01_<part>.md / .html               one part: the paper, then every audit result (HTML: one fold-out per station)
    01_text\canonical\                 the source as audited
    03_nlp_api\<NN_STATION>\<part>\    every file each station wrote
    04_data\json\   04_data\excel\
    05_site_build\html\                the page HTML, ready for the site build
    99_archive\superseded\             earlier versions, never deleted
    02_media  06_inbox_imports  07_exports  98_file_intelligence   (empty until used)
  00_STANDALONE\                       papers that are not part of a series: the same shape, one page each
```

**Series or not:** the note's YAML `series` / `part` (written by the title step), else the folder it was dropped in
(`INBOX\01_SERIES\<series name>\`), else it is standalone. The part number comes from YAML, else from the file name (`bgl-02` -> 2).

**Where:** `site_root` in `_system\config\paths.json`; if not set, `OUTBOX\SITE` here.

On its own: `python BACKSIDE\64_site_package.py <papers> --from <audit output folder>` (default: the papers 63 last ran,
results from 063's OUTBOX).

Next (not automated yet): copy a finished series into `faiththruphysics-site-data\<series>\` for `top_bar_bottom_bar.py`
(page-shell-builder), and the audit numbers into its `rigor\` and `claims\` JSON.
