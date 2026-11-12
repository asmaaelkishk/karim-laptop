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
    V="$('#modal').style.display==='flex'"
    async def drain():
      log=[]
      for i in range(70):
        await pg.wait_for_timeout(350)
        if await pg.evaluate(V+" && !!document.querySelector('#modal [data-act=alarm-do]')"): log.append('alarm'); await pg.click('#modal [data-act="alarm-do"]'); continue
        if await pg.evaluate(V+" && !!document.querySelector('#modal .dk .btn')"): log.append('desk'); await pg.click('#modal .dk .btn'); continue
        if await pg.evaluate("!!document.querySelector('[data-act=cq-empty]') && $('#veil') && $('#veil').style.display==='block'"): log.append('inbox'); await pg.click('[data-act="cq-empty"]'); continue
        if await pg.evaluate(V+" && !!document.querySelector('#modal [data-act=cq-next]')"): log.append(await pg.evaluate("document.querySelector('#modal .rc-h span, #modal .gc-h span').textContent")+': '+await pg.evaluate("(document.querySelector('#modal .rc-b p, #modal .gc-b p')||{}).textContent.slice(0,70)")+' | '+await pg.evaluate("(document.querySelector('#modal .rc-n')||{}).textContent?.slice(0,60)||''")); await pg.click('#modal [data-act="cq-next"]', force=True); continue
        if await pg.evaluate(V): await pg.evaluate("closeModal()")
        if await pg.evaluate("DS().cqDone"): break
      return log
    await pg.goto(F); await pg.wait_for_timeout(400)
    await pg.click('#modal [data-act="open-laptop"]'); await pg.wait_for_timeout(600)
    await pg.evaluate("S.arrivalSec=0; DS().revealDone=true; ui.app='calendar'; renderAll(); place('s_l_commute1',T('8:00')); place('s_crm',T('9:00'))")
    await pg.click('#top [data-act="close-day"]'); await pg.wait_for_timeout(300); await pg.click('#modal [data-act="confirm-close"]'); await pg.wait_for_timeout(600)
    print('carried to Monday', await pg.evaluate("S.carry.mon.tasks.filter(t=>t.leftover).map(t=>t.title)"))
    await pg.click('#modal .rep-top [data-act="next-round"]'); await pg.wait_for_timeout(500); await pg.click('#modal [data-act="open-laptop"]')
    for x in await drain(): print('  ', x)
    await pg.wait_for_timeout(300)
    print('leftover note', await pg.evaluate("(document.querySelector('.lo-note')||{}).innerText?.slice(0,120)"))
    print('energy', await pg.evaluate("[energyNow ? energyNow() : null]") if False else '', await pg.evaluate("[...document.querySelectorAll('.toast')].map(t=>t.textContent).slice(-4)"))
    print('on calendar', await pg.evaluate("tasks().filter(t=>t.leftover).map(t=>t.title.slice(0,35)+' @'+(DS().blocks[t.id]?fmt(DS().blocks[t.id].start):'tray')+' sort:'+needsSort(t)+' locked:'+cqLocked(t.id))"))
    # Monday AI versions are not locked
    await pg.evaluate("closeModal(); setQuad('m_stats','q4'); setQuad('m_a_13','q4'); syncSpawns(); renderAll(); closeModal()"); await pg.wait_for_timeout(400); await pg.evaluate("closeModal()")
    print('stats task?', await pg.evaluate("[!!task('m_stats'), DS().quad.m_stats, !!task('m_x_statsai'), JSON.stringify(spawnList(task('m_stats')).map(x=>x.id))]"))
    print('MON AI', await pg.evaluate("tasks().filter(t=>/AI/.test(t.title)).map(t=>t.title.slice(0,40)+' sort:'+needsSort(t))"))
    # a leftover can be moved
    lid=await pg.evaluate("(tasks().find(t=>t.leftover && DS().blocks[t.id])||{}).id")
    print('move leftover', lid, await pg.evaluate(f"place('{lid}', T('16:00'))"), await pg.evaluate("[...document.querySelectorAll('.toast')].map(t=>t.textContent).slice(-1)[0]"))
    # Monday → Tuesday leftovers
    await pg.evaluate("closeModal(); restartTomorrow(); closeDay()")
    print('carried to Tuesday', await pg.evaluate("S.carry.tue.tasks.filter(t=>t.leftover).map(t=>t.title).slice(0,12)"))
    print(errs or 'NO ERRORS'); await b.close()
asyncio.run(main())
