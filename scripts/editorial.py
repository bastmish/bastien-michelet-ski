"""Explicit mapping from validated copy to bc9bb78 components, without a design system."""
from pathlib import Path
import copy,json,re,html
from urllib.parse import quote
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
E=lambda s:html.escape(s,quote=True)
def clean(s):return re.sub(r'\*\*(.*?)\*\*',r'\1',s).split(' — version')[0].strip()
def put(node,markup):
 assert node is not None
 node.clear();node.append(BeautifulSoup(markup,'html.parser'))
def text(node,s):
 decorations=[str(child) for child in node.find_all('span',recursive=False) if not child.get_text(strip=True)]
 put(node,''.join(decorations)+E(s))
def value(section,label):return next((b['text'] for b in section['blocks'] if b['label']==label),'')
def a(label,url,cls='btn btn-primary'):return f'<a class="{cls}" href="{E(url)}">{E(label)}</a>'
def chat(name):return 'https://wa.me/33763532601?text='+quote('Bonjour Ski Society, je souhaite organiser '+name+'. Station : ... Dates : ... Niveau : ... Nombre de participants : ... Format : ...')
def block(b):
 label=b['label'];s=clean(b['text'])
 if not s:return ''
 if s.startswith('- '):return '<ul>'+''.join('<li>'+E(line.removeprefix('- '))+'</li>' for line in s.splitlines())+'</ul>'
 if label.startswith('Surtitre') or b['text'].startswith('**'):tag='div';cls='kicker'
 elif label in ['H1','H2']:tag=label.lower();cls=''
 elif 'titre' in label.lower() or label.startswith(('Titre','Offre')):tag='h3';cls=''
 else:tag='p';cls='booking-note' if label=='Note' else ''
 return f'<{tag} class="{cls}">{E(s)}</{tag}>'
def groups(section):
 lead=[];cards=[];tail=[];current=None
 for b in section['blocks']:
  start=(not b['label'] and b['text'].startswith('**')) or b['label'].startswith(('Titre 0','Offre','Surtitre 0')) or bool(re.match(r'\d+ — Titre',b['label']))
  if start:current=[];cards.append(current)
  if b['label'] in ['Note','CTA']:tail.append(b)
  elif current is None:lead.append(b)
  else:current.append(b)
 return lead,cards,tail
def mark(node,sid):node['data-editorial-section']=sid
def heading(node,s,split=None):
 # Keep the original element, id and italic treatment when it exists.
 if node.find('em') and split and split in s:
  left,right=s.split(split,1);put(node,E(left)+'<br/><em>'+E(split+right)+'</em>')
 else:text(node,s)
def save(soup,page,finish):
 soup.title.string=page['title']
 hero=page['sections'][0]
 description=value(hero,'Introduction') or value(hero,'Texte') or value(hero,'Paragraphe')
 soup.select_one('meta[name="description"]')['content']=description
 soup.head.append(soup.new_tag('link',rel='stylesheet',href='/editorial-content.css'))
 # Guarantee all original aria references still point to an element.
 for node in soup.select('[aria-labelledby]'):
  if not soup.find(id=node['aria-labelledby']):
   h=node.find(['h1','h2','h3'])
   if h:h['id']=node['aria-labelledby']
 (ROOT/'public'/page['path']).write_text(finish(str(soup),page['path']))
