#!/usr/bin/env python3
"""
make-walkthrough.py: record a polished 20-40 s walkthrough MP4 of a website from a JSON shot list.

Frames are rendered deterministically: every frame is a Playwright screenshot taken after the
script sets the scroll position, cursor and caption for that exact moment. Page loads happen
between frames and are hidden behind short crossfades, so there is no dead time, no flicker and
no cursor jank, whatever the speed of the machine. Frames are piped into ffmpeg (H.264, yuv420p,
+faststart), re-encoded until the file is under the size budget, and a poster JPG is saved.

Usage:
  pip install playwright pillow && playwright install chromium     # plus ffmpeg with libx264 on PATH
  BASE_URL=http://localhost:5001 python3 scripts/make-walkthrough.py <example>/walkthrough.json [--out DIR] [--base URL]
                                       [--fps 30] [--max-mb 14.5] [--keep-master]

Outputs <out>/<slug>-walkthrough.mp4 (1920x1080 H.264 High, yuv420p, faststart, no audio) and
<out>/<slug>-walkthrough-poster.jpg, then prints a JSON summary.

Secrets: never put passwords in the shot list. A scene with "signin": true signs in first with
SITE_USER_EMAIL / SITE_USER_PASSWORD (or the variable names given in the shot list's "login"
block). Use a public site user, never an admin. The shot-list format is documented in
scripts/make-walkthrough.md.
"""
import argparse, asyncio, base64, json, math, os, shutil, subprocess, sys, tempfile, time
from io import BytesIO
from PIL import Image, ImageDraw, ImageFilter
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
# Uses system Chrome when present (WALK_CHROME overrides), else Playwright's bundled Chromium.
CHROME = os.environ.get("WALK_CHROME", "/usr/bin/google-chrome")

def ease(t):  # easeInOutCubic
    t = max(0.0, min(1.0, t))
    return 4 * t * t * t if t < .5 else 1 - pow(-2 * t + 2, 3) / 2

async def grab(page):
    """Fast frame grab through CDP (about 6x quicker than page.screenshot)."""
    cdp = getattr(page, "_wt_cdp", None)
    if cdp is None:
        cdp = await page.context.new_cdp_session(page); page._wt_cdp = cdp
    r = await cdp.send("Page.captureScreenshot", {"format": "jpeg", "quality": 93, "optimizeForSpeed": True})
    return Image.open(BytesIO(base64.b64decode(r["data"]))).convert("RGB")

# ---------------------------------------------------------------- overlay (cursor + caption) JS
OVERLAY_JS = r"""
(() => {
  if (window.__wt) return;
  const st = document.createElement('style');
  st.textContent = `
  html{scroll-behavior:auto!important}
  ::-webkit-scrollbar{display:none} html{scrollbar-width:none}
  #__wt_cur{position:fixed;left:0;top:0;z-index:2147483647;pointer-events:none;width:26px;height:26px;opacity:0;
    filter:drop-shadow(0 2px 4px rgba(0,0,0,.45));will-change:transform}
  #__wt_ring{position:fixed;left:0;top:0;z-index:2147483646;pointer-events:none;width:44px;height:44px;margin:-22px 0 0 -22px;border-radius:50%;
    border:2px solid rgba(255,255,255,.95);box-shadow:0 0 0 3px rgba(100,110,203,.55);opacity:0}
  #__wt_cap{position:fixed;left:28px;bottom:28px;z-index:2147483645;pointer-events:none;opacity:0;display:flex;align-items:center;gap:10px;
    font:600 17px/1.2 "Geist","Inter",system-ui,-apple-system,"Segoe UI",sans-serif;letter-spacing:-.005em;color:#fff;
    background:rgba(12,13,32,.78);border:1px solid rgba(255,255,255,.16);padding:11px 18px 11px 14px;border-radius:999px;
    backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);box-shadow:0 12px 30px -10px rgba(0,0,0,.55)}
  #__wt_cap i{width:8px;height:8px;border-radius:50%;background:linear-gradient(135deg,#858dda,#9b7cf0);box-shadow:0 0 0 4px rgba(100,110,203,.3)}`;
  document.documentElement.appendChild(st);
  const cur = document.createElement('div'); cur.id = '__wt_cur';
  cur.innerHTML = '<svg viewBox="0 0 26 26" width="26" height="26"><path d="M5 3 L5 21 L9.6 16.8 L12.7 23.4 L15.6 22.1 L12.6 15.7 L19 15.7 Z" fill="#111" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  const ring = document.createElement('div'); ring.id = '__wt_ring';
  const cap = document.createElement('div'); cap.id = '__wt_cap'; cap.innerHTML = '<i></i><span></span>';
  document.documentElement.append(cur, ring, cap);
  window.__wt = (s) => {
    if (s.y !== undefined && s.y !== null) window.scrollTo(0, s.y);
    cur.style.opacity = s.co; cur.style.transform = `translate(${s.cx - 5}px,${s.cy - 3}px)`;
    ring.style.opacity = s.ro; ring.style.left = s.cx + 'px'; ring.style.top = s.cy + 'px';
    ring.style.transform = `scale(${s.rs})`;
    cap.style.opacity = s.ko; cap.style.transform = `translateY(${(1 - s.ko) * 8}px)`;
    if (s.kt !== undefined && cap.lastChild.textContent !== s.kt) cap.lastChild.textContent = s.kt;
  };
})();
"""

