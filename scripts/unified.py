"""Readable entry point shared by the workflow library and POF execution repo."""
from __future__ import annotations
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from engines.pipeline.pof_bridge import call_pof


def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.' + uuid4().hex + '.tmp')
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding='utf-8')
    os.replace(temp, path)


def workflow_path(name):
    path = Path(name)
    if path.is_file():
        return path.resolve()
    path = ROOT / 'workflows' / (name if name.endswith('.json') else name + '.json')
    if not path.is_file():
        raise FileNotFoundError(f'Unknown workflow: {name}')
    return path


def run_workflow(name, packet, execute=False, resume=True, registry=None, config=None, profile=None, model=None):
    definition = json.loads(workflow_path(name).read_text(encoding='utf-8'))
    if not execute:
        return {'status': 'preview', 'workflow': definition['name'], 'packet': str(Path(packet).resolve()),
                'stages': definition['stages'], 'profile_override': profile, 'model_override': model,
                'note': 'No stations, provider calls, or file operations executed.'}
    from scripts.orchestrator import Orchestrator
    packet = Path(packet).resolve()
    runner = Orchestrator(registry_path=registry, config_path=config, manifest_path=packet / 'MANIFEST.json')
    runner.config.update(pof_profile=profile, pof_model=model)
    return runner.run(workflow_path(name), packet, resume=resume)


