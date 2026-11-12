import os as _os
CHROME = {'executable_path': _os.environ['CHROMIUM']} if _os.environ.get('CHROMIUM') else {}
HERE = _os.path.dirname(_os.path.abspath(__file__))
PAGE = 'file://' + _os.path.join(_os.path.dirname(HERE), 'public', 'index.html')
import asyncio, sys
from playwright.async_api import async_playwright
F=sys.argv[1] if len(sys.argv) > 1 else PAGE
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' — '+str(x)[:200] if x!='' else ''))
SETUP=open(_os.path.join(HERE, 'v11_manual.py')).read().split('SETUP="""')[1].split('"""')[0]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**CHROME)
    pg=await b.new_page(viewport={'width':1440,'height':900}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)[:300]))
    async def fresh():
      await pg.goto(F); await pg.wait_for_timeout(300); await pg.evaluate("localStorage.clear()"); await pg.goto(F); await pg.wait_for_timeout(400)
    async def tue():
      await fresh(); await pg.evaluate(SETUP % ''); await pg.evaluate("closeModal()")
    await fresh()
    bn=await pg.evaluate("budgetNumbers('sun')"); ok('sleep 7 h in the equation', bn['bud']==24*60-420-bn['groom']-bn['eat'], bn)
    await pg.evaluate("ui.app='tools'; ui.tool='budget'; renderAll()"); await pg.wait_for_timeout(150)
    ok('time budget tool says sleep 7 h', '7 h' in await pg.evaluate("(document.querySelector('.tb-calc')||document.body).innerText"))
    await pg.evaluate("S.round=3; renderAll(); closeModal()")
    ok('slides 1 h 15 min, parts 20+20+10+25', await pg.evaluate("[BASE_TASKS.wed.find(t=>t.id==='w_slides').dur, wSlidesParts().map(p=>p[2]).join('+')]")==[75,'20+20+10+25'])
    await tue()
    r=await pg.evaluate("[task('t_vip').dur, task('t_delivery').dur, task('t_vip').negNote, task('t_delivery').negNote]")
    ok('VIP 2 h, Tarek 3 h', r[0]==120 and r[1]==180, r[:2])
    ok('VIP note: part today, 2 hours, Mariam hint (no answer)', 'part of it today' in r[2] and '2 hours' in r[2] and 'Mariam' in r[2] and 'about an hour' not in r[2])
    ok('Tarek note: 3 hours', '3 hours' in r[3])
    # IT handle now = 5
    await pg.evaluate("place('t_l_commute1',T('8:00')); place('t_crm',T('9:00'))"); await pg.wait_for_timeout(700); await pg.evaluate("closeModal()")
    await pg.evaluate("place('t_huddle',T('9:15'))"); await pg.wait_for_timeout(700)
    if await pg.evaluate("!!document.querySelector('#slide [data-act=tue-now]')"):
      await pg.click('#slide [data-act="tue-now"]'); await pg.wait_for_timeout(400)
      if await pg.evaluate("!!document.querySelector('#modal [data-act=tue-now]')"): await pg.click('#modal [data-act="tue-now"]'); await pg.wait_for_timeout(300)
    c=await pg.evaluate("JSON.stringify((DS().tueCost||{}).ti_it||null)"); ok('IT email handled now costs 5 min', '"mins":5' in c, c)
    # lunch buffet offered on Tuesday + cycle: one block
    await tue()
    await pg.evaluate("place('t_l_commute1',T('8:00')); place('t_l_lunch',T('12:00'))"); await pg.wait_for_timeout(600); await pg.evaluate("closeModal()")
    for id,tm in [('t_crm','9:00'),('t_huddle','9:15')]:
      await pg.evaluate(f"place('{id}',T('{tm}'))"); await pg.wait_for_timeout(700)
      if await pg.evaluate("!!document.querySelector('#bat-after')"):
        o=await pg.evaluate("[...document.querySelectorAll('#bat-after option')].map(o=>o.value)"); ok('Tuesday picker offers the lunch buffet', 't_buffet_lunch' in o, o)
        await pg.click('#slide [data-act="tue-del"]'); await pg.wait_for_timeout(300); await pg.evaluate("closeModal()")
      else: await pg.evaluate("closeModal()")
    await pg.evaluate("DS().mode.t_a_13='reduced'; DS().mode.t_a_14='reduced'; DS().mode.t_a_12='free'; DS().tag.t_a_12='deep'")
    for id,tm in [('t_a_12','14:00'),('t_a_13','14:20'),('t_a_14','14:40'),('t_a_15','14:50')]:
      await pg.evaluate(f"place('{id}',T('{tm}'))"); await pg.wait_for_timeout(700)
      for k in range(3):
        if await pg.evaluate("!!document.querySelector('#slide [data-act=tue-batch]')"):
          await pg.click('#slide [data-act="tue-batch"]'); await pg.wait_for_timeout(300); await pg.evaluate("closeModal()")
        elif await pg.evaluate("$('#modal').style.display==='flex'"): await pg.evaluate("closeModal()")
    bl=await pg.evaluate("Object.keys(DS().blocks).filter(k=>/^t_(batch|buffet)_/.test(k) && k!=='t_buffet_lunch')")
    ok('after an approval cycle: at most one batch/held block', len(bl)<=1, bl)
    # Mom: dialogue + plan
    await tue()
    await pg.evaluate("place('t_l_lunch',T('12:30'))"); await pg.wait_for_timeout(800)
    for k in range(4):
      if await pg.evaluate("!!document.querySelector('#modal .cp-b.yes')"): await pg.click('#modal .cp-b.yes'); await pg.wait_for_timeout(300); break
      await pg.evaluate("closeModal()"); await pg.wait_for_timeout(300)
    ok('Mom: the call dialogue shows', await pg.evaluate("document.querySelectorAll('#modal .call-script p').length")>=4)
    if await pg.query_selector('#modal .call-script'): await pg.click('#modal [data-act="tue-now"]'); await pg.wait_for_timeout(500)
    m=await pg.evaluate("$('#modal').innerText"); ok('Mom: the clinic plan card (10 / 15 / 30 / 15)', 'THE PLAN' in m.upper() and 'Pharmacy' in m and '30 min' in m, m[:150])
    ok('clinic visit body mentions the pharmacy', 'Pharmacy' in await pg.evaluate("task('t_x_clinic').body"))
    # split keeps first part today
    await fresh(); await pg.evaluate("S.round=1; renderAll(); closeModal(); const ds=DS(); ds.briefSeen=true; S.arrivalSec=0; ds.revealDone=true; ds.cqDone=true; pendingArrivals().forEach(t=>{ds.got[arrKey(t)]=true}); ds.negFirst='x'; save(); renderAll(); closeModal()")
    await pg.evaluate("DS().quad.m_hala3m='q1'; ui.negFor='m_hala3m'; ui.nopts=['split']; ui.app='tools'; ui.tool='negotiate'; renderAll(); closeModal()"); await pg.wait_for_timeout(200)
    if not await pg.evaluate("!!document.querySelector('#neg-day')"): await pg.click('[data-nopt="split"]'); await pg.wait_for_timeout(150)
    await pg.select_option('#neg-day','2'); await pg.fill('#batna','x'); await pg.click('[data-act="neg-score"]'); await pg.wait_for_timeout(400)
    r=await pg.evaluate("[!!task('m_hala3m_part1') && task('m_hala3m_part1').dur, ((S.moved||{}).tue||[]).map(x=>x.title+':'+x.dur)]")
    ok('split: first part stays today, the rest moves', r[0]==15 and any('(the rest):15' in x for x in r[1]), r)
    # Wednesday tag renamed; Tuesday unchanged
    r=await pg.evaluate("[JSON.stringify(INTERRUPTIONS.wed.find(i=>i.id==='wi_fbtag')), INTERRUPTIONS.tue.find(i=>i.id==='ti_fb').from]")
    ok('Wednesday tag from Sherif Nabil (Tuesday unchanged)', 'Sherif Nabil' in r[0] and 'Mostafa' not in r[0] and r[1]=='Mostafa Adel')
    # thought text
    ok('thought: "= 35 min"', await pg.evaluate("String(document.documentElement.innerHTML).length>0") and '= 35 min added' in open(F.replace('file://','')).read())
    # good news: no red card for the email
    await fresh()
    r=await pg.evaluate("""(()=>{S.round=3; const c={cards:[{kind:'good',title:'Maadi warranty cards',text:'Done — all 12 cards were activated yesterday.'}],tasks:[],wa:[],mails:[{id:'w_c_maadidone',app:'mail',info:true,good:true,from:'Warranty desk',subject:'Maadi',received:'Today, 9:00 AM',body:'<p>x</p>'}],late:0}; S.carry.wed=c; renderAll(); closeModal(); const ds=DS(); ds.briefSeen=true; ds.cqDone=false; ds.cqShown={}; return 1})()""")
    seen=[]
    for k in range(6):
      await pg.evaluate("closeModal(); cqNext()"); await pg.wait_for_timeout(200)
      t=await pg.evaluate("$('#modal').style.display==='flex' ? $('#modal').innerText.slice(0,60) : ''")
      if not t or 'TODAY' in t: break
      seen.append(t.replace('\n',' '))
    ok('delegation confirmation: no red card (rc28: no card at all)', not any('CONSEQUENCE' in x for x in seen) and not any('Warranty' in x for x in seen), seen)
    ok('the email still lands in the inbox', await pg.evaluate("!!DS().got && Object.keys(DS().got).some(k=>/maadidone/.test(k))"))
    # report headline
    await fresh(); await pg.evaluate("S.arrivalSec=0; closeModal(); place('s_inbox',T('13:15')); place('s_book',T('9:00')); closeDay(); showReport && showReport()"); await pg.wait_for_timeout(300)
    h=await pg.evaluate("[DS('sun').report.done, (DS('sun').report.res||[]).filter(x=>x.how==='late').length]")
    await pg.evaluate("ui.app='calendar'; renderAll()")
    html=await pg.evaluate("document.body.innerHTML")
    ok('report: late-planned tasks counted and named', (h[1]==0) or ('planned with a problem' in html), h)
    print(errs or 'NO ERRORS'); await b.close()
asyncio.run(main())
