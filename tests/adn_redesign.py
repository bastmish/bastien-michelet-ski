"""Focused ADN alpine layout checks. Serve public on 3000 and 0c1bfaf public on 3008."""
from pathlib import Path
import json, subprocess
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/adn-v2';OUT.mkdir(parents=True,exist_ok=True)
# Prove that all markup outside this zone and all other public pages are unchanged.
before=BeautifulSoup(subprocess.check_output(['git','show','0c1bfaf:public/index.html'],cwd=ROOT),'html.parser')
after=BeautifulSoup((ROOT/'public/index.html').read_text(),'html.parser')
for soup in [before,after]:
 for node in list(soup.select('#expertise,#adn')):
  if node.parent:node.decompose()
assert [l for l in str(before).splitlines() if l.strip()]==[l for l in str(after).splitlines() if l.strip()],'Change outside ADN'
for file in (ROOT/'public').rglob('*.html'):
 if file.name=='index.html' and file.parent==ROOT/'public':continue
 old=subprocess.check_output(['git','show','0c1bfaf:public/'+str(file.relative_to(ROOT/'public'))],cwd=ROOT)
 assert old==file.read_bytes(),str(file)
blocks=json.loads((ROOT/'content/pages.json').read_text())[0]['sections'][1]['blocks']
results={'reference':'0c1bfaf','scope':'PASS: only ADN HTML/CSS changed; other public HTML byte-identical','viewports':[],'page_errors':[],'failed_hosts':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(reduced_motion='reduce')
 page.on('pageerror',lambda e:results['page_errors'].append(str(e)))
 page.on('requestfailed',lambda r:results['failed_hosts'].append({'url':r.url,'error':r.failure}))
 for width,height in [(1440,900),(1280,800),(1024,768),(768,1024),(390,844)]:
  page.set_viewport_size({'width':width,'height':height})
  page.goto('http://localhost:3000/',wait_until='networkidle')
  area=page.locator('#expertise')
  assert area.locator('img').count()==1
  assert area.locator('a,button,svg').count()==0
  assert area.locator('.adn-secondary-block').count()==2
  for block in blocks:
   assert area.get_by_text(block['text'],exact=True).count()==1,block['label']
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  geo=area.evaluate('''s=>{const r=q=>{let a=s.querySelector(q).getBoundingClientRect();return {x:a.x,y:a.y,w:a.width,h:a.height,b:a.bottom,r:a.right}},image=r('figure'),main=r('.adn-main-copy'),composition=r('.adn-v2-composition'),secondary=[...s.querySelectorAll('.adn-secondary-block')].map(n=>{let a=n.getBoundingClientRect();return {x:a.x,y:a.y,b:a.bottom,w:a.width}});return {image,main,composition,secondary,mask:getComputedStyle(s.querySelector('figure')).maskImage,background:getComputedStyle(s).backgroundColor,clipping:[...s.querySelectorAll('h2,h3,p')].some(n=>n.scrollWidth>n.clientWidth+1||(['hidden','clip'].includes(getComputedStyle(n).overflowY)&&n.scrollHeight>n.clientHeight+1))}}''')
  assert geo['background']=='rgb(248, 247, 244)'
  assert not geo['clipping']
  assert geo['secondary'][0]['y']>=max(geo['main']['b'],geo['image']['b'])
  if width>=1280:
   assert 540<=geo['composition']['h']<=720
   if width==1440:assert abs(geo['composition']['h']-620)<1
   assert geo['main']['x']>=width*.63-1
   assert geo['main']['y']>=geo['composition']['y']
   assert geo['main']['b']<=geo['composition']['b']
   assert geo['mask']!='none'
  else:
   assert geo['mask']=='none'
   assert geo['main']['y']>=geo['image']['b']
   if width<768:assert 340<=geo['image']['h']<=420
   else:assert geo['image']['h']<=520
  two_columns=abs(geo['secondary'][0]['y']-geo['secondary'][1]['y'])<1
  assert two_columns==(width>=816)
  if two_columns:assert all(n['w']>=320 for n in geo['secondary'])
  else:assert geo['secondary'][1]['y']>=geo['secondary'][0]['b']+48
  assert area.locator('h2').evaluate('(n)=>getComputedStyle(n).fontWeight')=='400'
  page.add_style_tag(content='html{scroll-behavior:auto!important}')
  page.evaluate('scrollTo(0,0)');page.wait_for_timeout(100)
  clip=area.evaluate('s=>{let r=s.getBoundingClientRect(),y=Math.floor(r.top+scrollY);return {x:0,y,width:innerWidth,height:Math.ceil(r.bottom+scrollY)-y}}')
  page.screenshot(path=str(OUT/f'after-section-{width}.png'),clip=clip,full_page=True,animations='disabled')
  page.evaluate('y=>scrollTo(0,y)',max(0,clip['y']-100));page.wait_for_timeout(100)
  page.screenshot(path=str(OUT/f'after-viewport-{width}x{height}.png'),animations='disabled')
  loaded=area.locator('img').evaluate('(i)=>i.complete&&i.naturalWidth>0')
  results['viewports'].append({'width':width,'height':height,'copy':'PASS: nine exact labels/titles/paragraphs','layout':'PASS','overflow':False,'photo_loaded':loaded,'geometry':geo})
  for sid,dark in [('offres',True),('avis',False)]:
   page.evaluate("sid=>{const h=document.querySelector('#'+sid+' h2');scrollTo(0,h.getBoundingClientRect().top+scrollY-150)}",sid)
   page.wait_for_timeout(150)
   assert page.evaluate("document.body.classList.contains('ski-dark-mode')")==dark
 for width in [1440,1024,390]:
  page.set_viewport_size({'width':width,'height':1000})
  page.goto('http://localhost:3008/',wait_until='networkidle')
  page.add_style_tag(content='*{scroll-behavior:auto!important;transition:none!important;animation:none!important}')
  page.locator('#expertise').scroll_into_view_if_needed();page.wait_for_timeout(100)
  page.evaluate('scrollTo(0,0)');page.wait_for_timeout(100)
  clip=page.evaluate('''()=>{let a=document.querySelector('#expertise').getBoundingClientRect(),b=document.querySelector('#expertise').getBoundingClientRect();let y=Math.floor(a.top+scrollY);return {x:0,y,width:innerWidth,height:Math.ceil(b.bottom+scrollY)-y}}''')
  page.screenshot(path=str(OUT/f'before-{width}.png'),clip=clip,full_page=True,animations='disabled')
 page.goto('http://localhost:3000/',wait_until='networkidle')
 page.add_script_tag(path='/tmp/ski-qa/node_modules/axe-core/axe.min.js')
 issues=page.evaluate('''async()=> (await axe.run(document.querySelector('#expertise'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)}))''')
 results['accessibility']=issues
 assert not issues and not results['page_errors']
 browser.close()
results['functional_and_layout']='PASS'
results['photographic_validation']='PASS' if all(i['photo_loaded'] for i in results['viewports']) else 'BLOCKED'
# Keep the network report readable without dropping the actual failure evidence.
results['failed_hosts']=list({(r['url'],r['error']):r for r in results['failed_hosts']}.values())
(OUT/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print('PASS: exact copy, scope, responsive 1440/1280/1024/768/390, chapter transitions, no JS errors or axe violations in ADN.')
print('Photographs:',results['photographic_validation'])
