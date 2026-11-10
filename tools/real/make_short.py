#!/usr/bin/env python3
"""숏츠 생성기 v2: scenes.json -> 1080x1920 MP4 (텍스트·그래픽 모션)
사용법: python3 make_short.py scenes.json out.mp4
scenes.json 형식:
{"brand": "@계정명", "scenes": [
  {"dur": 3.0, "bg": "#1b1b1b", "fg": "#ffffff", "kicker": "작은 윗줄", "title": "큰 제목\\n두 줄 가능",
   "body": "설명 문장", "swatches": ["#4a2340", "#5a3825"], "source": "출처 표기",
   "num": "01", "accent": "#7fb3ff"}
]}
v3(2026-10-26): ① "points": ["짧은 팁", ...] (2~3개)를 주면 본문 아래 빈 공간에 체크 카드(번호 원 + 한 줄 팁)가
  하나씩 옆에서 밀려 들어옴. ② 훅이 아닌 장면은 시작 0.25초 동안 accent 색 사선 와이프(약 0.25초)가 오른쪽으로 빠지며 전환.
v2(2026-10-25): 제목이 줄마다 아래에서 밀려 올라오는 마스크 리빌(키네틱 타이포),
  "num"을 주면 왼쪽 위에 매거진식 큰 번호(01·02…) + 얇은 강조선이 표시됨(accent 색).
"""
import json, sys, os, subprocess, tempfile, math
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
FONT_B = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
FONT_R = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
KR = 1  # .ttc index for KR

def font(path, size):
    return ImageFont.truetype(path, size, index=KR)

def hex2rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def ease(t):  # easeOutCubic
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

def wrap(draw, text, fnt, maxw):
    lines = []
    for para in text.split("\n"):
        cur = ""
        for ch in para:
            if draw.textlength(cur + ch, font=fnt) > maxw and cur:
                # 공백 기준으로 되돌리기
                if " " in cur:
                    head, tail = cur.rsplit(" ", 1); lines.append(head); cur = tail + ch
                else:
                    lines.append(cur); cur = ch
            else:
                cur += ch
        lines.append(cur.strip())
    return lines

def draw_text_block(img, lines, fnt, y, color, alpha, dy, lh):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for i, ln in enumerate(lines):
        d.text((90, y + i * lh + dy), ln, font=fnt, fill=color + (int(255 * alpha),))
    img.alpha_composite(layer)
    return y + len(lines) * lh

def draw_title_masked(img, lines, fnt, y, color, t0, t, lh, x=90):
    """키네틱 마스크 리빌: 각 줄이 자기 칸 안에서 아래→위로 밀려 올라옴 (줄마다 0.07씩 시차)"""
    for i, ln in enumerate(lines):
        p = ease((t - t0 - i * 0.07) / 0.3)
        if p <= 0: continue
        box_h = lh + 10
        tile = Image.new("RGBA", (W, box_h), (0, 0, 0, 0))
        ImageDraw.Draw(tile).text((x, int((1 - p) * box_h) - 8), ln, font=fnt, fill=color + (255,))
        img.alpha_composite(tile, (0, y + i * lh))
    return y + len(lines) * lh

def draw_numeral(img, sc, t, fg, bg):
    """매거진식 큰 번호: 왼쪽 위(안전영역 안), 얇은 강조선이 옆으로 자라남"""
    num = sc.get("num")
    if not num: return
    acc = hex2rgb(sc.get("accent", "#ffd166"))
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    p = ease(t / 0.4)
    fn = font(FONT_B, 260)
    col = tuple(int(a * 0.85 + b * 0.15) for a, b in zip(acc, bg))
    d.text((80, 300 - int(30 * (1 - p))), num, font=fn, fill=col + (int(255 * p),))
    tw = d.textlength(num, font=fn)
    x0 = int(80 + tw + 30); x1 = x0 + int((900 - x0) * ease((t - 0.1) / 0.5))
    if x1 > x0: d.rectangle([x0, 560, x1, 566], fill=acc + (230,))
    tot = sc.get("num_total")
    if tot:
        d.text((x0, 500), f"/ {tot}", font=font(FONT_B, 40), fill=fg + (int(170 * p),))
    img.alpha_composite(lay)

