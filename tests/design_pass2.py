"""Capture the actual pass-1/pass-2 composition; do not substitute blocked images."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'docs/visual-pass2';out.mkdir(parents=True,exist_ok=True)
records=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for name,port in [('before',3003),('after',3000)]:
  for path in ['index.html','manifesto.html','stations/courchevel.html']:
   for width in [1440,390]:
    page=browser.new_page(viewport={'width':width,'height':1000})
    failed=[]
    page.on('requestfailed',lambda r:failed.append({'url':r.url,'error':r.failure}))
    page.goto(f'http://localhost:{port}/{path}',wait_until='networkidle')
    page.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=700){scrollTo(0,y);await new Promise(r=>setTimeout(r,25))}scrollTo(0,0)}")
    page.wait_for_timeout(250)
    filename=f'{name}-{path.replace("/","-").replace(".html","")}-{width}.png'
    page.screenshot(path=str(out/filename),full_page=True)
    info=page.evaluate("({height:document.body.scrollHeight,overflow:document.documentElement.scrollWidth>innerWidth,images:[...document.images].map(i=>({url:i.currentSrc,loaded:i.complete&&i.naturalWidth>0}))})")
    records.append({'version':name,'path':path,'width':width,'screenshot':filename,'failed_requests':failed,**info})
    if name=='after' and path=='index.html':
     for part in ['art-prefooter','art-footer']:
      page.locator('.'+part).screenshot(path=str(out/f'{part}-{width}.png'))
     # Expanded programmes and enquiry form also get checked for usable flow.
     page.locator('.art-formats-disclosure > summary').click()
     page.locator('.art-request-disclosure > summary').click()
     assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
     page.locator('.art-formats-disclosure').screenshot(path=str(out/f'formats-open-{width}.png'))
    page.close()
 for width in [1440,390]:
  page=browser.new_page(viewport={'width':width,'height':1000})
  page.goto('http://localhost:3000/questions.html',wait_until='networkidle')
  page.locator('.ss-questions-list summary').first.click()
  page.screenshot(path=str(out/f'faq-{width}.png'),full_page=True)
  page.close()
 browser.close()
(out/'captures.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
html='<h1>Deuxième passe design — avant / après</h1><p>Avant : branche au commit 5a9cc1f. Après : deuxième passe. Captures réelles, sans substitution des ressources externes refusées par le proxy. Les photos et polices absentes empêchent une validation complète.</p>'
for path in ['index.html','manifesto.html','stations/courchevel.html']:
 for width in [1440,390]:
  pair=[r for r in records if r['path']==path and r['width']==width]
  html+=f'<section><h2>{path} / {width} px</h2><div class="pair">'
  for r in pair:
   html+=f'<article><h3>{r["version"]} — hauteur {r["height"]} px</h3><a href="{r["screenshot"]}">Ouvrir la capture complète</a><div class="frame"><img src="{r["screenshot"]}" loading="lazy" alt="Capture {r["version"]} {path}"></div></article>'
  html+='</div></section>'
html+='<section><h2>Footer et contenus repliés</h2><div class="pair">'
for width in [1440,390]:
 for part in ['art-prefooter','art-footer','formats-open','faq']:
  html+=f'<article><h3>{part} / {width} px</h3><a href="{part}-{width}.png"><img src="{part}-{width}.png" loading="lazy" alt="{part}"></a></article>'
html+='</div></section>'
(out/'index.html').write_text('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Ski Society — Design pass 2</title><style>body{font:16px/1.6 Arial;background:#eef1ed;color:#15271f;margin:0;padding:30px}h1{font-size:34px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:25px}article{padding:20px;background:white;min-width:0}.frame{max-height:780px;overflow:auto;margin-top:20px}img{width:100%;display:block}section{margin:50px 0}@media(max-width:700px){body{padding:15px}.pair{grid-template-columns:1fr}}</style></head><body>'+html+'</body></html>')
print('Saved 20 screenshots and six before/after comparisons.')
print([(r['width'],r['version'],r['height']) for r in records if r['path']=='index.html'])
