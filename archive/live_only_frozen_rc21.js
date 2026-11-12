/* =========================================================
   PROTOTYPE — "Live Tuesday"
   Plan by drag & drop (no interruptions while planning), then ▶ Start Tuesday:
   a now-line runs down the calendar and the interruptions arrive as it passes.
   ========================================================= */
var LIVE = { on: false, running: false, clock: null, secPerHour: 10, timer: null, fired: {}, batchesSeen: {}, deepSeen: {}, waiting: false, done: false };

// while planning, placing a task fires nothing — and Karim doesn't fall asleep at the planning table
tueOnPlace = function () {};
const _checkEnergy0 = checkEnergy;
checkEnergy = function () { if (!isAdapt()) return _checkEnergy0(); };
function liveEnergyAt(t) { const { pts } = energySeries(); let e = pts[0].e; pts.forEach(p => { if (p.t <= t) e = p.e; }); return e; }
// interruption time goes in at the moment it happens
tueAdd = function (onId, mins, label) {
  const ds = DS(), b = ds.blocks[onId]; if (!b || mins <= 0) return;
  const at = LIVE.clock != null ? Math.min(Math.max(LIVE.clock, b.start + 1), b.start + blockLen(onId) - 1) : b.start + 5;
  insertAt(at, mins, label);
};

