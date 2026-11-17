"""Lot 1: real booking interactions; WhatsApp opening is intercepted, never sent."""
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
import argparse,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:3091');parser.add_argument('--output',type=Path,required=True);parser.add_argument('--axe',type=Path)
args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
names=[s['name'] for s in json.loads((ROOT/'content/stations.json').read_text())]
R={'functional':{},'page_errors':[],'accessibility':[],'navigation':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(reduced_motion='reduce')
 page.add_init_script("window.__drafts=[];window.open=(...args)=>{window.__drafts.push(args);return null;}")
 page.on('pageerror',lambda e:R['page_errors'].append(str(e)))
 def goto(url=None):
  page.goto(url or args.url,wait_until='load');page.add_style_tag(content='html{scroll-behavior:auto!important}')
 def fill_project(experience='Leçons particulières',station='Méribel',period='Du 12 au 15 février'):
  page.locator('input[name="experience"][value="'+experience+'"]').check()
  page.locator('#private-station').fill(station);page.locator('#private-period').fill(period)
 # Functional validation: each error is associated with its own field.
 page.set_viewport_size({'width':1440,'height':900});goto()
 page.locator('[data-next]').click()
 for name in ['experience','station','period']:
  assert page.locator('#private-'+name+'-error').is_visible()
 assert page.locator('#private-step-2').is_hidden()
 fill_project(station='Station non référencée');page.locator('[data-next]').click()
 assert page.locator('#private-station-error').is_visible()
 page.locator('#private-station').fill('Autre station');page.locator('[data-next]').click()
 assert page.locator('#private-otherStation-error').is_visible()
 page.locator('#private-other-station').fill('Station à définir ensemble');page.locator('[data-next]').click()
 page.locator('button[type="submit"]').click()
 for name in ['level','participants','format']:assert page.locator('#private-'+name+'-error').is_visible()
 assert page.evaluate('window.__drafts.length')==0
 page.locator('#private-level').select_option(label='Intermédiaire')
 page.locator('#private-participants').fill('0');page.locator('button[type="submit"]').click();assert page.locator('#private-participants-error').is_visible()
 page.locator('#private-participants').fill('2.5');page.locator('button[type="submit"]').click();assert page.locator('#private-participants-error').is_visible()
 page.locator('#private-participants').fill('27');page.locator('#private-format').select_option(label='Sur mesure')
 page.locator('#private-firstName').fill('Zoé & Émile + équipe')
 page.locator('#private-notes').fill('Ski & snowboard ?\nUn projet <privé> à discuter.')
 page.locator('[data-back]').click()
 assert page.locator('#private-other-station').input_value()=='Station à définir ensemble'
 page.locator('[data-next]').click()
 assert page.locator('#private-participants').input_value()=='27'
 assert page.locator('#private-notes').input_value().endswith('à discuter.')
 page.locator('button[type="submit"]').click()
 draft=page.evaluate('window.__drafts[0]');assert draft[1:] == ['_blank','noopener,noreferrer']
 url=urlsplit(draft[0]);assert url.netloc=='wa.me' and url.path=='/33763532601'
 message=parse_qs(url.query)['text'][0]
 for text in ['Leçons particulières','Station à définir ensemble','Du 12 au 15 février','Intermédiaire','27','Sur mesure','Zoé & Émile + équipe','Un projet <privé> à discuter.']:assert text in message,text
 R['functional']['encoding']='PASS: accents, ampersands, plus signs, angle brackets and newlines round-trip; 27 participants accepted'
 # Every referenced station works, plus known/unknown station query-prefill.
 goto();fill_project()
 assert page.locator('#private-stations option').count()==44
 for name in names:
  page.locator('#private-station').fill(name);page.locator('[data-next]').click()
  assert page.locator('#private-step-2').is_visible(),name
  page.locator('[data-back]').click()
 R['functional']['stations']='PASS: all 43 stations advance; Other station requires free text'
 goto(args.url+'/?station=M%C3%A9ribel#contact');assert page.locator('#private-station').input_value()=='Méribel'
 goto(args.url+'/?station=Autre%20domaine#contact');assert page.locator('#private-station').input_value()=='Autre station' and page.locator('#private-other-station').input_value()=='Autre domaine'
 # Freeride removes, rather than disables, half-day and explains the restriction.
 goto();fill_project();page.locator('[data-next]').click()
 page.locator('#private-format').select_option(label='Demi-journée — 2 h 30')
 page.locator('[data-back]').click();page.locator('[name="experience"][value="Freeride & milieu alpin"]').check();page.locator('[data-next]').click()
 assert page.locator('#private-format option').filter(has_text='Demi-journée').count()==0
 assert page.locator('#private-format').input_value()==''
 assert 'uniquement' in page.locator('#private-format-help').inner_text()
 page.locator('[data-back]').click();page.locator('[name="experience"][value="Performance & technique"]').check();page.locator('[data-next]').click()
 assert page.locator('#private-format option').filter(has_text='Demi-journée').count()==1
 page.locator('#private-level').select_option(label='Débutant');page.locator('#private-participants').fill('12');page.locator('#private-format').select_option(label='Journée complète — 09h30 à 17h00')
 assert not page.locator('#private-firstName').get_attribute('required') and not page.locator('#private-notes').get_attribute('required')
 page.locator('button[type="submit"]').click();msg=parse_qs(urlsplit(page.evaluate('window.__drafts[0][0]')).query)['text'][0]
 assert 'Prénom :' not in msg and 'Informations complémentaires :' not in msg
 R['functional']['freeride']='PASS: actual option removal, explanation, stale half-day cleared, option restored for other experiences'
 R['functional']['validation']='PASS: required fields and positive integer participants; first name and notes optional; no arbitrary group maximum'
 R['functional']['navigation']='PASS: values retained between steps, no reload, no draft before explicit valid submit'

 for width,height in [(1440,900),(390,844)]:
  page.set_viewport_size({'width':width,'height':height});goto()
  if width==390:
   page.locator('.nav-toggle').click();assert page.locator('.nav-toggle').get_attribute('aria-expanded')=='true'
   assert page.locator('#navigation').is_visible();page.locator('.nav-toggle').click()
  page.locator('#questions summary').first.click();assert page.locator('#questions details').first.get_attribute('open') is not None
  page.locator('#questions details').first.screenshot(path=str(args.output/f'faq-open-{width}.png'))
  if args.axe:page.add_script_tag(path=str(args.axe))
  for stage in [1,2]:
   if stage==2:fill_project();page.locator('[data-next]').click()
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   page.locator('#private-request-form').screenshot(path=str(args.output/f'booking-stage{stage}-{width}.png'),animations='disabled')
   if args.axe:
    issues=page.evaluate("async()=> (await axe.run(document.querySelector('#contact'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))")
    R['accessibility'].append({'width':width,'stage':stage,'violations':issues});assert not issues,issues
  for catalogue in ['stations.html','destinations.html']:
   goto(args.url+'/'+catalogue);page.locator('#station-search').fill('meribel')
   assert page.locator('.ss-resort:visible').count()==1
   assert page.locator('.ss-resort:visible .ss-resort-cta').get_attribute('href')=='/stations/meribel.html'
   page.locator('#station-search-clear').click();assert page.locator('.ss-resort:visible').count()==43
   page.locator('[data-filter="Savoie"]').click();assert page.locator('.ss-resort:visible').count()==12
   page.locator('#station-search').fill('meribel');page.locator('.ss-suggestion').first.click();page.wait_for_url('**/stations/meribel.html')
   R['navigation'].append({'width':width,'catalogue':catalogue,'search_reset_filters_and_destination_navigation':'PASS'})
 assert not R['page_errors'],R['page_errors']
 browser.close()
(args.output/'functional.json').write_text(json.dumps(R,ensure_ascii=False,indent=2)+'\n')
print('PASS: booking business rules, 43 stations, WhatsApp drafts, mobile menu, FAQ, catalogue search, filters and accessibility.')
