const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/ad.html'); await p.waitForTimeout(500);
const N=Math.round(23.5*30);
for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/30); await p.screenshot({path:`fr/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close();})();
