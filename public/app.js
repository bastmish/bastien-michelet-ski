
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

 // Inquiry form: no backend, no data stored on this site. WhatsApp requires the visitor to press Send.
 // Set this to Bastien's verified professional number with country code and digits only, e.g. "41XXXXXXXXX".
 // Leave empty until the founder supplies the correct recipient.
 const WHATSAPP_RECIPIENT = '';
 const inquiryForm=document.getElementById('ski-request-form');
 const preview=document.getElementById('request-preview');
 const messageOutput=document.getElementById('request-message');
 const copyButton=document.getElementById('copy-request');
 const whatsappLink=document.getElementById('open-whatsapp');
 const pendingNotice=document.getElementById('whatsapp-pending');
 const requestStatus=document.getElementById('request-notice');
 let preparedMessage='';
 if(inquiryForm&&preview&&messageOutput){
  const read=(field)=>String(inquiryForm.elements.namedItem(field)?.value??'').trim();
  const formatMessage=()=>{
   const name=read('firstName');
   const experience=read('experience');
   const level=read('level');
   const participants=read('participants');
   const format=read('format');
   const period=read('period');
   const destination=read('destination');
   const station=read('station');
   const notes=read('notes');
   return [
    'Bonjour Bastien,',
    '',
    'Je souhaite organiser une journée de ski avec vous.',
    '',
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
  inquiryForm.addEventListener('input',()=>{
   preview.hidden=true;
   if(requestStatus)requestStatus.textContent='';
  });
  inquiryForm.addEventListener('change',()=>{
   preview.hidden=true;
   if(requestStatus)requestStatus.textContent='';
  });
  inquiryForm.addEventListener('submit',e=>{
   e.preventDefault();
   if(!inquiryForm.reportValidity())return;
   preparedMessage=formatMessage();
   messageOutput.textContent=preparedMessage;
   preview.hidden=false;
   const number=WHATSAPP_RECIPIENT.replace(/\D/g,'');
   const ready=/^\d{8,15}$/.test(number);
   if(whatsappLink){
    whatsappLink.hidden=!ready;
    if(ready)whatsappLink.href='https://wa.me/'+number+'?text='+encodeURIComponent(preparedMessage);
    else whatsappLink.removeAttribute('href');
   }
   if(pendingNotice)pendingNotice.hidden=ready;
   if(requestStatus)requestStatus.textContent='';
   preview.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth',block:'nearest'});
  });
  if(copyButton)copyButton.addEventListener('click',async()=>{
   if(!preparedMessage)return;
   try{
    if(navigator.clipboard&&window.isSecureContext)await navigator.clipboard.writeText(preparedMessage);
    else{
     const field=document.createElement('textarea');
     field.value=preparedMessage;
     field.style.position='fixed';
     field.style.opacity='0';
     document.body.append(field);
     field.select();
     const copied=document.execCommand('copy');
     field.remove();
     if(!copied)throw new Error('copy rejected');
    }
    if(requestStatus)requestStatus.textContent='Message copié. Il peut être collé dans une conversation WhatsApp.';
   }catch{
    if(requestStatus)requestStatus.textContent='Copie automatique indisponible. Sélectionnez le texte ci-dessus pour le copier.';
   }
  });
 }

})();
