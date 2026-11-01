"""셀럽 스냅 해부 릴스 (v4.4 — 첫 화면 ON/OFF 분할 슬라이더(split) + 커버에서 셀럽 이름 제거(훅 규칙 10/30), v4.3 — 첫 화면 후킹 문구(hook·hook_cta) + 0초부터 글자 표시, v4.2 — 큰 글씨 요약 리스트 + 카드 보조글씨 30px, 브랜드 틸 #00A8A8) — 9:16 화면을 꽉 채우는 네이티브 레이아웃
사용: python3 make_reel.py look.json out_silent.mp4 [cover_out.jpg]
look.json: episode, celeb, city, date, title, image, accent(옵션 HEX), source(옵션),
           items[4]: cat, brand, name, pt, find, pt_xy[x,y](원본 픽셀), crop[cx,cy,size]
v4 변경: 4:5 이미지를 줄여 넣던 방식 폐기. 사진을 풀스크린으로 깔고 카메라가 아이템으로 이동,
        큰 정보 카드(확대 컷 + 큰 글씨)가 화면 아래쪽 안전영역 위에 뜸. 끝에 4개 요약 그리드.
안전영역: 하단 25%(y>1440)·오른쪽 140px(x>940)에는 글자를 두지 않음.
"""
import sys, os, json, subprocess, shutil, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

L = json.load(open(sys.argv[1])); OUT = sys.argv[2]
COVER_OUT = sys.argv[3] if len(sys.argv) > 3 else None
W, H, FPS = 1080, 1920, 30
FD = "/usr/share/fonts/opentype/noto/"
def F(s, w="Black"): return ImageFont.truetype(FD + f"NotoSansCJK-{w}.ttc", s, index=1)
def SF(s): return ImageFont.truetype(FD + "NotoSerifCJK-Black.ttc", s, index=1)
def hx(c): c = c.lstrip("#"); return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
INK, PAPER, WHITE = (17, 17, 19), (247, 244, 238), (255, 255, 255)
ACC = hx(L.get("accent", "#C8A27A"))
ACC_D = tuple(int(v * 0.55) for v in ACC)
BRAND = (0, 168, 168)  # zzebi 브랜드 틸 #00A8A8 (프로필 로고와 통일)  # 종이 위 글자용 진한 포인트색

src = Image.open(L["image"]).convert("RGB")
IW, IH = src.size
# 원본을 화면 높이에 맞춰 키운 '무대' (줌 여유 포함)
BASE = H / IH * 1.0
stage = src.resize((int(IW * BASE * 1.35), int(IH * BASE * 1.35)), Image.LANCZOS)
SS = BASE * 1.35  # 원본 → stage 배율
SPLIT = L.get("split")  # v4.4: {"image_off": 비교용(문제) 이미지, "off_label": "무지 코트", "on_label": "체크 코트"}
if SPLIT:
    src_off = Image.open(SPLIT["image_off"]).convert("RGB").resize((IW, IH), Image.LANCZOS)
    stage_off = src_off.resize(stage.size, Image.LANCZOS)

def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def eio(t): t = max(0, min(1, t)); return 4 * t ** 3 if t < .5 else 1 - (-2 * t + 2) ** 3 / 2
def lerp(a, b, t): return a + (b - a) * t

def view(cx, cy, z, stg=None):
    """원본 좌표 (cx,cy)를 화면 (540, 760)에 두고 배율 z(1=화면높이 맞춤)로 보여줌"""
    stg = stg or stage
    s = BASE * z
    vw, vh = W / s, H / s
    x0 = cx - 540 / s; y0 = cy - 760 / s
    x0 = max(0, min(IW - vw, x0)) if vw < IW else (IW - vw) / 2
    y0 = max(0, min(IH - vh, y0)) if vh < IH else (IH - vh) / 2
    box = tuple(int(v * SS) for v in (x0, y0, x0 + vw, y0 + vh))
    return stg.crop(box).resize((W, H), Image.BILINEAR), (x0, y0, s)

def grad(h, top=True, a0=170):
    g = Image.new("L", (1, h))
    for y in range(h):
        t = y / (h - 1); g.putpixel((0, y), int(a0 * ((1 - t) if top else t) ** 1.6))
    return g.resize((W, h))

def shade(img, a_top=150, a_bot=0, h_top=520, h_bot=0):
    img = img.convert("RGBA")
    if h_top: img.alpha_composite(Image.merge("RGBA", (*Image.new("RGB", (W, h_top), (0, 0, 0)).split(), grad(h_top, True, a_top))), (0, 0))
    if h_bot: img.alpha_composite(Image.merge("RGBA", (*Image.new("RGB", (W, h_bot), (0, 0, 0)).split(), grad(h_bot, False, a_bot))), (0, H - h_bot))
    return img

