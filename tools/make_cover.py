#!/usr/bin/env python3
"""Zzebi.St 위클리 인스타 공지 캐러셀 (매거진 커버형, 4:5 1080x1350 × 5장)

사용: python3 tools/make_cover.py DATA_DIR OUT_DIR --vol 1 --period "2026.10.29-11.01" --hero w15 --feature w15:1
  DATA_DIR : 이번 주 데이터(meta.json, look_*.json, market.json, img/)
  --period : 리포트 기간 "YYYY.MM.DD-MM.DD" (월~일)
  --hero   : 커버 사진으로 쓸 룩 id
  --feature: 3장 '가격 비교'에 쓸 룩 id:핵심아이템 번호(1|2)
결과: OUT_DIR/slide1.jpg … slide5.jpg (+ slides.html)
1장 = 패션 잡지 표지(마스트헤드·기간·커버 라인), 2장 = 이번 주 목차, 3장 = 명품→가성비 가격, 4장 = 핫딜, 5장 = 받는 법.
"""
import sys, os, json, glob, base64, io, argparse, html, datetime, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
esc = lambda s: html.escape(str(s or ''))
WD = '월화수목금토일'

def img_uri(p, w=1080, q=86):
    from PIL import Image
    im = Image.open(p).convert('RGB')
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q); return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

def font_uri(name):
    return 'data:font/woff2;base64,' + base64.b64encode(open(os.path.join(ROOT, 'tools', 'fonts', name), 'rb').read()).decode()

