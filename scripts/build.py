"""Render the approved copy. No deployment or indexing operation."""
from pathlib import Path
import json,re,html,os
from urllib.parse import quote,urlparse
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'public'
pages=json.loads((ROOT/'content/pages.json').read_text())
stations=json.loads((ROOT/'content/stations.json').read_text())
esc=lambda s:html.escape(s,quote=True)
def clean(s):return re.sub(r'\*\*(.*?)\*\*',r'\1',s).strip()
def wa(message):return 'https://wa.me/33763532601?text='+quote(message)
def link(label,url):return '<a class="ss-action" href="'+esc(url)+'">'+esc(clean(label))+'</a>'
origin=os.environ.get('APPROVED_CANONICAL_ORIGIN','').rstrip('/')
if origin and (urlparse(origin).scheme!='https' or urlparse(origin).path or not urlparse(origin).netloc):raise ValueError('An approved HTTPS origin is required')
def shell(path,title,description,body):
 canonical='<link rel="canonical" href="'+esc(origin+'/'+('' if path=='index.html' else path))+'">' if origin else ''
 return '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><meta name="description" content="'+esc(description)+'"><title>'+esc(title)+'</title>'+canonical+''.join('<link rel="stylesheet" href="/'+x+'">' for x in ['styles.css','ridgeline-footer.css','white-theme.css','architecture-v21.css','site-nav.css','edition.css'])+'<script src="/app.js" defer></script><script src="/ridgeline-footer.js" defer></script></head><body class="ss-edition"><a class="skip" href="#contenu">Aller au contenu</a>'+(ROOT/'content/header.html').read_text()+'<main id="contenu">'+body+'</main>'+(ROOT/'content/footer.html').read_text()+'</body></html>'
offers=[('/'+p['path'],p['title'].split(' |')[0]) for p in pages[2:]]
for page in pages:
 sections=page['sections']; rendered=[]
 message='Bonjour Ski Society, je souhaite organiser une expérience : '+page['title'].split(' |')[0]+'. Station : ... Dates : ... Niveau : ... Nombre de participants : ... Format : ...'
 description=next(b['text'] for b in sections[0]['blocks'] if b['label'] in ['Introduction','Texte','Paragraphe'])
 for index,section in enumerate(sections):
  sid=section['id']; anchor={'a03':'offres','a05':'destinations','a06':'avis','a08':'contact'}.get(sid,sid)
  chunks=[]
  for block in section['blocks']:
   label=block['label']; raw=block['text']; text=clean(raw)
   if label.startswith('CTA') or text.startswith('CTA :'):
    if text.startswith('CTA :'):text=text[6:]
    url=wa(message)
    if label in ['CTA secondaire','CTA 2']:url='#'+('offres' if sid=='a01' else sections[3 if sid=='c01' else 1]['id'])
    if sid=='a03':
     j=sum('class="ss-action"' in c for c in chunks);url=offers[min(j,3)][0]
    if sid=='a05':url='/stations.html'
    if sid=='a06':url='#avis'
    chunks.append(link(text,url));continue
   if label.startswith('Surtitre'):tag='div';cls='kicker'
   elif label=='H1':tag='h1';cls=''
   elif label=='H2':tag='h2';cls=''
   elif label.startswith('Q'):tag='h3';cls=''
   elif 'titre' in label.lower() or label.startswith('Titre'):tag='h3';cls=''
   elif raw.startswith('**'):tag='h3';cls='';text=clean(raw.split(' — version')[0])
   else:tag='p';cls='ss-note' if label=='Note' else ''
   if '\n' in text:
    chunks.append('<ul>'+''.join('<li>'+esc(line.removeprefix('- '))+'</li>' for line in text.splitlines())+'</ul>')
   else:chunks.append('<'+tag+' class="'+cls+'">'+esc(text)+'</'+tag+'>')
  if sid=='a05':
   chunks.append('<div class="ss-links">'+''.join(link(s['name'],s['URL']) for s in stations if s['name'] in ['Courchevel','Megève','Val d’Isère','Serre Chevalier'])+'</div>')
  if index==0:
   chunks.append('<img class="ss-edition-art" src="/assets/alpes-atlas-society.svg" alt="" width="960" height="600">')
  rendered.append('<section class="ss-copy '+('ss-copy-hero' if index==0 else '')+'" id="'+anchor+'"><div class="wrap ss-copy-inner">'+''.join(chunks)+'</div></section>')
 rendered.append('<aside class="wrap ss-related" aria-label="Continuer la découverte">'+link('Toutes nos destinations','/stations.html')+''.join(link(n,u) for u,n in offers if u!='/'+page['path'])+'</aside>')
 target=OUT/page['path'];target.write_text(shell(page['path'],page['title'],description,''.join(rendered)))
for s in stations:
 path=s['URL'].lstrip('/');message=s['Message WhatsApp']
 body='<nav class="wrap ss-breadcrumb" aria-label="Fil d’Ariane">'+link('Accueil','/')+link('Destinations','/stations.html')+'</nav>'
 for i,(heading,txt) in enumerate([('H1','Hero'),('H2 — Station','Texte local'),('H2 — Ski Society','Texte service'),('H2 — Contact','Texte contact')]):
  body+='<section class="ss-copy '+('ss-local-hero' if i==0 else '')+'"><div class="wrap ss-copy-inner">'
  if i==0:body+='<p class="kicker">'+esc(s['Surtitre'])+'</p>'
  tag='h1' if i==0 else 'h2'
  body+='<'+tag+'>'+esc(s[heading])+'</'+tag+'><p>'+esc(s[txt])+'</p>'
  if i in [0,3]:body+=link(s['CTA Hero' if i==0 else 'CTA contact'],wa(message))
  if i==2:
   body+='<p class="ss-note">Les prestations locales restent à confirmer. Découvrez nos disciplines ; leur présentation ne garantit pas leur disponibilité dans cette station.</p><div class="ss-links">'+''.join(link(n,u) for u,n in offers)+'</div>'
  if i==3:body+='<p class="ss-note">La prise de contact ne confirme pas une réservation. Tarifs et conditions communiqués avant confirmation. Questionnaire de préparation envoyé après confirmation.</p>'
  body+='</div></section>'
 body+='<aside class="wrap ss-verification">Contenu local en attente de vérification factuelle et opérationnelle : ouverture, encadrement, qualifications, assurances et autorisations'+(' d’enseignement en Suisse' if s['region']=='Jura suisse' else '')+'.</aside>'
 target=OUT/path;target.parent.mkdir(exist_ok=True)
 target.write_text(shell(path,s['Title SEO'],s['Meta description'],body))
# Sitemap is generated only with a validated origin, and never submitted.
if origin:
 urls=['' if p=='index.html' else p for p in [p['path'] for p in pages]+['stations.html']+[s['URL'].lstrip('/') for s in stations]]
 (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+esc(origin+'/'+u)+'</loc></url>' for u in urls)+'</urlset>')
print('Rendered 6 main pages and 43 destinations; indexing remains disabled.')
