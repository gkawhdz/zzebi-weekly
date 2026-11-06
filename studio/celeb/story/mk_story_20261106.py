import os, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1080, 1920
TEAL = (0, 168, 168)
def F(kind, sz):
    p = {"SansB": "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", "Sans": "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc",
         "Serif": "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc", "Black": "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"}[kind]
    return ImageFont.truetype(p, sz, index=1)

def shadow_text(d, xy, t, f, fill=(255, 255, 255), anchor="la"):
    x, y = xy
    for dx, dy in ((2, 3), (0, 3), (3, 0)):
        d.text((x + dx, y + dy), t, font=f, fill=(0, 0, 0, 150), anchor=anchor)
    d.text((x, y), t, font=f, fill=fill, anchor=anchor)

def footer(d, ep):
    f = F("Sans", 30)
    d.text((70, 1560), f"셀럽 스냅 해부 #{ep}  ·  @zzebi.st", font=f, fill=(255, 255, 255, 235))
    d.text((W - 70, 1560), "AI 재현 이미지", font=F("Sans", 26), fill=(255, 255, 255, 200), anchor="ra")

def button(d, y, t):
    f = F("SansB", 44)
    tw = d.textlength(t, font=f)
    x0 = (W - tw) / 2 - 44
    d.rounded_rectangle((x0, y, x0 + tw + 88, y + 96), radius=48, fill=TEAL)
    d.text((W / 2, y + 48), t, font=f, fill="white", anchor="mm")

def ease(t):
    t = max(0, min(1, t)); return t * t * (3 - 2 * t)

# ---------- Story 1 (#32): macro zoom-out reveal, 7s ----------
def story1(out):
    src = Image.open("img32.jpg").convert("RGB")
    fps, dur = 30, 7.0
    # start: macro on mock-neck collar (right half), end: full split image (w=864,h=1536)
    s = (720, 230, 340)   # cx, cy, width
    e = (594, 768, 864)
    os.makedirs("s1f", exist_ok=True)
    n = int(fps * dur)
    for i in range(n):
        t = i / fps
        k = ease((t - 1.8) / 3.0)
        cx = s[0] + (e[0] - s[0]) * k; cy = s[1] + (e[1] - s[1]) * k
        w = s[2] * (e[2] / s[2]) ** k; h = w * 16 / 9
        x0 = min(max(cx - w / 2, 0), 1024 - w); y0 = min(max(cy - h / 2, 0), 1536 - h)
        fr = src.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.LANCZOS)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        # top & bottom gradient for legibility
        for y in range(0, 760):
            a = int(170 * (1 - y / 760) ** 1.4); d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
        for y in range(1100, H):
            a = int(200 * ((y - 1100) / (H - 1100)) ** 1.2); d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
        # phase texts
        chip_f = F("SansB", 34)
        if t < 2.6:
            d.rounded_rectangle((70, 290, 70 + d.textlength("확대", font=chip_f) + 48, 352), radius=31, fill=TEAL)
            d.text((94, 321), "확대", font=chip_f, fill="white", anchor="lm")
            shadow_text(d, (70, 385), "재킷 깃 아래", F("Black", 92))
            shadow_text(d, (70, 495), "흰 줄 하나의 힘", F("Black", 92))
            d.rectangle((70, 615, 70 + 300, 623), fill=TEAL)
        else:
            a2 = ease((t - 2.6) / 0.5)
            d.rounded_rectangle((70, 290, 70 + d.textlength("전체", font=chip_f) + 48, 352), radius=31, fill=TEAL)
            d.text((94, 321), "전체", font=chip_f, fill="white", anchor="lm")
            shadow_text(d, (70, 385), "청청이 덜 무거워", F("Black", 88))
            shadow_text(d, (70, 490), "보이는 이유예요", F("Black", 88))
        if t >= 4.6:
            a3 = ease((t - 4.6) / 0.5)
            yoff = int(40 * (1 - a3))
            card = (60, 1170 + yoff, W - 60, 1420 + yoff)
            d.rounded_rectangle(card, radius=28, fill=(18, 22, 30, int(215 * a3)), outline=(0, 168, 168, int(255 * a3)), width=3)
            d.text((100, 1200 + yoff), "에디터 대체 팁", font=F("SansB", 34), fill=(0, 200, 200, int(255 * a3)))
            d.text((100, 1255 + yoff), "모크넥이 없다면?", font=F("SansB", 50), fill=(255, 255, 255, int(255 * a3)))
            d.text((100, 1330 + yoff), "흰 크루넥 니트·헨리넥 티도 OK", font=F("Sans", 46), fill=(235, 235, 235, int(255 * a3)))
        if t >= 5.4:
            button(d, 1445, "4개 포인트 전부는 오늘 릴스에서 ↑")
        footer(d, "32")
        fr = Image.alpha_composite(fr.convert("RGBA"), ov).convert("RGB")
        fr.save(f"s1f/{i:04d}.jpg", quality=92)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", str(fps), "-i", "s1f/%04d.jpg", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-movflags", "+faststart", out], check=True)
    Image.open(f"s1f/{n-10:04d}.jpg").save("story_32_preview.jpg")

