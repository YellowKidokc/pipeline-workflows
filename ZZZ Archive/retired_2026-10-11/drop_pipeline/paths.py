"""Portable receipt paths, including older Windows-created workspaces."""
from pathlib import Path, PurePosixPath


def relative(value):
    text=str(value).replace('\\', '/')
    parts=PurePosixPath(text)
    if parts.is_absolute() or '..' in parts.parts or ':' in text:
        raise ValueError('Receipt path must stay inside the workspace')
    return parts.as_posix()


def inside(root, value):
    root=Path(root).resolve()
    target=root/relative(value)
    if not target.resolve().is_relative_to(root):
        raise ValueError('Receipt path escapes the workspace')
    return target


def portable_jobs(state):
    result={}
    for name, original in state.items():
        job=dict(original)
        for field in ('packet','duplicate_of'):
            if job.get(field): job[field]=relative(job[field])
        if 'notes' in job: job['notes']=[relative(p) for p in job['notes']]
        if job.get('previous'):
            previous=dict(job['previous']); previous.pop('previous',None)
            job['previous']=portable_jobs({'previous':previous})['previous']
        result[relative(name)]=job
    return result
