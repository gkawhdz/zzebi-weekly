# 2026-11-07 셀럽 스냅 스토리: ① 플랫레이 장바구니 체크리스트 틱 모션(#34) ② 질감 2x2 매크로 그리드(#35)
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
W, H = 1080, 1920
TEAL = (0, 168, 168)
WK = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/work"
def F(kind, sz):
    p = {"SansB": "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", "Sans": "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc",
         "Serif": "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc", "Black": "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"}[kind]
    return ImageFont.truetype(p, sz, index=1)
def ease(t): t = max(0, min(1, t)); return t * t * (3 - 2 * t)

# ---------- 스토리 1: 장바구니 체크리스트 ----------
def story1():
    src = Image.open(f"{WK}/img34.jpg").convert("RGB")
    bg = (214, 215, 216)
    flat = src.crop((10, 320, 505, 1345))           # 왼쪽 플랫레이
    sc = 0.9; fw, fh = int(flat.width * sc), int(flat.height * sc)
    flat = flat.resize((fw, fh), Image.LANCZOS)
    X0, Y0 = 34, 505
    # 행: (라벨, 원본 y, 릴스에 없음 여부)
    rows = [("선글라스", 365, True), ("스카이블루 바람막이", 560, False), ("블랙+흰 티 레이어드", 720, False),
            ("그레이 플리츠 미니", 950, False), ("블랙 숄더백", 1130, True), ("흰 양말·흰 스니커즈", 1265, False)]
    ry = [540 + i * 152 for i in range(6)]
    fT = F("SansB", 46); fH = F("Serif", 72); fS = F("SansB", 44); fF = F("Sans", 30); fTag = F("SansB", 30)
    os.makedirs(f"{WK}/story/s1", exist_ok=True)
    N = 210
    for k in range(N):
        t = k / 30
        im = Image.new("RGB", (W, H), bg)
        z = 1 + 0.03 * (t / 7)
        fz = flat.resize((int(fw * z), int(fh * z)), Image.LANCZOS)
        im.paste(fz, (X0 - (fz.width - fw) // 2, Y0 - (fz.height - fh) // 2))
        d = ImageDraw.Draw(im, "RGBA")
        d.rectangle([0, 0, W, 492], fill=bg)  # 위 여백 정리
        d.text((60, 262), "릴스엔 4개,", font=fH, fill=(25, 25, 25))
        d.text((60, 352), "장바구니엔 6개", font=fH, fill=(25, 25, 25))
        hl = ease((t - 4.4) / 0.5)
        if hl > 0:
            w6 = d.textlength("장바구니엔 6개", font=fH)
            d.rectangle([60, 456, 60 + w6 * hl, 464], fill=TEAL)
        for i, (lab, oy, extra) in enumerate(rows):
            a = ease((t - 0.15 * i) / 0.5)
            if a <= 0: continue
            y = ry[i]; al = int(255 * a)
            ix = X0 + fw - 30; iy = Y0 + int((oy - 320) * sc)
            d.line([(ix, iy), (486, y + 26)], fill=(0, 168, 168, int(200 * a)), width=3)
            d.ellipse([ix - 7, iy - 7, ix + 7, iy + 7], fill=(0, 168, 168, al))
            d.rounded_rectangle([486, y - 6, 1046, y + 102 if extra else y + 62], 18, fill=(255, 255, 255, int(225 * a)))
            on = t >= 1.0 + 0.55 * i
            d.rounded_rectangle([500, y + 4, 548, y + 52], 10, outline=TEAL + (al,), width=4, fill=(TEAL + (al,)) if on else None)
            if on:
                d.line([(510, y + 28), (521, y + 40), (540, y + 14)], fill=(255, 255, 255, al), width=6)
            d.text((562, y + 2), lab, font=fT, fill=(25, 25, 25, al))
            if extra:
                d.text((562, y + 56), "릴스에 없는 템", font=fTag, fill=TEAL + (al,))
        c = ease((t - 4.8) / 0.5)
        if c > 0:
            txt = "4개 포인트 전부는 릴스에서 ↑"
            tw = d.textlength(txt, font=fS)
            d.rounded_rectangle([540 - tw / 2 - 40, 1440, 540 + tw / 2 + 40, 1530], 45, fill=TEAL + (int(255 * c),))
            d.text((540, 1485), txt, font=fS, fill=(255, 255, 255, int(255 * c)), anchor="mm")
        d.text((60, 1550), "셀럽 스냅 해부 #34 · @zzebi.st", font=fF, fill=(40, 40, 40))
        d.text((W - 60, 1550), "AI 재현 이미지", font=fF, fill=(70, 70, 70), anchor="ra")
        im.save(f"{WK}/story/s1/{k:04d}.jpg", quality=92)
        if k == 180: im.save(f"{WK}/story/story_34_frame.jpg", quality=92)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-i", f"{WK}/story/s1/%04d.jpg",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", f"{WK}/story/story_34.mp4"], check=True)

