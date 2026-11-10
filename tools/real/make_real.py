#!/usr/bin/env python3
"""Trend Daily 실사풍 샘플 (make_webtoon.py v6.4 에서 복사·수정, 2026-11-10 샘플 — 게시용 아님)
- 그림: 얼굴 없는 실사 스트리트 사진(gpt-image-1.5, 1024x1536)을 화면 꽉 채움(1.25배, 가운데 1080).
- 글자: 사진 위 어두운 그라데이션 + 흰 글씨, 좌상단 'TREND DAILY' 틸 라벨(높이 90).
scene type
  rcompare : {left, right, title, title_size, body, left_stamp, right_stamp, stamp_y}
  rboard   : {img, head:{num,total,kicker,title,body}, chip, items:[{xy(원본px), name, sub, swatch, zoom}], t_board, t_item}
  rformula : {bg, title, rows:[{img, box:[x0,y0,x1,y1], text}]}
  text     : make_short 문구 장면(CTA)
원본 좌표 → 화면(줌 1.0): x*1.25-100, y*1.25
"""
import json, sys, os, subprocess, tempfile, math
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_short as MS
import make_lookbook as LB

W, H, FPS = 1080, 1920, 30
K, OX = 1.25, 100
HS = 2
PX, PY = 360, 760
WHITE = (255, 255, 255)
ease = MS.ease
_C = {}

def canvas(P, key):
    """사진을 1.25배(1280x1920)로 + 가장자리 바깥은 흐리게 늘린 같은 사진(확대 시 빈칸 방지), HS배 고해상도"""
    if key not in _C:
        src = P[key]
        cw, ch = (1280 + 2 * PX) * HS, (1920 + 2 * PY) * HS
        bg = src.resize((cw, ch), Image.BILINEAR).filter(ImageFilter.GaussianBlur(40 * HS))
        bg = Image.blend(bg, Image.new("RGB", bg.size, (20, 20, 22)), 0.35)
        bg.paste(src.resize((1280 * HS, 1920 * HS), Image.LANCZOS), (PX * HS, PY * HS))
        _C[key] = bg
    return _C[key]

def view(cv, z, fx, fy, sx=540, sy=960):
    """원본 좌표 (fx,fy)가 화면 (sx,sy)에 오도록 z배"""
    bx = (fx * K + PX) * HS; by = (fy * K + PY) * HS
    cw, ch = W * HS / z, H * HS / z
    x0 = bx - sx * HS / z; y0 = by - sy * HS / z
    return cv.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS).convert("RGBA")

HOME = (1.0, (540 + OX) / K, 960 / K)  # z, 원본 x, 원본 y (화면 가운데)

def grad(img, h, a0, y0=0, up=True):
    g = np.linspace(1, 0, h) ** 1.25 * a0 if up else np.linspace(0, 1, h) ** 1.5 * a0
    lay = Image.new("RGBA", (W, h), (10, 10, 12, 0)); lay.putalpha(Image.fromarray(np.repeat(g[:, None], W, 1).astype(np.uint8)))
    img.alpha_composite(lay, (0, y0))

def badge(img, prog=None):
    d = ImageDraw.Draw(img); f = LB.F(True, 46); s = "TREND DAILY"; tw = d.textlength(s, font=f)
    d.rounded_rectangle([60, 92, 60 + tw + 56, 182], radius=16, fill=LB.BRAND + (255,))
    d.text((88, 137), s, font=f, fill=WHITE, anchor="lm")
    if prog is not None:
        d.rectangle([60, 60, W - 60, 66], fill=(255, 255, 255, 70))
        d.rectangle([60, 60, 60 + int((W - 120) * prog), 66], fill=LB.BRAND + (255,))

def shadow_text(d, xy, s, f, fill, k=3):
    for ox, oy in ((k, k), (0, k), (k, 0)):
        d.text((xy[0] + ox, xy[1] + oy), s, font=f, fill=(0, 0, 0, 150))
    d.text(xy, s, font=f, fill=fill)

