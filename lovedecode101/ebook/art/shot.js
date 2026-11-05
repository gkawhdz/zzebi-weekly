const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1600,height:900}});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(500);
for(const id of ['a1','a2']){const el=await p.$('#'+id);await el.screenshot({path:'detail_'+id+'.png'});}
await b.close();})();
