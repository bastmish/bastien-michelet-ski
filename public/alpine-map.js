/* V12.2 — Animated journey through all stations, Jura · Haute-Savoie · Suisse.
 * Concept inspired by Codrops scroll SVG animations, original implementation.
 * Every connected SVG segment goes through its corresponding station marker.
 * The red line is a presentation graphic, NOT a road, ski run or safe itinerary.
 */
(()=>{'use strict';
 const section=document.querySelector('.alpine-map-section');
 if(!section)return;
 const panel=section.querySelector('.alpine-map-panel');
 const scene=document.getElementById('alpine-map-scene');
 const route=document.getElementById('alpine-journey-progress');
 const pinElements=Array.from(section.querySelectorAll('.alpine-pin'));
 const buttons=Array.from(section.querySelectorAll('[data-alpine-region]'));
 const stationName=document.getElementById('alpine-active-station');
 const stationGroup=document.getElementById('alpine-active-region');
 const stationDesc=document.getElementById('alpine-active-description');
 const stationCounter=document.getElementById('alpine-active-counter');
 const stationCta=document.getElementById('alpine-station-cta');
 const hint=document.getElementById('alpine-map-hint');
 if(!panel||!scene||!route||pinElements.length===0)return;
 const groups={
  jura:['Massif du Jura','Des stations familiales de Métabief aux Rousses, jusqu’à la frontière suisse.'],
  portes:['Portes du Soleil','De Châtel aux Gets, entre villages alpins et grands domaines.'],
  grand:['Grand Massif','Entre Samoëns, Morillon et Flaine, dans la vallée du Giffre.'],
  aravis:['Massif des Aravis','La Clusaz, le Grand-Bornand et des villages de caractère.'],
  blanc:['Pays du Mont-Blanc','Megève, Saint-Gervais et la vallée de Chamonix.'],
  suisse:['Alpes suisses','Des Portes du Soleil suisses aux Alpes vaudoises et valaisannes.']
 };
 const points=pinElements.map((pin,index)=>({
  pin,index,zone:pin.dataset.alpineZone,
  name:pin.querySelector('.alpine-pin-name')?.textContent.trim()||'',
  distance:Number(pin.dataset.routeAt)||0
 }));
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 const isNarrow=matchMedia('(max-width: 950px)');
 const discovered=new Set();
 const totalDistance=route.getTotalLength();
 let active=points[0],maxRevealed=0,maxTravel=0,frame=0;
 route.style.strokeDasharray=String(totalDistance);
 route.style.strokeDashoffset=String(totalDistance);
 section.classList.add('map-ready');

 function highlight(point){
  if(!point)return;
  active?.pin.classList.remove('is-current');
  active=point;
  point.pin.classList.add('is-current');
  if(stationName)stationName.textContent=point.name;
  if(stationCounter)stationCounter.textContent=String(point.index+1).padStart(2,'0')+' / '+points.length;
  if(stationGroup)stationGroup.textContent=groups[point.zone]?.[0]||'Alpes';
  if(stationDesc)stationDesc.textContent=groups[point.zone]?.[1]||'Une journée de ski à imaginer ensemble.';
 }
 function focusZone(zone,{selectFirst=true}={}){
  if(!groups[zone])return;
  buttons.forEach(button=>{
   const selected=button.dataset.alpineRegion===zone;
   button.classList.toggle('is-current',selected);
   button.setAttribute('aria-pressed',String(selected));
  });
  points.forEach(point=>point.pin.classList.toggle('is-area',point.zone===zone));
  if(selectFirst)highlight(points.find(point=>point.zone===zone));
 }
 function revealOne(point){
  if(!point||discovered.has(point.index))return;
  discovered.add(point.index);
  point.pin.classList.add('is-revealed');
  point.pin.style.transitionDelay=(reduced.matches?'0':Math.min(140,point.index*3))+'ms';
  if(hint){
   hint.textContent=discovered.size===points.length?
    'Toutes les stations sont visibles · cliquez pour choisir':
    discovered.size+' / '+points.length+' stations · les noms restent affichés';
  }
 }
 function revealThrough(count){
  const goal=Math.min(points.length,Math.max(maxRevealed,Math.trunc(count)));
  if(goal===maxRevealed)return;
  for(let i=maxRevealed;i<goal;i++)revealOne(points[i]);
  maxRevealed=goal;
  const tip=points[goal-1];
  highlight(tip);
  focusZone(tip.zone,{selectFirst:false});
 }
 function drawThrough(distance){
  if(!Number.isFinite(distance))return;
  maxTravel=Math.max(maxTravel,Math.min(totalDistance,Math.max(0,distance)));
  route.style.strokeDashoffset=String(Math.max(0,totalDistance-maxTravel));
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
 for(const point of points){
  point.pin.addEventListener('mouseenter',()=>{
   revealThrough(point.index+1);
   revealOne(point);
   focusZone(point.zone,{selectFirst:false});
   highlight(point);
  });
  point.pin.addEventListener('focus',()=>{
   revealThrough(point.index+1);
   focusZone(point.zone,{selectFirst:false});
   highlight(point);
  });
  point.pin.addEventListener('click',()=>{
   revealThrough(point.index+1);
   drawThrough(point.distance);
   focusZone(point.zone,{selectFirst:false});
   highlight(point);
   choose();
  });
 }
 for(const button of buttons){
  button.addEventListener('click',()=>{
   const zone=button.dataset.alpineRegion;
   const matches=points.filter(point=>point.zone===zone);
   if(!matches.length)return;
   const last=matches[matches.length-1];
   revealThrough(last.index+1);
   drawThrough(last.distance);
   focusZone(zone,{selectFirst:false});
   highlight(matches[0]);
  });
 }
 // Label fitting is computed for all points, so an appearing name does not move
 // its neighbors as the scroll progresses. Leader lines make dense clusters legible.
 function layoutLabels(){
  const width=panel.clientWidth,height=panel.clientHeight;
  if(width<1||height<1)return;
  const placed=[];
  const pinSize=points[0]?.pin.offsetWidth||25;
  const ordered=points.slice().sort((a,b)=>{
   const ay=parseFloat(a.pin.style.top),by=parseFloat(b.pin.style.top);
   return ay-by||parseFloat(a.pin.style.left)-parseFloat(b.pin.style.left);
  });
  const positions=points.map(p=>({
   x:parseFloat(p.pin.style.left)/100*width,
   y:parseFloat(p.pin.style.top)/100*height
  }));
  for(const point of ordered){
   const pin=point.pin,label=pin.querySelector('.alpine-pin-name');
   if(!label)continue;
   label.style.left='';label.style.top='';label.style.right='auto';
   const lw=label.offsetWidth||Math.max(55,point.name.length*6+13);
   const lh=label.offsetHeight||21;
   const px=positions[point.index].x,py=positions[point.index].y;
   let winner=null,scoreBest=Infinity;
   const preferred=px>width*.62?-1:1;
   for(const side of [preferred,-preferred]){
    for(const dist of [14,29,47,69,95,122,145]){
     for(const dy of [0,-22,22,-44,44,-66,66,-88,88,-113,113,-141,141,-172,172,-205,205]){
      const x=side>0?px+dist:px-dist-lw;
      const y=py-lh/2+dy;
      let score=Math.hypot(x+lw/2-px,y+lh/2-py)*.38;
      for(const n of [14-x,x+lw-(width-15),42-y,y+lh-(height-40)]){
       if(n>0)score+=9000+n*700;
      }
      for(const b of placed){
       const ox=Math.max(0,Math.min(x+lw+3,b.x+b.w+3)-Math.max(x-3,b.x-3));
       const oy=Math.max(0,Math.min(y+lh+2,b.y+b.h+2)-Math.max(y-2,b.y-2));
       if(ox>0&&oy>0)score+=7000+ox*oy*24;
      }
      for(let i=0;i<positions.length;i++){
       if(i===point.index)continue;
       const q=positions[i];
       if(q.x>x-6&&q.x<x+lw+6&&q.y>y-7&&q.y<y+lh+7)score+=1400;
      }
      if(score<scoreBest){scoreBest=score;winner={x,y,w:lw,h:lh};}
     }
    }
   }
   if(!winner)continue;
   placed.push(winner);
   label.style.left=(winner.x-px+pinSize/2).toFixed(1)+'px';
   label.style.top=(winner.y-py+pinSize/2).toFixed(1)+'px';
   let leader=pin.querySelector('.alpine-pin-leader');
   if(!leader){
    leader=document.createElement('span');
    leader.className='alpine-pin-leader';
    leader.setAttribute('aria-hidden','true');
    pin.append(leader);
   }
   const dx=winner.x+winner.w/2-px,dy=winner.y+winner.h/2-py;
   const dist=Math.hypot(dx,dy);
   leader.classList.toggle('has-leader',dist>38);
   leader.style.width=Math.max(0,dist-10).toFixed(1)+'px';
   leader.style.transform='rotate('+Math.atan2(dy,dx).toFixed(4)+'rad)';
  }
 }
 let labelFrame=0;
 function scheduleLabels(){
  if(labelFrame)cancelAnimationFrame(labelFrame);
  labelFrame=requestAnimationFrame(()=>{labelFrame=0;layoutLabels();});
 }
 // A quick, native scroll reveal: ~0.7 viewport of scrolling for 40 stations.
 // Progress is monotonic so the names AND the route never disappear on reverse.
 function syncScroll(){
  frame=0;
  if(reduced.matches){
   revealThrough(points.length);drawThrough(totalDistance);return;
  }
  const vh=innerHeight,rect=panel.getBoundingClientRect();
  if(rect.top>vh*.97||rect.bottom<0)return;
  const progress=Math.max(0,Math.min(1,(vh*.91-rect.top)/(vh*.74)));
  const segment=progress*(points.length-1);
  const index=Math.min(points.length-1,Math.floor(segment));
  const next=Math.min(points.length-1,index+1);
  const interpolation=Math.max(0,segment-index);
  const start=points[index].distance,end=points[next].distance;
  const routeAt=start+(end-start)*interpolation;
  revealThrough(index+1);
  drawThrough(routeAt);
 }
 function scheduleScroll(){
  if(frame)return;
  frame=requestAnimationFrame(syncScroll);
 }
 addEventListener('scroll',scheduleScroll,{passive:true});
 addEventListener('resize',()=>{scheduleScroll();scheduleLabels();},{passive:true});
 if('ResizeObserver' in window)new ResizeObserver(scheduleLabels).observe(panel);
 if(document.fonts?.ready)document.fonts.ready.then(scheduleLabels);
 // GSAP is strictly optional enhancement. The marker and route animation works
 // without any external library.
 if(!reduced.matches&&!isNarrow.matches&&window.gsap&&window.ScrollTrigger){
  window.gsap.registerPlugin(window.ScrollTrigger);
  window.gsap.fromTo(scene,{scale:1.012},{scale:1,ease:'none',scrollTrigger:{
   trigger:panel,start:'top 90%',end:'top 17%',scrub:.35
  }});
 }
 focusZone(points[0].zone);
 if(reduced.matches){revealThrough(points.length);drawThrough(totalDistance);}
 scheduleLabels();scheduleScroll();
})();