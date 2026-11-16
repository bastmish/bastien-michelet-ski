"""Compact Experiences/Formats: current public on 3000, ccccbba reference on 3010."""
from pathlib import Path
import json,subprocess
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/compact-courses';OUT.mkdir(parents=True,exist_ok=True)
reference='ccccbba'
def original(path):return subprocess.check_output(['git','show',reference+':public/'+path],cwd=ROOT)
before=BeautifulSoup(original('index.html'),'html.parser');after=BeautifulSoup((ROOT/'public/index.html').read_text(),'html.parser')
expected_urls=[n['href'] for n in before.select('#offres .ss-offer-card')]
expected_ctas=[n.get_text() for n in before.select('#offres .ss-offer-cta')]
assert expected_urls==[n['href'] for n in after.select('.ss-experiences-compact__item')]
assert [n['src'] for n in before.select('#offres img')]==[n['src'] for n in after.select('#offres img')]
for soup in [before,after]:
 for n in list(soup.select('.ss-home-courses,#offres,#formules')):
  if n.parent:n.decompose()
assert [l for l in str(before).splitlines() if l.strip()]==[l for l in str(after).splitlines() if l.strip()],'Change outside authorised chapter'
for file in (ROOT/'public').rglob('*.html'):
 if file==ROOT/'public/index.html':continue
 assert original(str(file.relative_to(ROOT/'public')))==file.read_bytes(),str(file)
