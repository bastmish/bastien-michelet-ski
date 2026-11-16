"""UI SPEC 04: serve current public on 3000, reference 14df990 on 3009."""
from pathlib import Path
import json,subprocess
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/course-formats';OUT.mkdir(parents=True,exist_ok=True)
reference='14df990'
def original(path):return subprocess.check_output(['git','show',reference+':public/'+path],cwd=ROOT)
before=BeautifulSoup(original('index.html'),'html.parser');after=BeautifulSoup((ROOT/'public/index.html').read_text(),'html.parser')
assert [str(n) for n in before.select('#offres .ss-offer-card')]==[str(n) for n in after.select('#offres .ss-offer-card')]
for soup in [before,after]:
 for n in soup.select('#formules,link[href="/course-formats.css"]'):n.decompose()
 node=soup.select_one('#offres');node['class']=[c for c in node['class'] if c!='ss-formats-transition']
assert str(before)==str(after),'HTML changed outside authorised section/transition'
for file in (ROOT/'public').rglob('*.html'):
 if file==ROOT/'public/index.html':continue
 assert original(str(file.relative_to(ROOT/'public')))==file.read_bytes(),str(file)
source=json.loads((ROOT/'content/pages.json').read_text())[0]['sections'][3]
result={'reference':reference,'scope':'PASS: unchanged experience-card DOM, home outside formats/join, and other public HTML','viewports':[],'page_errors':[],'failed_requests':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(reduced_motion='reduce')
 page.on('pageerror',lambda e:result['page_errors'].append(str(e)))
 page.on('requestfailed',lambda r:result['failed_requests'].append({'url':r.url,'error':r.failure}))
 for width,height in [(1536,960),(1440,900),(1280,800),(1024,768),(768,1024),(390,844),(375,812)]:
  page.set_viewport_size({'width':width,'height':height});page.goto('http://localhost:3000/',wait_until='networkidle')
  page.add_style_tag(content='html{scroll-behavior:auto!important}')
  area=page.locator('#formules');assert area.locator('.ss-course-format').count()==3
  assert area.locator('img,svg,button,article a').count()==0
  for b in source['blocks']:
   if b['text'].startswith('**'):continue
   assert area.get_by_text(b['text'],exact=True).count()==1,b['text']
  assert area.get_by_text('Freeride : journée complète ou sur mesure.',exact=True).count()==1
  geometry=area.evaluate('''s=>{const rect=n=>{let a=n.getBoundingClientRect();return {x:a.x,y:a.y,w:a.width,h:a.height,r:a.right,b:a.bottom}},r=rect(s),cards=[...s.querySelectorAll('article')].map(n=>({rect:rect(n),category:rect(n.querySelector('h3')),duration:rect(n.querySelector('.ss-course-format__duration')),body:rect(n.querySelector('p'))})),grid=document.querySelector('.ss-offer-grid').getBoundingClientRect(),h=s.querySelector('h2').getBoundingClientRect();return {rect:r,cards,gap:h.top-grid.bottom,background:getComputedStyle(s).backgroundColor,footerBackground:getComputedStyle(s.querySelector('footer')).backgroundColor,overflow:[...s.querySelectorAll('h2,h3,h4,p,a')].filter(n=>n.scrollWidth>n.clientWidth+1||(['hidden','clip'].includes(getComputedStyle(n).overflowY)&&n.scrollHeight>n.clientHeight+1)).map(n=>n.tagName)}}''')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width
  assert not geometry['overflow'],geometry['overflow']
  assert geometry['background']=='rgb(247, 246, 242)'
  assert geometry['footerBackground']=='rgba(0, 0, 0, 0)'
  if width>=1200:assert abs(geometry['gap']-88)<1,geometry['gap']
  for card in geometry['cards']:
   assert card['duration']['x']>=card['category']['r']-1
   assert abs(card['duration']['y']-card['category']['y'])<1
   if width<768:assert card['body']['y']>=card['category']['b']
  # Capture full section without introducing a fixed-header overlay into the crop.
  page.evaluate('scrollTo(0,0)');page.wait_for_timeout(100)
  clip=area.evaluate('s=>{let r=s.getBoundingClientRect(),y=Math.floor(r.top+scrollY);return {x:0,y,width:innerWidth,height:Math.ceil(r.bottom+scrollY)-y}}')
  page.screenshot(path=str(OUT/f'after-section-{width}.png'),clip=clip,full_page=True,animations='disabled')
  # Also keep exact requested viewport dimensions.
  page.evaluate('y=>scrollTo(0,y)',clip['y']-100);page.wait_for_timeout(100)
  page.screenshot(path=str(OUT/f'after-viewport-{width}x{height}.png'),animations='disabled')
  result['viewports'].append({'width':width,'height':height,'layout':'PASS','copy':'PASS','overflow':False,'geometry':geometry})
 # Combined desktop chapter capture with the native scrolled card appearance.
 page.set_viewport_size({'width':1440,'height':900});page.goto('http://localhost:3000/',wait_until='networkidle')
 page.add_style_tag(content='html{scroll-behavior:auto!important}')
 page.locator('#tiles-title').scroll_into_view_if_needed();page.wait_for_timeout(200)
 def card_styles():return page.locator('#offres .ss-offer-card').evaluate_all("nodes=>nodes.map(n=>({rect:{w:n.getBoundingClientRect().width,h:n.getBoundingClientRect().height},parts:[...n.querySelectorAll('h3,p,img')].map(e=>({color:getComputedStyle(e).color,font:getComputedStyle(e).font,borderRadius:getComputedStyle(e).borderRadius,aspectRatio:getComputedStyle(e).aspectRatio}))}))")
 after_cards=card_styles()
 clip=page.evaluate("()=>{let a=document.querySelector('#offres').getBoundingClientRect(),b=document.querySelector('#formules').getBoundingClientRect(),y=Math.floor(a.top+scrollY);return {x:0,y,width:innerWidth,height:Math.ceil(b.bottom+scrollY)-y}}")
 page.screenshot(path=str(OUT/'after-experiences-formats-1440.png'),clip=clip,full_page=True,animations='disabled')
 # Genuine action: CTA opens the existing contact flow, with no external submission.
 cta=page.locator('.ss-course-formats__cta');assert cta.get_attribute('href')=='#contact'
 cta.focus();assert cta.evaluate("n=>getComputedStyle(n).outlineWidth")=='3px'
 cta.press('Enter');assert page.url.endswith('#contact')
 assert page.locator('#ski-request-form').count()==1
 page.add_script_tag(path='/tmp/ski-qa/node_modules/axe-core/axe.min.js')
 result['accessibility']=page.evaluate("async()=> (await axe.run(document.querySelector('#formules'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))")
 assert not result['accessibility'],result['accessibility']
 # Compare untouched experience card geometry/type with the prior scrolled state.
 page.goto('http://localhost:3009/',wait_until='networkidle');page.add_style_tag(content='html{scroll-behavior:auto!important}')
 page.locator('#tiles-title').scroll_into_view_if_needed();page.wait_for_timeout(200)
 assert card_styles()==after_cards,'Experience card style/size regression'
 clip=page.evaluate("()=>{let a=document.querySelector('#offres').getBoundingClientRect(),b=document.querySelector('#formules').getBoundingClientRect(),y=Math.floor(a.top+scrollY);return {x:0,y,width:innerWidth,height:Math.ceil(b.bottom+scrollY)-y}}")
 page.screenshot(path=str(OUT/'before-experiences-formats-1440.png'),clip=clip,full_page=True,animations='disabled')
 assert not result['page_errors']
 browser.close()
result['cta_keyboard']='PASS: #contact, existing enquiry form, no submission'
result['experience_cards']='PASS: DOM, dimensions and typography unchanged'
result['failed_requests']=list({(r['url'],r['error']):r for r in result['failed_requests']}.values())
result['photographs_and_fonts']='BLOCKED' if result['failed_requests'] else 'LOADED'
(OUT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print('PASS: seven viewports, exact copy, scope, original experience cards, CTA keyboard, no JS errors or targeted axe violations.')
print('Remote resources:',result['photographs_and_fonts'])
