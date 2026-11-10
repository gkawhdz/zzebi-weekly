#!/usr/bin/env python3
"""코디 스케치 숏츠 생성기 v2 — 패션 디자이너 크로키 스타일
사람의 왼쪽 절반은 마커·색연필 채색, 오른쪽 절반은 연필 스케치(해칭).
사용법: python3 make_lookbook.py lookbook.json out.mp4

look 항목
  hair: bun | short | long | bob      hair_color, skin (HEX)      legwear(선택, 스타킹 색)
  top    : {type: knit | turtleneck | tee | shirt | hoodie, color, texture}
  outer  : {type: coat_long | trench | jacket | blazer | puffer | cardigan | vest, color, texture, open, length(밑단 y, 예: 960 엉덩이·1190 무릎·1440 발목), belt, belt_y(벨트 높이, 기본 712·높게 650)}
  bottom : {type: wide_pants | straight | slacks | cargo | skirt_mini | skirt_midi | skirt_long, color, texture}
  dress  : true 이면 상의+스커트를 원피스처럼(허리 밴드·밑단 골지 생략, top과 bottom 색을 같게)
  mirror : true 이면 포즈 좌우 반전(체중이 반대 다리) — 매일 포즈를 섞으세요
  shoes  : {type: loafer | boots | sneakers, color, texture}
  acc    : [{type: scarf | bag_shoulder | tote | beanie | belt, color, color2(체크 보조색), texture}]
질감: smooth, knit, rib, cable, herringbone, tweed, wool, boucle, corduroy, denim, leather, suede,
      puffer, check, fleece, satin, cotton
scenes: hook / look / detail / text   (예시는 lookbook_example.json)
v3(2026-10-26): 오른쪽 말풍선·확대 카드가 x 940 안에서 끝나도록(릴스·틱톡 오른쪽 버튼 영역 회피),
  text 장면은 make_short v3의 체크 카드("points")와 사선 와이프 전환을 그대로 사용.
"""
import json, sys, os, subprocess, tempfile, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_short as MS

W, H, FPS = 1080, 1920, 30
S = 2                       # 내부 고해상도 배율
INK = (52, 46, 44)          # 채색 쪽 선
GRAPHITE = (78, 78, 84)     # 연필 쪽 선
PAPER = (245, 241, 234)
SKETCH_FILL = (249, 246, 240)

def rgb(h): return MS.hex2rgb(h) if isinstance(h, str) else tuple(h)
def F(b, s): return MS.font(MS.FONT_B if b else MS.FONT_R, s)
def ease(t): return MS.ease(t)
def mixc(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

# ---------------- 곡선 도구 ----------------
def smooth(pts, closed=True, n=7):
    P = [(p[0], p[1]) for p in pts]; C = [len(p) > 2 for p in pts]; L = len(P); out = []
    idx = range(L) if closed else range(L - 1)
    for i in idx:
        g = lambda k: P[k % L] if closed else P[min(max(k, 0), L - 1)]
        p0, p1, p2, p3 = g(i - 1), g(i), g(i + 1), g(i + 2)
        if C[i]: p0 = p1
        if C[(i + 1) % L]: p3 = p2
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in range(2)))
    if not closed: out.append(P[-1])
    return out

