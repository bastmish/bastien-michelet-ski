"""Home themes and two-step enquiry. Current public on 3000, 23821ca on 3011."""
from pathlib import Path
from urllib.parse import urlsplit,parse_qs
import json,subprocess
from bs4 import BeautifulSoup
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/booking-v3';OUT.mkdir(exist_ok=True,parents=True)
REF='8653c75'
# Other pages remain byte-for-byte unchanged; editorial sources are protected separately.
media_source=json.loads((ROOT/'content/home-immersive-media.json').read_text())
original_contact=BeautifulSoup((ROOT/'content/original-pages/index.html').read_text(),'html.parser').select_one('#contact img')['src']
assert urlsplit(media_source['url']).path==urlsplit(original_contact).path
for file in (ROOT/'public').rglob('*.html'):
 if file==ROOT/'public/index.html':continue
 assert subprocess.check_output(['git','show',REF+':public/'+str(file.relative_to(ROOT/'public'))],cwd=ROOT)==file.read_bytes(),str(file)
before=BeautifulSoup(subprocess.check_output(['git','show',REF+':public/index.html'],cwd=ROOT),'html.parser')
after=BeautifulSoup((ROOT/'public/index.html').read_text(),'html.parser')
# The destination closing copy was subsequently replaced with explicit owner approval.
for soup in [before,after]:
 for node in soup.select('.ss-station-index-v72,.ss-destinations-closing'):node.decompose()
for sid in ['accueil','expertise','offres','formules','destinations','avis','questions']:
 assert before.select_one('#'+sid).get_text(' ',strip=True)==after.select_one('#'+sid).get_text(' ',strip=True),sid+' editorial changes'
