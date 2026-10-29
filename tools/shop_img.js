// 상품 페이지의 대표 사진을 저장 (상품 매칭 비교용)
// 사용: node tools/shop_img.js <상품url> <저장.jpg>
// og:image → 없으면 화면에서 가장 큰 상품 이미지. 출력 JSON {ok, src, title, price, sale_rate, soldout}
const {chromium}=require('playwright');
(async()=>{
  const [url,out]=process.argv.slice(2);
  const b=await chromium.launch({args:['--disable-blink-features=AutomationControlled']});
  const ctx=await b.newContext({locale:'ko-KR',timezoneId:'Asia/Seoul',viewport:{width:430,height:930},isMobile:true,
    userAgent:'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'});
  const p=await ctx.newPage(); const res={ok:false,url};
  try{
    await p.goto(url,{waitUntil:'domcontentloaded',timeout:45000}); await p.waitForTimeout(3500);
    const info=await p.evaluate(()=>{const m=n=>{const e=document.querySelector(`meta[property="${n}"]`)||document.querySelector(`meta[name="${n}"]`);return e?e.content:''};
      let src=m('og:image');
      if(!src){let best=null,ba=0;for(const i of document.images){const r=i.getBoundingClientRect();const a=r.width*r.height;if(a>ba&&i.naturalWidth>200){ba=a;best=i}} if(best) src=best.currentSrc||best.src;}
      const t=document.body.innerText;
      return {src,title:m('og:title')||document.title,price:m('product:price:amount'),sale_rate:m('product:price:sale_rate'),
        soldout:/품절|SOLD OUT|Sold out|일시품절|판매 ?종료/.test(t.slice(0,4000))}});
    Object.assign(res,info);
    if(info.src){
      const r=await p.goto(info.src,{timeout:30000}); await p.waitForTimeout(800);
      const img=await p.$('img');
      if(img){await img.screenshot({path:out,type:'jpeg',quality:85}); res.ok=true;}
      else if(r){require('fs').writeFileSync(out,await r.body()); res.ok=true;}
    }
  }catch(e){res.error=String(e.message).slice(0,120)}
  console.log(JSON.stringify(res)); await b.close();
})();
