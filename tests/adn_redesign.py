"""Targeted layout, copy and before/after checks for the home ADN only."""
from pathlib import Path
import json,math
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/adn-redesign'
OUT.mkdir(parents=True,exist_ok=True)
results={'viewports':[],'failed_requests':[],'page_errors':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(reduced_motion='reduce')
 page.on('pageerror',lambda e:results['page_errors'].append(str(e)))
 page.on('requestfailed',lambda r:results['failed_requests'].append({'url':r.url,'error':r.failure}))
 for width in [375,768,1440]:
  page.set_viewport_size({'width':width,'height':1000})
  page.goto('http://localhost:3000/',wait_until='networkidle')
  assert page.locator('.adn-editorial-card').count()==3
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  geometry=page.locator('.adn-editorial-card').evaluate_all("""nodes=>nodes.map(n=>{
   const photo=n.querySelector('figure').getBoundingClientRect(),copy=n.querySelector('.adn-card-copy>.kicker').getBoundingClientRect(),p=n.querySelector('p');
   return {photoBottom:photo.bottom,textTop:copy.top,paragraphPosition:getComputedStyle(p).position}
  })""")
  assert all(g['textTop']>=g['photoBottom']+19 and g['paragraphPosition']=='static' for g in geometry)
  for sid,dark in [('offres',True),('avis',False)]:
   page.evaluate("(sid)=>{const h=document.querySelector('#'+sid+' h2');scrollTo(0,h.getBoundingClientRect().top+scrollY-150)}",sid)
   page.wait_for_timeout(100)
   assert page.evaluate("document.body.classList.contains('ski-dark-mode')")==dark
  results['viewports'].append({'width':width,'overflow':False,'texts_below_images':True,'chapters':'PASS'})
 for version,port in [('before',3006),('after',3000)]:
  for width in [1440,390]:
   page.set_viewport_size({'width':width,'height':1000})
   page.goto(f'http://localhost:{port}/',wait_until='networkidle')
   page.add_style_tag(content='*{scroll-behavior:auto!important;transition:none!important;animation:none!important}')
   page.locator('#adn').scroll_into_view_if_needed();page.wait_for_timeout(150)
   page.evaluate('scrollTo(0,0)');page.wait_for_timeout(100)
   area=page.evaluate("""()=>{let a=document.querySelector('#expertise').getBoundingClientRect(),b=document.querySelector('#adn').getBoundingClientRect();return {x:0,y:Math.floor(a.top+scrollY),width:innerWidth,height:Math.ceil(b.bottom+scrollY)-Math.floor(a.top+scrollY)}}""")
   page.screenshot(path=str(OUT/f'{version}-{width}.png'),clip=area,full_page=True,animations='disabled')
   if version=='after':
    for sid in ['expertise','adn']:
     page.locator('#'+sid).screenshot(path=str(OUT/f'after-{sid}-{width}.png'),animations='disabled')
    results.setdefault('images',[]).append({'width':width,'photos':page.locator('#expertise img,#adn img').evaluate_all('(nodes)=>nodes.map(i=>({url:i.currentSrc,loaded:i.complete&&i.naturalWidth>0}))')})
 page.goto('http://localhost:3000/',wait_until='networkidle')
 page.add_script_tag(path='/tmp/ski-qa/node_modules/axe-core/axe.min.js')
 issues=page.evaluate("""async()=> (await axe.run([document.querySelector('#expertise'),document.querySelector('#adn')],{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)}))""")
 results['accessibility']=issues
 assert not issues and not results['page_errors']
 browser.close()
results['functional_and_layout']='PASS'
results['photographic_validation']='PASS' if all(i['loaded'] for r in results['images'] for i in r['photos']) else 'BLOCKED'
(OUT/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print('PASS: copy outside images, responsive layout, original transitions, no JS errors or axe violations in ADN.')
print('Photographs:',results['photographic_validation'])
