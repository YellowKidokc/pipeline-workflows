"""Preference-event adapter for BIL inputs.

The adapter maps browser/folder/manual observations into the contract at
contracts/schemas/preference-event.schema.json. It has no network side effects
and is safe to import in tests or offline environments.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from .config import SIGNAL_WEIGHTS, SOURCE_ALIASES


def utc_now() -> str:
    """Return an ISO-8601 UTC timestamp for preference events."""

    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def normalize_signal(raw_signal: str) -> str:
    """Normalize package-specific signal names to preference-event signals."""

    normalized = raw_signal.strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "approval": "manual_approval",
        "approved": "manual_approval",
        "correction": "manual_correction",
        "corrected": "manual_correction",
        "reuse": "file_reused",
        "file_reuse": "file_reused",
        "copy": "copied_text",
        "copied": "copied_text",
        "bookmark": "bookmark_save",
        "save": "bookmark_save",
        "dwell": "long_dwell_scroll",
        "scroll": "long_dwell_scroll",
        "tab": "opened_tab",
        "open_tab": "opened_tab",
        "short_visit": "accidental_visit",
    }
    return aliases.get(normalized, normalized)


def normalize_source(raw_source: str) -> str:
    """Normalize a BIL emitter into the contract source field."""

    normalized = raw_source.strip().lower().replace("-", "_").replace(" ", "_")
    return SOURCE_ALIASES.get(normalized, normalized)


def build_preference_event(
    *,
    signal: str,
    source: str,
    subject: str = "",
    timestamp: str | None = None,
    weight: float | None = None,
    workflow: str = "",
    station: str = "",
    packet_id: str = "",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a preference-event payload compatible with the contract schema."""

    normalized_signal = normalize_signal(signal)
    event = {
        "event_type": "preference_event",
        "timestamp": timestamp or utc_now(),
        "source": normalize_source(source),
        "signal": normalized_signal,
        "weight": SIGNAL_WEIGHTS.get(normalized_signal, 0.0) if weight is None else weight,
    }
    if subject:
        event["subject"] = subject
    if workflow:
        event["workflow"] = workflow
    if station:
        event["station"] = station
    if packet_id:
        event["packet_id"] = packet_id
    if metadata:
        event["metadata"] = metadata
    return event
