/* V12.1 · Haute-Savoie — permanent scroll-driven station reveal.
 * Original implementation inspired by the Codrops GSAP scroll-map tutorial.
 * Base geographic outline: IGN Admin Express (Licence Ouverte) via france-geojson.
 * Animated red track is illustrative, NOT a skiing or travel itinerary.
 */
(()=>{'use strict';
 const section=document.querySelector('.alpine-map-section');
 if(!section)return;
 const panel=section.querySelector('.alpine-map-panel');
 const scene=document.getElementById('alpine-map-scene');
 const route=document.getElementById('alpine-journey-progress');
 const pinElements=[...section.querySelectorAll('.alpine-pin')];
 const buttons=[...section.querySelectorAll('[data-alpine-region]')];
 const stationName=document.getElementById('alpine-active-station');
 const stationGroup=document.getElementById('alpine-active-region');
 const stationDesc=document.getElementById('alpine-active-description');
 const stationCounter=document.getElementById('alpine-active-counter');
 const stationCta=document.getElementById('alpine-station-cta');
 const discoveryCount=document.getElementById('alpine-reveal-count');
 const hint=document.getElementById('alpine-map-hint');
 const ledger=document.getElementById('alpine-ledger-grid');
 if(!panel||!scene||!route||!pinElements.length)return;

 const groups={
  portes:['Portes du Soleil','Des villages aux grands domaines, entre Châtel et Morzine.'],
  grand:['Grand Massif','Du Giffre au Grand Massif, des paysages à explorer.'],
  aravis:['Massif des Aravis','Entre La Clusaz et Le Grand-Bornand, au cœur des Alpes.'],
  blanc:['Pays du Mont-Blanc','Megève, Saint-Gervais et la vallée de Chamonix.']
 };
 const points=pinElements.map((pin,index)=>({
  pin,index,zone:pin.dataset.alpineZone,
  name:pin.querySelector('.alpine-pin-name')?.textContent.trim()||''
 }));
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const narrow=matchMedia('(max-width: 1100px)');
 let active=points[0], activeZone='portes', maxRevealed=0, raf=0;
 const revealed=new Set();

 function highlight(point){
  if(!point)return;
  active?.pin.classList.remove('is-current');
  active=point;
  point.pin.classList.add('is-current');
  if(stationName)stationName.textContent=point.name;
  if(stationCounter)stationCounter.textContent=String(point.index+1).padStart(2,'0')+' / '+points.length;
  if(stationGroup)stationGroup.textContent=groups[point.zone]?.[0]||'Haute-Savoie';
  if(stationDesc)stationDesc.textContent=groups[point.zone]?.[1]||'Une journée de ski à imaginer ensemble.';
  for(const p of points)p.ledgerButton?.classList.toggle('is-current',p===point);
 }
 function focusZone(key,{selectFirst=true}={}){
  if(!groups[key])return;
  activeZone=key;
  buttons.forEach(button=>{
   const selected=button.dataset.alpineRegion===key;
   button.classList.toggle('is-current',selected);
   button.setAttribute('aria-pressed',String(selected));
  });
  points.forEach(point=>point.pin.classList.toggle('is-area',point.zone===key));
  if(selectFirst)highlight(points.find(point=>point.zone===key));
 }
 function displayPoint(point){
  if(!point||revealed.has(point.index))return;
  revealed.add(point.index);
  point.pin.classList.add('is-revealed');
  point.pin.style.transitionDelay=(reduced.matches?0:Math.min(210,point.index*8))+'ms';
  if(point.ledgerButton){
   point.ledgerButton.classList.add('is-revealed');
   point.ledgerButton.removeAttribute('aria-hidden');
   point.ledgerButton.tabIndex=0;
  }
  if(discoveryCount)discoveryCount.textContent=revealed.size+' / '+points.length;
  if(hint)hint.textContent=revealed.size===points.length?'24 stations à découvrir ensemble':revealed.size+' stations révélées · continuez à défiler';
 }
 function revealThrough(count){
  const goal=Math.max(maxRevealed,Math.min(points.length,Math.max(0,count)));
  if(goal===maxRevealed)return;
  for(let i=maxRevealed;i<goal;i++)displayPoint(points[i]);
  maxRevealed=goal;
  highlight(points[goal-1]);
  focusZone(points[goal-1].zone,{selectFirst:false});
 }
 function revealGroup(key){
  points.filter(point=>point.zone===key).forEach(displayPoint);
  const first=points.find(point=>point.zone===key);
  focusZone(key,{selectFirst:false});
  highlight(first);
 }
 function choose(){
  const destination=document.getElementById('request-destination');
  const station=document.getElementById('request-station');
  if(destination&&station){
   destination.value="J'ai une station en tête";
   destination.dispatchEvent(new Event('change',{bubbles:true}));
   station.value=active.name;
   station.dispatchEvent(new Event('input',{bubbles:true}));
  }
  document.getElementById('reservation')?.scrollIntoView({
   behavior:reduced.matches?'auto':'smooth',block:'start'
  });
 }
 stationCta?.addEventListener('click',choose);

 // Keep a readable, persistent catalogue when all 24 geographic names cannot
 // be placed around the points at phone/tablet widths.
 if(ledger){
  for(const point of points){
   const item=document.createElement('button');
   item.type='button';
   item.className='alpine-ledger-item';
   item.textContent=point.name;
   item.setAttribute('aria-hidden','true');
   item.tabIndex=-1;
   item.addEventListener('click',()=>{
    displayPoint(point);
    focusZone(point.zone,{selectFirst:false});
    highlight(point);
    choose();
   });
   point.ledgerButton=item;
   ledger.append(item);
  }
 }

 // Greedy 2D label placement: keep all revealed geographic names legible.
 // All coordinates are relative to the real size of the map panel.
 function layoutLabels(){
  if(narrow.matches)return;
  const width=panel.clientWidth,height=panel.clientHeight;
  if(!width||!height)return;
  const placed=[];
  const pinSize=pinElements[0]?.offsetWidth||30;
  const ordered=[...points].sort((a,b)=>
   parseFloat(a.pin.style.top)-parseFloat(b.pin.style.top)||
   parseFloat(a.pin.style.left)-parseFloat(b.pin.style.left));
  for(const point of ordered){
   const pin=point.pin;
   const label=pin.querySelector('.alpine-pin-name');
   if(!label)continue;
   // offsetWidth works even for visibility:hidden: labels reserve no layout.
   const lw=label.offsetWidth||94,lh=label.offsetHeight||23;
   const x=parseFloat(pin.style.left)/100*width;
   const y=parseFloat(pin.style.top)/100*height;
   const prefer=x>width*.59?-1:1;
   let best=null,bestScore=Infinity;
   for(const side of [prefer,-prefer]){
    for(const distance of [17,35,56,82]){
     for(const vy of [0,-26,26,-52,52,-78,78,-107,107,-137,137]){
      const xx=side>0?x+distance:x-distance-lw;
      const yy=y-lh/2+vy;
      const box={x:xx,y:yy,w:lw,h:lh};
      let score=Math.hypot(xx+lw/2-x,yy+lh/2-y)*.34;
      // Leaving the map frame is prohibitively expensive.
      const bounds=[14-xx,xx+lw-(width-11),40-yy,yy+lh-(height-33)];
      for(const overflow of bounds)if(overflow>0)score+=10000+overflow*900;
      for(const b of placed){
       const ox=Math.max(0,Math.min(box.x+box.w+4,b.x+b.w+4)-Math.max(box.x-4,b.x-4));
       const oy=Math.max(0,Math.min(box.y+box.h+3,b.y+b.h+3)-Math.max(box.y-3,b.y-3));
       if(ox>0&&oy>0)score+=3000+ox*oy*13;
      }
      // Avoid placing a label on top of a different ski station's dot.
      for(const other of points){
       if(other===point)continue;
       const px=parseFloat(other.pin.style.left)/100*width;
       const py=parseFloat(other.pin.style.top)/100*height;
       if(px>xx-7&&px<xx+lw+7&&py>yy-7&&py<yy+lh+7)score+=700;
      }
      if(score<bestScore){best=box;bestScore=score;}
     }
    }
   }
   if(!best)continue;
   placed.push(best);
   // pin is absolute with translate(-50%,-50%), so its content coordinate
   // origin is 15 pixels before the geographic center.
   label.style.left=(best.x-x+pinSize/2).toFixed(1)+'px';
   label.style.top=(best.y-y+pinSize/2).toFixed(1)+'px';
   let leader=pin.querySelector('.alpine-pin-leader');
   if(!leader){leader=document.createElement('span');leader.className='alpine-pin-leader';leader.setAttribute('aria-hidden','true');pin.append(leader);}
   const dx=best.x+best.w/2-x,dy=best.y+best.h/2-y;
   const length=Math.hypot(dx,dy);
   leader.classList.toggle('has-leader',length>42);
   leader.style.width=Math.max(0,length-10).toFixed(1)+'px';
   leader.style.transform='rotate('+Math.atan2(dy,dx).toFixed(4)+'rad)';
  }
 }
 let layoutFrame=0;
 function scheduleLayout(){
  if(layoutFrame)cancelAnimationFrame(layoutFrame);
  layoutFrame=requestAnimationFrame(()=>{layoutFrame=0;layoutLabels();});
 }

 // Map reveal is driven by scroll itself; no timer, autoplay or library needed.
 // 176vh total section height: 24 stations reveal over ~0.76 screen of scroll.
 const pathLength=route.getTotalLength();
 route.style.strokeDasharray=String(pathLength);
 route.style.strokeDashoffset=String(pathLength);
 section.classList.add('map-ready');

 function sync(){
  raf=0;
  if(reduced.matches){
   revealThrough(points.length);
   route.style.strokeDashoffset='0';
   return;
  }
  const viewport=innerHeight;
  const s=section.getBoundingClientRect();
  const p=panel.getBoundingClientRect();
  if(s.top>viewport*.94||s.bottom<0)return;
  const fraction=narrow.matches?
   Math.max(0,Math.min(1,(viewport*.89-p.top)/(viewport*.6))):
   Math.max(0,Math.min(1,-s.top/Math.max(1,section.offsetHeight-viewport)));
  const count=Math.max(2,Math.ceil(fraction*points.length));
  revealThrough(count);
  route.style.strokeDashoffset=String(pathLength*(1-fraction));
 }
 const schedule=()=>{
  if(raf)return;
  raf=requestAnimationFrame(sync);
 };
 addEventListener('scroll',schedule,{passive:true});
 addEventListener('resize',()=>{schedule();scheduleLayout();},{passive:true});
 if(document.fonts?.ready)document.fonts.ready.then(scheduleLayout);
 if('ResizeObserver' in window)new ResizeObserver(scheduleLayout).observe(panel);

 // GSAP is enhancement only; the core reveal above works even without CDN.
 if(!reduced.matches&&!narrow.matches&&window.gsap&&window.ScrollTrigger){
  window.gsap.registerPlugin(window.ScrollTrigger);
  window.gsap.fromTo(scene,{scale:1.018},{scale:1,ease:'none',
   scrollTrigger:{trigger:section,start:'top top',end:'bottom bottom',scrub:.35}});
 }

 for(const point of points){
  const {pin}=point;
  pin.addEventListener('mouseenter',()=>{
   displayPoint(point);
   focusZone(point.zone,{selectFirst:false});
   highlight(point);
  });
  pin.addEventListener('focus',()=>{
   displayPoint(point);
   focusZone(point.zone,{selectFirst:false});
   highlight(point);
  });
  pin.addEventListener('click',()=>{
   displayPoint(point);
   focusZone(point.zone,{selectFirst:false});
   highlight(point);
   choose();
  });
 }
 for(const button of buttons){
  button.addEventListener('click',()=>{
   revealGroup(button.dataset.alpineRegion);
   schedule();
  });
 }
 if(reduced.matches)revealThrough(points.length);
 scheduleLayout();
 schedule();
})();