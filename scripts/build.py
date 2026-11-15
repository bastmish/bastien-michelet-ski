"""Integrate approved copy into the original Ski Society visual components."""
from pathlib import Path
import json,re,html,os
from urllib.parse import quote,urlparse
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'public'
pages=json.loads((ROOT/'content/pages.json').read_text());stations=json.loads((ROOT/'content/stations.json').read_text())
esc=lambda s:html.escape(s,quote=True)
def clean(s):return re.sub(r'\*\*(.*?)\*\*',r'\1',s).split(' — version')[0].strip()
def wa(s):return 'https://wa.me/33763532601?text='+quote(s)
def link(text,url,cls='btn btn-primary'):return f'<a class="{cls}" href="{esc(url)}">{esc(clean(text))}</a>'
def img(photo,alt='',cls='',priority=False):
 return f'<img class="{cls}" src="https://images.pexels.com/photos/{photo}/pexels-photo-{photo}.jpeg?auto=compress&amp;cs=tinysrgb&amp;w=1600" alt="{esc(alt)}" '+('fetchpriority="high"' if priority else 'loading="lazy"')+' decoding="async">'
def value(section,label):return next((b['text'] for b in section['blocks'] if b['label']==label),'')
def put(node,markup):
 node.clear()
 node.append(BeautifulSoup(markup,'html.parser'))
def element(b,message):
 label=b['label'];text=clean(b['text'])
 if not text:return ''
 if label.startswith('CTA') or text.startswith('CTA :'):
  return link(text.removeprefix('CTA : '),wa(message))
 if text.startswith('- '):return '<ul>'+''.join('<li>'+esc(x.removeprefix('- '))+'</li>' for x in text.splitlines())+'</ul>'
 if label.startswith('Surtitre') or b['text'].startswith('**'):tag='div';cls='kicker'
 elif label in ['H1','H2']:tag=label.lower();cls=''
 elif 'titre' in label.lower() or label.startswith(('Titre','Offre')):tag='h3';cls=''
 else:tag='p';cls='booking-note' if label=='Note' else ''
 return f'<{tag} class="{cls}">{esc(text)}</{tag}>'
def groups(section):
 lead=[];cards=[];tail=[];current=None
 for b in section['blocks']:
  label=b['label'];raw=b['text']
  start=(not label and raw.startswith('**')) or label.startswith(('Titre 0','Offre','Surtitre 0')) or bool(re.match(r'\d+ — Titre',label))
  if start:
   current=[];cards.append(current)
  if label in ['Note','CTA']:tail.append(b)
  elif current is not None:current.append(b)
  else:lead.append(b)
 return lead,cards,tail
photos=['20159351','31112554','12100585','6721020']
offerpaths=['/'+p['path'] for p in pages[2:]]
def message(p):return 'Bonjour Ski Society, je souhaite organiser une expérience : '+p['title'].split(' |')[0]+'. Station : ... Dates : ... Niveau : ... Nombre de participants : ... Format : ...'
origin=os.environ.get('APPROVED_CANONICAL_ORIGIN','').rstrip('/')
if origin and (urlparse(origin).scheme!='https' or urlparse(origin).path or not urlparse(origin).netloc):raise ValueError('Approved HTTPS origin required')
def finish(soup,page):
 for node in soup.select('link[rel="canonical"],link[href$="edition.css"]'):node.decompose()
 soup.title.string=page['title']
 soup.select_one('meta[name="description"]')['content']=page.get('description','')
 for n in soup.select('meta[name="robots"]'):n['content']='noindex,nofollow'
 if origin:
  n=soup.new_tag('link',rel='canonical',href=origin+'/'+('' if page['path']=='index.html' else page['path']));soup.head.append(n)
 for tag,attr in [('a','href'),('link','href'),('script','src'),('img','src')]:
  for n in soup.find_all(tag):
   u=n.get(attr,'')
   if u and not u.startswith(('/','#','http','mailto:','tel:')):
    n[attr]='/'+u.removeprefix('../').removeprefix('./')
 for n in soup.select('.nav-links a,.ss-footer-col a'):
  if n.get('href')=='/manifesto.html':n.string='Le collectif'
 css=soup.new_tag('link',rel='stylesheet',href='/integration.css');soup.head.append(css)
 return str(soup)
