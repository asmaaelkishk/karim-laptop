/* =========================================================
   MANUAL TUESDAY — interruptions arrive while planning:
   placing a task on the calendar fires its interruption (same set-up, same modes, buffets and batches).
   ========================================================= */
var LIVE; // (the live day isn't part of this version)
tueFireFor = function (id) {
  const ds = DS(), t = task(id); if (!t || ds.closed) return;
  const deep = ds.tag[id] === 'deep';
  const list = intList(D()).filter(i => i.trigger === D() && !ds.ints[i.id] && !(ds.thoughtWait || []).includes(i.id) && (!i.cond || i.cond()) && !((ds.wFired || {})[i.id]));
  let it = list.find(i => i.on === id || (i.onRx && i.onRx.test(id)));
  const b0 = ds.blocks[id], fits = i => b0 && b0.start + blockLen(id) > i.time && (i.until == null || b0.start < i.until) && (!i.workTask || isWorkTask(t));
  if (!it && deep && !/_stats$/.test(id)) { it = list.find(i => i.on === '@deep' && fits(i)); }
  if (!it && ds.tag[id] === 'collab') it = list.find(i => i.on === '@collab' && fits(i));
  if (!it && t.app !== 'life' && !t.habitCard && !/_ccxp/.test(id)) it = list.find(i => i.on === '@any' && fits(i));
  if (it && D() === 'wed') (ds.wFired = ds.wFired || {})[it.id] = true; // v1.2: an interruption chosen once is never chosen again, even if it was held
  if (!it && deep && (ds.thoughtWait || []).length) { // a thought that came during other work surfaces in the next deep task
    const w = ds.thoughtWait.shift(); save(); const wi = intFind(w);
    if (wi) { ui.tueCur = { id: wi.id, on: id, pot: potentialOf(wi, t) }; tueThought(wi, t); return; }
  }
  if (it) tueFire(it, id);
};
window.__allLoaded = true;
setTimeout(() => renderAll(), 50);

/* planning past a batch or buffet opens it, so Karim sees what was waiting (manual version) */
function manualBatchReach(placedId) {
  const ds = DS(), b = ds.blocks[placedId]; if (!b || placedId.startsWith('t_batch_') || placedId.startsWith('t_buffet_')) return;
  ui.reachUpTo = Math.max(ui.reachUpTo || 0, b.start); if (ui.reachWaiting) return; ui.reachWaiting = true; // one check at a time: a batch opens once, never repeatedly
  let tries = 0; const go = () => {
    if ($('#modal').style.display === 'flex' || (($('#slide') || {}).innerHTML)) { if (tries++ < 150) return setTimeout(go, 400); ui.reachWaiting = false; return; }
    const ds2 = DS(); ds2.batchShown = ds2.batchShown || {};
    const due = Object.keys(ds2.blocks).filter(id => (id.startsWith('t_batch_') || id.startsWith('t_buffet_')) && ds2.blocks[id].start <= ui.reachUpTo && ((ds2.batches || {})[id] || []).length > (ds2.batchShown[id] || 0)).sort((x, y) => ds2.blocks[x].start - ds2.blocks[y].start)[0];
    if (!due) { ui.reachWaiting = false; return; }
    ds2.batchShown[due] = (ds2.batches[due] || []).length; save(); toast('📥 Karim reaches "' + task(due).title + '" — here\'s what was waiting.'); batchOpen(due);
    tries = 0; setTimeout(go, 600); // next one (if several were reached), after this one is closed
  };
  setTimeout(go, 700);
}
const _tffM = tueFireFor;
tueFireFor = function (id) {
  const ds = DS(), items = ((ds.batches || {}).t_buffet_lunch || []).length; ds.batchShown = ds.batchShown || {};
  if (/_l_lunch$/.test(id) && items > (ds.batchShown.t_buffet_lunch || 0)) { // at lunch: first what was held for the buffet, then whatever comes in
    ensureBuffets(); ds.batchShown.t_buffet_lunch = items; save(); toast('🍽️ Lunch — first, your interruption buffet: here is what was held for it.'); batchOpen('t_buffet_lunch');
    let tries = 0; const go = () => { if ($('#modal').style.display === 'flex') { if (tries++ < 150) setTimeout(go, 400); return; } _tffM(id); };
    setTimeout(go, 500); return;
  }
  const before = JSON.stringify(ds.batches || {});
  _tffM(id); manualBatchReach(id);
  if (ds.mode[id] === 'free' && ds.tag[id] === 'deep') setTimeout(() => manualDF(id, before), 350);
};
window.MANUAL_DF = true;
/* placing a distraction-free task: a side notification like the live version — what was blocked and when it will show up */
function manualDF(id, before) {
  const ds = DS(), t = task(id); if (!t || !ds.blocks[id]) return;
  const was = JSON.parse(before || '{}'), held = [];
  Object.entries(ds.batches || {}).forEach(([bid, list]) => list.forEach(iid => { if (!(was[bid] || []).includes(iid)) { const it = intFind(iid); if (it) held.push({ it, bid }); } }));
  const sp = buffetSpot(id), b = ds.blocks[sp.bid];
  const when = b ? 'at ' + fmt(b.start) + (sp.lunch ? ' (lunch)' : '') : sp.lunch ? 'at lunch — it appears once lunch is on the calendar' : 'right after this task';
  const el = document.createElement('div'); el.className = 'notif n-df';
  el.innerHTML = `<div class="n-h"><span>🔕 Distraction-free</span><time>${fmt(ds.blocks[id].start)}</time></div><b>${esc(t.title)}</b>`
    + (held.length ? `<p>${held.length} interruption${held.length > 1 ? 's were' : ' was'} blocked: ${held.map(h => '<b>' + esc(who(h.it)) + '</b> (' + esc(APPN[h.it.kind] || h.it.kind) + ') — waits for ' + (/^w_hab_batch[12]$/.test(h.bid) ? 'your email window ' + h.bid.slice(-1) + (ds.blocks[h.bid] ? ' at ' + fmt(ds.blocks[h.bid].start) : '') : /^t_buffet_after_/.test(h.bid) ? 'the end of this task' + (ds.blocks[h.bid] ? ' (' + fmt(ds.blocks[h.bid].start) + ')' : '') : 'your interruption buffet ' + when)).join('; ')}.</p>`
      : `<p>You've blocked interruptions here. Calls, emails, WhatsApp and notifications will wait for your interruption buffet ${when}.</p>`);
  const box = $('#toasts'); while (box.children.length >= 4) box.firstChild.remove(); box.appendChild(el); setTimeout(() => el.remove(), 8000);
}

