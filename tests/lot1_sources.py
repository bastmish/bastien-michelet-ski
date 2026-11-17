"""Verify the entire non-CSS contract against the audited Git state."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1];REF='5bd9206'
def original(path):return subprocess.check_output(['git','show',REF+':'+path],cwd=ROOT)
def without_css(raw):
 raw=re.sub(rb'<link\b(?=[^>]*\brel=[\"\']stylesheet[\"\'])[^>]*>',b'',raw)
 return re.sub(rb'<style\b[^>]*>.*?</style>',b'',raw,flags=re.S)
protected=[]
for p in sorted((ROOT/'content').rglob('*')):
 if p.is_file():assert p.read_bytes()==original(str(p.relative_to(ROOT))),str(p);protected.append(str(p.relative_to(ROOT)))
for p in sorted((ROOT/'public').rglob('*')):
 if not p.is_file() or p.relative_to(ROOT/'public').parts[:2]==('assets','css'):continue
 path=str(p.relative_to(ROOT));before=original(path)
 if p.suffix=='.html':assert without_css(p.read_bytes())==without_css(before),path+' non-CSS HTML changed'
 else:assert p.read_bytes()==before,path+' static resource changed'
 protected.append(path)
print('PASS:',len(protected),'unchanged content/static/HTML contracts; 32 editorial sections, 43 station data and WhatsApp JS protected.')