def draw_points(img, pts, y, fg, bg, acc, t):
    """v3 체크 카드: 본문 아래 빈 공간(최대 y 1420)에 팁 2~3개를 순서대로 밀어 넣음"""
    if not pts: return y
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    fn, fnum = font(FONT_B, 40), font(FONT_B, 34)
    rh = 74; top = y; card_h = 22 + rh * len(pts)
    p0 = ease((t - 0.3) / 0.3)
    if p0 > 0:
        tint = tuple(int(a * 0.10 + b * 0.90) for a, b in zip(fg, bg))
        d.rounded_rectangle([90, top, 930, top + card_h], radius=26, fill=tint + (int(255 * p0),))
        d.rectangle([90, top + 18, 98, top + card_h - 18], fill=acc + (int(255 * p0),))
    for i, txt in enumerate(pts):
        p = ease((t - 0.38 - i * 0.1) / 0.3)
        if p <= 0: continue
        x = 130 + int(60 * (1 - p)); cy = top + 12 + rh * i + rh // 2; a = int(255 * p)
        d.ellipse([x, cy - 26, x + 52, cy + 26], fill=acc + (a,))
        num = str(i + 1); tw = d.textlength(num, font=fnum)
        d.text((x + 26 - tw / 2, cy - 24), num, font=fnum, fill=bg + (a,))
        d.text((x + 76, cy - 28), txt, font=fn, fill=fg + (a,))
    img.alpha_composite(lay)
    return top + card_h

def draw_wipe(img, t, acc):
    """v3 장면 전환: accent 색 사선 패널이 장면 앞 8.5%(약 0.25초) 동안 오른쪽으로 빠져나감"""
    p = ease(t / 0.085)
    if p >= 1: return
    x0 = int(-260 + (W + 520) * p)
    d = ImageDraw.Draw(img)
    d.polygon([(x0 + 260, 0), (W + 400, 0), (W + 400, H), (x0, H)], fill=acc)

def render_hook(sc, t, brand, idx, total):
    """훅(첫 장면): 0프레임부터 완성된 화면. 트렌드 컬러 띠가 화면을 꽉 채우고,
    큰 문구 + 배지로 '무슨 영상인지' 즉시 보이게 함. 썸네일/커버로도 그대로 쓰임."""
    fg = hex2rgb(sc.get("fg", "#ffffff"))
    stripes = [hex2rgb(c) for c in sc["stripes"]]
    img = Image.new("RGBA", (W, H), stripes[0] + (255,))
    d = ImageDraw.Draw(img)
    n = len(stripes); bw = W / n
    drift = int(60 * math.sin(t * math.pi))  # 띠가 천천히 흔들리는 움직임 (0프레임에도 꽉 찬 상태)
    for i, c in enumerate(stripes):
        x0 = int(i * bw) - 60 + drift
        d.polygon([(x0, 0), (x0 + bw + 120, 0), (x0 + bw, H), (x0 - 120, H)], fill=c)
    # 가독성용 어두운 패널
    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle([60, 560, W - 60, 1400], radius=36, fill=(12, 8, 12, 215))
    img.alpha_composite(panel)
    d = ImageDraw.Draw(img)
    fb_badge = font(FONT_B, 46)
    if sc.get("badge"):  # 살짝 커졌다 작아지는 배지
        s = 1 + 0.06 * math.sin(t * math.pi * 4)
        tw = d.textlength(sc["badge"], font=fb_badge)
        bw2, bh2 = (tw + 64) * s, 84 * s
        bx, by = 90, 470 - (bh2 - 84) / 2
        d.rounded_rectangle([bx, by, bx + bw2, by + bh2], radius=42, fill=hex2rgb(sc.get("badge_bg", "#f4efe8")))
        d.text((bx + 32 * s, by + 10 * s), sc["badge"], font=fb_badge, fill=hex2rgb(sc.get("badge_fg", "#141414")))
    y = 640
    fk, ft, fb = font(FONT_B, 46), font(FONT_B, 124), font(FONT_B, 54)
    if sc.get("kicker"):
        y = draw_text_block(img, wrap(d, sc["kicker"], fk, W - 220), fk, y, fg, 0.8, 0, 66) + 26
    if sc.get("title"):
        y = draw_text_block(img, wrap(d, sc["title"], ft, W - 220), ft, y, fg, 1.0, 0, 148) + 30
    if sc.get("body"):
        draw_text_block(img, wrap(d, sc["body"], fb, W - 240), fb, y, hex2rgb(sc.get("accent", "#ffd166")), 1.0, 0, 76)
    d = ImageDraw.Draw(img)
    prog = (idx + t) / total
    d.rectangle([90, 150, 90 + int((W - 180) * prog), 158], fill=fg)
    d.text((90, 180), brand, font=font(FONT_R, 30), fill=fg)
    return img.convert("RGB")

