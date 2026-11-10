
(function(){
 'use strict';
 const nav=document.querySelector('.site-header');
 const toggle=document.querySelector('.nav-toggle');
 const links=document.querySelector('.nav-links');
 const dropdown=document.querySelector('.offer-dropdown');
 const setNav=(open)=>{
  if(!toggle||!links)return;
  links.classList.toggle('is-open',open);
  toggle.setAttribute('aria-expanded',String(open));
  toggle.textContent=open?'Fermer':'Menu';
 };
 if(toggle)toggle.addEventListener('click',()=>setNav(toggle.getAttribute('aria-expanded')!=='true'));
 if(links)links.addEventListener('click',e=>{if(e.target.closest('a')){setNav(false);if(dropdown)dropdown.open=false;}});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'){setNav(false);if(dropdown)dropdown.open=false;}});
 document.addEventListener('click',e=>{if(nav&&!nav.contains(e.target)){setNav(false);if(dropdown)dropdown.open=false;}});
 let ticking=false;
 function updateNav(){if(nav)nav.classList.toggle('is-scrolled',(window.scrollY||0)>32);ticking=false;}
 window.addEventListener('scroll',()=>{if(!ticking){requestAnimationFrame(updateNav);ticking=true;}},{passive:true});
 updateNav();
 // Destination-choice helper only: never asserts that a booking slot is available.
 const placeButtons=[...document.querySelectorAll('[data-place-mode]')];
 const placeMessage=document.getElementById('place-message');
 const placeText={
  specific:'Vous avez déjà une station préférée : nous vérifions ensemble si elle correspond à votre groupe, à votre niveau et aux conditions.',
  advice:'Vous n’avez pas de lieu en tête : je vous propose une destination adaptée à vos envies, à votre niveau et aux conditions du moment.'
 };
 placeButtons.forEach(btn=>btn.addEventListener('click',()=>{
  placeButtons.forEach(other=>other.setAttribute('aria-pressed',String(other===btn)));
  if(placeMessage)placeMessage.textContent=placeText[btn.dataset.placeMode]||'';
 }));
 // An editorial experience navigator, linked to real individual pages.
 const offers={
  progresser:{title:'Progresser, à votre rythme.',text:'Un coaching centré sur votre technique, vos sensations et les objectifs que vous choisissez.',img:'https://images.pexels.com/photos/31112554/pexels-photo-31112554.jpeg?auto=compress&cs=tinysrgb&w=1150',alt:'Skieur en poudreuse',href:'offres/progresser.html'},
  famille:{title:'La montagne en famille.',text:'Une expérience partagée, adaptée à l’âge, au niveau et aux envies de chacun.',img:'https://images.pexels.com/photos/20159351/pexels-photo-20159351.jpeg?auto=compress&cs=tinysrgb&w=1150',alt:'Parent et enfant à skis',href:'offres/famille.html'},
  amis:{title:'Une journée entre amis.',text:'Du plaisir, une destination choisie ensemble et un programme qui respecte le rythme de votre groupe.',img:'https://images.pexels.com/photos/20529384/pexels-photo-20529384.jpeg?auto=compress&cs=tinysrgb&w=1150',alt:'Groupe de skieurs en montagne',href:'offres/amis.html'},
  explorer:{title:'Explorer autrement.',text:'Découvrir de nouveaux terrains en tenant compte du niveau, de l’enneigement et des conditions de sécurité.',img:'https://images.pexels.com/photos/12100585/pexels-photo-12100585.jpeg?auto=compress&cs=tinysrgb&w=1150',alt:'Skieur sur pente de neige poudreuse',href:'offres/explorer.html'}
 };
 const offerButtons=[...document.querySelectorAll('[data-offer-select]')];
 const offerPhoto=document.getElementById('offer-photo'),offerTitle=document.getElementById('offer-title'),
 offerText=document.getElementById('offer-text'),offerLink=document.getElementById('offer-link');
 offerButtons.forEach(btn=>btn.addEventListener('click',()=>{
  const offer=offers[btn.dataset.offerSelect];if(!offer)return;
  offerButtons.forEach(other=>other.setAttribute('aria-pressed',String(other===btn)));
  if(offerPhoto){offerPhoto.src=offer.img;offerPhoto.alt=offer.alt;}
  if(offerTitle)offerTitle.textContent=offer.title;
  if(offerText)offerText.textContent=offer.text;
  if(offerLink)offerLink.href=offer.href;
 }));
 // Verified-review component is ready for real, authorized content only.
 // Example: {quote:"...",author:"...",source:"https://..."}; never fill with fictional testimonials.
 const verifiedReviews=[];
 const track=document.getElementById('review-track');
 const trackWrap=document.getElementById('review-track-wrap');
 const empty=document.getElementById('review-empty');
 if(track&&trackWrap){
  const valid=verifiedReviews.filter(r=>r&&r.quote&&r.author&&r.source);
  if(valid.length){
   const build=(r)=>{
    const article=document.createElement('article');article.className='review-quote';
    const quote=document.createElement('blockquote');quote.textContent=r.quote;
    const cite=document.createElement('cite');cite.textContent=r.author;
    article.append(quote,cite);return article;
   };
   const originals=valid.map(build);
   track.append(...originals);
   if(valid.length>1)track.append(...valid.map(build));
   else track.style.animation='none';
   trackWrap.hidden=false;if(empty)empty.hidden=true;
  }
 }


 // WhatsApp click-to-chat: the visitor starts navigation, reviews the drafted message,
 // and must tap Send in WhatsApp. No website-side storage or automatic message sending.
 // Professional WhatsApp recipient configured with the number supplied by the founder.
 // This site opens Bastien's chat directly with the request text prefilled.
 const WHATSAPP_RECIPIENT = '33763532601';
 const inquiryForm=document.getElementById('ski-request-form');
 const requestStatus=document.getElementById('request-notice');
 const destinationSelect=document.getElementById('request-destination');
 const stationField=document.getElementById('request-station-field');
 const stationInput=document.getElementById('request-station');
 if(destinationSelect&&stationField&&stationInput){
  const updateStation=()=>{
   const hasStation=destinationSelect.value==="J'ai une station en tête";
   stationField.hidden=!hasStation;
   stationInput.required=hasStation;
   if(!hasStation)stationInput.value='';
  };
  destinationSelect.addEventListener('change',updateStation);
  updateStation();
 }
 if(inquiryForm){
  const read=(field)=>String(inquiryForm.elements.namedItem(field)?.value??'').trim();
  const formatMessage=()=>{
   const name=read('firstName'),experience=read('experience'),level=read('level');
   const participants=read('participants'),format=read('format'),period=read('period');
   const destination=read('destination'),station=read('station'),notes=read('notes');
   return [
    'Bonjour Bastien,','',
    'Je souhaite organiser une journée de ski avec vous.','',
    '*Ma demande*',
    'Prénom : '+name,
    'Expérience : '+experience,
    'Niveau : '+level,
    'Nombre de skieurs : '+participants,
    'Format : '+format,
    'Période souhaitée : '+(period||'À définir ensemble'),
    'Destination : '+destination+(station?' ('+station+')':''),
    ...(notes?['','*Précisions*',notes]:[]),
    '',
    'Pouvons-nous échanger pour organiser cette journée ?'
   ].join('\n');
  };
  inquiryForm.addEventListener('submit',event=>{
   event.preventDefault();
   if(!inquiryForm.reportValidity())return;
   const number=WHATSAPP_RECIPIENT.replace(/\D/g,'');
   if(number&&!/^\d{8,15}$/.test(number)){
    if(requestStatus)requestStatus.textContent='Le numéro WhatsApp professionnel est mal configuré. Veuillez réessayer plus tard.';
    return;
   }
   const message=formatMessage();
   // Documented WhatsApp URLs: wa.me/number?text=... or wa.me/?text=...
   // No phone configured => WhatsApp lets visitors pick their recipient.
   const url='https://wa.me/'+number+'?text='+encodeURIComponent(message);
   if(requestStatus)requestStatus.textContent='Ouverture de WhatsApp avec votre message prérempli…';
   window.location.assign(url);
  });
 }

})();
