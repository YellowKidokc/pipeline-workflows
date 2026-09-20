"""Process-isolated bridge to POF's existing provider and action implementations."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from .station_base import StationBase, StationVerdict

DEFAULT_POF_ROOT = Path(r'D:\GitHub\POF-Intelligence-CLI-API')


def call_pof(request, pof_root=None, timeout=600):
    root = Path(pof_root or os.environ.get('POF_ROOT') or DEFAULT_POF_ROOT)
    service = root / 'integration_service.py'
    if not service.is_file():
        raise FileNotFoundError(f'POF bridge not found: {service}; set POF_ROOT')
    response = subprocess.run([sys.executable, str(service)], input=json.dumps(request, ensure_ascii=False),
        capture_output=True, text=True, encoding='utf-8', cwd=root, timeout=timeout)
    try:
        result = json.loads(response.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError('POF returned no valid JSON response') from exc
    if response.returncode or result.get('status') == 'failed':
        raise RuntimeError(result.get('error', 'POF request failed'))
    return result


class POFReviewStation(StationBase):
    """Full-source review via any configured POF provider; never admits canon."""
    def __init__(self, name, packet, entry, config):
        packet = Path(packet)
        super().__init__(name, str(packet / 'INPUT'), str(packet / 'OUTPUT' / name),
                         review_dir=str(packet / 'REVIEW'), fail_dir=str(packet / 'ERROR'))
        self.entry, self.config = entry, config

    def process(self, file_path, manifest):
        if not file_path.is_file():
            return StationVerdict.HOLD, 0.0, 'No source file supplied'
        text = file_path.read_text(encoding='utf-8', errors='strict')
        prompt = self.entry.get('prompt', 'Reconstruct the argument, examine its support, identify the strongest objection, and state what survives. Preserve uncertainty. This is a candidate review, not canon admission.')
        result = call_pof({'action': 'evaluate', 'execute': True,
            'profile': self.config.get('pof_profile') or self.entry.get('profile', 'deepseek'),
            'model': self.config.get('pof_model') or self.entry.get('model'),
            'text': prompt + '\n\nCOMPLETE ORIGINAL SOURCE:\n' + text},
            pof_root=self.config.get('pof_root'), timeout=self.entry.get('timeout_seconds', 600))
        digest = hashlib.sha256(file_path.read_bytes()).hexdigest()
        output = self.output_dir / f'{file_path.stem}-{digest[:12]}.review.json'
        output.write_text(json.dumps({**result, 'source': str(file_path), 'source_sha256': digest,
            'canon_status': 'CANDIDATE_DRAFT'}, indent=2, ensure_ascii=False), encoding='utf-8')
        manifest.metadata['pof_review'] = str(output)
        return StationVerdict.REVIEW, 0.0, f'Candidate review written: {output}'
