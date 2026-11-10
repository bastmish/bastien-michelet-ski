/* V14 — Ski Society: interactive 4-region map, 15 landmark stations.
   A click prepares an inquiry, never an automatic booking or payment. */
(()=>{
 'use strict';
 const root=document.querySelector('.society-map');
 if(!root)return;
 const viewer=root.querySelector('#society-map-scroll');
 const art=root.querySelector('#society-map-art');
 const pins=[...root.querySelectorAll('[data-society-station]')];
 const regions=[...root.querySelectorAll('[data-society-region]')];
 const shapes=[...root.querySelectorAll('.society-department')];
 const area=root.querySelector('#society-selected-area');
 const count=root.querySelector('#society-selected-count');
 const station=root.querySelector('#society-selected-station');
 const description=root.querySelector('#society-selected-description');
 const cta=root.querySelector('#society-selected-button');
 const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
 if(!viewer||!art||!pins.length)return;
 let chosen=pins.find(p=>p.dataset.societyStation==='Megève')||pins[0];
 function pan(pin,animate){
  if(viewer.scrollWidth<=viewer.clientWidth+2)return;
  const x=parseFloat(pin.style.left)/100*art.clientWidth;
  if(!Number.isFinite(x))return;
  const left=Math.max(0,Math.min(viewer.scrollWidth-viewer.clientWidth,x-viewer.clientWidth/2));
  viewer.scrollTo({left,behavior:animate&&!reduced.matches?'smooth':'auto'});
 }
 function activate(pin,scrollMap){
  if(!pin)return;
  chosen=pin;
  const zone=pin.dataset.societyZone;
  const r=regions.find(x=>x.dataset.societyRegion===zone);
  pins.forEach(p=>{
   p.classList.toggle('is-selected',p===pin);
   p.classList.toggle('is-muted',p.dataset.societyZone!==zone);
   p.setAttribute('aria-pressed',String(p===pin));
  });
  regions.forEach(b=>{
   const selected=b.dataset.societyRegion===zone;
   b.classList.toggle('is-active',selected);
   b.setAttribute('aria-pressed',String(selected));
  });
  shapes.forEach(s=>s.classList.toggle('is-active',s.dataset.societyZone===zone));
  if(area)area.textContent=r?.querySelector('span:nth-child(2)')?.textContent||'Alpes';
  if(count)count.textContent=String(pins.filter(p=>p.dataset.societyZone===zone).length).padStart(2,'0')+' STATIONS REPÈRES';
  if(station)station.textContent=pin.dataset.societyStation;
  if(description)description.textContent=r?.dataset.societySummary||'Une journée à préparer selon vos envies.';
  if(scrollMap)pan(pin,true);
 }
 function inquire(){
  if(!chosen)return;
  const dest=document.getElementById('request-destination');
  const input=document.getElementById('request-station');
  if(dest&&input){
   dest.value="J'ai une station en tête";
   dest.dispatchEvent(new Event('change',{bubbles:true}));
   input.value=chosen.dataset.societyStation;
   input.dispatchEvent(new Event('input',{bubbles:true}));
  }
  document.getElementById('reservation')?.scrollIntoView({behavior:reduced.matches?'auto':'smooth',block:'start'});
 }
 for(const b of regions){
  b.addEventListener('click',()=>{
   const group=pins.filter(p=>p.dataset.societyZone===b.dataset.societyRegion);
   activate(group.find(p=>p.classList.contains('is-featured'))||group[0],true);
  });
 }
 for(const p of pins){
  p.addEventListener('click',()=>{activate(p,false);inquire();});
  p.addEventListener('mouseenter',()=>activate(p,false));
  p.addEventListener('focus',()=>activate(p,true));
 }
 cta?.addEventListener('click',inquire);
 // Place prominent labels deterministically to keep close stations legible.
 function arrangeLabels(){
  const w=art.clientWidth,h=art.clientHeight;
  if(!w||!h)return;
  const visible=pins.filter(p=>p.classList.contains('is-featured'));
  visible.sort((a,b)=>parseFloat(a.style.top)-parseFloat(b.style.top));
  const used=[];
  for(const pin of visible){
   const label=pin.querySelector('.society-station-label');
   if(!label)continue;
   label.style.left='';label.style.top='';
   const x=parseFloat(pin.style.left)/100*w;
   const y=parseFloat(pin.style.top)/100*h;
   const lw=label.offsetWidth||90,lh=label.offsetHeight||20;
   const pw=pin.offsetWidth||25,ph=pin.offsetHeight||25;
   let best=null,cost=Infinity;
   for(const side of [x>w*.60?-1:1,x>w*.60?1:-1]){
    for(const d of [17,27,45,68,98]){
     for(const dy of [0,-25,25,-50,50,-75,75,-105,105]){
      const xx=side>0?x+d:x-d-lw;
      const yy=y-lh/2+dy;
      let score=Math.hypot(xx+lw/2-x,yy+lh/2-y)*.4;
      for(const overflow of [12-xx,xx+lw-(w-12),36-yy,yy+lh-(h-34)])
       if(overflow>0)score+=9000+overflow*700;
      for(const b of used){
       const overlapX=Math.max(0,Math.min(xx+lw+3,b.x+b.w+3)-Math.max(xx-3,b.x-3));
       const overlapY=Math.max(0,Math.min(yy+lh+3,b.y+b.h+3)-Math.max(yy-3,b.y-3));
       if(overlapX&&overlapY)score+=9000+overlapX*overlapY*20;
      }
      if(score<cost){cost=score;best={x:xx,y:yy,w:lw,h:lh};}
     }
    }
   }
   if(best){
    used.push(best);
    label.style.left=(best.x-x+pw/2).toFixed(1)+'px';
    label.style.top=(best.y-y+ph/2).toFixed(1)+'px';
   }
  }
 }
 let frame=0;
 function relayout(){
  if(frame)cancelAnimationFrame(frame);
  frame=requestAnimationFrame(()=>{frame=0;arrangeLabels();});
 }
 addEventListener('resize',relayout,{passive:true});
 if('ResizeObserver' in window)new ResizeObserver(relayout).observe(art);
 if(document.fonts?.ready)document.fonts.ready.then(relayout);
 activate(chosen,false);
 requestAnimationFrame(()=>{pan(chosen,false);relayout();});
})();