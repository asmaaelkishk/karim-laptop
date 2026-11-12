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
    # 1. Mom's call at lunch adds nothing
    await pg.evaluate("place('t_l_lunch',T('12:30'))"); await pg.wait_for_timeout(800)
    if live: await pg.evaluate("tueFire(intList('tue').find(i=>i.id==='ti_mom'),'t_l_lunch')"); await pg.wait_for_timeout(400)
    await pg.click('#modal .cp-b.yes'); await pg.wait_for_timeout(400)
    if await pg.query_selector('#modal .call-script'): await pg.click('#modal [data-act="tue-now"]')  # rc24: hang up after Mom's dialogue
    await pg.wait_for_timeout(500)
    print('1 lunch length after Mom', await pg.evaluate("blockLen('t_l_lunch')"), '|', await pg.evaluate("(document.querySelector('#modal .gc-n')||{}).textContent"))
    await pg.evaluate("closeModal()")
    # 2. deleted notifications stay in their apps
    for tid,on,tm in [('ti_talabat1','t_a_13','13:40'),('ti_it','t_huddle','9:15')]:
      await pg.evaluate(f"closeModal(); ui.tueCur=null; const s=$('#slide'); if(s) s.innerHTML=''; tueFire(intList('tue').find(i=>i.id==='{tid}'),'{on}')"); await pg.wait_for_timeout(300)
      if await pg.query_selector('#slide [data-act="tue-del"]'): await pg.click('#slide [data-act="tue-del"]'); await pg.wait_for_timeout(300)
      await pg.evaluate("closeModal()")
    print('2 phone notifications', await pg.evaluate("DS().notifs.map(n=>n.from+': '+String(n.text).slice(0,40))"), '| outlook', await pg.evaluate("DS().mails.filter(m=>/^tm_/.test(m.id)).map(m=>m.subject)"), '| logged', await pg.evaluate("JSON.stringify(Object.fromEntries(Object.entries(DS().tueCost).map(([k,v])=>[k,v.kind])))"))
    await pg.evaluate("ui.app='phone'; ui.phone='notifs'; renderAll()"); await pg.wait_for_timeout(200)
    print('2 phone tab shows', await pg.evaluate("document.querySelector('#win').innerText.includes('Talabat')"))
    print('errors A', errs or 'none'); await pg.close()
    # 3. voice notes
    pg=await b.new_page(viewport={'width':1440,'height':900}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    await pg.goto(F); await pg.wait_for_timeout(300)
    await pg.evaluate("S.arrivalSec=0; closeModal(); place('s_inbox',T('13:15')); restartTomorrow(); closeDay(); S.carry.mon.tasks=S.carry.mon.tasks.filter(t=>!t.leftover); S.round=1; const t=DS(); t.briefSeen=true; t.cqDone=true; t.revealDone=true; t.growSeen={m_study:true}; ui.app='calendar'; renderAll(); closeModal(); place('m_l_commute1',T('8:00')); place('m_l_commute2',T('17:00'))")
    await pg.evaluate("place('m_ccxp',T('19:00'))"); await pg.wait_for_timeout(900); await pg.click('#modal [data-act="ahmed-open"]'); await pg.wait_for_timeout(400)  # rc23: Ahmed's voice note plays in the chat
    print('3 voice screen play button', await pg.evaluate("ui.app==='whatsapp' && ui.chat==='ahmed' && !!document.querySelector('[data-act=vn-play][data-audio=ahmed]')"))
    await pg.click('[data-act="vn-play"][data-audio="ahmed"]'); await pg.wait_for_timeout(300); print('3 playing', await pg.evaluate("!!curAudio"))
    await pg.click('#ahmed-back [data-act="ahmed-back"]'); await pg.wait_for_timeout(400); await pg.evaluate("closeModal(); ui.app='whatsapp'; ui.chat='ahmed'; renderAll()"); await pg.wait_for_timeout(200)
    print('3 Ahmed voice bubble playable', await pg.evaluate("!!document.querySelector('[data-act=vn-play][data-audio=ahmed]')"))
    # 4. replay Monday from planning
    await pg.evaluate("closeModal(); ui.app='calendar'; DS().quad.m_crm='q1'; place('m_crm',T('9:30')); renderAll(); facOpen=true; showFac()"); await pg.wait_for_timeout(200)
    await pg.click('[data-act="replay-plan"]'); await pg.wait_for_timeout(200); await pg.click('[data-act="replay-plan"]'); await pg.wait_for_timeout(600)
    print('4 after replay', await pg.evaluate("[D(), DS().briefSeen, DS().cqDone, Object.keys(DS().blocks), JSON.stringify(DS().quad), Object.keys(DS().ints).length, $('#modal').style.display]"))
    print('errors B', errs or 'none'); await b.close()
asyncio.run(main())