def head(img, hd, a=1.0):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    al = int(255 * a); y = 214
    fnum = LB.F(True, 96); d.text((60, y - 14), hd["num"], font=fnum, fill=(127, 227, 227, al))
    x = 60 + d.textlength(hd["num"], font=fnum) + 18
    ft = LB.F(True, 34); d.text((x, y + 44), f"/ {hd['total']}", font=ft, fill=(230, 230, 230, al)); x += d.textlength(f"/ {hd['total']}", font=ft) + 28
    fk = LB.F(True, 40)
    d.rounded_rectangle([x, y + 22, x + d.textlength(hd["kicker"], font=fk) + 44, y + 92], radius=35, fill=LB.BRAND + (al,))
    d.text((x + 22, y + 30), hd["kicker"], font=fk, fill=(255, 255, 255, al))
    y += 124; ftt = LB.F(True, hd.get("title_size", 92))
    for ln in hd["title"].split("\n"):
        shadow_text(d, (60, y), ln, ftt, (255, 255, 255, al)); y += int(ftt.size * 1.14)
    if hd.get("body"):
        shadow_text(d, (62, y + 8), hd["body"], LB.F(True, 44), (127, 227, 227, al), 2)
    img.alpha_composite(lay)

def chip(img, text):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f = LB.F(True, 50); tw = d.textlength(text, font=f)
    d.rounded_rectangle([60, 214, 60 + tw + 56, 296], radius=41, fill=(14, 14, 16, 215))
    d.text((88, 255), text, font=f, fill=WHITE, anchor="lm")
    img.alpha_composite(lay)

def r_compare(sc, T, P, prog):
    img = Image.new("RGBA", (W, H), (16, 16, 18, 255))
    top = sc.get("top", 670); ph = H - top; s = ph / 1536 * 1.0
    for key, x0, fx in ((sc["left"], 0, sc.get("left_cx", 512)), (sc["right"], 540, sc.get("right_cx", 512))):
        src = P[key]; st = sc.get("src_top", 0)  # 11/10 전신 샘플: 위 빈 배경 잘라 인물 크게
        if st: src = src.crop((0, st, 1024, 1536)); s = ph / (1536 - st)
        pw = int(1024 * s)
        pan = src.resize((pw, ph), Image.LANCZOS)
        cx = int(fx * s); cx = min(max(270, cx), pw - 270)
        img.paste(pan.crop((cx - 270, 0, cx + 270, ph)), (x0, top))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, top], fill=LB.rgb(sc.get("band", "#16222b")) + (255,))
    grad(img, 160, 200, top, up=True)
    d.rectangle([536, top, 544, H], fill=LB.BRAND + (255,))
    badge(img, prog)
    ft = LB.F(True, sc.get("title_size", 124)); y = 222
    for ln in sc["title"].split("\n"):
        d.text((56, y), ln, font=ft, fill=WHITE); y += int(ft.size * 1.13)
    if sc.get("body"):
        d.text((60, y + 22), sc["body"], font=LB.F(True, 48), fill=(127, 227, 227))
    for (kind, lab), cx in ((sc["left_stamp"], 270), (sc["right_stamp"], 810)):
        LB.stamp(img, cx, sc.get("stamp_y", 1150), kind, lab, 1.0, scale=1.0 + 0.04 * math.sin(T * 2 * math.pi * 1.2))  # 0초부터 완성 + 살짝 맥박
    return img

