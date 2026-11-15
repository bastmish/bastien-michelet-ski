"""Run with Python Playwright and AXE_SCRIPT pointing to a trusted axe-core install."""
import json,os
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
paths=[p['path'] for p in json.loads((root/'content/pages.json').read_text())]+['stations.html']+[s['URL'].lstrip('/') for s in json.loads((root/'content/stations.json').read_text())]
results=[];violations=[];console=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 page=browser.new_page()
 page.on('pageerror',lambda e:console.append(str(e)))
 for path in paths:
  for width in [375,768,1440]:
   page.set_viewport_size({'width':width,'height':900})
   response=page.goto('http://localhost:3000/'+path,wait_until='networkidle')
   assert response.status==200,(path,response.status)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(path,width,'overflow')
   assert page.locator('h1').count()==1
  page.add_script_tag(path=os.environ['AXE_SCRIPT'])
  issues=page.evaluate("""async()=> (await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)}))""")
  if issues:violations.append({'path':path,'issues':issues})
  results.append(path)
 page.set_viewport_size({'width':375,'height':850})
 page.goto('http://localhost:3000/')
 page.locator('.nav-toggle').click()
 assert page.locator('.nav-toggle').get_attribute('aria-expanded')=='true'
 page.keyboard.press('Escape')
 assert page.locator('.nav-toggle').get_attribute('aria-expanded')=='false'
 page.goto('http://localhost:3000/stations.html')
 page.locator('#station-search').fill('Meribel')
 page.locator('#station-search').press('ArrowDown')
 page.locator('#station-search').press('Enter')
 page.wait_for_url('**/stations/meribel.html')
 assert 'Méribel' in page.locator('h1').inner_text()
 # Inspect WhatsApp href without sending a message.
 assert 'wa.me/33763532601?text=' in page.locator('.ss-copy a').first.get_attribute('href')
 page.screenshot(path='/tmp/ski-mobile.png',full_page=True)
 browser.close()
report={'pages':len(results),'viewports':[375,768,1440],'axe_violations':violations,'page_errors':console,'navigation':'PASS','station_keyboard_search':'PASS','whatsapp_href':'PASS (no message sent)'}
Path('/tmp/ski-browser-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
assert not violations and not console
