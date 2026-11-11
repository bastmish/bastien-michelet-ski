
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
 // Animate the four visible stages when the timeline reaches the viewport.
 // Observe only the presentation; no user data or third-party tracking.
 const timeline=document.querySelector('.timeline');
 if(timeline){
  if('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches){
   const observer=new IntersectionObserver(entries=>{
    if(entries.some(entry=>entry.isIntersecting)){
     timeline.classList.add('is-visible');
     observer.disconnect();
    }
   },{threshold:0.15});
   observer.observe(timeline);
  }else timeline.classList.add('is-visible');
 }
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
    'Bonjour Ski Society,','',
    'Je souhaite organiser une expérience privée avec Ski Society.','',
    '*Ma demande*',
    'Prénom : '+name,
    'Expérience : '+experience,
    'Niveau : '+level,
    'Nombre de participants : '+participants,
    'Format : '+format,
    'Période souhaitée : '+(period||'À définir ensemble'),
    'Destination : '+destination+(station?' ('+station+')':''),
    ...(notes?['','*Précisions*',notes]:[]),
    '',
    'Pouvons-nous échanger sur les possibilités, le moniteur disponible et les conditions avant toute réservation ?'
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
