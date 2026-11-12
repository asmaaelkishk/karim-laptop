import os as _os
CHROME = {'executable_path': _os.environ['CHROMIUM']} if _os.environ.get('CHROMIUM') else {}
HERE = _os.path.dirname(_os.path.abspath(__file__))
PAGE = 'file://' + _os.path.join(_os.path.dirname(HERE), 'public', 'index.html')
import asyncio, sys
from playwright.async_api import async_playwright
F=sys.argv[1] if len(sys.argv) > 1 else PAGE
def ok(n,c,x=''): print(('PASS ' if c else 'FAIL ')+n+(' — '+str(x)[:220] if x!='' else ''))
TUE=open(_os.path.join(HERE, 'v11_manual.py')).read().split('SETUP="""')[1].split('"""')[0]
MON="S.round=1; renderAll(); closeModal(); const ds=DS(); ds.briefSeen=true; S.arrivalSec=0; ds.revealDone=true; ds.cqDone=true; pendingArrivals().forEach(t=>{ds.got[arrKey(t)]=true}); save(); renderAll(); closeModal()"
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**CHROME)
    pg=await b.new_page(viewport={'width':1440,'height':900}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)[:300]))
    toast="[...document.querySelectorAll('.toast')].map(x=>x.textContent).slice(-1)[0]||''"
    async def fresh():
      await pg.goto(F); await pg.wait_for_timeout(300); await pg.evaluate("localStorage.clear()"); await pg.goto(F); await pg.wait_for_timeout(400)
    # 1 coaching text
    await fresh(); await pg.evaluate(MON)
    await pg.click('.blk[data-id="m_coach"]'); await pg.wait_for_timeout(250)
    ok('coaching says it moves later when pushed', 'moves later by itself' in await pg.evaluate("document.body.innerText"))
    # 2 undo removes Youssef's interruption
    await pg.evaluate("DS().quad.m_b_12='q1'; undoMark(); place('m_b_12',T('13:30'))"); await pg.wait_for_timeout(900)
    t=await pg.query_selector('#modal [data-act="trig-take"]')
    if t: await t.click(); await pg.wait_for_timeout(500)
    had=await pg.evaluate("[!!DS().ints.mi_youssef, (DS().extra||[]).map(e=>e.id).filter(i=>/refocus|ytvideo/.test(i))]")
    ok('setup: Youssef watched -> refocus added', had[0] and 'm_x_refocus' in had[1], had)
    await pg.evaluate("closeModal(); undoLast(); undoLast(); undoLast()"); await pg.wait_for_timeout(300)
    r=await pg.evaluate("[!!DS().blocks.m_b_12, !!DS().ints.mi_youssef, (DS().extra||[]).map(e=>e.id).filter(i=>/refocus|ytvideo/.test(i))]")
    ok('undo the approval: Youssef\'s video and refocus are gone', not r[0] and not r[1] and r[2]==[], r)
    await pg.evaluate("place('m_b_12',T('13:30'))"); await pg.wait_for_timeout(900)
    ok('placing it again replays the same interruption', await pg.evaluate("!!document.querySelector('#modal [data-act=trig-take]')"))
    # refocus never carried as a leftover
    await pg.click('#modal [data-act="trig-take"]'); await pg.wait_for_timeout(500)
    await pg.evaluate("closeModal(); DS().blocks.m_x_refocus && (delete DS().blocks.m_x_refocus); restartTomorrow(); closeDay();")
    c=await pg.evaluate("carryOf('tue').tasks.map(t=>t.id)"); ok('refocus never comes back as a leftover', not any('refocus' in x or 'ytvideo' in x for x in c), [x for x in c if 'refocus' in x])
    # 3 VIP: Wednesday refused, Thursday accepted
    await fresh(); await pg.evaluate(TUE % ''); await pg.evaluate("closeModal()")
    await pg.evaluate("DS().quad.t_vip='q1'; ui.negFor='t_vip'; ui.nopts=['split']; ui.app='tools'; ui.tool='negotiate'; renderAll(); closeModal()"); await pg.wait_for_timeout(200)
    for k in ['split','resource']:
      el=await pg.query_selector(f'[data-nopt="{k}"]')
      if el and not await el.is_checked(): await el.click(); await pg.wait_for_timeout(100)
    note=await pg.evaluate("document.body.innerText"); ok('VIP note: supplier quotes take two working days', 'two working days' in note)
    await pg.select_option('#neg-day','3'); await pg.fill('#batna','x'); await pg.click('[data-act="neg-score"]'); await pg.wait_for_timeout(300)
    ok('VIP to Wednesday refused', await pg.evaluate("(DS().neg.t_vip||{}).status")!='accepted', await pg.evaluate(toast))
    await pg.select_option('#neg-day','4'); await pg.click('[data-act="neg-score"]'); await pg.wait_for_timeout(300)
    ok('VIP to Thursday agreed', await pg.evaluate("(DS().neg.t_vip||{}).status")=='accepted', await pg.evaluate(toast))
    # 4 planned late is not a leftover
    await fresh(); await pg.evaluate("S.arrivalSec=0; closeModal(); place('s_minutes',T('17:00')); restartTomorrow(); closeDay();")
    c=await pg.evaluate("[carryOf('mon').tasks.map(t=>t.id), (DS('sun').report.res||[]).find(x=>x.id==='s_minutes')]")
    ok('task planned late is not a leftover next day', 'mon_lo_s_minutes' not in c[0], c[1])
    await fresh(); await pg.evaluate("S.arrivalSec=0; closeModal(); place('s_inbox',T('13:15')); restartTomorrow(); closeDay();")
    ok('a task never planned still comes back', 'mon_lo_s_minutes' in await pg.evaluate("carryOf('mon').tasks.map(t=>t.id)"))
    # 5 patterns
    ok('patterns review: no Thursday', await pg.evaluate("CARRY.mon.map(r=>r.add).filter(Boolean).find(a=>a.id==='t_c_patterns').due")=='')
    # 6 delegation emails silent
    await fresh()
    await pg.evaluate("""(()=>{S.round=3; S.carry.wed={cards:[{kind:'good',title:'Maadi warranty cards',text:'x'}],tasks:[],wa:[],mails:[{id:'w_c_maadidone',app:'mail',info:true,from:'Warranty desk',subject:'Maadi',received:'Today, 9:00 AM',body:'<p>x</p>'}],late:0}; renderAll(); closeModal(); const ds=DS(); ds.briefSeen=true; ds.cqDone=false; ds.cqShown={}; return 1})()""")
    seen=[]
    for k in range(4):
      await pg.evaluate("closeModal(); cqNext()"); await pg.wait_for_timeout(200)
      t=await pg.evaluate("$('#modal').style.display==='flex' ? $('#modal').innerText.slice(0,50) : ''")
      if t: seen.append(t.replace('\n',' '))
    ok('delegation confirmation: no card at the start of the day', not any('Maadi' in x or 'Warranty' in x for x in seen), seen)
    ok('the email is in the inbox', await pg.evaluate("Object.keys(DS().got||{}).some(k=>/maadidone/.test(k))"))
    # 7 AI hint: one note pinned below all tasks in the Eisenhower tool (rc29)
    await fresh(); await pg.evaluate(MON); await pg.evaluate("ui.app='tools'; ui.tool='eisen'; renderAll()"); await pg.wait_for_timeout(200)
    r=await pg.evaluate("(()=>{const pl=document.querySelector('aside.eis-pile'); const h=pl&&pl.querySelector('.ai-hint-all'); const cards=[...pl.querySelectorAll('.ec')]; const hb=h.getBoundingClientRect(), pb=pl.getBoundingClientRect(); return [!!h, (cards[cards.length-1].compareDocumentPosition(h) & Node.DOCUMENT_POSITION_FOLLOWING)>0, hb.bottom<=pb.bottom+1 && hb.top>=pb.top, document.querySelectorAll('.ai-hint-all').length]})()")
    ok('Eisenhower: one hint below all tasks, visible without scrolling', r[0] and r[1] and r[2] and r[3]==1, r)
    await pg.evaluate("ui.app='calendar'; renderAll()"); await pg.wait_for_timeout(150)
    ok('not on the calendar', await pg.evaluate("!document.querySelector('.ai-hint-all') && !document.querySelector('.ai-hint')"))
    await pg.evaluate("S.round=2; renderAll(); closeModal(); ui.app='tools'; ui.tool='eisen'; renderAll()"); await pg.wait_for_timeout(150)
    ok('Monday only', await pg.evaluate("!document.querySelector('.ai-hint-all')"))
    # 8 sound: data first, blob fallback, text backup
    await fresh(); await pg.evaluate(MON)
    await pg.evaluate("place('m_l_lunch',T('13:30'))"); await pg.wait_for_timeout(800); await pg.click('#modal [data-act="trig-take"]'); await pg.wait_for_timeout(1500)
    ok('car call plays the embedded recording', await pg.evaluate("!!curAudio && curAudio.src.startsWith('data:') && curAudio.currentTime>0.5"))
    ok('call screen has "Show as text"', await pg.evaluate("!!document.querySelector('#modal [data-act=vn-text]')"))
    await pg.click('#modal [data-act="vn-text"]'); await pg.wait_for_timeout(150)
    ok('the call text shows', 'AutoDrive' in await pg.evaluate("(document.querySelector('#modal .vt-box')||{}).innerText||''"))
    await fresh(); await pg.evaluate(MON)
    await pg.evaluate("(()=>{const P=HTMLMediaElement.prototype.play; HTMLMediaElement.prototype.play=function(){ if(this.src.startsWith('data:')) return Promise.reject(Object.assign(new Error('blocked'),{name:'NotSupportedError'})); return P.call(this);}; return 1})()")
    await pg.evaluate("place('m_l_lunch',T('13:30'))"); await pg.wait_for_timeout(800); await pg.click('#modal [data-act="trig-take"]'); await pg.wait_for_timeout(1500)
    ok('if the embedded sound is blocked, it plays from memory', await pg.evaluate("!!curAudio && curAudio.src.startsWith('blob:') && curAudio.currentTime>0.5"))
    await fresh(); await pg.evaluate(MON)
    await pg.evaluate("(()=>{HTMLMediaElement.prototype.play=function(){return Promise.reject(Object.assign(new Error('x'),{name:'NotSupportedError'}))}; return 1})()")
    await pg.evaluate("place('m_l_lunch',T('13:30'))"); await pg.wait_for_timeout(800); await pg.click('#modal [data-act="trig-take"]'); await pg.wait_for_timeout(800)
    ok('if no sound at all: Play button and "Show as text" stay on screen', await pg.evaluate("!!document.querySelector('#modal [data-act=lv-play]') && !!document.querySelector('#modal [data-act=vn-text]')"), await pg.evaluate(toast))
    # Ahmed in WhatsApp
    await fresh(); await pg.evaluate(MON)
    await pg.evaluate("place('m_ccxp',T('19:00'))"); await pg.wait_for_timeout(800); await pg.click('#modal [data-act="ahmed-open"]'); await pg.wait_for_timeout(400)
    await pg.click('.vplay[data-audio="ahmed"]'); await pg.wait_for_timeout(1200)
    ok('Ahmed\'s voice note plays when clicked in the chat', await pg.evaluate("!!curAudio && curAudio.currentTime>0.5"))
    await pg.click('[data-act="vn-text"][data-audio="ahmed"]'); await pg.wait_for_timeout(150)
    ok('Ahmed\'s voice note can be read as text', 'الـCV' in await pg.evaluate("[...document.querySelectorAll('.vt-box')].map(x=>x.innerText).join(' ')"))
    print(errs or 'NO ERRORS'); await b.close()
asyncio.run(main())
