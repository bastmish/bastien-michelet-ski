"""Responsive story page and its reused home chapter transitions."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
OUT=Path(__file__).resolve().parents[1]/'docs/story-home'
OUT.mkdir(parents=True,exist_ok=True)
report=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(reduced_motion='reduce')
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 for width in [375,768,1440]:
  page.set_viewport_size({'width':width,'height':1000})
  page.goto('http://localhost:3000/manifesto.html',wait_until='networkidle')
  assert page.locator('h1').count()==1
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert page.locator('[data-editorial-section]').count()==4
  page.add_style_tag(content='*{scroll-behavior:auto!important;transition:none!important}')
  for sid,dark,light in [('offres',True,False),('formules',True,False),('contact',False,True)]:
   page.evaluate("(sid)=>{let e=document.querySelector('#'+sid+' h2');scrollTo(0,e.getBoundingClientRect().top+scrollY-150)}",sid)
   page.wait_for_timeout(100)
   assert page.evaluate("document.body.classList.contains('ski-dark-mode')")==dark,(width,sid)
   assert page.evaluate("document.body.classList.contains('ski-reviews-light')")==light
  report.append({'width':width,'overflow':False,'chapters':'PASS'})
 for version,port in [('before',3005),('after',3000)]:
  for width in [390,1440]:
   page.set_viewport_size({'width':width,'height':1000})
   page.goto(f'http://localhost:{port}/manifesto.html',wait_until='networkidle')
   page.add_style_tag(content='*{scroll-behavior:auto!important;transition:none!important;animation:none!important}')
   page.screenshot(path=str(OUT/f'{version}-{width}.png'),full_page=True)
   if version=='after':
    for sid in ['offres','formules']:
     page.evaluate("(sid)=>{let e=document.querySelector('#'+sid+' h2');scrollTo(0,e.getBoundingClientRect().top+scrollY-150)}",sid)
     page.wait_for_timeout(100)
     page.locator('#'+sid).screenshot(path=str(OUT/f'after-{sid}-{width}.png'))
 assert not errors,errors
 browser.close()
(OUT/'results.json').write_text(json.dumps({'viewports':report,'page_errors':errors},indent=2))
print('PASS: story page at 375/768/1440, all four sections, home chapter transitions, no JS errors.')