assert before.select_one('.art-footer').get_text(' ',strip=True)==after.select_one('.art-footer').get_text(' ',strip=True)
assert [(n.get('href'),n.get_text()) for n in before.select('.art-footer a')]==[(n.get('href'),n.get_text()) for n in after.select('.art-footer a')]
stations=json.loads((ROOT/'content/stations.json').read_text());names=[s['name'] for s in stations]
R={'reference':REF,'scope':'PASS: booking V3 and decorative transition media only; existing section text and other public HTML unchanged','viewports':[],'functional':{},'page_errors':[],'failed_requests':[],'accessibility':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
 page=browser.new_page(reduced_motion='reduce')
 page.add_init_script("window.__drafts=[];window.open=(...args)=>{window.__drafts.push(args);return null;}")
 page.on('pageerror',lambda e:R['page_errors'].append(str(e)))
 page.on('requestfailed',lambda r:R['failed_requests'].append({'url':r.url,'error':r.failure}))
 def goto(url='http://localhost:3000/'):
  page.goto(url,wait_until='networkidle');page.add_style_tag(content='html{scroll-behavior:auto!important}')
 def fill_project(experience='Leçons particulières',station='Méribel',period='Du 12 au 15 février'):
  page.locator('input[name="experience"][value="'+experience+'"]').check()
  page.locator('#private-station').fill(station)
  page.locator('#private-period').fill(period)
 def capture_full_section(width):
  page.evaluate('scrollTo(0,0)');page.wait_for_timeout(100)
  clip=page.locator('#contact').evaluate('n=>{let r=n.getBoundingClientRect(),y=Math.floor(r.top+scrollY);return{x:0,y,width:innerWidth,height:Math.ceil(r.bottom+scrollY)-y}}')
  page.screenshot(path=str(OUT/f'reservation-step1-{width}.png'),clip=clip,full_page=True,animations='disabled')
 for width,height in [(1440,900),(1280,800),(1024,768),(768,1024),(390,844),(375,812)]:
  page.set_viewport_size({'width':width,'height':height});goto()
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  geometry=page.evaluate('''()=>{const ids=['.ss-home-courses','#destinations','#avis','#questions','#contact','.art-prefooter','.art-footer'],rect=n=>{let r=n.getBoundingClientRect();return {x:r.x,y:r.top+scrollY,w:r.width,h:r.height,b:r.bottom+scrollY,color:getComputedStyle(n).backgroundColor}};return Object.fromEntries(ids.map(id=>[id,rect(document.querySelector(id))]));}''')
  for n in geometry.values():assert abs(n['x'])<1 and abs(n['w']-width)<1,n
  pairs=[('.ss-home-courses','#destinations'),('#destinations','#avis'),('#avis','#questions'),('#questions','#contact'),('#contact','.art-prefooter'),('.art-prefooter','.art-footer')]
  for a,b in pairs:assert abs(geometry[a]['b']-geometry[b]['y'])<1,(width,a,b,geometry[a],geometry[b])
  for sid in ['#destinations','#contact','.art-prefooter','.art-footer']:assert geometry[sid]['color']=='rgb(17, 19, 18)'
  for sid in ['#avis','#questions']:assert geometry[sid]['color']=='rgb(255, 255, 255)'
  assert geometry['.ss-home-courses']['color']=='rgb(247, 246, 242)'
  # Verify header theme at the actual pill position; no dimension change between modes.
  header_sizes=[]
  for selector,tone in [('#expertise','light'),('.ss-home-courses','light'),('#destinations','dark'),('#avis','light'),('#questions','light'),('#contact','dark'),('.art-footer','dark')]:
   y=page.locator(selector).evaluate('n=>n.getBoundingClientRect().top+scrollY+80')
   page.evaluate('y=>scrollTo(0,y)',y);page.wait_for_timeout(100)
   page.locator('.site-header .brand').evaluate('n=>n.focus({preventScroll:true})');page.wait_for_timeout(50)
   assert page.locator('.site-header').get_attribute('data-home-theme')==tone,(width,selector)
   header_sizes.append(page.locator('.nav-shell').evaluate('n=>n.getBoundingClientRect().height'))
  assert max(header_sizes)-min(header_sizes)<1,header_sizes
  # First stage is isolated from the second, with all fields inside the viewport width.
  assert page.locator('#private-step-2').is_hidden()
  assert page.locator('#private-step-1').is_visible()
  assert page.locator('.ss-reservation__process,.ss-reservation__invitation,.ss-reservation__direct').count()==0
  assert page.get_by_role('heading',name='Préparer votre message WhatsApp',exact=True).count()==1
  assert page.locator('.ss-private-request__brand svg[role="img"]').get_attribute('aria-label')=='WhatsApp'
  assert page.locator('#private-step-indicator').inner_text()=='Étape 1 sur 2 — Votre projet'
  if width<768:
   note=page.locator('.ss-reservation__reassurance').bounding_box();panel=page.locator('#private-request-form').bounding_box()
   assert note['y']>=panel['y']+panel['height']
  media=page.locator('[data-immersive-photo]').evaluate_all('ns=>ns.map(n=>({state:n.dataset.mediaState,hidden:n.hidden,width:n.querySelector("img").naturalWidth}))')
  assert len(media)==3
  assert all((m['width']>0 and not m['hidden']) if m['state']=='ready' else m['hidden'] for m in media)
  R.setdefault('photographic_states',[]).append({'width':width,'media':media})
  capture_full_section(width)
  page.locator('#private-request-form').screenshot(path=str(OUT/f'form-step1-{width}.png'),animations='disabled')
  fill_project();page.locator('[data-next]').click()
  assert page.locator('#private-step-2').is_visible() and page.locator('#private-step-1').is_hidden()
  assert page.locator('[role="progressbar"]').get_attribute('aria-valuenow')=='2'
  assert page.locator('#private-step-indicator').inner_text()=='Étape 2 sur 2 — Votre profil'
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  button=page.get_by_role('button',name='Ouvrir mon message dans WhatsApp',exact=True)
  assert button.is_visible()
  assert button.evaluate('n=>getComputedStyle(n).backgroundColor')=='rgb(30, 108, 75)'
  assert button.bounding_box()['height']>=56
  assert page.locator('.ss-private-request__progress').evaluate('n=>getComputedStyle(n).height')=='3px'
  page.locator('#private-request-form').screenshot(path=str(OUT/f'form-step2-{width}.png'),animations='disabled')
  page.locator('[data-back]').click()
  assert page.locator('#private-station').input_value()=='Méribel'
  assert page.locator('#private-period').input_value()=='Du 12 au 15 février'
  assert page.evaluate('window.__drafts.length')==0
  R['viewports'].append({'width':width,'height':height,'geometry':geometry,'header':'PASS: correct themes and constant height','wizard':'PASS: steps, progress, preserved data, no overflow'})
 # Full-page and exact transitions. RGB pixels at both viewport edges prove the full-width paint.
 for width,height in [(1440,900),(390,844)]:
  page.set_viewport_size({'width':width,'height':height});goto()
  page.evaluate('scrollTo(0,0)');page.wait_for_timeout(100)
  page.screenshot(path=str(OUT/f'home-full-{width}.png'),full_page=True,animations='disabled')
  for key,sid,above,below in [('formats-destinations','#destinations',(247,246,242),(17,19,18)),('destinations-reviews','#avis',(17,19,18),(255,255,255)),('faq-reservation','#contact',(255,255,255),(17,19,18))]:
   boundary=page.locator(sid).evaluate('n=>n.getBoundingClientRect().top+scrollY')
   y=int(boundary)-100
   path=OUT/f'{key}-{width}.png'
   page.screenshot(path=str(path),clip={'x':0,'y':y,'width':width,'height':360},full_page=True,animations='disabled')
   im=Image.open(path).convert('RGB')
   # Floating contact control is away from the viewport edges.
   for x in [0,width-1]:
    if page.locator('[data-immersive-photo][data-media-state="ready"]').count()==0:assert im.getpixel((x,75))==above,(key,width,x,im.getpixel((x,75)),above)
    if page.locator('[data-immersive-photo][data-media-state="ready"]').count()==0:assert im.getpixel((x,125))==below,(key,width,x,im.getpixel((x,125)),below)
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
 goto('http://localhost:3000/?station=M%C3%A9ribel#contact');assert page.locator('#private-station').input_value()=='Méribel'
 goto('http://localhost:3000/?station=Autre%20domaine#contact');assert page.locator('#private-station').input_value()=='Autre station' and page.locator('#private-other-station').input_value()=='Autre domaine'
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
 # Axe on the new wizard and header in both themes/stages, desktop and mobile.
 for width,height in [(1440,900),(390,844)]:
  page.set_viewport_size({'width':width,'height':height});goto()
  page.add_script_tag(path='/tmp/ski-qa/node_modules/axe-core/axe.min.js')
  for stage in [1,2]:
   if stage==2:fill_project();page.locator('[data-next]').click()
   issues=page.evaluate("async()=> (await axe.run(document.querySelector('#contact'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))")
   R['accessibility'].append({'width':width,'stage':stage,'violations':issues})
   assert not issues,issues
  for selector in ['#destinations','#questions']:
   y=page.locator(selector).evaluate('n=>n.getBoundingClientRect().top+scrollY+80');page.evaluate('y=>scrollTo(0,y)',y)
   page.locator('.brand').evaluate('n=>n.focus({preventScroll:true})');page.wait_for_timeout(100)
   if width<768 and page.locator('.nav-toggle').get_attribute('aria-expanded')!='true':page.locator('.nav-toggle').click()
   issues=page.evaluate("async()=> (await axe.run(document.querySelector('.site-header'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))")
   R['accessibility'].append({'width':width,'headerAt':selector,'violations':issues});assert not issues,issues
 # Before/after reference at desktop and mobile, without touching current media URLs.
 for width,height in [(1440,900),(390,844)]:
  page.set_viewport_size({'width':width,'height':height});goto('http://localhost:3013/')
  page.locator('#contact').screenshot(path=str(OUT/f'before-reservation-{width}.png'),animations='disabled')
 # Other pages still execute legacy JS without new-wizard dependencies.
 for url in ['manifesto.html','offres/ski-prive.html','stations.html']:
  goto('http://localhost:3000/'+url)
 assert not R['page_errors'],R['page_errors']
 browser.close()
R['failed_requests']=list({(r['url'],r['error']):r for r in R['failed_requests']}.values())
R['remote_resources']='BLOCKED' if R['failed_requests'] else 'LOADED'
R['photographic_validation']='BLOCKED' if any(m['state']!='ready' for v in R['photographic_states'] for m in v['media']) else 'REQUIRES_VISUAL_REVIEW'
(OUT/'results.json').write_text(json.dumps(R,ensure_ascii=False,indent=2))
print('PASS: booking V3 on six widths, two stages, 43 stations, validation, preserved data, freeride, encoded WhatsApp drafts and accessibility. Photographic transitions are reported separately.')
print('Remote resources:',R['remote_resources']);print('Photographic validation:',R['photographic_validation'])
