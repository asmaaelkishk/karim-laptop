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
    pg,errs=await fresh(b)
    tests=[["I have a lot of tasks today and pulling 3 months of complaints takes time, can I send it Thursday? I understand your vendor meeting is on Monday."],
           ["I'm swamped today with escalations. Thursday works? I know you need it for your meeting with the vendor."],
           ["can I send it on Thursday?","I'm busy today","today my schedule is completely full with the team meeting and approvals so I really cannot do it properly"],
           ["Can we move it to Thursday please, I appreciate your patience","sorry I just can't today, there is so much going on and I want to do it well for you before your vendor meeting"]]
    for msgs in tests:
      r=await pg.evaluate("""(msgs)=>{ const ds=DS(); delete ds.neg.t_delivery; ds.neg.t_delivery={status:'open',chat:[],met:{},tries:0,batna:'x',opts:['shift'],pickDay:4}; let n; for (const m of msgs) { n=negotiateMsg(task('t_delivery'),m); if (n.status!=='open') break; } closeModal(); return [n.status, n.chat.filter(c=>c.who==='them').map(c=>c.text.slice(0,70))]; }""", msgs)
      print(r)
    print(errs or 'NO ERRORS'); await b.close()
asyncio.run(main())