def render_frame(sc, t, brand, idx, total):
    if sc.get("stripes"):
        return render_hook(sc, t, brand, idx, total)
    bg, fg = hex2rgb(sc.get("bg", "#111111")), hex2rgb(sc.get("fg", "#ffffff"))
    img = Image.new("RGBA", (W, H), bg + (255,))
    d = ImageDraw.Draw(img)
    sw = sc.get("swatches", [])
    # 컬러 스와치: 오른쪽에서 밀려 들어오는 큰 블록
    if sw:
        n = len(sw); bh = 440 // n if n else 0
        for i, c in enumerate(sw):
            p = ease((t - 0.1 - i * 0.12) / 0.5)
            x0 = int(W - (W - 90) * p)
            d.rectangle([x0, 330 + i * bh, W, 330 + (i + 1) * bh - 14], fill=hex2rgb(c))
    y = 860 if sw else (680 if sc.get("num") else 700)
    if sc.get("points") and not sw:  # v3: 체크 카드가 있으면 블록 전체를 위로 올려 출처까지 하단 25% 위에서 끝나게
        y = 610 if sc.get("num") else 560
    draw_numeral(img, sc, t, fg, bg)
    a1, o1 = ease(t / 0.35), int(40 * (1 - ease(t / 0.35)))
    a2, o2 = ease((t - 0.15) / 0.35), int(40 * (1 - ease((t - 0.15) / 0.35)))
    a3, o3 = ease((t - 0.35) / 0.35), int(40 * (1 - ease((t - 0.35) / 0.35)))
    fk, ft, fb, fs = font(FONT_B, 44), font(FONT_B, 108), font(FONT_R, 50), font(FONT_R, 30)
    if sc.get("kicker"):
        y = draw_text_block(img, wrap(d, sc["kicker"], fk, W - 180), fk, y, fg, a1 * 0.75, o1, 64) + 24
    if sc.get("title"):
        y = draw_title_masked(img, wrap(d, sc["title"], ft, W - 180), ft, y, fg, 0.12, t, 132) + 30
    if sc.get("body"):
        y = draw_text_block(img, wrap(d, sc["body"], fb, W - 240), fb, y, fg, a3 * 0.9, o3, 74)
    acc = hex2rgb(sc.get("accent", "#ffd166"))
    if sc.get("points"):
        y = draw_points(img, sc["points"], y + 28, fg, bg, acc, t)
    d = ImageDraw.Draw(img)
    src_y = y + 36  # 본문 바로 아래 (스와치 장면은 하단 UI 영역 위에서 끝나도록 레이아웃 조정)
    # 상단 진행바 + 브랜드, 하단 출처
    prog = (idx + t) / total
    d.rectangle([90, 150, 90 + int((W - 180) * prog), 158], fill=fg)
    d.text((90, 180), brand, font=fs, fill=fg)
    if sc.get("source"):
        draw_text_block(img, ["출처: " + sc["source"]], fs, src_y, tuple(int(c * 0.6 + b * 0.4) for c, b in zip(fg, bg)), a3, o3, 40)
    if not sc.get("no_wipe"):
        draw_wipe(img, t, acc)
    return img.convert("RGB")

def main(spec_path, out):
    spec = json.load(open(spec_path, encoding="utf-8"))
    scenes, brand = spec["scenes"], spec.get("brand", "")
    tmp = tempfile.mkdtemp()
    n = 0
    for i, sc in enumerate(scenes):
        frames = int(sc.get("dur", 3) * FPS)
        for f in range(frames):
            render_frame(sc, f / frames, brand, i, len(scenes)).save(f"{tmp}/{n:05d}.png"); n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/%05d.png",
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-profile:v", "high", "-crf", "20",
                    "-c:a", "aac", "-movflags", "+faststart", out], check=True)
    # 썸네일(커버)
    render_frame(scenes[0], 1.0, brand, 0, len(scenes)).save(os.path.splitext(out)[0] + "_cover.jpg", quality=92)
    print("done", out, n, "frames")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
