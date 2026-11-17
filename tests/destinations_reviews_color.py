"""Real visual/DOM checks for the color-only Destinations → Reviews boundary."""
from pathlib import Path
import json,subprocess
from bs4 import BeautifulSoup
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/destinations-reviews-color';OUT.mkdir(parents=True,exist_ok=True)
REF='a7719d8'
def old(path):return subprocess.check_output(['git','show',REF+':'+path],cwd=ROOT)
before=BeautifulSoup(old('public/index.html'),'html.parser');after=BeautifulSoup((ROOT/'public/index.html').read_text(),'html.parser')
before.select_one('.ss-photo-transition--exit').decompose();after.select_one('.ss-destinations-to-reviews').decompose()
for soup in [before,after]:
 for node in soup.select('link[href^="/home-system.css"],link[href^="/booking-v3.css"]'):node['href']=node['href'].split('?')[0]
assert [l for l in str(before).splitlines() if l.strip()]==[l for l in str(after).splitlines() if l.strip()],'Change outside requested transition'
for file in (ROOT/'public').rglob('*.html'):
 if file==ROOT/'public/index.html':continue
 assert old(str(file.relative_to(ROOT)))==file.read_bytes(),str(file)
for path in ['public/home-system.js','public/app.js','content/pages.json','content/stations.json','content/home-reservation.html','content/destinations-closing.json']:
 assert old(path)==(ROOT/path).read_bytes(),path
R={'reference':REF,'scope':'PASS: all text, links, four featured destination cards, other transitions, reservation and other pages unchanged','viewports':[],'page_errors':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);page=browser.new_page(reduced_motion='reduce')
 page.on('pageerror',lambda e:R['page_errors'].append(str(e)))
 for width,height in [(1440,900),(1280,800),(1024,768),(768,1024),(390,844),(375,812)]:
  page.set_viewport_size({'width':width,'height':height});page.goto('http://localhost:3000/',wait_until='networkidle')
  page.add_style_tag(content='html{scroll-behavior:auto!important}')
  assert page.locator('.ss-photo-transition--exit').count()==0
  band=page.locator('.ss-destinations-to-reviews');assert band.count()==1
  assert band.locator('*').count()==0 and band.inner_text()==''
  geometry=page.evaluate('''()=>{const r=q=>{let n=document.querySelector(q),b=n.getBoundingClientRect(),s=getComputedStyle(n);return{top:b.top+scrollY,bottom:b.bottom+scrollY,x:b.x,width:b.width,height:b.height,background:s.backgroundColor,gradient:s.backgroundImage,filter:s.filter,before:getComputedStyle(n,'::before').content,after:getComputedStyle(n,'::after').content}},inner=document.querySelector('.ss-destinations-closing__inner');return{dest:r('#destinations'),band:r('.ss-destinations-to-reviews'),reviews:r('#avis'),faq:r('#questions'),cta:r('.ss-destinations-closing__cta'),paddingBottom:getComputedStyle(inner).paddingBottom}}''')
  g=geometry['band'];assert g['x']==0 and g['width']==width
  assert g['height']==(72 if width<=767 else 120)
  assert g['filter']=='none' and g['before']==g['after']=='none'
  assert 'rgb(51, 54, 52) 25%' in g['gradient'] and 'rgb(139, 141, 138) 55%' in g['gradient'] and 'rgb(217, 218, 215) 80%' in g['gradient']
  assert geometry['paddingBottom']==('40px' if width<=767 else '56px')
  assert abs(geometry['dest']['bottom']-geometry['cta']['bottom']-(40 if width<=767 else 56))<1
  assert abs(geometry['dest']['bottom']-g['top'])<.1
  assert abs(g['bottom']-geometry['reviews']['top'])<.1
  assert geometry['reviews']['background']==geometry['faq']['background']=='rgb(255, 255, 255)'
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  # Capture the CTA, all of the band, and the real beginning of Reviews together.
  page.evaluate('scrollTo(0,0)');page.wait_for_timeout(100)
  y=int(page.locator('.ss-destinations-closing').evaluate('n=>n.getBoundingClientRect().top+scrollY'))
  end=int(geometry['reviews']['top'])+(270 if width>=768 else 320)
  path=OUT/f'junction-{width}.png'
  page.screenshot(path=str(path),clip={'x':0,'y':y,'width':width,'height':end-y},full_page=True,animations='disabled')
  bitmap=Image.open(path).convert('RGB');band_y=g['top']-y
  # Every row must have the same color across the viewport: no photograph or side seam.
  samples=[]
  for dy in range(2,int(g['height'])-2):
   row=int(band_y+dy);colors=[bitmap.getpixel((x,row)) for x in [0,width//2,width-1]]
   assert all(max(c[i] for c in colors)-min(c[i] for c in colors)<=2 for i in range(3)),(width,dy,colors)
   if dy in [2,int(g['height']*.25),int(g['height']*.55),int(g['height']*.8),int(g['height'])-3]:samples.append({'offsetY':dy,'rgb':colors[0]})
  for x in [0,width//2,width-1]:
   assert bitmap.getpixel((x,int(band_y)-3))==(17,19,18)
   assert bitmap.getpixel((x,int(band_y+g['height'])+3))==(255,255,255)
  assert all(samples[i]['rgb'][0]<=samples[i+1]['rgb'][0] for i in range(len(samples)-1))
  if width in [1440,390]:
   page.screenshot(path=str(OUT/f'home-full-{width}.png'),full_page=True,animations='disabled')
  R['viewports'].append({'width':width,'height':height,'geometry':geometry,'pixels':samples,'overflow':False})
 assert not R['page_errors']
 browser.close()
(OUT/'results.json').write_text(json.dumps(R,ensure_ascii=False,indent=2))
print('PASS: six widths; no exit photo, overlay, pseudo-element, text or blur; exact 120/72px gradient; padding 56/40px; full-width pixels; contiguous boundaries; unchanged copy/links/cards/form and other pages.')
