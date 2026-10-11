from __future__ import annotations
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path
from ..models import ConvertResult


def timestamp(seconds):
    seconds = max(0, int(seconds))
    return f"{seconds // 3600:02d}:{seconds % 3600 // 60:02d}:{seconds % 60:02d}"


def label_segments(segments, turns):
    """Label only segments covered by one voice; mixed turns remain unresolved."""
    for segment in segments:
        start, end = float(segment['start']), float(segment['end'])
        overlaps = {}
        for a, b, speaker in turns:
            overlap = max(0., min(end, b) - max(start, a))
            if overlap:
                overlaps[speaker] = overlaps.get(speaker, 0.) + overlap
        if len(overlaps) == 1 and max(overlaps.values()) >= .8 * (end - start):
            segment['speaker'] = next(iter(overlaps))
        else:
            segment['speaker'] = 'UNRESOLVED'
    return segments


def diarize(source):
    token = os.environ.get('HF_TOKEN')
    if not token:
        raise RuntimeError('Speaker detection requires HF_TOKEN and accepted pyannote model access.')
    try:
        from pyannote.audio import Pipeline
    except ImportError as exc:
        raise RuntimeError('Optional pyannote.audio dependency is not installed.') from exc
    pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization-community-1', token=token)
    output = pipeline(str(source))
    return [(float(turn.start), float(turn.end), str(speaker))
            for turn, speaker in output.speaker_diarization]


def split_paragraphs(text, target_chars=900, max_chars=1400):
    """Build substantial sentence-aligned prose instead of caption fragments."""
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    paragraphs, current = [], []
    for sentence in sentences:
        candidate = " ".join(current + [sentence])
        if current and len(candidate) > max_chars:
            paragraphs.append(" ".join(current))
            current = [sentence]
        else:
            current.append(sentence)
        if len(" ".join(current)) >= target_chars and len(current) >= 4:
            paragraphs.append(" ".join(current))
            current = []
    if current:
        paragraphs.append(" ".join(current))
    return paragraphs


def render(source, segments, speakers, speaker_status, source_hash, model_size, language):
    title = source.stem.replace('_', ' ')
    word_count = len(re.findall(r"\b[\w’'-]+\b", " ".join(s.get('text', '') for s in segments)))
    lines = [
        '---',
        f'title: {json.dumps(title, ensure_ascii=False)}',
        'type: media_transcript',
        f'source_file: {json.dumps(str(source), ensure_ascii=False)}',
        f'source_sha256: {json.dumps(source_hash)}',
        'converted: whisper-readable-prose-v1',
        f'converted_on: {date.today().isoformat()}',
        f'whisper_model: {json.dumps(model_size)}',
        f'language: {json.dumps(language or "")}',
        'timestamp_interval_minutes: 5',
        f'words: {word_count}',
        'tags: [media, transcript, readable-prose]',
        '---', '',
        f"# {title}", '',
        f"**Source:** `{source.name}`", '',
        f"**Speaker detection:** {speaker_status}",
        f"**Detected voices:** {len(speakers) if speaker_status == 'completed' else 'not determined'}", ''
    ]
    if speakers:
        lines += ['## Speakers', ''] + [f'- {s}: identity unconfirmed' for s in speakers] + ['']
    lines += ['## Transcript', '']
    buckets = {}
    for segment in segments:
        bucket = int(float(segment['start']) // 300) * 300
        buckets.setdefault(bucket, []).append(segment)
    for bucket, grouped in sorted(buckets.items()):
        lines += [f"### {timestamp(bucket)}", '']
        if speaker_status == 'completed':
            runs = []
            for segment in grouped:
                speaker = segment.get('speaker', 'UNRESOLVED')
                if not runs or runs[-1][0] != speaker:
                    runs.append([speaker, []])
                runs[-1][1].append(segment.get('text', '').strip())
            for speaker, parts in runs:
                lines += [f"**{speaker}:**", '']
                for paragraph in split_paragraphs(" ".join(parts)):
                    lines += [paragraph, '']
        else:
            for paragraph in split_paragraphs(" ".join(s.get('text', '').strip() for s in grouped)):
                lines += [paragraph, '']
    return '\n'.join(lines).rstrip() + '\n'


def transcribe_audio_video(source: Path, *, model_size='base', language=None, speaker_detection=False):
    local_exe = Path(sys.executable).resolve().parent / ('whisper.exe' if os.name == 'nt' else 'whisper')
    exe = str(local_exe) if local_exe.exists() else shutil.which('whisper')
    if not exe:
        return ConvertResult(markdown='', warnings=['Whisper CLI is not available on PATH.'])
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix='theophysics-whisper-') as tmp:
        command = [exe, str(source), '--model', model_size, '--output_dir', tmp,
                   '--output_format', 'json', '--word_timestamps', 'True', '--verbose', 'False', '--fp16', 'False']
        if language:
            command += ['--language', language]
        env = os.environ.copy(); env['PYTHONIOENCODING'] = 'utf-8'
        try:
            result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8',
                                    errors='replace', env=env, timeout=7200)
        except subprocess.TimeoutExpired:
            return ConvertResult(markdown='', warnings=['Transcription exceeded two hours; source retained.'])
        outputs = list(Path(tmp).glob('*.json'))
        if result.returncode or not outputs:
            return ConvertResult(markdown='', warnings=['Whisper failed: ' + (result.stderr or result.stdout)[-2000:]])
        payload = json.loads(outputs[0].read_text(encoding='utf-8'))
    segments = payload.get('segments', [])
    if not segments:
        return ConvertResult(markdown='', warnings=['No timed speech segments returned.'])
    warnings, speakers = [], []
    status = 'not requested'
    if speaker_detection:
        try:
            turns = diarize(source)
            speakers = sorted({s for _, _, s in turns})
            label_segments(segments, turns)
            status = 'completed' if turns else 'unresolved'
            if not turns or any(s['speaker'] == 'UNRESOLVED' for s in segments):
                warnings.append('Some speech has unresolved or overlapping voices; review speaker assignments.')
        except Exception as exc:
            status = 'unavailable'
            warnings.append(str(exc))
    if hashlib.sha256(source.read_bytes()).hexdigest() != digest:
        return ConvertResult(markdown='', warnings=['Source changed during processing; retry after download completes.'])
    return ConvertResult(markdown=render(source, segments, speakers, status, digest, model_size,
                                         payload.get('language', language)), warnings=warnings,
        metadata={'source_format':'AUDIO_VIDEO', 'transcriber':'whisper-cli', 'model_size':model_size,
                  'source_sha256':digest, 'language':payload.get('language', language),
                  'speaker_detection':status, 'speakers':speakers,
                  'speaker_count':len(speakers) if status == 'completed' else None,
                  'review_required':bool(speaker_detection and (status != 'completed' or warnings)),
                  'segments':segments})
