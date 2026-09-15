import importlib.util, json
from pathlib import Path

def module(path,name):
 spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def test_split_parse_clean_and_note(tmp_path):
 r=module(Path('workflows/YouTubeChannelRefinery/SCRIPTS/run_pipeline.py'),'refinery')
 source=tmp_path/'channel_Test.md'; source.write_text('''# Test Channel - Videos\n**Total Videos:** 2\n\n## 1. First: Video?\n\n**Video ID:** abc123\n**URL:** https://www.youtube.com/watch?v=abc123\n**Transcript Language:** English\n\n### Transcript\n\nUm Gary spoke about 1 Corinthians 15:3-7. [music] It happened in AD 30.\n\n---\n## 2. Silent\n\n**Video ID:** def\n**URL:** https://youtu.be/def\n\n---\n''',encoding='utf-8')
 channel,videos=r.parse(source)
 assert channel=='Test Channel' and len(videos)==2 and videos[1]['transcript']==''
 clean=r.clean_text(videos[0]['transcript'],{'remove_stage_directions':True,'remove_fillers':True,'paragraph_words':200})
 assert '[music]' not in clean and not clean.lower().startswith('um ')
 note=r.note(channel,videos[1],'general')
 assert 'status: "no_transcript"' in note and '# Chapter 002' in note

def test_watcher_dry_run_and_undo(tmp_path):
 w=module(Path('tools/drop_watcher/drop_watcher.py'),'watcher')
 src=tmp_path/'a.md'; src.write_text('hello'); cfg={'rules':[{'name':'m','match':'*.md','actions':[{'move':str(tmp_path/'done/') }]}]}
 watcher=w.Watcher(tmp_path,cfg,True); watcher.scan(); assert src.exists() and not (tmp_path/'done/a.md').exists()
 watcher=w.Watcher(tmp_path,cfg,False); watcher.scan(); dst=tmp_path/'done/a.md'; assert dst.exists()
 assert w.undo(tmp_path,1)==0 and src.exists()

def test_schema_is_json_and_profiles_exist():
 schema=json.loads(Path('schemas/youtube_chapter.schema.json').read_text())
 assert schema['properties']['status']['enum']
 assert {x.stem for x in Path('workflows/YouTubeChannelRefinery/PROMPTS/profiles').glob('*.md')} >= {'general','christian','conspiracy','science'}
