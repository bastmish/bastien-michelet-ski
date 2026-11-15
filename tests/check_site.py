from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote,parse_qs
import json,re,sys
ROOT=Path(__file__).resolve().parents[1];PUBLIC=ROOT/'public'
class Doc(HTMLParser):
 def __init__(self,s):
  super().__init__();self.tags=[];self.feed(s)
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
for path in PUBLIC.rglob('*.html'):
 d=Doc(path.read_text());rel=path.relative_to(PUBLIC)
 robots=[a.get('content','') for t,a in d.tags if t=='meta' and a.get('name')=='robots']
 check(robots==['noindex,nofollow'],str(rel)+': robots')
 check(len([t for t,a in d.tags if t=='h1'])==1,str(rel)+': H1')
 for t,a in d.tags:
  for attr in (['href'] if t=='a' else ['src'] if t in ['script','img'] else []):
   url=urlsplit(a.get(attr,''));href=a.get(attr,'')
   if url.scheme or url.netloc:continue
   target=(PUBLIC/url.path.lstrip('/') if url.path.startswith('/') else path.parent/url.path) if url.path else path
   if target.is_dir():target=target/'index.html'
   check(target.exists(),str(rel)+': missing '+href)
   if target.exists() and url.fragment and target.suffix=='.html':
    ids=[a.get('id') for t,a in Doc(target.read_text()).tags]
    check(unquote(url.fragment) in ids,str(rel)+': missing anchor '+href)
pages=json.loads((ROOT/'content/pages.json').read_text())
for p in pages:
 raw=(PUBLIC/p['path']).read_text()
 from html import unescape
 text=unescape(re.sub('<[^>]+>',' ',raw))
 text=' '.join(text.split())
 for sec in p['sections']:
  for b in sec['blocks']:
   value=re.sub(r'\*\*(.*?)\*\*',r'\1',b['text']).split(' — version')[0]
   if value.startswith('CTA :'):value=value[6:]
   for line in value.splitlines():
    line=line.removeprefix('- ')
    check(' '.join(line.split()) in text,p['path']+': copy '+line[:70])
stations=json.loads((ROOT/'content/stations.json').read_text())
check(len(stations)==43,'station count')
for s in stations:
 raw=(PUBLIC/s['URL'].lstrip('/')).read_text();d=Doc(raw)
 check(s['Texte local'].replace('&','&amp;') in raw,'local copy '+s['name'])
 chats=[a['href'] for t,a in d.tags if t=='a' and 'wa.me/' in a.get('href','') and 'text=' in a['href']]
 check(sum(parse_qs(urlsplit(u).query).get('text')==[s['Message WhatsApp']] for u in chats)==2,'CTA '+s['name'])
print('\n'.join(errors) if errors else 'PASS: HTML links, anchors, robots, H1, approved copy and 86 local WhatsApp CTAs.')
if errors: sys.exit(1)
# Exact destination inventory, distinct metadata and a link from the index.
index=Doc((PUBLIC/'stations.html').read_text())
inventory=[a['data-name'] for t,a in index.tags if t=='article' and a.get('class')=='ss-resort']
assert len(inventory)==43 and len(set(inventory))==43
links={a.get('href') for t,a in index.tags if t=='a'}
assert all(s['URL'] in links for s in stations)
assert len({s['Title SEO'] for s in stations})==43
assert len({s['Meta description'] for s in stations})==43
assert 'DEMI-JOURNÉE' not in (PUBLIC/'offres/freeride-decouverte.html').read_text()
assert not (PUBLIC/'sitemap.xml').exists(),'Sitemap must remain pending domain approval in this checkout'
print('PASS: 43 index links, distinct local metadata, freeride formats and deferred sitemap.')
