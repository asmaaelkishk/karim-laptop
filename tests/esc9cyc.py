import os as _os
CHROME = {'executable_path': _os.environ['CHROMIUM']} if _os.environ.get('CHROMIUM') else {}
HERE = _os.path.dirname(_os.path.abspath(__file__))
PAGE = 'file://' + _os.path.join(_os.path.dirname(HERE), 'public', 'index.html')
import asyncio, sys
from playwright.async_api import async_playwright
exec(open('v12.py').read().split('L="[...')[0])
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**CHROME)
    live='LIVE' in F
    pg,errs=await fresh(b)
    await pg.evaluate("place('t_a_12',T('10:00'))"); await pg.wait_for_timeout(800)
    if live: await pg.evaluate("tueFire(intList('tue').find(i=>i.id==='ti_mariam'),'t_a_12')"); await pg.wait_for_timeout(400)
    await pg.click('#modal [data-act="desk-later"]'); await pg.wait_for_timeout(400); await pg.evaluate("closeModal()")
    print('blocks', await pg.evaluate("Object.entries(DS().blocks).filter(([k])=>/t_a_|esc9/.test(k)).sort((a,b)=>a[1].start-b[1].start).map(([k,v])=>k+'@'+fmt(v.start)+'+'+blockLen(k)).join(', ')"))
    print('fill form after the call-back ('+await pg.evaluate("fmt(stepEnd('t_a_12'))")+')', await pg.evaluate("place('t_a_13', stepEnd('t_a_12'))"), await pg.evaluate("[...document.querySelectorAll('.toast')].map(t=>t.textContent).slice(-1)[0]"))
    print('send + route', await pg.evaluate("[place('t_a_14', stepEnd('t_a_13')), place('t_a_15', stepEnd('t_a_14'))]"), '| gaps', await pg.evaluate("cycleGaps()"))
    # a batch after step 1 is also an interruption result
    pg2,errs2=await fresh(b)
    await pg2.evaluate("place('t_b_12',T('11:00'))"); await pg2.wait_for_timeout(800)
    if live: await pg2.evaluate("tueFire(intList('tue').find(i=>i.id==='ti_mkt'),'t_b_12')"); await pg2.wait_for_timeout(400)
    if await pg2.query_selector('#slide [data-act="tue-batch"]'): await pg2.click('#slide [data-act="tue-batch"]'); await pg2.wait_for_timeout(300)
    await pg2.evaluate("closeModal()")
    print('B blocks', await pg2.evaluate("Object.entries(DS().blocks).filter(([k])=>/t_b_|batch|buffet/.test(k)).map(([k,v])=>k+'@'+fmt(v.start)).join(', ')"), '| step 2 after it', await pg2.evaluate("place('t_b_13', stepEnd('t_b_12'))"), await pg2.evaluate("[fmt(stepEnd('t_b_12')), [...document.querySelectorAll('.toast')].map(t=>t.textContent).slice(-1)[0]]"))
    print(errs or errs2 or 'NO ERRORS'); await b.close()
asyncio.run(main())
