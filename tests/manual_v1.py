import os as _os
CHROME = {'executable_path': _os.environ['CHROMIUM']} if _os.environ.get('CHROMIUM') else {}
HERE = _os.path.dirname(_os.path.abspath(__file__))
PAGE = 'file://' + _os.path.join(_os.path.dirname(HERE), 'public', 'index.html')
import asyncio, sys
from playwright.async_api import async_playwright
F=PAGE
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**CHROME)
    ctx=await b.new_context(viewport={'width':1440,'height':900}); pg=await ctx.new_page(); errs=[]
    pg.on('pageerror',lambda e: errs.append((e.stack or str(e))[:300])); pg.on('dialog', lambda d: asyncio.ensure_future(d.accept()))
    vis="$('#modal').style.display==='flex'"
    await pg.goto(F); await pg.wait_for_timeout(600)
    print('KEY', await pg.evaluate("KEY"), '| brief', await pg.evaluate("!!document.querySelector('#modal [data-act=open-laptop]')"))
    await pg.click('#modal [data-act="open-laptop"]'); await pg.wait_for_timeout(4500)
    print('SUN emails', await pg.evaluate("mailItems().filter(m=>!m.draft).length"))
    await pg.evaluate("S.arrivalSec=0; DS().revealDone=true; renderAll()")
    for app in ['outlook','calendar','whatsapp','facebook','phone','crm','team','tools']:
      await pg.click(f'[data-app="{app}"]'); await pg.wait_for_timeout(100)
    print('SUN rules', await pg.evaluate("[place('s_l_shower',T('6:30')), place('s_book',T('10:30')), place('s_esc4',T('9:00'))]"))
    await pg.evaluate("closeModal(); restartTomorrow(); closeDay(); showReport()"); await pg.wait_for_timeout(300)
    await pg.click('#modal .rep-top [data-act="next-round"]'); await pg.wait_for_timeout(500); await pg.click('#modal [data-act="open-laptop"]')
    log=[]
    for i in range(30):
      await pg.wait_for_timeout(450)
      if await pg.evaluate(vis+" && !!document.querySelector('#modal [data-act=alarm-do]')"): log.append('alarm'); await pg.click('#modal [data-act="alarm-do"]'); continue
      if await pg.evaluate(vis+" && !!document.querySelector('#modal .dk .btn')"): log.append('desk'); await pg.click('#modal .dk .btn'); continue
      if await pg.evaluate("!!document.querySelector('[data-act=cq-empty]') && $('#veil') && $('#veil').style.display==='block'"): log.append('inbox'); await pg.click('[data-act="cq-empty"]'); continue
      if await pg.evaluate(vis+" && !!document.querySelector('#modal [data-act=cq-next]')"): log.append('cq'); await pg.click('#modal [data-act="cq-next"]'); continue
      if await pg.evaluate(vis): await pg.evaluate("closeModal()")
      if await pg.evaluate("DS().cqDone"): break
    print('MON morning', log)
    await pg.evaluate("closeModal(); restartTomorrow(); closeDay(); S.round=2; DS().briefSeen=true; DS().cqDone=true; S.arrivalSec=0; DS().revealDone=true; renderAll(); closeModal()")
    await pg.evaluate("closeModal(); restartTomorrow(); closeDay(); S.round=2; DS().briefSeen=true; DS().cqDone=true; renderAll(); closeModal()")
    print('TUE manual: live bar absent', await pg.evaluate("!document.querySelector('#livebar [data-act=live-start]')"))
    print('\n'.join(errs) if errs else 'NO ERRORS'); await b.close()
asyncio.run(main())