def base(page,body,extra=''):
 soup=BeautifulSoup((ROOT/('content/templates/collective.html' if page['path']=='manifesto.html' else 'content/templates/offer.html')).read_text(),'html.parser')
 put(soup.main,body);soup.main['class']='ss-integrated'+(' ss-manifesto-v37' if page['path']=='manifesto.html' else '');soup.body['class']='ss-integrated-page'
 for path in ['manifesto.css']:
  soup.head.append(soup.new_tag('link',rel='stylesheet',href='/'+path))
 if extra:soup.main['class']+=' '+extra
 return finish(soup,page)
# The home remains the original composition, with copy integrated into each component.
p=pages[0];ss=p['sections'];soup=BeautifulSoup((ROOT/'content/templates/home.html').read_text(),'html.parser')
m=message(p);p['description']=value(ss[0],'Texte')
hero=soup.select_one('.hero-copy')
put(hero,element(ss[0]['blocks'][0],m)+'<h1 id="hero-title">'+esc(value(ss[0],'H1'))+'</h1><p>'+esc(value(ss[0],'Texte'))+'</p><div class="hero-actions">'+link(value(ss[0],'CTA principal'),wa(m))+link(value(ss[0],'CTA secondaire'),'#offres','ss-hero-contact')+'</div>')
# Keep the original full-bleed diptych and its interactions; no duplicate marketing copy.
for n in soup.select('.ss-photo-panel-label,.ss-photo-panel-story'):n.decompose()
soup.select_one('#expertise').attrs.pop('aria-labelledby',None)
for i,card in enumerate(soup.select('.ss-adn-photo-card')):
 blocks=ss[1]['blocks'][i*3:i*3+3]
 put(card.select_one('.ss-adn-photo-caption'),'<div>'+''.join(element(b,m) for b in blocks)+'</div>')
heading=soup.select_one('.ss-offers-heading')
put(heading,'<div>'+''.join(element(b,m) for b in ss[2]['blocks'][:3])+'</div>')
_,cards,_=groups(ss[2])
for i,card in enumerate(soup.select('.ss-offer-card')):
 for n in card.select('.ss-offer-meta'):n.decompose()
 content=card.select_one('.ss-offer-content')
 put(content,'<h3>'+esc(cards[i][0]['text'])+'</h3>'+''.join(element(b,m) if not (b['text'].startswith('CTA :')) else '<span class="ss-offer-cta">'+esc(b['text'][6:])+'</span>' for b in cards[i][1:] if b['label']!='Badge'))
 card['href']=offerpaths[i]
 # The badge is already present over the photograph.
lead,cards,tail=groups(ss[3])
put(soup.select_one('.ss-programmes-intro-v72'),''.join(element(b,m) for b in lead)+link(value(ss[3],'CTA'),wa(m),'ss-programmes-link-v72'))
for i,card in enumerate(soup.select('.ss-programme-v72')):
 put(card,'<div class="ss-programme-index-v72">'+str(i+1).zfill(2)+'</div><div class="ss-programme-detail-v72">'+''.join(element(b,m) for b in cards[i])+'</div>')
soup.select_one('.ss-programmes-disclaimer-v72').string=value(ss[3],'Note')
put(soup.select_one('.ss-destinations-heading'),'<div>'+''.join(element(b,m) for b in ss[4]['blocks'][:3])+'</div>')
featured=['Courchevel','Megève','Val d’Isère','Serre Chevalier']
featurelines=ss[4]['blocks'][4]['text'].splitlines()
for i,card in enumerate(soup.select('.ss-region-card')):
 station=next(x for x in stations if x['name']==featured[i])
 card['href']=station['URL'];card['aria-label']='Découvrir '+station['name']
 card.img['alt']='Photographie d’ambiance alpine ; ne représente pas nécessairement '+station['name']
 put(card.select_one('.ss-region-overlay'),'<span class="ss-region-title">'+esc(featurelines[i].removeprefix('- '))+'</span><span class="ss-region-discover">Découvrir la destination</span>')
n=soup.select_one('.ss-station-index-v72')
replacement='<div class="ss-destination-close">'+''.join(element(b,m) if b['label']!='CTA' else link(b['text'],'/stations.html') for b in ss[4]['blocks'][5:])+'</div>'
n.replace_with(BeautifulSoup(replacement,'html.parser'))
put(soup.select_one('#avis .wrap'),'<div class="ss-reviews-heading">'+''.join(element(b,m) for b in ss[5]['blocks'][:3])+'</div><div class="integrated-review-reserve">'+''.join(element(b,m) if b['label']!='CTA' else link(b['text'],'#avis','ss-text-link') for b in ss[5]['blocks'][3:])+'</div>')
for n in soup.select('script[src="reviews-gallery.js"]'):n.decompose()
faq=ss[6]['blocks'];put(soup.select_one('#questions .ss-questions-layout > div'),''.join(element(b,m) for b in faq[:2]))
out=[];item=None
for b in faq[2:]:
 if b['label'].startswith('Q'):
  if item:out.append(item+'</details>')
  item='<details><summary>'+esc(b['text'])+'</summary>'
 else:item+=element(b,m)