def limb(centers, widths, n=8):
    """관절 중심선 + 폭 → 팔·다리·소매·바지 외곽선"""
    c = smooth(centers, closed=False, n=n)
    ws = np.interp(np.linspace(0, len(widths) - 1, len(c)), range(len(widths)), widths)
    left, right = [], []
    for i, (x, y) in enumerate(c):
        a = c[max(i - 1, 0)]; b = c[min(i + 1, len(c) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) + 1e-6
        nx, ny = -dy / L, dx / L
        left.append((x + nx * ws[i] / 2, y + ny * ws[i] / 2)); right.append((x - nx * ws[i] / 2, y - ny * ws[i] / 2))
    return left + right[::-1], left, right

def mirror(pts): return [((1080 - p[0], p[1]) + tuple(p[2:])) for p in pts]
def shift(pts, dx, dy): return [((p[0] + dx, p[1] + dy) + tuple(p[2:])) for p in pts]
def ell(cx, cy, rx, ry, n=40): return [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]
def hi(pts): return [(p[0] * S, p[1] * S) for p in pts]

# ---------------- 질감 (곱해지는 밝기 변화) ----------------
def noise(rng, w, h, sx, sy, amp):
    a = rng.random((max(2, h // sy), max(2, w // sx)))
    im = Image.fromarray((a * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
    return (np.asarray(im, np.float32) / 255 - 0.5) * 2 * amp

def fabric(kind, x0, y0, w, h, rng, u):
    xx, yy = np.meshgrid(np.arange(x0, x0 + w, dtype=np.float32), np.arange(y0, y0 + h, dtype=np.float32))
    s = S; m = np.zeros((h, w), np.float32)
    if kind in ("rib", "cable"):
        m += 0.07 * np.cos(2 * np.pi * xx / (6 * s))
    if kind == "cable":
        per = 46 * s; c = (xx // per) * per + per / 2; dx = xx - c; ph = yy / (13 * s); a = 9 * s
        r1 = np.clip(1 - np.abs(dx - a * np.sin(ph)) / (8 * s), 0, 1)
        r2 = np.clip(1 - np.abs(dx + a * np.sin(ph)) / (8 * s), 0, 1)
        front = np.where(np.cos(ph) > 0, r1, r2); back = np.where(np.cos(ph) > 0, r2, r1)
        m += 0.16 * front ** 0.7 + 0.05 * back - 0.07 * (np.abs(dx) > 17 * s)
    if kind == "knit":
        v = np.abs(((xx / (5 * s)) % 2) - 1) * 2 - 1
        m += 0.06 * np.sin(2 * np.pi * (yy / (5 * s) + 0.5 * v))
    if kind in ("herringbone", "tweed"):
        band = (xx // (7 * s)) % 2
        t = np.where(band == 0, xx + yy, xx - yy)
        m += 0.055 * np.cos(2 * np.pi * t / (4 * s))
    if kind in ("tweed", "boucle"):
        f = rng.random((h, w)).astype(np.float32)
        m += np.where(f > 0.992, 0.30, 0) + np.where(f < 0.008, -0.25, 0) + noise(rng, w, h, 2 * s, 2 * s, 0.05)
    if kind in ("wool", "boucle", "fleece", "suede"):
        m += noise(rng, w, h, 3 * s, 3 * s, 0.05) + noise(rng, w, h, 18 * s, 18 * s, 0.05)
    if kind == "corduroy":
        m += 0.10 * np.cos(2 * np.pi * xx / (7 * s)) ** 3 + 0.04 * np.cos(2 * np.pi * xx / (7 * s))
    if kind == "denim":
        m += 0.06 * np.cos(2 * np.pi * (xx + yy) / (3 * s)) + noise(rng, w, h, 1 * s, 14 * s, 0.07)
        m += 0.12 * np.exp(-((u - 0.42) / 0.16) ** 2)  # 허벅지 워싱
    if kind == "cotton":
        m += noise(rng, w, h, 2 * s, 2 * s, 0.025)
    if kind == "puffer":
        p = ((yy - y0) % (64 * s)) / (64 * s)
        m += 0.22 * np.sin(np.pi * p) - 0.14 - 0.25 * (p < 0.03)
    if kind in ("satin", "leather"):
        m += 0.20 * np.exp(-((u - 0.30) / 0.09) ** 2) + 0.08 * np.exp(-((u - 0.75) / 0.05) ** 2)
    if kind == "leather":
        m += noise(rng, w, h, 2 * s, 2 * s, 0.02)
    return m

def check_overlay(x0, y0, w, h, color2):
    xx, yy = np.meshgrid(np.arange(x0, x0 + w), np.arange(y0, y0 + h))
    s = S; per = 34 * s
    gx = ((xx % per) < 7 * s); gy = ((yy % per) < 7 * s)
    thin = ((xx % per) == 17 * s) | ((yy % per) == 17 * s)
    a = gx.astype(np.float32) * 0.55 + gy.astype(np.float32) * 0.55
    return np.clip(a, 0, 0.85), thin

# ---------------- 렌더러 ----------------
class Canvas:
    def __init__(self, seed):
        self.rng = np.random.default_rng(seed)
        self.color = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
        self.sketch = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
        hx = np.zeros((32 * S, 32 * S), np.uint8)
        for k in range(-32 * S, 32 * S, 7 * S):
            for i in range(32 * S):
                j = i + k
                if 0 <= j < 32 * S: hx[i, j] = 255
        self.hatch_tile = Image.fromarray(hx).filter(ImageFilter.GaussianBlur(0.6))

    def pencil(self, layer, pts, closed, color, alpha, width, jitter=0.8):
        d = ImageDraw.Draw(layer); rng = self.rng
        P = pts + ([pts[0]] if closed else [])
        for pas in range(2):
            wv = width if pas == 0 else width * 0.45
            al = alpha if pas == 0 else alpha * 0.55
            prev = None
            for i, (x, y) in enumerate(P):
                j = rng.normal(0, jitter * S * (1 + pas))
                q = (x + j, y + rng.normal(0, jitter * S * (1 + pas)))
                if prev is not None:
                    taper = 0.55 + 0.45 * math.sin(math.pi * i / max(1, len(P) - 1)) if not closed else 0.75 + 0.25 * math.sin(i * 0.37)
                    ww = max(1, int(wv * S * taper * (0.8 + 0.4 * rng.random())))
                    d.line([prev, q], fill=color + (int(al * (0.75 + 0.25 * rng.random())),), width=ww)
                prev = q

    def shape(self, pts1x, color, kind="smooth", folds=(), shade=True, line=True, hatch=True, highlight=None,
              color2=None, stitch=None, n=7, smooth_it=True, flat=False):
        pts = hi(smooth(pts1x, True, n) if smooth_it else pts1x)
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        x0, y0 = int(max(0, min(xs) - 4)), int(max(0, min(ys) - 4))
        x1, y1 = int(min(W * S, max(xs) + 5)), int(min(H * S, max(ys) + 5))
        w, h = x1 - x0, y1 - y0
        if w < 3 or h < 3: return
        mk = Image.new("L", (w, h), 0); ImageDraw.Draw(mk).polygon([(x - x0, y - y0) for x, y in pts], fill=255)
        M = np.asarray(mk, np.float32) / 255
        has = M > 0.5; cols = np.arange(w)[None, :]
        anyr = has.any(1)
        xmin = np.where(anyr, has.argmax(1), 0)[:, None]; xmax = np.where(anyr, w - 1 - has[:, ::-1].argmax(1), 1)[:, None]
        u = np.clip((cols - xmin) / np.maximum(1, xmax - xmin), 0, 1).astype(np.float32)
        # 형태 음영 (빛은 왼쪽 위)
        sh = (0.30 * np.clip((u - 0.52) / 0.48, 0, 1) ** 1.4 + 0.10 * np.clip((0.10 - u) / 0.10, 0, 1)
              - 0.07 * np.exp(-((u - 0.30) / 0.17) ** 2)) if shade and not flat else np.zeros_like(u)
        # ----- 채색 레이어 -----
        base = np.array(rgb(color), np.float32)
        m = fabric(kind, x0, y0, w, h, self.rng, u) + noise(self.rng, w, h, 3 * S, 40 * S, 0.035)  # 마커 결
        img = base[None, None, :] * (1 + m[..., None]) * (1 - sh[..., None])
        if kind == "check":
            a, thin = check_overlay(x0, y0, w, h, color2)
            c2 = np.array(rgb(color2) if color2 else [v * 0.45 for v in base], np.float32)
            img = img * (1 - a[..., None]) + c2[None, None, :] * (1 - sh[..., None]) * a[..., None]
            img = np.where(thin[..., None], np.minimum(255, img * 1.25), img)
        img = np.clip(img, 0, 255).astype(np.uint8)
        bleed = mk.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
        bleed = Image.fromarray((np.asarray(bleed, np.float32) * (0.93 + 0.07 * self.rng.random((h, w)))).astype(np.uint8))
        tile = Image.fromarray(img).convert("RGBA"); tile.putalpha(bleed)
        self.color.alpha_composite(tile, (x0 - S, y0 + S // 2))
        # ----- 연필 레이어 (종이색으로 가리고 해칭) -----
        sk = Image.new("RGBA", (w, h), SKETCH_FILL + (0,)); sk.putalpha(mk)
        self.sketch.alpha_composite(sk, (x0, y0))
        if hatch and shade and not flat:
            ha = np.clip((sh - 0.06) * 3.2, 0, 0.75)
            tex = np.clip(-fabric(kind, x0, y0, w, h, self.rng, u) * 3.5, 0, 0.5) if kind not in ("smooth", "satin", "leather") else 0
            ht = np.asarray(self.hatch_tile.resize((32 * S, 32 * S)), np.float32) / 255
            reps = np.tile(ht, (h // (32 * S) + 1, w // (32 * S) + 1))[:h, :w]
            al = np.clip(ha * reps + tex * 0.5, 0, 1) * M * 200
            hl = Image.new("RGBA", (w, h), GRAPHITE + (0,)); hl.putalpha(Image.fromarray(al.astype(np.uint8)))
            self.sketch.alpha_composite(hl, (x0, y0))
        # ----- 하이라이트 · 접힘 · 스티치 · 외곽선 -----
        dk = tuple(int(v * 0.62) for v in base)
        if highlight or kind in ("leather", "satin", "puffer"):
            for (x, y) in pts[:: max(1, len(pts) // 18)]:
                pass
            rows = np.where(anyr)[0]
            if len(rows) > 10:
                lx = [(x0 + xmin[r, 0] + 0.2 * (xmax[r, 0] - xmin[r, 0]), y0 + r) for r in rows[::12 * S]]
                if len(lx) > 3:
                    seg = lx[len(lx) // 6: len(lx) * 4 // 5]
                    self.pencil(self.color, seg, False, (255, 255, 255), 120, 3.0, 0.5)
        for f in folds:
            fp = hi(smooth(f, False, 6))
            self.pencil(self.color, fp, False, dk, 150, 2.0, 0.4)
            self.pencil(self.sketch, fp, False, GRAPHITE, 170, 1.6, 0.4)
        if stitch:
            sp = hi(smooth(stitch, False, 6))
            d = ImageDraw.Draw(self.color)
            for i in range(0, len(sp) - 1, 2):
                d.line([sp[i], sp[i + 1]], fill=(214, 150, 70, 220), width=2 * S)
            d2 = ImageDraw.Draw(self.sketch)
            for i in range(0, len(sp) - 1, 3):
                d2.line([sp[i], sp[i + 1]], fill=GRAPHITE + (120,), width=S)
        if line:
            self.pencil(self.color, pts, True, INK, 175, 1.7)
            self.pencil(self.sketch, pts, True, GRAPHITE, 235, 1.9)

    def stroke(self, pts1x, color_c=INK, alpha=180, width=1.6, both=True):
        p = hi(smooth(pts1x, False, 6))
        self.pencil(self.color, p, False, color_c, alpha, width, 0.4)
        if both: self.pencil(self.sketch, p, False, GRAPHITE, alpha, width, 0.4)

# ---------------- 인체 (9등신 크로키, 왼발 체중) ----------------
HEAD = (540, 370, 44, 57)
NECK = [(524, 412), (556, 412), (563, 482), (517, 482)]
TORSO = [(517, 468), (563, 468), (606, 490), (642, 508, 'c'), (636, 600), (604, 720), (628, 840), (604, 905), (540, 918), (476, 905), (452, 840), (476, 720), (444, 600), (438, 508, 'c'), (474, 490)]
ARM_L = [(446, 514), (411, 716), (421, 902)]
ARM_R = [(634, 514), (677, 708), (648, 866)]
LEG_L = [(494, 846), (490, 1172), (495, 1466)]
LEG_R = [(586, 846), (592, 1170), (589, 1460)]
FOOT_L = [(482, 1458), (509, 1458), (513, 1496), (504, 1526, 'c'), (472, 1530, 'c'), (470, 1504)]
FOOT_R = shift(FOOT_L, 94, -6)

def draw_look(look, seed=3):
    cv = Canvas(seed)
    skin = rgb(look.get("skin", "#eccdb0")); hairc = rgb(look.get("hair_color", "#2a1d18")); hair = look.get("hair", "short")
    top, outer, bottom, shoes, accs = look.get("top", {}), look.get("outer"), look.get("bottom", {}), look.get("shoes", {}), look.get("acc", [])
    acc = {a["type"]: a for a in accs}
    # 바닥 그림자
    sh = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse(hi([(400, 1516), (690, 1552)]), fill=(60, 54, 52, 55))
    sh = sh.filter(ImageFilter.GaussianBlur(8 * S)); cv.color.alpha_composite(sh); cv.sketch.alpha_composite(sh)
    # 뒷머리
    if hair in ("long", "bob"):
        bot = 580 if hair == "long" else 452
        cv.shape([(494, 340), (480, 440), (474, bot, 'c'), (606, bot, 'c'), (600, 440), (586, 340)], hairc, "satin", shade=True,
                 folds=[[(510, 370), (502, bot - 20)], [(570, 370), (580, bot - 20)]])
    if top.get("type") == "hoodie":
        cv.shape([(486, 505), (494, 448), (540, 436), (586, 448), (594, 505)], top.get("color", "#888"), top.get("texture", "fleece"))
    # 피부: 다리 → 팔 → 목 → 몸통
    legc = rgb(look["legwear"]) if look.get("legwear") else skin
    for c, wv in ((LEG_L, [96, 52, 30]), (LEG_R, [94, 52, 30])):
        cv.shape(limb(c, wv)[0], legc, "smooth", shade=True, hatch=bool(look.get("legwear")), n=3)
    hand_r = ell(646, 888, 16, 24)
    cv.shape(hand_r, skin, flat=True)
    cv.shape(limb(ARM_L, [54, 40, 32])[0], skin, n=3)
    cv.shape(limb(ARM_R, [54, 40, 32])[0], skin, n=3)
    cv.shape(ell(424, 932, 16, 26), skin, flat=True, folds=[[(418, 940), (420, 952)]])
    cv.shape(NECK, skin, smooth_it=False, folds=[[(532, 470), (540, 476), (548, 470)]])
    cv.shape(TORSO, skin, hatch=False)
    btype = bottom.get("type", "straight")
    pants = btype in ("wide_pants", "straight", "slacks", "cargo")

    def draw_shoes():
        if not shoes: return
        st = shoes.get("type", "loafer"); c = shoes.get("color", "#2a1d17"); k = shoes.get("texture", "leather")
        for foot in (FOOT_L, FOOT_R):
            if st == "boots":
                fx, fy = foot[0]
                cv.shape([(fx - 6, fy - 82), (fx + 30, fy - 82)] + foot[2:] + [(fx - 12, fy - 20)], c, k, highlight=True,
                         folds=[[(fx + 2, fy - 30), (fx + 22, fy - 34)]])
            elif st == "sneakers":
                big = [(p[0] + (-6 if i > 3 else 4 if i in (1, 2) else -4), p[1] + (-4 if i < 2 else 4)) + tuple(p[2:]) for i, p in enumerate(foot)]
                cv.shape(big, c, k)
                cv.shape([(big[5][0] - 2, big[3][1] - 12), (big[2][0] + 6, big[3][1] - 12), (big[2][0] + 6, big[3][1] + 6, 'c'), (big[5][0] - 4, big[3][1] + 8, 'c')], "#f6f4ee", "smooth", flat=True)
            else:
                cv.shape(foot, c, k, highlight=True, folds=[[(foot[0][0] + 4, foot[0][1] + 18), (foot[1][0] - 2, foot[0][1] + 16)]])

    # 하의
    bc, bk = bottom.get("color", "#333"), bottom.get("texture", "smooth")
    if pants:
        draw_shoes()
        WID = {"wide_pants": ([104, 100, 108], [(492, 846), (486, 1172), (481, 1488)], [(588, 846), (596, 1170), (603, 1484)]),
               "cargo": ([104, 98, 102], [(492, 846), (486, 1172), (482, 1486)], [(588, 846), (596, 1170), (601, 1482)]),
               "straight": ([100, 68, 60], [(493, 846), (490, 1172), (494, 1488)], [(587, 846), (592, 1170), (589, 1482)]),
               "slacks": ([100, 66, 56], [(493, 846), (490, 1172), (494, 1486)], [(587, 846), (592, 1170), (589, 1480)])}[btype]
        wv, cl, cr = WID
        for i, cc in enumerate((cl, cr)):
            poly, le, ri = limb(cc, wv)
            folds = [[(cc[1][0] - 16, 1150), (cc[1][0] + 2, 1166), (cc[1][0] + 14, 1158)], [(cc[2][0] - 18, 1440), (cc[2][0] + 6, 1452)]]
            if btype == "slacks": folds.append([(cc[0][0] + 6, 880), (cc[1][0] + 2, 1170), (cc[2][0], 1470)])
            stitch = [(p[0] + 6, p[1]) for p in le[2:-2:3]] if bk == "denim" else None
            cv.shape(poly, bc, bk, folds=folds, stitch=stitch, n=3)
            if btype == "cargo":
                px = cc[1][0] - 50 if i == 0 else cc[1][0] + 8
                cv.shape([(px, 1010), (px + 44, 1010), (px + 46, 1100, 'c'), (px - 2, 1100, 'c')], bc, bk, folds=[[(px, 1022), (px + 44, 1022)]])
        cv.shape([(476, 722, 'c'), (604, 722, 'c'), (632, 850), (540, 930), (448, 850)], bc, bk,
                 folds=[[(540, 760), (540, 900)], [(520, 880), (540, 905), (560, 880)]], stitch=[(486, 760), (520, 770)] if bk == "denim" else None)
        cv.shape([(476, 720, 'c'), (604, 720, 'c'), (606, 744, 'c'), (474, 744, 'c')], bc, bk, hatch=False)
    else:
        hem = {"skirt_midi": 1215, "skirt_long": 1390}.get(btype, 962)
        hw = {"skirt_midi": 138, "skirt_long": 150}.get(btype, 112)
        cv.shape([(476, 722, 'c'), (604, 722, 'c'), (634, 850), (540 + hw, hem, 'c'), (540 - hw, hem, 'c'), (446, 850)], bc, bk,
                 folds=[[(500, 860), (470, hem - 10)], [(540, 870), (540, hem - 8)], [(585, 860), (612, hem - 10)]])
        if not look.get("dress"):
            cv.shape([(476, 720, 'c'), (604, 720, 'c'), (606, 744, 'c'), (474, 744, 'c')], bc, bk, hatch=False)
        draw_shoes()
    if "belt" in acc:
        a = acc["belt"]; cv.shape([(474, 724, 'c'), (606, 724, 'c'), (607, 742, 'c'), (473, 742, 'c')], a.get("color", "#2a1d17"), a.get("texture", "leather"), highlight=True)
        cv.shape([(530, 722, 'c'), (552, 722, 'c'), (552, 744, 'c'), (530, 744, 'c')], "#c9a86a", "satin", flat=True)
    # 상의
    if top:
        tt = top.get("type", "knit"); tc = top.get("color", "#ddd"); tk = top.get("texture", "knit")
        hem_t = 760 if look.get("dress") else 860
        body = [(514, 470), (540, 490 if tt != "turtleneck" else 478), (566, 470), (608, 488), (650, 508, 'c'), (644, 600), (612, 722), (636, hem_t, 'c'), (444, hem_t, 'c'), (468, 722), (436, 600), (430, 508, 'c'), (472, 488)]
        if tt == "shirt":
            body[1] = (540, 520)
        cv.shape(body, tc, tk, folds=[[(476, 760), (520, 790)], [(604, 770), (568, 800)], [(470, 620), (488, 660)]])
        if tt in ("tee",):
            for arm in (ARM_L, ARM_R):
                cv.shape(limb(arm[:2] if False else [arm[0], (arm[0][0] + (arm[1][0] - arm[0][0]) * 0.55, arm[0][1] + (arm[1][1] - arm[0][1]) * 0.55)], [66, 60])[0], tc, tk, n=3)
        else:
            for arm in (ARM_L, ARM_R):
                ext = [arm[0], arm[1], (arm[2][0], arm[2][1] - 6)]
                cv.shape(limb(ext, [64, 52, 44])[0], tc, tk, n=3,
                         folds=[[(arm[1][0] - 16, arm[1][1] - 8), (arm[1][0] + 4, arm[1][1] + 6)], [(arm[1][0] - 10, arm[1][1] + 26), (arm[1][0] + 12, arm[1][1] + 22)]])
        if tt in ("knit", "turtleneck", "hoodie"):
            dk = tuple(int(v * 0.88) for v in rgb(tc))
            if not look.get("dress"):
                cv.shape([(440, 832), (640, 832), (636, hem_t, 'c'), (444, hem_t, 'c')], dk, "rib", hatch=False)
            for arm in (ARM_L, ARM_R):
                cv.shape(limb([(arm[2][0] - 1, arm[2][1] - 30), (arm[2][0], arm[2][1] - 6)], [46, 44])[0], dk, "rib", hatch=False, n=2)
        if tt == "knit":
            dk = tuple(int(v * 0.88) for v in rgb(tc))
            cv.shape([(510, 466), (540, 484), (570, 466), (575, 476), (540, 498), (505, 476)], dk, "rib", hatch=False)
        if tt == "turtleneck":
            cv.shape([(519, 436, 'c'), (561, 436, 'c'), (570, 484), (540, 492), (510, 484)], tc, "rib", folds=[[(522, 450), (558, 452)], [(520, 466), (560, 469)]])
        if tt == "shirt":
            cv.shape([(514, 470), (532, 460), (541, 522), (522, 528)], tc, tk, flat=True)
            cv.shape(mirror([(514, 470), (532, 460), (541, 522), (522, 528)]), tc, tk, flat=True)
            cv.stroke([(540, 522), (540, 856)], alpha=140, width=1.2)
            for by in (560, 640, 720, 800):
                cv.shape(ell(540, by, 4, 4, 12), "#efe9df", flat=True)
        if tt == "hoodie":
            cv.stroke([(528, 492), (526, 600)], width=1.6); cv.stroke([(552, 492), (555, 600)], width=1.6)
            cv.shape([(486, 740), (594, 740), (606, 820, 'c'), (474, 820, 'c')], tc, tk, folds=[[(486, 742), (594, 742)]])
    # 아우터
    if outer:
        ot = outer.get("type", "coat_long"); oc = outer.get("color", "#8a6a4a"); ok = outer.get("texture", "wool"); op = outer.get("open", True)
        hem = outer.get("length") or {"coat_long": 1190, "trench": 1200, "jacket": 880, "blazer": 868, "puffer": 884, "cardigan": 856, "vest": 872}[ot]
        is_vest = ot == "vest"
        if is_vest: ot = "puffer" if ok == "puffer" else "cardigan"
        ix = 500 if op else 546
        if ot == "puffer":
            panel = [(522, 452), (470, 474), (402, 506, 'c'), (394, 600), (404, 722), (398, hem, 'c'), (544, hem + 4, 'c'), (544, 456)]
            sw = [84, 72, 64]
        else:
            waist = 438 if ot in ("blazer", "trench") else 428
            flare = 404 if ot in ("coat_long", "trench") else 416
            panel = [(518, 468), (476, 486), (420, 506, 'c'), (414, 600), (waist, 722), (424, 860), (flare, hem, 'c'), (ix - 4, hem + 6, 'c'), (ix, 800), (522, 560)]
            sw = [72, 58, 50]
        for arm in (() if is_vest else (ARM_L, ARM_R)):
            ext = [arm[0], arm[1], (arm[2][0] + (arm[2][0] - arm[1][0]) * 0.06, arm[2][1] + 8)]
            folds = [[(arm[1][0] - 22, arm[1][1] - 12), (arm[1][0] + 6, arm[1][1] + 6)], [(arm[1][0] - 16, arm[1][1] + 30), (arm[1][0] + 16, arm[1][1] + 24)]]
            if ot == "puffer": folds += [[(arm[0][0] - 30, 620), (arm[0][0] + 20, 628)], [(arm[1][0] - 30, 800), (arm[1][0] + 20, 806)]]
            cv.shape(limb(ext, sw)[0], oc, ok, folds=folds, n=3)
        drape = [[(470, 900), (456, hem - 20)], [(500, 760), (494, hem - 30)]] if hem > 1000 else [[(470, 760), (480, hem - 16)]]
        if ot == "puffer": drape = [[(402, y), (544, y + 4)] for y in (580, 660, 740, 820)]
        for pn in (panel, mirror(panel)):
            fl = drape if pn is panel else [[(1080 - x, y) for x, y in f] for f in drape]
            cv.shape(pn, oc, ok, folds=fl)
        if ot in ("coat_long", "trench", "jacket", "blazer"):
            lp_dark = tuple(int(v * 0.9) for v in rgb(oc))
            lap = [(518, 468), (488, 490), (476, 560), (494, 580, 'c'), (484, 600), (510, 700 if ot != "blazer" else 740), (522, 560)]
            for l in (lap, mirror(lap)):
                cv.shape(l, lp_dark, ok, hatch=False)
            py = hem - 140 if hem > 1000 else hem - 90
            for flap in ([(430, py), (494, py - 2), (494, py + 22, 'c'), (432, py + 24, 'c')],):
                cv.shape(flap, lp_dark, ok, hatch=False); cv.shape(mirror(flap), lp_dark, ok, hatch=False)
            if not op:
                for by in (620, 720, 820):
                    cv.shape(ell(560, by, 7, 7, 14), "#2b2220", "leather", flat=True)
        if ot == "trench" or outer.get("belt"):
            bdk = tuple(int(v * 0.86) for v in rgb(oc)); by_ = outer.get("belt_y", 712)
            bl = [(426, by_), (512, by_ - 4), (512, by_ + 24), (428, by_ + 28)]
            cv.shape(bl, bdk, ok); cv.shape(mirror(bl), bdk, ok)
        if ot == "cardigan" and not is_vest:
            dk = tuple(int(v * 0.88) for v in rgb(oc))
            cv.shape([(420, 830), (ix, 830), (ix - 2, hem + 4, 'c'), (422, hem, 'c')], dk, "rib", hatch=False)
            cv.shape(mirror([(420, 830), (ix, 830), (ix - 2, hem + 4, 'c'), (422, hem, 'c')]), dk, "rib", hatch=False)
            for by in (640, 720, 800):
                cv.shape(ell(ix - 4, by, 5, 5, 12), "#e9e2d6", flat=True)
        if ot == "puffer":
            cv.shape([(500, 420, 'c'), (580, 420, 'c'), (592, 486), (540, 500), (488, 486)], oc, ok, folds=[[(504, 450), (576, 452)]])
    # 소품
    if "scarf" in acc:
        a = acc["scarf"]
        cv.shape([(510, 452), (570, 452), (590, 480), (580, 508), (540, 520), (500, 508), (490, 480)], a.get("color", "#7a1f33"), a.get("texture", "wool"),
                 color2=a.get("color2"), folds=[[(500, 478), (540, 494), (582, 478)]])
        cv.shape([(562, 500), (594, 496), (602, 690, 'c'), (572, 704, 'c')], a.get("color", "#7a1f33"), a.get("texture", "wool"), color2=a.get("color2"),
                 folds=[[(574, 520), (582, 690)]])
        for fx in range(574, 602, 6):
            cv.stroke([(fx, 700), (fx + 1, 716)], alpha=150, width=1.0)
    if "bag_shoulder" in acc:
        a = acc["bag_shoulder"]
        cv.shape([(468, 506), (476, 500), (656, 820), (646, 826)], a.get("strap", a.get("color", "#333")), "leather", smooth_it=False, hatch=False)
        cv.shape([(628, 812, 'c'), (726, 812, 'c'), (738, 910, 'c'), (616, 910, 'c')], a.get("color", "#4a2e1e"), a.get("texture", "leather"), highlight=True)
        cv.shape([(626, 812, 'c'), (728, 812, 'c'), (722, 856), (632, 856)], tuple(int(v * 0.85) for v in rgb(a.get("color", "#4a2e1e"))), a.get("texture", "leather"), hatch=False)
    if "tote" in acc:
        a = acc["tote"]
        cv.stroke([(394, 960), (408, 918), (428, 912), (446, 930), (460, 960)], alpha=200, width=2.4)
        cv.shape([(370, 956, 'c'), (484, 956, 'c'), (494, 1116, 'c'), (360, 1116, 'c')], a.get("color", "#d8cbb3"), a.get("texture", "cotton"), folds=[[(380, 1000), (392, 1100)]])
    # 머리
    face = [(540, 313), (574, 324), (586, 358), (580, 392), (562, 420), (540, 429), (518, 420), (500, 392), (494, 358), (506, 324)]
    cv.shape(face, skin, folds=[[(578, 370), (574, 396)]])
    lip = (176, 132, 86)
    for side in (-1, 1):  # 눈썹·눈
        cx = 540 + side * 17
        cv.stroke([(cx - 9, 318), (cx, 315), (cx + 9, 318)], alpha=170, width=1.4)
        cv.stroke([(cx - 8, 333), (cx, 330), (cx + 8, 333)], alpha=200, width=1.5)
        cv.stroke([(cx - 7, 334), (cx, 336), (cx + 7, 334)], alpha=90, width=1.0)
    cv.stroke([(541, 380), (538, 396), (543, 398)], alpha=130, width=1.1)
    cv.shape([(530, 410), (540, 406), (550, 410), (540, 416)], lip, flat=True, line=False)
    cv.stroke([(530, 410), (540, 412), (550, 410)], alpha=140, width=1.0)
    if "beanie" in acc:
        a = acc["beanie"]; bc2 = a.get("color", "#444")
        cv.shape([(488, 346, 'c'), (492, 302), (516, 276), (564, 276), (588, 302), (592, 346, 'c')], bc2, a.get("texture", "rib"), folds=[[(520, 290), (526, 330)], [(560, 290), (556, 330)]])
        cv.shape([(486, 324), (594, 324), (596, 350, 'c'), (484, 350, 'c')], tuple(int(v * 0.86) for v in rgb(bc2)), "rib", hatch=False)
    else:
        cap = [(492, 370, 'c'), (494, 330), (512, 308), (540, 302), (568, 308), (586, 330), (588, 370, 'c'), (580, 340), (556, 328), (530, 332), (500, 346)]
        strands = [[(500, 352), (512, 320), (540, 308)], [(526, 330), (548, 312), (576, 322)], [(560, 328), (578, 340), (584, 366)]]
        cv.shape(cap, hairc, "satin", folds=strands)
        if hair == "bun":
            cv.shape(ell(540, 294, 24, 20, 24), hairc, "satin", folds=[[(524, 292), (540, 284), (556, 292)]])
        if hair == "long":
            cv.shape([(494, 360), (488, 420), (484, 520, 'c'), (504, 500), (506, 440)], hairc, "satin", folds=[[(492, 400), (490, 480)]])
            cv.shape(mirror([(494, 360), (488, 420), (484, 520, 'c'), (504, 500), (506, 440)]), hairc, "satin", folds=[[(588, 400), (590, 480)]])
    return cv

def finish_figure(cv, split=True):
    """왼쪽 채색 + 오른쪽 연필. 경계는 붓 자국처럼 불규칙하게."""
    out = cv.sketch.copy()
    if split:
        rng = np.random.default_rng(11)
        yy, xx = np.mgrid[0:H * S, 0:W * S].astype(np.float32)
        xb = 578 * S + 14 * S * np.sin(yy / (190 * S)) + 6 * S * np.sin(yy / (37 * S))
        n = noise(rng, W * S, H * S, 5 * S, 60 * S, 0.45) + noise(rng, W * S, H * S, 2 * S, 14 * S, 0.18)
        m = np.clip((xb - xx) / (34 * S) + 0.5 + n, 0, 1) ** 1.3
        a = np.asarray(cv.color.getchannel("A"), np.float32) * m
        col = cv.color.copy(); col.putalpha(Image.fromarray(a.astype(np.uint8)))
        out.alpha_composite(col)
        d = ImageDraw.Draw(out)  # 오른쪽 크로키 가이드선
        for k in range(10):
            y = (262 + k * 128) * S
            d.line([(786 * S, y), (800 * S, y)], fill=GRAPHITE + (90,), width=S)
    else:
        out = cv.sketch.copy(); out.alpha_composite(cv.color)
    return out

ANCHOR = {"hair": (575, 330), "beanie": (575, 310), "outer": (432, 690), "top": (540, 600), "bottom": (604, 1080),
          "shoes": (600, 1500), "scarf": (588, 560), "bag_shoulder": (724, 870), "tote": (370, 1040), "belt": (592, 733)}
DETAIL = {"hair": (520, 340), "beanie": (520, 310), "outer": (460, 820), "top": (526, 640), "bottom": (488, 1080),
          "shoes": (492, 1500), "scarf": (526, 494), "bag_shoulder": (640, 862), "tote": (420, 1040), "belt": (520, 733)}

def item_color(look, item):
    if item in ("outer", "top", "bottom", "shoes"): return look.get(item, {}).get("color", "#888")
    for a in look.get("acc", []):
        if a["type"] == item: return a.get("color", "#888")
    return look.get("hair_color", "#333")

# ---------------- 장면 ----------------
def paper_bg(tint=None, wash=None):
    rng = np.random.default_rng(1)
    base = np.array(rgb(tint) if tint else PAPER, np.float32)
    n = noise(rng, W, H, 1, 1, 4) + noise(rng, W, H, 40, 40, 3)
    img = base[None, None, :] + n[..., None]
    if wash:  # 인물 뒤 수채 번짐
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xx - 470) / 300) ** 2 + ((yy - 900) / 620) ** 2) + noise(rng, W, H, 60, 60, 0.18)
        a = np.clip(1 - r, 0, 1) ** 0.8 * 0.22
        img = img * (1 - a[..., None]) + np.array(rgb(wash), np.float32)[None, None, :] * a[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")

def chrome(img, brand, prog, fg=INK):
    d = ImageDraw.Draw(img)
    d.rectangle([90, 150, W - 90, 158], fill=fg + (60,) if len(fg) == 3 else fg)
    d.rectangle([90, 150, 90 + int((W - 180) * prog), 158], fill=(0, 168, 168))
    d.text((90, 180), brand, font=F(False, 30), fill=fg)

def callout(img, anchor, side, y, name, sub, swatch, alpha):
    if alpha <= 0: return
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    a = int(255 * alpha); bw = 300; bx0 = 940 - bw if side == "R" else 28  # v3: 오른쪽 말풍선도 x 940 안(릴스 오른쪽 140px 안전영역)
    fs = F(False, 28)
    for size in (34, 30, 27):
        fn = F(True, size)
        if d.textlength(name, font=fn) <= bw - 80: break
    subl = MS.wrap(d, sub, fs, bw - 40) if sub else []
    bh = 72 + 36 * len(subl); by = max(230, min(1390 - bh, y - bh // 2))
    ax, ay = anchor; ex = bx0 if side == "R" else bx0 + bw
    d.line([(ax, ay), (ex, by + 36)], fill=INK + (a,), width=2)
    d.ellipse([ax - 8, ay - 8, ax + 8, ay + 8], fill=(255, 255, 255, a), outline=INK + (a,), width=3)
    d.rounded_rectangle([bx0, by, bx0 + bw, by + bh], radius=16, fill=(255, 253, 249, int(238 * alpha)), outline=INK + (a,), width=2)
    d.ellipse([bx0 + 18, by + 20, bx0 + 50, by + 52], fill=rgb(swatch) + (a,), outline=INK + (a,), width=2)
    d.text((bx0 + 62, by + 14), name, font=fn, fill=INK + (a,))
    for i, l in enumerate(subl):
        d.text((bx0 + 20, by + 64 + i * 36), l, font=fs, fill=(90, 80, 76, a))
    img.alpha_composite(lay)

BRAND = (0, 168, 168)       # 브랜드 틸 #00A8A8 (배지·진행바·CTA·포인트)
BRAND_DK = (0, 124, 124)

class Look:
    def __init__(self, spec, seed):
        self.spec = spec
        cv = draw_look(spec, seed)
        if spec.get("mirror"):  # v4: 포즈 좌우 반전
            cv.color = cv.color.transpose(Image.FLIP_LEFT_RIGHT); cv.sketch = cv.sketch.transpose(Image.FLIP_LEFT_RIGHT)
        self.cv = cv
        self.hi = finish_figure(cv, split=spec.get("split", True))
        self.lo = self.hi.resize((W, H), Image.LANCZOS)
        self._full = None
        self._v4 = None

    def v4(self, bg):
        """v4 합성본: 연필만(sk) / 완전 채색(co) — 저해상도·고해상도"""
        if self._v4 is None:
            sk_hi = self.cv.sketch
            co_hi = self.cv.sketch.copy(); co_hi.alpha_composite(self.cv.color)
            bgh = bg.resize((W * S, H * S))
            full_co = bgh.copy(); full_co.alpha_composite(co_hi)
            sk_lo = sk_hi.resize((W, H), Image.LANCZOS); co_lo = co_hi.resize((W, H), Image.LANCZOS)
            self._v4 = dict(sk_lo=sk_lo, co_lo=co_lo, full_co=full_co)
        return self._v4

    def anchor(self, item, table=None):
        x, y = (table or ANCHOR4)[item]
        return (1080 - x, y) if self.spec.get("mirror") else (x, y)

# v4: 카메라가 찾아갈 아이템 중심(그림 좌표, 반전 전 기준)
ANCHOR4 = {"hair": (540, 330), "beanie": (540, 320), "outer": (452, 700), "top": (540, 620), "bottom": (520, 1100),
           "shoes": (540, 1490), "scarf": (548, 520), "bag_shoulder": (676, 860), "tote": (426, 1040), "belt": (470, 720),
           "collar": (540, 470), "hem": (470, 1150)}

_REVEAL_NOISE = {}
def reveal_mask(p, angle=True):
    """붓 쓸기 마스크(저해상도): p 0→1 동안 왼쪽 위→오른쪽 아래로 채색이 번져 나감"""
    if "n" not in _REVEAL_NOISE:
        rng = np.random.default_rng(21)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        _REVEAL_NOISE["d"] = (xx / W) * 0.72 + (yy / H) * 0.28
        _REVEAL_NOISE["n"] = noise(rng, W, H, 3, 70, 0.07) + noise(rng, W, H, 30, 30, 0.03)
    d = _REVEAL_NOISE["d"] + _REVEAL_NOISE["n"]
    edge = -0.15 + 1.35 * p
    return np.clip((edge - d) / 0.06, 0, 1)

def compose_reveal(lk, bg, p, with_bg=True):
    v = lk.v4(bg); img = bg.copy() if with_bg else Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if p <= 0:
        img.alpha_composite(v["sk_lo"]); return img
    if p >= 1:
        img.alpha_composite(v["co_lo"]); return img
    m = reveal_mask(p)
    co = v["co_lo"].copy(); a = np.asarray(co.getchannel("A"), np.float32) * m
    co.putalpha(Image.fromarray(a.astype(np.uint8)))
    img.alpha_composite(v["sk_lo"]); img.alpha_composite(co)
    return img

def camera(lk, bg, z, fx, fy, sx=540, sy=760):
    """완전 채색 고해상도에서 (fx,fy)가 화면 (sx,sy)에 오도록 z배 확대"""
    full = lk.v4(bg)["full_co"]
    cw, ch = W * S / z, H * S / z
    x0 = fx * S - sx * S / z; y0 = fy * S - sy * S / z
    x0 = min(max(0, x0), W * S - cw); y0 = min(max(0, y0), H * S - ch)
    return full.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR)

def big_card(img, name, sub, swatch, a, num=None, total=None):
    """v4 큰 정보 카드: 화면 아래쪽(하단 25% 위), 아이템 이름 56px + 한 줄 설명 38px"""
    if a <= 0: return
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    al = int(255 * a); x0, x1 = 60, 940
    fn = F(True, 56)
    while d.textlength(name, font=fn) > x1 - x0 - 150 and fn.size > 40: fn = F(True, fn.size - 2)
    fs = F(False, 38); subl = MS.wrap(d, sub, fs, x1 - x0 - 80) if sub else []
    h = 120 + 52 * len(subl); y1 = 1420; y0 = y1 - h + int(40 * (1 - a))
    d.rounded_rectangle([x0, y0, x1, y1 + int(40 * (1 - a))], radius=30, fill=(255, 253, 249, int(242 * a)))
    d.rectangle([x0, y0 + 26, x0 + 10, y0 + 96], fill=BRAND + (al,))
    d.ellipse([x0 + 36, y0 + 30, x0 + 96, y0 + 90], fill=rgb(swatch) + (al,), outline=INK + (al,), width=3)
    d.text((x0 + 116, y0 + 22), name, font=fn, fill=INK + (al,))
    if num:
        nt = f"{num}/{total}"; fnn = F(True, 30)
        d.text((x1 - 30 - d.textlength(nt, font=fnn), y0 + 34), nt, font=fnn, fill=BRAND_DK + (al,))
    for i, l in enumerate(subl):
        d.text((x0 + 40, y0 + 106 + i * 52), l, font=fs, fill=(70, 62, 58, al))
    img.alpha_composite(lay)

def ring(img, x, y, a, r=70):
    if a <= 0: return
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    rr = r * (1.25 - 0.25 * a)
    d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=BRAND + (int(230 * a),), width=6)
    img.alpha_composite(lay)

def label_chip(img, text, y=226, a=1.0, sub=None):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f = F(True, 52); tw = d.textlength(text, font=f); al = int(255 * a)
    d.rounded_rectangle([60, y, 60 + tw + 56, y + 84], radius=42, fill=(255, 253, 249, int(235 * a)))
    d.text((88, y + 8), text, font=f, fill=INK + (al,))
    d.rectangle([88, y + 72, 88 + tw, y + 77], fill=BRAND + (al,))
    if sub:
        d.text((66, y + 100), sub, font=F(True, 38), fill=INK + (int(220 * a),))
    img.alpha_composite(lay)

def palette_row(img, colors, names, a):
    if a <= 0: return
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    al = int(255 * a); n = len(colors); y0 = 1250 + int(30 * (1 - a))
    d.rounded_rectangle([60, y0, 940, y0 + 170], radius=30, fill=(255, 253, 249, int(240 * a)))
    d.text((92, y0 + 18), "오늘의 컬러 조합", font=F(True, 34), fill=BRAND_DK + (al,))
    w = (940 - 120) / n
    for i, (c, nm) in enumerate(zip(colors, names)):
        x = 92 + i * w
        d.rounded_rectangle([x, y0 + 72, x + w - 16, y0 + 112], radius=12, fill=rgb(c) + (al,), outline=INK + (al,), width=2)
        f = F(True, 28)
        while d.textlength(nm, font=f) > w - 16 and f.size > 20: f = F(True, f.size - 2)
        d.text((x, y0 + 120), nm, font=f, fill=INK + (al,))
    img.alpha_composite(lay)

def stamp(img, x, y, kind, label, a, scale=1.0):
    """⭕/△/❌ 도장 + 라벨 (비교 장면)"""
    if a <= 0: return
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    s = scale * (1.6 - 0.6 * ease(a)); al = int(255 * min(1, a * 1.5))
    col = {"o": BRAND, "x": (214, 64, 64), "tri": (226, 150, 40)}[kind]
    r = 64 * s
    if kind == "o":
        d.ellipse([x - r, y - r, x + r, y + r], outline=col + (al,), width=int(16 * s))
    elif kind == "x":
        d.line([(x - r, y - r), (x + r, y + r)], fill=col + (al,), width=int(18 * s)); d.line([(x - r, y + r), (x + r, y - r)], fill=col + (al,), width=int(18 * s))
    else:
        d.polygon([(x, y - r), (x + r, y + r * 0.8), (x - r, y + r * 0.8)], outline=col + (al,), width=int(14 * s))
    f = F(True, 42); tw = d.textlength(label, font=f)
    d.rounded_rectangle([x - tw / 2 - 24, y + r + 24, x + tw / 2 + 24, y + r + 90], radius=33, fill=col + (al,))
    d.text((x - tw / 2, y + r + 30), label, font=f, fill=(255, 255, 255, al))
    img.alpha_composite(lay)

def top_title(img, sc_, t, dark=True, band=True):
    """v4 상단: 브랜드 틸 배지 + 아주 큰 제목(한 단어씩 '쾅' 들어오는 키네틱) — 0프레임부터 첫 단어가 보임"""
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if band:
        bc = rgb(sc_.get("band", "#2a1d18"))
        d.rectangle([0, 0, W, sc_.get("band_h", 700 if "\n" in sc_.get("title", "") else 560)], fill=bc + (255,))
    fg = (255, 255, 255) if (band or sc_.get("light_text")) else INK
    y = 226
    if sc_.get("badge"):
        f = F(True, 42); tw = d.textlength(sc_["badge"], font=f)
        pulse = 1 + 0.05 * math.sin(t * 2 * math.pi * 2)
        d.rounded_rectangle([60, y, 60 + (tw + 56) * pulse, y + 72 * pulse], radius=36, fill=BRAND + (255,))
        d.text((88, y + 6), sc_["badge"], font=f, fill=(255, 255, 255, 255))
        if sc_.get("kicker"):
            d.text((60 + tw + 80, y + 10), sc_["kicker"], font=F(True, 40), fill=fg + (225,))
        y += 96
    words_lines = sc_.get("title", "").split("\n")
    ft = F(True, sc_.get("title_size", 112)); k = 0; tt = sc_.get("t_speed", 0.09)
    for ln in words_lines:
        x = 60
        for wd in ln.split(" "):
            st = k * tt; p = ease((t * sc_.get("dur", 3) - st) / 0.18)
            k += 1
            # v4: 0프레임부터 모든 단어가 보이고, 단어마다 차례로 '톡' 커졌다 작아짐(읽기 방해 없이 움직임)
            sz = 1 + 0.07 * (1 - p)
            fw = F(True, int(ft.size * sz))
            grow = d.textlength(wd, font=fw) - d.textlength(wd, font=ft)
            d.text((x, y - (fw.size - ft.size) / 2), wd, font=fw, fill=fg + (255,))
            x += d.textlength(wd + " ", font=ft) + 14
        y += int(ft.size * 1.16)
    if sc_.get("body"):
        pb = 1.0
        d.text((60, y + 6), sc_["body"], font=F(True, 46), fill=rgb(sc_.get("accent", "#7FE3E3")) + (int(255 * pb),))
    img.alpha_composite(lay)

def render_v4(sc_, t, looks, brand, idx, total, bg):
    typ = sc_["type"]; dur = sc_.get("dur", 3); T = t * dur
    if typ == "hook4":
        lk = looks[sc_.get("look", 0)]
        # 0~0.55초: 핵심 아이템 클로즈업에서 확 빠지며 전신 등장, 동시에 연필→채색 붓 쓸기
        fx, fy = lk.anchor(sc_.get("focus", "top"))
        zp = ease(T / 0.6); z = 1.8 + (1.0 - 1.8) * zp
        rp = min(1, 0.5 + T / 1.2)
        base = compose_reveal(lk, bg, rp, with_bg=False)
        top = sc_.get("fig_top", 735); scale = sc_.get("scale", 0.9)
        tmp = bg.copy(); place(tmp, base, scale + 1e-3, top=top)
        if z > 1.001:
            cx = fx; cy = fy + (top - FIG_TOP)
            cw, ch = W / z, H / z
            x0 = min(max(0, cx - cw / 2), W - cw); y0 = min(max(0, cy - ch / 2), H - ch)
            tmp = tmp.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR)
        img = tmp
        top_title(img, sc_, t)
        if sc_.get("tag"):
            f = F(True, 38); d = ImageDraw.Draw(img); tw = d.textlength(sc_["tag"], font=f)
            pa = ease((T - 0.6) / 0.25)
            if pa > 0:
                d.rounded_rectangle([60, 1330, 60 + tw + 48, 1400], radius=35, fill=(20, 20, 20))
                d.text((84, 1338), sc_["tag"], font=f, fill=(255, 255, 255))
        chrome(img, brand, (idx + t) / total, fg=(255, 255, 255))
        return img.convert("RGB")
    if typ == "compare":
        img = bg.copy()
        L = looks[sc_["left"]]; R = looks[sc_["right"]]
        sl = ease(0.45 + T / 0.6) if T < 0.33 else 1.0
        for lk, cx, sgn in ((L, 290, -1), (R, 790, 1)):
            fig = compose_reveal(lk, bg, 1.0, with_bg=False)
            place(img, fig, sc_.get("scale", 0.74), top=sc_.get("fig_top", 640), cx=cx + sgn * int(260 * (1 - sl)))
        top_title(img, sc_, t)
        for (kind, lab), cx, st in ((sc_["left_stamp"], 290, 0.45), (sc_["right_stamp"], 790, 0.75)):
            stamp(img, cx, 1180, kind, lab, ease((T - st) / 0.22))
        chrome(img, brand, (idx + t) / total, fg=(255, 255, 255))
        return img.convert("RGB")
    if typ == "reveal":
        lk = looks[sc_.get("look", 0)]
        items = sc_.get("items", [])
        t_rev, t_item, t_out = sc_.get("t_reveal", 1.1), sc_.get("t_item", 1.9), sc_.get("t_outro", 1.2)
        # 카메라 키프레임: 전신(1.0) → 아이템1 → 아이템2 … → 전신
        if T < t_rev:
            img = compose_reveal(lk, bg, ease(T / (t_rev * 0.85)))
            label_chip(img, sc_.get("label", ""), a=ease(T / 0.25), sub=sc_.get("label_sub"))
        else:
            k = int((T - t_rev) // t_item); tl = (T - t_rev) - k * t_item
            def cam_of(i):
                if i < 0 or i >= len(items): return (1.0, 540, 760 + 0)
                it = items[i]; x, y = lk.anchor(it["item"]) if "xy" not in it else tuple(it["xy"])
                return (it.get("zoom", 1.9), x, y)
            if k >= len(items):
                to = T - t_rev - len(items) * t_item
                prev = cam_of(len(items) - 1); cur = (1.0, 540, 900)
                p = ease(to / 0.45)
                z = prev[0] + (cur[0] - prev[0]) * p
                fx = prev[1] + (cur[1] - prev[1]) * p; fy = prev[2] + (cur[2] - prev[2]) * p
                sy = 760 + (900 - 760) * p
                img = camera(lk, bg, z, fx, fy, 540, sy) if z > 1.001 else lk.v4(bg)["full_co"].resize((W, H), Image.BILINEAR)
                label_chip(img, sc_.get("label", ""), a=1.0)
                if sc_.get("palette"):
                    palette_row(img, [c for c, _ in sc_["palette"]], [n for _, n in sc_["palette"]], ease((to - 0.3) / 0.3))
            else:
                prev = cam_of(k - 1) if k > 0 else (1.0, 540, 760)
                cur = cam_of(k); p = ease(tl / 0.45)
                z = prev[0] + (cur[0] - prev[0]) * p
                fx = prev[1] + (cur[1] - prev[1]) * p; fy = prev[2] + (cur[2] - prev[2]) * p
                if k == 0 and prev[0] == 1.0: fx, fy = 540 + (cur[1] - 540) * p, 760 + (cur[2] - 760) * p
                img = camera(lk, bg, max(1.0001, z), fx, fy, 540, 760)
                it = items[k]
                ring(img, 540, 760, ease((tl - 0.35) / 0.2), r=it.get("ring", 90))
                big_card(img, it["name"], it.get("sub", ""), it.get("swatch") or item_color(lk.spec, it["item"]),
                         ease((tl - 0.3) / 0.25), num=k + 1, total=len(items))
                label_chip(img, sc_.get("label", ""), a=1.0)
        chrome(img, brand, (idx + t) / total)
        return img.convert("RGB")
    raise ValueError(typ)

FIG_TOP = 272
def place(img, fig, scale, top=None, dy=0, cx=540):
    if abs(scale - 1) < 1e-3 and top is None:
        img.alpha_composite(fig, (0, dy)); return
    fw, fh = int(W * scale), int(H * scale)
    f = fig.resize((fw, fh), Image.BILINEAR)
    ox = int(cx - 540 * scale); oy = int(top - FIG_TOP * scale) + dy
    # 화면 밖으로 나가는 부분은 잘라서 붙이기
    sx, sy = max(0, -ox), max(0, -oy)
    f = f.crop((sx, sy, min(fw, W - ox), min(fh, H - oy)))
    img.alpha_composite(f, (max(0, ox), max(0, oy)))

def render_scene(sc_, t, looks, brand, idx, total, bg):
    typ = sc_.get("type", "text")
    if typ == "text":
        return MS.render_frame(sc_, t, brand, idx, total)
    if typ in ("hook4", "compare", "reveal"):
        return render_v4(sc_, t, looks, brand, idx, total, bg)
    lk = looks[sc_.get("look", 0)]
    img = bg.copy()
    if typ == "hook":
        # 0프레임부터 완성: 위쪽은 진한 컬러 붓 띠 + 흰 큰 글씨, 아래는 오늘의 코디 전부를 나란히
        band = rgb(sc_.get("band", "#4b2342"))
        if getattr(render_scene, "_band_key", None) != (band, id(bg)):
            rng = np.random.default_rng(5)
            xx = np.arange(W)[None, :]; yy = np.arange(H)[:, None]
            edge = 812 + 18 * np.sin(xx / 110.0) + noise(rng, W, 1, 45, 1, 16)[0][None, :] + noise(rng, W, 1, 7, 1, 5)[0][None, :]
            a = np.clip((edge - yy) / 6.0, 0, 1) * (1 - 0.06 * noise(rng, W, H, 2, 30, 1.0))
            lay = Image.new("RGBA", (W, H), band + (0,)); lay.putalpha(Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)))
            render_scene._band = lay; render_scene._band_key = (band, id(bg))
        img.alpha_composite(render_scene._band)
        n = min(len(looks), 3); sc_f = {1: 0.68, 2: 0.58, 3: 0.46}[n]
        pos = {1: [540], 2: [330, 760], 3: [210, 540, 870]}[n]
        bob = 6 * math.sin(t * math.pi * 2)
        for i in range(n):
            place(img, looks[i].lo, sc_f, top=850 + (bob if i % 2 else -bob), cx=pos[i])
        d = ImageDraw.Draw(img)
        if sc_.get("badge"):
            f = F(True, 44); tw = d.textlength(sc_["badge"], font=f)
            d.rounded_rectangle([90, 236, 90 + tw + 60, 314], radius=39, fill=rgb(sc_.get("badge_bg", "#ffd166")))
            d.text((120, 246), sc_["badge"], font=f, fill=rgb(sc_.get("badge_fg", "#2c2523")))
        y = 342
        if sc_.get("kicker"):
            d.text((90, y), sc_["kicker"], font=F(True, 44), fill=(255, 255, 255, 210)); y += 70
        for ln in sc_.get("title", "").split("\n"):
            d.text((90, y), ln, font=F(True, 112), fill=(255, 255, 255)); y += 130
        if sc_.get("body"):
            d.text((90, y + 2), sc_["body"], font=F(True, 46), fill=rgb(sc_.get("accent", "#ffd166")))
        for i in range(n):  # 룩 번호 꼬리표
            lab = sc_.get("tags", [])[i] if i < len(sc_.get("tags", [])) else f"LOOK {i + 1}"
            f = F(True, 32); tw = d.textlength(lab, font=f)
            x0 = pos[i] - tw / 2 - 22
            d.rounded_rectangle([x0, 1600, x0 + tw + 44, 1654], radius=27, fill=(255, 253, 249), outline=INK, width=2)
            d.text((x0 + 22, 1608), lab, font=f, fill=INK)
        chrome(img, brand, (idx + t) / total, fg=(255, 255, 255))
        return img.convert("RGB")
    elif typ == "look":
        place(img, lk.lo, 1.0, dy=int(-16 + 16 * ease(t)))
        d = ImageDraw.Draw(img)
        d.text((90, 222), sc_.get("label", ""), font=F(True, 40), fill=rgb(sc_.get("label_color", "#7a2d4a")))
        if sc_.get("title"): d.text((90, 272), sc_["title"], font=F(True, 58), fill=INK)
        cs = sc_.get("callouts", [])
        for i, c in enumerate(cs):
            st = 0.12 + i * (0.6 / max(1, len(cs))); al = ease((t - st) / 0.15)
            ax, ay = ANCHOR[c["item"]]
            side = c.get("side") or ("L" if ax < 540 else "R")
            callout(img, (ax, ay), side, c.get("y", ay), c["name"], c.get("sub", ""), c.get("swatch") or item_color(lk.spec, c["item"]), al)
    elif typ == "detail":
        ax, ay = sc_.get("focus_xy") or DETAIL[sc_["focus"]]
        z = 1 + (sc_.get("zoom", 2.6) - 1) * ease(t / 0.55)
        if lk._full is None:
            lk._full = bg.resize((W * S, H * S)); lk._full.alpha_composite(lk.hi)
        cw, ch = W * S / z, H * S / z
        cx = min(max(ax * S, cw / 2), W * S - cw / 2); cy = min(max(ay * S + 310 * S / z, ch / 2), H * S - ch / 2)
        img = lk._full.crop((int(cx - cw / 2), int(cy - ch / 2), int(cx + cw / 2), int(cy + ch / 2))).resize((W, H), Image.BILINEAR)
        a = ease((t - 0.35) / 0.25)
        if a > 0:
            lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            fs, fb = F(False, 34), F(True, 64)
            subl = MS.wrap(d, sc_.get("sub", ""), fs, 940 - 160); hgt = 200 + 48 * len(subl); y0 = 1400 - hgt
            d.rounded_rectangle([60, y0, 940, 1400], radius=28, fill=(255, 253, 249, int(235 * a)), outline=INK + (int(255 * a),), width=3)
            d.text((100, y0 + 30), sc_.get("kicker", "디테일 · 질감"), font=F(True, 34), fill=rgb(sc_.get("label_color", "#7a2d4a")) + (int(255 * a),))
            d.text((100, y0 + 76), sc_.get("label", ""), font=fb, fill=INK + (int(255 * a),))
            for i, l in enumerate(subl):
                d.text((100, y0 + 170 + i * 48), l, font=fs, fill=(80, 70, 66, int(255 * a)))
            img.alpha_composite(lay)
    chrome(img, brand, (idx + t) / total)
    return img.convert("RGB")

def main(spec_path, out):
    spec = json.load(open(spec_path, encoding="utf-8"))
    brand = spec.get("brand", "")
    looks = [Look(l, 3 + i) for i, l in enumerate(spec["looks"])]
    bg = paper_bg(spec.get("paper"), spec.get("wash"))
    scenes = spec["scenes"]
    tmp = tempfile.mkdtemp(); n = 0
    for i, s_ in enumerate(scenes):
        frames = int(s_.get("dur", 3) * FPS)
        for f in range(frames):
            render_scene(s_, f / frames, looks, brand, i, len(scenes), bg).save(f"{tmp}/{n:05d}.jpg", quality=93); n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/%05d.jpg",
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "20",
                    "-c:a", "aac", "-movflags", "+faststart", out], check=True)
    ct = 0.97 if scenes[0].get("type") in ("hook4", "compare") else 0.0
    render_scene(scenes[0], ct, looks, brand, 0, len(scenes), bg).save(os.path.splitext(out)[0] + "_cover.jpg", quality=92)
    print("done", out, n, "frames")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
