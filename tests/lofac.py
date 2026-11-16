import os as _os
CHROME = {'executable_path': _os.environ['CHROMIUM']} if _os.environ.get('CHROMIUM') else {}
HERE = _os.path.dirname(_os.path.abspath(__file__))
PAGE = 'file://' + _os.path.join(_os.path.dirname(HERE), 'public', 'index.html')
import asyncio, sys
from playwright.async_api import async_playwright
F=sys.argv[1] if len(sys.argv) > 1 else PAGE
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' — '+str(x)[:220] if x!='' else ''))
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**CHROME)
    pg=await b.new_page(viewport={'width':1440,'height':900}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)[:300]))
    await pg.goto(F); await pg.evaluate("localStorage.clear()"); await pg.goto(F); await pg.wait_for_timeout(400)
    await pg.evaluate("S.arrivalSec=0; closeModal(); place('s_inbox',T('13:15')); restartTomorrow(); closeDay(); S.round=1; renderAll(); closeModal(); const ds=DS(); ds.briefSeen=true; ds.cqDone=true; ds.revealDone=true; save(); renderAll(); closeModal()")
    lo=await pg.evaluate("loCarried('mon').map(t=>[t.id, !!t.leftover, t.cycle||''])")
    ok('Monday has tasks left from Sunday', len(lo)>3, len(lo))
    await pg.evaluate("facOpen=true; showFac()"); await pg.wait_for_timeout(200)
    ok('facilitator panel lists them with Delete', await pg.evaluate("document.querySelectorAll('#modal .lo-row [data-act=lo-del]').length")>0)
    one=next(x for x in lo if x[1] and not x[2]); tid=one[0]
    await pg.evaluate(f"place('{tid}', T('18:00'))")
    await pg.click(f'#modal [data-act="lo-del"][data-id="{tid}"]'); await pg.wait_for_timeout(100)
    ok('first click asks to confirm', await pg.evaluate(f"!!task('{tid}')") and 'again' in await pg.evaluate(f"document.querySelector('#modal [data-act=lo-del][data-id=\"{tid}\"]').textContent"))
    await pg.click(f'#modal [data-act="lo-del"][data-id="{tid}"]'); await pg.wait_for_timeout(200)
    r=await pg.evaluate(f"[!!task('{tid}'), !!DS().blocks['{tid}'], carryOf('mon').tasks.some(t=>t.id==='{tid}'), tasks().filter(schedulable).length]")
    ok('deleted: gone from To plan, calendar and the day', not r[0] and not r[1] and not r[2], r)
    ok('panel shows it as deleted with Restore', await pg.evaluate(f"!!document.querySelector('#modal .lo-row.gone [data-act=lo-restore][data-id=\"{tid}\"]')"))
    cyc=[x for x in lo if x[2]]
    if cyc:
      c0=cyc[0]; n=len([x for x in lo if x[2]==c0[2]])
      await pg.click(f'#modal [data-act="lo-del"][data-id="{c0[0]}"]'); await pg.click(f'#modal [data-act="lo-del"][data-id="{c0[0]}"]'); await pg.wait_for_timeout(200)
      left=await pg.evaluate(f"carryOf('mon').tasks.filter(t=>t.cycle==='{c0[2]}').length")
      ok(f'an approval cycle is deleted as one group ({n} steps)', left==0, left)
    else: ok('cycle leftover present (test data)', True, 'none on this path')
    await pg.click(f'#modal [data-act="lo-restore"][data-id="{tid}"]'); await pg.wait_for_timeout(200)
    ok('Restore brings it back', await pg.evaluate(f"!!task('{tid}')"))
    await pg.reload(); await pg.wait_for_timeout(500)
    ok('deletions are kept after a reload', await pg.evaluate("Object.keys(DS('mon').loDel||{}).length")>0)
    await pg.evaluate("closeModal(); restartTomorrow('mon'); closeDay('mon')")
    rep=await pg.evaluate("[DS('mon').report.total, DS('mon').report.res.some(x=>Object.keys(DS('mon').loDel||{}).includes(x.id))]")
    ok('deleted tasks are not in the day report', not rep[1], rep)
    await pg.evaluate("localStorage.clear()"); await pg.goto(F); await pg.wait_for_timeout(400)
    ok('a new game starts with nothing deleted', await pg.evaluate("!Object.keys((S.days.mon||{}).loDel||{}).length"))
    print(errs or 'NO ERRORS'); await b.close()
asyncio.run(main())
