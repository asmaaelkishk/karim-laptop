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
    pg=await b.new_page(viewport={'width':1440,'height':900}); errs=[]; pg.on('pageerror',lambda e: errs.append((e.stack or str(e))[:300])); pg.on('dialog', lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(F); await pg.wait_for_timeout(300)
    await pg.evaluate("S.arrivalSec=0; closeModal(); restartTomorrow(); closeDay(); S.round=1; const t=DS(); t.briefSeen=true; t.cqDone=true; t.revealDone=true; t.growSeen={m_study:true}; t.blocks.m_l_commute1={start:T('8:00'),extra:0}; renderAll(); closeModal()")
    print('eisen hint', await pg.evaluate("(ui.app='tools', ui.tool='eisen', renderAll(), (!!document.querySelector('aside.eis-pile .ai-hint-all') && !document.querySelector('aside.tray .ai-hint-all') && !document.querySelector('.eis-hint')))"))  # rc28: hint on the task cards
    await pg.evaluate("setQuad('m_groceries','q4')"); await pg.wait_for_timeout(300)
    print('green delete card', await pg.evaluate("!!document.querySelector('#modal .gc-b')")); await pg.evaluate("closeModal()")
    r=await pg.evaluate("""(()=>{ const ds=DS(); ds.quad.m_hala3m='q1'; ds.neg.m_hala3m={status:'open',chat:[],met:{},tries:0,batna:'x',opts:['shift'],pickDay:2}; const n=negotiateMsg(task('m_hala3m'),"I'm covering my team today because Mariam is off sick, can I send it tomorrow morning? Our meeting is next week."); closeModal(); return [n.status, status(task('m_hala3m')), tasks().filter(t=>t.spawned).map(t=>t.id).join(',')]; })()""")
    print('negotiation', r)
    print('cycle rule', await pg.evaluate("[place('m_a_13',T('11:00')), place('m_a_12',T('11:00')), place('m_a_13',T('11:40'))]"))
    print('stats rule', await pg.evaluate("[place('m_stats',T('15:00'))]"))
    await pg.evaluate("closeModal(); closeDay(); showReport()"); await pg.wait_for_timeout(300)
    print('report', await pg.evaluate("[!!document.querySelector('#modal .gains'), !!document.querySelector('#modal .bd'), !!document.querySelector('#modal .rep-top [data-act=next-round]')]"))
    print(errs or 'NO ERRORS'); await b.close()
asyncio.run(main())
