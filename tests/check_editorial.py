"""Literal editorial checks and proof that reference resources/components are reused."""
from pathlib import Path
import json,re,hashlib,sys
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
pages=json.loads((ROOT/'content/pages.json').read_text())
expected=[8,4,5,5,5,5]
assert [len(p['sections']) for p in pages]==expected
def norm(text):return ' '.join(text.split())
def copytext(text):return re.sub(r'\*\*(.*?)\*\*',r'\1',text).split(' — version')[0].removeprefix('CTA : ').strip()
report=[];failures=[]
for page in pages:
 raw=(ROOT/'public'/page['path']).read_text();soup=BeautifulSoup(raw,'html.parser')
 ref=BeautifulSoup((ROOT/'content/original-pages'/('index.html' if page['path']=='manifesto.html' else page['path'])).read_text(),'html.parser')
 # Each page keeps its own source photos and linked stylesheets, not another offer's template.
 if page['path']=='manifesto.html':
  assert all(n['src'] in {i['src'] for i in ref.main.select('img')} for n in soup.main.select('img'))
  assert soup.main.get('class')==['ss-architecture']
  assert len(soup.select('.ss-offer-card'))==3 and len(soup.select('.ss-programme-v72'))==3
 elif page['path']=='index.html':
  removed=ref.select('.ss-photo-panel--transmission img,.ss-adn-photo-card img')
  expected_photos=[n['src'] for n in ref.main.select('img') if n not in removed]
  assert [n['src'] for n in soup.main.select('img')]==expected_photos
  assert len(soup.select('#expertise img'))==1
  assert len(soup.select('.adn-secondary-block'))==2
  assert not soup.select('#expertise a,#expertise button,#expertise svg')
 else:assert [n['src'] for n in soup.main.select('img')]==[n['src'] for n in ref.main.select('img')],page['path']+' photographs'
 refstyles={n['href'] for n in ref.select('link[rel="stylesheet"]') if 'ridgeline-footer' not in n['href']}
 assert refstyles.issubset({n['href'] for n in soup.select('link[rel="stylesheet"]')}),page['path']+' CSS'
 assert 'integration.css' not in raw and 'art-direction.css' not in raw,page['path']+' redesign layer'
 for oldnode in ref.main.find_all(['p','h1','h2','h3']):
  oldtext=norm(oldnode.get_text(' ',strip=True))
  if oldnode.get('id')=='request-notice':continue
  if len(oldtext)>50 and oldtext in norm(soup.main.get_text(' ',strip=True)):
   approved=norm(' '.join(b['text'] for sec in page['sections'] for b in sec['blocks']))
   assert oldtext in approved,page['path']+' superseded marketing text: '+oldtext
 for section in page['sections']:
  nodes=soup.select('[data-editorial-section="'+section['id']+'"]')
  text=norm(' '.join(n.get_text(' ',strip=True) for n in nodes))
  missing=[]
  for b in section['blocks']:
   for line in copytext(b['text']).splitlines():
    line=line.removeprefix('- ')
    if section['id']=='a04' and re.match(r'^0[123] / ',line):
     parts=re.split(r' / | — ',line)
     if not all(norm(part) in text for part in parts):missing.append(line)
    elif norm(line) and norm(line) not in text:missing.append(line)
  if not nodes or missing:failures.append({'page':page['path'],'section':section['id'],'missing':missing})
  report.append({'page':page['path'],'section':section['id'].upper(),'blocks':len(section['blocks']),'status':'PASS' if nodes and not missing else 'FAIL','components':[n.get('class',[]) for n in nodes],'missing':missing})
aux=BeautifulSoup((ROOT/'public/offres/index.html').read_text(),'html.parser')
auxref=BeautifulSoup((ROOT/'content/original-pages/offres/index.html').read_text(),'html.parser')
assert [n['src'] for n in aux.main.select('img')]==[n['src'] for n in auxref.main.select('img')]
assert 'Principalement les week-ends.' not in aux.main.get_text()
# Protect the immutable approved sources and original visual resources.
manifest=json.loads((ROOT/'content/original-manifest.json').read_text())
for filename,sha in manifest['editorial_source_sha256'].items():assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==sha,filename
for filename,sha in manifest['sha256'].items():
 if filename.endswith('.html') or filename in ['public/app.js','public/stations-search.js']:continue
 assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==sha,filename
out=ROOT/'docs/editorial-integration';out.mkdir(exist_ok=True,parents=True)
(out/'sections.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
table='# Vérification des 32 sections\n\nContrôle du texte dans le HTML final de chaque section, sans modification des sources. Les retours à la ligne de présentation sont normalisés ; les mots et la ponctuation sont conservés.\n\n| Page | Section | Blocs sources | Composants bc9bb78 réutilisés | Résultat |\n|---|---|---:|---|---|\n'
for row in report:table+='| '+row['page']+' | '+row['section']+' | '+str(row['blocks'])+' | '+', '.join(' '.join(x) for x in row['components'])+' | '+row['status']+' |\n'
(out/'sections.md').write_text(table)
print(json.dumps(failures,ensure_ascii=False,indent=2) if failures else 'PASS: all 32 sections, every approved block, original photographs/styles and immutable sources.')
sys.exit(bool(failures))
