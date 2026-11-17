"""Two empty outputs must reproduce checked-in HTML/assets exactly."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
def hashes(root):return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file()}
with tempfile.TemporaryDirectory(prefix='ski-build-') as temp:
 outputs=[]
 for name in ['a','b']:
  out=Path(temp)/name
  subprocess.run([sys.executable,'scripts/build.py','--output-dir',str(out)],cwd=ROOT,check=True)
  outputs.append(hashes(out))
 assert outputs[0]==outputs[1],'Two clean builds differ'
 assert outputs[0]==hashes(ROOT/'public'),'Clean output differs from checked-in public'
 print('PASS: two empty-directory builds and committed public match:',len(outputs[0]),'files.')
 if os.environ.get('LOT1_BUILD_REPORT'):
  Path(os.environ['LOT1_BUILD_REPORT']).write_text(json.dumps({'clean_builds':2,'files':len(outputs[0]),'identical':True,'sha256':outputs[0]},indent=2)+'\n')
