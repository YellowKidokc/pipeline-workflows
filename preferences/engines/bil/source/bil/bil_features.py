"""Feature extraction for optional BIL online learning."""

from __future__ import annotations

from urllib.parse import urlparse


def browser_features(event: dict) -> dict[str, float | str]:
    """Extract lightweight browser preference features from an event payload."""

    metadata = event.get("metadata") or {}
    url = metadata.get("url", "")
    parsed = urlparse(url)
    return {
        "source": event.get("source", ""),
        "signal": event.get("signal", ""),
        "domain": parsed.netloc,
        "has_subject": 1.0 if event.get("subject") else 0.0,
        "dwell_seconds": float(metadata.get("dwell_seconds", 0) or 0),
        "scroll_depth": float(metadata.get("scroll_depth", 0) or 0),
    }


def manual_features(event: dict) -> dict[str, float | str]:
    """Extract features from approval/correction events."""

    return {
        "source": event.get("source", ""),
        "signal": event.get("signal", ""),
        "workflow": event.get("workflow", ""),
        "station": event.get("station", ""),
        "weight": float(event.get("weight", 0) or 0),
    }
