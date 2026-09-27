"""Portable two-stage watched queues. Paths are workspace-relative."""
import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import shutil
import time
from uuid import uuid4
from .routing import route, ROUTES
from .processing import extract, render, sentences
from .stages import DEFAULT_STAGES, run_stages
from .connections import rebuild
from .paths import inside, relative, portable_jobs


def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_name(path.name+'.'+uuid4().hex+'.tmp')
    tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    try:
        for attempt in range(10):
            try:
                os.replace(tmp,path)
                break
            except PermissionError:
                if attempt==9:raise
                time.sleep(.1*(attempt+1))
    finally:
        with contextlib.suppress(OSError):tmp.unlink(missing_ok=True)

@contextlib.contextmanager
def lock(path):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a+b') as f:
        f.seek(0)
        if not f.read(1):f.write(b'0');f.flush()
        f.seek(0)
        if os.name=='nt':
            import msvcrt
            msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK,1)
        else:
            import fcntl
            fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
        try:yield
        finally:
            f.seek(0)
            if os.name=='nt':msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK,1)
            else:fcntl.flock(f,fcntl.LOCK_UN)

def init(workspace):
    workspace.mkdir(parents=True,exist_ok=True)
    config=workspace/'pipeline.json'
    if not config.exists():
        save(config,{'version':1,'model':'deepseek-chat','routing_chunk_chars':24000,'settle_seconds':3,
                     'poll_seconds':3,'categories':{},'notes':'All directories resolve relative to this file. API key is environment-only.'})
    for folder in ['DROP','STATE','OBSIDIAN_READY','ORIGINALS']:
        (workspace/folder).mkdir(exist_ok=True)
    for name in sorted(ROUTES):
        folder=workspace/'WORKFLOWS'/name
        for child in ['INPUT','OUTPUT','REVIEW']:(folder/child).mkdir(parents=True,exist_ok=True)
        definition=folder/'workflow.json'
        if not definition.exists():save(definition,{'route':name,'stages':DEFAULT_STAGES + [] if name != 'prompt' else [*DEFAULT_STAGES[:-1], 'prompt_structure', 'obsidian_note']})
    return config

def process_packet(packet, workspace):
    manifest=json.loads((packet/'job.json').read_text(encoding='utf-8'))
    route_name=manifest['route']; digest=manifest['sha256']
    if route_name=='review':return {'status':'review','reason':'Router requested review'}
    source=inside(packet,manifest['source_name'])
    if hashlib.sha256(source.read_bytes()).hexdigest()!=digest:raise ValueError('Packet source hash changed')
    definition=json.loads((workspace/'WORKFLOWS'/route_name/'workflow.json').read_text(encoding='utf-8'))
    output=workspace/'WORKFLOWS'/route_name/'OUTPUT'/digest
    output.mkdir(parents=True,exist_ok=True)
    notes=[]
    config=json.loads((workspace/'pipeline.json').read_text(encoding='utf-8'))
    save(workspace/'STATE'/'link-refresh.json',{'pending':True})
    for index,video in enumerate(extract(source)):
        if video['title']==source.stem:
            video['title']=Path(relative(manifest.get('original_name',source.name))).stem
        context=run_stages(video, manifest['categories'], definition, config)
        analysis=context['analysis']
        note_id=digest[:16]+f'-{index+1:03d}'
        title=''.join(c if c.isalnum() or c in ' -_' else ' ' for c in video['title'])[:90].strip() or 'Untitled'
        name=f'{title}--{note_id}.md'
        context['extras']['Related material']=[f'[[Links/{note_id}|Explore related passages]]']
        content=render(video,analysis,digest,route_name,context['extras'])
        temp=output/(name+'.tmp');temp.write_text(content,encoding='utf-8');os.replace(temp,output/name)
        save(output/(note_id+'.analysis.json'),{**analysis,'signals':context.get('signals',{}),'stages':context['executed_stages']})
        # Generated files only, deterministically named. Original source never overwritten.
        target=workspace/'OBSIDIAN_READY'/name
        tmp=target.with_suffix('.tmp');tmp.write_text(content,encoding='utf-8');os.replace(tmp,target)
        notes.append(target.relative_to(workspace).as_posix())
        save(workspace/'STATE'/'documents'/(note_id+'.json'),{'id':note_id,'title':video['title'],'source_sha256':digest,
             'note':target.relative_to(workspace).as_posix(), 'text':video['text'],'passages':sentences(video['text']), 'route':route_name})
    return {'status':'completed','notes':notes,'source_sha256':digest}

