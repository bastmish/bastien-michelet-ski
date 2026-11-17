"""Measure exact-selector cascade repetition; not a claim to solve all specificity debt."""
from collections import Counter
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from css_build import parse_rules
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'public/assets/css/manifest.json').read_text());registry=json.loads((ROOT/'styles/design-tokens.json').read_text())
def repeated(rules):
 counts=Counter((r.selector,r.context,d['name']) for r in rules for d in r.declarations)
 return sum(n-1 for n in counts.values())
report={}
for family,entry in m['entries'].items():
 before=[]
 for source in entry['sources']:before+=parse_rules((ROOT/source).read_text(),source,registry)[0]
 after=parse_rules((ROOT/'public/assets/css'/entry['css']).read_text(),entry['css'],registry)[0]
 report[family]={'declarations_before':entry['before']['declarations'],'declarations_after':entry['after']['declarations'],'important_before':entry['before']['important'],'important_after':entry['after']['important'],'repeated_selector_property_before':repeated(before),'repeated_selector_property_after':repeated(after),'unreachable_selectors_removed':len(entry['removed_unreachable']),'superseded_declarations_removed':len(entry['removed_superseded'])}
print(json.dumps(report,indent=2))
if len(sys.argv)>1:Path(sys.argv[1]).write_text(json.dumps(report,indent=2)+'\n')