REVEAL_JS = r"""
() => {
  // Show scroll-reveal content up front so nothing pops in on camera.
  document.querySelectorAll('.reveal,[data-reveal],.fade-up,.fade-in,.animate-on-scroll,[data-aos]').forEach(e => {
    e.classList.add('in','is-in','is-visible','visible','revealed','aos-animate'); e.style.transitionDelay = '0s';
  });
  document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager');
}
"""

# ---------------------------------------------------------------- cards
def card_html(kind, cfg, W, H, caption=None):
    rx_mark = ('<svg viewBox="0 0 109.375 109.375" class="mark"><rect width="109.375" height="109.375" rx="20" fill="#646ecb"/>'
               '<g transform="matrix(1.6359 0 0 1.6359 18.832 -12.017)" fill="#fff"><path d="M10.2 48.18 l-8.34 0 l2.22 -8.34 l8.34 0 l2.76 0 '
               'l22.2 0 l0.72 -2.76 l-2.76 0 l-19.44 0 l-11.1 0 l2.28 -8.34 l11.1 0 l19.44 0 l11.04 0 l-5.22 19.44 l-8.28 0 l5.28 11.1 l-9.96 0 '
               'l-5.34 -11.1 l-7.5 0 l-7.44 0 z"/></g></svg>')
    esc = lambda s: (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if kind == "title":
        t = cfg.get("title", {})
        body = f"""<div class="wrap"><div class="kicker"><span class="dot"></span>{esc(t.get('kicker','A Raytha use case'))}</div>
          <h1>{esc(t.get('heading', cfg.get('name','')))}</h1><p>{esc(t.get('subheading',''))}</p></div>"""
    elif kind == "end":
        e = cfg.get("end", {})
        body = f"""<div class="wrap center">{rx_mark}<h1 class="sm">{esc(e.get('heading','Built with Raytha'))}</h1>
          <p>{esc(e.get('subheading','The open-source .NET CMS. Free and MIT licensed.'))}</p>
          <div class="url">{esc(e.get('url','raytha.com'))}</div></div>"""
    else:  # backdrop for phone scenes
        body = f"""<div class="wrap side"><div class="kicker"><span class="dot"></span>{esc((caption or {}).get('kicker','On a phone'))}</div>
          <h2>{esc((caption or {}).get('text',''))}</h2></div>"""
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@500&display=block" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#090a1c;color:#fff;font-family:Geist,Inter,system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
body{{position:relative;isolation:isolate}}
body:before{{content:"";position:absolute;inset:0;z-index:-2;background:
 radial-gradient(55% 70% at 18% 0%,rgb(100 110 203/.55),transparent 70%),
 radial-gradient(45% 60% at 100% 100%,rgb(155 124 240/.38),transparent 70%),
 radial-gradient(35% 45% at 0% 100%,rgb(70 200 232/.16),transparent 70%),linear-gradient(160deg,#151735,#090a1c 65%)}}
body:after{{content:"";position:absolute;inset:0;z-index:-1;background-image:linear-gradient(rgb(255 255 255/.05) 1px,transparent 1px),
 linear-gradient(90deg,rgb(255 255 255/.05) 1px,transparent 1px);background-size:56px 56px;
 -webkit-mask-image:radial-gradient(75% 75% at 50% 40%,#000 25%,transparent 85%)}}
.wrap{{position:absolute;left:{int(W*.085)}px;right:{int(W*.085)}px;top:50%;transform:translateY(-50%)}}
.wrap.center{{text-align:center;display:flex;flex-direction:column;align-items:center}}
.wrap.side{{right:auto;width:{int(W*.36)}px}}
.kicker{{display:inline-flex;align-items:center;gap:12px;font:500 15px/1 "Geist Mono",monospace;letter-spacing:.16em;text-transform:uppercase;color:#c3c7f2;
 padding:10px 16px;border:1px solid rgb(255 255 255/.16);border-radius:999px;background:rgb(255 255 255/.05)}}
.dot{{width:8px;height:8px;border-radius:50%;background:#9b7cf0;box-shadow:0 0 0 4px rgb(155 124 240/.25)}}
h1{{font-size:{int(W*.052)}px;line-height:1.02;letter-spacing:-.045em;font-weight:700;margin-top:28px;max-width:16ch;text-wrap:balance}}
h1.sm{{font-size:{int(W*.042)}px;margin-top:26px}}
h2{{font-size:{int(W*.03)}px;line-height:1.1;letter-spacing:-.035em;font-weight:700;margin-top:22px;text-wrap:balance}}
p{{font-size:{int(W*.0145)}px;line-height:1.5;color:#b9bce0;margin-top:22px;max-width:60ch}}
.mark{{width:{int(W*.05)}px;height:{int(W*.05)}px;border-radius:22%;box-shadow:0 20px 50px -12px rgb(100 110 203/.8)}}
.url{{margin-top:34px;font:500 {int(W*.0125)}px/1 "Geist Mono",monospace;color:#fff;padding:14px 22px;border-radius:999px;
 background:linear-gradient(90deg,rgb(100 110 203/.35),rgb(155 124 240/.3));border:1px solid rgb(255 255 255/.2)}}
</style></head><body>{body}</body></html>"""

# ---------------------------------------------------------------- recorder
class Recorder:
    def __init__(self, cfg, args):
        self.cfg, self.args = cfg, args
        self.vw, self.vh = cfg.get("viewport", [1440, 810])
        self.W, self.H = cfg.get("output", [1920, 1080])
        self.dsf = self.W / self.vw
        self.fps = args.fps
        self.base = (args.base or os.environ.get("BASE_URL") or cfg.get("base") or "http://localhost:5001").rstrip("/")
        self.frames = 0
        self.last = None
        self.poster = None
        self.cur = [self.vw * .62, self.vh * .7]  # cursor position (CSS px)
        self.cap = ""
        self.capop = 0.0

    # -- output
    def emit(self, img, mark_poster=False):
        if img.size != (self.W, self.H): img = img.resize((self.W, self.H), Image.LANCZOS)
        if img.mode != "RGB": img = img.convert("RGB")
        self.ff.stdin.write(img.tobytes()); self.frames += 1; self.last = img
        if mark_poster and self.poster is None: self.poster = img.copy()

    def fade_to(self, img, secs):
        a = self.last if self.last is not None else Image.new("RGB", (self.W, self.H), (9, 10, 28))
        if img.size != (self.W, self.H): img = img.resize((self.W, self.H), Image.LANCZOS)
        n = max(1, int(secs * self.fps))
        for i in range(1, n + 1):
            self.emit(Image.blend(a, img.convert("RGB"), ease(i / n)))

    async def snap(self, page):
        return await grab(page)

    # -- per-frame state
    async def state(self, page, y=None, co=0.0, ro=0.0, rs=1.0):
        await page.evaluate("s => window.__wt && window.__wt(s)", {
            "y": y, "co": co, "cx": self.cur[0], "cy": self.cur[1], "ro": ro, "rs": rs,
            "ko": self.capop, "kt": self.cap})

    async def frame(self, page, poster=False, **kw):
        await self.state(page, **kw)
        self.emit(await self.snap(page), poster)

    # -- page prep
    async def prep(self, page, url):
        await page.goto(url, wait_until="networkidle", timeout=60000)
        await page.evaluate("document.fonts.ready")
        await page.evaluate(REVEAL_JS)
        # pre-scroll to trigger lazy content, then back to top
        await page.evaluate("""async()=>{const h=document.documentElement.scrollHeight;for(let y=0;y<h;y+=500){scrollTo(0,y);await new Promise(r=>setTimeout(r,40))}scrollTo(0,0)}""")
        await page.evaluate(REVEAL_JS)
        if self.cfg.get("prepJs"): await page.evaluate(self.cfg["prepJs"])
        if self.cfg.get("css"): await page.add_style_tag(content=self.cfg["css"])
        await page.evaluate(OVERLAY_JS)
        try: await page.wait_for_load_state("networkidle", timeout=8000)
        except Exception: pass
        await page.wait_for_timeout(int(self.cfg.get("settleMs", 700)))

    async def scroll_y(self, page):
        return await page.evaluate("scrollY")

    async def resolve_y(self, page, to):
        if isinstance(to, (int, float)): y = to
        elif to == "bottom": y = await page.evaluate("document.documentElement.scrollHeight - innerHeight")
        elif isinstance(to, dict):
            y = await page.evaluate("([s,o])=>{const e=document.querySelector(s);if(!e)return null;return e.getBoundingClientRect().top+scrollY-o}",
                                    [to["selector"], to.get("offset", 90)])
            if y is None: raise SystemExit(f"scroll target not found: {to['selector']}")
        else:
            y = await page.evaluate("([s,o])=>{const e=document.querySelector(s);if(!e)return null;return e.getBoundingClientRect().top+scrollY-o}", [to, 90])
            if y is None: raise SystemExit(f"scroll target not found: {to}")
        maxy = await page.evaluate("document.documentElement.scrollHeight - innerHeight")
        return max(0, min(maxy, y))

    async def el_center(self, page, sel):
        loc = page.locator(sel).first
        try: bb = await loc.bounding_box(timeout=5000)
        except Exception: bb = None
        if not bb: raise SystemExit(f"element not found or hidden: {sel}")
        if bb["y"] < 0 or bb["y"] + bb["height"] > self.vh:
            raise SystemExit(f"element is off screen (scroll to it first so the move stays smooth): {sel}")
        return [bb["x"] + bb["width"] / 2, bb["y"] + bb["height"] / 2]

    # -- actions
    async def run_actions(self, page, actions, cursor_on):
        co = 1.0 if cursor_on else 0.0
        for a in actions:
            if "hold" in a:
                for i in range(int(a["hold"] * self.fps)):
                    await self.frame(page, poster=a.get("poster", False) and i == int(a["hold"] * self.fps) // 2, co=co)
            elif "caption" in a:
                txt = a["caption"]
                if txt and self.capop > 0 and txt != self.cap:  # fade out old first
                    for i in range(1, 7): self.capop = 1 - i / 6; await self.frame(page, co=co)
                if txt: self.cap = txt
                n = int(a.get("fade", .35) * self.fps); start = self.capop; target = 1.0 if txt else 0.0
                for i in range(1, n + 1):
                    self.capop = start + (target - start) * ease(i / n); await self.frame(page, co=co)
            elif "scroll" in a:
                y0 = await self.scroll_y(page); y1 = await self.resolve_y(page, a["scroll"])
                n = max(1, int(a.get("dur", 2.0) * self.fps))
                for i in range(1, n + 1):
                    await self.frame(page, y=y0 + (y1 - y0) * ease(i / n), co=co)
            elif "move" in a or "click" in a or "type" in a or "hover" in a:
                sel = a.get("click") or a.get("move") or a.get("hover") or (a.get("type") or {}).get("selector")
                target = await self.el_center(page, sel)
                start = list(self.cur)
                if co < 1:  # fade cursor in where it is
                    for i in range(1, 7): co = i / 6; await self.frame(page, co=co)
                n = max(1, int(a.get("dur", .9) * self.fps))
                for i in range(1, n + 1):
                    t = ease(i / n)
                    arc = math.sin(math.pi * i / n) * 18  # gentle arc, not a robotic straight line
                    self.cur = [start[0] + (target[0] - start[0]) * t, start[1] + (target[1] - start[1]) * t - arc]
                    await self.frame(page, co=co)
                if "hover" in a:
                    await page.mouse.move(*target); await page.wait_for_timeout(250)
                    for _ in range(int(a.get("hold", .6) * self.fps)): await self.frame(page, co=co)
                if "type" in a:
                    await page.mouse.click(*target)
                    text = a["type"]["text"]; per = max(1, int(a["type"].get("cps", 14)))
                    fpc = max(1, round(self.fps / per))
                    for ch in text:
                        await page.keyboard.type(ch)
                        for _ in range(fpc): await self.frame(page, co=co)
                    for _ in range(int(.35 * self.fps)): await self.frame(page, co=co)
                if "click" in a:
                    for i in range(1, 9):  # press ring
                        await self.frame(page, co=co, ro=math.sin(math.pi * i / 8) * .9, rs=.6 + .5 * i / 8)
                    nav = a.get("navigates", True)
                    if nav:
                        async with page.expect_navigation(wait_until="networkidle", timeout=60000):
                            await page.mouse.click(*target)
                        await self.after_nav(page, a.get("fade", .45), co)
                    else:
                        await page.mouse.click(*target); await page.wait_for_timeout(int(a.get("waitMs", 500)))
                if a.get("press"):
                    async with page.expect_navigation(wait_until="networkidle", timeout=60000):
                        await page.keyboard.press(a["press"])
                    await self.after_nav(page, a.get("fade", .45), co)
            elif "press" in a:
                async with page.expect_navigation(wait_until="networkidle", timeout=60000):
                    await page.keyboard.press(a["press"])
                await self.after_nav(page, a.get("fade", .45), co)
            elif "cursor" in a:
                on = bool(a["cursor"]); n = 6
                for i in range(1, n + 1):
                    co = (i / n) if on else (1 - i / n); await self.frame(page, co=co)
            elif "eval" in a:
                await page.evaluate(a["eval"]); await page.wait_for_timeout(int(a.get("waitMs", 300)))
            else:
                raise SystemExit(f"unknown action: {a}")
        return co

    async def after_nav(self, page, fade, co):
        await page.evaluate(REVEAL_JS)
        if self.cfg.get("prepJs"): await page.evaluate(self.cfg["prepJs"])
        if self.cfg.get("css"): await page.add_style_tag(content=self.cfg["css"])
        await page.evaluate(OVERLAY_JS)
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(int(self.cfg.get("settleMs", 700)))
        await self.state(page, co=co)
        self.fade_to(await self.snap(page), fade)

    async def signin(self, page):
        lg = self.cfg.get("login") or {}
        email = os.environ.get(lg.get("emailEnv", "SITE_USER_EMAIL"), "")
        pw = os.environ.get(lg.get("passwordEnv", "SITE_USER_PASSWORD"), "")
        if not email or not pw:
            raise SystemExit(f"scene needs sign-in: set ${lg.get('emailEnv','SITE_USER_EMAIL')} and ${lg.get('passwordEnv','SITE_USER_PASSWORD')} (a public site user, never an admin)")
        await page.goto(self.base + lg.get("path", "/account/login"), wait_until="networkidle")
        await page.fill(lg.get("emailSelector", "input[type=email], input[name=EmailAddress], #email"), email)
        await page.fill(lg.get("passwordSelector", "input[type=password]"), pw)
        async with page.expect_navigation(wait_until="networkidle"):
            await page.click(lg.get("submitSelector", "form button[type=submit]"))
        if "/account/login" in page.url and "returnUrl" not in page.url:
            # still on the login page: probably wrong credentials
            txt = await page.inner_text("body")
            if "invalid" in txt.lower() or "incorrect" in txt.lower(): raise SystemExit("sign-in failed")
        print("  signed in", file=sys.stderr)

    async def card(self, page, kind, caption=None):
        await page.set_content(card_html(kind, self.cfg, self.vw, self.vh, caption), wait_until="networkidle")
        await page.evaluate("document.fonts.ready"); await page.wait_for_timeout(250)
        return await self.snap(page)

    # -- phone scene: a real mobile viewport composited into a branded frame
    async def phone_scene(self, browser, cardpage, sc):
        ctx = await browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                                        is_mobile=True, has_touch=True, storage_state=await self.ctx.storage_state())
        page = await ctx.new_page()
        await self.prep(page, self.base + sc["url"])
        bg = await self.card(cardpage, "phone", sc.get("phoneCaption", {}))
        if bg.size != (self.W, self.H): bg = bg.resize((self.W, self.H), Image.LANCZOS)
        ph_h = int(self.H * .86); ph_w = int(ph_h * 390 / 844)
        bez = int(ph_h * .018); r_out = int(ph_w * .16); r_in = r_out - bez
        cx = int(self.W * .66); top = (self.H - ph_h - 2 * bez) // 2
        box = (cx - ph_w // 2 - bez, top, cx + ph_w // 2 + bez, top + ph_h + 2 * bez)
        # shadow + bezel drawn once onto the background
        shadow = Image.new("L", (self.W, self.H), 0)
        ImageDraw.Draw(shadow).rounded_rectangle((box[0] + 10, box[1] + 40, box[2] - 10, box[3] + 30), r_out, fill=170)
        shadow = shadow.filter(ImageFilter.GaussianBlur(40))
        base_bg = Image.composite(Image.new("RGB", bg.size, (2, 2, 10)), bg, shadow)
        d = ImageDraw.Draw(base_bg)
        d.rounded_rectangle(box, r_out, fill=(6, 7, 16), outline=(70, 74, 110), width=2)
        mask = Image.new("L", (ph_w, ph_h), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, ph_w - 1, ph_h - 1), r_in, fill=255)
        scr_xy = (box[0] + bez, box[1] + bez)
        async def pframe(poster=False, y=None):
            await page.evaluate("s => window.__wt && window.__wt(s)", {"y": y, "co": 0, "cx": 0, "cy": 0, "ro": 0, "rs": 1, "ko": 0, "kt": ""})
            shot = (await grab(page)).resize((ph_w, ph_h), Image.LANCZOS)
            f = base_bg.copy(); f.paste(shot, scr_xy, mask)
            # dynamic island
            di_w = int(ph_w * .3); di_h = int(ph_h * .028)
            ImageDraw.Draw(f).rounded_rectangle((cx - di_w // 2, scr_xy[1] + int(ph_h * .014), cx + di_w // 2, scr_xy[1] + int(ph_h * .014) + di_h), di_h // 2, fill=(0, 0, 0))
            return f
        first = await pframe()
        self.fade_to(first, sc.get("fade", .5))
        for a in sc.get("actions", [{"hold": 1.5}]):
            if "hold" in a:
                for i in range(int(a["hold"] * self.fps)): self.emit(await pframe(), a.get("poster", False))
            elif "scroll" in a:
                y0 = await page.evaluate("scrollY"); y1 = await self.resolve_y(page, a["scroll"])
                n = max(1, int(a.get("dur", 2.0) * self.fps))
                for i in range(1, n + 1): self.emit(await pframe(y=y0 + (y1 - y0) * ease(i / n)))
            else:
                raise SystemExit(f"phone scenes support hold and scroll only: {a}")
        await ctx.close()

    async def run(self, out_master):
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{self.W}x{self.H}",
               "-r", str(self.fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", "-pix_fmt", "yuv420p", out_master]
        self.ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        async with async_playwright() as p:
            exe = {"executable_path": CHROME} if os.path.exists(CHROME) else {}
            browser = await p.chromium.launch(**exe, args=["--no-sandbox", "--hide-scrollbars", "--force-color-profile=srgb"])
            self.ctx = await browser.new_context(viewport={"width": self.vw, "height": self.vh}, device_scale_factor=self.dsf,
                                                 color_scheme=self.cfg.get("colorScheme", "light"), reduced_motion="no-preference")
            cardpage = await self.ctx.new_page()
            page = await self.ctx.new_page()
            t0 = time.time()
            # title card
            if self.cfg.get("title") is not False:
                img = await self.card(cardpage, "title")
                self.last = Image.new("RGB", (self.W, self.H), (9, 10, 28))
                self.fade_to(img, .5)
                for _ in range(int(self.cfg.get("title", {}).get("hold", 1.6) * self.fps)): self.emit(img)
            for i, sc in enumerate(self.cfg["scenes"]):
                print(f"scene {i+1}/{len(self.cfg['scenes'])}: {sc.get('url')}  (frames so far {self.frames}, {time.time()-t0:.0f}s)", file=sys.stderr)
                if sc.get("phone"):
                    await self.phone_scene(browser, cardpage, sc); continue
                if sc.get("signin"): await self.signin(page)
                self.cap = sc.get("caption", ""); self.capop = 0.0
                await self.prep(page, self.base + sc["url"])
                if sc.get("startScroll") is not None:
                    await self.state(page, y=await self.resolve_y(page, sc["startScroll"]))
                await self.state(page, co=0)
                self.fade_to(await self.snap(page), sc.get("fade", .5))
                acts = list(sc.get("actions", [{"hold": 1.5}]))
                if self.cap: acts.insert(0, {"caption": self.cap})
                co = await self.run_actions(page, acts, False)
                # fade caption and cursor out at the end of the scene
                if self.capop > 0 or co > 0:
                    n = 6; c0, k0 = co, self.capop
                    for j in range(1, n + 1):
                        self.capop = k0 * (1 - j / n); await self.frame(page, co=c0 * (1 - j / n))
            # end card
            if self.cfg.get("end") is not False:
                img = await self.card(cardpage, "end")
                self.fade_to(img, .6)
                for _ in range(int(self.cfg.get("end", {}).get("hold", 2.4) * self.fps)): self.emit(img)
            await browser.close()
        self.ff.stdin.close(); self.ff.wait()
        if self.ff.returncode: raise SystemExit("ffmpeg (master) failed")
        print(f"rendered {self.frames} frames ({self.frames/self.fps:.1f}s) in {time.time()-t0:.0f}s", file=sys.stderr)

def encode(master, out, max_mb, fps):
    for crf in (20, 22, 24, 26, 28, 30):
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", master, "-an", "-c:v", "libx264", "-preset", "slow", "-crf", str(crf),
               "-maxrate", "6M", "-bufsize", "12M", "-profile:v", "high", "-level", "4.1", "-pix_fmt", "yuv420p",
               "-r", str(fps), "-g", str(fps * 2), "-movflags", "+faststart", out]
        subprocess.run(cmd, check=True)
        mb = os.path.getsize(out) / 1e6
        print(f"  crf {crf}: {mb:.1f} MB", file=sys.stderr)
        if mb <= max_mb: return crf, mb
    return crf, mb

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("shotlist"); ap.add_argument("--out", help="output directory (default: ./walkthrough-out/<slug>, or $WALK_OUT/<slug>)")
    ap.add_argument("--base", help="override the site base URL"); ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--max-mb", type=float, default=14.5); ap.add_argument("--keep-master", action="store_true")
    args = ap.parse_args()
    cfg = json.load(open(args.shotlist))
    slug = cfg.get("slug") or os.path.splitext(os.path.basename(args.shotlist))[0]
    out = args.out or os.path.join(os.environ.get("WALK_OUT", os.path.join(os.getcwd(), "walkthrough-out")), slug)
    os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="walk-"); master = os.path.join(tmp, "master.mp4")
    rec = Recorder(cfg, args)
    asyncio.run(rec.run(master))
    mp4 = os.path.join(out, f"{slug}-walkthrough.mp4")
    crf, mb = encode(master, mp4, args.max_mb, args.fps)
    poster = rec.poster or rec.last
    pj = os.path.join(out, f"{slug}-walkthrough-poster.jpg"); poster.save(pj, quality=88, optimize=True, progressive=True)
    if args.keep_master: shutil.copy(master, os.path.join(out, "master.mp4"))
    shutil.rmtree(tmp, ignore_errors=True)
    dur = rec.frames / args.fps
    print(json.dumps({"mp4": mp4, "poster": pj, "seconds": round(dur, 2), "mb": round(mb, 2), "crf": crf,
                      "size": f"{rec.W}x{rec.H}"}))
    if not 20 <= dur <= 40: print(f"WARNING: duration {dur:.1f}s is outside 20-40 s; adjust holds/durations", file=sys.stderr)

if __name__ == "__main__":
    main()
