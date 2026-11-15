"""Compare original components with the approved-copy integration, not pixel-identical text."""
from pathlib import Path
import json,os
from playwright.sync_api import sync_playwright,TimeoutError as BrowserTimeout
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/editorial-integration/visual';OUT.mkdir(parents=True,exist_ok=True)
paths=['index.html','manifesto.html','offres/ski-prive.html','offres/performance-technique.html','offres/freeride-decouverte.html','offres/snowboard.html','stations.html','offres/index.html']
selected_paths=os.environ.get('ONLY_PATHS','').split(',') if os.environ.get('ONLY_PATHS') else paths
selected_versions=os.environ.get('ONLY_VERSION','').split(',') if os.environ.get('ONLY_VERSION') else ['main-bc9bb78','new-copy']
records=[r for r in json.loads((OUT/'captures.json').read_text()) if r['path'] not in selected_paths or r['version'] not in selected_versions] if (OUT/'captures.json').exists() else []
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for path in paths:
  if path not in selected_paths:continue
  for width in [1440,390]:
   for version,port in [('main-bc9bb78',3004),('new-copy',3000)]:
    if version not in selected_versions:continue
    page=b.new_page(viewport={'width':width,'height':1000},reduced_motion='reduce',locale='fr-FR')
    failed=[];page.on('requestfailed',lambda r:failed.append({'url':r.url,'error':r.failure}))
    page.goto(f'http://localhost:{port}/{path}',wait_until='networkidle')
    page.add_style_tag(content='*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}')
    height=page.locator('main').evaluate('(e)=>e.offsetHeight')
    page.evaluate("async h=>{for(let y=0;y<h;y+=700){scrollTo(0,y);await new Promise(r=>setTimeout(r,20))}scrollTo(0,0)}",height)
    try:page.wait_for_function("Array.from(document.querySelectorAll('main img')).every(i=>i.complete)",timeout=5000)
    except BrowserTimeout:failed.append({'url':'lazy images','error':'Some images remain pending; captured without substitution.'})
    name=version+'-'+path.replace('/','-').replace('.html','')+'-'+str(width)+'.png'
    page.locator('main').screenshot(path=str(OUT/name),animations='disabled')
    record={'version':version,'path':path,'width':width,'capture':name,'failed_requests':failed,'height':height,
      'overflow':page.evaluate('document.documentElement.scrollWidth>innerWidth'),
      'photos':page.locator('main img').evaluate_all("(nodes)=>nodes.map(i=>({url:i.currentSrc,loaded:i.complete&&i.naturalWidth>0,fit:getComputedStyle(i).objectFit,position:getComputedStyle(i).objectPosition}))")}
    records.append(record)
    if path=='index.html' and version=='new-copy':
     for part in ['art-prefooter','art-footer']:
      page.locator('.'+part+(','+('.review-prefooter' if part=='art-prefooter' else '.review-footer'))).screenshot(path=str(OUT/f'{part}-{width}.png'),animations='disabled')
    if path=='index.html':
     # Capture the live reference chapter tones at each heading, not a forced page-wide theme.
     for sid in ['offres','formules','avis']:
      page.locator('#'+sid).scroll_into_view_if_needed()
      page.evaluate("(sid)=>{let h=document.querySelector('#'+sid+' h2');scrollTo(0,h.getBoundingClientRect().top+scrollY-150)}",sid)
      page.wait_for_timeout(100)
      page.locator('#'+sid).screenshot(path=str(OUT/f'{version}-{sid}-{width}.png'),animations='disabled')
    page.close()
 b.close()
(OUT/'captures.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
html='<h1>Design bc9bb78 / nouveaux textes validés</h1><p>Les différences de texte sont voulues. Les photographies et feuilles de style de référence sont conservées. Les ressources externes refusées par le proxy ne sont pas remplacées ; elles sont listées dans captures.json.</p>'
for path in paths:
 for width in [1440,390]:
  html+=f'<section><h2>{path} / {width} px</h2><div class="pair">'
  for row in [r for r in records if r['path']==path and r['width']==width]:
   html+=f'<article><h3>{row["version"]}</h3><a href="{row["capture"]}">Capture complète</a><div class="frame"><img src="{row["capture"]}" loading="lazy" alt="{row["version"]} {path}"></div></article>'
  html+='</div></section>'
for sid in ['offres','formules','avis']:
 for width in [1440,390]:
  html+=f'<section><h2>Home — {sid} en cours de navigation / {width} px</h2><div class="pair">'
  for version in ['main-bc9bb78','new-copy']:
   filename=f'{version}-{sid}-{width}.png'
   html+=f'<article><h3>{version}</h3><a href="{filename}"><img src="{filename}" loading="lazy" alt="{sid}"></a></article>'
  html+='</div></section>'
html+='<section><h2>Nouveau footer — exception graphique</h2><div class="pair">'
for width in [1440,390]:
 for part in ['art-prefooter','art-footer']:
  html+=f'<article><h3>{part} / {width} px</h3><a href="{part}-{width}.png"><img src="{part}-{width}.png" loading="lazy" alt="{part}"></a></article>'
html+='</div></section>'
(OUT/'index.html').write_text('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Ski Society — design et contenu</title><style>body{font:16px/1.6 Arial;padding:25px;background:#eff2ee;color:#15271e}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}article{min-width:0;background:white;padding:20px}.frame{max-height:750px;overflow:auto;margin-top:20px}img{display:block;width:100%}section{margin:45px 0}@media(max-width:700px){body{padding:12px}.pair{grid-template-columns:1fr}}</style></head><body>'+html+'</body></html>')
assert not any(r['overflow'] for r in records)
print('PASS: 32 page captures, 12 live-chapter captures and 4 footer captures; no horizontal overflow.')