/* v1.2 — Karim's email-batching habit: routine emails go straight to the next email window, no decision, no refocus */
const _tffBatch = tueFireFor;
tueFireFor = function (id) {
  const tt0 = task(id); if (D() === 'wed' && tt0 && (tt0.habitCard || tt0.personal || tt0.fixedLife || tt0.app === 'life')) return; // no interruptions in Karim's personal or habit time
  if (D() === 'wed' && tt0 && !DS().mode[id]) { const ds0 = DS(); ds0.tag[id] = ds0.tag[id] || (tt0.type === 'deep' ? 'deep' : 'collab'); ds0.mode[id] = 'reduced'; } // a work task with no mode yet (e.g. the AI form) behaves as reduced: notifications can be batched, and handling them now costs
  if (D() === 'wed' && tt0) { const ds0 = DS(); if ((ds0.tag[id] || tt0.type) === 'deep' && ds0.mode[id] !== 'free') { ds0.mode[id] = 'free'; if (!ds0.deepRuleSeen) { ds0.deepRuleSeen = true; setTimeout(() => toast('Deep focus: nothing gets through except desk visits — emails wait for your email window, other notifications for the lunch buffet.'), 50); } } }
  const ds = DS(), w = ['w_hab_batch1', 'w_hab_batch2'].filter(x => ds.blocks[x]);
  if (false && D() === 'wed' && w.length) { // v1.2 (rc16): no automatic routing — Karim chooses email window 1 or 2 in the batch picker
    const t = task(id), b = ds.blocks[id];
    const list = intList('wed').filter(i => i.trigger === 'wed' && !ds.ints[i.id] && i.kind === 'email' && i.cls !== 'must' && (!i.cond || i.cond()) && (i.on === id || (i.on === '@collab' && ds.tag[id] === 'collab' && b && b.start + blockLen(id) > i.time)));
    const it = list[0];
    if (it && b) { const win = w.find(x => ds.blocks[x].start >= b.start + blockLen(id)); const opens = win ? ds.blocks[win].start : null;
      if (win && (!it.batchWithin || opens <= b.start + it.batchWithin)) {
        ui.tueCur = { id: it.id, on: id, pot: potentialOf(it, t) }; tueHold(it, win, false); ui.tueCur = null; ds.habBatched = (ds.habBatched || 0) + 1; save(); renderAll();
        greenCard('📥 ' + (it.from || 'An email') + ' — it waits for your email window at ' + fmt(opens) + '. Your email-batching habit just saved Karim a decision and a refocus.', 'No time lost on "' + t.title + '".'); return; } }
  }
  return _tffBatch(id);
};