out.append(item+'</details>')
put(soup.select_one('.ss-questions-list'),''.join(out))
put(soup.select_one('.ss-contact-heading'),''.join(element(b,m) for b in ss[7]['blocks'][:3]))
side=soup.select_one('.ss-request-side-body')
put(side,''.join(element(b,m) for b in ss[7]['blocks'][3:]))
# Preserve the inquiry form, without unapproved participant restrictions or freeride half-days.
for option in soup.select('select[name="experience"] option'):
 if option.get('value'):option.string=option['value']
for n in soup.select('select[name="participants"] option'):
 n.attrs.pop('disabled',None)
(OUT/p['path']).write_text(finish(soup,p))
# Editorial pages: original photographic offer hero, manifesto layouts, image cards and programme rows.
for j,p in enumerate(pages[1:]):
 m=message(p);sections=p['sections'];hero=sections[0]
 p['description']=value(hero,'Introduction') or value(hero,'Paragraphe')
 photo='31293431' if j==0 else photos[j-1]
 herohtml=''.join(element(b,m) if b['label']!='CTA 2' else link(b['text'],'#'+sections[3 if j==1 else 1]['id'],'btn btn-secondary') for b in hero['blocks'])
 body='<section class="detail-hero integrated-hero"><div class="detail-photo">'+img(photo,'Photographie d’illustration alpine, sans identification d’un membre du collectif',priority=True)+'</div><div class="wrap detail-inner">'+herohtml+'</div></section>'
 if j==0:
  body='<section class="mf-hero integrated-collective-hero"><div class="mf-hero-photo" aria-hidden="true"></div><div class="wrap mf-hero-layout"><div class="mf-hero-copy">'+herohtml+'</div></div></section>'
 for k,section in enumerate(sections[1:],1):
  lead,cards,tail=groups(section)
  if not cards:lead=section['blocks'];tail=[]
  if j==0 and k==1:
   cls='mf-origin';layout='integrated-editorial'
  elif k==3 and j>0:
   cls='ss-section ss-formules ss-programmes-v72 integrated-formats';layout='ss-programmes-layout-v72'
  elif k==len(sections)-1:
   cls='integrated-booking';layout='integrated-booking-layout'
  else:cls='integrated-section';layout='integrated-editorial'
  body+=f'<section class="{cls}" id="{section["id"]}"><div class="wrap {layout}"><div class="integrated-intro">'+''.join(element(b,m) for b in lead)+'</div>'
  if cards:
   body+='<div class="'+('ss-programmes-list-v72' if k==3 and j>0 else 'integrated-card-grid')+'">'
   for i,card in enumerate(cards):
    if k==3 and j>0:
     body+='<article class="ss-programme-v72"><div class="ss-programme-index-v72">'+str(i+1).zfill(2)+'</div><div class="ss-programme-detail-v72">'+''.join(element(b,m) for b in card)+'</div></article>'
    else:
     photohtml=('<figure>'+img(photos[i%4],'Photographie d’illustration de la pratique du ski et du snowboard')+'</figure>') if k==1 else ''
     body+='<article class="integrated-card">'+photohtml+'<div class="integrated-card-body">'+''.join(element(b,m) for b in card)+'</div></article>'
   body+='</div>'
  body+='</div><div class="wrap integrated-notes">'+''.join(element(b,m) for b in tail)+'</div></section>'
 body+='<nav class="wrap integrated-related" aria-label="Autres expériences">'+link('Nos destinations','/stations.html','ss-text-link')+''.join(link(x['title'].split(' |')[0],'/'+x['path'],'ss-text-link') for x in pages[2:] if x!=p)+'</nav>'
 (OUT/p['path']).write_text(base(p,body))
