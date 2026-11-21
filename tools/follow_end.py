#!/usr/bin/env python3
"""'팔로우 이유' 엔딩 장면 붙이기 (2026-11-21 사장님 지시 · 트렌드 릴스·셀럽 스냅 해부 공통)

사용:
  python3 tools/follow_end.py <입력.mp4> <배경 사진.jpg> <출력.mp4> "<1줄>" "<2줄 또는 빈 문자열>" "<청록 강조 단어>" [길이초=2.6]

- 9:16 전체 화면, 배경 = 마지막 코디 사진을 흐리게(+어둡게) 깔기
- 큰 글자 최대 2줄(한 줄 14자 이내), 화면 가운데보다 살짝 위, 강조 단어 1개만 #00A8A8
- 아래 작은 글씨 @zzebi.st (하단 25% UI 영역 위)
- 입력에 소리가 있으면 소리를 엔딩 길이만큼 늘리고 끝에서 부드럽게 줄임. 소리가 없으면 영상만 이어 붙임
  (트렌드 팀: 소리 없는 X_silent.mp4 에 붙인 뒤 전체 길이로 배경음을 만들어 합치기)
- 미리보기만: 출력 경로를 .jpg 로 주면 엔딩 한 장면만 그림
"""
import sys, os, subprocess, tempfile, json
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
TEAL = (0, 168, 168)
FB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
FR = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

def font(p, s): return ImageFont.truetype(p, s, index=1)  # index 1 = KR

def bg_image(path):
    im = Image.open(path).convert("RGB")
    r = max(W / im.width, H / im.height)
    im = im.resize((int(im.width * r + .5), int(im.height * r + .5)), Image.LANCZOS)
    x0, y0 = (im.width - W) // 2, (im.height - H) // 2
    im = im.crop((x0, y0, x0 + W, y0 + H)).filter(ImageFilter.GaussianBlur(28))
    return Image.blend(im, Image.new("RGB", (W, H), (14, 16, 18)), 0.52)

def draw_line(d, y, s, f, accent):
    tw = d.textlength(s, font=f); x = (W - tw) / 2
    if accent and accent in s:
        a, b = s.split(accent, 1)
        for part, col in ((a, (255, 255, 255)), (accent, TEAL), (b, (255, 255, 255))):
            if part:
                d.text((x + 3, y + 3), part, font=f, fill=(0, 0, 0, 140), anchor="ls")
                d.text((x, y), part, font=f, fill=col + (255,), anchor="ls"); x += d.textlength(part, font=f)
    else:
        d.text((x + 3, y + 3), s, font=f, fill=(0, 0, 0, 140), anchor="ls")
        d.text((x, y), s, font=f, fill=(255, 255, 255, 255), anchor="ls")

def frame(bg, l1, l2, accent, a=1.0):
    lines = [l for l in (l1, l2) if l]
    for l in lines: assert len(l) <= 14, f"한 줄 14자 이내: {l} ({len(l)}자)"
    assert sum(accent in l for l in lines) <= 1 or not accent, "강조 단어는 1번만"
    img = bg.copy().convert("RGBA"); lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    size = 92
    while size > 60 and max(d.textlength(l, font=font(FB, size)) for l in lines) > W - 140: size -= 2
    f = font(FB, size); lh = int(size * 1.32)
    top = 860 - (lh * len(lines)) // 2  # 가운데(960)보다 살짝 위
    for i, l in enumerate(lines): draw_line(d, top + lh * (i + 1) - int(size * .25), l, f, accent)
    y_bar = top + lh * len(lines) + 34
    d.rectangle([W / 2 - 40, y_bar, W / 2 + 40, y_bar + 5], fill=TEAL + (255,))
    fh = font(FR, 42); s = "@zzebi.st"
    d.text((W / 2, y_bar + 80), s, font=fh, fill=(255, 255, 255, 215), anchor="mm")
    if a < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
    img.alpha_composite(lay); return img.convert("RGB")

def has_audio(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", p], capture_output=True, text=True)
    return bool(r.stdout.strip())

def main():
    src, bgp, out, l1, l2, accent = sys.argv[1:7]; dur = float(sys.argv[7]) if len(sys.argv) > 7 else 2.6
    assert 2.0 <= dur <= 3.0, "엔딩은 2~3초"
    bg = bg_image(bgp)
    if out.lower().endswith(".jpg"): frame(bg, l1, l2, accent).save(out, quality=92); print("preview", out); return
    tmp = tempfile.mkdtemp(); fps = 30; n = int(round(dur * fps))
    for i in range(n): frame(bg, l1, l2, accent, min(1.0, (i / fps) / 0.25)).save(f"{tmp}/{i:04d}.jpg", quality=93)
    end = f"{tmp}/end.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", f"{tmp}/%04d.jpg", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", end], check=True)
    D = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
    if has_audio(src):
        fc = (f"[0:v]scale={W}:{H},setsar=1,fps={fps}[a0];[1:v]setsar=1,fps={fps}[a1];[a0][a1]concat=n=2:v=1:a=0[v];"
              f"[0:a]apad=pad_dur={dur},afade=t=out:st={D + dur - 1.6:.2f}:d=1.6[a]")
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", end, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    else:
        fc = f"[0:v]scale={W}:{H},setsar=1,fps={fps}[a0];[1:v]setsar=1,fps={fps}[a1];[a0][a1]concat=n=2:v=1:a=0[v]"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-i", end, "-filter_complex", fc, "-map", "[v]",
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True); print("done", out, round(D + dur, 2), "s")

if __name__ == "__main__": main()
