import os as _os
CHROME = {'executable_path': _os.environ['CHROMIUM']} if _os.environ.get('CHROMIUM') else {}
HERE = _os.path.dirname(_os.path.abspath(__file__))
PAGE = 'file://' + _os.path.join(_os.path.dirname(HERE), 'public', 'index.html')
import asyncio, sys
from playwright.async_api import async_playwright
F=sys.argv[1] if len(sys.argv) > 1 else PAGE
SETUP="""(()=>{S.arrivalSec=0; closeModal(); place('s_inbox',T('13:15')); restartTomorrow(); closeDay(); S.round=1; let t=DS(); t.briefSeen=true; t.cqDone=true; t.revealDone=true; restartTomorrow(); closeDay(); S.round=2; t=DS(); t.briefSeen=true; t.cqDone=true; t.revealDone=true;
  tasks().filter(schedulable).forEach(x=>{ if(needsSort(x)) t.quad[x.id]='q1'; if(needsTagMode(x)) { t.tag[x.id]='collab'; t.mode[x.id]='reduced'; } });
  ['t_prepmeet','t_esc78','t_study'].forEach(id=>{ t.tag[id]='deep'; t.mode[id]='free'; }); t.tag.t_esc78='deep'; t.mode.t_esc78='reduced';
  ui.app='calendar'; renderAll(); closeModal(); place('t_l_commute1',T('8:00')); })()"""
