// Shared top bar: every page includes <script src="/nav.js"></script> as the first thing in <body>.
// Sections follow the paper lifecycle (workflow.stages in the paper YAML / PAPER_LIFECYCLE_CHECKLIST v0.1).
(function () {
  const links = [
    ['/', 'Home'], ['/intake', '1 Intake'], ['/run', '2 Decompose'], ['/verify', '3 Verify'],
    ['/research', '4 Research'], ['/ruling', '5 Ruling'], ['/rebuild', '6 Rebuild'],
    ['/publish', '7 Publish'], ['/feedback', '8 Feedback'], ['/settings', 'Settings'],
  ];
  const alias = { '/backside.html': '/run', '/backside': '/run' };
  let here = location.pathname.replace(/\.html$/, '').replace(/^\/home$/, '/');
  here = alias[location.pathname] || here;
  const css = `#topnav{display:flex;gap:2px;align-items:center;padding:0 12px;height:40px;background:var(--panel,#fff);
    border-bottom:1px solid var(--line,#ddd);font:14px system-ui,Segoe UI,sans-serif;overflow-x:auto}
    #topnav b{margin-right:12px;white-space:nowrap}#topnav a{padding:6px 10px;border-radius:6px;color:inherit;text-decoration:none;white-space:nowrap}
    #topnav a:hover{background:var(--sel,#eef)}#topnav a.on{background:var(--acc,#2f5d8a);color:#fff}
    #subnav{display:flex;gap:4px;padding:6px 12px;border-bottom:1px solid var(--line,#ddd);font:13px system-ui,sans-serif}
    #subnav a{padding:3px 10px;border-radius:5px;color:inherit;text-decoration:none}#subnav a.on{background:var(--sel,#eef);font-weight:600}`;
  document.head.insertAdjacentHTML('beforeend', `<style>${css}</style>`);
  let html = '<nav id="topnav"><b>David-OS</b>' + links.map(([h, t]) =>
    `<a href="${h}" class="${here === h ? 'on' : ''}">${t}</a>`).join('') + '</nav>';
  if (here === '/run') {
    const p = location.pathname;
    html += `<nav id="subnav"><a href="/run" class="${p === '/run' || p === '/run.html' ? 'on' : ''}">Run</a>` +
      `<a href="/backside.html" class="${p.startsWith('/backside') ? 'on' : ''}">API Calls (backside)</a></nav>`;
  }
  document.body.insertAdjacentHTML('afterbegin', html);
})();
