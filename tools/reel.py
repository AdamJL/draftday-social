# Animated Reel template (1080x1920, 30 fps). Run from tools/: python3 reel.py NAME [--stills]
# Edit S: each scene is (theme, logo, html, seconds). Elements with class "a" animate in,
# staggered by their "--d" delay (seconds). Key content stays inside the Reels safe zone.
import asyncio, subprocess, sys, os
src = open('build.py').read(); exec(src[:src.index('P={')])  # shared css, logos, dashes
FPS, VW, VH = 30, 1080, 1920
reel_css = """
body{height:1920px;padding:300px 84px}
.dash{margin-top:220px}
.mid{top:46%}
.foot{bottom:540px}
.a{opacity:0;transform:translateY(40px);animation:in .5s cubic-bezier(.2,.8,.2,1) forwards;animation-delay:var(--d,0s)}
@keyframes in{to{opacity:1;transform:none}}
.big{text-align:center}.big .logo{height:120px;margin:0 auto 60px}
"""
S = {
'reel1_howitworks': [
  ('ink', R, '<h1 class="a">Think you’re fast?</h1><p class="sub a" style="--d:.6s"><em style="font-style:normal;color:#4F82EE;font-weight:700">Put a number on it.</em></p>', 3.0),
  ('blue', W, '<div class="tag a" style="color:#fff">STEP 1</div><h1 class="a" style="--d:.2s">Run the drills on your own.</h1>', 2.8),
  ('white', C, '<div class="tag a">STEP 2</div><h1 class="a" style="--d:.2s">Log your score.</h1><div class="field a" style="--d:.7s"><span>Drill score</span><div class="pill" style="color:#4F82EE">Self-reported</div></div>', 3.0),
  ('ink', R, '<div class="tag a">STEP 3</div><h1 class="a" style="--d:.2s">See how you compare.</h1><div class="rows"><div class="a" style="--d:.7s">Against your age group</div><div class="a" style="--d:1.0s">Against other ages</div><div class="a" style="--d:1.3s">Across other sports</div></div>', 3.6),
  ('blue', W, '<div class="big"><img class="logo a" src="'+W+'"><h1 class="a" style="--d:.3s;font-size:110px">draftday.pro</h1><p class="sub a" style="--d:.7s">Track your progress over time.</p></div>', 2.8),
],
}
def page(t, l, m, final):
    foot = '' if final else f'<div class="foot"><div>Self-reported scores.</div><div class="url">draftday.pro</div></div>'
    logo = '' if final else f'<img class="logo" src="{l}">'
    return f'<!doctype html><html><head><style>{css}{reel_css}</style></head><body class="{t}">{dashes}{logo}<div class="mid">{m}</div>{foot}</body></html>'

async def main(name, stills):
    from playwright.async_api import async_playwright
    os.makedirs('out', exist_ok=True)
    scenes = S[name]; parts = []
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await br.new_page(viewport={'width': VW, 'height': VH})
        for i, (t, l, m, dur) in enumerate(scenes):
            await pg.set_content(page(t, l, m, i == len(scenes) - 1))
            await pg.evaluate('document.fonts.ready')
            await pg.evaluate('document.getAnimations().forEach(a=>a.pause())')
            seek = lambda ms: pg.evaluate(f'document.getAnimations().forEach(a=>a.currentTime={ms})')
            if stills:
                await seek(dur * 1000); await pg.screenshot(path=f'out/{name}_s{i}.png'); continue
            tmp, fin = f'out/{name}_{i}.tmp.mp4', f'out/{name}_{i}.mp4'
            ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                                   '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', str(FPS), tmp], stdin=subprocess.PIPE)
            for f in range(round(dur * FPS)):
                await seek(f * 1000 / FPS)
                ff.stdin.write(await pg.screenshot(type='jpeg', quality=92))
            ff.stdin.close()
            assert ff.wait() == 0; os.replace(tmp, fin); parts.append(fin)
            if i == 0:
                await seek(dur * 1000); await pg.screenshot(path=f'out/{name}_cover.jpg', type='jpeg', quality=92)
        await br.close()
    if stills: return
    with open('out/list.txt', 'w') as fh: fh.writelines(f"file '{os.path.basename(x)}'\n" for x in parts)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'out/list.txt', '-c', 'copy', f'out/{name}_v.mp4'], check=True)
    # silent AAC track for platform compatibility
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'out/{name}_v.mp4', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo',
                    '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-shortest', '-movflags', '+faststart', f'out/{name}.mp4'], check=True)

asyncio.run(main(sys.argv[1], '--stills' in sys.argv))
