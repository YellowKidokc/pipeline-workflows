from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class ConversionConfig(BaseModel):
    export_root: Path = Path("Workspace/CONVERTED")
    state_root: Path = Path("Workspace/STATE/conversion")
    markitdown_enabled: bool = True
    youtube_prefer_transcript: bool = True
    whisper_enabled: bool = False
    whisper_speaker_detection: bool = False
    whisper_model_size: str = "base"
    whisper_language: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ConvertResult(BaseModel):
    markdown: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)