@contextlib.contextmanager
def watcher_lock(path):
    """OS lock releases on crash; an existing lock file is not a stale lock."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('a+b') as handle:
        handle.seek(0)
        if not handle.read(1):
            handle.write(b'0'); handle.flush()
        handle.seek(0)
        if os.name == 'nt':
            import msvcrt
            msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == 'nt':
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)


def watch_once(registry_path, execute=False, runner=run_workflow, now=None):
    registry_path = Path(registry_path).resolve()
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    state_root = Path(registry.get('state_root', str(registry_path.parent / '_watch_state'))).resolve()
    watches = [w for w in registry.get('watches', []) if w.get('enabled', False)]
    if not execute:
        return {'status': 'preview', 'watches': watches, 'state_root': str(state_root)}
    timestamp = time.time() if now is None else now
    with watcher_lock(state_root / 'watch.lock'):
        state_file = state_root / 'state.json'
        state = json.loads(state_file.read_text(encoding='utf-8')) if state_file.exists() else {}
        results = []
        for watch in watches:
            source_root = Path(watch['folder']).resolve()
            if not source_root.is_dir():
                results.append({'status': 'missing_folder', 'folder': str(source_root)}); continue
            if state_root == source_root or state_root.is_relative_to(source_root):
                raise ValueError('Watcher state must be outside watched folders')
            matches = set()
            for pattern in watch.get('patterns', ['*.md', '*.txt']):
                matches.update(source_root.glob(pattern))
            for source in sorted(matches):
                if not source.is_file() or source.is_symlink() or source.name.startswith('.'):
                    continue
                if not source.resolve().is_relative_to(source_root):
                    continue
                key = hashlib.sha256((str(source.resolve()) + '|' + watch['workflow']).encode()).hexdigest()
                stat = source.stat(); signature = [stat.st_size, stat.st_mtime_ns]
                previous = state.get(key, {})
                if previous.get('signature') != signature:
                    state[key] = {'signature': signature, 'seen_at': timestamp, 'status': 'settling'}
                    continue
                if previous.get('status') != 'settling' or timestamp - previous['seen_at'] < float(watch.get('settle_seconds', 2)):
                    continue
                raw = source.read_bytes()
                if [source.stat().st_size, source.stat().st_mtime_ns] != signature:
                    continue
                digest = hashlib.sha256(raw).hexdigest()
                packet = state_root / 'packets' / (key[:12] + '-' + digest[:12])
                state[key].update(status='running', packet=str(packet), sha256=digest)
                save_json(state_file, state)  # interrupted runs never silently retry a billed request
                try:
                    dest = packet / 'INPUT' / source.name
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    if dest.exists() and dest.read_bytes() != raw:
                        raise ValueError('Existing packet source differs; explicit review needed')
                    if not dest.exists():
                        with dest.open('xb') as handle:
                            handle.write(raw)
                    if hashlib.sha256(dest.read_bytes()).hexdigest() != digest:
                        raise ValueError('Source copy hash mismatch')
                    result = runner(watch['workflow'], packet, execute=True, profile=watch.get('profile'), model=watch.get('model'))
                    state[key]['status'] = result['status']
                    results.append({'source': str(source), 'packet': str(packet), 'status': result['status']})
                except Exception as exc:
                    state[key].update(status='failed', error=str(exc))
                    results.append({'source': str(source), 'status': 'failed', 'error': str(exc)})
                save_json(state_file, state)
        save_json(state_file, state)
        return {'status': 'checked', 'results': results, 'state_file': str(state_file)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list', help='List workflows with readable descriptions')
    drop = sub.add_parser('drop', help='Portable DeepSeek routing and local Obsidian preparation')
    drop.add_argument('action', choices=['init','once','watch','status','retry','stop','relink','resolve','reprocess'])
    drop.add_argument('--workspace', default=str(ROOT / 'DropWorkspace'))
    drop.add_argument('--job')
    drop.add_argument('--route', choices=['youtube','document','prompt'])
    sub.add_parser('providers', help='List POF profiles without credentials')
    run = sub.add_parser('run', help='Preview or execute a named workflow')
    run.add_argument('workflow'); run.add_argument('packet'); run.add_argument('--execute', action='store_true')
    run.add_argument('--no-resume', action='store_true')
    run.add_argument('--profile'); run.add_argument('--model')
    watch = sub.add_parser('watch', help='Watch configured folders; preview by default')
    watch.add_argument('registry'); watch.add_argument('--execute', action='store_true'); watch.add_argument('--once', action='store_true')
    watch.add_argument('--interval', type=float, default=5)
    assess = sub.add_parser('assess-folder', help='Inspect folder tasks, optionally ask a model')
    assess.add_argument('folder'); assess.add_argument('--profile', default='deepseek'); assess.add_argument('--execute', action='store_true')
    assess.add_argument('--model')
    station = sub.add_parser('station', help='Preview or run an existing POF station')
    station.add_argument('folder'); station.add_argument('--execute', action='store_true'); station.add_argument('--profile')
    for name in ('copy', 'move', 'rename'):
        cmd = sub.add_parser(name); cmd.add_argument('source'); cmd.add_argument('destination'); cmd.add_argument('--execute', action='store_true')
    undo = sub.add_parser('undo'); undo.add_argument('count', type=int, default=1, nargs='?'); undo.add_argument('--execute', action='store_true')
    args = parser.parse_args(argv)
    if args.command == 'drop':
        from drop_pipeline.runner import main as drop_main
        values=[args.action,'--workspace',args.workspace]
        if args.job: values.extend(['--job',args.job])
        if args.route: values.extend(['--route',args.route])
        drop_main(values)
        return 0
    if args.command == 'list':
        result = {'status': 'inspected', 'workflows': []}
        for path in sorted((ROOT / 'workflows').glob('*.json')):
            value = json.loads(path.read_text(encoding='utf-8'))
            if 'stages' in value:
                result['workflows'].append({'name': value['name'], 'description': value.get('description', ''), 'stages': len(value['stages'])})
    elif args.command == 'run':
        result = run_workflow(args.workflow, args.packet, args.execute, not args.no_resume, profile=args.profile, model=args.model)
    elif args.command == 'watch':
        if args.interval < 1:
            parser.error('Watcher interval must be at least one second')
        while True:
            result = watch_once(args.registry, args.execute)
            print(json.dumps(result, ensure_ascii=False), flush=True)
            if args.once or not args.execute:
                return 0
            time.sleep(args.interval)
    elif args.command in ('copy', 'move', 'rename', 'undo'):
        values = [args.count] if args.command == 'undo' else [args.source, args.destination]
        result = call_pof({'action': 'file', 'operation': args.command, 'args': values, 'execute': args.execute})
    else:
        request = {'action': args.command, 'execute': getattr(args, 'execute', False)}
        if getattr(args, 'model', None):
            request['model'] = args.model
        if hasattr(args, 'folder'):
            request['station' if args.command == 'station' else 'folder'] = args.folder
            if args.profile:
                request['profile'] = args.profile
        result = call_pof(request)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result.get('status') in {'failed', 'partial_failure'} else 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({'status': 'failed', 'error': str(exc)})); raise SystemExit(1)
