// 컴퓨터 없이 쇼핑몰 페이지를 읽는 도구 (작업 공간의 Playwright Chromium 사용, 설치 불필요)
// 사용: node tools/shop.js <url> [scrolls=6] [mobile|desktop]
// 출력(JSON): {status, url, meta:{price,sale_rate,title}, links:[{href,text}], text}
//  - 무신사 상품: meta.price / meta.sale_rate 가 정확한 판매가·할인율
//  - 무신사 랭킹: https://www.musinsa.com/main/musinsa/ranking?gf=F (또는 gf=M) → links 의 /products/ID
//  - 29CM 베스트: https://www.29cm.co.kr/best-products?period=HOURLY&ranking=POPULARITY&gender=F&age=ALL → links 의 /product/catalog/ID (여성의류·가방·슈즈 외 카테고리는 걸러서 쓰기)
//  - 크림: https://kream.co.kr/search?shop_category_id=34&sort=popular
//  - 지그재그: https://zigzag.kr/search?keyword=패딩 (랭킹 페이지는 막혀 있음)
const {chromium}=require('playwright');
(async()=>{
  const [url, sc='6', mode='desktop']=process.argv.slice(2);
  const b=await chromium.launch({args:['--disable-blink-features=AutomationControlled']});
  const mob=mode==='mobile';
  const ctx=await b.newContext({locale:'ko-KR',timezoneId:'Asia/Seoul',viewport:mob?{width:430,height:930}:{width:1280,height:900},isMobile:mob,
    userAgent:mob?'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'});
  const p=await ctx.newPage(); let status=0;
  try{const r=await p.goto(url,{waitUntil:'domcontentloaded',timeout:45000}); status=r?r.status():0; await p.waitForTimeout(4000);
    for(let i=0;i<+sc;i++){await p.mouse.wheel(0,1200); await p.waitForTimeout(1100);} }catch(e){status='ERR '+e.message.slice(0,100)}
  const out=await p.evaluate(()=>{const m=n=>{const e=document.querySelector(`meta[property="${n}"]`);return e?e.content:''};
    const seen=new Set(); const links=[];
    for(const a of document.querySelectorAll('a[href]')){const h=a.href; if(!/\/products?\/|catalog|\/product\//.test(h)) continue; const t=a.innerText.replace(/\s+/g,' ').trim(); if(!t) continue; const k=h+t; if(seen.has(k)) continue; seen.add(k); links.push({href:h,text:t.slice(0,160)}); if(links.length>=80) break;}
    return {meta:{price:m('product:price:amount'),sale_rate:m('product:price:sale_rate'),title:m('og:title')},links,text:document.body.innerText.replace(/\s+/g,' ').slice(0,6000)}});
  console.log(JSON.stringify({status,url,...out},null,1)); await b.close();
})();
