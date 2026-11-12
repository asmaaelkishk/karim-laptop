import os as _os
CHROME = {'executable_path': _os.environ['CHROMIUM']} if _os.environ.get('CHROMIUM') else {}
HERE = _os.path.dirname(_os.path.abspath(__file__))
PAGE = 'file://' + _os.path.join(_os.path.dirname(HERE), 'public', 'index.html')
import asyncio
from playwright.async_api import async_playwright
F=PAGE
SETUP="""(()=>{S.arrivalSec=0; closeModal(); place('s_inbox',T('13:15')); restartTomorrow(); closeDay(); S.round=1; let t=DS(); t.briefSeen=true; t.cqDone=true; t.revealDone=true;
  %s
  closeDay(); S.round=2; t=DS(); t.briefSeen=true; t.cqDone=true; t.revealDone=true;
  tasks().filter(schedulable).forEach(x=>{ if(needsSort(x)) t.quad[x.id]='q1'; if(needsTagMode(x)) { t.tag[x.id]='collab'; t.mode[x.id]='reduced'; } });
  ['t_esc78','t_a_12','t_prepmeet','t_b_12','t_study'].forEach(id=>{ t.tag[id]='deep'; t.mode[id]='free'; });
  ui.app='calendar'; renderAll(); closeModal(); })()"""
