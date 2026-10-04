#!/usr/bin/env python3
"""Capture desktop and mobile screenshots of a Raytha site with Playwright.

Usage:
  pip install playwright && playwright install chromium
  BASE_URL=http://localhost:5001 python3 scripts/capture-screenshots.py conference-horizon-summit/shots.json [OUT_DIR]

shots.json is a list of shots:
  {"name": "01-home-1440.png", "path": "/", "device": "desktop", "full_page": false, "scroll": 0, "login": false}

device is "desktop" (1440x900) or "mobile" (390x844). Shots with "login": true are taken after signing in
with SITE_USER_EMAIL / SITE_USER_PASSWORD (a public site user, never an admin), if those are set.
Elements with the class "reveal" are forced visible so scroll animations do not leave blank areas.
"""
import asyncio, json, os, sys
from playwright.async_api import async_playwright

BASE = os.environ.get("BASE_URL", "http://localhost:5001").rstrip("/")
DEVICES = {
    "desktop": dict(viewport={"width": 1440, "height": 900}, device_scale_factor=2),
    "mobile": dict(viewport={"width": 390, "height": 844}, device_scale_factor=3, is_mobile=True, has_touch=True),
}

async def prep(page, path, scroll=0):
    await page.goto(BASE + path, wait_until="networkidle")
    await page.evaluate("document.fonts.ready")
    await page.evaluate("""async () => { for (let y = 0; y < document.body.scrollHeight; y += 500) {
        window.scrollTo(0, y); await new Promise(r => setTimeout(r, 50)); } window.scrollTo(0, 0); }""")
    await page.evaluate("document.querySelectorAll('.reveal').forEach(e => e.classList.add('in'))")
    # Load any lazy images the quick scroll skipped past.
    await page.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => i.loading = 'eager')")
    await page.wait_for_load_state("networkidle")
    if scroll:
        await page.evaluate(f"window.scrollTo(0, {int(scroll)})")
    await page.wait_for_timeout(1200)

async def login(page):
    email, pw = os.environ.get("SITE_USER_EMAIL"), os.environ.get("SITE_USER_PASSWORD")
    if not (email and pw):
        return False
    await page.goto(BASE + "/account/login", wait_until="networkidle")
    await page.fill("#email", email)
    await page.fill("#password", pw)
    await page.click("button[type=submit]")
    await page.wait_for_load_state("networkidle")
    return True

async def main():
    shots = json.load(open(sys.argv[1]))
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(sys.argv[1]), "screenshots")
    os.makedirs(out, exist_ok=True)
    exe = os.environ.get("CHROME_PATH")
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=exe, args=["--no-sandbox"]) if exe else await p.chromium.launch()
        contexts = {}
        for shot in shots:
            dev = shot.get("device", "desktop")
            key = (dev, bool(shot.get("login")))
            if key not in contexts:
                ctx = await browser.new_context(**DEVICES[dev])
                page = await ctx.new_page()
                if shot.get("login") and not await login(page):
                    print(f"skip {shot['name']}: set SITE_USER_EMAIL and SITE_USER_PASSWORD", file=sys.stderr)
                    continue
                contexts[key] = page
            page = contexts[key]
            await prep(page, shot["path"], shot.get("scroll", 0))
            await page.screenshot(path=os.path.join(out, shot["name"]), full_page=bool(shot.get("full_page")))
            print(shot["name"])
        await browser.close()

asyncio.run(main())
