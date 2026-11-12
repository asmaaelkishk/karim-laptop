import os as _os
CHROME = {'executable_path': _os.environ['CHROMIUM']} if _os.environ.get('CHROMIUM') else {}
HERE = _os.path.dirname(_os.path.abspath(__file__))
PAGE = 'file://' + _os.path.join(_os.path.dirname(HERE), 'public', 'index.html')
import asyncio, sys
from playwright.async_api import async_playwright
F=sys.argv[1] if len(sys.argv) > 1 else PAGE
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**CHROME)
    pg=await b.new_page(viewport={'width':1440,'height':900}); errs=[]; pg.on('pageerror',lambda e: errs.append((e.stack or str(e))[:300]))
    await pg.goto(F); await pg.wait_for_timeout(300)
    await pg.evaluate("S.arrivalSec=0; closeModal(); place('s_inbox',T('13:15')); restartTomorrow(); closeDay(); S.carry.mon.tasks=S.carry.mon.tasks.filter(t=>!t.leftover); S.round=1; const t=DS(); t.briefSeen=true; t.cqDone=true; t.revealDone=true; t.growSeen={m_study:true}; ['m_b_12','m_b_13','m_b_14','m_b_15'].forEach(i=>t.quad[i]='q1'); t.blocks.m_l_commute1={start:T('8:00'),extra:0}; ui.app='calendar'; renderAll(); closeModal()")
    print('step 1', await pg.evaluate("place('m_b_12',T('13:30'))")); await pg.wait_for_timeout(900)
    if await pg.query_selector('#modal [data-act="trig-take"]'): await pg.click('#modal [data-act="trig-take"]'); await pg.wait_for_timeout(600)
    for k in range(4):
      if await pg.evaluate("$('#modal').style.display==='flex'"): 
        if await pg.query_selector('#modal [data-act="lv-end"]'): await pg.click('#modal [data-act="lv-end"]'); await pg.wait_for_timeout(300)
        await pg.evaluate("closeModal()")
    print('blocks', await pg.evaluate("Object.entries(DS().blocks).filter(([k])=>/m_b_|m_x_/.test(k)).sort((a,b)=>a[1].start-b[1].start).map(([k,v])=>k+'@'+fmt(v.start)+'+'+blockLen(k)).join(', ')"))
    print('step 2 right after the interruption ('+await pg.evaluate("fmt(stepEnd('m_b_12'))")+')', await pg.evaluate("place('m_b_13', stepEnd('m_b_12'))"), await pg.evaluate("[...document.querySelectorAll('.toast')].map(t=>t.textContent).slice(-1)[0]"))
    print('step 2 with a real gap', await pg.evaluate("delete DS().blocks.m_b_13, place('m_b_13', stepEnd('m_b_12')+10)"), '| back to back again', await pg.evaluate("place('m_b_13', stepEnd('m_b_12'))"))
    print('another task inside the cycle', await pg.evaluate("place('m_b_14', DS().blocks.m_b_13.start+blockLen('m_b_13')) && place('m_crm', DS().blocks.m_b_13.start+blockLen('m_b_13'))"), '| gaps', await pg.evaluate("cycleGaps()"))
    print(errs or 'NO ERRORS'); await b.close()
asyncio.run(main())
