"""Safety cases for conservative family pruning and retained CSS priorities."""
from pathlib import Path
import json,sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from css_build import impossible,parse_rules,render,tokens_css
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
class Safety(unittest.TestCase):
 def test_dynamic_and_functional_selectors(self):
  self.assertTrue(impossible('.absent > .card',{'card','is-open'}))
  for selector in ['.card.is-open','.card:not(.absent)',':is(.absent,.card)',':has(.absent) .card','button:focus-visible']:
   self.assertFalse(impossible(selector,{'card','is-open'}),selector)
 def test_priority_against_inline_and_animation(self):
  registry=json.loads((ROOT/'styles/design-tokens.json').read_text())
  source='''.card{color:#111312!important;padding:20px!important;opacity:.5!important}
.card{color:#ffffff;padding:48px;opacity:1;animation:pulse 1s paused both}
@keyframes pulse{from{opacity:0}to{opacity:1}}'''
  rules,_=parse_rules(source,'fixture',registry)
  compiled,retained=render(rules,registry)
  self.assertEqual(retained,3)
  with sync_playwright() as p:
   b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);values=[]
   for css in [source,tokens_css(registry)+compiled]:
    page=b.new_page();page.set_content('<style>'+css+'</style><div class="card" style="padding:48px">Test</div>')
    values.append(page.locator('.card').evaluate('n=>{let s=getComputedStyle(n);return [s.color,s.padding,s.opacity]}'));page.close()
   b.close()
  self.assertEqual(values[0],values[1]);self.assertEqual(values[1],['rgb(17, 19, 18)','20px','0.5'])
if __name__=='__main__':unittest.main()