source=json.loads((ROOT/'content/pages.json').read_text())[0]['sections']
result={'reference':reference,'scope':'PASS: only home sections 03/04 HTML/CSS; all other public HTML byte-identical','viewports':[],'page_errors':[],'failed_requests':[]}
viewports=[(1536,960),(1440,900),(1280,800),(1024,768),(768,1024),(390,844),(375,812)]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(reduced_motion='reduce')
 page.on('pageerror',lambda e:result['page_errors'].append(str(e)))
 page.on('requestfailed',lambda r:result['failed_requests'].append({'url':r.url,'error':r.failure}))
 for width,height in viewports:
  page.set_viewport_size({'width':width,'height':height});page.goto('http://localhost:3000/',wait_until='networkidle')
  page.add_style_tag(content='html{scroll-behavior:auto!important}')
  area=page.locator('.ss-home-courses')
  assert area.locator('.ss-experiences-compact__item').count()==4
  assert area.locator('.ss-formats-compact__item').count()==3
  assert area.locator('a a').count()==0
  assert area.locator('img').count()==4
  assert area.get_by_text('NOTRE SPÉCIALITÉ',exact=True).count()==1
  for txt in [source[2]['blocks'][1]['text'],source[2]['blocks'][2]['text'],source[3]['blocks'][1]['text'],source[3]['blocks'][12]['text'],source[3]['blocks'][13]['text']]:
   assert area.get_by_text(txt,exact=True).count()==1,txt
  for category,duration in [('DEMI-JOURNÉE','2 h 30'),('JOURNÉE COMPLÈTE','09h30 – 17h00'),('SUR MESURE','Sur demande')]:
   assert area.get_by_text(category,exact=True).count()==1
   assert area.get_by_text(duration,exact=True).count()==1
  for i,cta in enumerate(expected_ctas):
   assert area.locator('.ss-experiences-compact__link').nth(i).inner_text().strip()==cta
  assert area.get_by_text('Freeride : journée complète ou sur mesure.',exact=True).count()==1
  geometry=area.evaluate('''s=>{const r=n=>{let a=n.getBoundingClientRect();return {x:a.x,y:a.y,w:a.width,h:a.height,r:a.right,b:a.bottom}},bg=n=>getComputedStyle(n).backgroundColor;return {rect:r(s),background:bg(s),cards:[...s.querySelectorAll('.ss-experiences-compact__item')].map(n=>({rect:r(n),bg:bg(n),photo:r(n.querySelector('img'))})),formats:[...s.querySelectorAll('.ss-formats-compact__item')].map(n=>({rect:r(n),bg:bg(n)})),clipped:[...s.querySelectorAll('h2,h3,p,a')].some(n=>n.scrollWidth>n.clientWidth+1||(['hidden','clip'].includes(getComputedStyle(n).overflowY)&&n.scrollHeight>n.clientHeight+1))}}''')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert not geometry['clipped']
  assert geometry['background']=='rgb(247, 246, 242)'
  assert all(c['bg']=='rgba(0, 0, 0, 0)' for c in geometry['cards']+geometry['formats'])
  rows=len({round(c['rect']['y']) for c in geometry['cards']})
  assert rows==(1 if width>=1280 else 2 if width>=768 else 4)
  if width>=1280:assert all(abs(c['photo']['h']-280)<1 for c in geometry['cards'])
  elif width>=768:assert all(abs(c['photo']['w']/c['photo']['h']-4/3)<.01 for c in geometry['cards'])
  else:assert all(abs(c['photo']['w']/c['photo']['h']-16/10)<.01 for c in geometry['cards'])
  if width==1440:assert 780<=geometry['rect']['h']<=850,geometry['rect']['h']
  photo_loaded=area.locator('img').evaluate_all('ns=>ns.every(n=>n.complete&&n.naturalWidth>0)')
  # Whole chapter capture, then exact viewport from the beginning of the chapter.
  page.evaluate('scrollTo(0,0)');page.wait_for_timeout(100)
  clip=area.evaluate('s=>{let r=s.getBoundingClientRect(),y=Math.floor(r.top+scrollY);return {x:0,y,width:innerWidth,height:Math.ceil(r.bottom+scrollY)-y}}')
  page.screenshot(path=str(OUT/f'after-full-{width}.png'),clip=clip,full_page=True,animations='disabled')
  page.evaluate('y=>scrollTo(0,y)',geometry['rect']['y']);page.wait_for_timeout(200)
  if width==1440:
   visible=area.evaluate('''s=>[...s.querySelectorAll('h2,.ss-experiences-compact__item,.ss-formats-compact__item,.ss-formats-compact__cta')].every(n=>{let r=n.getBoundingClientRect();return r.top>=0&&r.bottom<=innerHeight})''')
   assert visible,'Required experiences and formats must fit simultaneously in 1440x900'
  page.screenshot(path=str(OUT/f'after-viewport-{width}x{height}.png'),animations='disabled')
  result['viewports'].append({'width':width,'height':height,'layout':'PASS','overflow':False,'photo_loaded':photo_loaded,'geometry':geometry})
 # Accessibility and every real action, without submitting a request.
 page.set_viewport_size({'width':1440,'height':900});page.goto('http://localhost:3000/',wait_until='networkidle')
 page.add_script_tag(path='/tmp/ski-qa/node_modules/axe-core/axe.min.js')
 result['accessibility']=page.evaluate("async()=> (await axe.run(document.querySelector('.ss-home-courses'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))")
 assert not result['accessibility'],result['accessibility']
 for i,url in enumerate(expected_urls):
  node=page.locator('.ss-experiences-compact__item').nth(i);node.focus()
  assert node.evaluate('n=>getComputedStyle(n).outlineWidth')=='2px'
  node.press('Enter');page.wait_for_url('**/'+url)
  assert page.locator('h1').count()==1
  page.goto('http://localhost:3000/',wait_until='networkidle')
 cta=page.locator('.ss-formats-compact__cta');cta.focus();cta.press('Enter')
 assert page.url.endswith('#contact') and page.locator('#ski-request-form').count()==1
 # Before/after comparison from the same previous branch state.
 for width,height in [(1440,900),(390,844)]:
  page.set_viewport_size({'width':width,'height':height});page.goto('http://localhost:3010/',wait_until='networkidle')
  page.add_style_tag(content='html{scroll-behavior:auto!important}')
  page.locator('#tiles-title').scroll_into_view_if_needed();page.wait_for_timeout(200)
  clip=page.evaluate("()=>{let a=document.querySelector('#offres').getBoundingClientRect(),b=document.querySelector('#formules').getBoundingClientRect(),y=Math.floor(a.top+scrollY);return {x:0,y,width:innerWidth,height:Math.ceil(b.bottom+scrollY)-y}}")
  page.screenshot(path=str(OUT/f'before-full-{width}.png'),clip=clip,full_page=True,animations='disabled')
 assert not result['page_errors']
 browser.close()
result['actions']='PASS: four original experience URLs and contact CTA by keyboard; no form submitted'
result['failed_requests']=list({(r['url'],r['error']):r for r in result['failed_requests']}.values())
result['photographs_and_fonts']='BLOCKED' if result['failed_requests'] else 'LOADED'
(OUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print('PASS: seven viewports, scope, compact copy, links/keyboard, no clipping/overflow, targeted axe and simultaneous 1440x900 visibility.')
print('Remote resources:',result['photographs_and_fonts'])
