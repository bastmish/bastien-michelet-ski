"""Home/footer review gate. Exit 2 means required photo validation is blocked."""
from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/home-review';OUT.mkdir(exist_ok=True,parents=True)
report={'scope':'home and proposed footer only','viewports':[],'errors':[],'failed_requests':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(reduced_motion='reduce')
 page.on('pageerror',lambda e:report['errors'].append(str(e)))
 page.on('requestfailed',lambda r:report['failed_requests'].append({'url':r.url,'failure':r.failure}))
 for width in [375,768,1440]:
  page.set_viewport_size({'width':width,'height':1000})
  page.goto('http://localhost:3000/',wait_until='networkidle')
  page.add_style_tag(content='*{animation:none!important;transition:none!important;scroll-behavior:auto!important}')
  assert page.locator('h1').count()==1
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  ids=page.locator('[data-editorial-section]').evaluate_all('(nodes)=>[...new Set(nodes.map(n=>n.dataset.editorialSection))]')
  assert sorted(ids)==['a01','a02','a03','a04','a05','a06','a07','a08']
  assert page.locator('#offres .ss-offer-card').count()==4
  assert page.locator('#adn .ss-adn-photo-card').count()==3
  assert page.locator('#formules .ss-programme-v72').count()==3
  assert page.locator('#formules .home-review-times li').count()==3
  assert page.locator('#questions details').count()==6
  assert page.locator('.review-prefooter').count()==1 and page.locator('.review-footer').count()==1
  boxes=page.locator('#adn .ss-adn-photo-card').evaluate_all('(nodes)=>nodes.map(n=>({width:n.offsetWidth,height:n.offsetHeight}))')
  assert boxes[0]['height']!=boxes[1]['height'],'ADN must not be three identical panels'
  for sid,dark in [('offres',True),('formules',True),('avis',False)]:
   page.evaluate("(sid)=>{let h=document.querySelector('#'+sid+' h2');scrollTo(0,h.getBoundingClientRect().top+scrollY-150)}",sid)
   page.wait_for_timeout(80)
   assert page.evaluate("document.body.classList.contains('ski-dark-mode')")==dark
  page.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=650){scrollTo(0,y);await new Promise(r=>setTimeout(r,30))}scrollTo(0,0)}")
  page.wait_for_timeout(200)
  photos=page.locator('img').evaluate_all('(nodes)=>nodes.map(i=>({url:i.currentSrc,loaded:i.complete&&i.naturalWidth>0}))')
  report['viewports'].append({'width':width,'geometry':'PASS','chapters':'PASS','adn_panels':boxes,'photos':photos})
  if width in [375,1440]:
   page.screenshot(path=str(OUT/f'provisional-home-{width}.png'),full_page=True)
   for part in ['review-prefooter','review-footer']:
    page.locator('.'+part).screenshot(path=str(OUT/f'provisional-{part}-{width}.png'))
 page.set_viewport_size({'width':375,'height':1000})
 page.goto('http://localhost:3000/',wait_until='networkidle')
 page.locator('.nav-toggle').click();assert page.locator('.nav-toggle').get_attribute('aria-expanded')=='true'
 page.keyboard.press('Escape');assert page.locator('.nav-toggle').get_attribute('aria-expanded')=='false'
 page.locator('#questions summary').first.click();assert page.locator('#questions details').first.evaluate('(e)=>e.open')
 page.locator('select[name="experience"]').select_option('Freeride & milieu alpin')
 page.wait_for_function("document.querySelector('select[name=format]').options[1].disabled")
 page.add_script_tag(path='/tmp/ski-qa/node_modules/axe-core/axe.min.js')
 footer_issues=page.evaluate("async()=> (await axe.run(document.querySelector('.review-footer'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>v.id)")
 assert not footer_issues
 report['new_footer_accessibility']=footer_issues
 assert not report['errors']
 browser.close()
report['structural_and_functional']='PASS'
report['required_photographic_validation']='PASS' if all(i['loaded'] for v in report['viewports'] for i in v['photos']) else 'BLOCKED'
(OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('Structural, content, responsive, chapter, menu, FAQ, freeride and footer checks: PASS.')
print('Required photographic validation:',report['required_photographic_validation'])
sys.exit(0 if report['required_photographic_validation']=='PASS' else 2)
