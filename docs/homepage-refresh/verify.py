"""Validate the actual Jekyll output and capture responsive review evidence.

Run from the repository root after the production build:
  python docs/homepage-refresh/verify.py
Requires Python Playwright and an installed Chrome browser.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from urllib.parse import urlparse, unquote
import hashlib
import json
import subprocess
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/homepage-refresh'
SHOTS = OUT / 'screenshots'
SHOTS.mkdir(exist_ok=True)
assert (ROOT / '_site/index.html').is_file(), 'Build with Jekyll first'
portrait = ROOT / 'assets/img/prof_pic.jpg'
expected = '5a48201603f476ab5d549eaf138401d0a43aa1098a79656feddcfc93bf0ce343'
assert hashlib.sha256(portrait.read_bytes()).hexdigest() == expected

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(ROOT / '_site')))
Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}'
results = {'portrait_sha256': expected, 'viewports': [], 'pages': [], 'external_links': []}
try:
    with sync_playwright() as p:
        chrome = os.environ.get('CHROME_PATH', 'C:/Program Files/Google/Chrome/Application/chrome.exe')
        browser = p.chromium.launch(executable_path=chrome, headless=True)
        page = browser.new_page(device_scale_factor=1)
        errors = []
        page.on('pageerror', lambda err: errors.append(str(err)))
        for width, height in [(1440,900),(768,1024),(390,844),(375,812)]:
            page.set_viewport_size({'width':width,'height':height})
            response = page.goto(base, wait_until='networkidle')
            assert response.status == 200
            page.locator('.portrait').wait_for()
            page.evaluate('document.fonts.ready')
            assert page.locator('.paper').count() == 3
            assert page.locator('.paper .authors strong').all_text_contents() == ['Xinyuan Zhou'] * 3
            assert page.locator('.prize-row').count() == 3
            assert page.locator('.biography p').count() == 3
            text = page.locator('main').inner_text()
            for forbidden in ['Albert Einstein','Former Class President','Accepted','SWIRL','My Contributions','National Grand Prize']:
                assert forbidden not in text, forbidden
            overflow = page.evaluate('document.documentElement.scrollWidth > innerWidth')
            assert not overflow, f'Horizontal overflow at {width}'
            broken = page.locator('img').evaluate_all('(els)=>els.filter(e=>!e.complete||!e.naturalWidth).map(e=>e.src)')
            assert not broken, broken
            ratio = page.locator('.portrait').evaluate('(e)=>({natural:e.naturalWidth/e.naturalHeight,display:e.getBoundingClientRect().width/e.getBoundingClientRect().height})')
            assert abs(ratio['natural']-ratio['display']) < .01
            boxes = [page.locator('.paper-visual').first.bounding_box(), page.locator('.paper-copy').first.bounding_box()]
            if width <= 390:
                assert boxes[1]['y'] >= boxes[0]['y']+boxes[0]['height']
            else:
                assert boxes[1]['x'] > boxes[0]['x']
            page.screenshot(path=str(SHOTS/f'new-{width}-full.png'),full_page=True)
            page.screenshot(path=str(SHOTS/f'new-{width}-hero.png'))
            page.locator('#research').screenshot(path=str(SHOTS/f'new-{width}-research.png'))
            page.locator('#honors').screenshot(path=str(SHOTS/f'new-{width}-honors.png'))
            page.get_by_role('navigation').get_by_role('link',name='Research',exact=True).click()
            assert page.url.endswith('#research')
            results['viewports'].append({'width':width,'height':height,'horizontal_overflow':overflow,'broken_images':broken,'portrait_ratio':ratio,'paper_layout':'stacked' if width <=390 else 'side-by-side'})
        for route in ['/', '/honors/', '/cv/', '/404.html']:
            for width in [1440,390]:
                page.set_viewport_size({'width':width,'height':900})
                page.goto(base+route,wait_until='networkidle')
                assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
                links = page.locator('a[href]').evaluate_all('(els)=>els.map(e=>e.getAttribute("href"))')
                for href in links:
                    if href.startswith('mailto:'):
                        assert href == 'mailto:202311260012@mail.bnu.edu.cn'
                    elif href.startswith('http'):
                        results['external_links'].append(href)
                    else:
                        target = urlparse(href)
                        file = ROOT / '_site' / unquote(target.path).lstrip('/')
                        if not target.path: file = ROOT / '_site' / route.lstrip('/')
                        if file.is_dir(): file = file / 'index.html'
                        assert file.exists(), f'Broken local link {href}'
                if route in ['/honors/','/cv/']:
                    page.screenshot(path=str(SHOTS/f'{route.strip("/")}-{width}.png'),full_page=True)
                results['pages'].append({'route':route,'width':width,'local_links':'pass','overflow':False})
        page.goto(base)
        page.keyboard.press('Tab')
        assert page.locator(':focus').inner_text() == 'Skip to content'
        assert not errors, errors
        results['keyboard_skip_link'] = 'pass'
        results['page_errors'] = errors
        results['external_links'] = sorted(set(results['external_links']))
        browser.close()
finally:
    server.shutdown()
(OUT/'verification.json').write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps(results,indent=2,ensure_ascii=False))
