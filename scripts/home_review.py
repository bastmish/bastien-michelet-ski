"""Stage-one proposal: change only the rendered home; other pages await approval."""
from pathlib import Path
import copy,json
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
def apply():
 target=ROOT/'public/index.html'
 soup=BeautifulSoup(target.read_text(),'html.parser')
 soup.body['class']=soup.body.get('class',[])+['home-review']
 source=json.loads((ROOT/'content/pages.json').read_text())[0]
 # All programme slots are already approved in the FAQ; reuse them verbatim.
 schedule=next(b['text'] for b in source['sections'][6]['blocks'] if b['text'].startswith('- Matin'))
 slot_list=soup.new_tag('ul',attrs={'class':'home-review-times'})
 for line in schedule.splitlines():
  li=soup.new_tag('li');li.string=line.removeprefix('- ');slot_list.append(li)
 soup.select_one('#formules .ss-programme-facts-v72').append(slot_list)
 # Prepare the replacement footer only on the home for visual review.
 old=soup.select_one('.art-footer')
 nav=copy.copy(old.select_one('.art-footer-navigation'))
 nav_markup=str(nav).replace('art-footer','review-footer')
 legal=old.select_one('.art-footer-legal').get_text(' ',strip=True)
 mark=copy.copy(soup.select_one('.brand-mark'));mark['class']='review-brand-mark'
 contact=soup.select_one('.art-prefooter .art-cta')['href']
 footer=soup.new_tag('footer',attrs={'class':'review-footer'})
 # Use the approved brand signature, actual source photograph and a direct booking link.
 opening=BeautifulSoup('<section class="review-prefooter" aria-labelledby="review-closing-title"><div class="review-prefooter-photo"><img src="https://images.pexels.com/photos/416805/pexels-photo-416805.jpeg?auto=compress&amp;cs=tinysrgb&amp;w=1800" loading="lazy" decoding="async" alt="Skieur en virage, photographie d’illustration sportive"></div><div class="review-prefooter-copy"><span class="kicker">SKI SOCIETY</span><h2 id="review-closing-title">L’excellence du geste.<br>Le plaisir de transmettre.</h2><a class="btn btn-primary" href=""></a></div></section>','html.parser').section
 opening.a['href']=contact;opening.a.string='Nous contacter sur WhatsApp'
 wrapper=soup.new_tag('div',attrs={'class':'wrap'})
 top=soup.new_tag('div',attrs={'class':'review-footer-top'})
 brand=soup.new_tag('a',href='index.html',attrs={'class':'review-footer-brand','aria-label':'Ski Society, accueil'})
 brand.append(mark);brand.append('SKI SOCIETY');top.append(brand)
 back=soup.new_tag('a',href='#header',attrs={'class':'review-footer-back'});back.string='Retour en haut ↑';top.append(back)
 wrapper.append(top);wrapper.append(BeautifulSoup(nav_markup,'html.parser'))
 bottom=soup.new_tag('div',attrs={'class':'review-footer-bottom'})
 bottom.append(BeautifulSoup('<span>© 2026 Ski Society. Tous droits réservés.</span><span>Haute-Savoie · Savoie · Hautes-Alpes</span>','html.parser'))
 wrapper.append(bottom)
 note=soup.new_tag('p',attrs={'class':'review-footer-legal'});note.string=legal;wrapper.append(note);footer.append(wrapper)
 for node in soup.select('.art-prefooter,.art-footer,link[href="/premium-footer.css"]'):node.decompose()
 soup.body.append(opening);soup.body.append(footer)
 soup.head.append(soup.new_tag('link',rel='stylesheet',href='/home-review.css'))
 target.write_text(str(soup))
