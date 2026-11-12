import os as _os
CHROME = {'executable_path': _os.environ['CHROMIUM']} if _os.environ.get('CHROMIUM') else {}
HERE = _os.path.dirname(_os.path.abspath(__file__))
PAGE = 'file://' + _os.path.join(_os.path.dirname(HERE), 'public', 'index.html')
import asyncio, sys
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**CHROME)
    pg=await b.new_page(viewport={'width':1440,'height':900}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto(sys.argv[1]); await pg.wait_for_timeout(300)
    await pg.evaluate("S.arrivalSec=0; closeModal(); restartTomorrow(); closeDay(); S.round=1; let t=DS(); t.briefSeen=true; t.cqDone=true; t.revealDone=true; t.blocks.m_l_commute1={start:T('8:00'),extra:0}; ui.app='tools'; ui.tool='eisen'; renderAll(); closeModal()")
    # sort everything; delete stats + both forms; the AI cards then wait in the matrix
    await pg.evaluate("tasks().filter(schedulable).filter(t=>needsSort(t)).forEach(t=>setQuad(t.id, /m_stats|m_[ab]_13$|m_groceries/.test(t.id)?'q4':'q1')); syncSpawns(); renderAll(); closeModal()"); await pg.wait_for_timeout(400); await pg.evaluate("closeModal()")
    print('still to sort', await pg.evaluate("tasks().filter(schedulable).filter(t=>needsSort(t)).map(t=>t.title)"), '| tool', await pg.evaluate("ui.tool"))
    await pg.evaluate("tasks().filter(schedulable).filter(t=>needsSort(t)).forEach(t=>setQuad(t.id,'q1')); renderAll(); closeModal()"); await pg.wait_for_timeout(400); await pg.evaluate("closeModal()")
    print('after sorting AI cards → tool', await pg.evaluate("ui.tool"), '| placeable', await pg.evaluate("place('m_x_statsai',T('10:00'))"), await pg.evaluate("[...document.querySelectorAll('.toast')].map(t=>t.textContent).slice(-1)[0]"))
    # saved state from before this fix: an AI card without the flag
    await pg.evaluate("const x=DS().extra.find(e=>/_13ai$/.test(e.id)); delete x.sortAgain; save()"); await pg.reload(); await pg.wait_for_timeout(1200)
    print('migrated', await pg.evaluate("DS().extra.filter(e=>/_13ai$|statsai$/.test(e.id)).map(e=>e.id+':'+e.sortAgain)"))
    # Tuesday with Monday's AI choice: locked until sorted, then tag & mode
    await pg.evaluate("closeModal(); restartTomorrow(); closeDay(); S.round=2; const t=DS(); t.briefSeen=true; t.cqDone=true; t.revealDone=true; ui.app='calendar'; renderAll(); closeModal()")
    print('TUE', await pg.evaluate("tasks().filter(t=>/AI/.test(t.title)).map(t=>t.title.slice(0,40)+' sort:'+needsSort(t)+' tag:'+needsTagMode(t))"))
    print(errs or 'NO ERRORS'); await b.close()
asyncio.run(main())
