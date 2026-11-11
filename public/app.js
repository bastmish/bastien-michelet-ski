
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

 // Always-available WhatsApp contact, with no form requirement.
 const contactBubble=document.createElement('a');
 contactBubble.className='ss-whatsapp-float';
 contactBubble.href='https://wa.me/'+WHATSAPP_RECIPIENT+'?text='+encodeURIComponent('Bonjour Ski Society, je souhaiterais avoir des renseignements sur vos cours privés de ski ou snowboard.');
 contactBubble.target='_blank';
 contactBubble.rel='noopener noreferrer';
 contactBubble.setAttribute('aria-label','Nous contacter directement sur WhatsApp (nouvel onglet)');
 contactBubble.title='Écrivez-nous sur WhatsApp';
 contactBubble.innerHTML='<svg viewBox="0 0 32 32" aria-hidden="true" focusable="false"><path fill="currentColor" d="M16.01 3.2a12.73 12.73 0 0 0-11 19.14L3.2 29l6.82-1.79A12.8 12.8 0 1 0 16.01 3.2Zm0 23.24c-2.06 0-4.07-.56-5.83-1.61l-.42-.25-4.05 1.06 1.08-3.94-.27-.44a10.48 10.48 0 1 1 9.49 5.18Zm5.75-7.8c-.32-.16-1.88-.92-2.17-1.03-.29-.1-.5-.16-.71.16-.21.31-.82 1.03-1.01 1.24-.18.21-.37.24-.68.08-.32-.16-1.33-.49-2.54-1.56-.94-.84-1.57-1.87-1.75-2.18-.18-.32-.02-.49.14-.65.14-.14.32-.37.47-.55.16-.18.21-.32.32-.53.1-.21.05-.39-.03-.55-.08-.16-.71-1.71-.98-2.34-.25-.61-.51-.53-.71-.54h-.61c-.21 0-.55.08-.84.39-.29.32-1.1 1.08-1.1 2.63s1.13 3.05 1.29 3.26c.16.21 2.21 3.38 5.36 4.74.75.32 1.34.52 1.8.66.76.24 1.45.21 2 .13.61-.09 1.88-.77 2.14-1.52.27-.75.27-1.39.19-1.52-.08-.13-.29-.21-.61-.37Z"/></svg>';
 if(document.body&&!document.querySelector('.ss-whatsapp-float'))document.body.appendChild(contactBubble);

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
  // Preserve the station selected from the resort directory when entering the questionnaire.
  const selectedStation=new URLSearchParams(window.location.search).get('station');
  if(selectedStation && selectedStation.trim()){
    destinationSelect.value="J'ai une station en tête";
    stationInput.value=selectedStation.trim().slice(0,100);
  }
  updateStation();
 }
 if(inquiryForm){
  const experienceSelect=inquiryForm.elements.namedItem('experience');
  const participantsSelect=inquiryForm.elements.namedItem('participants');
  if(experienceSelect&&participantsSelect){
   const updateParticipants=()=>{
    const individual=experienceSelect.value==='Performance & technique';
    const allowed=Array.from(participantsSelect.options);
    allowed.forEach(option=>{
     if(option.value==='2 personnes'||option.value==='3 personnes')option.disabled=individual;
    });
    if(individual)participantsSelect.value='1 personne';
   };
   experienceSelect.addEventListener('change',updateParticipants);
   updateParticipants();
  }
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

 // V54: Photo-led editorial motion, shared across the site.
 // Images are Pexels editorial illustrations, not portraits of Ski Society staff.
 const motionReduced=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
 const main=document.querySelector('main');
 const homepage=main&&main.classList.contains('ss-architecture');
 if(homepage){
  const hero=main.querySelector('.hero');
  const heroImage=hero&&hero.querySelector('.hero-image img');
  if(hero&&heroImage){
   const crossfade=document.createElement('div');
   crossfade.className='ss-hero-crossfade';
   crossfade.setAttribute('aria-hidden','true');
   const sources=[
    heroImage.getAttribute('src'),
    'https://images.pexels.com/photos/416805/pexels-photo-416805.jpeg?auto=compress&cs=tinysrgb&w=1900',
    'https://images.pexels.com/photos/31293431/pexels-photo-31293431.jpeg?auto=compress&cs=tinysrgb&w=1900'
   ];
   const slides=sources.map((src,i)=>{
    const image=document.createElement('img');
    image.src=src;image.alt='';image.decoding='async';
    if(i===0){image.classList.add('is-active');image.fetchPriority='high'}
    else image.loading='lazy';
    crossfade.appendChild(image);return image;
   });
   hero.insertBefore(crossfade,hero.querySelector('.hero-inner'));
   heroImage.style.opacity='0';
   if(!motionReduced){
    let active=0;
    const swap=()=>{
     if(document.hidden)return;
     const next=(active+1)%slides.length;
     const image=slides[next];
     if(!image.complete||!image.naturalWidth)return;
     slides[active].classList.remove('is-active');
     image.classList.add('is-active');
     active=next;
    };
    // Only run while the hero is visible, and stop when the page is in the background.
    let rotation=null;
    const observe=new IntersectionObserver(entries=>{
     const visible=entries.some(e=>e.isIntersecting);
     if(visible&&!rotation)rotation=window.setInterval(swap,5600);
     if(!visible&&rotation){window.clearInterval(rotation);rotation=null}
    },{threshold:.05});
    observe.observe(hero);
    document.addEventListener('visibilitychange',()=>{
     if(document.hidden&&rotation){window.clearInterval(rotation);rotation=null}
    });
   }
  }
 }
 const toneSections=homepage?[
  main.querySelector('#offres'),main.querySelector('#destinations')
 ].filter(Boolean):[];
 toneSections.forEach(section=>section.dataset.editorialTone='dark');
 let toneScheduled=false;
 function updateEditorialTone(){
  toneScheduled=false;
  const focus=window.innerHeight*.43;
  let active=null;
  if(main){
   const blocks=Array.from(main.querySelectorAll('section'));
   for(const block of blocks){
    const rect=block.getBoundingClientRect();
    if(rect.top<=focus&&rect.bottom>=focus){active=block;break}
   }
  }
  const isDark=!!(active&&(active.dataset.editorialTone==='dark'||
   active.id==='avis'||active.classList.contains('mf-hero')||
   active.classList.contains('detail-hero')));
  toneSections.forEach(section=>section.classList.toggle('is-tone-active',section===active));
  document.body.dataset.scrollTone=isDark?'dark':'light';
 }
 function requestEditorialTone(){
  if(!toneScheduled){toneScheduled=true;requestAnimationFrame(updateEditorialTone)}
 }
 window.addEventListener('scroll',requestEditorialTone,{passive:true});
 window.addEventListener('resize',requestEditorialTone,{passive:true});
 updateEditorialTone();
 // Only a small scale change on imagery, no blocking scroll animation.
 if('IntersectionObserver'in window&&!motionReduced){
  const imageObserver=new IntersectionObserver(entries=>{
   entries.forEach(entry=>entry.target.classList.toggle('is-inview',entry.isIntersecting));
  },{threshold:.12});
  document.querySelectorAll('.ss-offer-image,.ss-adn-photo-card,.ss-resort-photo,.mf-turning-photo,.detail-photo').forEach(el=>{
   el.classList.add('ss-story-visual');imageObserver.observe(el);
  });
 }

})();
