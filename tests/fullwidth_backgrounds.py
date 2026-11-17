"""Verify real painted pixels at both edges and center, not just CSS declarations."""
from pathlib import Path
import subprocess,json
from bs4 import BeautifulSoup
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/fullwidth-fix';OUT.mkdir(exist_ok=True,parents=True)
REF='bf42dea'
def old(path):return subprocess.check_output(['git','show',REF+':'+path],cwd=ROOT)
before=BeautifulSoup(old('public/index.html'),'html.parser');after=BeautifulSoup((ROOT/'public/index.html').read_text(),'html.parser')
for soup in [before,after]:
 # Later approved replacement of the destination closing banner is independently tested.
 for node in soup.select('.ss-station-index-v72,.ss-destinations-closing'):node.decompose()
 for node in soup.select('.ss-fullwidth,.ss-container'):
  node['class']=[c for c in node['class'] if c not in ['ss-fullwidth','ss-container']]
 for link in soup.select('link[href^="/home-system.css"]'):link['href']='/home-system.css'
assert str(before)==str(after),'DOM change beyond wrapper/container classes and CSS revision'
for path in ['public/app.js','public/home-system.js','content/home-reservation.html','content/pages.json','content/stations.json']:
 assert old(path)==(ROOT/path).read_bytes(),path
for file in (ROOT/'public').rglob('*.html'):
 if file==ROOT/'public/index.html':continue
 assert old(str(file.relative_to(ROOT)))==file.read_bytes(),str(file)
R={'reference':REF,'scope':'PASS: wrapper classes/CSS only, reservation, text, photographs and JS identical','viewports':[],'page_errors':[]}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=b.new_page(reduced_motion='reduce')
 page.on('pageerror',lambda e:R['page_errors'].append(str(e)))
 for width,height in [(1920,1080),(1536,960),(1440,900),(1280,800),(1024,768),(768,1024),(390,844),(375,812)]:
  page.set_viewport_size({'width':width,'height':height});page.goto('http://localhost:3000/',wait_until='networkidle')
  page.add_style_tag(content='html{scroll-behavior:auto!important}')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  # Captures are genuine page renders. No masks, color injection, or hidden UI.
  page.evaluate('scrollTo(0,0)');page.wait_for_timeout(100)
  shot=OUT/f'home-full-{width}.png';page.screenshot(path=str(shot),full_page=True,animations='disabled')
  bitmap=Image.open(shot).convert('RGB')
  samples=[]
  for sid,color in [('#destinations',(17,19,18)),('#avis',(255,255,255)),('#questions',(255,255,255)),('#contact',(17,19,18)),('.art-footer',(17,19,18))]:
   data=page.locator(sid).evaluate('''n=>{let s=getComputedStyle(n),r=n.getBoundingClientRect(),i=n.querySelector(':scope>.ss-container'),q=i.getBoundingClientRect();return {x:r.x,y:r.top+scrollY,b:r.bottom+scrollY,width:r.width,maxWidth:s.maxWidth,color:s.backgroundColor,paddingLeft:s.paddingLeft,paddingRight:s.paddingRight,inner:{x:q.x,width:q.width,maxWidth:getComputedStyle(i).maxWidth,background:getComputedStyle(i).backgroundColor},before:getComputedStyle(n,'::before').content,after:getComputedStyle(n,'::after').content}}''')
   assert abs(data['x'])<.1 and abs(data['width']-width)<.1 and data['maxWidth']=='none'
   assert data['paddingLeft']==data['paddingRight']=='0px'
   assert data['inner']['width']<=1320 and data['inner']['background']=='rgba(0, 0, 0, 0)'
   assert data['before']==data['after']=='none'
   y=int(data['y'])+12
   points=[]
   for x in [0,width//2,width-1]:
    actual=bitmap.getpixel((x,y));assert actual==color,(sid,width,x,y,actual,color)
    points.append({'x':x,'y':y,'rgb':actual})
   samples.append({'section':sid,'computed':data,'pixels':points})
  boundaries=[]
  for left,right,above,below in [('.ss-home-courses','#destinations',(247,246,242),(17,19,18)),('#destinations','#avis',(17,19,18),(255,255,255)),('#questions','#contact',(255,255,255),(17,19,18))]:
   edges=page.evaluate('''([a,b])=>{let x=document.querySelector(a).getBoundingClientRect(),y=document.querySelector(b).getBoundingClientRect();return {end:x.bottom+scrollY,start:y.top+scrollY}}''',[left,right])
   assert abs(edges['end']-edges['start'])<.1
   boundary=int(edges['start']);checks=[]
   for x in [0,width//2,width-1]:
    for dy,expected in [(-6,above),(6,below)]:
     pixel=bitmap.getpixel((x,boundary+dy));assert pixel==expected,(left,right,width,x,dy,pixel,expected)
     checks.append({'x':x,'y':boundary+dy,'rgb':pixel})
   boundaries.append({'from':left,'to':right,'positions':edges,'pixels':checks})
   if width in [1440,390]:
    key={'#destinations':'formats-destinations','#avis':'destinations-avis','#contact':'faq-reservation'}[right]
    bitmap.crop((0,boundary-90,width,boundary+160)).save(OUT/f'{key}-{width}.png')
  # No physical gap between reservation, photographic pre-footer, and functional footer.
  for a,c in [('#contact','.art-prefooter'),('.art-prefooter','.art-footer')]:
   assert abs(page.locator(a).evaluate('n=>n.getBoundingClientRect().bottom')-page.locator(c).evaluate('n=>n.getBoundingClientRect().top'))<.1
  R['viewports'].append({'width':width,'height':height,'samples':samples,'boundaries':boundaries,'overflow':False})
 assert not R['page_errors']
 b.close()
(OUT/'results.json').write_text(json.dumps(R,ensure_ascii=False,indent=2))
# Annotation is a separate evidence sheet; the original full-page captures are unmodified.
im=Image.open(OUT/'home-full-1440.png').convert('RGB');draw=ImageDraw.Draw(im)
for sample in next(v for v in R['viewports'] if v['width']==1440)['samples']:
 for p in sample['pixels']:
  x,y=p['x'],p['y'];draw.ellipse((max(0,x-5),y-5,min(1439,x+5),y+5),fill='#e33e32')
 draw.text((20,sample['pixels'][0]['y']+15),sample['section']+' — x=0 / 720 / 1439',fill='#e33e32',stroke_width=1)
im.save(OUT/'pixel-evidence-1440.png')
print('PASS: eight widths, actual full-page pixels at left/center/right, three exact boundaries, unlimited outer wrappers, unchanged content/form/JS and other pages.')
