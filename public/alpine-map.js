/* V12: Original Codrops-inspired scroll map adaptation.
 * Inspiration: https://tympanus.net/codrops/2026/05/21/creating-scroll-driven-svg-map-animations-with-gsap/
 * Contour data: IGN Admin Express COG 2018, Licence Ouverte, via france-geojson.
 * Decorative line is not a driving or ski route.
 */
(()=>{'use strict';
 const section=document.querySelector('.alpine-map-section');
 if(!section)return;
 const scene=document.getElementById('alpine-map-scene');
 const route=document.getElementById('alpine-journey-progress');
 const panel=section.querySelector('.alpine-map-panel');
 const pins=[...section.querySelectorAll('.alpine-pin')];
 const regions=[...section.querySelectorAll('[data-alpine-region]')];
 const name=document.getElementById('alpine-active-station');
 const region=document.getElementById('alpine-active-region');
 const desc=document.getElementById('alpine-active-description');
 const counter=document.getElementById('alpine-active-counter');
 const cta=document.getElementById('alpine-station-cta');
 if(!scene||!route||!panel||!pins.length)return;
 const groups={
  portes:['Portes du Soleil','Des villages aux grands domaines, entre Châtel et Morzine.'],
  grand:['Grand Massif','Du Giffre au Grand Massif, des paysages à explorer.'],
  aravis:['Massif des Aravis','Entre La Clusaz et Le Grand-Bornand, au cœur des Alpes.'],
  blanc:['Pays du Mont-Blanc','Megève, Saint-Gervais et la vallée de Chamonix.']
 };
 const groupOrder=Object.keys(groups);
 const points=pins.map((pin,index)=>({pin,index,group:pin.dataset.alpineZone,station:pin.querySelector('.alpine-pin-name')?.textContent.trim()||''}));
 let active=points[0],activeGroup='portes',visible=false,pauseUntil=0,focused=false,chapter=0;
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const mobile=matchMedia('(max-width: 790px)');
 const setStation=point=>{
  if(!point||active===point)return;
  active.pin.classList.remove('is-current');
  active=point;
  point.pin.classList.add('is-current');
  if(name)name.textContent=point.station;
  if(counter)counter.textContent=String(point.index+1).padStart(2,'0')+' / '+pins.length;
  if(region)region.textContent=groups[point.group]?.[0]||'Haute-Savoie';
  if(desc)desc.textContent=groups[point.group]?.[1]||'Une journée de ski sur mesure.';
 };
 const setGroup=(key,selectFirst=true)=>{
  if(!groups[key])return;
  activeGroup=key;
  regions.forEach(button=>{
   const selected=button.dataset.alpineRegion===key;
   button.classList.toggle('is-current',selected);
   button.setAttribute('aria-pressed',String(selected));
  });
  pins.forEach(pin=>pin.classList.toggle('is-area',pin.dataset.alpineZone===key));
  if(selectFirst)setStation(points.find(p=>p.group===key));
 };
 const choose=()=>{
  const destination=document.getElementById('request-destination');
  const station=document.getElementById('request-station');
  if(destination&&station){
   destination.value="J'ai une station en tête";
   destination.dispatchEvent(new Event('change',{bubbles:true}));
   station.value=active.station;
   station.dispatchEvent(new Event('input',{bubbles:true}));
  }
  document.getElementById('reservation')?.scrollIntoView({behavior:reduced.matches?'auto':'smooth',block:'start'});
 };
 cta?.addEventListener('click',choose);
 points.forEach(point=>{
  const el=point.pin;
  if(parseFloat(el.style.left)>68)el.dataset.flip='true';
  el.addEventListener('mouseenter',()=>{
   pauseUntil=Date.now()+9000;
   setGroup(point.group,false);
   setStation(point);
  });
  el.addEventListener('focus',()=>{focused=true;setGroup(point.group,false);setStation(point);});
  el.addEventListener('blur',()=>{focused=false;pauseUntil=Date.now()+6000;});
  el.addEventListener('click',()=>{
   pauseUntil=Date.now()+30000;
   setGroup(point.group,false);
   setStation(point);
   choose();
  });
 });
 regions.forEach(button=>button.addEventListener('click',()=>{
  pauseUntil=Date.now()+8500;
  setGroup(button.dataset.alpineRegion);
 }));
 const advance=()=>{
  if(!visible||document.hidden||reduced.matches||focused||Date.now()<pauseUntil)return;
  const within=points.filter(p=>p.group===activeGroup);
  const index=within.findIndex(p=>p.index===active.index);
  setStation(within[(index+1)%within.length]);
 };
 let interval=null;
 if(!reduced.matches)interval=setInterval(advance,2600);
 if('IntersectionObserver' in window){
  new IntersectionObserver(entries=>{visible=entries.some(e=>e.isIntersecting);},{threshold:.3}).observe(panel);
 }else visible=true;
 const length=route.getTotalLength();
 route.style.strokeDasharray=String(length);
 route.style.strokeDashoffset=String(length);
 const sync=progress=>{
  const p=Math.max(0,Math.min(1,progress));
  if(!mobile.matches){
   const next=Math.min(3,Math.floor(Math.min(.9999,p)*4));
   if(next!==chapter){
    chapter=next;
    setGroup(groupOrder[next]);
    pauseUntil=Date.now()+1000;
   }
  }
  route.style.strokeDashoffset=String(reduced.matches?0:length*(1-p));
  if(!window.gsap&&!reduced.matches)scene.style.transform='scale('+(1.045-.045*p).toFixed(4)+')';
 };
 section.classList.add('map-ready');
 setGroup('portes');
 if(mobile.matches||reduced.matches)sync(1);
 const hasGSAP=Boolean(!reduced.matches&&!mobile.matches&&window.gsap&&window.ScrollTrigger);
 if(hasGSAP){
  const gsap=window.gsap,ScrollTrigger=window.ScrollTrigger;
  gsap.registerPlugin(ScrollTrigger);
  gsap.fromTo(scene,{scale:1.045},{scale:1,ease:'none',
   scrollTrigger:{trigger:section,start:'top top',end:'bottom bottom',scrub:.7}});
  ScrollTrigger.create({trigger:section,start:'top top',end:'bottom bottom',
   onUpdate:self=>sync(self.progress),onEnter:()=>sync(0),
   onLeave:()=>sync(1),onEnterBack:self=>sync(self.progress)});
 }else if(!mobile.matches&&!reduced.matches){
  let ticking=false;
  const onScroll=()=>{
   if(ticking)return;
   ticking=true;
   requestAnimationFrame(()=>{
    const rect=section.getBoundingClientRect();
    sync(-rect.top/Math.max(1,section.offsetHeight-innerHeight));
    ticking=false;
   });
  };
  addEventListener('scroll',onScroll,{passive:true});
  addEventListener('resize',onScroll,{passive:true});
  onScroll();
 }
 addEventListener('pagehide',()=>{if(interval)clearInterval(interval);},{once:true});
})();