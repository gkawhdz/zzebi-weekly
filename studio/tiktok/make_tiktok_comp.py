"""틱톡용 1분 이상 몰아보기 영상 만들기 (zzebi.st)
사용: python3 make_tiktok_comp.py spec.json out.mp4
spec 예:
{
  "kicker": "셀럽 스냅 해부 몰아보기",
  "title": ["셀럽 3명", "스트릿룩 해부"],
  "sub": "끝까지 보고 투표해 주세요 👇",
  "segments": [{"file": "c08.mp4", "label": "BELLA HADID", "sub": "그레이 레깅스 공항룩", "thumb_t": 1.0}],
  "vote": true,                      # 마지막에 '어떤 게 제일 좋아요?' 투표 카드
  "vote_q": "제일 따라 입고 싶은 룩은?",
  "recap_t": 13.0,                   # (선택) 각 영상에서 요약 화면 시각 → 요약 장면 추가
  "seed": 7, "min_total": 62
}
- 원본 오디오는 쓰지 않고, 전체에 이어지는 오리지널 배경음(chill_bgm.py)을 깝니다.
- 카드 디자인: 오프화이트 #f6f1ea + 진한 글자 #221e1e + 브랜드 틸 #00A8A8, 큰 글씨(본문 44px 이상).
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
BG, INK, TEAL, DARK = "#f6f1ea", "#221e1e", "#00A8A8", "#1c1a1a"
HERE = os.path.dirname(os.path.abspath(__file__))
FB = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
FBD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
KR = 1  # ttc 안의 한국어 서체 번호


def font(sz, black=True):
    p = FB if black and os.path.exists(FB) else FBD
    try:
        return ImageFont.truetype(p, sz, index=KR)
    except Exception:
        return ImageFont.truetype(p, sz)


def sh(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode().strip())


def frame(f, t, out):
    sh(["ffmpeg", "-y", "-ss", str(t), "-i", f, "-frames:v", "1", out])
    return Image.open(out).convert("RGB")


def rounded_thumb(im, w, h, r=28):
    im = im.copy(); s = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * s + 1), int(im.height * s + 1)))
    l, t = (im.width - w) // 2, (im.height - h) // 2
    im = im.crop((l, t, l + w, t + h))
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w, h), r, fill=255)
    return im, m


def text_c(d, y, s, f, fill, x=None):
    bw = d.textlength(s, font=f)
    d.text(((W - bw) / 2 if x is None else x, y), s, font=f, fill=fill)


def pill(d, x, y, s, f, bg, fg, pad=(28, 14)):
    bw = d.textlength(s, font=f); hh = f.size + pad[1] * 2
    d.rounded_rectangle((x, y, x + bw + pad[0] * 2, y + hh), hh // 2, fill=bg)
    d.text((x + pad[0], y + pad[1] - f.size * 0.12), s, font=f, fill=fg)
    return x + bw + pad[0] * 2


def card_intro(spec, thumbs, out):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    d.rectangle((90, 150, 330, 158), fill=INK)
    d.text((90, 180), "zzebi.st · 1분 몰아보기", font=font(40, False), fill=INK)
    pill(d, 90, 300, spec.get("kicker", "몰아보기"), font(46), TEAL, "white")
    y = 410
    for ln in spec["title"]:
        d.text((86, y), ln, font=font(132), fill=INK); y += 162
    d.text((90, y + 20), spec.get("sub", ""), font=font(52, False), fill=TEAL)
    n = len(thumbs); gap = 24; tw = (W - 180 - gap * (n - 1)) // n; th = int(tw * 16 / 9)
    th = min(th, 1820 - (y + 140)); ty = y + 130
    for i, t in enumerate(thumbs):
        x = 90 + i * (tw + gap); tm, m = rounded_thumb(t, tw, th); im.paste(tm, (x, ty), m)
        pill(d, x + 18, ty + 18, f"{i + 1:02d}", font(44), INK, "white", (20, 8))
    im.save(out, quality=95)


def card_chapter(i, n, seg, out):
    im = Image.new("RGB", (W, H), DARK); d = ImageDraw.Draw(im)
    text_c(d, 700, f"{i:02d} / {n:02d}", font(64), TEAL)
    f = font(120 if len(seg["label"]) <= 12 else 92)
    text_c(d, 800, seg["label"], f, "white")
    if seg.get("sub"):
        text_c(d, 800 + f.size + 50, seg["sub"], font(56, False), "#e8e2da")
    d.rectangle((W / 2 - 60, 1180, W / 2 + 60, 1188), fill=TEAL)
    im.save(out, quality=95)


def card_vote(spec, thumbs, out):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    pill(d, 90, 170, "댓글 투표", font(46), TEAL, "white")
    y = 270
    for ln in [spec.get("vote_q", "제일 따라 입고 싶은 룩은?")]:
        d.text((86, y), ln, font=font(88), fill=INK); y += 120
    n = len(thumbs); gap = 24; tw = (W - 180 - gap * (n - 1)) // n; th = int(tw * 16 / 9); ty = y + 60
    for i, t in enumerate(thumbs):
        x = 90 + i * (tw + gap); tm, m = rounded_thumb(t, tw, th); im.paste(tm, (x, ty), m)
        d.ellipse((x + tw / 2 - 56, ty + th - 70, x + tw / 2 + 56, ty + th + 42), fill=TEAL)
        text_c(d, ty + th - 58, str(i + 1), font(80), "white", x + tw / 2 - d.textlength(str(i + 1), font=font(80)) / 2)
    text_c(d, ty + th + 110, "번호로 댓글 남겨주세요 ↓", font(60, False), INK)
    im.save(out, quality=95)


def card_outro(out):
    im = Image.new("RGB", (W, H), TEAL); d = ImageDraw.Draw(im)
    text_c(d, 760, "저장 & 팔로우", font(130), "white")
    text_c(d, 940, "매일 1분 셀럽룩 · 날씨 코디", font(58, False), "white")
    text_c(d, 1060, "@zzebi.st", font(76), "white")
    im.save(out, quality=95)


def main(spec_path, out):
    spec = json.load(open(spec_path)); base = os.path.dirname(os.path.abspath(spec_path))
    tmp = tempfile.mkdtemp(); segs = spec["segments"]
    for s in segs:
        s["file"] = s["file"] if os.path.isabs(s["file"]) else os.path.join(base, s["file"])
    thumbs = [frame(s["file"], s.get("thumb_t", 1.0), f"{tmp}/th{i}.jpg") for i, s in enumerate(segs)]
    parts = []  # (kind, path, seconds)
    card_intro(spec, thumbs, f"{tmp}/intro.jpg"); parts.append(("img", f"{tmp}/intro.jpg", spec.get("intro_s", 2.6)))
    for i, s in enumerate(segs, 1):
        card_chapter(i, len(segs), s, f"{tmp}/ch{i}.jpg"); parts.append(("img", f"{tmp}/ch{i}.jpg", 1.3))
        parts.append(("vid", s["file"], dur(s["file"])))
    if spec.get("recap_t") is not None:
        for i, s in enumerate(segs):
            r = frame(s["file"], spec["recap_t"], f"{tmp}/rc{i}.jpg").resize((W, H)); r.save(f"{tmp}/rc{i}.jpg")
            parts.append(("img", f"{tmp}/rc{i}.jpg", spec.get("recap_s", 3.0)))
    if spec.get("vote"):
        card_vote(spec, thumbs, f"{tmp}/vote.jpg"); parts.append(("img", f"{tmp}/vote.jpg", 4.0))
    total = sum(p[2] for p in parts) + 3.0
    outro_s = max(3.0, spec.get("min_total", 62) - (total - 3.0))
    card_outro(f"{tmp}/outro.jpg"); parts.append(("img", f"{tmp}/outro.jpg", outro_s))
    total = sum(p[2] for p in parts)

    inputs, fl = [], []
    for i, (k, p, s) in enumerate(parts):
        if k == "img":
            inputs += ["-loop", "1", "-framerate", str(FPS), "-t", f"{s:.3f}", "-i", p]
            # 카드는 아주 천천히 확대돼서 정지 화면처럼 보이지 않게
            fl.append(f"[{i}:v]scale={W*1.04:.0f}:{H*1.04:.0f},zoompan=z='min(1+0.0006*on,1.04)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={W}x{H}:fps={FPS},setsar=1,format=yuv420p[v{i}]")
        else:
            inputs += ["-i", p]
            fl.append(f"[{i}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps={FPS},setsar=1,format=yuv420p[v{i}]")
    fl.append("".join(f"[v{i}]" for i in range(len(parts))) + f"concat=n={len(parts)}:v=1:a=0[v]")
    silent = f"{tmp}/silent.mp4"
    subprocess.run(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(fl), "-map", "[v]", "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", "-r", str(FPS), silent],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    bgm = f"{tmp}/bgm.wav"
    sh(["python3", os.path.join(HERE, "chill_bgm.py"), bgm, f"{total + 0.5:.2f}", str(spec.get("seed", 1))])
    sh(["ffmpeg", "-y", "-i", silent, "-i", bgm, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
        "-af", f"afade=t=out:st={total - 1.5:.2f}:d=1.5,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100,alimiter=limit=0.6:level=false,volume=0.8",
        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out])
    sh(["ffmpeg", "-y", "-ss", "0.5", "-i", out, "-frames:v", "1", out.rsplit(".", 1)[0] + "_cover.jpg"])
    print(f"{out} {dur(out):.1f}s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
