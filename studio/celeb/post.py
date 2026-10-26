"""셀럽 스냅 해부 피드 이미지 생성기 (v3: 에디토리얼 화이트 카드 + 세리프 이탤릭 번호 / v2: accent 포인트컬러, source 출처 표기)
사용: python3 post.py look.json out.jpg
look.json: {episode, celeb, city, date, title, image, offset_x, items:[{cat,brand,name,pt,find,pt_xy:[x,y],crop:[cx,cy,size]}]}
"""
import json, sys, os, html
from PIL import Image
from playwright.sync_api import sync_playwright

cfg = json.load(open(sys.argv[1])); out = sys.argv[2]
ACC = cfg.get("accent", "#D4FF3A")  # v2: 룩의 주요 색에서 뽑은 포인트 컬러
SRC = cfg.get("source", "Coveteur")
HERE = os.path.dirname(os.path.abspath(__file__))
tag = os.path.splitext(os.path.basename(sys.argv[1]))[0]
src = Image.open(cfg["image"]).convert("RGB"); IW, IH = src.size
PANEL_W, PANEL_H = 492, 1063
S = PANEL_H / IH
disp_w = IW * S
ox = cfg.get("offset_x", -(disp_w - PANEL_W) / 2)  # 기본: 가운데 맞춤