def txt(d, xy, s, f, fill, anchor="la"): d.text(xy, s, font=f, fill=fill, anchor=anchor)

def header(img, a=1.0):
    d = ImageDraw.Draw(img)
    c = lambda col: col + (int(255 * a),)
    txt(d, (60, 118), f"셀럽 스냅 해부  #{L['episode']}", F(34, "Bold"), c(WHITE))
    d.line([(60, 168), (140, 168)], fill=c(BRAND), width=5)
    txt(d, (60, 190), L["celeb"], F(58), c(WHITE))
    sub = f"{L['city']} · {L['date']}  |  {L['title']}"; fs_ = F(30, "Bold")
    for ox, oy in ((2, 2), (-1, 1), (1, -1), (2, 0)): txt(d, (60 + ox, 268 + oy), sub, fs_, (0, 0, 0, int(200 * a)))  # v4.4: 무늬 위에서도 읽히게 그림자
    txt(d, (60, 268), sub, fs_, c(WHITE))

crops = []
for it in L["items"]:
    cx, cy, sz = it["crop"]
    b = (max(0, cx - sz // 2), max(0, cy - sz // 2), min(IW, cx + sz // 2), min(IH, cy + sz // 2))
    crops.append(src.crop(b).resize((300, 300), Image.LANCZOS))

def rr(size, r):
    m = Image.new("L", size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], r, fill=255); return m

def info_card(i):
    it = L["items"][i]
    cw, ch = 880, 380
    card = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    sh = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([10, 16, cw - 6, ch - 2], 34, fill=(0, 0, 0, 90))
    card.alpha_composite(sh.filter(ImageFilter.GaussianBlur(12)))
    body = Image.new("RGBA", (cw - 16, ch - 20), PAPER + (255,)); body.putalpha(rr(body.size, 30))
    card.alpha_composite(body, (0, 0))
    ph = crops[i].resize((300, 300), Image.LANCZOS).convert("RGBA"); ph.putalpha(rr((300, 300), 22))
    card.alpha_composite(ph, (30, 30))
    d = ImageDraw.Draw(card)
    txt(d, (360, 28), f"{i + 1:02d}", SF(64), ACC_D)
    txt(d, (455, 46), it["cat"], F(30, "Bold"), (120, 116, 110))
    txt(d, (360, 128), it["name"], F(48), INK)
    txt(d, (360, 196), it["pt"], F(31, "Medium"), (70, 68, 64))
    br = it["brand"]
    txt(d, (360, 244), br, F(30, "Medium"), (130, 126, 118))
    f = F(30, "Bold"); s = "검색  " + it["find"]
    w = d.textlength(s, font=f)
    d.rounded_rectangle([360, 290, 360 + w + 36, 340], 25, fill=BRAND)
    txt(d, (378, 315), s, f, WHITE, "lm")
    return card

CARDS = [info_card(i) for i in range(4)]

def dot(img, x, y, a, n):
    d = ImageDraw.Draw(img)
    r = 15
    d.ellipse([x - r - 8, y - r - 8, x + r + 8, y + r + 8], outline=WHITE + (int(200 * a),), width=3)
    d.ellipse([x - r, y - r, x + r, y + r], fill=BRAND + (int(255 * a),), outline=WHITE + (int(255 * a),), width=3)
    txt(d, (x, y + 1), str(n), F(18), WHITE + (int(255 * a),), "mm")

# 타임라인
T_COVER, T_ITEM, T_END = 1.8, 2.3, 3.0
HOOK = L.get("hook")  # v4.3: 첫 화면 후킹 문구(2줄까지). 있으면 커버 2.4초로 늘려 읽을 시간 확보
if HOOK: T_COVER = 2.4

def wrap_hook(d, s, maxw=820):
    """후킹 문구를 최대 2줄로 — '\\n'이 있으면 그대로, 없으면 폭에 맞춰 자르고 글씨 크기 자동 조절"""
    for fs in range(70, 52, -2):
        f = F(fs)
        if "\n" in s:
            lines = s.split("\n")[:2]
        else:
            words, lines, cur = s.split(), [], ""
            for w_ in words:
                t_ = (cur + " " + w_).strip()
                if d.textlength(t_, font=f) > maxw and cur: lines.append(cur); cur = w_
                else: cur = t_
            lines.append(cur)
        if len(lines) <= 2 and all(d.textlength(l_, font=f) <= maxw for l_ in lines):
            return lines, f
    return lines[:2], F(54)
segs = [("cover", T_COVER)] + [(i, T_ITEM) for i in range(4)] + [("end", T_END)]
FR = OUT + "_frames"; shutil.rmtree(FR, ignore_errors=True); os.makedirs(FR)
full_c = (IW / 2, IH * 0.48)
n = 0; prev = (full_c[0], full_c[1], 1.0)
for kind, dur in segs:
    N = int(dur * FPS)
    for k in range(N):
        t = k / (N - 1)
        if kind == "cover":
            z = lerp(1.06, 1.0, ease(t))
            fr, _ = view(full_c[0], full_c[1], z)
            tsec = k / FPS
            if SPLIT:  # v4.4: 같은 룩 ON/OFF 비교 슬라이더 — 0초부터 분할, 1초 안에 경계선이 움직이고 끝에 ON으로 닦아내며 본편 시작
                fo, _ = view(full_c[0], full_c[1], z, stage_off)
                wipe = ease((tsec - (dur - 0.55)) / 0.5)
                dx = int((540 + 70 * math.sin(2 * math.pi * min(tsec, 1.6) / 1.6)) * (1 - wipe))
                if dx > 0: fr.paste(fo.crop((0, 0, dx, H)), (0, 0))
            fr = shade(fr, 200, 210, 640, 760)
            d = ImageDraw.Draw(fr)
            if SPLIT and dx > 0:
                ca = int(255 * (1 - wipe))
                d.line([(dx, 0), (dx, H)], fill=WHITE + (ca,), width=6)
                d.ellipse([dx - 34, 1010 - 34, dx + 34, 1010 + 34], fill=BRAND + (ca,), outline=WHITE + (ca,), width=4)
                txt(d, (dx, 1010), "◀▶", F(22, "Bold"), WHITE + (ca,), "mm")
                fl = F(42)
                for lab, x_, col in ((SPLIT["off_label"], 60, (40, 40, 44)), (SPLIT["on_label"], 600, BRAND)):
                    w_ = d.textlength(lab, font=fl)
                    if x_ == 60 and 60 + w_ + 48 > dx - 50: continue  # 경계선에 가리면 숨김
                    if x_ == 600 and dx > 560: x_ = max(x_, dx + 40)
                    if x_ + w_ + 48 > 930: continue
                    d.rounded_rectangle([x_, 1120, x_ + w_ + 48, 1196], 38, fill=col + (ca,))
                    txt(d, (x_ + 24, 1158), lab, fl, WHITE + (ca,), "lm")
            # v4.3: 0초 첫 프레임부터 글자가 다 보이게(페이드인 없음) — 스크롤 멈추게 하는 건 첫 화면
            txt(d, (60, 140), f"셀럽 스냅 해부  #{L['episode']}", F(40, "Bold"), WHITE + (255,))
            d.line([(60, 200), (180, 200)], fill=BRAND, width=6)
            if not L.get("cover_no_celeb"):
                fs_c = 88
                while d.textlength(L["celeb"], font=F(fs_c)) > 820 and fs_c > 60: fs_c -= 2  # 이름이 길면 줄여서 오른쪽 140px 금지구역 보호
                txt(d, (60, 232 + (88 - fs_c) // 2), L["celeb"], F(fs_c), WHITE + (255,))
            if HOOK:
                hl, hf = wrap_hook(d, HOOK, 790)
                lh = int(hf.size * 1.24); bw = max(d.textlength(l_, font=hf) for l_ in hl)
                hy0 = 250 if L.get("cover_no_celeb") else 362; hy1 = hy0 + lh * len(hl) + 70
                fr = fr.convert("RGBA"); ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
                od.rounded_rectangle([40, hy0 - 18, 40 + bw + 64, hy1], 22, fill=(12, 12, 14, 175))  # 사진 위에서도 잘 읽히게 어두운 판
                od.rectangle([40, hy0 - 18, 50, hy1], fill=BRAND + (255,))  # 브랜드 틸 세로 막대
                fr.alpha_composite(ov); d = ImageDraw.Draw(fr)
                hy = hy0
                for ln in hl:
                    txt(d, (70, hy), ln, hf, WHITE + (255,)); hy += lh
                txt(d, (70, hy + 4), L.get("cover_sub", L["title"]), F(36, "Bold"), (190, 228, 226, 255))
            else:
                txt(d, (60, 352), L["title"], F(52, "Bold"), (240, 236, 228, 255))
            b = 1.0 if HOOK else ease(t * 2.5 - .8)
            if b > 0:
                f = F(40, "Bold"); s = L.get("hook_cta", "포인트 4개만 기억하세요 →")
                w = d.textlength(s, font=f)
                d.rounded_rectangle([60, 1250, 60 + w + 56, 1340], 45, fill=BRAND + (int(255 * b),))
                txt(d, (88, 1295), s, f, WHITE + (int(255 * b),), "lm")
            prev = (full_c[0], full_c[1], 1.0)
        elif kind == "end":
            fr, _ = view(full_c[0], full_c[1], 1.0)
            fr = fr.filter(ImageFilter.GaussianBlur(18 * ease(t * 2)))
            fr = fr.convert("RGBA"); fr.alpha_composite(Image.new("RGBA", (W, H), (12, 12, 14, int(150 * ease(t * 2)))))
            d = ImageDraw.Draw(fr)
            a = ease(t * 2.5)
            txt(d, (60, 120), "오늘의 포인트 4", F(64), WHITE + (int(255 * a),))
            d.line([(60, 214), (60 + 120 * a, 214)], fill=BRAND + (int(255 * a),), width=6)
            txt(d, (60, 236), f"{L['celeb']} · {L['title']}", F(32, "Medium"), (230, 230, 230, int(255 * a)))
            for i in range(4):
                p = ease(t * 3 - i * 0.18)
                if p <= 0: continue
                gx = 60 + int((1 - p) * 60); gy = 300 + i * 252
                row = Image.new("RGBA", (880, 236), PAPER + (255,)); row.putalpha(rr((880, 236), 26))
                ph = crops[i].resize((204, 204), Image.LANCZOS).convert("RGBA"); ph.putalpha(rr((204, 204), 18))
                row.alpha_composite(ph, (16, 16))
                td = ImageDraw.Draw(row)
                txt(td, (246, 20), f"{i + 1:02d}", SF(46), ACC_D)
                txt(td, (324, 30), L["items"][i]["cat"], F(30, "Bold"), (120, 116, 110))
                nm = L["items"][i]["name"]
                txt(td, (246, 84), nm, F(48 if len(nm) <= 10 else 44), INK)
                if "추천" in L["items"][i]["brand"]:
                    tg = F(30, "Bold"); tw_ = td.textlength("추천", font=tg)
                    td.rounded_rectangle([840 - tw_ - 30, 26, 852, 72], 23, outline=(120, 116, 110), width=2)
                    txt(td, (846 - tw_ - 12, 49), "추천", tg, (110, 106, 100), "lm")
                fs = F(30, "Bold"); sch = "검색  " + L["items"][i]["find"]
                w2 = td.textlength(sch, font=fs)
                td.rounded_rectangle([246, 160, 246 + w2 + 36, 212], 26, fill=BRAND)
                txt(td, (264, 186), sch, fs, WHITE, "lm")
                row.putalpha(row.getchannel("A").point(lambda v: int(v * p)))
                fr.alpha_composite(row, (gx, gy))
            b = ease(t * 2.5 - 1.2)
            if b > 0:
                f = F(42); s = "저장하고 따라 입기"
                w = d.textlength(s, font=f)
                d.rounded_rectangle([60, 1326, 60 + w + 64, 1414], 44, fill=BRAND + (int(255 * b),))
                txt(d, (92, 1370), s, f, WHITE + (int(255 * b),), "lm")
                txt(d, (60 + w + 96, 1370), "@zzebi.st", F(38, "Bold"), WHITE + (int(255 * b),), "lm")
        else:
            i = kind; it = L["items"][i]
            tx, ty = it["pt_xy"]
            m = eio(min(1, t / 0.45))
            cx = lerp(prev[0], tx, m); cy = lerp(prev[1], ty, m); z = lerp(prev[2], 1.32, m)
            fr, (x0, y0, s) = view(cx, cy, z)
            fr = shade(fr, 195, 120, 440, 520)  # v4.2: 헤더 보조글씨 대비 강화
            sx, sy = (tx - x0) * s, (ty - y0) * s
            if sy > 340: header(fr)  # 점이 헤더 영역에 올 때는 헤더를 숨겨 겹침 방지
            da = ease((t - 0.3) / 0.15)
            if da > 0:
                ca = ease((t - 0.38) / 0.18)
                cy0 = 1040 if sy < 980 else 430
                if ca > 0:
                    d = ImageDraw.Draw(fr)
                    ex, ey = 520, (cy0 if cy0 > sy else cy0 + 360)
                    d.line([(sx, sy), (lerp(sx, ex, ca), lerp(sy, ey, ca))], fill=WHITE + (int(220 * ca),), width=3)
                    c = CARDS[i].copy(); c.putalpha(c.getchannel("A").point(lambda v: int(v * ca)))
                    fr.alpha_composite(c, (60, int(cy0 + (1 - ca) * 50)))
                dot(fr, sx, sy, da, i + 1)
            if t > 0.9: prev = (tx, ty, 1.32)
        fr.convert("RGB").save(os.path.join(FR, f"{n:04d}.jpg"), quality=92)
        if kind == "cover" and COVER_OUT and k == (min(N - 1, int(L.get("cover_t", 99) * FPS)) if SPLIT else N - 1): fr.convert("RGB").save(COVER_OUT, quality=94)
        n += 1
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(FR, "%04d.jpg"),
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT], check=True)
shutil.rmtree(FR)
print("done", OUT, f"{n / FPS:.1f}s")
