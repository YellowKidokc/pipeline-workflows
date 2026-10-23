/* ════════════════════════════════════════════════════════════════════════════════
   CONSILIENCE ATLAS — UNIVERSAL ATOM SHELL v1.2
   Data-driven renderer: type-aware lens, computed fields, evidence graph.
   ════════════════════════════════════════════════════════════════════════════════ */

(function() {
  'use strict';

  // ─── DEFAULT GRAMMAR (overridden by grammar.json if fetch succeeds) ───
  const DEFAULT_GRAMMAR = {
    claim:      { m05:'Rests on', m06:'Weakest link', m07:'Kills it', m08:'Support' },
    evidence:   { m05:'Grounds', m06:'Data cited', m07:'Replicates?', m08:'Kills empirically' },
    proof:      { m05:'Proves', m06:'Method', m07:'Assumptions', m08:'Receipt' },
    lean:       { m05:'Formalizes', m06:'File / line', m07:'Axioms used', m08:'Build receipt' },
    bridge:     { m05:'Domain A', m06:'Domain B', m07:'Isomorphism', m08:'Metaphor test' },
    definition: { m05:'Term', m06:'Distinguishes from', m07:'Used by', m08:'Invariants' },
    unknown:    { m05:'TODO', m06:'TODO', m07:'TODO', m08:'TODO' }
  };

  // ─── DEFAULT SAMPLE DATA (used if nothing else is provided) ───
  const FALLBACK_DATA = {
    protocol_version: 'ATLAS-ATOM-1.2',
    atom: {
      type: 'claim',
      status: 'leanProven',
      id: 'AX-ME-01',
      role: 'Canonical Claim',
      title: 'The Master Equation',
      claim: 'χ(W) = C_W[∏ᵢ₌₁⁹ Xᵢ] — nine factors, multiplied; any factor at zero collapses the whole.',
      commitment: 'Canon'
    },
    identity: {
      uuid: '6f0849c8-a1b2-4c3d-8e9f-0123456789ab',
      semantic_code: 'ATOM.ME.L5.C1',
      human_label: 'Closed-System Trilemma',
      publication_state: 'canon',
      version: '1.2',
      source_hash: 'sha256:a1b2...',
      last_computed: '2026-10-15T20:31:00Z'
    },
    nabla: {
      address: 'TECH/MASTER_EQUATION/F/AI_RESEARCH/T/R1',
      vector: { G:3, M:3, E:0, S:0, T:3, K:3, R:3, Q:0, F:3, C:3 },
      hash: '[C·Q][G·S][K·E][M·F][T·R]',
      confidence: 0.91
    },
    epistemic: {
      class: 'theorem',
      class_label: 'Derived theorem',
      scope_class: { level:'G2', label:'cross-domain invariant', basis:'same abstract grammar survives 6 independent domains' },
      derivation_status: 'derived-from-foundations',
      external_independence: 'high'
    },
    markers: {
      home: 'MAT',
      native: ['MAT','PHY','INF'],
      bridged: ['THE']
    },
    lens: {
      m05: '2 · ∃ Existence, D Distinction',
      m06: 'closure assumption',
      m07: 'open-system counterexample',
      m08: 'Full · 3 anchored'
    },
    source: {
      document_id: 'master-equation-v5',
      spans: [{span_id:'SPAN-001', text:'The closed-system trilemma...', lines:'142-158'}]
    },
    dependency_spine: {
      upstream: [
        { id:'atom-existence', symbol:'∃', name:'Existence', grade:'B', type:'claim', hiero:'ℂ' },
        { id:'atom-distinction', symbol:'D', name:'Distinction', grade:'B', type:'claim', hiero:'ℂ' }
      ],
      center: { id:'atom-me', symbol:'∫χ', name:'Master Equation', grade:'B', type:'equation', hiero:'Σ' },
      downstream: [
        { id:'atom-negentropy', symbol:'G', name:'Negentropy', grade:'B', type:'variable', hiero:'χ' },
        { id:'atom-alignment', symbol:'M', name:'Alignment', grade:'B', type:'variable', hiero:'χ' }
      ]
    },
    evidence_graph: {
      nodes: [
        { id:'AX-ME-01', role:'claim', title:'The Master Equation' },
        { id:'listProd_eq_zero_iff', role:'lean', title:'Product collapse theorem', edge:'formalizes' },
        { id:'cannot_rescue_zero', role:'lean', title:'No rescue for a zero factor', edge:'sharpens' },
        { id:'SRC-ME-AUG1', role:'evidence', title:'Source span · master doc (Aug 1)', edge:'sources' },
        { id:'KILL-ZF-NZP', role:'audit', title:'Kill: zero factor, nonzero product', edge:'challenges' },
        { id:'chi_zero_if_any_factor_zero', role:'proof', title:'χ = 0 if any Xᵢ = 0', edge:'instantiates' },
        { id:'CI-2026-10-08', role:'receipt', title:'lake build · CI green', edge:'verifies' }
      ]
    },
    warrant: {
      claim: 'No closed system can sustain coherence without external negentropic input.',
      evidence: ['EVD-001','EVD-002'],
      proof: 'PRF-014',
      counterevidence: [],
      kill_conditions: ['Demonstration of perpetual motion machine sustaining coherence'],
      native_grade: 'B+',
      normalized_grade: 'B+',
      coverage: 0.84,
      strength: 0.88
    },
    dynamics: {
      coherence: 'System maintains local order against global entropy gradient',
      degradation: 'Entropy increase without external work input',
      measurement: 'Negentropy flux across system boundary',
      threshold: 'χ_c = ħ / (m_e c) — proposed, needs empirical anchor',
      asymmetric: 'Yes — decay is spontaneous, restoration requires work',
      restoration: { self:'Limited — local reversal possible, global reversal impossible', external:'Required — W_G operator' },
      counterexample: 'None known'
    },
    ascent_translation_descent: {
      meeting_state: 'CONVERGED',
      ascent: ['Thermodynamic second law','Information theory channel capacity','Gödel incompleteness'],
      translation: {
        preserved: ['Boundary requirement','Work differential','Non-closure'],
        lost: ['Specific heat engine mechanism'],
        introduced: ['χ-field operator formalism'],
        forbidden: ['Perpetual motion','Closed-system perpetual coherence']
      },
      descent: ['Law V: Self-Limitation','Law VIII: Negentropic Work','C0 grade label']
    },
    bridges: [
      {
        id:'BRIDGE-001', source_domain:'PHY', target_domain:'THE', direction:'PHY → THE', state:'Admitted',
        preserved:['Boundary','Work','Conservation'], lost:['Mechanistic detail'],
        introduced:['Grace operator semantics'], forbidden:['Magic / violation of conservation']
      }
    ],
    reality_mirror: {
      class:'N', status:'anchored', anchor_object:'Thermodynamic second law',
      independence:'High — derived independently across 3 domains', closed_loop_warning:false
    },
    receipts: {
      human: { status:'COMPLETE', result:'Admitted', timestamp:'2026-08-05' },
      python: { status:'COMPLETE', result:'Verified', timestamp:'2026-08-05' },
      api: { status:'COMPLETE', result:'Admitted', timestamp:'2026-08-05' },
      method_convergence:'3/3 EXACT'
    },
    alerts: [
      { level:'warn', text:'C0 grade label pending formal adjudication' },
      { level:'info', text:'Bridge to THE domain under periodic review' }
    ],
    computed: {
      blast_radius: 8,
      articulation_point: true,
      dependency_depth: 3,
      reachability_up: 5,
      reachability_down: 12
    }
  };

  // ─── CONFIG: 15-slot skeleton ───
  const P15_SLOTS = [
    { slot:'m01', label:'Identity', path:'identity.semantic_code' },
    { slot:'m02', label:'Home', path:'markers.home' },
    { slot:'m03', label:'Native', path:'markers.native', join:true, empty:'—' },
    { slot:'m04', label:'Bridged', path:'markers.bridged', join:true, empty:'None' },
    { slot:'m05', lens:true, path:'lens.m05' },
    { slot:'m06', lens:true, path:'lens.m06' },
    { slot:'m07', lens:true, path:'lens.m07' },
    { slot:'m08', lens:true, path:'lens.m08' },
    { slot:'m09', label:'Commitment', path:'atom.commitment' },
    { slot:'m10', label:'Standing', computed:'standing' },
    { slot:'m11', label:'Dispute', computed:'dispute' },
    { slot:'m12', label:'Grade', computed:'grade' },
    { slot:'m13', label:'Runs', path:'computed.runs', empty:'0' },
    { slot:'m14', label:'Degree', computed:'degree' },
    { slot:'m15', label:'Alert', computed:'alertText' }
  ];

  let GRAMMAR = DEFAULT_GRAMMAR;
  let DATA = null;

  // ─── HELPERS ───
  function get(obj, path) {
    if (!path) return undefined;
    const parts = path.split('.');
    let v = obj;
    for (const p of parts) {
      v = v?.[p];
      if (v === undefined || v === null) return undefined;
    }
    return v;
  }

  function esc(s) {
    return String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function fmtArray(v, empty) {
    if (!Array.isArray(v)) return v;
    if (v.length === 0) return empty ?? '—';
    return v.join(' · ');
  }

  function computeStanding(status) {
    const map = {
      leanProven: 'Floor',
      structurallyMapped: 'Mapped',
      leanDefined: 'Defined',
      empiricallyTestable: 'Testable',
      theologicallyIdentified: 'Identified',
      open: 'Open',
      teachingLayer: 'Prose'
    };
    return map[status] || 'TODO';
  }

  function computeGrade(status) {
    const map = {
      leanProven: 'A',
      structurallyMapped: 'B',
      leanDefined: 'B',
      empiricallyTestable: 'B',
      theologicallyIdentified: 'C',
      open: 'C',
      teachingLayer: 'D'
    };
    return map[status] || 'C0';
  }

  function computeAlerts(D) {
    if (Array.isArray(D.alerts) && D.alerts.length) {
      return D.alerts.map(a => a.text);
    }
    const status = D.atom?.status;
    if (status === 'open') return ['Open item: no receipt yet'];
    if (status === 'teachingLayer') return ['Teaching layer: no formal claim'];
    return [];
  }

  function computeDispute(D) {
    if (D.computed?.dispute) return D.computed.dispute;
    const status = D.atom?.status;
    if (status === 'open') return 'Open — kill condition needed';
    return 'None';
  }

  function enrichData(D) {
    const status = D.atom?.status || 'unknown';
    D._computed = {
      standing: computeStanding(status),
      grade: D.computed?.grade || computeGrade(status),
      dispute: computeDispute(D),
      runs: D.computed?.runs ?? '—',
      degree: D.computed?.degree ?? `${D.computed?.reachability_up ?? '?'}/${D.computed?.reachability_down ?? '?'}`,
      alerts: computeAlerts(D)
    };
    D._computed.alertText = D._computed.alerts.length ? D._computed.alerts.join('; ') : 'None';
    return D;
  }

  // ─── LOADERS ───
  async function loadGrammar() {
    try {
      const res = await fetch('grammar.json');
      if (res.ok) {
        const json = await res.json();
        GRAMMAR = { ...DEFAULT_GRAMMAR, ...json };
      }
    } catch (e) {
      console.warn('Could not load grammar.json, using default grammar', e);
    }
  }

  async function loadAtomData() {
    // 1. Inline JSON block (generated per-atom pages)
    const block = document.getElementById('atom-data');
    if (block) {
      try {
        return JSON.parse(block.textContent);
      } catch (e) {
        console.error('Inline atom-data JSON is invalid', e);
      }
    }

    // 2. URL query ?atom=path/to/file.json (universal viewer)
    const params = new URLSearchParams(location.search);
    const src = params.get('atom');
    if (src) {
      try {
        const res = await fetch(src);
        if (res.ok) return await res.json();
        console.error(`Failed to load ${src}: ${res.status}`);
      } catch (e) {
        console.error(`Could not fetch ${src}`, e);
      }
    }

    // 3. window.ATLAS_DATA fallback (legacy support)
    if (window.ATLAS_DATA) return window.ATLAS_DATA;

    // 4. Built-in sample
    console.warn('No atom data found; rendering fallback sample.');
    return JSON.parse(JSON.stringify(FALLBACK_DATA));
  }

  // ─── RENDERERS ───
  function renderFields(D) {
    document.querySelectorAll('[data-field]').forEach(el => {
      const path = el.dataset.field;
      let val = get(D, path);
      if (val === undefined || val === null) return;
      if (Array.isArray(val)) val = val.join(', ');
      else if (typeof val === 'object') val = JSON.stringify(val);
      el.textContent = val;
    });

    // Resolution label
    const resEl = document.querySelector('[data-field="resolution"]');
    if (resEl) resEl.textContent = 'Resolution: LOCAL';
  }

  function renderNabla(D) {
    const vector = D.nabla?.vector || {};
    document.querySelectorAll('.nabla-v').forEach(el => {
      const key = el.dataset.nabla;
      const val = vector[key];
      el.classList.toggle('active', val > 0);
      el.textContent = val !== undefined ? `${key}${val}` : `${key}0`;
    });
  }

  function renderP15(D) {
    const grid = document.getElementById('p15-grid');
    if (!grid) return;
    const type = D.atom?.type || 'unknown';
    const lensGrammar = GRAMMAR[type] || GRAMMAR.unknown;

    grid.innerHTML = P15_SLOTS.map((cfg, i) => {
      const index = i + 1;
      const isLens = cfg.lens;
      const label = isLens ? (lensGrammar[cfg.slot] || 'TODO') : cfg.label;

      let value;
      if (cfg.computed) {
        value = D._computed[cfg.computed];
      } else {
        value = get(D, cfg.path);
        if (Array.isArray(value)) value = fmtArray(value, cfg.empty);
        if (value === undefined || value === null || value === '') value = cfg.empty ?? 'TODO';
      }

      const isComputed = ['m10','m11','m12','m13','m14','m15'].includes(cfg.slot);
      const isAlert = cfg.slot === 'm15' && D._computed.alerts.length > 0;
      const isTodo = String(value).toUpperCase() === 'TODO';
      const small = String(value).length > 12;

      return `<div class="p15-cell ${isComputed?'computed':''} ${isAlert?'alert':''} ${isLens?'lens':''} ${isTodo?'todo':''}" data-marker="${cfg.slot}">
        <span class="p15-num">${String(index).padStart(2,'0')}</span>
        <span class="p15-key">${esc(label)}</span>
        <span class="p15-val ${small?'small':''}">${esc(value)}</span>
      </div>`;
    }).join('');
  }

  function renderAtomNote(D) {
    const container = document.getElementById('atom-note-container');
    if (!container) return;
    const a = D.atom || {};
    const status = a.status || 'unknown';
    const standing = D._computed.standing;
    const grade = D._computed.grade;
    const typeLabel = (a.type || 'unknown').toUpperCase();

    container.innerHTML = `
      <div class="atom-note">
        <div class="note-head">
          <div>
            <div class="note-eyebrow">${esc(a.id)} · ${esc(a.role)} · ${esc(typeLabel)}</div>
            <div class="note-title">${esc(a.title)}</div>
            <div class="note-claim">${esc(a.claim)}</div>
          </div>
          <div class="note-badge st-${standing.replace(/\s+/g,'-').toUpperCase()}">${esc(standing)}</div>
        </div>
        <div class="note-markers">
          <div class="note-marker"><div class="mk">Identity</div><div class="mv">${esc(D.identity?.semantic_code)}</div></div>
          <div class="note-marker"><div class="mk">Home</div><div class="mv">${esc(D.markers?.home)}</div></div>
          <div class="note-marker"><div class="mk">Type</div><div class="mv">${esc(a.type)}</div></div>
          <div class="note-marker"><div class="mk">Commitment</div><div class="mv">${esc(a.commitment)}</div></div>
          <div class="note-marker"><div class="mk">Standing</div><div class="mv">${esc(standing)}</div></div>
          <div class="note-marker"><div class="mk">Grade</div><div class="mv">${esc(grade)}</div></div>
        </div>
      </div>
    `;
  }

  function tile(atom, isCenter) {
    if (!atom) return '';
    return `<div class="atom-tile ${isCenter?'center-node':''}" data-atom-id="${esc(atom.id)}" onclick="openAtom('${esc(atom.id)}')">
      <span class="tile-hiero">${esc(atom.hiero||'·')}</span>
      <span class="tile-sym">${esc(atom.symbol||'')}</span>
      <span class="tile-name">${esc(atom.name||'')}</span>
      <span class="tile-grade grade-${(atom.grade||'c').toLowerCase()}">${esc(atom.grade||'')}</span>
    </div>`;
  }

  function renderDependencySpine(D) {
    const spine = D.dependency_spine || {};
    const up = document.getElementById('upstream-container');
    const center = document.getElementById('center-container');
    const down = document.getElementById('downstream-container');
    if (up) up.innerHTML = (spine.upstream||[]).map(a => tile(a,false)).join('');
    if (center) center.innerHTML = tile(spine.center,true);
    if (down) down.innerHTML = (spine.downstream||[]).map(a => tile(a,false)).join('');
  }

  function renderEvidenceGraph(D) {
    const stage = document.getElementById('evidence-graph-stage');
    const svg = document.getElementById('evidence-graph-edges');
    if (!stage) return;
    stage.querySelectorAll('.gnode').forEach(n => n.remove());
    if (svg) svg.innerHTML = '';

    const graph = D.evidence_graph || {};
    const nodes = graph.nodes || [];
    const centerNode = nodes[0];
    const neighbors = nodes.slice(1);
    if (!centerNode) return;

    const center = document.createElement('div');
    center.className = 'gnode center k-' + (centerNode.role || 'claim');
    center.style.left = '50%';
    center.style.top = '50%';
    center.innerHTML = `<div class="nid">${esc(centerNode.id)}</div><div class="nt">${esc(centerNode.title)}</div><div class="nrole">${esc(centerNode.role || '')}</div>`;
    stage.appendChild(center);

    const n = neighbors.length;
    neighbors.forEach((g, i) => {
      const ang = -Math.PI/2 + (n ? i * (2*Math.PI/n) : 0);
      const x = 50 + 36*Math.cos(ang);
      const y = 50 + 36*Math.sin(ang);
      const el = document.createElement('div');
      el.className = 'gnode k-' + (g.role || 'claim');
      el.style.left = x + '%';
      el.style.top = y + '%';
      el.innerHTML = `<div class="nid">${esc(g.id)}</div><div class="nt">${esc(g.title)}</div><div class="nrole">${esc(g.role || '')}</div>`;
      stage.appendChild(el);
    });

    requestAnimationFrame(() => drawEvidenceEdges(stage, svg, neighbors));
  }

  function drawEvidenceEdges(stage, svg, neighbors) {
    if (!stage || !svg) return;
    if (window.innerWidth < 980) return;
    const sr = stage.getBoundingClientRect();
    const center = stage.querySelector('.gnode.center');
    if (!center) return;
    const cr = center.getBoundingClientRect();
    const cx = cr.left + cr.width/2 - sr.left;
    const cy = cr.top + cr.height/2 - sr.top;
    let out = '';
    stage.querySelectorAll('.gnode:not(.center)').forEach((el, i) => {
      const r = el.getBoundingClientRect();
      const x = r.left + r.width/2 - sr.left;
      const y = r.top + r.height/2 - sr.top;
      const mx = (cx + x)/2;
      const label = neighbors[i]?.edge || '';
      out += `<path class="edge" d="M${x},${y} C${mx},${y} ${mx},${cy} ${cx},${cy}"/>`;
      if (label) {
        const lx = (x + cx)/2;
        const ly = (y + cy)/2 - 6;
        out += `<text class="edge-label" x="${lx}" y="${ly}" text-anchor="middle">${esc(label)}</text>`;
      }
    });
    svg.innerHTML = out;
  }

  function renderKills(D) {
    const container = document.getElementById('kill-container');
    if (!container) return;
    const kills = D.warrant?.kill_conditions || [];
    container.innerHTML = kills.map(k => `
      <div class="alert-item" style="background:rgba(201,64,64,0.08);color:#dc8b8b;"><strong>Kill:</strong> ${esc(k)}</div>
    `).join('') || '<span class="dim">None defined</span>';
  }

  function renderWarrantSummary(D) {
    const native = document.querySelector('[data-field="warrant.native_grade"]');
    const norm = document.querySelector('[data-field="warrant.normalized_grade"]');
    const cov = document.querySelector('[data-field="warrant.coverage"]');
    const str = document.querySelector('[data-field="warrant.strength"]');
    if (native) native.textContent = D.warrant?.native_grade ?? D._computed.grade;
    if (norm) norm.textContent = D.warrant?.normalized_grade ?? D._computed.grade;
    if (cov) cov.textContent = (D.warrant?.coverage ?? 0) + '%';
    if (str) str.textContent = (D.warrant?.strength ?? 0) + '%';
  }

  function renderDynamics(D) {
    const tbody = document.getElementById('dynamics-container');
    if (!tbody) return;
    const dyn = D.dynamics || {};
    const questions = [
      {q:'What counts as coherence?', k:'coherence'},
      {q:'What counts as degradation?', k:'degradation'},
      {q:'How is it measured?', k:'measurement'},
      {q:'Is there a threshold?', k:'threshold'},
      {q:'Is the transition asymmetric?', k:'asymmetric'},
      {q:'What restores it?', k:'restoration', isSplit:true},
      {q:'Is there a counterexample?', k:'counterexample'}
    ];
    tbody.innerHTML = questions.map((item,i) => {
      let ans = dyn[item.k];
      let status = 'OBSERVED';
      if (item.isSplit && typeof ans === 'object') {
        ans = `Self: ${ans.self||'—'} | External: ${ans.external||'—'}`;
        status = 'DEFINED';
      }
      if (!ans) { ans = '—'; status = 'UNRESOLVED'; }
      return `<tr><td>${i+1}</td><td class="dyn-q">${esc(item.q)}</td><td class="dyn-a">${esc(ans)}</td><td><span class="dyn-status status-${status.toLowerCase()}">${esc(status)}</span></td></tr>`;
    }).join('');
  }

  function renderATD(D) {
    const atd = D.ascent_translation_descent || {};
    const asc = document.getElementById('ascent-container');
    const trans = document.getElementById('translation-container');
    const desc = document.getElementById('descent-container');
    if (asc) asc.innerHTML = (atd.ascent||[]).map(a => `<div class="atd-item">${esc(a)}</div>`).join('');
    if (desc) desc.innerHTML = (atd.descent||[]).map(d => `<div class="atd-item">${esc(d)}</div>`).join('');
    if (trans) {
      const t = atd.translation || {};
      let html = '';
      (t.preserved||[]).forEach(x => html += `<div class="atd-item preserved">✓ ${esc(x)}</div>`);
      (t.lost||[]).forEach(x => html += `<div class="atd-item lost">✗ ${esc(x)}</div>`);
      (t.introduced||[]).forEach(x => html += `<div class="atd-item introduced">+ ${esc(x)}</div>`);
      (t.forbidden||[]).forEach(x => html += `<div class="atd-item forbidden">⊘ ${esc(x)}</div>`);
      trans.innerHTML = html || '<span class="dim">No translation data</span>';
    }
  }

  function renderBridges(D) {
    const container = document.getElementById('bridges-container');
    if (!container) return;
    const bridges = D.bridges || [];
    container.innerHTML = bridges.map(b => `
      <div class="bridge-card" data-bridge-id="${esc(b.id)}">
        <div class="bridge-header">
          <span class="bridge-route">${esc(b.source_domain)} → ${esc(b.target_domain)}</span>
          <span class="bridge-state ${esc((b.state||'').toLowerCase())}">${esc(b.state)}</span>
        </div>
        <div style="font-size:10px;color:var(--textfaint);margin-bottom:6px;">${esc(b.direction)}</div>
        <div style="display:flex;flex-wrap:wrap;gap:4px;">
          ${(b.preserved||[]).map(x => `<span class="pill" style="background:rgba(127,199,127,0.1);color:var(--green);border-color:rgba(127,199,127,0.3);">${esc(x)}</span>`).join('')}
          ${(b.lost||[]).map(x => `<span class="pill" style="background:rgba(201,64,64,0.1);color:var(--red);border-color:rgba(201,64,64,0.3);text-decoration:line-through;">${esc(x)}</span>`).join('')}
          ${(b.introduced||[]).map(x => `<span class="pill" style="background:rgba(215,169,75,0.1);color:var(--amber);border-color:rgba(215,169,75,0.3);">+ ${esc(x)}</span>`).join('')}
        </div>
      </div>
    `).join('') || '<span class="dim">No bridges defined</span>';
  }

  function renderAlerts(D) {
    const container = document.getElementById('alerts-container');
    if (!container) return;
    const alerts = D.alerts || [];
    container.innerHTML = alerts.map(a => `
      <div class="alert-item ${esc(a.level||'warn')}">${esc(a.text)}</div>
    `).join('') || '<span class="dim">No alerts</span>';
  }

  function renderGraphSignature(D) {
    const computed = D.computed || {};
    const set = (path, val) => {
      const el = document.querySelector(`[data-field="computed.${path}"]`);
      if (el) el.textContent = val;
    };
    set('blast_radius', computed.blast_radius ?? '—');
    set('articulation_point', computed.articulation_point ? 'Yes' : 'No');
    set('dependency_depth', computed.dependency_depth ?? '—');
    set('reachability_up', computed.reachability_up ?? '—');
    set('reachability_down', computed.reachability_down ?? '—');
  }

  function renderReceipts(D) {
    const receipts = D.receipts || {};
    const set = (path, val) => {
      const el = document.querySelector(`[data-field="receipts.${path}"]`);
      if (el) el.textContent = val;
    };
    set('human.result', receipts.human?.result ?? '—');
    set('python.result', receipts.python?.result ?? '—');
    set('api.result', receipts.api?.result ?? '—');
    set('method_convergence', receipts.method_convergence ?? '—');
  }

  // ─── TABS / CONTROLS ───
  window.switchTab = function(id) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.toggle('active', b.dataset.tab === id));
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.toggle('active', p.dataset.tabPane === id));
    if (id === 'evidence-graph') {
      requestAnimationFrame(() => renderEvidenceGraph(DATA));
    }
  };

  window.setResolution = function(res) {
    document.querySelectorAll('.res-btn').forEach(b => b.classList.toggle('active', b.dataset.res === res));
    console.log('Resolution:', res);
  };

  window.setGraphState = function(state) {
    document.querySelectorAll('[data-toggle="graph-state"] .toggle-btn').forEach(b => b.classList.toggle('active', b.dataset.state === state));
  };

  window.setSnapshot = function(state) {
    document.querySelectorAll('[data-toggle="snapshot-state"] .toggle-btn').forEach(b => b.classList.toggle('active', b.dataset.state === state));
  };

  window.openAtom = function(id) {
    console.log('Open atom:', id);
  };

  function setupSampleLoader() {
    const select = document.getElementById('sample-loader');
    if (!select) return;
    select.addEventListener('change', () => {
      const src = select.value;
      if (!src) return;
      const url = new URL(location.href);
      url.searchParams.set('atom', src);
      location.href = url.toString();
    });
    // Set current selection from URL
    const params = new URLSearchParams(location.search);
    const current = params.get('atom');
    if (current) select.value = current;
  }

  // ─── MAIN ───
  async function main() {
    await loadGrammar();
    DATA = await loadAtomData();
    enrichData(DATA);

    renderFields(DATA);
    renderNabla(DATA);
    renderP15(DATA);
    renderAtomNote(DATA);
    renderDependencySpine(DATA);
    renderEvidenceGraph(DATA);
    renderKills(DATA);
    renderWarrantSummary(DATA);
    renderDynamics(DATA);
    renderATD(DATA);
    renderBridges(DATA);
    renderAlerts(DATA);
    renderGraphSignature(DATA);
    renderReceipts(DATA);

    setupSampleLoader();

    window.addEventListener('resize', () => {
      const pane = document.querySelector('.tab-pane.active');
      if (pane && pane.dataset.tabPane === 'evidence-graph') {
        renderEvidenceGraph(DATA);
      }
    });

    console.log('Atom shell v1.2 rendered. Type:', DATA.atom?.type, 'Status:', DATA.atom?.status);
  }

  main().catch(err => console.error('Atom shell failed to render', err));
})();
