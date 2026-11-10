/* Ski Society: scroll-linked timeline, no React dependency.
   The content is always in the DOM and readable even without JS. */
(()=>{'use strict';const root=document.querySelector('.ss-scroll-story');if(!root)return;
const track=root.querySelector('.ss-story-track'),steps=[...root.querySelectorAll('.ss-story-step')];if(!track||!steps.length)return;
if(!('IntersectionObserver'in window)||window.matchMedia('(prefers-reduced-motion: reduce)').matches){root.style.setProperty('--ss-progress','100%');steps.forEach(s=>s.classList.add('is-active'));return}
let ticking=false;
function update(){ticking=false;const rect=track.getBoundingClientRect();const focus=Math.min(window.innerHeight*.52,460);const total=Math.max(1,rect.height-100);const progress=Math.max(0,Math.min(1,(focus-rect.top-35)/total));track.style.setProperty('--ss-progress',(progress*100).toFixed(2)+'%');
let current=0;steps.forEach((step,i)=>{const r=step.getBoundingClientRect();if(r.top<=focus)current=i});steps.forEach((s,i)=>{s.classList.toggle('is-active',i===current);s.classList.toggle('is-passed',i<current)});
}
function schedule(){if(!ticking){ticking=true;requestAnimationFrame(update)}}
window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule,{passive:true});update();
})();
