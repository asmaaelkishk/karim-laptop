import os as _os
CHROME = {'executable_path': _os.environ['CHROMIUM']} if _os.environ.get('CHROMIUM') else {}
HERE = _os.path.dirname(_os.path.abspath(__file__))
PAGE = 'file://' + _os.path.join(_os.path.dirname(HERE), 'public', 'index.html')
import asyncio, sys
from playwright.async_api import async_playwright
F=sys.argv[1] if len(sys.argv) > 1 else PAGE
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' — '+str(x) if x!='' else ''))
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**CHROME)
    pg=await b.new_page(viewport={'width':1440,'height':900}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)[:300]))
    toast="[...document.querySelectorAll('.toast')].map(x=>x.textContent).slice(-1)[0]||''"
    async def fresh():
      await pg.goto(F); await pg.wait_for_timeout(300); await pg.evaluate("localStorage.clear()"); await pg.goto(F); await pg.wait_for_timeout(400)
    async def setup(rnd):
      await pg.evaluate(f"S.round={rnd}; renderAll(); closeModal(); const ds=DS(); ds.briefSeen=true; S.arrivalSec=0; ds.revealDone=true; ds.cqDone=true; pendingArrivals().forEach(t=>{{ds.got[arrKey(t)]=true}}); save(); renderAll(); closeModal()")
    # ---- (6) Tuesday / Wednesday negotiation without score card
    for rnd,tid,day in [(2,'t_delivery',4),(3,'w_hrtrain',7)]:
      await fresh(); await setup(rnd)
      ids=await pg.evaluate("tasks().filter(t=>t.negotiable&&!t.spawned).map(t=>t.id)")
      if tid not in ids: tid=ids[0]
      await pg.evaluate(f"DS().quad['{tid}']='q1'; ui.negFor='{tid}'; ui.nopts=['shift']; ui.app='tools'; ui.tool='negotiate'; renderAll(); closeModal()"); await pg.wait_for_timeout(200)
      if not await pg.evaluate("!!document.querySelector('#neg-day')"): await pg.click('[data-nopt="shift"]'); await pg.wait_for_timeout(150)
      opts=await pg.evaluate("[...document.querySelectorAll('#neg-day option')].map(o=>o.value).filter(Boolean)")
      await pg.select_option('#neg-day', opts[-1] if str(day) not in opts else str(day))
      await pg.fill('#batna','I send what I have and flag the gap')
      rows=await pg.evaluate("document.querySelectorAll('.ns-row').length")
      ok(f'(6) round {rnd}: no score card', rows==0, rows)
      await pg.click('[data-act="neg-score"]'); await pg.wait_for_timeout(300)
      ok(f'(6) round {rnd}: agreed with options + day + BATNA', await pg.evaluate(f"(DS().neg['{tid}']||{{}}).status")=='accepted', await pg.evaluate(toast))
    # VIP still needs the split on Tuesday
    await fresh(); await setup(2)
    await pg.evaluate("DS().quad.t_vip='q1'; ui.negFor='t_vip'; ui.nopts=['shift']; ui.app='tools'; ui.tool='negotiate'; renderAll(); closeModal()"); await pg.wait_for_timeout(200)
    o=await pg.evaluate("[...document.querySelectorAll('#neg-day option')].map(o=>o.value).filter(Boolean)"); (o and await pg.select_option("#neg-day",o[0])); await pg.fill("#batna","x")
    await pg.click('[data-act="neg-score"]'); await pg.wait_for_timeout(300)
    ok('(6) VIP without a split is still refused', await pg.evaluate("(DS().neg.t_vip||{}).status")!='accepted', await pg.evaluate(toast))
    # Monday unchanged: first scored, later not
    await fresh(); await setup(1)
    await pg.evaluate("DS().quad.m_hala3m='q1'; ui.negFor='m_hala3m'; ui.nopts=['shift']; ui.app='tools'; ui.tool='negotiate'; renderAll(); closeModal()"); await pg.wait_for_timeout(200)
    ok('(6) Monday first task still scored 0-1', await pg.evaluate("document.querySelectorAll('.ns-row').length")==5)
    # ---- (7) no more than 2 negotiated deadlines on one day
    await fresh(); await setup(1)
    await pg.evaluate("S.days.mon.neg={a1:{status:'accepted',dayIdx:3},a2:{status:'accepted',dayIdx:3}}; S.days.mon.negFirst='a1'; save()")
    await pg.evaluate("DS().quad.m_privacy='q1'; ui.negFor='m_privacy'; ui.nopts=['shift']; ui.app='tools'; ui.tool='negotiate'; renderAll(); closeModal()"); await pg.wait_for_timeout(200)
    if not await pg.evaluate("!!document.querySelector('#neg-day')"): await pg.click('[data-nopt="shift"]'); await pg.wait_for_timeout(150)
    await pg.focus('#neg-day'); lab=await pg.evaluate("[...document.querySelectorAll('#neg-day option')].map(o=>o.textContent).join(' | ')")
    ok('(7) picker marks Wednesday full', 'full' in lab, lab)
    await pg.select_option('#neg-day','3'); await pg.fill('#batna','x'); await pg.click('[data-act="neg-score"]'); await pg.wait_for_timeout(300)
    ok('(7) moving a third task to Wednesday is refused', (await pg.evaluate("(DS().neg.m_privacy||{}).status"))!='accepted', await pg.evaluate(toast))
    o=await pg.evaluate("[...document.querySelectorAll('#neg-day option')].map(o=>o.value).filter(v=>v&&v!=='3')")
    if o:
      await pg.select_option('#neg-day',o[0]); await pg.click('[data-act="neg-score"]'); await pg.wait_for_timeout(300)
      ok('(7) another day is accepted', (await pg.evaluate("(DS().neg.m_privacy||{}).status"))=='accepted', await pg.evaluate(toast))
    else: ok('(7) other day available', False, 'no other day offered for m_privacy')
    # ---- (8) offers are Q2: no deadline, not late
    await fresh(); await setup(2)
    r=await pg.evaluate("['t_halaoffers','t_offersbrief'].map(i=>{const t=task(i);return [i,t.dueMin==null,!t.negotiable,!!t.q2target]})")
    ok('(8) offer tasks have no deadline, aren\'t negotiable, count as Q2 work', all(x[1] and x[2] and x[3] for x in r), r)
    # ---- (3) Ahmed: voice + CV only; voice plays in the chat
    await fresh(); await setup(1)
    await pg.evaluate("place('m_ccxp',T('19:00'))"); await pg.wait_for_timeout(700)
    pop=await pg.evaluate("$('#modal').innerText")
    ok('(3) popup shows the voice note and CV, no repeated text', 'Voice message' in pop and 'Ahmed_CV.pdf' in pop and 'بعتلك' not in pop and 'محتاج رأيك' not in pop)
    await pg.click('#modal [data-act="ahmed-open"]'); await pg.wait_for_timeout(400)
    ok('(3) Open goes to Ahmed\'s WhatsApp chat', await pg.evaluate("ui.app==='whatsapp' && ui.chat==='ahmed'"))
    msgs=await pg.evaluate("DS().wa.filter(m=>m.chat==='ahmed').map(m=>m.voice?'voice':m.file?'file':'text')")
    ok('(3) chat has the voice note and the CV only', msgs==['voice','file'], msgs)
    await pg.click('.vplay[data-audio="ahmed"]'); await pg.wait_for_timeout(1500)
    ok('(3) the voice note plays from the chat', await pg.evaluate("!!curAudio && !curAudio.paused && curAudio.currentTime>0.5"))
    await pg.click('#ahmed-back [data-act="ahmed-back"]'); await pg.wait_for_timeout(400)
    ok('(3) Done -> back, absence consequence', await pg.evaluate("!!DS().ccxpAbsent && /absence/i.test($('#modal').innerText)"))
    msgs=await pg.evaluate("DS().wa.filter(m=>m.chat==='ahmed').map(m=>m.voice?'voice':m.file?'file':'text')")
    ok('(3) no duplicate messages after the outcome', msgs==['voice','file'], msgs)
    await fresh(); await setup(1)
    await pg.evaluate("place('m_ccxp',T('19:00'))"); await pg.wait_for_timeout(700); await pg.click('#modal [data-act="trig-leave"]'); await pg.wait_for_timeout(300)
    msgs=await pg.evaluate("DS().wa.filter(m=>m.chat==='ahmed').map(m=>m.voice?'voice':m.file?'file':'text')")
    ok('(3) Later: reminder added, chat has voice + CV only', await pg.evaluate("!!task('m_cv')") and msgs==['voice','file'], msgs)
    # ---- (2) car call: sound plays; if the browser refuses, the screen stays with a Play button
    await fresh(); await setup(1)
    await pg.evaluate("place('m_l_lunch',T('13:30'))"); await pg.wait_for_timeout(800); await pg.click('#modal [data-act="trig-take"]'); await pg.wait_for_timeout(1500)
    ok('(2) car call plays on Answer', await pg.evaluate("!!curAudio && curAudio.currentTime>0.5"))
    await pg.click('#modal [data-act="lv-end"]'); await pg.wait_for_timeout(300); await pg.evaluate("closeModal()")
    await fresh(); await setup(1)
    await pg.evaluate("(()=>{HTMLMediaElement.prototype.play=function(){return Promise.reject(new Error('blocked'))}; return 1})()")
    await pg.evaluate("place('m_l_lunch',T('13:30'))"); await pg.wait_for_timeout(800); await pg.click('#modal [data-act="trig-take"]'); await pg.wait_for_timeout(800)
    ok('(2) blocked sound: call screen stays open with a Play button', await pg.evaluate("!!document.querySelector('#modal .call-pop [data-act=\"lv-play\"]')"), await pg.evaluate(toast))
    print(errs or 'NO ERRORS'); await b.close()
asyncio.run(main())
