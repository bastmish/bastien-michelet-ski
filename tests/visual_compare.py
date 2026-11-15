"""Capture actual reference/rejected/corrected renders, with resource failures recorded."""
from pathlib import Path
import json,os
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'docs/visual';out.mkdir(parents=True,exist_ok=True)
targets={'reference':(3001,['index.html','manifesto.html','offres/ski-prive.html','stations.html']),'rejected':(3002,['index.html']),'corrected':(3000,['index.html','manifesto.html','offres/ski-prive.html','stations.html','stations/courchevel.html'])}
capture_versions=os.environ.get('CAPTURE_VERSIONS','').split(',') if os.environ.get('CAPTURE_VERSIONS') else list(targets)
report=[r for r in json.loads((out/'captures.json').read_text()) if r['version'] not in capture_versions or (os.environ.get('CAPTURE_PATHS') and r['path'] not in os.environ['CAPTURE_PATHS'].split(','))] if (out/'captures.json').exists() else []
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for label,(port,paths) in targets.items():
  if label not in capture_versions:continue
  for path in paths:
   if os.environ.get('CAPTURE_PATHS') and path not in os.environ['CAPTURE_PATHS'].split(','):continue
   for width in [1440,390]:
    page=browser.new_page(viewport={'width':width,'height':1000},device_scale_factor=1)
    failed=[]
    page.on('requestfailed',lambda r:failed.append({'url':r.url,'error':r.failure}))
    page.goto(f'http://localhost:{port}/{path}',wait_until='networkidle',timeout=30000)
    # Reveal lazy photos and in-view animations as a visitor scrolls.
    page.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=700){scrollTo(0,y);await new Promise(r=>setTimeout(r,30))}scrollTo(0,0)}")
    page.wait_for_timeout(300)
    name=label+'-'+path.replace('/','-').replace('.html','')+'-'+str(width)+'.png'
    page.screenshot(path=str(out/name),full_page=True)
    metrics=page.evaluate("({overflow:document.documentElement.scrollWidth>innerWidth,images:[...document.images].map(i=>({url:i.currentSrc,loaded:i.complete&&i.naturalWidth>0}))})")
    report.append({'version':label,'path':path,'width':width,'capture':name,'failed_requests':failed,**metrics})
    page.close()
 browser.close()
(out/'captures.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
rows=[]
for r in report:
 rows.append(f'<article><h2>{r["version"]} — {r["path"]} — {r["width"]} px</h2><a href="{r["capture"]}"><img src="{r["capture"]}" loading="lazy"></a></article>')
(out/'index.html').write_text('<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><title>Comparaison visuelle Ski Society</title><style>body{font:16px Arial;background:#eee;padding:30px}main{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}img{width:100%}article{background:white;padding:18px}h2{font-size:17px}@media(max-width:800px){main{grid-template-columns:1fr}}</style><h1>Référence main / proposition rejetée / intégration corrigée</h1><p>Captures réelles. Les ressources externes bloquées par le proxy sont consignées dans captures.json ; les images absentes ne sont pas simulées.</p><main>'+''.join(rows)+'</main></html>')
print('Saved',len(report),'captures; image failures:',sum(not i['loaded'] for r in report for i in r['images']))