def r_board(sc, T, P, prog):
    cv = canvas(P, sc["img"]); items = sc.get("items", [])
    tb, ti = sc.get("t_board", 3.0), sc.get("t_item", 2.3)
    hm = tuple(sc.get("home", HOME))  # 11/10 전신 샘플: 첫 화면을 살짝 축소해 머리가 글자 판 아래로
    def cam(i):
        if i < 0 or i >= len(items): return hm + (960,)
        it = items[i]; return (it.get("zoom", 2.0), it["xy"][0], it["xy"][1], it.get("sy", 760))  # 11/10: 발밑 아이템은 sy 크게(화면 아래쪽)
    if T < tb:
        z = hm[0] * (1.0 + 0.03 * T / tb)
        img = view(cv, z, hm[1], hm[2])
        grad(img, 1000, 250)
        badge(img, prog); head(img, sc["head"])
        return img
    k = int((T - tb) // ti); tl = T - tb - k * ti
    k = min(k, len(items) - 1) if items else 0
    a, b = cam(k - 1), cam(k)
    p = ease(tl / 0.5)
    z, fx, fy, sy = [a[j] + (b[j] - a[j]) * p for j in range(4)]
    img = view(cv, z * (1 + 0.02 * tl / ti), fx, fy, 540, sy)
    grad(img, 420, 190)
    grad(img, 700, 150, H - 700, up=False)
    badge(img, prog)
    it = items[k]
    if sc.get("chip"): chip(img, sc["chip"])
    LB.ring(img, 540, it.get("sy", 760), ease((tl - 0.4) / 0.2), r=it.get("ring", 100))
    LB.big_card(img, it["name"], it.get("sub", ""), it.get("swatch", "#888888"), ease((tl - 0.35) / 0.25), num=k + 1, total=len(items))
    return img

def r_formula(sc, T, P, prog):
    img = P[sc["bg"]].resize((1280, 1920), Image.LANCZOS).crop((OX, 0, OX + W, H)).filter(ImageFilter.GaussianBlur(18)).convert("RGBA")
    img.alpha_composite(Image.new("RGBA", (W, H), (12, 12, 14, 175)))
    badge(img, prog)
    d = ImageDraw.Draw(img)
    fk = LB.F(True, 42); d.text((60, 236), sc.get("kicker", ""), font=fk, fill=(127, 227, 227))
    ft = LB.F(True, 92); y = 300
    for ln in sc["title"].split("\n"):
        d.text((60, y), ln, font=ft, fill=WHITE); y += 106
    y += 30; rh = 250
    for i, r in enumerate(sc["rows"]):
        p = ease((T - 0.3 - i * 0.35) / 0.35)
        if p <= 0: continue
        lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        yy = y + i * (rh + 22) + int(30 * (1 - p)); al = int(255 * p)
        dl.rounded_rectangle([60, yy, 940, yy + rh], radius=28, fill=(255, 253, 249, int(240 * p)))
        dl.rectangle([60, yy + 30, 70, yy + rh - 30], fill=LB.BRAND + (al,))
        img.alpha_composite(lay)
        src = P[r["img"]].crop(tuple(r["box"])); s = 210
        rr = max(s / src.width, s / src.height); src = src.resize((int(src.width * rr) + 1, int(src.height * rr) + 1), Image.LANCZOS)
        src = src.crop(((src.width - s) // 2, (src.height - s) // 2, (src.width - s) // 2 + s, (src.height - s) // 2 + s))
        m = Image.new("L", (s, s), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, s - 1, s - 1], radius=20, fill=al)
        img.paste(src, (90, yy + 20), m)
        d = ImageDraw.Draw(img)
        d.text((330, yy + 34), f"0{i + 1}", font=LB.F(True, 40), fill=LB.BRAND_DK + (al,))
        fn = LB.F(True, 50)
        d.text((330, yy + 86), r["text"], font=fn, fill=(34, 30, 30, al))
        if r.get("sub"): d.text((332, yy + 156), r["sub"], font=LB.F(False, 36), fill=(80, 72, 68, al))
    return img

def render(sc, t, P, brand, idx, total):
    typ = sc.get("type", "text"); dur = sc.get("dur", 3); T = t * dur
    prog = (idx + t) / total
    if typ == "text":
        return MS.render_frame(sc, t, brand, idx, total)
    img = {"rcompare": r_compare, "rboard": r_board, "rformula": r_formula}[typ](sc, T, P, prog)
    return img.convert("RGB")

def load(spec_path):
    spec = json.load(open(spec_path, encoding="utf-8")); base = os.path.dirname(os.path.abspath(spec_path))
    P = {k: Image.open(os.path.join(base, v)).convert("RGB") for k, v in spec["paintings"].items()}
    return spec, P

def main(spec_path, out):
    spec, P = load(spec_path); brand = spec.get("brand", ""); scenes = spec["scenes"]
    tmp = tempfile.mkdtemp(); n = 0
    for i, sc in enumerate(scenes):
        nf = int(round(sc.get("dur", 3) * FPS))
        for f in range(nf):
            render(sc, f / nf, P, brand, i, len(scenes)).save(f"{tmp}/{n:05d}.jpg", quality=93); n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/%05d.jpg",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "20", "-movflags", "+faststart", out], check=True)
    render(scenes[0], 0.0, P, brand, 0, len(scenes)).save(os.path.splitext(out)[0] + "_cover.jpg", quality=92)
    print("done", out, n, "frames", n / FPS, "s")

def preview(spec_path, out_jpg, times):
    spec, P = load(spec_path); frames = []
    for i, sc in enumerate(spec["scenes"]):
        for tt in times.get(str(i), [0.0]):
            frames.append(render(sc, tt / sc.get("dur", 3), P, spec.get("brand", ""), i, len(spec["scenes"])).resize((360, 640)))
    cols = min(6, len(frames)); rows = math.ceil(len(frames) / cols)
    sheet = Image.new("RGB", (360 * cols, 640 * rows), "black")
    for j, f in enumerate(frames): sheet.paste(f, ((j % cols) * 360, (j // cols) * 640))
    sheet.save(out_jpg, quality=88)

if __name__ == "__main__":
    if sys.argv[1] == "preview": preview(sys.argv[2], sys.argv[3], json.loads(sys.argv[4]))
    else: main(sys.argv[1], sys.argv[2])