async def fresh(b, mon=''):
    pg=await b.new_page(viewport={'width':1440,'height':900}); errs=[]; pg.on('pageerror',lambda e: errs.append((e.stack or str(e))[:300])); pg.on('dialog', lambda d: asyncio.ensure_future(d.accept()))
    await pg.goto(F); await pg.wait_for_timeout(300); await pg.evaluate(SETUP % mon); await pg.wait_for_timeout(200); await pg.evaluate("closeModal()")
    return pg, errs
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(**CHROME)
    pg,errs=await fresh(b)
    print('energy (no PlayStation night)', await pg.evaluate("[energyCfg('tue').max, (carryOf('tue').cards||[]).map(c=>c.text).filter(t=>/PlayStation/.test(t))]"))
    await pg.evaluate("ui.app='tools'; ui.tool='focus'; renderAll()"); await pg.wait_for_timeout(150)
    print('focus tool: buffet choices left', await pg.evaluate("document.querySelectorAll('[data-buffet],[data-bufdur]').length"), '|', await pg.evaluate("(document.querySelector('.buffet-pick')||{}).textContent"))
    await pg.evaluate("ui.app='calendar'; renderAll()")
    L="[...document.querySelectorAll('.toast')].map(t=>t.textContent).slice(-1)[0]"
    print('8:00 work without car', await pg.evaluate("[place('t_l_commute1',T('7:00')), place('t_crm',T('8:00'))]"), '|', await pg.evaluate(L))
    async def plc(id,tm, choose=None):
      await pg.evaluate(f"place('{id}', T('{tm}'))"); await pg.wait_for_timeout(650)
      out=[]
      for k in range(4):
        if await pg.evaluate("!!document.querySelector('#slide [data-act=tue-del]')"):
          out.append('slide['+await pg.evaluate("[...document.querySelectorAll('#slide .n-act button')].map(b=>b.textContent).join('/')")+']')
          await pg.click('#slide [data-act="tue-del"]' if choose=='del' else '#slide [data-act="tue-batch"]'); await pg.wait_for_timeout(250); continue
        if await pg.evaluate("$('#modal').style.display==='flex'"):
          if await pg.evaluate("!!document.querySelector('#modal [data-act=desk-later]')"):
            out.append('mariam['+await pg.evaluate("[...document.querySelectorAll('#modal .actions button')].map(b=>b.textContent.slice(0,22)).join(' | ')")+']')
            await pg.click(f'#modal [data-act="{choose or "desk-later"}"]')
            if choose=='desk-note': await pg.fill('#rtr-t','stopped at RT-1203 next approve'); await pg.click('#modal [data-act="desk-note"]')
            await pg.wait_for_timeout(250); out.append('card:'+await pg.evaluate("(document.querySelector('#modal .gc-b p,#modal .rc-b p')||{}).textContent?.slice(0,60)")); await pg.evaluate("closeModal()"); continue
          if await pg.evaluate("!!document.querySelector('#modal .cp-b.yes')"):
            out.append('call'); await pg.click('#modal .cp-b.yes'); await pg.wait_for_timeout(250)
            out.append('script:'+str(await pg.evaluate("document.querySelectorAll('#modal .call-script p').length"))); 
            if await pg.query_selector('#modal .call-script'): await pg.click('#modal [data-act="tue-now"]'); await pg.wait_for_timeout(250)
            await pg.evaluate("closeModal()"); continue
          if await pg.evaluate("!!document.querySelector('#modal [data-act=th-back]')"): await pg.click('#modal [data-act="th-back"]'); await pg.fill('#th-note','ask yassin later'); await pg.click('#modal [data-act="th-back"]'); out.append('thought'); continue
          if await pg.evaluate("!!document.querySelector('#modal [data-act=tue-now]')"): await pg.click('#modal [data-act="tue-now"]'); out.append('pop'); continue
          await pg.evaluate("closeModal()")
      print(id, tm, out)
    await pg.evaluate("place('t_l_commute1',T('8:00'))")
    for id,tm in [('t_crm','9:00'),('t_huddle','9:15'),('t_halaoffers','9:30'),('t_esc78','11:30'),('t_l_lunch','12:30'),('t_a_12','15:00'),('t_b_12','16:30')]:
      await plc(id,tm)
    print('buffets', await pg.evaluate("Object.keys(DS().blocks).filter(k=>/t_buffet/.test(k)).map(k=>k+'@'+fmt(DS().blocks[k].start)+' ['+((DS().batches||{})[k]||[]).join(',')+']')"), '| callback', await pg.evaluate("DS().blocks.t_x_esc9_call ? fmt(DS().blocks.t_x_esc9_call.start) : null"))
    await pg.evaluate("closeDay(); showReport()"); await pg.wait_for_timeout(300)
    print('report', await pg.evaluate("[...document.querySelectorAll('.gains .g-msg')].map(p=>p.textContent.slice(0,70))"))
    print('errors A', errs or 'none'); await pg.close()
    # Mariam other choices
    for ch in ['desk-now','desk-note']:
      pg,errs=await fresh(b)
      await pg.evaluate("place('t_l_commute1',T('8:00'))"); await plc('t_a_12','11:00', ch); print('errors', ch, errs or 'none'); await pg.close()
    # Delete in reduced mode
    pg,errs=await fresh(b); await pg.evaluate("place('t_l_commute1',T('8:00'))"); await plc('t_huddle','9:15','del'); print('deleted logged', await pg.evaluate("JSON.stringify(DS().tueCost)")); await pg.close()
    # with the car: early arrival on Tuesday only
    pg,errs=await fresh(b)
    await pg.evaluate("S.days.mon.blocks.m_x_carpapers={start:T('17:00'),extra:0}; S.carry.tue.flags=Object.assign(S.carry.tue.flags||{}, {hasCar:true}); save()")
    print('car owner Tuesday 7:30 work', await pg.evaluate("[earlyOK('tue'), earlyOK('mon'), place('t_l_commute1',T('7:00')), place('t_crm',T('7:30'))]"), await pg.evaluate("[...document.querySelectorAll('.toast')].map(t=>t.textContent).slice(-1)[0]"))
    print('errors car', errs or 'none'); await pg.close()
    # negotiation: one extra try only
    pg,errs=await fresh(b)
    r=await pg.evaluate("""(()=>{ const ds=DS(); ui.app='tools'; ui.tool='negotiate'; const id='t_delivery'; ds.neg[id]={status:'declined',chat:[],met:{},tries:6,batna:'x',opts:['shift']};
      const a=document.createElement('button'); a.dataset.act='neg-again'; a.dataset.id=id; document.body.appendChild(a); a.click(); const first=!ds.neg[id];
      ds.neg[id]={status:'declined',chat:[],met:{},tries:6,batna:'x',opts:['shift']}; a.click(); const second=!ds.neg[id]; return [first, second]; })()""")
    print('try again: first allowed, second blocked', r); print('errors neg', errs or 'none')
    await b.close()
asyncio.run(main())
