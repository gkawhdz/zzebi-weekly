const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
await p.goto('file://'+__dirname+'/car.html'); await p.waitForTimeout(600);
for(let i=1;i<=7;i++){await (await p.$('#s'+i)).screenshot({path:`zzebi_free_${i}.jpg`,type:'jpeg',quality:92});}
await b.close();})();
