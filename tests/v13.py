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
    print('approvals', await pg.evaluate("[fmt(task('t_a_12').avail), task('t_a_12').received, fmt(task('t_b_12').avail), task('t_b_12').received]"))
    if live:
      await b.close(); return
    # held item for the lunch buffet (deep + distraction-free before lunch)
    await pg.evaluate("DS().mode.t_esc78='free'; place('t_esc78',T('11:30'))"); await pg.wait_for_timeout(800); await pg.evaluate("closeModal()")
    print('held', await pg.evaluate("JSON.stringify(DS().batches)"))
    await pg.evaluate("place('t_l_lunch',T('12:30'))"); await pg.wait_for_timeout(900)
    order=[]
    for k in range(12):
      if await pg.evaluate("$('#modal').style.display==='flex' && !!document.querySelector('#modal .bv')"): order.append('buffet:'+await pg.evaluate("document.querySelector('#modal .bv .tp-h').textContent.slice(0,30)")); await pg.click('#modal [data-act="bv-done"], #modal [data-act="bv-next"]'); await pg.wait_for_timeout(300); continue
      if await pg.evaluate("$('#modal').style.display==='flex' && !!document.querySelector('#modal .cp-b.yes')"): order.append('Mom call'); await pg.click('#modal .cp-b.yes'); await pg.wait_for_timeout(500)
      if await pg.query_selector('#modal .call-script'): await pg.click('#modal [data-act="tue-now"]'); await pg.wait_for_timeout(900)  # rc24: Mom's dialogue, then hang up
      continue
      if await pg.evaluate("$('#modal').style.display==='flex'"): order.append('card'); await pg.evaluate("closeModal()")
      await pg.wait_for_timeout(500)
    print('lunch order', order)
    print('clinic call', await pg.evaluate("[DS().blocks.t_x_clinic_call?fmt(DS().blocks.t_x_clinic_call.start):null, fmt(DS().blocks.t_l_lunch.start)+'+'+blockLen('t_l_lunch'), DS().blocks.t_buffet_lunch?fmt(DS().blocks.t_buffet_lunch.start)+'+'+blockLen('t_buffet_lunch'):null, DS().blocks.t_x_clinic?fmt(DS().blocks.t_x_clinic.start):null]"))
    print('move clinic call', await pg.evaluate("place('t_x_clinic_call',T('15:00'))"), '|', await pg.evaluate("[...document.querySelectorAll('.toast')].map(t=>t.textContent).slice(-1)[0]"))
    print(errs or 'NO ERRORS'); await b.close()
asyncio.run(main())
