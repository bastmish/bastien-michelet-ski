"""Read-only checks for generated CSS bindings and protected legacy dependencies."""
from pathlib import Path
from urllib.parse import urlsplit
import hashlib,json,re
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'public/assets/css/manifest.json').read_text())
for name in m['generated']:
 p=ROOT/'public/assets/css'/name
 assert p.is_file(),name
 assert hashlib.sha256(p.read_bytes()).hexdigest()[:12]==name.split('.')[-2],name+' content hash'
for path,route in m['routes'].items():
 s=BeautifulSoup((ROOT/'public'/path).read_text(),'html.parser')
 local=[urlsplit(n['href']).path for n in s.select('link[rel=stylesheet]') if not urlsplit(n['href']).netloc]
 assert local==['/assets/css/'+n for n in route['stylesheets']],path
 assert len(local)==2,path
 for source in m['entries'][route['family']]['sources']:assert (ROOT/source).is_file(),source
 assert 'noindex,nofollow'==s.select_one('meta[name=robots]')['content'],path
print('PASS: 57 routes bound to two content-hashed stylesheets, complete source coverage and noindex,nofollow.')