def integrate(pages,finish):
 home=BeautifulSoup((ROOT/'content/original-pages/index.html').read_text(),'html.parser')
 sections=pages[0]['sections'];m=chat('une expérience avec Ski Society')
 hero=home.select_one('#accueil');mark(hero,'a01')
 heading(hero.h1,value(sections[0],'H1'),'avec des moniteurs')
 text(hero.select_one('.hero-copy>p'),value(sections[0],'Texte'))
 kicker=home.new_tag('div',attrs={'class':'kicker'});kicker.string=value(sections[0],'Surtitre');hero.h1.insert_before(kicker)
 actions=hero.select('.hero-actions a')
 for node,label,url in zip(actions,['CTA principal','CTA secondaire'],[m,'#offres']):text(node,value(sections[0],label));node['href']=url
 # ADN V2: one photographic composition and its two editorial continuations.
 adn=sections[1]
 reference=BeautifulSoup((ROOT/'content/original-pages/index.html').read_text(),'html.parser')
 photo=copy.copy(reference.select_one('.ss-photo-panel--performance img'))
 photo['srcset']=photo['src']+' 1400w, '+photo['src'].replace('w=1400','w=2400')+' 2400w'
 photo['sizes']='(min-width: 1280px) 75vw, 100vw'
 section=home.new_tag('section',id='expertise',attrs={'class':'ss-adn-editorial-v2','aria-labelledby':'adn-main-title'})
 mark(section,'a02')
 principal='<div class="adn-primary"><div class="adn-main-copy"><div class="adn-block-label">'+E(value(adn,'Surtitre 01'))+'</div><h2 id="adn-main-title">'+E(value(adn,'Titre 01'))+'</h2><p>'+E(value(adn,'Texte 01'))+'</p></div></div>'
 secondary=''
 for i in [2,3]:
  secondary+='<article class="adn-secondary-block" aria-labelledby="adn-title-'+str(i)+'"><div class="adn-block-label">'+E(value(adn,f'Surtitre 0{i}'))+'</div><h3 id="adn-title-'+str(i)+'">'+E(value(adn,f'Titre 0{i}'))+'</h3><p>'+E(value(adn,f'Texte 0{i}'))+'</p></article>'
 put(section,'<div id="adn" class="adn-v2-composition"><figure class="adn-v2-image">'+str(photo)+'</figure>'+principal+'</div><div class="adn-secondary-grid">'+secondary+'</div>')
 home.select_one('#adn').decompose()
 home.select_one('#expertise').replace_with(section)
 home.head.append(home.new_tag('link',rel='stylesheet',href='/adn-editorial.css'))
 # Experiences: retain the exact original anchors, photos, feature badge and ids.
 section=home.select_one('#offres');mark(section,'a03');s=sections[2]
 text(section.select_one('.kicker'),value(s,'Surtitre'));text(section.h2,value(s,'H2'))
 intro=home.new_tag('p');intro.string=value(s,'Introduction');section.select_one('.ss-offers-heading').append(intro)
 _,cards,_=groups(s)
 for i,card in enumerate(section.select('.ss-offer-card')):
  content=card.select_one('.ss-offer-content')
  # Remove the superseded group-size/level promises, preserving the metadata slot.
  put(content,'<span class="ss-offer-meta" aria-hidden="true">'+str(i+1).zfill(2)+' /</span><h3>'+E(cards[i][0]['text'])+'</h3>'+''.join(block(b) if not b['text'].startswith('CTA :') else '<span class="ss-offer-cta">'+E(b['text'][6:])+'</span>' for b in cards[i][1:] if b['label']!='Badge'))
 # Programmes stay in their original full section.
 section=home.select_one('#formules');mark(section,'a04');s=sections[3]
 text(section.select_one('.kicker'),value(s,'Surtitre'));heading(section.h2,value(s,'H2'),'son rythme.')
 text(section.select_one('.ss-programmes-intro-v72>p'),value(s,'Introduction'))
 cta=section.select_one('.ss-programmes-link-v72');svg=str(cta.svg);put(cta,E(value(s,'CTA'))+svg);cta['href']=m
 _,cards,_=groups(s)
 for i,node in enumerate(section.select('.ss-programme-v72')):
  put(node.select_one('.ss-programme-index-v72'),str(i+1).zfill(2))
  put(node.select_one('.ss-programme-detail-v72'),''.join(block(b) for b in cards[i][1:])+'<div class="ss-programme-facts-v72"><span>'+E(clean(cards[i][0]['text']))+'</span></div>')
 text(section.select_one('.ss-programmes-disclaimer-v72'),value(s,'Note'))
 # Destinations keep the original four photographic cards and station-index banner.
 section=home.select_one('#destinations');mark(section,'a05');s=sections[4]
 text(section.select_one('.kicker'),value(s,'Surtitre'));text(section.h2,value(s,'H2'))
 intro=home.new_tag('p');intro.string=value(s,'Introduction');section.select_one('.ss-destinations-heading').append(intro)
 stationdata=json.loads((ROOT/'content/stations.json').read_text())
 section.select_one('.ss-region-gallery')['aria-label']='Stations à la une'
 names=['Courchevel','Megève','Val d’Isère','Serre Chevalier']
 lines=s['blocks'][4]['text'].splitlines()
 for i,node in enumerate(section.select('.ss-region-card')):
  station=next(x for x in stationdata if x['name']==names[i]);node['href']=station['URL'];node['aria-label']='Découvrir '+names[i]
  node.img['alt']='Photographie d’ambiance alpine ; ne représente pas nécessairement '+names[i]
  text(node.select_one('.ss-region-title'),lines[i].removeprefix('- '))
  text(node.select_one('.ss-region-kicker'),station['region'])
 banner=section.select_one('.ss-station-index-v72');banner['href']='stations.html'
 text(banner.select_one('.ss-station-eyebrow-v72'),'SKI SOCIETY')
 text(banner.select_one('.ss-station-copy-v72>strong'),value(s,'Bloc de fermeture — titre'))
 text(banner.select_one('.ss-station-copy-v72>span:last-child'),value(s,'Bloc de fermeture — texte'))
 text(banner.select_one('.ss-station-action-v72>span'),value(s,'CTA'))
 # Reviews retain their shell and columns; only approved reserve copy is displayed.
 section=home.select_one('#avis');mark(section,'a06');s=sections[5]
 text(section.select_one('.kicker'),value(s,'Surtitre'));text(section.h2,value(s,'H2'))
 intro=home.new_tag('p');intro.string=value(s,'Introduction');section.select_one('.ss-reviews-heading').append(intro)
 cols=section.select('.ss-reviews-col')
 put(cols[0],'<figure class="ss-review-card"><h3>'+E(value(s,'Titre de la zone avis'))+'</h3><p>'+E(value(s,'Présentation'))+'</p></figure>')
 put(cols[1],'<figure class="ss-review-card"><span class="ss-review-demo-tag">'+E(value(s,'Libellé de réserve'))+'</span><p>'+E(value(s,'Texte de réserve'))+'</p></figure>')
 put(cols[2],'<div aria-hidden="true" class="ss-review-card">SKI SOCIETY</div>')
 for col in cols:
  approved_card='<figure class="ss-review-card"><h3>'+E(value(s,'Titre de la zone avis'))+'</h3><p>'+E(value(s,'Présentation'))+'</p><span class="ss-review-demo-tag">'+E(value(s,'Libellé de réserve'))+'</span><p>'+E(value(s,'Texte de réserve'))+'</p></figure>'
  put(col,'<div class="ss-review-track">'+approved_card+'</div><div class="ss-review-track" aria-hidden="true">'+approved_card+'</div>')
  col['class']=col.get('class',[])+['ss-reviews-animate']
 section.select_one('.ss-reviews-marquee')['data-reviews-state']='ready'
 bottom=section.select_one('.ss-reviews-v52-bottom');text(bottom.span,value(s,'Libellé de réserve'));text(bottom.a,value(s,'CTA'));bottom.a['href']='#avis';bottom.a.attrs.pop('target',None)
 for script in home.select('script[src="reviews-gallery.js"]'):script.decompose()
 # All six approved questions replace the eight superseded ones; the section stays.
 section=home.select_one('#questions');mark(section,'a07');s=sections[6]
 text(section.select_one('.kicker'),value(s,'Surtitre'));text(section.h2,value(s,'H2'))
 result=[];item=None
 for b in s['blocks'][2:]:
  if b['label'].startswith('Q'):
   if item:result.append(item+'</details>')
   item='<details><summary>'+E(b['text'])+'</summary>'
  else:item+=block(b)
 result.append(item+'</details>');put(section.select_one('.ss-questions-list'),''.join(result))
 # Preserve the original inquiry form and photograph; integrate the approved copy beside it.
 section=home.select_one('#contact');mark(section,'a08');s=sections[7]
 text(section.select_one('.kicker'),value(s,'Surtitre'));text(section.h2,value(s,'H2'));text(section.select_one('.ss-contact-heading>p'),value(s,'Introduction'))
 side=section.select_one('.ss-request-side-body')
 put(side,''.join(block(b) if b['label']!='CTA' else a(b['text'],m,'ss-request-direct') for b in s['blocks'][3:]))
 for option in section.select('select[name="experience"] option'):
  if option.get('value'):option.string=option['value']
 save(home,pages[0],finish)
 # Collective now explicitly uses the homepage components, as requested.
 page=pages[1];ss=page['sections'];m=chat('une expérience avec le collectif Ski Society')
 soup=BeautifulSoup((ROOT/'content/original-pages/index.html').read_text(),'html.parser')
 soup.body['class']='story-home'
 soup.main.clear()
 # Homepage hero, with the complete approved collective introduction.
 node=copy.copy(home.select_one('#accueil'));mark(node,'b01')
 put(node.select_one('.hero-copy'),'<div class="kicker">'+E(value(ss[0],'Surtitre'))+'</div><h1 id="hero-title">'+E(value(ss[0],'H1'))+'</h1><p>'+E(value(ss[0],'Paragraphe'))+'</p><p>'+E(value(ss[0],'Phrase finale'))+'</p><div class="hero-actions">'+a(value(ss[3],'CTA'),'#contact')+a(value(ss[1],'Surtitre'),'#offres','ss-hero-contact')+'</div>')
 soup.main.append(node)
 # The homepage photographic cards carry the three heritage points.
 node=copy.copy(home.select_one('#offres'));mark(node,'b02')
 s=ss[1];text(node.select_one('.kicker'),value(s,'Surtitre'));text(node.h2,value(s,'H2'))
 text(node.select_one('.ss-offers-heading>p'),value(s,'Introduction'))
 _,cards,_=groups(s)
 for i,card in enumerate(node.select('.ss-offer-card')):
  if i>=len(cards):card.decompose();continue
  card.name='article';card.attrs.pop('href',None);card.attrs.pop('aria-label',None)
  card['class']=['ss-offer-card']
  for badge in card.select('.ss-offer-feature-tag'):badge.decompose()
  put(card.select_one('.ss-offer-content'),'<span class="ss-offer-meta" aria-hidden="true">'+str(i+1).zfill(2)+' /</span>'+''.join(block(b) for b in cards[i]))
 soup.main.append(node)
 # The homepage programme layout becomes the collective's three-step philosophy.
 node=copy.copy(home.select_one('#formules'));mark(node,'b03');s=ss[2]
 text(node.select_one('.kicker'),value(s,'Surtitre'));text(node.h2,value(s,'H2'))
 text(node.select_one('.ss-programmes-intro-v72>p'),value(s,'Introduction'))
 cta=node.select_one('.ss-programmes-link-v72');svg=str(cta.svg);put(cta,E(value(ss[3],'CTA'))+svg);cta['href']=m
 _,cards,_=groups(s)
 for i,(card,items) in enumerate(zip(node.select('.ss-programme-v72'),cards)):
  put(card.select_one('.ss-programme-index-v72'),str(i+1).zfill(2))
  put(card.select_one('.ss-programme-detail-v72'),''.join(block(b) for b in items[1:])+'<div class="ss-programme-facts-v72"><span>'+E(clean(items[0]['text']))+'</span></div>')
 node.select_one('.ss-programmes-disclaimer-v72').decompose()
 soup.main.append(node)
 # Same homepage contact composition, without adding a second enquiry form.
 node=copy.copy(home.select_one('#contact'));mark(node,'b04');s=ss[3]
 node['aria-labelledby']='reviews-title'
 text(node.select_one('.kicker'),value(s,'Surtitre'));text(node.h2,value(s,'H2'));node.h2['id']='reviews-title'
 text(node.select_one('.ss-contact-heading>p'),value(s,'Introduction'))
 form=node.select_one('#ski-request-form')
 form.name='div';form.attrs.pop('id',None);form['class']=['ss-request-form','story-summary']
 put(form,'<div class="kicker">'+E(value(s,'Surtitre'))+'</div><h3>'+E(value(s,'Sous-titre'))+'</h3>'+block(s['blocks'][4]))
 put(node.select_one('.ss-request-side-body'),'<span>SKI SOCIETY</span>'+a(value(s,'CTA'),m,'ss-request-direct'))
 soup.main.append(node)
 for script in soup.select('script[src="reviews-gallery.js"]'):script.decompose()
 soup.head.append(soup.new_tag('link',rel='stylesheet',href='/story-home.css'))
 save(soup,page,finish)
 # Offers retain each page's own photo/head/style and existing component structures.
 home_template=BeautifulSoup((ROOT/'content/original-pages/index.html').read_text(),'html.parser')
 for page in pages[2:]:
  ss=page['sections'];m=chat(page['title'].split(' |')[0])
  soup=BeautifulSoup((ROOT/'content/original-pages'/page['path']).read_text(),'html.parser')
  hero=soup.select_one('.detail-hero');mark(hero,ss[0]['id'])
  text(hero.select_one('.kicker'),value(ss[0],'Surtitre'));text(hero.h1,value(ss[0],'H1'));text(hero.select_one('.detail-inner>p'),value(ss[0],'Introduction'))
  actions=hero.select_one('.detail-inner>div:last-child')
  second='#'+ss[3 if ss[0]['id']=='c01' else 1]['id']
  put(actions,a(value(ss[0],'CTA 1'),m)+a(value(ss[0],'CTA 2'),second,'btn btn-secondary'))
  original_sections=soup.main.find_all('section',recursive=False)
  # 02: the original split description / practical list.
  node=original_sections[1];node['id']=ss[1]['id'];mark(node,ss[1]['id'])
  lead,cards,tail=groups(ss[1]);columns=node.select('.detail-points>div')
  put(columns[0],''.join(block(b) for b in lead))
  put(columns[1],'<ul class="detail-list">'+''.join('<li>'+''.join(block(b) for b in items)+'</li>' for items in cards)+'</ul>'+''.join(block(b) for b in tail))
  # 03: the original three other-offer cards, now carrying the validated method.
  node=original_sections[2];node['id']=ss[2]['id'];mark(node,ss[2]['id']);original_heading_attrs=copy.copy(node.h2.attrs)
  lead,cards,tail=groups(ss[2])
  put(node.select_one('.wrap'),''.join(block(b) for b in lead)+'<div class="other-offers">'+''.join('<article class="other-offer">'+''.join(block(b) for b in items)+'</article>' for items in cards)+'</div>'+''.join(block(b) for b in tail))
  node.h2.attrs.update(original_heading_attrs)
  for card_title in node.select('.other-offer h3'):card_title.name='strong'
  # 04: exact programme component from the original homepage, not a new template.
  programme=copy.copy(home_template.select_one('#formules'));programme['id']=ss[3]['id'];mark(programme,ss[3]['id'])
  programme.attrs.pop('aria-labelledby',None)
  s=ss[3];text(programme.select_one('.kicker'),value(s,'Surtitre'));text(programme.h2,value(s,'H2'))
  programme.h2.attrs.pop('id',None);text(programme.select_one('.ss-programmes-intro-v72>p'),value(s,'Introduction'))
  cta=programme.select_one('.ss-programmes-link-v72');svg=str(cta.svg);put(cta,E(value(s,'CTA'))+svg);cta['href']=m
  _,cards,tail=groups(s);nodes=programme.select('.ss-programme-v72')
  for i,node in enumerate(nodes):
   if i>=len(cards):node.decompose();continue
   put(node.select_one('.ss-programme-index-v72'),str(i+1).zfill(2))
   put(node.select_one('.ss-programme-detail-v72'),''.join(block(b) for b in cards[i]))
  text(programme.select_one('.ss-programmes-disclaimer-v72'),value(s,'Note'))
  wrapper=soup.new_tag('div',attrs={'class':'ss-architecture editorial-programmes'});wrapper.append(programme)
  original_sections[3].insert_before(wrapper)
  # 05: keep the original full photographic final CTA, followed by the original steps component.
  node=original_sections[3];node['id']=ss[4]['id'];mark(node,ss[4]['id']);s=ss[4]
  inner=node.select_one('.wrap');text(inner.select_one('.kicker'),value(s,'Surtitre'));text(inner.h2,value(s,'H2'));text(inner.select_one('p'),value(s,'Introduction'))
  text(inner.a,value(s,'CTA'));inner.a['href']=m
  text(inner.select_one('.booking-note'),value(s,'Note'))
  _,cards,_=groups(s)
  steps='<div class="wrap"><div class="steps-grid">'+''.join('<article class="step"><div class="step-number">'+str(i+1).zfill(2)+'</div>'+''.join(block(b) for b in items)+'</article>' for i,items in enumerate(cards))+'</div></div>'
  steps_node=BeautifulSoup('<section class="section steps" data-editorial-section="'+s['id']+'">'+steps+'</section>','html.parser')
  node.insert_before(steps_node)
  save(soup,page,finish)
 # The original offer catalogue is linked from the retained back buttons.
 # Keep its four compositions, but do not leave obsolete availability promises there.
 soup=BeautifulSoup((ROOT/'content/original-pages/offres/index.html').read_text(),'html.parser')
 experience=pages[0]['sections'][2];contact=pages[0]['sections'][7];m=chat('une expérience avec Ski Society')
 text(soup.select_one('.detail-hero .kicker'),value(experience,'Surtitre'))
 text(soup.h1,value(experience,'H2'))
 text(soup.select_one('.detail-inner>p'),value(experience,'Introduction'))
 _,cards,_=groups(experience)
 for node,items in zip(soup.select('.offer-index-card'),cards):
  text(node.strong,items[0]['text'])
  cta=next(b['text'][6:] for b in items if b['text'].startswith('CTA :'))
  text(node.small,cta)
 catalogue_sections=soup.main.find_all('section',recursive=False)
 text(catalogue_sections[1].select_one('.kicker'),value(experience,'Surtitre'))
 details=catalogue_sections[2].select('.detail-points>div')
 put(details[0],'<div class="kicker">'+E(value(contact,'Surtitre'))+'</div><h2>'+E(value(contact,'Sous-titre'))+'</h2>')
 put(details[1],block(contact['blocks'][4])+block(contact['blocks'][2]))
 cta=catalogue_sections[3]
 text(cta.select_one('.kicker'),value(contact,'Surtitre'));text(cta.h2,value(contact,'H2'));text(cta.p,value(contact,'Introduction'));text(cta.a,value(contact,'CTA'));cta.a['href']=m
 soup.title.string='Nos expériences | Ski Society'
 soup.select_one('meta[name="description"]')['content']=value(experience,'Introduction')
 (ROOT/'public/offres/index.html').write_text(finish(str(soup),'offres/index.html'))
