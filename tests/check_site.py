"""Assert exact restoration outside the permitted footer and protect the extension."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote,parse_qs
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1];PUBLIC=ROOT/'public'
class Doc(HTMLParser):
 def __init__(self,text):super().__init__();self.tags=[];self.feed(text)
 def handle_starttag(self,t,a):self.tags.append((t,dict(a)))
def without_footer(text):
 text=re.sub(r'<section\b[^>]*class="art-prefooter"[^>]*>.*?</section>','',text,flags=re.S)
 text=re.sub(r'<section\b[^>]*class="art-prefooter"[^>]*>.*?</section>','',text,flags=re.S)
 text=re.sub(r'<footer\b[^>]*>.*?</footer>','',text,flags=re.S)
 text=re.sub(r'<link\b[^>]*(?:ridgeline-footer\.css|premium-footer\.css)[^>]*>','',text)
 return re.sub(r'<script\b[^>]*ridgeline-footer\.js[^>]*>\s*</script>','',text)
manifest=json.loads((ROOT/'content/original-manifest.json').read_text())
for filename,expected in manifest['sha256'].items():
 path=ROOT/filename
 if path.suffix=='.html':
  original=(ROOT/'content/original-pages'/path.relative_to(PUBLIC)).read_text()
  assert hashlib.sha256(original.encode()).hexdigest()==expected,filename+' snapshot'
  assert without_footer(path.read_text())==without_footer(original),filename+' differs outside footer'
  assert 'integration.css' not in path.read_text() and 'art-direction.css' not in path.read_text(),filename
 else:assert hashlib.sha256(path.read_bytes()).hexdigest()==expected,filename+' original resource changed'
for filename,expected in manifest['editorial_source_sha256'].items():
 assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==expected,filename
print('PASS: every original page matches bc9bb78 literally outside footer; all original assets and editorial sources match SHA-256.')
errors=[]
for path in PUBLIC.rglob('*.html'):
 d=Doc(path.read_text());rel=path.relative_to(PUBLIC)
 assert [a.get('content') for t,a in d.tags if t=='meta' and a.get('name')=='robots']==['noindex,nofollow'],str(rel)
 assert sum(t=='h1' for t,a in d.tags)==1,str(rel)
 for t,a in d.tags:
  for attr in (['href'] if t=='a' else ['src'] if t in ['script','img'] else []):
   href=a.get(attr,'');url=urlsplit(href)
   if url.scheme or url.netloc:continue
   target=(PUBLIC/url.path.lstrip('/') if url.path.startswith('/') else path.parent/url.path) if url.path else path
   if target.is_dir():target=target/'index.html'
   if not target.exists():errors.append(str(rel)+': missing '+href);continue
   if url.fragment and target.suffix=='.html':
    ids={a.get('id') for t,a in Doc(target.read_text()).tags}
    if unquote(url.fragment) not in ids:errors.append(str(rel)+': missing anchor '+href)
assert not errors,'\n'.join(errors)
stations=json.loads((ROOT/'content/stations.json').read_text())
assert len(stations)==43
index=Doc((PUBLIC/'destinations.html').read_text());links={a.get('href') for t,a in index.tags if t=='a'}
assert all(s['URL'] in links for s in stations)
for s in stations:
 raw=(PUBLIC/s['URL'].lstrip('/')).read_text();d=Doc(raw)
 from html import unescape
 assert s['Title SEO'] in unescape(raw) and s['Meta description'] in unescape(raw),s['name']
 for field in ['H1','Hero','H2 — Station','Texte local','H2 — Ski Society','Texte service','H2 — Contact','Texte contact']:
  assert s[field] in unescape(raw),s['name']+' '+field
 chats=[a['href'] for t,a in d.tags if t=='a' and 'wa.me/' in a.get('href','') and 'text=' in a['href']]
 assert sum(parse_qs(urlsplit(u).query).get('text')==[s['Message WhatsApp']] for u in chats)==2,s['name']
 assert 'destination-hero' in raw and 'premium-footer.css' in raw
assert not (PUBLIC/'sitemap.xml').exists()
assert not (PUBLIC/'questions.html').exists()
print('PASS: all links, robots, H1, 43 destination copies/metadata, extension index and 86 contextual CTAs.')
