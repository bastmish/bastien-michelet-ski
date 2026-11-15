"""Restore bc9bb78 pages literally, replace only their footer, build extensions.
The validated copy in content/pages.json remains staged editorial source.
"""
from pathlib import Path
from urllib.parse import quote,urlparse
import html,json,os,re
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'public'
pages=json.loads((ROOT/'content/pages.json').read_text())
stations=json.loads((ROOT/'content/stations.json').read_text())
esc=lambda s:html.escape(s,quote=True)
photos=['20159351','31112554','12100585','6721020']
def wa(text):return 'https://wa.me/33763532601?text='+quote(text)
def link(text,url,cls='btn btn-primary'):return f'<a class="{cls}" href="{esc(url)}">{esc(text)}</a>'
def img(photo,alt='',priority=False):
 return f'<img src="https://images.pexels.com/photos/{photo}/pexels-photo-{photo}.jpeg?auto=compress&amp;cs=tinysrgb&amp;w=1600" alt="{esc(alt)}" '+('fetchpriority="high"' if priority else 'loading="lazy"')+' decoding="async">'
def footer(path):
 local=next((s for s in stations if s['URL'].lstrip('/')==path),None)
 message='Bonjour Ski Society, je souhaite préparer une expérience'+(' à '+local['name'] if local else ' avec Ski Society')+'. Dates : ... Niveau : ... Nombre de participants : ...'
 return (ROOT/'content/premium-footer.html').read_text().strip().replace('{{WHATSAPP}}',esc(wa(message)))
FOOTER_CSS='<link rel="stylesheet" href="/premium-footer.css">'
def restore_original(source,path):
 # Literal edits only in the footer and its own resource tags. No DOM serialization.
 if not re.search(r'<footer\b',source):return source
 source=re.sub(r'<link\b[^>]*ridgeline-footer\.css[^>]*>','',source)
 source=re.sub(r'<script\b[^>]*ridgeline-footer\.js[^>]*>\s*</script>','',source)
 source=source.replace('</head>',FOOTER_CSS+'</head>',1)
 return re.sub(r'<footer\b[^>]*>.*?</footer>',lambda _:footer(path),source,count=1,flags=re.S)
def finish_extension(soup,path):
 for node in soup.select('footer,.art-prefooter'):node.decompose()
 for node in soup.select('link[href$="art-direction.css"],link[href$="premium-footer.css"],link[href$="ridgeline-footer.css"],script[src$="ridgeline-footer.js"]'):node.decompose()
 soup.head.append(soup.new_tag('link',rel='stylesheet',href='/premium-footer.css'))
 soup.body.append(BeautifulSoup(footer(path),'html.parser'))
 return str(soup)
origin=os.environ.get('APPROVED_CANONICAL_ORIGIN','').rstrip('/')
if origin and (urlparse(origin).scheme!='https' or urlparse(origin).path or not urlparse(origin).netloc):raise ValueError('Approved HTTPS origin required')
def base(page,body):
 soup=BeautifulSoup((ROOT/'content/original-pages/offres/ski-prive.html').read_text(),'html.parser')
 soup.title.string=page['title'];soup.select_one('meta[name="description"]')['content']=page['description']
 soup.main.clear();soup.main.append(BeautifulSoup(body,'html.parser'))
 soup.main['class']='ss-integrated';soup.body['class']='ss-integrated-page'
 for tag,attr in [('a','href'),('link','href'),('script','src')]:
  for node in soup.find_all(tag):
   url=node.get(attr,'')
   if url and not url.startswith(('/','#','http','mailto:','tel:')):node[attr]='/'+url.removeprefix('../').removeprefix('./')
 for css in ['manifesto.css','integration.css']:soup.head.append(soup.new_tag('link',rel='stylesheet',href='/'+css))
 if origin:soup.head.append(soup.new_tag('link',rel='canonical',href=origin+'/'+page['path']))
 return finish_extension(soup,page['path'])
# Original pages use the immutable snapshots, not the approved replacement copy.
for template in (ROOT/'content/original-pages').rglob('*.html'):
 path=str(template.relative_to(ROOT/'content/original-pages'))
 (OUT/path).write_bytes(restore_original(template.read_bytes().decode(),path).encode())
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
# Extension entry point. The original stations.html and its search stay untouched.
soup=BeautifulSoup((ROOT/'content/destinations-index.html').read_text(),'html.parser')
soup.title.string='Destinations — 43 fiches locales | Ski Society'
soup.select_one('meta[name="description"]')['content']='Explorez les 43 fiches destinations Ski Society : informations locales et demandes de cours privés, sous réserve de confirmation.'
for node in soup.select('script[src$="stations-search.js"]'):node['src']='/destinations-search.js'
(OUT/'destinations.html').write_text(finish_extension(soup,'destinations.html'))
# Remove the previous redesign's standalone FAQ; the original home FAQ is restored.
(OUT/'questions.html').unlink(missing_ok=True)
(OUT/'404.html').write_text(base({'path':'404.html','title':'Page introuvable | Ski Society','description':'Retrouvez les expériences et destinations Ski Society.'},'<section class="integrated-section"><div class="wrap"><h1>Cette piste reste à découvrir.</h1>'+link('Retour à l’accueil','/')+'</div></section>'))
if origin:
 paths=['','manifesto.html','stations.html','destinations.html']+[p['path'] for p in pages[2:]]+[s['URL'].lstrip('/') for s in stations]
 (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+esc(origin+'/'+p)+'</loc></url>' for p in paths)+'</urlset>')
print('Restored original pages; generated 43 destinations and a separate extension index. No editorial reinjection.')
