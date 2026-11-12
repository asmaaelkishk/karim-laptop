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
    await pg.evaluate("DS().mode.t_esc78='free'; place('t_esc78',T('11:30'))"); await pg.wait_for_timeout(800)
    if live: await pg.evaluate("tueFire(intList('tue').find(i=>i.id==='ti_fb'),'t_esc78')"); await pg.wait_for_timeout(300)
    await pg.evaluate("closeModal(); renderAll()")
    print('before lunch: buffet on calendar?', await pg.evaluate("[!!DS().blocks.t_buffet_lunch, !!document.querySelector('.blk[data-id=t_buffet_lunch]'), !!task('t_buffet_lunch'), JSON.stringify(DS().batches)]"), '| toast', await pg.evaluate("[...document.querySelectorAll('.toast')].map(t=>t.textContent).filter(t=>/held/.test(t)).slice(-1)[0]"))
    await pg.evaluate("place('t_l_lunch',T('12:30')); renderAll()"); await pg.wait_for_timeout(1200)
    print('after lunch placed', await pg.evaluate("[DS().blocks.t_buffet_lunch?fmt(DS().blocks.t_buffet_lunch.start)+'+'+blockLen('t_buffet_lunch'):null, !!document.querySelector('#modal .bv')]"))
    await pg.evaluate("closeModal()")
    # moving lunch moves the buffet with it
    await pg.evaluate("place('t_l_lunch',T('12:45')); renderAll()"); await pg.wait_for_timeout(500)
    print('lunch moved → buffet', await pg.evaluate("[fmt(DS().blocks.t_l_lunch.start), DS().blocks.t_buffet_lunch?fmt(DS().blocks.t_buffet_lunch.start):null]"))
    print(errs or 'NO ERRORS'); await b.close()
asyncio.run(main())