def won(w, ap=False):
    if ap or w >= 1_000_000:
        m = w / 10000
        return (f'{m:,.0f}만원' if m >= 100 else f'{m:.1f}만원'.replace('.0만', '만'))
    return f'{w:,}원'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('data'); ap.add_argument('out')
    ap.add_argument('--vol', type=int, default=1)
    ap.add_argument('--period', required=True)
    ap.add_argument('--hero', required=True)
    ap.add_argument('--feature', required=True)
    a = ap.parse_args()
    D = a.data
    meta = json.load(open(os.path.join(D, 'meta.json')))
    mk = json.load(open(os.path.join(D, 'market.json')))
    looks = {os.path.basename(f)[5:-5]: json.load(open(f)) for f in glob.glob(os.path.join(D, 'look_*.json'))}
    order = meta['women'] + meta['men']
    y, rest = a.period.split('.', 1)
    s, e = rest.split('-')
    sd = datetime.date(int(y), int(s.split('.')[0]), int(s.split('.')[1]))
    ed = datetime.date(int(y) + (1 if int(e.split('.')[0]) < sd.month else 0), int(e.split('.')[0]), int(e.split('.')[1]))
    per_en = f'{sd:%Y.%m.%d} — {ed:%m.%d}'
    per_ko = f'{sd.month}월 {sd.day}일({WD[sd.weekday()]}) ~ {ed.month}월 {ed.day}일({WD[ed.weekday()]})'
    hero = looks[a.hero]
    fid, fno = a.feature.split(':')
    F = looks[fid]; core = F['cores'][int(fno) - 1]
    tiers = core['tiers']
    lux, val = tiers.get('lux') or tiers.get('mid'), tiers.get('value') or tiers.get('mid')
    deals = sorted((mk.get('deals_women', [])[:6] + mk.get('deals_men', [])[:6]), key=lambda p: -int(p.get('off') or 0))[:4]
    imgs = {i: img_uri(os.path.join(D, 'img', looks[i]['img']), 720, 82) for i in order}
    hero_img = img_uri(os.path.join(D, 'img', hero['img']), 1080, 88)
    feat_img = img_uri(os.path.join(D, 'img', F['img']), 1080, 86)
    n_look = len(order)

    css = f'''
@font-face{{font-family:Bod;src:url({font_uri('bodoni-moda-latin-900-normal.woff2')});font-weight:900}}
@font-face{{font-family:Bod;src:url({font_uri('bodoni-moda-latin-700-normal.woff2')});font-weight:700}}
@font-face{{font-family:Bod;src:url({font_uri('bodoni-moda-latin-400-normal.woff2')});font-weight:400}}
@font-face{{font-family:Bod;src:url({font_uri('bodoni-moda-latin-400-italic.woff2')});font-weight:400;font-style:italic}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#222;word-break:keep-all}}
.s{{width:1080px;height:1350px;position:relative;overflow:hidden;background:#F5F1EA;color:#141414;font-family:"Noto Sans CJK KR",sans-serif;margin-bottom:20px}}
.serif{{font-family:"Noto Serif CJK KR",serif}}
.bod{{font-family:Bod,"Noto Serif CJK KR",serif}}
.teal{{color:#00A8A8}}
/* 1 cover */
.c1 .ph{{position:absolute;inset:0;background:url({hero_img}) center 62%/cover}}
.c1 .sh{{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(0,0,0,.42) 0%,rgba(0,0,0,0) 30%,rgba(0,0,0,0) 52%,rgba(0,0,0,.72) 100%)}}
.c1 .top{{position:absolute;left:56px;right:56px;top:44px;display:flex;justify-content:space-between;color:#fff;font:600 22px Inter,sans-serif;letter-spacing:.28em}}
.c1 .mast{{position:absolute;left:40px;right:40px;top:70px;color:#fff;font:900 214px/1 Bod,serif;letter-spacing:-.02em;text-align:center}}
.c1 .mast em{{font-style:normal;color:#5FE0DC}}
.c1 .per{{position:absolute;left:0;right:0;top:300px;text-align:center;color:#fff;font:400 30px Bod,serif;letter-spacing:.12em}}
.c1 .per b{{font:700 21px Inter,sans-serif;letter-spacing:.3em;margin-right:14px;padding:6px 12px;border:1.5px solid #fff}}
.c1 .lines{{position:absolute;left:56px;bottom:200px;color:#fff;max-width:640px}}
.c1 .kick{{font:400 italic 34px Bod,serif;margin-bottom:10px;color:#5FE0DC}}
.c1 .hl{{font-family:"Noto Serif CJK KR",serif;font-weight:900;font-size:86px;line-height:1.12;letter-spacing:-.02em;text-shadow:0 2px 24px rgba(0,0,0,.35)}}
.c1 .cl{{position:absolute;right:56px;bottom:214px;text-align:right;color:#fff;font-size:27px;font-weight:700;line-height:1.55}}
.c1 .cl span{{display:block;border-top:1.5px solid rgba(255,255,255,.7);padding-top:6px;margin-top:10px}}
.c1 .cl small{{display:block;font:600 18px Inter,sans-serif;letter-spacing:.2em;opacity:.85}}
.c1 .bot{{position:absolute;left:56px;right:56px;bottom:56px;display:flex;align-items:center;justify-content:space-between;color:#fff}}
.pill{{display:inline-flex;align-items:center;gap:14px;background:#007C7C;color:#fff;border-radius:999px;padding:20px 34px;font-size:32px;font-weight:900}}
.c1 .bar{{display:flex;align-items:flex-end;gap:3px;height:62px}}
.c1 .bar i{{display:block;background:#fff;height:100%}}
.c1 .ai{{position:absolute;right:56px;top:362px;color:#fff;font-size:18px;opacity:.85}}
/* common page */
.hd{{position:absolute;left:64px;right:64px;top:56px;display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid #141414;padding-bottom:18px}}
.hd .m{{font:900 52px Bod,serif}} .hd .m em{{font-style:normal;color:#00A8A8}}
.hd .r{{font:600 20px Inter,sans-serif;letter-spacing:.24em;color:#57534C}}
.foot{{position:absolute;left:64px;right:64px;bottom:44px;display:flex;justify-content:space-between;font-size:20px;color:#57534C}}
/* 2 contents */
.c2 h2{{position:absolute;left:64px;top:170px;font:400 italic 92px/1 Bod,serif}}
.c2 h2 b{{display:block;font:900 54px "Noto Sans CJK KR",sans-serif;font-style:normal;margin-top:16px;letter-spacing:-.02em}}
.c2 .grid{{position:absolute;left:64px;right:64px;top:430px;display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
.c2 .g{{position:relative;height:330px;border-radius:14px;overflow:hidden;background:#ccc center 70%/cover}}
.c2 .g span{{position:absolute;left:0;right:0;bottom:0;padding:40px 14px 12px;color:#fff;font-size:22px;font-weight:700;background:linear-gradient(to top,rgba(0,0,0,.8),transparent)}}
.c2 .g em{{position:absolute;left:12px;top:12px;font:700 22px Bod,serif;font-style:normal;color:#fff;background:#007C7C;border-radius:999px;padding:2px 12px}}
.c2 .toc{{position:absolute;left:64px;right:64px;bottom:110px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
.c2 .toc div{{border-top:2px solid #141414;padding-top:12px;font-size:24px;font-weight:800;line-height:1.35}}
.c2 .toc small{{display:block;font:700 18px Inter,sans-serif;letter-spacing:.2em;color:#00A8A8;margin-bottom:4px}}
/* 3 feature */
.c3 .hd{{left:580px;right:60px}}.c3 .hd .m{{font-size:38px;white-space:nowrap}}.c3 .hd .r{{font-size:17px}}
.c3 .ph{{position:absolute;left:0;top:0;bottom:0;width:520px;background:url({feat_img}) center 60%/cover}}
.c3 .tx{{position:absolute;left:580px;right:60px;top:190px}}
.c3 .tx .k{{font:600 20px Inter,sans-serif;letter-spacing:.24em;color:#00A8A8}}
.c3 .tx h3{{font-family:"Noto Serif CJK KR",serif;font-weight:900;font-size:58px;line-height:1.18;margin:16px 0 30px;letter-spacing:-.02em}}
.c3 .row{{border-top:2px solid #141414;padding:20px 0 22px}}
.c3 .row small{{font-size:22px;font-weight:800;color:#fff;background:#141414;border-radius:999px;padding:3px 14px}}
.c3 .row.v small{{background:#007C7C}}
.c3 .row .n{{display:block;font-size:25px;margin:12px 0 4px;color:#57534C;line-height:1.35}}
.c3 .row .p{{font:900 64px/1.05 Bod,serif}}
.c3 .row.v .p{{color:#007C7C}}
.c3 .ar{{font:400 italic 40px Bod,serif;color:#57534C;margin:2px 0}}
.c3 .ai{{position:absolute;left:20px;top:20px;font-size:18px;color:#fff;background:rgba(0,0,0,.45);padding:4px 12px;border-radius:999px}}
/* 4 deals */
.c4 h2{{position:absolute;left:64px;top:170px;font:400 italic 92px/1 Bod,serif}}
.c4 h2 b{{display:block;font:900 54px "Noto Sans CJK KR",sans-serif;font-style:normal;margin-top:16px}}
.c4 .list{{position:absolute;left:64px;right:64px;top:420px}}
.c4 .it{{display:grid;grid-template-columns:220px 1fr;align-items:center;border-top:2px solid #141414;padding:24px 0;gap:24px}}
.c4 .it .o{{font:900 108px/1 Bod,serif;color:#D2382A}}
.c4 .it .o small{{font-size:52px}}
.c4 .it .w{{font-size:21px;color:#57534C;font-weight:700}}
.c4 .it .n{{font-size:30px;font-weight:800;line-height:1.3;margin:4px 0}}
.c4 .it .pr{{font-size:28px;font-weight:900}}
/* 5 how */
.c5{{background:#007C7C;color:#fff}}
.c5 .hd{{border-color:#fff}} .c5 .hd .m em{{color:#5FE0DC}} .c5 .hd .r{{color:#CFEFEC}}
.c5 h2{{position:absolute;left:64px;top:180px;font-family:"Noto Serif CJK KR",serif;font-weight:900;font-size:86px;line-height:1.15;letter-spacing:-.02em}}
.c5 ol{{position:absolute;left:64px;right:64px;top:470px;list-style:none;counter-reset:n}}
.c5 li{{counter-increment:n;display:flex;gap:28px;align-items:center;border-top:2px solid rgba(255,255,255,.6);padding:30px 0;font-size:40px;font-weight:800}}
.c5 li::before{{content:counter(n,decimal-leading-zero);font:900 64px Bod,serif;color:#5FE0DC;width:110px}}
.c5 .per{{position:absolute;left:64px;right:64px;bottom:130px;font-size:30px;line-height:1.5}}
.c5 .per b{{display:block;font:700 22px Inter,sans-serif;letter-spacing:.24em;color:#CFEFEC}}
.c5 .foot{{color:#CFEFEC}}
'''
    vol = f'VOL. {a.vol:02d}'
    hd = lambda r: f'<div class="hd"><span class="m">zzebi<em>.st</em> weekly</span><span class="r">{esc(r)}</span></div>'
    foot = lambda n: f'<div class="foot"><span>@zzebi.st · {esc(per_en)}</span><span>{n} / 5</span></div>'
    bars = ''.join(f'<i style="width:{w}px;height:{h}%"></i>' for w, h in [(4,100),(2,100),(6,100),(2,80),(3,100),(5,100),(2,100),(4,90),(2,100),(6,100),(3,100),(2,85),(5,100),(2,100),(4,100)])
    s1 = f'''<section class="s c1"><div class="ph"></div><div class="sh"></div>
<div class="top"><span>WEEKLY STYLE &amp; SHOPPING</span><span>{vol}</span></div>
<div class="mast">ZZEBI<em>.</em>ST</div>
<div class="per"><b>WEEKLY</b>{esc(per_en)}</div>
<div class="ai">AI 재현 이미지</div>
<div class="lines"><div class="kick">The Celeb Edit</div><div class="hl">셀럽 {n_look}룩,<br>명품부터<br>가성비까지</div></div>
<div class="cl"><small>INSIDE</small><span>명품→가성비 3단 가격</span><span>무신사·29CM·지그재그 랭킹</span><span>핫딜 TOP 10 · 크림 신발</span></div>
<div class="bot"><span class="pill">댓글 ‘리포트’ → DM으로 받기</span><span class="bar">{bars}</span></div></section>'''
    g = ''.join(f'<div class="g" style="background-image:url({imgs[i]})"><em>{esc(looks[i]["ep"])}</em><span>{esc(looks[i]["who"].replace(" 무드 재현",""))}</span></div>' for i in order[:6])
    s2 = f'''<section class="s c2">{hd(vol + " · CONTENTS")}<h2>This Week<b>{esc(per_ko)}</b></h2>
<div class="grid">{g}</div>
<div class="toc"><div><small>01 · LOOKS</small>여성·남성 셀럽 {n_look}룩 따라 사기</div><div><small>02 · RANKING</small>무신사·29CM·지그재그 이번 주 랭킹</div><div><small>03 · DEALS</small>핫딜 TOP 10 · 크림 인기 신발</div></div>
{foot(2)}</section>'''
    s3 = f'''<section class="s c3"><div class="ph"></div><span class="ai">AI 재현 이미지</span>{hd("FEATURE")}
<div class="tx"><div class="k">LOOK #{esc(F["ep"])} · {esc(F["who"].replace(" 무드 재현",""))}</div><h3>{esc(core["h"])},<br>얼마면 될까?</h3>
<div class="row"><small>명품</small><span class="n">{esc(lux.get("brand"))} {esc(lux.get("name"))}</span><span class="p">{esc(won(lux["won"], lux.get("approx")))}</span></div>
<div class="ar">↓</div>
<div class="row v"><small>가성비</small><span class="n">{esc(val.get("brand"))} {esc(val.get("name"))}</span><span class="p">{esc(won(val["won"]))}</span></div>
<p style="font-size:24px;color:#57534C;margin-top:18px">중가 선택지와 나머지 아이템은 리포트에서</p></div>
<div class="foot" style="left:580px"><span>@zzebi.st · {esc(per_en)}</span><span>3 / 5</span></div></section>'''
    its = ''.join(f'<div class="it"><span class="o">{int(p.get("off") or 0)}<small>%</small></span><div><div class="w">{esc((p.get("where") or "").split("·")[0].strip())}</div><div class="n">{esc(p.get("brand"))} {esc(p.get("name"))}</div><div class="pr">{esc(won(p["won"]))}</div></div></div>' for p in deals)
    s4 = f'''<section class="s c4">{hd("HOT DEALS")}<h2>Hot Deals<b>이번 주 할인 TOP 4</b></h2><div class="list">{its}</div>{foot(4)}</section>'''
    s5 = f'''<section class="s c5">{hd("HOW TO GET")}<h2>이번 주 리포트,<br>DM으로 받아 보세요</h2>
<ol><li>@zzebi.st 팔로우</li><li>이 게시물에 ‘리포트’ 댓글</li><li>DM으로 이번 주 링크 도착</li></ol>
<div class="per"><b>THIS WEEK</b>{esc(per_ko)} · 한국어 · EN · 中文<br>매주 월요일 새 리포트 · 수·금 가격 점검</div>{foot(5)}</section>'''
    os.makedirs(a.out, exist_ok=True)
    page = f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{s1}{s2}{s3}{s4}{s5}</body></html>'
    hp = os.path.join(a.out, 'slides.html'); open(hp, 'w').write(page)
    js = f'''const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1080,height:1350}}}});
await p.goto('file://{hp}');await p.waitForTimeout(800);const els=await p.$$('section.s');
for(let i=0;i<els.length;i++){{await els[i].screenshot({{path:'{a.out}/slide'+(i+1)+'.png'}});}}await b.close();}})();'''
    jp = os.path.join(a.out, '_shot.js'); open(jp, 'w').write(js)
    subprocess.run(['node', jp], check=True, cwd=ROOT)
    from PIL import Image
    for i in range(1, 6):
        Image.open(f'{a.out}/slide{i}.png').convert('RGB').save(f'{a.out}/slide{i}.jpg', quality=92)
        os.remove(f'{a.out}/slide{i}.png')
    os.remove(jp)
    print('\n'.join(f'{a.out}/slide{i}.jpg' for i in range(1, 6)))

if __name__ == '__main__':
    main()
