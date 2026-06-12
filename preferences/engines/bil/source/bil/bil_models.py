"""Offline-safe model facade for the P06 River hot loop.

The NAS runtime can replace this with real River estimators. The repo snapshot
keeps a tiny deterministic learner so tests and docs can reason about behavior
without starting services or storing learned artifacts.
"""

from __future__ import annotations

from collections import defaultdict


class PreferenceCounter:
    """Minimal online score accumulator shaped like a River hot-loop adapter."""

    def __init__(self) -> None:
        self._scores: dict[str, float] = defaultdict(float)

    def learn_one(self, event: dict) -> None:
        subject = event.get("subject") or event.get("signal") or "unknown"
        self._scores[str(subject)] += float(event.get("weight", 0) or 0)

    def predict_one(self, subject: str) -> float:
        return self._scores.get(subject, 0.0)

    def snapshot(self) -> dict[str, float]:
        return dict(sorted(self._scores.items()))