function liveSchedule() { // when each interruption arrives: a third into its trigger task, or its own time
  const ds = DS(), out = [];
  intList(D()).filter(i => i.trigger === D()).forEach(it => {
    let at = it.time;
    if (it.on && it.on[0] !== '@' && ds.blocks[it.on]) at = ds.blocks[it.on].start + Math.max(5, Math.round(blockLen(it.on) / 3));
    if (it.on === '@deep') { // the first deep-focus block after its usual time (never the statistics log)
      const deep = Object.keys(ds.blocks).filter(id => ds.tag[id] === 'deep' && !/_stats$/.test(id) && ds.blocks[id].start + blockLen(id) > it.time).sort((a, b) => ds.blocks[a].start - ds.blocks[b].start)[0];
      at = deep ? Math.max(ds.blocks[deep].start + 10, Math.min(it.time, ds.blocks[deep].start + blockLen(deep) - 5)) : it.time;
    }
    if (it.on === '@halaSig') {
      const sent = ds.blocks.t_b_14, end = sent ? sent.start + blockLen('t_b_14') : null;
      const deep = Object.keys(ds.blocks).filter(id => isDeep(task(id)) && end != null && ds.blocks[id].start >= end && ds.blocks[id].start < T('15:00')).sort((a, b) => ds.blocks[a].start - ds.blocks[b].start)[0];
      at = deep ? ds.blocks[deep].start + 10 : ds.blocks.t_b_15 ? ds.blocks.t_b_15.start : T('14:30');
    }
    if (it.id === 'ti_mom' && ds.blocks.t_buffet_lunch && ((ds.batches || {}).t_buffet_lunch || []).length) at = Math.max(at, ds.blocks.t_buffet_lunch.start + blockLen('t_buffet_lunch')); // the lunch buffet first, then Mom's call
    out.push({ it, at });
  });
  return out.sort((a, b) => a.at - b.at);
}
function liveStart() {
  const ds = DS(); if (ds.closed) return; if (typeof ensureBuffets === 'function') ensureBuffets();
  const starts = Object.values(ds.blocks).map(b => b.start);
  if (!ds.planSnap) ds.planSnap = JSON.parse(JSON.stringify({ blocks: ds.blocks, extra: ds.extra, wa: ds.wa, notes: ds.notes || [], marks: ds.marks || [], durOv: ds.durOv || {} }));
  LIVE.on = true; LIVE.done = false; ds.liveRan = true; save(); LIVE.clock = LIVE.clock != null ? LIVE.clock : Math.min(T('7:00'), ...starts);
  liveResume(); renderAll(); toast('▶ Tuesday has started — watch the line move down Karim\'s day.');
}
/* start the live day again from the plan, without redoing the tools or the calendar */
function liveRestart() {
  const ds = DS(); clearInterval(LIVE.timer);
  Object.assign(LIVE, { on: false, running: false, clock: null, fired: {}, batchesSeen: {}, deepSeen: {}, dfSeen: {}, done: false });
  if (ds.planSnap) { const p = JSON.parse(JSON.stringify(ds.planSnap)); ds.blocks = p.blocks; ds.extra = p.extra; ds.wa = p.wa; ds.notes = p.notes; ds.marks = p.marks; ds.durOv = p.durOv; }
  else { // a day that was played before this option existed: undo what the interruptions added
    ds.marks = []; Object.keys(ds.blocks).forEach(id => { ds.blocks[id].extra = 0; });
    const drop = x => x.app === 'int' || /_cont/.test(x.id) || MOM_TASKS.some(m => m.id === x.id) || /^t_batch_/.test(x.id) || x.id === 't_x_ytvideo';
    ds.extra.filter(drop).forEach(x => delete ds.blocks[x.id]); ds.extra = ds.extra.filter(x => !drop(x));
    (ds.extra || []).forEach(x => { if (x.id.startsWith('t_buffet_')) x.dur = x.planned || x.dur; });
  }
  Object.assign(ds, { batchShown: {}, recorded: {}, ints: {}, tueCost: {}, batches: {}, thoughts: {}, thoughtWait: [], resume: [], waShown: {}, closed: false, slept: false, report: null, calls: [] });
  Object.keys(ds.removed || {}).forEach(id => { if (ds.removed[id] === 'replaced') delete ds.removed[id]; });
  const sl = $('#slide'); if (sl) sl.innerHTML = ''; closeModal(); ui.tueCur = null; ui.app = 'calendar';
  save(); renderAll(); toast('↺ The day is back to your plan — press ▶ Start Tuesday to play it again.');
}
function liveResume() { LIVE.running = true; clearInterval(LIVE.timer); LIVE.timer = setInterval(liveTick, 200); liveBar(); }
function livePause() { LIVE.running = false; clearInterval(LIVE.timer); liveBar(); }
function liveTick() {
  if (!LIVE.running) return;
  if ($('#modal').style.display === 'flex' || ($('#slide') && $('#slide').innerHTML)) return; // waiting for a decision
  const ds = DS(), step = 60 / (LIVE.secPerHour * 5); // minutes per 200 ms
  const prev = LIVE.clock; LIVE.clock = Math.min(GRID_END, LIVE.clock + step);
  // new tasks landed in "To plan" (e.g. Mom's clinic): pause so they can be placed
  if (ui.newTasks) { ui.newTasks = false; livePause(); toast('New tasks were added to "To plan" — place them on the calendar, then press ▶ Resume.', 'warn'); return; }
  // a thought that came during collaborative work waits for the next deep-focus block
  for (const id in ds.blocks) { const s = ds.blocks[id].start; if (s > prev && s <= LIVE.clock && ds.tag[id] === 'deep' && !LIVE.deepSeen[id]) { LIVE.deepSeen[id] = true; const w = (ds.thoughtWait || []).shift(); if (w) { save(); const it = intFind(w); if (it) { ui.tueCur = { id: it.id, on: id, pot: potentialOf(it, task(id)) }; tueThought(it, task(id)); liveDraw(); return; } } } }
  // a batch block starts: the held messages are handled
  for (const id in ds.blocks) { if (!(id.startsWith('t_batch_') || id.startsWith('t_buffet_')) || LIVE.batchesSeen[id]) continue; const s = ds.blocks[id].start; if (s > prev - 0.01 && s <= LIVE.clock) { LIVE.batchesSeen[id] = true; liveBatch(id); liveDraw(); return; } }
  // entering a distraction-free block: tell participants interruptions are blocked here
  for (const id in ds.blocks) { const s = ds.blocks[id].start; if (s > prev - 0.01 && s <= LIVE.clock && ds.mode[id] === 'free' && !(LIVE.dfSeen || (LIVE.dfSeen = {}))[id]) { LIVE.dfSeen[id] = true; liveDF(id); } }
  // interruptions due now
  const next = liveSchedule().find(x => !LIVE.fired[x.it.id] && !ds.ints[x.it.id] && x.at <= LIVE.clock);
  if (next) {
    LIVE.fired[next.it.id] = true; LIVE.clock = Math.max(prev, next.at);
    const cur = blockAt(LIVE.clock);
    if (cur) { ui.tueCur = null; tueFire(next.it, cur); }
    else if (next.it.kind === 'thought') { (ds.thoughtWait = ds.thoughtWait || []).push(next.it.id); save(); } // thoughts only come during deep focus
    else if (next.it.cls === 'must' || next.it.kind === 'call') { ui.tueCur = { id: next.it.id, on: null, pot: next.it.dur || 5 }; tueFull(next.it, { id: null, title: 'free time — nothing planned' }); }
    else { ui.tueCur = { id: next.it.id, on: null, pot: next.it.dur || 5 }; liveFree(next.it); }
    liveDraw(); return;
  }
  // Karim runs out of energy at this point of the day
  if (liveEnergyAt(LIVE.clock) <= 1 && !DS().closed) {
    livePause(); LIVE.done = true; const ds2 = DS(); ds2.slept = 'energy'; closeDay(); renderAll();
    modal(`<div class="sleep"><div class="zz">😴</div><h2>Yaaawn… it's ${fmt(LIVE.clock)} and Karim is out of energy.</h2><p class="lead">The laptop shuts — he's off to bed. Whatever is left will have to wait.</p><div class="actions"><button class="btn primary" data-act="report">See how the day went</button></div></div>`, 'sleep-box');
    return;
  }
  // end of the day
  const last = Math.max(...Object.keys(ds.blocks).map(id => ds.blocks[id].start + blockLen(id)));
  if (LIVE.clock >= last + 5 || LIVE.clock >= GRID_END) { livePause(); LIVE.done = true; liveBar(); modal(`<div class="tue-pop"><div class="tp-h">🌙 <b>Karim's Tuesday is over</b></div><p class="tp-s">See what the interruptions cost — and what your modes, batches and notes saved.</p><div class="actions"><button class="btn primary" data-act="live-report">See the day report</button></div></div>`, 'tue-box'); }
  liveDraw();
}
function liveDF(id) {
  const sp = typeof buffetSpot === 'function' ? buffetSpot(id) : null, b = sp && DS().blocks[sp.bid];
  const el = document.createElement('div'); el.className = 'notif n-df';
  el.innerHTML = `<div class="n-h"><span>🔕 Distraction-free</span><time>${fmt(LIVE.clock)}</time></div><b>${esc(task(id).title)}</b><p>You've blocked interruptions here. Calls, emails, WhatsApp and notifications will wait for your buffet${b ? ' at ' + fmt(b.start) + ' (' + blockLen(sp.bid) + ' min)' : ''}.</p>`;
  const box = $('#toasts'); while (box.children.length >= 4) box.firstChild.remove(); box.appendChild(el); setTimeout(() => el.remove(), 6000);
}
function liveFree(it) { // nothing planned at that moment: it just shows up
  modal(`<div class="tue-pop"><div class="tp-h">${KIND_IC[it.kind] || '🔔'} <b>${esc(who(it))}</b></div><p class="tp-s">${esc(it.subject || it.text || '')}</p><p class="tp-doing">Nothing planned right now — no cost.</p><div class="actions"><button class="btn primary" data-act="modal-close">OK</button></div></div>`, 'tue-box');
  DS().ints[it.id] = { t: LIVE.clock, choice: 'free', kind: 'good' }; (DS().tueCost = DS().tueCost || {})[it.id] = { kind: 'free', mins: 0, potential: 0 }; save();
}
function liveBatch(id) { const ds = DS(), n = ((ds.batches || {})[id] || []).length; ds.batchShown = ds.batchShown || {}; if (n && (ds.batchShown[id] || 0) >= n) return; ds.batchShown[id] = n; save(); batchOpen(id); } // each batch opens once, even after a reload
/* the now-line on the calendar */
function liveDraw() {
  const g = $('#grid'); if (!g || LIVE.clock == null || !isAdapt()) return;
  let l = $('#nowline'); if (!l) { l = document.createElement('div'); l.id = 'nowline'; g.appendChild(l); }
  l.style.top = ((LIVE.clock - GRID_START) * PXM) + 'px'; l.dataset.t = fmt(LIVE.clock);
  const w = $('.grid-wrap'); if (w && LIVE.running) { const y = (LIVE.clock - GRID_START) * PXM; if (y < w.scrollTop + 80 || y > w.scrollTop + w.clientHeight - 160) w.scrollTop = y - 160; }
  const c = $('#live-clock'); if (c) c.textContent = fmt(LIVE.clock);
}
function liveBar() {
  let b = $('#livebar'); if (!b) { b = document.createElement('div'); b.id = 'livebar'; document.body.appendChild(b); }
  if (!isAdapt()) { b.innerHTML = ''; return; }
  if (DS().closed) { b.innerHTML = DS().liveRan ? `<button class="btn" data-act="live-restart">↺ Restart the day (keep my plan)</button>` : ''; liveBarPlace(b); return; }
  if (!LIVE.on && ui.app !== 'calendar') { b.innerHTML = ''; return; }
  const missing = tasks().filter(schedulable).filter(t => needsSort(t) || needsTagMode(t));
  const ready = DS().cqDone && !missing.length;
  if (!LIVE.on && !ready) { b.innerHTML = `<button class="btn" disabled>🔒 Start Tuesday</button><span title="${esc(missing.map(t => t.title).join(' · '))}">${missing.length ? missing.length + ' task' + (missing.length > 1 ? 's' : '') + ' still to sort, tag &amp; mode' : 'Waiting for this morning\'s messages'}</span>`; liveBarPlace(b); return; }
  b.innerHTML = !LIVE.on ? `<button class="btn primary big" data-act="live-start">▶ ${DS().liveRan ? 'Continue' : 'Start'} Tuesday</button>${DS().liveRan ? '<button class="btn" data-act="live-restart">↺ Restart from my plan</button>' : '<span>Plan first — interruptions arrive once the day starts.</span>'}`
    : `<b class="lv-t">⏱ <span id="live-clock">${fmt(LIVE.clock)}</span></b>${LIVE.done ? '<span>Day over</span>' : `<button class="btn" data-act="${LIVE.running ? 'live-pause' : 'live-resume'}">${LIVE.running ? '⏸ Pause' : '▶ Resume'}</button>`}
       <button class="btn" data-act="live-restart" title="Back to your plan, before any interruption">↺ Restart</button>
       <label>Speed <select id="live-speed">${[[20, 'Slow'], [10, 'Normal'], [5, 'Fast']].map(([v, l]) => `<option value="${v}" ${LIVE.secPerHour === v ? 'selected' : ''}>${l}</option>`).join('')}</select></label>`;
  liveBarPlace(b);
}
/* the bar sits in the calendar's own header (never on top of anything); elsewhere it floats small in the bottom corner */
function liveBarPlace(b) {
  if (!document.getElementById('lb-style')) { const st = document.createElement('style'); st.id = 'lb-style';
    st.textContent = '#livebar.lb-inline{position:static;transform:none;box-shadow:none;margin:0 auto 0 14px;padding:3px 12px 3px 4px;flex-wrap:nowrap;white-space:nowrap;gap:8px}#livebar.lb-inline span{max-width:none;font-size:11.5px;padding:0}#livebar.lb-inline .btn{padding:4px 10px;font-size:12.5px}.day-h{flex-wrap:wrap;row-gap:6px}#livebar.lb-float{top:auto;bottom:66px;left:auto;right:16px;transform:none}'; document.head.appendChild(st); }
  const host = ui.app === 'calendar' && !ui.peek ? document.querySelector('.day-h') : null;
  if (host) { const h2 = host.querySelector('h2'); if (b.parentNode !== host) (h2 ? h2.after(b) : host.prepend(b)); b.className = 'lb-inline'; }
  else { if (b.parentNode !== document.body) document.body.appendChild(b); b.className = 'lb-float'; }
}
const _rAll = renderAll;
renderAll = function () { _rAll(); liveBar(); setTimeout(liveDraw, 0); };
document.addEventListener('click', e => {
  const a = e.target.closest('[data-act]'); if (!a) return;
  if (a.dataset.act === 'live-start') { if (!(DS().cqDone && !tasks().filter(schedulable).some(t => needsSort(t) || needsTagMode(t)))) return; ui.app = 'calendar'; liveStart(); }
  else if (a.dataset.act === 'live-restart') { if (armOk(a, 'Restart Tuesday from your plan? Everything that happened during the live day will be undone.')) liveRestart(); }
  else if (a.dataset.act === 'live-pause') livePause();
  else if (a.dataset.act === 'live-resume') { ui.app = 'calendar'; renderAll(); liveResume(); }
  else if (a.dataset.act === 'live-report') { closeModal(); closeDay(); renderAll(); showReport(); }
});
document.addEventListener('change', e => { if (e.target.id === 'live-speed') { LIVE.secPerHour = Number(e.target.value); } });

/* on load: a Tuesday that was closed by "energy" while still being planned (older versions) is reopened,
   and the live bar is drawn straight away */
(function () {
  const t = S.days.tue;
  if (t && t.closed && !t.liveRan && t.slept) { t.closed = false; t.slept = false; t.report = null; save(); }
  setTimeout(() => { renderAll(); }, 50);
})();

window.__allLoaded = true;
