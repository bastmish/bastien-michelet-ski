"""Compare real renders before the footer; freeze motion equally, never substitute assets."""
from pathlib import Path
import json,hashlib,math,os
from PIL import Image,ImageChops
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/restoration';OUT.mkdir(parents=True,exist_ok=True)
paths=['index.html','manifesto.html','offres/ski-prive.html','offres/performance-technique.html','offres/freeride-decouverte.html','offres/snowboard.html','stations.html']
selected=os.environ.get('ONLY_PAGES','').split(',') if os.environ.get('ONLY_PAGES') else paths
report=[r for r in json.loads((OUT/'comparison.json').read_text()) if r['path'] not in selected] if os.environ.get('ONLY_PAGES') and (OUT/'comparison.json').exists() else []
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for path in paths:
  if path not in selected:continue
  for width in [1440,390]:
   pair=[]
   for label,port in [('original',3004),('restored',3000)]:
    page=browser.new_page(viewport={'width':width,'height':1000},reduced_motion='reduce',locale='fr-FR',timezone_id='Europe/Zurich')
    failed=[];page.on('requestfailed',lambda r:failed.append({'url':r.url,'error':r.failure}))
    page.goto(f'http://localhost:{port}/{path}',wait_until='networkidle')
    page.add_style_tag(content='*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}')
    # Scroll at the same absolute offsets through the main, independently of footer height.
    height=page.locator('main').evaluate('(e)=>e.offsetTop+e.offsetHeight')
    page.evaluate("async h=>{for(let y=0;y<h;y+=650){scrollTo(0,y);await new Promise(r=>setTimeout(r,25))}scrollTo(0,0)}",height)
    page.wait_for_function("Array.from(document.querySelectorAll('main img')).every(i=>i.complete)",timeout=20000)
    page.evaluate('document.fonts.ready.then(()=>true)')
    page.wait_for_timeout(100)
    filename=f'{label}-{path.replace("/","-").replace(".html","")}-{width}.png'
    bounds=page.locator('main').bounding_box()
    # Stay strictly inside main: a ceil-rounded element screenshot can include
    # one subpixel row of the deliberately different footer.
    clip={'x':math.ceil(bounds['x']),'y':math.ceil(bounds['y']),'width':math.floor(bounds['width']),'height':math.floor(bounds['y']+bounds['height'])-math.ceil(bounds['y'])}
    page.screenshot(path=str(OUT/filename),clip=clip,full_page=True,animations='disabled')
    pair.append(filename)
    if label=='restored' and path=='index.html':
     page.locator('.art-prefooter').screenshot(path=str(OUT/f'prefooter-{width}.png'),animations='disabled')
     page.locator('.art-footer').screenshot(path=str(OUT/f'footer-{width}.png'),animations='disabled')
    images=page.evaluate("()=>[...document.querySelectorAll('main img')].map(i=>({url:i.currentSrc,loaded:i.complete&&i.naturalWidth>0}))")
    report.append({'path':path,'width':width,'version':label,'screenshot':filename,'failed_requests':failed,'images':images})
    page.close()
   a,b=(Image.open(OUT/f).convert('RGB') for f in pair)
   equal=a.size==b.size and ImageChops.difference(a,b).getbbox() is None
   row={'path':path,'width':width,'original_size':a.size,'restored_size':b.size,'identical_pixels':equal,'original':pair[0],'restored':pair[1]}
   if equal:(OUT/f'diff-{path.replace("/","-")}-{width}.png').unlink(missing_ok=True)
   if a.size==b.size and not equal:
    diff=ImageChops.difference(a,b)
    row['different_pixels']=sum(pixel!=(0,0,0) for pixel in diff.getdata())
    diff.save(OUT/f'diff-{path.replace("/","-")}-{width}.png')
   report.append(row)
   print(row,flush=True)
 browser.close()
(OUT/'comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
comparisons=sorted([r for r in report if 'identical_pixels' in r],key=lambda r:(paths.index(r['path']),-r['width']))
html='<h1>Restauration de bc9bb78 — comparaison hors footer</h1><p>Les captures de main excluent les footers. Mouvement réduit et animations figées identiquement des deux côtés pour comparer les pixels. Aucune image distante n’est remplacée. Les chargements refusés par le proxy sont enregistrés dans comparison.json.</p>'
for r in comparisons:
 html+=f'<section><h2>{r["path"]} / {r["width"]} px — '+('pixels identiques' if r['identical_pixels'] else 'écart à examiner')+'</h2><div class="pair">'
 for label in ['original','restored']:
  html+=f'<article><h3>{label}</h3><a href="{r[label]}">Ouvrir la capture complète</a><div class="frame"><img src="{r[label]}" loading="lazy" alt="{label}"></div></article>'
 html+='</div></section>'
html+='<section><h2>Seule exception graphique : le nouveau footer</h2><div class="pair">'
for width in [1440,390]:
 for part in ['prefooter','footer']:html+=f'<article><h3>{part} / {width} px</h3><a href="{part}-{width}.png"><img src="{part}-{width}.png" loading="lazy" alt="{part}"></a></article>'
html+='</div></section>'
(OUT/'index.html').write_text('<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Ski Society — restauration exacte</title><style>body{font:16px/1.6 Arial;background:#edf1ed;color:#17271f;padding:25px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}article{background:white;padding:20px;min-width:0}.frame{max-height:780px;overflow:auto;margin-top:15px}img{width:100%;display:block}section{margin:45px 0}@media(max-width:700px){body{padding:15px}.pair{grid-template-columns:1fr}}</style></head><body>'+html+'</body></html>')
assert all(r['identical_pixels'] for r in comparisons),'Pixel differences found; inspect comparison.json'
print('PASS: 14 original/restored comparisons match outside footer.')