for i, it in enumerate(cfg["items"]):
    cx, cy, sz = it["crop"]
    box = (max(0, cx - sz // 2), max(0, cy - sz // 2), min(IW, cx + sz // 2), min(IH, cy + sz // 2))
    src.crop(box).resize((240, 240), Image.LANCZOS).save(os.path.join(HERE, f"{tag}_c{i}.jpg"), quality=92)

e = html.escape
cards = ""
for i, it in enumerate(cfg["items"]):
    cards += f'''<div class="card"><div class="ico"><img src="{tag}_c{i}.jpg"></div>
    <div class="num">0{i+1}</div><div class="cat">{e(it["cat"])}</div><div class="brand">{e(it["brand"])}</div>
    <div class="name">{e(it["name"])}</div><div class="pt">{e(it["pt"])}</div><div class="find">검색어: {e(it["find"])}</div></div>'''
pts = json.dumps([it["pt_xy"] for it in cfg["items"]])

page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;background:#F3EEE6;font-family:'Noto Sans CJK KR',sans-serif;color:#121214;position:relative;overflow:hidden}}
h1{{position:absolute;left:40px;top:34px;font-size:56px;font-weight:900;letter-spacing:-1px}}
.meta{{position:absolute;left:40px;top:132px;display:flex;gap:14px;align-items:center}}
.pill{{background:#D4FF3A;border-radius:99px;padding:5px 18px;font-weight:700;font-size:25px}}
.sub{{font-size:27px;font-weight:700;color:#78746E}}
.handle{{position:absolute;right:40px;top:50px;background:#121214;color:#D4FF3A;border-radius:99px;padding:8px 22px;font-size:28px;font-weight:900}}
.panel{{position:absolute;left:40px;top:210px;width:500px;height:1071px;border-radius:30px;overflow:hidden;border:4px solid #121214}}
.panel img{{position:absolute;top:0;left:{ox}px;height:{PANEL_H}px}}
.credit{{position:absolute;right:12px;top:10px;font-size:19px;color:#fff;font-weight:500;background:rgba(10,10,12,.55);border-radius:99px;padding:3px 12px}}
.cards{{position:absolute;left:562px;top:210px;width:478px}}
.card{{height:255px;margin-bottom:17px;background:#FFFDF9;border:2px solid #121214;border-radius:24px;color:#121214;position:relative;overflow:hidden}}
.card:before{{content:"";position:absolute;right:0;top:0;width:14px;height:100%;background:#D4FF3A;border-left:2px solid #121214}}
.ico{{width:118px;height:118px;background:#fff;border-radius:16px;position:absolute;left:14px;top:14px;overflow:hidden;border:2px solid #121214}}
.ico img{{width:114px;height:114px;object-fit:cover;display:block}}
.num{{position:absolute;left:148px;top:-2px;font-family:'Liberation Serif',serif;font-style:italic;font-weight:700;font-size:62px;color:#121214;letter-spacing:-2px}}
.cat{{position:absolute;left:226px;top:22px;font-size:21px;font-weight:700;color:#121214;white-space:nowrap;border-bottom:3px solid #D4FF3A;line-height:1.25}}
.brand{{position:absolute;left:150px;top:78px;font-size:20px;font-weight:500;color:#6E6A64;white-space:nowrap}}
.name{{position:absolute;left:18px;top:128px;font-size:31px;font-weight:900;letter-spacing:-.5px;white-space:nowrap}}
.pt{{position:absolute;left:18px;top:172px;font-size:22px;font-weight:500;color:#4A4743;white-space:nowrap}}
.find{{position:absolute;left:16px;bottom:10px;background:#D4FF3A;color:#121214;font-size:19px;font-weight:700;border-radius:99px;padding:1px 13px;white-space:nowrap;border:1.5px solid #121214}}
.foot{{position:absolute;left:40px;right:40px;bottom:22px;display:flex;justify-content:space-between;font-size:20px;color:#78746E;font-weight:500}}
.foot b{{color:#121214;font-size:27px;font-weight:700}}
.over{{position:absolute;inset:0;pointer-events:none}}
</style></head><body>
<h1>셀럽 스냅 해부 #{e(cfg["episode"])}</h1>
<div class="meta"><span class="pill">{e(cfg["celeb"])} · {e(cfg["city"])} · {e(cfg["date"])}</span><span class="sub">룩 재현 · {e(cfg["title"])}</span></div>
<div class="handle">@zzebi.st</div>
<div class="panel"><img src="{os.path.abspath(cfg["image"])}"><div class="credit">이미지: AI 생성 · 룩 참고: {e(SRC)}</div></div>
<div class="cards">{cards}</div>
<svg class="over" width="1080" height="1350"><g id="lines"></g></svg>
<div class="foot"><span>※ 같은 제품이 아니어도 비슷한 무드로 찾을 수 있는 검색어</span><b>저장하고 따라 입기 ↓</b></div>
<script>
const PX={44+ox},PY=214,S={S};const pts={pts};let h='';
pts.forEach(([x,y],i)=>{{const sx=PX+x*S,sy=PY+y*S,ex=558,ey=210+i*272+127;
h+=`<line x1="${{sx}}" y1="${{sy}}" x2="${{ex}}" y2="${{ey}}" stroke="#121214" stroke-opacity=".55" stroke-width="3" stroke-linecap="round"/>
<line x1="${{sx}}" y1="${{sy}}" x2="${{ex}}" y2="${{ey}}" stroke="#D4FF3A" stroke-width="1.6" stroke-linecap="round"/>
<circle cx="${{sx}}" cy="${{sy}}" r="9" fill="#D4FF3A" stroke="#121214" stroke-width="2"/>
<text x="${{sx}}" y="${{sy+4.5}}" text-anchor="middle" font-size="12" font-weight="900" fill="#121214" font-family="Noto Sans CJK KR">${{i+1}}</text>
<circle cx="${{ex}}" cy="${{ey}}" r="4" fill="#121214"/>`;}});
document.getElementById('lines').innerHTML=h;
</script></body></html>'''
page = page.replace('#D4FF3A', ACC)
hp = os.path.join(HERE, f"{tag}.html"); open(hp, "w").write(page)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
    pg.goto("file://" + hp); pg.wait_for_timeout(400)
    over = pg.evaluate("[...document.querySelectorAll('.name,.pt,.find,.brand')].filter(el=>el.getBoundingClientRect().right>1020).map(el=>el.textContent)")
    if over: print("WARN overflow:", over)
    pg.screenshot(path=os.path.join(HERE, f"{tag}.png")); b.close()
Image.open(os.path.join(HERE, f"{tag}.png")).convert("RGB").save(out, quality=88)
print("done", out)
