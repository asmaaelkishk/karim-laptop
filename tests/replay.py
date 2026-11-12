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
    V="$('#modal').style.display==='flex'"
    await pg.goto(F); await pg.wait_for_timeout(400)
    await pg.click('#modal [data-act="open-laptop"]'); await pg.wait_for_timeout(2500)
    await pg.evaluate("ui.app='calendar'; renderAll(); place('s_l_commute1',T('8:00')); place('s_crm',T('9:00'))")
    before=await pg.evaluate("[Object.keys(DS().blocks).length, mailItems().filter(m=>!m.draft).length]")
    await pg.evaluate("facOpen=true; showFac()"); await pg.click('[data-act="replay-plan"]'); await pg.wait_for_timeout(200); await pg.click('[data-act="replay-plan"]'); await pg.wait_for_timeout(500)
    print('SUN before', before, '→ after', await pg.evaluate("[Object.keys(DS().blocks), mailItems().filter(m=>!m.draft).length, DS().briefSeen, $('#modal').style.display]"))
    await pg.wait_for_timeout(3000); print('SUN emails arriving again', await pg.evaluate("mailItems().filter(m=>!m.draft).length"))
    # Monday through the real morning, then plan, then replay
    await pg.evaluate("S.arrivalSec=0; DS().revealDone=true; closeModal(); restartTomorrow(); closeDay(); S.carry.mon.tasks=S.carry.mon.tasks.filter(t=>!t.leftover); S.round=1; renderAll(); showBrief()"); await pg.wait_for_timeout(300)
    await pg.click('#modal [data-act="open-laptop"]')
    for i in range(40):
      await pg.wait_for_timeout(350)
      if await pg.evaluate(V+" && !!document.querySelector('#modal [data-act=alarm-do]')"): await pg.click('#modal [data-act="alarm-do"]'); continue
      if await pg.evaluate(V+" && !!document.querySelector('#modal .dk .btn')"): await pg.click('#modal .dk .btn'); continue
      if await pg.evaluate("!!document.querySelector('[data-act=cq-empty]') && $('#veil') && $('#veil').style.display==='block'"): await pg.click('[data-act="cq-empty"]'); continue
      if await pg.evaluate(V+" && !!document.querySelector('#modal [data-act=cq-next]')"): await pg.click('#modal [data-act="cq-next"]', force=True); continue
      if await pg.evaluate(V): await pg.evaluate("closeModal()")
      if await pg.evaluate("DS().cqDone"): break
    morning=await pg.evaluate("Object.keys(DS().blocks).sort()")
    await pg.evaluate("closeModal(); DS().growSeen={m_study:true}; DS().quad.m_crm='q1'; setQuad('m_groceries','q4'); syncSpawns(); place('m_l_commute1',T('8:00')); renderAll(); closeModal()"); await pg.wait_for_timeout(400); await pg.evaluate("closeModal()")
    await pg.evaluate("facOpen=true; showFac()"); await pg.click('[data-act="replay-plan"]'); await pg.wait_for_timeout(200); await pg.click('[data-act="replay-plan"]'); await pg.wait_for_timeout(500)
    print('MON morning blocks restored', await pg.evaluate("JSON.stringify(Object.keys(DS().blocks).sort())") == __import__('json').dumps(morning, separators=(',',':')), '| quad cleared', await pg.evaluate("JSON.stringify(DS().quad)"), '| cqDone', await pg.evaluate("DS().cqDone"), '| no brief', await pg.evaluate("$('#modal').style.display"))
    print(errs or 'NO ERRORS'); await b.close()
asyncio.run(main())
