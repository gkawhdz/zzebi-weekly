#!/usr/bin/env python3
"""상품 매칭 검증 시트 — 룩 사진의 아이템 확대 컷 옆에 후보 상품 사진을 나란히 붙여 눈으로 비교.

사용:
  python3 tools/match_sheet.py DATA_DIR LOOK_ID OUT_DIR [--spec studio/celeb/specs/lookNN.json]
    → OUT_DIR/<LOOK_ID>_sheet.jpg (아이템별 1줄: [룩 확대 컷 | 명품 | 중가 | 가성비] 또는 [룩 확대 컷 | 함께 입을 상품])
    → OUT_DIR/<LOOK_ID>_fetch.json (상품별 사진 수집 결과·품절 표시)
  python3 tools/match_sheet.py --candidates CROP.jpg OUT.jpg URL1 URL2 ...   # 후보 여러 개를 한 번에 비교(고르기 전)

규칙(SCHEMA.md 의 match 점수): 시트를 Read 로 직접 보고 상품마다 match 1~5 를 매김.
  5 = 같은 제품 또는 거의 똑같음 / 4 = 색·소재·실루엣·핵심 디테일이 모두 같음(작은 차이만) /
  3 이하 = 색이 다르거나(블랙↔네이비, 크림↔화이트, 코발트↔네이비 등), 기장·핏·종류가 다름 → 사용 금지.
  사진을 못 가져온 상품(해외몰 차단 등)은 검증 불가 → 사용 금지(국내 판매처의 같은 상품으로 바꾸기).
"""
import sys, os, json, subprocess, glob, difflib, textwrap
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = subprocess.check_output(['fc-match', '-f', '%{file}', 'Noto Sans CJK KR:weight=700']).decode()
F = lambda n: ImageFont.truetype(FONT, n)
CELL = 300

def fetch(url, out):
    try:
        r = subprocess.run(['node', os.path.join(ROOT, 'tools', 'shop_img.js'), url, out], capture_output=True, text=True, timeout=90)
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception as e:
        return {'ok': False, 'url': url, 'error': str(e)[:100]}

def tile(img, label, sub='', warn=False):
    t = Image.new('RGB', (CELL, CELL + 70), 'white')
    if img is not None:
        im = img.copy(); im.thumbnail((CELL, CELL)); t.paste(im, ((CELL - im.width) // 2, (CELL - im.height) // 2))
    else:
        d0 = ImageDraw.Draw(t); d0.rectangle([0, 0, CELL, CELL], fill='#ddd'); d0.text((20, CELL // 2 - 20), '사진 없음\n(검증 불가)', font=F(24), fill='#a00')
    d = ImageDraw.Draw(t)
    d.text((6, CELL + 4), label[:22], font=F(19), fill='#a00' if warn else '#111')
    d.text((6, CELL + 32), textwrap.shorten(sub, 30, placeholder='…'), font=F(15), fill='#555')
    return t

def crop_from_spec(look_img, spec_items, name):
    if not spec_items: return look_img
    names = [it['name'] for it in spec_items]
    m = difflib.get_close_matches(name, names, n=1, cutoff=0.2)
    it = spec_items[names.index(m[0])] if m else None
    if not it or 'crop' not in it: return look_img
    cx, cy, s = it['crop']; h = s // 2
    return look_img.crop((max(0, cx - h), max(0, cy - h), min(look_img.width, cx + h), min(look_img.height, cy + h)))

def main_look(data, lid, out, spec):
    L = json.load(open(os.path.join(data, f'look_{lid}.json')))
    look = Image.open(os.path.join(data, 'img', L['img'])).convert('RGB')
    if not spec:
        cand = glob.glob(os.path.join(ROOT, 'studio', 'celeb', 'specs', f'look{L["ep"]}.json'))
        spec = cand[0] if cand else None
    items = json.load(open(spec))['items'] if spec else []
    os.makedirs(out, exist_ok=True)
    rows, log = [], []
    def get(p, tag):
        fn = os.path.join(out, f'{lid}_{len(log)}.jpg'); r = fetch(p['url'], fn); r['tag'] = tag; r['name'] = p.get('name'); log.append(r)
        im = Image.open(fn).convert('RGB') if r.get('ok') and os.path.exists(fn) else None
        return tile(im, f'{tag} · {p.get("brand","")}', f'{p.get("name","")} · {p.get("won",0):,}원' + (' · 품절?' if r.get('soldout') else ''), warn=(im is None or r.get('soldout')))
    for c in L.get('cores', []):
        row = [tile(crop_from_spec(look, items, c['h']), '룩: ' + c['h'], '← 이것과 비교')]
        for k, lab in (('lux', '명품'), ('mid', '중가'), ('value', '가성비')):
            if c['tiers'].get(k): row.append(get(c['tiers'][k], lab))
        rows.append(row)
    for w in L.get('with', []):
        rows.append([tile(crop_from_spec(look, items, w['p'].get('name', '')), '룩: ' + w.get('role', '')[:14], '← 이것과 비교'), get(w['p'], '함께')])
    W = max(len(r) for r in rows) * (CELL + 10) + 10
    H = len(rows) * (CELL + 80) + 10
    sheet = Image.new('RGB', (W, H), '#f2f2f2')
    for y, r in enumerate(rows):
        for x, t in enumerate(r):
            sheet.paste(t, (10 + x * (CELL + 10), 10 + y * (CELL + 80)))
    sp = os.path.join(out, f'{lid}_sheet.jpg'); sheet.save(sp, quality=85)
    json.dump(log, open(os.path.join(out, f'{lid}_fetch.json'), 'w'), ensure_ascii=False, indent=1)
    print(sp)

def main_cand(crop, out, urls):
    tiles = [tile(Image.open(crop).convert('RGB'), '룩 아이템', '← 이것과 비교')]
    tmp = os.path.splitext(out)[0]
    for i, u in enumerate(urls, 1):
        fn = f'{tmp}_c{i}.jpg'; r = fetch(u, fn)
        im = Image.open(fn).convert('RGB') if r.get('ok') and os.path.exists(fn) else None
        tiles.append(tile(im, f'후보 {i}', (r.get('title') or u)[:40], warn=im is None))
    cols = 4; rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (CELL + 10) + 10, rows * (CELL + 80) + 10), '#f2f2f2')
    for i, t in enumerate(tiles):
        sheet.paste(t, (10 + (i % cols) * (CELL + 10), 10 + (i // cols) * (CELL + 80)))
    sheet.save(out, quality=85); print(out)

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(1)
    if a[0] == '--candidates':
        main_cand(a[1], a[2], a[3:])
    else:
        spec = a[a.index('--spec') + 1] if '--spec' in a else None
        main_look(a[0], a[1], a[2], spec)