# ---------- Story 2 (#33): ruler hem guide, static ----------
def story2(out):
    src = Image.open("img33.jpg").convert("RGB")
    # right-half lower leg/shoe region full-bleed
    x0, w = 560, 464; h = int(w * 16 / 9); y0 = 1536 - h
    fr = src.crop((x0, y0, x0 + w, y0 + h)).resize((W, H), Image.LANCZOS).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for x in range(0, 700):
        a = int(185 * (1 - x / 700) ** 1.1); d.line([(x, 0), (x, H)], fill=(0, 0, 0, a))
    for y in range(0, 640):
        a = int(150 * (1 - y / 640)); d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    chip_f = F("SansB", 34)
    d.rounded_rectangle((70, 290, 70 + d.textlength("밑단 자", font=chip_f) + 48, 352), radius=31, fill=TEAL)
    d.text((94, 321), "밑단 자", font=chip_f, fill="white", anchor="lm")
    d.text((70, 380), "밑단, 어디서", font=F("Serif", 84), fill="white")
    d.text((70, 485), "끊을까?", font=F("Serif", 84), fill="white")
    # ruler
    rx, ry0, ry1 = 110, 650, 1380
    d.rectangle((rx, ry0, rx + 10, ry1), fill=TEAL)
    for j, yy in enumerate(range(ry0, ry1 + 1, 30)):
        L = 46 if j % 4 == 0 else 24
        d.line([(rx + 10, yy), (rx + 10 + L, yy)], fill=(0, 168, 168, 230), width=4)
    marks = [(920, "1", "발목 위 9부", "양말이 보여요 → 바지 색 양말로", False),
             (1150, "2", "발목에서 끊김", "운동화와 가장 쉬운 기본", True),
             (1340, "3", "신발을 덮음", "운동화가 묻혀 보여요", False)]
    for yy, num, title, sub, ok in marks:
        d.ellipse((rx - 25, yy - 30, rx + 35, yy + 30), fill=TEAL if ok else (255, 255, 255), outline=TEAL, width=4)
        d.text((rx + 5, yy), num, font=F("SansB", 36), fill="white" if ok else TEAL, anchor="mm")
        bx = 200
        if True:
            tw = max(d.textlength(title, font=F("SansB", 54)), d.textlength(sub, font=F("Sans", 44)))
            d.rounded_rectangle((bx - 24, yy - 66, bx + tw + 30, yy + 82), radius=22, fill=(0, 0, 0, 120), outline=TEAL if ok else None, width=4)
        d.text((bx, yy - 52), title, font=F("SansB", 54), fill="white")
        d.text((bx, yy + 14), sub, font=F("Sans", 44), fill=(230, 230, 230))
    button(d, 1450, "나머지 포인트는 오늘 릴스에서 ↑")
    footer(d, "33")
    Image.alpha_composite(fr, ov).convert("RGB").save(out, quality=92)

if __name__ == "__main__":
    story2("20261106_story_33.jpg")
    story1("20261106_story_32.mp4")
