"""Browser/image dependencies are QA only, separate from requirements-build.txt."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image,ImageChops
import argparse,json,hashlib,sys,time
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Compare every CSS route at desktop/mobile; keep real external failures visible.')
parser.add_argument('--before',required=True);parser.add_argument('--after',required=True);parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args();stage='lot1';OUT=args.output;OUT.mkdir(parents=True,exist_ok=True)
meta=json.loads((ROOT/'content/pages.json').read_text());stations=json.loads((ROOT/'content/stations.json').read_text())
paths=[p['path'] for p in meta]+[s['URL'].lstrip('/') for s in stations]
for path in json.loads((ROOT/'public/assets/css/manifest.json').read_text())['routes']:
 if path not in paths:paths.append(path)
results=[];failures=[];errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 for i,path in enumerate(paths):
  for w,h in [(1440,900),(390,844)]:
   shots=[];vectors=[];resources=[]
   for name,origin in [('before',args.before),('after',args.after)]:
    page=b.new_page(viewport={'width':w,'height':h},reduced_motion='reduce',device_scale_factor=1)
    page.on('pageerror',lambda e:errors.append(str(e)));page.on('requestfailed',lambda r:failures.append(r.url))
    page.goto(origin.rstrip('/')+'/'+path,wait_until='load')
    page.evaluate("""()=>{for(const n of document.querySelectorAll('*')){n.style.setProperty('transition','none','important');n.style.setProperty('animation-play-state','paused','important');n.style.setProperty('caret-color','transparent','important')}document.documentElement.style.scrollBehavior='auto'}""")
    page.evaluate("async()=>{for(let y=0;y<document.documentElement.scrollHeight;y+=900){scrollTo(0,y);await new Promise(r=>requestAnimationFrame(r))}scrollTo(0,0);await new Promise(r=>setTimeout(r,120))}")
    vectors.append(page.evaluate("""()=>[...document.querySelectorAll('main h1,main h2,main h3,main p,main img,form,footer,header,.ss-fullwidth')].map(n=>{let r=n.getBoundingClientRect(),s=getComputedStyle(n);return{tag:n.tagName,id:n.id,cls:n.className,x:r.x,y:r.y,w:r.width,h:r.height,color:s.color,bg:s.backgroundColor,font:s.font,border:s.borderRadius,display:s.display}})"""))
    resources.append(page.evaluate('''()=>({images:[...document.images].map(n=>({url:n.currentSrc,loaded:n.complete&&n.naturalWidth>0})),fonts:[...document.fonts].map(n=>({family:n.family,status:n.status}))})'''))
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),(path,w,'horizontal overflow')
    file=OUT/(path.replace('/','_')+f'-{w}-{name}.png');page.screenshot(path=str(file),full_page=True,animations='disabled');shots.append(file)
    page.close()
   a=Image.open(shots[0]).convert('RGB');c=Image.open(shots[1]).convert('RGB');equal=a.size==c.size;box=ImageChops.difference(a,c).getbbox() if equal else (0,0,1,1)
   delta=ImageChops.difference(a,c) if equal else None
   max_channel_delta=max(v[1] for v in delta.getextrema()) if equal else 255
   changed_pixels=sum(v!=(0,0,0) for v in delta.crop(box).getdata()) if equal and box else 0
   changes=[j for j,(x,y) in enumerate(zip(vectors[0],vectors[1])) if x!=y]
   result={'path':path,'width':w,'pixel_identical':box is None,'max_channel_delta':max_channel_delta,'changed_pixels':changed_pixels,'captures':[{ 'file':str(f.name),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in shots],'before_size':a.size,'after_size':c.size,'diff_box':box,'computed_changes':len(changes),'sample_changes':[{'before':vectors[0][j],'after':vectors[1][j]} for j in changes[:3]],'resources':resources[1]}
   results.append(result)
   if box or changes:print('DIFF',path,w,'pixels',box,'vectors',len(changes),flush=True)
  if i%5==0:print('Compared',i+1,'/',len(paths),flush=True)
 b.close()
report={'stage':stage,'results':results,'failed_requests':sorted(set(failures)),'page_errors':errors}
(OUT/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print('TOTAL',len(results),'pixel diffs',sum(not r['pixel_identical'] for r in results),'computed diffs',sum(bool(r['computed_changes']) for r in results),'JS errors',len(errors),flush=True)

assert not errors,errors
assert all(r["max_channel_delta"]<=2 and not r["computed_changes"] and r["before_size"]==r["after_size"] for r in results), "Visual regression: inspect results.json; <=2 RGB rounding only is tolerated and reported."
