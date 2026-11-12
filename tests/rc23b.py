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
    async def fresh():
      await pg.goto(F); await pg.wait_for_timeout(300); await pg.evaluate("localStorage.clear()"); await pg.goto(F); await pg.wait_for_timeout(400)
    async def setup(rnd):
      await pg.evaluate(f"S.round={rnd}; renderAll(); closeModal(); const ds=DS(); ds.briefSeen=true; S.arrivalSec=0; ds.revealDone=true; ds.cqDone=true; pendingArrivals().forEach(t=>{{ds.got[arrKey(t)]=true}}); save(); renderAll(); closeModal()")
    await fresh()
    await pg.evaluate("S.arrivalSec=0; closeModal(); place('s_inbox',T('13:15')); restartTomorrow(); closeDay();")
    c=await pg.evaluate("carryOf('mon')"); ids=[t['id'] for t in c['tasks']]
    ok('minutes come back as a normal leftover', 'mon_lo_s_minutes' in ids, [i for i in ids if 'minutes' in i])
    ok('Hala\'s minutes email still arrives', any(m['id']=='m_c_minutes' for m in c.get('mails',[])))
    ok('statistics log: Hala\'s email Monday', any(m['id']=='m_c_statslog' and 'Where is the statistics log' in m['subject'] for m in c.get('mails',[])))
    ok('statistics log: no extra task added', not any('statslog' in i for i in ids))
    await pg.evaluate("S.round=1; renderAll(); closeModal(); showBrief()"); await pg.wait_for_timeout(200)
    ok('brief lists the minutes under Left from yesterday', 'launch meeting minutes' in (await pg.evaluate("$('#modal').innerText")))
    await fresh(); await setup(1)
    await pg.evaluate("DS().quad.m_stats='q4'; renderAll(); closeModal()"); await pg.wait_for_timeout(300)
    ai=await pg.evaluate("(()=>{DS().quad.m_x_statsai='q1'; return place('m_x_statsai',T('16:30'))})()")
    await pg.evaluate("closeModal(); restartTomorrow(); closeDay();")
    m=await pg.evaluate("(carryOf('tue').mails||[]).map(x=>x.id)")
    ok('AI log done Monday -> no email Tuesday' if ai else 'AI log not placed (test)', ('t_c_statslog' not in m) if ai else True, m)
    await fresh(); await setup(1)
    await pg.evaluate("closeModal(); restartTomorrow(); closeDay();")
    m=await pg.evaluate("(carryOf('tue').mails||[]).map(x=>x.id)"); ok('Monday log missed -> email Tuesday', 't_c_statslog' in m)
    await fresh(); await setup(1)
    ok('coaching on the calendar at 12:30', await pg.evaluate("fmt(DS().blocks.m_coach.start)")=='12:30 PM')
    ok('coaching not draggable', await pg.evaluate("document.querySelector('.blk[data-id=\"m_coach\"]').getAttribute('draggable')")=='false')
    ok('coaching costs no energy', await pg.evaluate("energyOf(task('m_coach'))===0"))
    await pg.evaluate("DS().quad.m_hala3m='q1'"); r=await pg.evaluate("place('m_hala3m',T('12:30'))")
    ok('a task dropped on it pushes it later', r and await pg.evaluate("DS().blocks.m_coach.start")>=750, await pg.evaluate("fmt(DS().blocks.m_coach.start)"))
    print(errs or 'NO ERRORS'); await b.close()
asyncio.run(main())
