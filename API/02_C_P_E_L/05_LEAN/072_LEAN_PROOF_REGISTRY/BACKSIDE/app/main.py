from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(
    title="Lean Proof Registry",
    version="0.1.0",
    description="Governed Lean verification and separately labeled explanation reports.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "scaffold", "implementation": "CODEX_ONLINE_REQUIRED"}


@app.get("/governance")
def governance() -> dict:
    return {
        "canonical_sources": "READ_ONLY",
        "negative_controls_first": True,
        "interpretation_is_formal_consequence": False,
        "canon_authority": "HUMAN_REVIEW_REQUIRED",
        "implementation_status": "SCAFFOLD_ONLY",
    }

