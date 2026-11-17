"""Home closing banner only; current public 3000 and 528f726 reference 3012."""
from pathlib import Path
import json,subprocess
from bs4 import BeautifulSoup
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/destinations-closing';OUT.mkdir(parents=True,exist_ok=True)
REF='528f726'
def old(path):return subprocess.check_output(['git','show',REF+':'+path],cwd=ROOT)
before=BeautifulSoup(old('public/index.html'),'html.parser');after=BeautifulSoup((ROOT/'public/index.html').read_text(),'html.parser')
assert str(before.select_one('.ss-region-gallery'))==str(after.select_one('.ss-region-gallery'))
before.select_one('.ss-station-index-v72').decompose();after.select_one('.ss-destinations-closing').decompose()
for soup in [before,after]:soup.select_one('link[href^="/home-system.css"]')['href']='/home-system.css'
assert [x for x in str(before).splitlines() if x.strip()]==[x for x in str(after).splitlines() if x.strip()],'Change outside closing banner'
for file in (ROOT/'public').rglob('*.html'):
 if file==ROOT/'public/index.html':continue
 assert old(str(file.relative_to(ROOT)))==file.read_bytes(),str(file)
for path in ['public/app.js','public/home-system.js','content/pages.json','content/stations.json','content/home-reservation.html']:
 assert old(path)==(ROOT/path).read_bytes(),path
copy=json.loads((ROOT/'content/destinations-closing.json').read_text())
R={'reference':REF,'scope':'PASS: other home HTML, four featured cards, other pages, editorial sources, wizard and JS unchanged','viewports':[],'page_errors':[],'accessibility':[]}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(reduced_motion='reduce')
 page.on('pageerror',lambda e:R['page_errors'].append(str(e)))
 for width,height in [(1440,900),(1280,800),(1024,768),(768,1024),(390,844),(375,812)]:
  page.set_viewport_size({'width':width,'height':height});page.goto('http://localhost:3000/',wait_until='networkidle')
  page.add_style_tag(content='html{scroll-behavior:auto!important}')
  area=page.locator('.ss-destinations-closing');cta=area.locator('a')
  for field in ['eyebrow','title','description','cta']:assert area.get_by_text(copy[field],exact=True).count()==1
  assert cta.get_attribute('href')==copy['href']
  assert page.locator('.ss-station-index-v72,.ss-station-count-v72,.ss-station-action-v72').count()==0
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  data=area.evaluate('''n=>{const r=x=>{let a=x.getBoundingClientRect();return{x:a.x,y:a.y,w:a.width,h:a.height,b:a.bottom}},i=n.firstElementChild,s=getComputedStyle(i),title=getComputedStyle(n.querySelector('h3'));return{outer:r(n),container:r(i),cta:r(n.querySelector('a')),padding:[s.paddingTop,s.paddingRight,s.paddingBottom,s.paddingLeft],background:getComputedStyle(n).backgroundColor,border:getComputedStyle(n).borderTopColor,title:{size:title.fontSize,weight:title.fontWeight,lineHeight:title.lineHeight}}}''')
  assert data['outer']['x']==0 and data['outer']['w']==width
  assert data['background']=='rgb(17, 19, 18)' and data['border']=='rgb(66, 71, 68)'
  assert data['container']['w']<=1320
  assert data['title']['weight']=='500'
  if width==1440:
   assert data['padding']==['64px','48px','80px','48px'] and data['title']['size']=='48px'
   assert data['cta']['w']<data['container']['w']/2
  if width<768:
   assert data['padding']==['48px','20px','48px','20px'] and data['title']['size']=='34px'
   assert abs(data['cta']['w']-(width-40))<1
  # Pixel proof of background and immediate transition to white Reviews.
  page.evaluate('scrollTo(0,0)');page.wait_for_timeout(100)
  clip=area.evaluate('n=>{let r=n.getBoundingClientRect(),y=Math.floor(r.top+scrollY);return{x:0,y,width:innerWidth,height:Math.ceil(r.bottom+scrollY)-y}}')
  path=OUT/f'after-{width}.png';page.screenshot(path=str(path),clip=clip,full_page=True,animations='disabled')
  im=Image.open(path).convert('RGB')
  for x in [0,width//2,width-1]:assert im.getpixel((x,12))==(17,19,18)
  edges=page.evaluate("()=>({end:document.querySelector('#destinations').getBoundingClientRect().bottom+scrollY,start:document.querySelector('#avis').getBoundingClientRect().top+scrollY})")
  assert abs(edges['end']-edges['start'])<.1
  if width in [1440,390]:
   page.screenshot(path=str(OUT/f'destinations-to-reviews-{width}.png'),clip={'x':0,'y':int(edges['start'])-100,'width':width,'height':200},full_page=True,animations='disabled')
  cta.focus();assert cta.evaluate('n=>getComputedStyle(n).outlineWidth')=='2px'
  if width in [1440,390]:
   page.add_script_tag(path='/tmp/ski-qa/node_modules/axe-core/axe.min.js')
   issues=page.evaluate("async()=> (await axe.run(document.querySelector('.ss-destinations-closing'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))")
   assert not issues,issues
   R['accessibility'].append({'width':width,'violations':issues})
  cta.press('Enter');page.wait_for_url('**/stations.html');assert page.locator('h1').count()==1
  R['viewports'].append({'width':width,'height':height,'geometry':data,'transition':edges,'copy':'PASS','CTA':'PASS: catalogue by keyboard','overflow':False})
 for width,height in [(1440,900),(390,844)]:
  page.set_viewport_size({'width':width,'height':height});page.goto('http://localhost:3012/',wait_until='networkidle');page.add_style_tag(content='html{scroll-behavior:auto!important}')
  page.locator('.ss-station-index-v72').screenshot(path=str(OUT/f'before-{width}.png'),animations='disabled')
 assert not R['page_errors']
 b.close()
(OUT/'results.json').write_text(json.dumps(R,ensure_ascii=False,indent=2))
print('PASS: six widths, exact approved banner copy, unchanged featured stations/other pages/wizard, exact dimensions, dark-to-white boundary, keyboard catalogue link and targeted axe.')
