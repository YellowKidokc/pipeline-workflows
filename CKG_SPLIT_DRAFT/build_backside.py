"""Build backside.html for a split CKG folder: calls in run order (left), selected call's template (right).

Usage: python build_backside.py <split folder>
The page is self-contained (data embedded), opens from file://, and saves edits as a downloaded ckg.json.
"""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
m = json.loads((root / "ckg.json").read_text(encoding="utf-8"))
for c in m["calls"]:
    f = root / c["folder"]
    c["prompt"] = (f / "prompt.md").read_text(encoding="utf-8") if (f / "prompt.md").exists() else ""
    c["template"] = (f / "output.md").read_text(encoding="utf-8") if (f / "output.md").exists() else ""
data = json.dumps(m, ensure_ascii=False).replace("</", "<\\/")

html = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CKG Backside</title>
<style>
:root{--bg:#f6f5f2;--panel:#fff;--ink:#1d1d1b;--mute:#6b6a66;--line:#dedcd6;--acc:#2f5d8a;--off:#b9b6ae;--sel:#e8eef5}
@media (prefers-color-scheme:dark){:root{--bg:#18191b;--panel:#202225;--ink:#e8e6e1;--mute:#9a978f;--line:#33363a;--acc:#7fb0e0;--off:#5c5a55;--sel:#26313d}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.45 system-ui,Segoe UI,sans-serif}
header{display:flex;gap:12px;align-items:center;padding:10px 16px;border-bottom:1px solid var(--line);background:var(--panel);flex-wrap:wrap}
header h1{font-size:16px;margin:0}header .v{color:var(--mute)}header .sp{flex:1}
button,select{font:inherit;padding:5px 10px;border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:6px;cursor:pointer}
button.pri{background:var(--acc);color:#fff;border-color:var(--acc)}
main{display:grid;grid-template-columns:minmax(260px,340px) 1fr;height:calc(100vh - 128px)}
@media (max-width:760px){main{grid-template-columns:1fr;height:auto}}
#list{overflow:auto;border-right:1px solid var(--line);background:var(--panel)}
.grp{padding:8px 12px 4px;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--mute)}
.call{display:flex;align-items:center;gap:8px;padding:6px 12px;border-top:1px solid transparent;cursor:pointer;user-select:none}
.call:hover{background:var(--sel)}.call.sel{background:var(--sel);box-shadow:inset 3px 0 var(--acc)}
.call.off .t{color:var(--off);text-decoration:line-through}.call.drop{border-top:1px solid var(--acc)}
.h{cursor:grab;color:var(--mute)}.n{width:22px;text-align:right;color:var(--mute);font-variant-numeric:tabular-nums}
.id{font-weight:600;min-width:64px}.t{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;flex:1;color:var(--mute)}
#detail{display:grid;grid-template-columns:1fr 1fr;min-height:0}
@media (max-width:1100px){#detail{grid-template-columns:1fr}}
.pane{display:flex;flex-direction:column;min-height:0;border-right:1px solid var(--line)}
.pane h2{margin:0;padding:10px 14px;font-size:13px;border-bottom:1px solid var(--line);display:flex;gap:8px;align-items:center}
.pane h2 .sp{flex:1}
textarea{flex:1;min-height:320px;width:100%;border:0;padding:12px 14px;background:var(--bg);color:var(--ink);font:12.5px/1.5 ui-monospace,Consolas,monospace;resize:none;outline:none}
.meta{padding:8px 14px;border-top:1px solid var(--line);color:var(--mute);font-size:12px;display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.dirty{color:#b5651d}
</style></head><body><script src="/nav.js"></script>
<header><h1>CKG · Backside</h1><span class="v" id="variant"></span><span class="sp"></span>
<label>Model <select id="model"><option>deepseek-chat</option><option>deepseek-reasoner</option><option>claude-sonnet-5-5</option></select></label>
<span id="count" class="v"></span>
<button id="save" class="pri">Download ckg.json</button></header>
<main><nav id="list"></nav>
<section id="detail">
 <div class="pane"><h2>PROMPT <span class="sp"></span><span id="pid" class="v"></span></h2><textarea id="prompt" spellcheck="false"></textarea></div>
 <div class="pane"><h2>OUTPUT TEMPLATE: what the answer should look like<span class="sp"></span>
   <select id="fmt"><option value="markdown">Markdown</option><option value="json">JSON</option></select></h2>
   <textarea id="tpl" spellcheck="false"></textarea>
   <div class="meta"><span id="size"></span><span id="state"></span></div></div>
</section></main>
<script>
let M = __DATA__, calls, idle, sel, dragging = null, dirty = new Set(), live = false;
const $ = id => document.getElementById(id);
function init(data){
  M = data;
  calls = M.calls.filter(c => c.run_order).sort((a,b)=>a.run_order-b.run_order);
  idle = M.calls.filter(c => !c.run_order);
  const keep = sel && M.calls.find(c => c.folder === sel.folder);
  sel = keep || calls[0];
  $('variant').textContent = M.label;
  $('model').value = M.model;
  pick(sel);
}
const groupName = c => c.id==='MAP'?'First':/^S\d/.test(c.id)?'Sections S01–S10':/^A\d/.test(c.id)?'Atom records A1–A16':'Summaries (read everything)';
function row(c, i, movable){
  const d = document.createElement('div');
  d.className = 'call'+(c.on?'':' off')+(c===sel?' sel':'');
  d.innerHTML = (movable?'<span class="h">≡</span>':'<span class="h"> </span>')+
    `<span class="n">${movable?i+1:''}</span>`+
    (movable?`<input type="checkbox" ${c.on?'checked':''}>`:'<input type="checkbox" disabled>')+
    `<span class="id">${c.id}</span><span class="t">${c.title.replace(/^S\d\d · |^A\d+ · /,'')}</span>`;
  d.onclick = e => { if(e.target.tagName==='INPUT') return; pick(c); };
  const cb = d.querySelector('input');
  if(movable) cb.onchange = () => { c.on = cb.checked; dirty.add('order'); render(); };
  if(movable){
    d.draggable = true;
    d.ondragstart = () => dragging = c;
    d.ondragover = e => { e.preventDefault(); d.classList.add('drop'); };
    d.ondragleave = () => d.classList.remove('drop');
    d.ondrop = e => { e.preventDefault(); if(!dragging||dragging===c) return;
      calls.splice(calls.indexOf(dragging),1); calls.splice(calls.indexOf(c),0,dragging);
      calls.forEach((x,k)=>x.run_order=k+1); dirty.add('order'); render(); };
  }
  return d;
}
function render(){
  const L = $('list'); L.innerHTML=''; let g='';
  calls.forEach((c,i)=>{ const gn=groupName(c); if(gn!==g){g=gn; L.insertAdjacentHTML('beforeend',`<div class="grp">${gn}</div>`);} L.appendChild(row(c,i,true)); });
  L.insertAdjacentHTML('beforeend','<div class="grp">Not called (layout / pasted source / legacy)</div>');
  idle.forEach(c=>L.appendChild(row(c,0,false)));
  const on = calls.filter(c=>c.on).length;
  $('count').textContent = `${on} of ${calls.length} calls on`;
  $('state').innerHTML = dirty.size?`<span class="dirty">unsaved changes${live?'':': download ckg.json to keep order/settings'}</span>`:'';
  $('save').textContent = live ? (dirty.size ? 'Save' : 'Saved') : 'Download ckg.json';
}
function pick(c){
  sel = c;
  $('pid').textContent = c.folder;
  $('prompt').value = c.prompt || '(no prompt: this part is not sent to a model)';
  $('prompt').readOnly = !c.prompt;
  $('tpl').value = c.template || '(no template: MAP returns the JSON schema shown in its prompt)';
  $('tpl').readOnly = !c.template;
  $('fmt').value = c.output_format || 'markdown';
  $('size').textContent = c.template ? `${c.template.length.toLocaleString()} chars ≈ ${Math.round(c.template.length/4).toLocaleString()} tokens` : '';
  render();
}
$('prompt').oninput = e => { sel.prompt = e.target.value; dirty.add(sel.id); render(); };
$('tpl').oninput = e => { sel.template = e.target.value; dirty.add(sel.id); render(); };
$('fmt').onchange = e => { sel.output_format = e.target.value; dirty.add(sel.id); render(); };
$('model').onchange = e => { M.model = e.target.value; dirty.add('model'); render(); };
$('save').onclick = async () => {
  if(live){
    const r = await fetch('/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(M)});
    const j = await r.json();
    if(!r.ok){ alert('Save failed: '+j.error); return; }
    dirty.clear();
    $('state').textContent = j.written.length ? `saved ${j.written.length} file(s); old versions in ${j.backup}` : 'nothing changed';
    $('save').textContent = 'Saved';
    return;
  }
  const out = {...M, calls: M.calls.map(({prompt,template,...c})=>c)};
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(out,null,2)+'\n'],{type:'application/json'}));
  a.download = 'ckg.json'; a.click();
};
init(M);
fetch('/data').then(r => r.ok ? r.json() : null).then(d => { if(d){ live = true; init(d); } }).catch(()=>{});
window.onbeforeunload = e => { if(dirty.size){ e.preventDefault(); e.returnValue=''; } };
</script></body></html>
"""
(root / "backside.html").write_text(html.replace("__DATA__", data), encoding="utf-8")
print("wrote", root / "backside.html")
