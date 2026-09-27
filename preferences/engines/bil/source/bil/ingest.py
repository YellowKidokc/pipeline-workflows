"""Ingestion helpers for browser, folder, and manual BIL observations."""

from __future__ import annotations

from .bil_api import build_preference_event


def browser_event(signal: str, url: str, title: str = "", **metadata) -> dict:
    subject = title or url
    return build_preference_event(
        signal=signal,
        source="browser_extension",
        subject=subject,
        metadata={"url": url, "title": title, **metadata},
    )


def folder_event(signal: str, path: str, **metadata) -> dict:
    return build_preference_event(
        signal=signal,
        source="folder_observer",
        subject=path,
        metadata=metadata,
    )


def manual_event(signal: str, subject: str, workflow: str = "", station: str = "", **metadata) -> dict:
    return build_preference_event(
        signal=signal,
        source="manual_signal",
        subject=subject,
        workflow=workflow,
        station=station,
        metadata=metadata,
    )
