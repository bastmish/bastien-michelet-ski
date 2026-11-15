/* Ski Society — local, accessible station search. No remote API or personal data transfer. */
(function(){
 'use strict';
 const input=document.getElementById('station-search');
 const list=document.getElementById('station-suggestions');
 const clear=document.getElementById('station-search-clear');
 const reset=document.getElementById('station-reset');
 const emptyReset=document.getElementById('stations-empty-reset');
 const empty=document.getElementById('stations-empty');
 const count=document.getElementById('station-results-count');
 if(!input||!list||!count)return;
 const sections=[...document.querySelectorAll('.ss-territory')];
 const cards=sections.flatMap(section=>[...section.querySelectorAll('.ss-resort')].map(element=>({
  element,section,name:element.dataset.name||'',region:element.dataset.region||'',
  search:element.dataset.search||''
 })));
 const buttons=[...document.querySelectorAll('.ss-territory-filter')];
 const normal=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('fr').replace(/[–—-]/g,' ').replace(/\s+/g,' ').trim();
 let region='all',query='',selected=null,active=-1,results=[];
 function announce(){
  let visible=0;
  sections.forEach(section=>{
   const shown=cards.filter(item=>item.section===section&&!item.element.hidden).length;
   section.hidden=shown===0;
   const label=section.querySelector('.ss-territory-visible');
   if(label)label.textContent=shown;
   visible+=shown;
  });
  count.textContent=visible+' station'+(visible>1?'s':'')+' '+(query||region!=='all'?'correspondant à votre recherche':'à explorer');
  empty.hidden=visible!==0;
  reset.hidden=!query&&region==='all';
  clear.hidden=!input.value;
 }
 function apply(){
  cards.forEach(item=>{
   const matchesRegion=region==='all'||item.region===region;
   const matchesSearch=!query||normal(item.name+' '+item.region+' '+item.search).includes(normal(query));
   item.element.hidden=!(matchesRegion&&matchesSearch&&(selected===null||item===selected));
  });
  announce();
 }
 function closeList(){
  list.hidden=true;list.replaceChildren();
  input.setAttribute('aria-expanded','false');input.removeAttribute('aria-activedescendant');
  active=-1;results=[];
 }
 function pick(item){
  input.value=item.name;query=item.name;selected=item;region='all';
  buttons.forEach(btn=>{const isActive=btn.dataset.filter==='all';btn.classList.toggle('is-active',isActive);btn.setAttribute('aria-pressed',String(isActive));});
  closeList();apply();
  const target=item.element;
  if(target){target.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'center'});}
 }
 function suggestions(){
  closeList();
  const term=normal(input.value);
  if(!term)return;
  // Prefix matches first, then the remaining substring matches.
  results=cards.filter(item=>normal(item.name).includes(term)).sort((a,b)=>{
   const aa=normal(a.name).startsWith(term)?0:1,bb=normal(b.name).startsWith(term)?0:1;
   return aa-bb||a.name.localeCompare(b.name,'fr');
  }).slice(0,8);
  if(!results.length)return;
  const frag=document.createDocumentFragment();
  results.forEach((item,index)=>{
   const option=document.createElement('button');option.type='button';option.className='ss-suggestion';
   option.setAttribute('role','option');option.setAttribute('aria-selected','false');option.id='station-suggestion-'+index;
   const name=document.createElement('span');name.textContent=item.name;
   const region=document.createElement('small');region.textContent=item.region;
   option.append(name,region);
   option.addEventListener('mousedown',e=>e.preventDefault());
   option.addEventListener('click',()=>pick(item));
   frag.appendChild(option);
  });
  list.appendChild(frag);list.hidden=false;input.setAttribute('aria-expanded','true');
 }
 function resetAll(){
  input.value='';query='';selected=null;region='all';
  buttons.forEach(btn=>{const yes=btn.dataset.filter==='all';btn.classList.toggle('is-active',yes);btn.setAttribute('aria-pressed',String(yes));});
  closeList();apply();input.focus();
 }
 input.addEventListener('input',()=>{
  query=input.value.trim();selected=null;apply();suggestions();
 });
 input.addEventListener('keydown',e=>{
  if(e.key==='Escape'){closeList();return;}
  if(list.hidden||!results.length)return;
  if(e.key==='ArrowDown'||e.key==='ArrowUp'){
   e.preventDefault();active=e.key==='ArrowDown'?(active+1)%results.length:(active+results.length-1)%results.length;
   [...list.children].forEach((node,i)=>node.setAttribute('aria-selected',String(i===active)));
   input.setAttribute('aria-activedescendant','station-suggestion-'+active);
  }else if(e.key==='Enter'){
   e.preventDefault();pick(results[active<0?0:active]);
  }
 });
 input.addEventListener('blur',()=>{ // The click handler runs before blur when a suggestion is selected.
  if(!list.matches(':hover'))closeList();
 });
 document.addEventListener('click',e=>{if(!e.target.closest('.ss-resort-search'))closeList();});
 clear.addEventListener('click',resetAll);reset.addEventListener('click',resetAll);
 if(emptyReset)emptyReset.addEventListener('click',resetAll);
 buttons.forEach(button=>button.addEventListener('click',()=>{
  region=button.dataset.filter||'all';selected=null;input.value='';query='';
  buttons.forEach(btn=>{const on=btn===button;btn.classList.toggle('is-active',on);btn.setAttribute('aria-pressed',String(on));});
  closeList();apply();
 }));
 apply();
})();