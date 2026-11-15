"""Check restored behavior and extensions; report baseline accessibility issues unchanged."""
import json,os
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
originals=[p['path'] for p in json.loads((ROOT/'content/pages.json').read_text())]+['stations.html','offres/index.html']
paths=originals+['destinations.html']+[s['URL'].lstrip('/') for s in json.loads((ROOT/'content/stations.json').read_text())]
issues=[];errors=[];footer_issues=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page()
 page.on('pageerror',lambda e:errors.append(str(e)))
 for path in paths:
  for width in [375,768,1440]:
   page.set_viewport_size({'width':width,'height':900})
   response=page.goto('http://localhost:3000/'+path,wait_until='load')
   page.evaluate('document.fonts.ready.then(()=>true)')
   assert response.status==200 and page.locator('h1').count()==1,path
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(path,width)
  page.add_script_tag(path=os.environ['AXE_SCRIPT'])
  results=page.evaluate("async()=> (await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)}))")
  if results:issues.append({'path':path,'original_page':path in originals,'issues':results})
  bad_footer=page.evaluate("async()=> (await axe.run(document.querySelector('.art-footer,.review-footer'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>v.id)")
  if bad_footer:footer_issues.append({'path':path,'issues':bad_footer})
 page.set_viewport_size({'width':390,'height':900})
 page.goto('http://localhost:3000/',wait_until='networkidle')
 page.locator('.nav-toggle').click();assert page.locator('.nav-toggle').get_attribute('aria-expanded')=='true'
 page.keyboard.press('Escape');assert page.locator('.nav-toggle').get_attribute('aria-expanded')=='false'
 assert page.locator('#ski-request-form').is_visible()
 page.locator('#questions summary').first.click()
 assert page.locator('#questions details').first.evaluate('(e)=>e.open')
 page.goto('http://localhost:3000/stations.html',wait_until='networkidle')
 page.locator('#station-search').fill('Meribel')
 page.locator('#station-search').press('ArrowDown');page.locator('#station-search').press('Enter')
 page.wait_for_url('**/stations/meribel.html')
 page.goto('http://localhost:3000/destinations.html',wait_until='networkidle')
 page.locator('#station-search').fill('Meribel')
 page.locator('#station-search').press('ArrowDown');page.locator('#station-search').press('Enter')
 page.wait_for_url('**/stations/meribel.html')
 assert 'Méribel' in page.locator('h1').inner_text()
 assert 'wa.me/33763532601?text=' in page.locator('.detail-inner a[href*="wa.me"]').first.get_attribute('href')
 browser.close()
report={'pages':len(paths),'viewports':[375,768,1440],'page_errors':errors,'accessibility_observations':issues,'new_footer_violations':footer_issues,'reference_navigation_approved_faq_and_catalogue':'PASS','extension_search_and_whatsapp':'PASS (no message sent)'}
Path('/tmp/ski-browser-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
assert not errors and not footer_issues
