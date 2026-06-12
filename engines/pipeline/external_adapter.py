"""
external_adapter.py — Bridge between pipeline engine and X:\\Backside stations.

The pipeline engine has its own station implementations in engines/pipeline/stations/.
The REAL stations live on X:\\Backside with RUN.bat files and 23/47 passing canary.

This adapter wraps an external station's RUN.bat into a StationBase subclass
so the pipeline engine can run both internal Python stations AND external
Backside stations through the same interface.

Usage:
    from engines.pipeline.external_adapter import ExternalStationAdapter

    station = ExternalStationAdapter.from_registry("claim-extractor")
    engine.register_station(station, pipeline_name="paper-analysis")
"""

import json
import subprocess
import shutil
import logging
import os
import re
import sys
from pathlib import Path
from typing import Optional

from .station_base import StationBase, StationVerdict, Manifest, SignalType

logger = logging.getLogger("FORGE.adapter")
PACKET_LEVEL_STATIONS = {"file-intelligence", "preference-engine", "classify-documents"}


class ExternalStationAdapter(StationBase):
    """
    Wraps an X:\\Backside station with RUN.bat into a StationBase-compatible object.
    The pipeline engine sees it as just another station.
    """

    def __init__(
        self,
        name: str,
        station_path: str,
        input_dir: str,
        output_dir: str,
        has_run_bat: bool = True,
        file_extensions: Optional[list] = None,
        timeout_seconds: int = 300,
        **kwargs,
    ):
        super().__init__(
            name=name,
            input_dir=input_dir,
            output_dir=output_dir,
            file_extensions=file_extensions or ["*"],
            **kwargs,
        )
        self.station_path = Path(station_path)
        self.has_run_bat = has_run_bat
        self.timeout_seconds = timeout_seconds
        self.run_bat = self._find_run_script()

    def _find_run_script(self) -> Path:
        for name in ("RUN.bat", "START_BIL.bat", "RUN_PIPELINE.bat", "run.bat"):
            candidate = self.station_path / name
            if candidate.exists():
                return candidate
        return self.station_path / "RUN.bat"

    @classmethod
    def from_registry(
        cls,
        station_name: str,
        registry_path: str = None,
        config_path: str = None,
    ) -> "ExternalStationAdapter":
        """
        Build an adapter from STATION_REGISTRY.json entry.

        Args:
            station_name: Key in the registry
            registry_path: Path to STATION_REGISTRY.json
            config_path: Path to pipeline.config.json
        """
        if registry_path is None:
            # Default: look relative to this file's repo root
            repo_root = Path(__file__).resolve().parent.parent.parent
            registry_path = repo_root / "stations" / "STATION_REGISTRY.json"

        with open(registry_path, "r", encoding="utf-8") as f:
            registry = json.load(f)

        entry = registry.get("stations", {}).get(station_name)
        if not entry:
            raise ValueError(f"Station '{station_name}' not found in registry")

        station_path = Path(entry["path"])
        input_dir = str(station_path / "INPUT")
        output_dir = str(station_path / "OUTPUT")
        timeout_seconds = int(entry.get("timeout_seconds", 300))
        # Some stations use DROP_PAPERS_HERE instead of INPUT
        if not Path(input_dir).exists():
            alt_input = station_path / "DROP_PAPERS_HERE"
            if alt_input.exists():
                input_dir = str(alt_input)
            else:
                # Create INPUT if nothing exists
                Path(input_dir).mkdir(parents=True, exist_ok=True)

        if not Path(output_dir).exists():
            Path(output_dir).mkdir(parents=True, exist_ok=True)

        return cls(
            name=station_name,
            station_path=str(station_path),
            input_dir=input_dir,
            output_dir=output_dir,
            has_run_bat=entry.get("has_run_bat", True),
            timeout_seconds=timeout_seconds,
        )

    def process(self, file_path: Path, manifest: Manifest) -> tuple[StationVerdict, float, str]:
        """
        Run the external station's RUN.bat against the input file.

        Strategy:
        1. Copy file into station's INPUT dir (nothing original destroyed)
        2. Run RUN.bat
        3. Check OUTPUT dir for results
        4. Return verdict based on what happened
        """
        packet = packet_path(manifest)
        if self.name in PACKET_LEVEL_STATIONS:
            marker = packet / "LOGS" / f"{self.name}.packet.done" if packet else None
            if marker and marker.exists():
                return StationVerdict.PASS, 1.0, f"{self.name} already ran for packet"

        file_hash = manifest.file_hash or Manifest.compute_hash(str(file_path))
        file_marker = done_marker(packet, self.name, file_hash)
        if file_marker and file_marker.exists():
            return StationVerdict.PASS, 1.0, f"Idempotency: already processed (hash={file_hash})"

        # 1. Copy input file to station's INPUT dir (NEVER move originals)
        station_input = self.station_path / "INPUT"
        station_input.mkdir(parents=True, exist_ok=True)
        dest_file = station_input / file_path.name
        shutil.copy2(str(file_path), str(dest_file))

        archive = self.station_path / "ARCHIVE"
        if archive.exists():
            for archived in archive.iterdir():
                if archived.is_file():
                    try:
                        if Manifest.compute_hash(str(archived)) == file_hash:
                            mark_done(file_marker)
                            return StationVerdict.PASS, 1.0, f"Idempotency: already processed (hash={file_hash})"
                    except Exception:
                        continue

        # 2. Run station entrypoint. Batch stations get the packet contract via env;
        # Python module stations receive the concrete file and packet output path.
        try:
            before = snapshot_files(self.station_path / "OUTPUT") | snapshot_files(packet / "OUTPUT" if packet else None)
            result = self._run_entrypoint(dest_file, manifest)
            exit_code = result.returncode
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()
            fis_errors = re.search(r"Errors:\s*([1-9]\d*)", stdout + "\n" + stderr)
            if self.name == "file-intelligence" and ("[E]" in stdout or "[E]" in stderr or fis_errors):
                exit_code = 1
        except subprocess.TimeoutExpired:
            self.emit_signal(
                SignalType.ERROR,
                f"Station {self.name} timed out after {self.timeout_seconds}s",
            )
            return StationVerdict.HOLD, 0.0, f"Timeout after {self.timeout_seconds}s"
        except Exception as e:
            self.emit_signal(SignalType.ERROR, f"Station {self.name} execution error: {e}")
            return StationVerdict.FAIL, 0.0, f"Execution error: {e}"

        # 3. Check for output
        station_output = self.station_path / "OUTPUT"
        packet_output = packet / "OUTPUT" if packet else None
        after = snapshot_files(station_output) | snapshot_files(packet_output)
        new_outputs = sorted(after - before)

        if exit_code == 0:
            notes = f"Exit 0. stdout={stdout[:200]}" if stdout else "Exit 0. No stdout."
            if stderr:
                notes += f" stderr={stderr[:200]}"
            if new_outputs:
                notes += f" outputs={len(new_outputs)}"
            mark_done(file_marker)
            self.emit_signal(SignalType.READY, f"{self.name} completed: {file_path.name}")
            return StationVerdict.PASS, 1.0, notes
        elif exit_code == 2:
            # Convention: exit 2 = needs review
            return StationVerdict.REVIEW, 0.5, f"Exit 2 (review). {stdout[:200]}"
        else:
            self.emit_signal(
                SignalType.ERROR,
                f"{self.name} failed with exit {exit_code}: {stderr[:200]}",
            )
            return StationVerdict.FAIL, 0.0, f"Exit {exit_code}. stderr={stderr[:200]}"

    def _run_entrypoint(self, dest_file: Path, manifest: Manifest) -> subprocess.CompletedProcess:
        packet = packet_path(manifest)
        if self.name in PACKET_LEVEL_STATIONS:
            marker = packet / "LOGS" / f"{self.name}.packet.done" if packet else None
            if marker and marker.exists():
                return subprocess.CompletedProcess(args=[], returncode=0, stdout=f"{self.name} already ran for packet", stderr="")
        else:
            marker = None
        env = dict(os.environ)
        env["FORGE_INPUT"] = str((packet / "INPUT") if packet else self.input_dir)
        env["FORGE_OUTPUT"] = str((packet / "OUTPUT") if packet else self.output_dir)
        env["FORGE_PACKET"] = str(packet or "")
        env["FORGE_FILE"] = str(dest_file)
        env["PYTHONUTF8"] = "1"
        pipeline_py = self.station_path / "pipeline.py"
        if self.name == "file-intelligence":
            result = self._run_file_intelligence(packet, env)
            if marker and result.returncode == 0:
                marker.write_text("ok", encoding="utf-8")
            return result
        if pipeline_py.exists():
            result = self._run_pipeline_py(packet, env)
            if marker and self.name in PACKET_LEVEL_STATIONS and result.returncode == 0:
                marker.write_text("ok", encoding="utf-8")
            return result
        if self.run_bat.exists():
            cmd = ["cmd.exe", "/d", "/c", str(self.run_bat)]
            if self.name == "file-intelligence":
                cmd.extend(["backfill", "--path", str((packet / "INPUT") if packet else self.input_dir)])
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                cwd=str(self.station_path),
                env=env,
            )
            if marker and self.name in PACKET_LEVEL_STATIONS and result.returncode in {0, 2}:
                marker.write_text("ok", encoding="utf-8")
            return result
        pyproject = self.station_path / "pyproject.toml"
        convert_module = self.station_path / "src" / "theophysics_conversion" / "convert.py"
        if pyproject.exists() and convert_module.exists():
            existing = env.get("PYTHONPATH", "")
            env["PYTHONPATH"] = str(self.station_path / "src") + (os.pathsep + existing if existing else "")
            return subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "theophysics_conversion.convert",
                    str(dest_file),
                    "--export-root",
                    str((packet / "OUTPUT") if packet else self.output_dir),
                ],
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                cwd=str(self.station_path),
                env=env,
            )
        self.emit_signal(SignalType.ERROR, f"Station {self.name} has no runnable entrypoint at {self.station_path}")
        return subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr=f"No runnable entrypoint in {self.station_path}")

    def _run_file_intelligence(self, packet: Optional[Path], env: dict[str, str]) -> subprocess.CompletedProcess:
        existing = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = str(self.station_path) + (os.pathsep + existing if existing else "")
        return subprocess.run(
            [sys.executable, "-m", "fis.backfill", "--path", str((packet / "INPUT") if packet else self.input_dir)],
            capture_output=True,
            text=True,
            timeout=self.timeout_seconds,
            cwd=str(self.station_path),
            env=env,
        )

    def _run_pipeline_py(self, packet: Optional[Path], env: dict[str, str]) -> subprocess.CompletedProcess:
        config_path = self.station_path / "config.json"
        original = None
        if config_path.exists():
            original = config_path.read_text(encoding="utf-8")
            try:
                config = json.loads(original)
            except json.JSONDecodeError:
                config = {}
        else:
            config = {}
        config["input_dir"] = str((packet / "INPUT") if packet else self.input_dir)
        config["output_dir"] = str((packet / "OUTPUT" / self.name) if packet else self.output_dir)
        config.setdefault("text_extensions", [".txt", ".md", ".html"])
        if ".html" not in config.get("text_extensions", []):
            config["text_extensions"] = list(config.get("text_extensions", [])) + [".html"]
        try:
            config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(self.station_path / "pipeline.py")],
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                cwd=str(self.station_path),
                env=env,
            )
        finally:
            if original is not None:
                config_path.write_text(original, encoding="utf-8")
            elif config_path.exists():
                config_path.unlink()

    def __repr__(self):
        return f"<ExternalStation:{self.name} path={self.station_path} run_bat={self.has_run_bat}>"


def packet_path(manifest: Manifest) -> Optional[Path]:
    packet = manifest.metadata.get("packet")
    return Path(packet) if packet else None


def done_marker(packet: Optional[Path], station_name: str, file_hash: str) -> Optional[Path]:
    if not packet:
        return None
    return packet / "LOGS" / f"{station_name}.{file_hash}.done"


def mark_done(marker: Optional[Path]) -> None:
    if not marker:
        return
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("ok", encoding="utf-8")


def snapshot_files(path: Optional[Path]) -> set[str]:
    if not path or not path.exists():
        return set()
    return {str(file_path) for file_path in path.rglob("*") if file_path.is_file()}
