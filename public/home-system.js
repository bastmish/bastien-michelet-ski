/* Home-only themes and private-request wizard. No tracking or persistent storage. */
(()=>{
 'use strict';
 if(!document.body.classList.contains('ss-home-themed'))return;
 const header=document.querySelector('.site-header');
 const themes=[...document.querySelectorAll('.ss-theme-light,.ss-theme-light-soft,.ss-theme-white,.ss-theme-dark')];
 let scheduled=false;
 const updateHeader=()=>{
  scheduled=false;
  if(!header)return;
  // Use the pill's layout position even while the hide-on-scroll transform is active.
  const top=Number.parseFloat(getComputedStyle(header).top)||0;
  const sampleY=Math.min(innerHeight-1,top+header.offsetHeight/2);
  let under=themes.find(n=>{const r=n.getBoundingClientRect();return r.top<=sampleY&&r.bottom>sampleY;});
  if(!under)return;
  const next=under.classList.contains('ss-theme-dark')?'dark':'light';
  if(header.dataset.homeTheme!==next){
   // A two-pixel boundary deadband avoids flapping due to fractional scroll positions.
   const r=under.getBoundingClientRect();
   if(header.dataset.homeTheme&&r.top>sampleY-2)return;
   header.dataset.homeTheme=next;
  }
 };
 const scheduleHeader=()=>{if(!scheduled){scheduled=true;requestAnimationFrame(updateHeader);}};
 addEventListener('scroll',scheduleHeader,{passive:true});addEventListener('resize',scheduleHeader,{passive:true});
 header?.addEventListener('click',scheduleHeader);header?.addEventListener('focusin',scheduleHeader);
 // ResizeObserver tracks menu expansion without changing the header's own dimensions.
 if(header&&'ResizeObserver'in window)new ResizeObserver(scheduleHeader).observe(header);
 updateHeader();
 const form=document.getElementById('private-request-form');
 if(!form)return;
 const step1=form.querySelector('#private-step-1'),step2=form.querySelector('#private-step-2');
 const indicator=form.querySelector('#private-step-indicator'),progress=form.querySelector('[role="progressbar"]');
 const station=form.elements.namedItem('station'),otherStation=form.elements.namedItem('otherStation');
 const otherField=form.querySelector('#private-other-field'),format=form.elements.namedItem('format');
 // Keep the actual option node so returning from freeride restores the same available formats.
 const halfOption=[...format.options].find(n=>n.value.startsWith('Demi-journée'));
 const formatHelp=form.querySelector('#private-format-help');
 const stations=[...form.querySelectorAll('#private-stations option')].map(n=>n.value);
 const value=name=>String(form.elements.namedItem(name)?.value??'').trim();
 let step=1;
 const showStep=number=>{
  step=number;form.dataset.step=String(step);
  step1.hidden=step!==1;step1.disabled=step!==1;
  step2.hidden=step!==2;step2.disabled=step!==2;
  indicator.textContent=step===1?'01 / 02':'02 / 02';
  progress.setAttribute('aria-valuenow',String(step));progress.setAttribute('aria-valuetext','Étape '+step+' sur 2');
  syncStation();
  (step===1?step1:step2).querySelector('legend').focus();
 };
 const error=(name,message)=>{
  const node=form.querySelector('#private-'+name+'-error');
  if(node){node.textContent=message;node.hidden=!message;}
  const fields=name==='experience'?[...form.querySelectorAll('[name="experience"]')]:[form.elements.namedItem(name)];
  fields.filter(Boolean).forEach(n=>{if(message)n.setAttribute('aria-invalid','true');else n.removeAttribute('aria-invalid');});
 };
 function syncStation(){
  const other=station.value.trim()==='Autre station';
  otherField.hidden=!other;otherStation.disabled=!other||step!==1;otherStation.required=other;
  if(!other)error('otherStation','');
 }
 const syncFormat=()=>{
  const freeride=value('experience')==='Freeride & milieu alpin';
  if(freeride){if(format.value.startsWith('Demi-journée'))format.value='';halfOption.remove();}
  else if(!halfOption.isConnected)format.insertBefore(halfOption,format.options[1]);
  formatHelp.textContent=freeride?'Le freeride est proposé uniquement à la journée ou sur mesure.':'Horaires indicatifs, à confirmer selon la station, le moniteur et les disponibilités.';
 };
 const validate=number=>{
  const problems=number===1?{
   experience:value('experience')?'':'Choisissez une expérience.',
   station:stations.includes(value('station'))?'':'Choisissez une destination référencée ou « Autre station ».',
   otherStation:value('station')!=='Autre station'||value('otherStation')?'':'Indiquez le nom de votre station.',
   period:value('period')?'':'Indiquez une date ou une période souhaitée.'
  }:{
   level:value('level')?'':'Choisissez votre niveau.',
   participants:/^[1-9]\d*$/.test(value('participants'))?'':'Indiquez un nombre entier de participants, au moins 1.',
   format:value('format')&&!(value('experience')==='Freeride & milieu alpin'&&value('format').startsWith('Demi-journée'))?'':'Choisissez un format adapté à votre expérience.'
  };
  Object.entries(problems).forEach(([name,message])=>error(name,message));
  const first=Object.keys(problems).find(name=>problems[name]);
  if(first){const n=first==='experience'?form.querySelector('[name="experience"]'):form.elements.namedItem(first);n.focus();return false;}
  return true;
 };
 form.querySelector('[data-next]').addEventListener('click',()=>{if(validate(1))showStep(2);});
 form.querySelector('[data-back]').addEventListener('click',()=>showStep(1));
 form.addEventListener('input',event=>{if(event.target.name)error(event.target.name,'');});
 form.addEventListener('change',event=>{
  if(event.target.name==='experience')syncFormat();
  if(event.target===station)syncStation();
  if(event.target.name)error(event.target.name,'');
 });
 station.addEventListener('input',syncStation);
 form.addEventListener('submit',event=>{
  event.preventDefault();
  if(step===1){if(validate(1))showStep(2);return;}
  if(!validate(1)){showStep(1);validate(1);return;}
  syncFormat();if(!validate(2))return;
  const message=[
   'Bonjour Ski Society,','',
   'Je souhaite préparer une demande privée.','',
   'Expérience : '+value('experience'),
   'Station : '+(value('station')==='Autre station'?value('otherStation'):value('station')),
   'Date ou période : '+value('period'),
   'Niveau : '+value('level'),
   'Nombre de participants : '+value('participants'),
   'Format : '+value('format'),
   ...(value('firstName')?['Prénom : '+value('firstName')]:[]),
   ...(value('notes')?['Informations complémentaires : '+value('notes')]:[]),'',
   'Pouvons-nous échanger sur les possibilités et les modalités avant toute réservation ?'
  ].join('\n');
  const url='https://wa.me/33763532601?text='+encodeURIComponent(message);
  // Only open the draft on this explicit submit action. WhatsApp owns the Send action.
  window.open(url,'_blank','noopener,noreferrer');
  form.querySelector('#private-request-notice').textContent='Votre message est prêt dans WhatsApp. Relisez-le avant de choisir de l’envoyer. Aucune réservation n’est confirmée par ce formulaire.';
 });
 const selected=new URLSearchParams(location.search).get('station')?.trim().slice(0,100);
 if(selected){const match=stations.find(n=>n.toLocaleLowerCase('fr')===selected.toLocaleLowerCase('fr'));station.value=match||'Autre station';if(!match)otherStation.value=selected;}
 form.dataset.step='1';syncStation();syncFormat();
})();
