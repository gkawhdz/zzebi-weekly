const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(800);
for(let i=1;i<=10;i++){const el=await p.$('#s'+i);await el.screenshot({path:process.argv[3]+'/slide_'+String(i).padStart(2,'0')+'.png'});}
await b.close();})();
