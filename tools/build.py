import asyncio, base64
from playwright.async_api import async_playwright
b=lambda f:'data:image/png;base64,'+base64.b64encode(open(f,'rb').read()).decode()
C,R,W=b('assets/logo_color.png'),b('assets/logo_rev.png'),b('assets/logo_white.png')
css="""*{margin:0;box-sizing:border-box}
body{width:1080px;height:1350px;font-family:Poppins;position:relative;overflow:hidden;padding:84px}
.ink{background:#0E1420;color:#fff}.white{background:#fff;color:#111}.blue{background:#4F82EE;color:#fff}
.logo{height:64px;display:block}
h1{font-weight:700;font-size:124px;line-height:1.04;letter-spacing:-3.5px}
h1 em{font-style:normal;color:#4F82EE}.blue h1 em{color:#0E1420}
.mid{position:absolute;left:84px;right:84px;top:50%;transform:translateY(-50%)}
.foot{position:absolute;left:84px;right:84px;bottom:80px;display:flex;justify-content:space-between;align-items:flex-end;font-size:34px;font-weight:500;line-height:1.3}
.url{font-weight:700}
.sub{font-size:48px;font-weight:500;line-height:1.28;margin-top:44px}
.tag{display:inline-block;font-size:30px;font-weight:700;letter-spacing:4px;margin-bottom:36px;color:#4F82EE}
.dash{position:absolute;right:0;height:14px;border-radius:7px 0 0 7px;background:#4F82EE}
.blue .dash{background:#fff}
.field{margin-top:64px;border:4px solid #C9D0DC;border-radius:24px;padding:44px 48px;display:flex;justify-content:space-between;align-items:center;font-size:46px;font-weight:600}
.ink .field{border-color:#4F82EE;background:#17233A}
.cursor{width:6px;height:60px;background:#111}
.ok{display:flex;align-items:center;gap:16px;color:#8FB2FF}
.dot{width:58px;height:58px;border-radius:50%;background:#4F82EE;display:flex;align-items:center;justify-content:center}
.pill{font-size:32px;font-weight:600;color:#8FB2FF;border:3px solid #4F82EE;border-radius:40px;padding:10px 26px}
.ink .sub{color:#fff}
.rows{margin-top:52px}.rows div{font-size:46px;font-weight:600;padding:26px 0;border-top:3px solid rgba(255,255,255,.55)}\n.pg{font-size:30px;font-weight:600;opacity:.65}"""
dashes='<div class="dash" style="top:100px;width:190px"></div><div class="dash" style="top:150px;width:110px"></div><div class="dash" style="top:200px;width:60px"></div>'
check='<div class="dot"><svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 13l5 5L20 6"/></svg></div>'
P={
'post1_launch':('ink',R,'<h1>Everybody’s fast in the group chat.<br><em>See how you compare.</em></h1>','Run the drills. Log your numbers.'),
'post2_slide1':('blue',W,'<h1>Don’t wait for a combine.</h1><p class="sub">Start building your numbers now.</p>','1 / 5 &nbsp; Swipe →'),
'post2_slide2':('white',C,'<div class="tag">STEP 1</div><h1>Run the drills on your own.</h1><p class="sub">Your field. Your schedule.</p>','2 / 5'),
'post2_slide3':('ink',R,'<div class="tag">STEP 2</div><h1>Log your scores.</h1><div class="field"><span>Drill score</span><div class="pill">Self-reported</div></div><p class="sub">Then track your progress over time.</p>','3 / 5'),
'post2_slide4':('blue',W,'<div class="tag" style="color:#fff">STEP 3</div><h1>See how you compare.</h1><div class="rows"><div>Against your age group</div><div>Against other ages</div><div>Across other sports</div></div>','4 / 5'),
'post2_slide5':('white',C,'<h1>Find out where you stand.</h1><p class="sub">Run the drills. Log your numbers. See how you compare.</p>','5 / 5'),
'post3_parents':('white',C,'<div class="tag">FOR PARENTS</div><h1>Your athlete put in the work.</h1><p class="sub">See how they stack up against their age group and beyond.</p>','Self-reported combine stats,<br>across ages and sports.'),
}
async def main():
  async with async_playwright() as p:
    br=await p.chromium.launch(); pg=await br.new_page(viewport={'width':1080,'height':1350})
    for n,(t,l,m,f) in P.items():
      await pg.set_content(f'<!doctype html><html><head><style>{css}</style></head><body class="{t}">{dashes}<img class="logo" src="{l}"><div class="mid">{m}</div><div class="foot"><div>{f}</div><div class="url">draftday.pro</div></div></body></html>')
      await pg.evaluate('document.fonts.ready'); await pg.screenshot(path=f'out/{n}.png')
    await br.close()
asyncio.run(main())
