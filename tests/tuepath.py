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
    pg=await b.new_page(viewport={'width':1440,'height':900}); errs=[]
    pg.on('pageerror',lambda e: errs.append((e.stack or str(e))[:400])); pg.on('dialog', lambda d: asyncio.ensure_future(d.accept()))
    vis="$('#modal').style.display==='flex'"
    async def drain():
      for i in range(30):
        await pg.wait_for_timeout(350)
        if await pg.evaluate(vis+" && !!document.querySelector('#modal [data-act=alarm-do]')"): await pg.click('#modal [data-act="alarm-do"]'); continue
        if await pg.evaluate(vis+" && !!document.querySelector('#modal .dk .btn')"): await pg.click('#modal .dk .btn'); continue
        if await pg.evaluate("!!document.querySelector('[data-act=cq-empty]') && $('#veil') && $('#veil').style.display==='block'"): await pg.click('[data-act="cq-empty"]'); continue
        if await pg.evaluate(vis+" && !!document.querySelector('#modal [data-act=cq-next]')"): await pg.click('#modal [data-act="cq-next"]'); continue
        if await pg.evaluate(vis): await pg.evaluate("closeModal()")
        if await pg.evaluate("DS().cqDone"): break
    await pg.goto(F); await pg.wait_for_timeout(400)
    await pg.click('#modal [data-act="open-laptop"]'); await pg.wait_for_timeout(500)
    await pg.evaluate("S.arrivalSec=0; DS().revealDone=true; renderAll()")
    await pg.click('[data-act="close-day"] >> nth=0'); await pg.wait_for_timeout(300); await pg.click('#modal [data-act="confirm-close"]'); await pg.wait_for_timeout(600)
    await pg.evaluate("S.carry.mon.tasks = S.carry.mon.tasks.filter(t=>!t.leftover); save()")  # (test only: an almost empty Sunday would otherwise exhaust Karim on Monday morning)
    await pg.click('#modal .rep-top [data-act="next-round"]'); await pg.wait_for_timeout(500); await pg.click('#modal [data-act="open-laptop"]')
    await drain(); await pg.evaluate("S.arrivalSec=0; DS().revealDone=true; renderAll(); closeModal()")
    # Monday: sort everything, deleting the statistics log and both forms; sort the AI cards too
    await pg.evaluate("ui.app='tools'; ui.tool='eisen'; renderAll()")
    for k in range(3):
      await pg.evaluate("tasks().filter(schedulable).filter(t=>needsSort(t)).forEach(t=>setQuad(t.id, /^m_stats$|^m_[ab]_13$/.test(t.id)?'q4':'q1')); syncSpawns(); renderAll()"); await pg.wait_for_timeout(500); await pg.evaluate("closeModal()")
    await pg.evaluate("ui.app='calendar'; renderAll(); place('m_l_shower',T('7:00')); place('m_l_breakfast',T('7:30')); place('m_l_commute1',T('8:00')); place('m_l_lunch',T('13:30'))")
    await pg.wait_for_timeout(800)
    if await pg.query_selector('#modal [data-act="trig-take"]'): await pg.click('#modal [data-act="trig-take"]'); await pg.wait_for_timeout(400)
    if await pg.query_selector('#modal [data-act="lv-end"]'): await pg.click('#modal [data-act="lv-end"]'); await pg.wait_for_timeout(300)
    await pg.evaluate("closeModal(); place('m_x_carpapers',T('17:00'))")
    print('MON', await pg.evaluate("[JSON.stringify(DS().ints.mi_car), DS().quad.m_stats, DS().quad.m_a_13, !!DS().blocks.m_x_carpapers]"))
    await pg.evaluate("ui.app='calendar'; renderAll(); closeModal()")
    btn=await pg.query_selector('#top [data-act="close-day"]')
    if btn: await btn.click(); await pg.wait_for_timeout(300); await pg.click('#modal [data-act="confirm-close"]'); await pg.wait_for_timeout(600)
    else: print('MON already closed?', await pg.evaluate("DS().closed"))
    print('carry flags', await pg.evaluate("JSON.stringify(S.carry.tue.flags)"))
    await pg.click('#modal .rep-top [data-act="next-round"]'); await pg.wait_for_timeout(500); await pg.click('#modal [data-act="open-laptop"]')
    await drain(); await pg.evaluate("closeModal()")
    print('TUE', await pg.evaluate("tasks().filter(t=>/t_stats|t_[ab]_13|commute/.test(t.id)).map(t=>t.id+' | '+t.title+' | '+dur(t)+' | sort:'+needsSort(t))"))
    # facilitator reset on Tuesday
    await pg.evaluate("closeModal(); facOpen=true; showFac()"); await pg.wait_for_timeout(200)
    await pg.click('[data-act="reset-day"]'); await pg.wait_for_timeout(300)
    print('first click', await pg.evaluate("document.querySelector('[data-act=reset-day]')?.textContent"), '| tuesday still there', await pg.evaluate("DS().cqDone"))
    await pg.click('[data-act="reset-day"]'); await pg.wait_for_timeout(800)
    print('after reset', await pg.evaluate("[D(), !!document.querySelector('#modal [data-act=open-laptop]'), DS().cqDone, Object.keys(DS().blocks).length]"))
    # re-closing Sunday restarts Monday AND Tuesday
    await pg.evaluate("closeModal(); S.round=0; DS().closed=false; renderAll(); closeModal(); restartTomorrow(); closeDay()")
    print('after re-closing Sunday', await pg.evaluate("[Object.keys(S.days.mon.blocks||{}).length, !!S.days.mon.briefSeen, Object.keys(S.days.tue.blocks||{}).length, !!S.days.tue.briefSeen]"))
    print(errs or 'NO ERRORS'); await b.close()
asyncio.run(main())