# ---------- 스토리 2: 질감 2x2 매크로 그리드 ----------
def story2():
    src = Image.open(f"{WK}/img35.jpg").convert("RGB")
    bg = (38, 33, 30)
    im = Image.new("RGB", (W, H), bg); d = ImageDraw.Draw(im, "RGBA")
    fH = F("Serif", 80); fL = F("Black", 58); fS = F("SansB", 44); fF = F("Sans", 30); fN = F("SansB", 34)
    d.text((60, 268), "같은 베이지인데", font=fH, fill=(245, 240, 232))
    d.text((60, 365), "질감은 4개", font=fH, fill=(245, 240, 232))
    d.rectangle([60, 470, 60 + d.textlength("질감은 4개", font=fH), 478], fill=TEAL)
    tiles = [((130, 450, 370, 650), "뽀글", "재킷"), ((110, 720, 410, 870), "매끈", "이너"),
             ((115, 1000, 395, 1205), "광택", "가방"), ((640, 1040, 880, 1260), "보송", "바지")]
    tw, th, gap = 500, 440, 20; x0, y0 = 30, 510
    for i, (box, lab, part) in enumerate(tiles):
        c = src.crop(box)
        r = max(tw / c.width, th / c.height)
        c = c.resize((int(c.width * r) + 1, int(c.height * r) + 1), Image.LANCZOS)
        c = c.crop(((c.width - tw) // 2, (c.height - th) // 2, (c.width - tw) // 2 + tw, (c.height - th) // 2 + th))
        c = c.filter(ImageFilter.UnsharpMask(2, 80, 2))
        x = x0 + (i % 2) * (tw + gap); y = y0 + (i // 2) * (th + gap)
        m = Image.new("L", (tw, th), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, tw, th], 26, fill=255)
        im.paste(c, (x, y), m)
        d.rounded_rectangle([x + 22, y + th - 104, x + 22 + d.textlength(lab, font=fL) + 44, y + th - 22], 20, fill=(15, 15, 15, 190))
        d.text((x + 44, y + th - 63), lab, font=fL, fill=(255, 255, 255), anchor="lm")
        d.text((x + tw - 24, y + 30), f"0{[1,2,3,4][i]} {part}", font=fN, fill=(255, 255, 255), anchor="ra",
               stroke_width=3, stroke_fill=(0, 0, 0))
    d.text((60, 1418), "4개 중 '반짝' 담당은 딱 하나", font=fS, fill=(245, 240, 232))
    txt = "나머지 포인트는 오늘 릴스에서 ↑"
    w_ = d.textlength(txt, font=fS)
    d.rounded_rectangle([60, 1482, 60 + w_ + 70, 1566], 42, fill=TEAL)
    d.text((95, 1524), txt, font=fS, fill=(255, 255, 255), anchor="lm")
    d.text((W - 60, 1500), "AI 재현 이미지", font=fF, fill=(200, 195, 188), anchor="ra")
    d.text((W - 60, 1540), "#35 · @zzebi.st", font=fF, fill=(200, 195, 188), anchor="ra")
    im.save(f"{WK}/story/story_35.jpg", quality=93)

story1(); story2(); print("ok")
