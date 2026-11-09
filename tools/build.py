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
'post4_lastscore':('ink',R,'<div class="tag">PROGRESS</div><h1>Beat your <em>last</em> score.</h1><p class="sub">Log your drills. Track your progress over time.</p>','Self-reported scores.'),
'post5_othersports':('blue',W,'<div class="tag" style="color:#fff">ANY SPORT</div><h1>How do you compare outside your sport?</h1><p class="sub">See your self-reported scores next to athletes in other sports.</p>','Your age group. Other ages.<br>Other sports.'),
'post6_slide1':('white',C,'<div class="tag">FOR PARENTS</div><h1>What “self-reported” means.</h1><p class="sub">A quick guide to DraftDay scores.</p>','1 / 4 &nbsp; Swipe →'),
'post6_slide2':('ink',R,'<div class="tag">ON THEIR OWN</div><h1>Your athlete runs the drills.</h1><p class="sub">Then logs the score themselves.</p>','2 / 4'),
'post6_slide3':('blue',W,'<div class="tag" style="color:#fff">THE NUMBER</div><h1>It’s their own report.</h1><div class="rows"><div>Logged by the athlete</div><div>Not verified</div><div>Labeled self-reported</div></div>','3 / 4'),
'post6_slide4':('white',C,'<h1>Use it to <em>track</em> and <em>compare.</em></h1><p class="sub">Progress over time, plus how they stack up by age group and sport.</p>','4 / 4'),
'story1_newweek':('ink',R,'<h1>New week.<br><em>New numbers.</em></h1><p class="sub">Run the drills. Log your scores.</p>','Self-reported scores.',1920),
'story2_compare':('blue',W,'<h1>Your age group. Other ages. Other sports.</h1><p class="sub">See how you compare.</p>','Self-reported scores.',1920),
'story3_parents':('white',C,'<div class="tag">FOR PARENTS</div><h1>Watch their progress add up.</h1><p class="sub">Track self-reported drill scores over time.</p>','Self-reported scores.',1920),
}
async def main():
  async with async_playwright() as p:
    br=await p.chromium.launch(); pg=await br.new_page(viewport={'width':1080,'height':1350})
    for n,v in P.items():
      t,l,m,f=v[:4]; h=v[4] if len(v)>4 else 1350
      await pg.set_viewport_size({'width':1080,'height':h})
      st='' if h==1350 else '<style>body{height:1920px;padding:260px 84px}.foot{bottom:300px}.dash{margin-top:180px}</style>'
      await pg.set_content(f'<!doctype html><html><head><style>{css}</style>{st}</head><body class="{t}">{dashes}<img class="logo" src="{l}"><div class="mid">{m}</div><div class="foot"><div>{f}</div><div class="url">draftday.pro</div></div></body></html>')
      await pg.evaluate('document.fonts.ready'); await pg.screenshot(path=f'out/{n}.png',full_page=False)
    await br.close()
asyncio.run(main())