# Local pages use a photographic hero, an asymmetric station portrait, service cards and a reservation panel.
for s in stations:
 path=s['URL'].lstrip('/');m=s['Message WhatsApp']
 regionphoto={'Savoie':'417173','Haute-Savoie':'1366919','Hautes-Alpes':'12100585','Jura suisse':'20159351'}[s['region']]
 body='<section class="detail-hero integrated-hero destination-hero"><div class="detail-photo">'+img(regionphoto,'Photographie d’ambiance alpine ; ne représente pas nécessairement '+s['name'],priority=True)+'</div><div class="wrap detail-inner"><a class="detail-back" href="/stations.html">← Toutes nos destinations</a><div class="kicker">'+esc(s['Surtitre'])+'</div><h1>'+esc(s['H1'])+'</h1><p>'+esc(s['Hero'])+'</p>'+link(s['CTA Hero'],wa(m))+'<span class="photo-caption">Photographie d’ambiance · localisation non attestée</span></div></section>'
 body+='<section class="integrated-section"><div class="wrap destination-portrait"><div><span class="kicker">'+esc(s['region'])+'</span><h2>'+esc(s['H2 — Station'])+'</h2><p>'+esc(s['Texte local'])+'</p><a class="ss-text-link" href="/stations.html">Explorer les destinations ↗</a></div><figure>'+img(regionphoto,'Photographie d’illustration alpine, sans identification de la station')+'<figcaption>Illustration alpine · photographie locale à valider</figcaption></figure></div></section>'
 body+='<section class="integrated-services"><div class="wrap"><div class="integrated-section-head"><span class="kicker">SKI SOCIETY / VOTRE EXPÉRIENCE</span><h2>'+esc(s['H2 — Ski Society'])+'</h2><p>'+esc(s['Texte service'])+'</p></div><p class="booking-note">Découvrez nos disciplines. Leur disponibilité locale, les qualifications et les autorisations sont vérifiées avant toute confirmation. Freeride uniquement à la journée ou sur mesure.</p><div class="integrated-service-grid">'
 for i,p in enumerate(pages[2:]):
  body+='<a class="integrated-service-card" href="/'+p['path']+'">'+img(photos[i],'Illustration de la discipline')+'<span>'+esc(p['title'].split(' |')[0])+' ↗</span></a>'
 body+='</div></div></section><section class="integrated-booking"><div class="wrap destination-booking"><div><span class="kicker">CONTACT & RÉSERVATION</span><h2>'+esc(s['H2 — Contact'])+'</h2><p>'+esc(s['Texte contact'])+'</p>'+link(s['CTA contact'],wa(m))+'</div><aside><span class="integrated-step">01 / VOTRE PROJET</span><p>La prise de contact ne confirme pas une réservation. Tarifs et conditions communiqués avant confirmation.</p><span class="integrated-step">02 / PRÉPARER VOTRE SÉANCE</span><p>Questionnaire de préparation envoyé après confirmation.</p><p class="booking-note">Contenu local en attente de vérification factuelle et opérationnelle : ouverture, encadrement, qualifications, assurances et autorisations'+(' d’enseignement en Suisse' if s['region']=='Jura suisse' else '')+'.</p></aside></div></section>'
 target=OUT/path;target.parent.mkdir(exist_ok=True);target.write_text(base({'path':path,'title':s['Title SEO'],'description':s['Meta description']},body))
# Restore the original station cards and photographs, retaining the new destination links.
soup=BeautifulSoup((ROOT/'content/templates/stations.html').read_text(),'html.parser')
for card,s in zip(soup.select('.ss-resort'),stations):
 card.select_one('.ss-resort-cta')['href']=s['URL']
 card.select_one('.ss-resort-cta')['aria-label']='Découvrir '+s['name']
 card.select_one('.ss-resort-cta').string='Découvrir la station ↗'
(OUT/'stations.html').write_text(finish(soup,{'path':'stations.html','title':soup.title.string,'description':soup.select_one('meta[name="description"]')['content']}))
if origin:
 urls=['' if p=='index.html' else p for p in [p['path'] for p in pages]+['stations.html']+[s['URL'].lstrip('/') for s in stations]]
 (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+esc(origin+'/'+u)+'</loc></url>' for u in urls)+'</urlset>')
(OUT/'404.html').write_text(base({'path':'404.html','title':'Page introuvable | Ski Society','description':'Retrouvez les expériences et destinations Ski Society.'},'<section class="integrated-section"><div class="wrap"><h1>Cette piste reste à découvrir.</h1>'+link('Retour à l’accueil','/')+'</div></section>'))
print('Integrated 6 approved pages and 43 destinations into the original visual components.')
