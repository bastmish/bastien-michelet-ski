/* Ski Society – dithered mountain layers, original vanilla Canvas implementation.
   Inspired by the supplied Ridgeline Dither Footer concept, no React dependency. */
(()=>{"use strict";
const root=document.querySelector(".ss-ridge-footer");
if(!root)return;
const canvas=root.querySelector(".ss-ridge-scene canvas"),scene=root.querySelector(".ss-ridge-scene");
if(!canvas||!scene)return;
const ctx=canvas.getContext("2d",{alpha:false});
if(!ctx)return;
const paper=[255,255,255],tones=[[255,255,255],[247,248,247],[230,232,231],[199,203,202],[150,156,156],[99,106,109],[35,39,42]];
const bayer=[0,32,8,40,48,16,56,24,12,44,4,36,60,28,52,20,3,35,11,43,51,19,59,27,15,47,7,39,63,31,55,23,2,34,10,42,50,18,58,26,14,46,6,38,62,30,54,22,1,33,9,41,49,17,57,25,13,45,5,37,61,29,53,21];
const reduce=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
let frame=0,visible=false,revealed=reduce,start=0;
function hash(x,y,s){let n=Math.sin(x*127.1+y*311.7+s*43.13)*43758.5453;return n-Math.floor(n)}
function ridge(x,layer,w,h){const u=x/w,k=layer/5;const slow=Math.sin(u*Math.PI*(2.6+k*.9)+layer*.75)*.52;const medium=Math.sin(u*Math.PI*(9+layer)+layer*1.8)*.23;const fine=Math.sin(u*Math.PI*(21+layer*2)+layer*3)*.10;const grit=(hash(Math.floor(u*63),layer,9)-.5)*.06;const depth=(.35+layer*.105)*h;return depth-(slow+medium+fine+grit)*h*(.06+.025*k)}
function draw(){const rect=scene.getBoundingClientRect(),step=3,W=Math.max(80,Math.round(rect.width/step)),H=Math.max(45,Math.round(rect.height/step));canvas.width=W;canvas.height=H;const out=ctx.createImageData(W,H),arr=out.data;const t=reduce?1:Math.min(1,(performance.now()-start)/1700);
for(let y=0;y<H;y++){let fade=Math.min(1,Math.max(0,(y/H-.02)/.28));for(let x=0;x<W;x++){let layer=-1;for(let i=5;i>=0;i--){if(y>=ridge(x,i,W,H)){layer=i;break}}let strength=layer<0?0:(.16+layer*.12)*fade*t;const dusk=layer>=0?Math.max(0,Math.min(1,(y-ridge(x,layer,W,H))/(H*.35))):0;strength*=1-.24*dusk;let val=strength*6+(bayer[(y%8)*8+x%8]+.5)/64;let index=Math.min(6,Math.max(0,Math.floor(val))),rgb=tones[index],p=(y*W+x)*4;arr[p]=rgb[0];arr[p+1]=rgb[1];arr[p+2]=rgb[2];arr[p+3]=255}}
ctx.putImageData(out,0,0);
if(!reduce&&t<1)frame=requestAnimationFrame(draw)
}
const observer=new IntersectionObserver(entries=>{visible=entries.some(e=>e.isIntersecting);if(visible&&!revealed){revealed=true;start=performance.now();draw()}},{threshold:.1});
observer.observe(root);
const resize=new ResizeObserver(()=>{if(revealed){cancelAnimationFrame(frame);if(!start)start=performance.now()-2000;draw()}});
resize.observe(scene);
document.addEventListener("visibilitychange",()=>{if(!document.hidden&&revealed)draw()});
if(reduce){start=performance.now()-2000;draw()}
})();
