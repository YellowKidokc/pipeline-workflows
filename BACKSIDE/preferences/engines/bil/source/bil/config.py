"""Configuration constants for the repo-safe BIL source snapshot.

Live endpoints and persistence paths are supplied by NAS/runtime deployment. This
module keeps only safe defaults and contract references in GitHub.
"""

PREFERENCE_EVENT_SCHEMA = "contracts/schemas/preference-event.schema.json"
DEFAULT_BIND_HOST = "127.0.0.1"
DEFAULT_PORT = 8420

SIGNAL_WEIGHTS = {
    "manual_approval": 1.0,
    "manual_correction": 1.0,
    "file_reused": 0.9,
    "copied_text": 0.8,
    "bookmark_save": 0.7,
    "long_dwell_scroll": 0.5,
    "opened_tab": 0.2,
    "accidental_visit": 0.0,
}

SOURCE_ALIASES = {
    "approval": "approval_gate",
    "correction": "correction_logger",
    "folder": "folder_observer",
    "browser": "browser_extension",
    "manual": "manual_signal",
}
