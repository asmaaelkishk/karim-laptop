import os as _os
CHROME = {'executable_path': _os.environ['CHROMIUM']} if _os.environ.get('CHROMIUM') else {}
HERE = _os.path.dirname(_os.path.abspath(__file__))
PAGE = 'file://' + _os.path.join(_os.path.dirname(HERE), 'public', 'index.html')
import asyncio, sys
from playwright.async_api import async_playwright
exec(open('v11_manual.py').read().split('async def main')[0].replace("F=PAGE","F=sys.argv[1] if len(sys.argv) > 1 else PAGE").replace("tasks().filter(schedulable).forEach(x=>{ if(needsSort(x)) t.quad[x.id]='q1';","tasks().filter(schedulable).filter(x=>!/t_webinar|t_maadi/.test(x.id)).forEach(x=>{ if(needsSort(x)) t.quad[x.id]='q1';"))
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**CHROME)
    pg,errs=await fresh(b)
    print('in To plan', await pg.evaluate("['t_webinar','t_maadi'].map(id=>[id, !!task(id), needsSort(task(id)), fmt(task(id).avail)])"))
    await pg.evaluate("ui.app='outlook'; ui.folder='inbox'; ui.mail='t_maadi'; renderAll()"); await pg.wait_for_timeout(150)
    print('maadi email', await pg.evaluate("document.querySelector('.ol-read')?.innerText.slice(0,260).replace(/\\n+/g,' | ')"))
    await pg.evaluate("ui.mail='t_webinar'; renderAll()"); await pg.wait_for_timeout(100)
    print('webinar has optional?', await pg.evaluate("/optional/i.test(document.querySelector('.ol-read').innerText)"))
    await pg.evaluate("setQuad('t_webinar','q4')"); await pg.wait_for_timeout(300)
    print('delete card', await pg.evaluate("[(document.querySelector('#modal .gc-n')||{}).textContent, (document.querySelector('#modal .gc-b p')||{}).textContent]")); await pg.evaluate("closeModal()")
    await pg.evaluate("setQuad('t_maadi','q3'); DS().deleg.t_maadi='mariam'; syncSpawns(); renderAll()")
    print('wrong person', await pg.evaluate("delegCheck(task('t_maadi'),'mariam')"))
    await pg.evaluate("DS().deleg.t_maadi='nadia'; syncSpawns(); renderAll(); closeModal()")
    print('spawned', await pg.evaluate("tasks().filter(t=>t.spawnOf==='t_maadi').map(t=>t.id+' | '+t.title+' | sort:'+needsSort(t)+' | tagmode:'+needsTagMode(t))"))
    await pg.evaluate("ui.app='calendar'; renderAll(); place('t_l_commute1',T('8:00'))")
    print('place email', await pg.evaluate("place('t_x_maadi_nadia',T('11:10'))"))
    await pg.evaluate("closeDay(); showReport()"); await pg.wait_for_timeout(300)
    print('report delegated/deleted', await pg.evaluate("[...document.querySelectorAll('#modal .rep-sec, #modal details')].map(e=>e.textContent).join(' ').match(/(Vendor webinar|Maadi)[^|]{0,40}/g)"))
    print(errs or 'NO ERRORS'); await b.close()
asyncio.run(main())
