"""LLM query placeholder for BIL explanations.

BIL should not require an LLM to learn preferences. Runtime deployments may add a
local LLM explanation hook; this repo-safe snapshot returns deterministic text.
"""

from __future__ import annotations


def explain_event(event: dict) -> str:
    signal = event.get("signal", "unknown")
    subject = event.get("subject", "unspecified subject")
    return f"BIL observed {signal} for {subject}."
