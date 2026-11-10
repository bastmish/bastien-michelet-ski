/* Ski Society V15: original alpine terrain experience.
 * Open-source MapLibre + free Maptoolkit Winter 3D style. The visual
 * inspiration is Harris Mountains Heli-Ski; no code/assets were copied.
 * Resort markers are illustrative and do not assert instructor availability.
 */
import * as maplibregl from "https://cdn.jsdelivr.net/npm/maplibre-gl@6.16.0/dist/maplibre-gl.mjs";

const resorts=[
 ["Les Rousses","jura",6.063,46.484,1],["Métabief","jura",6.350,46.774,1],
 ["Megève","haute-savoie",6.618,45.857,1],["Chamonix","haute-savoie",6.869,45.922,1],
 ["La Clusaz","haute-savoie",6.425,45.907,0],["Avoriaz","haute-savoie",6.774,46.192,1],
 ["Courchevel","savoie",6.634,45.415,1],["Méribel","savoie",6.566,45.394,0],
 ["Les Arcs","savoie",6.830,45.573,0],["Tignes","savoie",6.915,45.469,0],
 ["Val d’Isère","savoie",7.000,45.448,1],["Val Thorens","savoie",6.580,45.298,1],
 ["Serre Chevalier","hautes-alpes",6.587,44.940,1],
 ["Montgenèvre","hautes-alpes",6.723,44.931,0],["Vars","hautes-alpes",6.689,44.572,1]
].map(([name,zone,lon,lat,featured])=>({name,zone,lon,lat,featured:!!featured}));
const camera={
 jura:{bounds:[[5.83,46.34],[6.51,46.91]],pitch:48},
 "haute-savoie":{bounds:[[6.28,45.68],[7.07,46.28]],pitch:55},
 savoie:{bounds:[[6.40,45.19],[7.15,45.72]],pitch:54},
 "hautes-alpes":{bounds:[[6.29,44.40],[6.94,45.12]],pitch:53}
};
const regionName={jura:"JURA","haute-savoie":"HAUTE-SAVOIE",savoie:"SAVOIE","hautes-alpes":"HAUTES-ALPES"};
const root=document.querySelector('.society-map');
if(root){
 const mapElement=root.querySelector('#society-terrain-map');
 const frame=root.querySelector('#society-terrain-frame');
 const status=root.querySelector('#society-map-status');
 const badge=root.querySelector('#society-map-badge');
 const btns=[...root.querySelectorAll('[data-society-region]')];
 const nameText=root.querySelector('#society-selected-station');
 const regionText=root.querySelector('#society-selected-area');
 const countText=root.querySelector('#society-selected-count');
 const summaryText=root.querySelector('#society-selected-description');
 const requestButton=root.querySelector('#society-selected-button');
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 let selected=resorts.find(r=>r.name==="Megève");
 let map=null,started=false,markers=[];
 let requestedArea=selected.zone;
 function showSelection(resort){
  if(!resort)return;
  selected=resort;requestedArea=resort.zone;
  const b=btns.find(btn=>btn.dataset.societyRegion===selected.zone);
  btns.forEach(btn=>{
   const active=btn===b;
   btn.classList.toggle('is-active',active);
   btn.setAttribute('aria-pressed',String(active));
  });
  if(nameText)nameText.textContent=resort.name;
  if(regionText)regionText.textContent=b?.querySelector('span:nth-child(2)')?.textContent||'Alpes';
  if(countText)countText.textContent=String(resorts.filter(r=>r.zone===resort.zone).length).padStart(2,'0')+" STATIONS REPÈRES";
  if(summaryText)summaryText.textContent=b?.dataset.societySummary||'Une expérience à préparer selon vos envies.';
  if(badge)badge.textContent=regionName[resort.zone]||'ALPES FRANÇAISES';
  for(const {resort:r,element:e} of markers){
   e.classList.toggle('is-selected',r===resort);
   e.classList.toggle('is-secondary',r.zone!==resort.zone);
   e.classList.toggle('is-in-zone',r.zone===resort.zone);
   e.setAttribute('aria-pressed',String(r===resort));
  }
  if(map?.getLayer('society-coverage-fill')){
   map.setPaintProperty('society-coverage-fill','fill-opacity',['case',['==',['get','zone'],resort.zone],0.19,0.015]);
   map.setPaintProperty('society-coverage-line','line-opacity',['case',['==',['get','zone'],resort.zone],0.65,0.10]);
  }
 }
 function goToRequest(){
  const select=document.getElementById('request-destination');
  const station=document.getElementById('request-station');
  if(select&&station){
   select.value="J'ai une station en tête";
   select.dispatchEvent(new Event('change',{bubbles:true}));
   station.value=selected.name;
   station.dispatchEvent(new Event('input',{bubbles:true}));
  }
  document.getElementById('reservation')?.scrollIntoView({behavior:reduced.matches?'auto':'smooth',block:'start'});
 }
 function moveToArea(id){
  if(!map)return;
  const view=camera[id];if(!view)return;
  map.fitBounds(view.bounds,{
   padding:{top:72,bottom:65,left:49,right:49},
   duration:reduced.matches?0:950,maxZoom:10.2,pitch:view.pitch,bearing:-11,
   essential:true
  });
 }
 function selectArea(id){
  const next=resorts.find(r=>r.zone===id&&r.featured)||resorts.find(r=>r.zone===id);
  if(next)showSelection(next);
  if(!started)startMap();else moveToArea(id);
 }
 for(const b of btns)b.addEventListener('click',()=>selectArea(b.dataset.societyRegion));
 requestButton?.addEventListener('click',goToRequest);
 function createMarkers(){
  for(const resort of resorts){
   const e=document.createElement('button');
   e.type='button';
   e.className='society-geo-marker'+(resort.featured?' is-featured':'');
   e.setAttribute('aria-label',resort.name+' : demander un cours privé ici');
   e.title=resort.name;
   const dot=document.createElement('span');
   dot.className='society-geo-dot';dot.setAttribute('aria-hidden','true');
   const label=document.createElement('span');
   label.className='society-geo-label';label.textContent=resort.name;label.setAttribute('aria-hidden','true');
   e.append(dot,label);
   e.addEventListener('click',ev=>{ev.stopPropagation();showSelection(resort);goToRequest();});
   e.addEventListener('mouseenter',()=>showSelection(resort));
   e.addEventListener('focus',()=>showSelection(resort));
   new maplibregl.Marker({element:e,anchor:'center'}).setLngLat([resort.lon,resort.lat]).addTo(map);
   markers.push({resort,element:e});
  }
  showSelection(selected);
 }
 async function overlayCoverage(){
  try{
   const response=await fetch('ski-regions.geojson');
   if(!response.ok)throw new Error('Coverage source '+response.status);
   const data=await response.json();
   if(!map||map.getSource('society-coverage'))return;
   map.addSource('society-coverage',{type:'geojson',data});
   map.addLayer({id:'society-coverage-fill',type:'fill',source:'society-coverage',
    paint:{'fill-color':'#ba8c66','fill-opacity':['case',['==',['get','zone'],selected.zone],0.19,0.015]}});
   map.addLayer({id:'society-coverage-line',type:'line',source:'society-coverage',
    paint:{'line-color':'#9f754f','line-width':1.25,
     'line-opacity':['case',['==',['get','zone'],selected.zone],0.65,0.10]}});
  }catch(error){console.warn('Optional Ski Society department overlay:',error);}
 }
 function startMap(){
  if(started||!mapElement)return;
  started=true;
  if(!maplibregl.supported()){
   if(status)status.textContent='Le relief interactif n’est pas disponible sur ce navigateur. Les demandes restent accessibles.';
   return;
  }
  try{
   map=new maplibregl.Map({
    container:mapElement,
    style:'https://styles.maptoolkit.org/winter-3d.json',
    center:[6.49,45.84],zoom:7.1,pitch:46,bearing:-11,
    minZoom:5.5,maxZoom:14,maxPitch:75,antialias:true,
    attributionControl:{compact:false,customAttribution:''}
   });
   map.scrollZoom.disable();
   map.addControl(new maplibregl.NavigationControl({showCompass:true,visualizePitch:true}),'top-right');
   map.once('load',()=>{
    try{
     // The winter style retains its native alpine terrain and relief.
     // Hide only cluttering road & commercial POI labels.
     for(const layer of map.getStyle().layers||[]){
      if(layer.type==='symbol'&&/(poi|house(number)?|road[_-]?name|transport|rail)/i.test(layer.id))
       map.setLayoutProperty(layer.id,'visibility','none');
     }
     createMarkers();
     overlayCoverage();
     if(frame)frame.classList.add('is-loaded');
     if(status)status.hidden=true;
     if(requestedArea!=='haute-savoie')moveToArea(requestedArea);
    }catch(error){
     if(status){status.hidden=false;status.textContent='Carte partiellement disponible. Le formulaire de demande reste accessible.';}
     console.warn('Ski Society terrain rendering:',error);
    }
   });
   map.on('error',event=>{
    if(!frame?.classList.contains('is-loaded')&&status)
     status.textContent='Chargement du relief en cours. Vous pouvez déjà choisir votre région.';
    if(event.error)console.warn('Ski Society map tiles:',event.error);
   });
  }catch(error){
   if(status)status.textContent='Relief momentanément indisponible. Choisissez une région et contactez-nous.';
   console.warn('Ski Society map:',error);
  }
 }
 showSelection(selected);
 if('IntersectionObserver' in window){
  const observer=new IntersectionObserver(entries=>{
   if(entries.some(e=>e.isIntersecting)){startMap();observer.disconnect();}
  },{rootMargin:'280px'});
  observer.observe(root);
 }else startMap();
}