async def fresh(b):
    pg=await b.new_page(viewport={'width':1440,'height':900}); errs=[]; pg.on('pageerror',lambda e: errs.append((e.stack or str(e))[:300])); pg.on('dialog', lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(F); await pg.wait_for_timeout(300); await pg.evaluate(SETUP); await pg.wait_for_timeout(300); await pg.evaluate("closeModal()")
    return pg, errs
L="[...document.querySelectorAll('.toast')].map(t=>t.textContent).slice(-1)[0]"
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**CHROME)
    live='LIVE' in F
    pg,errs=await fresh(b)
    # 2. print & brief only after Hala's note
    print('2 brief before reading', await pg.evaluate("place('t_offersbrief',T('10:00'))"), '|', await pg.evaluate(L))
    await pg.evaluate("place('t_halaoffers',T('9:30'))"); await pg.wait_for_timeout(700); await pg.evaluate("closeModal(); const s=$('#slide'); if(s) s.innerHTML=''; ui.tueCur=null")
    print('2 brief overlapping the note', await pg.evaluate("place('t_offersbrief',T('9:35'))"), '| after it', await pg.evaluate("place('t_offersbrief',T('10:00'))"))
    # 1. the team meeting moves with its preparation
    await pg.evaluate("place('t_prepmeet',T('13:30'))"); await pg.wait_for_timeout(700)
    if live: await pg.evaluate("tueFire(intList('tue').find(i=>i.id==='ti_yassin'),'t_prepmeet')"); await pg.wait_for_timeout(300)
    if await pg.query_selector('#modal [data-act="th-check"]'): await pg.click('#modal [data-act="th-check"]'); await pg.wait_for_timeout(300)
    await pg.evaluate("closeModal()")
    print('1 prep / meeting', await pg.evaluate("[fmt(DS().blocks.t_prepmeet.start)+'+'+blockLen('t_prepmeet'), fmt(DS().blocks.t_teammeet.start), Object.keys(DS().blocks).some(k=>/_cont/.test(k))]"))
    # 3 + 7. Mom's call: clinic visit placed at 9:10 PM, side notification; nothing else between course and clinic
    await pg.evaluate("place('t_ccxp',T('19:00')); place('t_study',T('21:00'))"); await pg.wait_for_timeout(700); await pg.evaluate("closeModal(); ui.tueCur=null")
    await pg.evaluate("place('t_l_lunch',T('12:30'))"); await pg.wait_for_timeout(700)
    if live: await pg.evaluate("closeModal(); ui.tueCur=null; tueFire(intList('tue').find(i=>i.id==='ti_mom'),'t_l_lunch')"); await pg.wait_for_timeout(400)
    if await pg.query_selector('#modal .cp-b.yes'): await pg.click('#modal .cp-b.yes'); await pg.wait_for_timeout(400)
    if await pg.query_selector('#modal .call-script'): await pg.click('#modal [data-act="tue-now"]')  # rc24: hang up after Mom's dialogue
    await pg.wait_for_timeout(900)
    print('3 clinic', await pg.evaluate("[DS().blocks.t_x_clinic?fmt(DS().blocks.t_x_clinic.start):null, DS().blocks.t_study?fmt(DS().blocks.t_study.start):'tray', !!document.querySelector('.mom-note')]"))
    await pg.evaluate("closeModal()")
    print('7 gap after course', await pg.evaluate("[place('t_halaoffers',T('21:00')) , place('t_x_clinic_call',T('21:00'))]"), '|', await pg.evaluate("[...document.querySelectorAll('.toast')].map(t=>t.textContent).filter(t=>/clinic/.test(t)).slice(-1)[0]"))
    print('errors A', errs or 'none'); await pg.close()
    # 4. Facebook tag (reduced mode) → opens the post
    pg,errs=await fresh(b)
    await pg.evaluate("place('t_esc78',T('11:30'))"); await pg.wait_for_timeout(700)
    if live: await pg.evaluate("tueFire(intList('tue').find(i=>i.id==='ti_fb'),'t_esc78')"); await pg.wait_for_timeout(400)
    if await pg.query_selector('#slide [data-act="tue-now"]'): await pg.click('#slide [data-act="tue-now"]'); await pg.wait_for_timeout(400)
    print('4 facebook', await pg.evaluate("[ui.app, !!document.querySelector('#fb-tagged.fb-hi'), !!document.getElementById('fb-back')]"))
    await pg.click('#fb-back [data-act="tue-now"]'); await pg.wait_for_timeout(400)
    print('4 back', await pg.evaluate("[ui.app, (document.querySelector('#modal .gc-b p,#modal .rc-b p')||{}).textContent?.slice(0,50)]"))
    print('errors B', errs or 'none'); await pg.close()
    # 6. burst tap wording
    pg,errs=await fresh(b)
    await pg.evaluate("place('t_ccxp',T('19:00')); place('t_study',T('21:00'))"); await pg.wait_for_timeout(700)
    if live: await pg.evaluate("closeModal(); ui.tueCur=null; tueFire(intList('tue').find(i=>i.id==='ti_tap'),'t_study')"); await pg.wait_for_timeout(400)
    print('6 tap buttons', await pg.evaluate("[...document.querySelectorAll('#modal .actions button')].map(b=>b.textContent)"))
    await pg.click('#modal [data-act="desk-note"]'); print('6 note label', await pg.evaluate("document.querySelector('#rtr label').firstChild.textContent"))
    await pg.fill('#rtr-t','chapter 3 page 41 practice questions'); await pg.click('#modal [data-act="desk-note"]'); await pg.wait_for_timeout(300)
    print('6 card', await pg.evaluate("(document.querySelector('#modal .gc-b p')||{}).textContent?.slice(0,60)"))
    print('errors C', errs or 'none'); await pg.close()
    # 5. manual: planning past a batch opens it
    if not live:
      pg,errs=await fresh(b)
      await pg.evaluate("place('t_huddle',T('9:15'))"); await pg.wait_for_timeout(700); await pg.click('#slide [data-act="tue-batch"]'); await pg.wait_for_timeout(300); await pg.evaluate("closeModal()")
      await pg.evaluate("place('t_crm',T('10:00'))"); await pg.wait_for_timeout(700)
      for k in range(3):
        if await pg.query_selector('#modal .cp-b.no'): await pg.click('#modal .cp-b.no'); await pg.wait_for_timeout(300); await pg.evaluate("closeModal()")
      await pg.wait_for_timeout(1500)
      print('5 batch opened', await pg.evaluate("[!!document.querySelector('#modal .bv'), document.querySelector('#modal .bv .tp-h')?.textContent]"))
      print('errors D', errs or 'none'); await pg.close()
    await b.close()
asyncio.run(main())