def tick(workspace, classifier=route, now=None):
    workspace=Path(workspace).resolve(); config_path=init(workspace)
    config=json.loads(config_path.read_text(encoding='utf-8'));clock=time.time() if now is None else now
    with lock(workspace/'STATE'/'pipeline.lock'):
        statefile=workspace/'STATE'/'jobs.json'
        state=portable_jobs(json.loads(statefile.read_text(encoding='utf-8'))) if statefile.exists() else {}
        for source in sorted((workspace/'DROP').rglob('*')):
            if not source.is_file() or source.is_symlink() or source.suffix.lower() not in {'.md','.txt','.srt','.vtt'}:continue
            if not source.resolve().is_relative_to(workspace/'DROP'):continue
            name=source.relative_to(workspace/'DROP').as_posix()
            signature=[source.stat().st_size,source.stat().st_mtime_ns]
            prior=state.get(name,{})
            if prior.get('signature')!=signature:
                state[name]={'signature':signature,'status':'settling','seen':clock,'previous':{k:v for k,v in prior.items() if k!='previous'}};save(statefile,state);continue
            if prior['status']!='settling' or clock-prior['seen']<config['settle_seconds']:continue
            try:
                data=source.read_bytes()
            except OSError as exc:
                prior.update(status='failed',error=str(exc));save(statefile,state);continue
            if [source.stat().st_size,source.stat().st_mtime_ns]!=signature:continue
            digest=hashlib.sha256(data).hexdigest()
            previous=prior.get('previous',{})
            if previous.get('sha256')==digest and previous.get('status')=='completed':
                state[name]={**previous,'signature':signature};save(statefile,state);continue
            # Content duplicates reuse completed receipts and never bill again.
            completed=next((v for k,v in state.items() if v.get('sha256')==digest and v.get('status')=='completed'),None)
            if completed:
                prior.update(status='completed',sha256=digest,duplicate_of=completed.get('packet'));save(statefile,state);continue
            prior.update(status='routing',sha256=digest);save(statefile,state)
            try:
                decision=classifier(data.decode('utf-8-sig'),source.name,config)
                if decision['route'] not in ROUTES:raise ValueError('Unknown routing destination')
                packet=workspace/'WORKFLOWS'/decision['route']/'INPUT'/digest
                packet.mkdir(parents=True,exist_ok=True)
                original=packet/('source'+source.suffix.lower())
                if original.exists() and original.read_bytes()!=data:raise ValueError('Source collision')
                original.write_bytes(data)
                archive=workspace/'ORIGINALS'/digest
                archive.mkdir(exist_ok=True)
                archived=archive/original.name
                if archived.exists() and archived.read_bytes()!=data:raise ValueError('Archive collision')
                archived.write_bytes(data)
                save(packet/'routing.json',decision)
                save(packet/'job.json',{'route':decision['route'],'categories':decision['categories'],
                     'sha256':digest,'source_name':original.name,'original_name':name})
                prior.update(status='queued',packet=packet.relative_to(workspace).as_posix());save(statefile,state)
            except Exception as exc:
                prior.update(status='failed',error=str(exc));save(statefile,state)
        changed=False
        # Each route has its own input queue. Process only receipt-backed queued packets.
        for name,job in state.items():
            if job.get('status')!='queued':continue
            job['status']='processing';save(statefile,state)
            try:
                job.update(process_packet(inside(workspace,job['packet']),workspace))
                changed=changed or job['status']=='completed'
            except Exception as exc:job.update(status='failed',error=str(exc))
            save(statefile,state)
        refresh=workspace/'STATE'/'link-refresh.json'
        if changed or (refresh.exists() and json.loads(refresh.read_text(encoding='utf-8')).get('pending')):
            rebuild(workspace)
            save(refresh,{'pending':False})
        return state

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command',choices=['init','once','watch','status','retry','stop','relink','resolve','reprocess'])
    ap.add_argument('--workspace',type=Path,default=Path.cwd()/'Workspace')
    ap.add_argument('--job',help='Exact source-relative job name for explicit retry')
    ap.add_argument('--route', choices=sorted(ROUTES-{'review'}))
    args=ap.parse_args(argv)
    if args.job:args.job=relative(args.job)
    workspace=args.workspace.resolve();init(workspace)
    if args.command=='stop':
        (workspace/'STATE'/'stop.request').touch();print('Stop requested; current job will finish.');return
    if args.command=='relink':
        with lock(workspace/'STATE'/'pipeline.lock'):
            print(rebuild(workspace))
            save(workspace/'STATE'/'link-refresh.json',{'pending':False})
        return
    if args.command=='init':print(workspace/'DROP');return
    if args.command=='status':
        p=workspace/'STATE'/'jobs.json';print(p.read_text(encoding='utf-8') if p.exists() else '{}');return
    if args.command in {'resolve','reprocess'}:
        with lock(workspace/'STATE'/'pipeline.lock'):
            p=workspace/'STATE'/'jobs.json';state=portable_jobs(json.loads(p.read_text(encoding='utf-8'))) if p.exists() else {}
            if args.command=='resolve':
                if not args.job or not args.route:ap.error('resolve requires --job and --route')
                job=state[args.job]
                if job['status']!='review':raise ValueError('Resolve applies to review jobs only')
                source_packet=inside(workspace,job['packet'])
                manifest=json.loads((source_packet/'job.json').read_text(encoding='utf-8'))
                dest=workspace/'WORKFLOWS'/args.route/'INPUT'/job['sha256']
                dest.mkdir(parents=True,exist_ok=True)
                raw=(source_packet/manifest['source_name']).read_bytes()
                target=dest/manifest['source_name']
                if target.exists() and target.read_bytes()!=raw:raise ValueError('Packet collision')
                target.write_bytes(raw)
                save(dest/'routing.json',{'route':args.route,'resolution':'explicit operator selection','original_receipt':(source_packet/'routing.json').relative_to(workspace).as_posix()})
                save(dest/'job.json',{**manifest,'route':args.route})
                job.update(status='queued',packet=dest.relative_to(workspace).as_posix())
            else:
                for name,job in state.items():
                    if args.job and name!=args.job:continue
                    if not job.get('packet') or job['status']!='completed':continue
                    if args.route and Path(job['packet']).parts[1]!=args.route:continue
                    job['status']='queued'
            save(p,state)
        return
    if args.command=='retry':
        if not args.job:ap.error('retry requires --job')
        with lock(workspace/'STATE'/'pipeline.lock'):
            p=workspace/'STATE'/'jobs.json';state=portable_jobs(json.loads(p.read_text(encoding='utf-8'))) if p.exists() else {}
            job=state[args.job]
            if job['status'] not in {'failed','routing','processing','review'}:raise ValueError('Only interrupted/failed/review jobs can be retried')
            job['status']='queued' if job.get('packet') else 'settling'
            save(p,state)
        return
    if args.command=='once':
        print(json.dumps(tick(workspace),indent=2));return
    with lock(workspace/'STATE'/'worker.lock'):
        stop=workspace/'STATE'/'stop.request'
        if stop.exists():stop.unlink()
        runtime=workspace/'STATE'/'worker.json'
        last_message=None
        try:
            while not stop.exists():
                try:
                    save(runtime,{'pid':os.getpid(),'status':'working','heartbeat':time.time()})
                    state=tick(workspace)
                    save(runtime,{'pid':os.getpid(),'status':'watching','heartbeat':time.time(),
                                  'jobs':{k:v['status'] for k,v in state.items()}})
                    message=json.dumps({k:v['status'] for k,v in state.items()})
                except Exception as exc:
                    with contextlib.suppress(OSError):
                        save(runtime,{'pid':os.getpid(),'status':'error','heartbeat':time.time(),'error':str(exc)})
                    message=str(exc)
                if message!=last_message:
                    print(message,flush=True)
                    last_message=message
                interval=float(json.loads((workspace/'pipeline.json').read_text(encoding='utf-8'))['poll_seconds'])
                until=time.monotonic()+max(1,interval)
                while time.monotonic()<until and not stop.exists():time.sleep(.2)
        except KeyboardInterrupt:
            pass
        finally:
            with contextlib.suppress(OSError):
                save(runtime,{'pid':os.getpid(),'status':'stopped','heartbeat':time.time()})

if __name__=='__main__':main()
