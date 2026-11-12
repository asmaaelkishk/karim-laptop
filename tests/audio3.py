import os as _os
CHROME = {'executable_path': _os.environ['CHROMIUM']} if _os.environ.get('CHROMIUM') else {}
HERE = _os.path.dirname(_os.path.abspath(__file__))
PAGE = 'file://' + _os.path.join(_os.path.dirname(HERE), 'public', 'index.html')
import asyncio, sys
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**CHROME, args=['--autoplay-policy=no-user-gesture-required'])
    pg=await b.new_page(viewport={'width':1440,'height':900}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto(sys.argv[1]); await pg.wait_for_timeout(300)
    await pg.evaluate("S.arrivalSec=0; closeModal(); place('s_inbox',T('13:15')); restartTomorrow(); closeDay(); S.carry.mon.tasks=S.carry.mon.tasks.filter(t=>!t.leftover); S.round=1; const t=DS(); t.briefSeen=true; t.cqDone=true; t.revealDone=true; t.growSeen={m_study:true}; ui.app='calendar'; renderAll(); closeModal(); place('m_l_commute1',T('8:00')); place('m_l_commute2',T('17:00'))")
    await pg.evaluate("place('m_l_lunch',T('13:30'))"); await pg.wait_for_timeout(900); await pg.click('#modal [data-act="trig-take"]'); await pg.wait_for_timeout(600)
    print('car call: playing on Answer', await pg.evaluate("!!curAudio && !curAudio.paused"), '| play button shown', await pg.evaluate("!!document.querySelector('#modal [data-act=lv-play]')"))
    await pg.click('#modal [data-act="lv-end"]'); await pg.wait_for_timeout(500); await pg.evaluate("closeModal()")
    await pg.evaluate("place('m_ccxp',T('19:00'))"); await pg.wait_for_timeout(900); await pg.click('#modal [data-act="ahmed-open"]'); await pg.wait_for_timeout(400); await pg.click('[data-act="vn-play"][data-audio="ahmed"]'); await pg.wait_for_timeout(600)
    print('Ahmed voice note: playing', await pg.evaluate("!!curAudio && !curAudio.paused"), '| play button shown', await pg.evaluate("document.querySelector('[data-act=vn-play][data-audio=ahmed]') ? '▶ in the chat' : None"))
    print(errs or 'NO ERRORS'); await b.close()
asyncio.run(main())
