#!/usr/bin/env python3
"""틱톡·유튜브 전용 '네이티브' 영상 (2026-11-01 사장님 지시: "짜집기 티가 너무 난다, 재미·후킹·클릭률 없다")

예전 몰아보기(make_tiktok_comp.py)는 인스타 릴스 3개를 통째로 이어 붙여서
  - 썸네일 격자 인트로 · 어두운 '01/03' 챕터 카드 · 영상마다 따로 나오는 훅/저장&팔로우 · 60초 채우려는 정지 화면
  이 그대로 보였다 = 짜집기.
이 도구는 오늘 만든 Trend Daily 대본(JSON)과 그림을 다시 써서 '처음부터 틱톡용으로 만든 한 편'을 렌더한다.
  - 0초: 틱톡 전용 후킹 한 장면(그림 꽉 + 큰 글씨, 이 화면이 곧 썸네일)
  - 본문: 세 영상의 보드 장면만 골라 1/N 번호를 새로 매겨 한 흐름으로 (영상별 훅·CTA·공식·브랜드 표시 제거)
  - 끝: 짧은 CTA 1번. 정지 화면으로 시간 채우기 금지.

사용: python3 make_tiktok_native.py native.json out.mp4 [--en]
native.json:
{
  "tools_dir": "/home/claude/td/tools",        # make_webtoon.py 가 있는 폴더 (Trend Daily 도구)
  "brand": "TREND DAILY · 11.01",
  "parts": [                                    # 오늘 A·B·C 대본 JSON, keep = 쓸 장면 번호(0부터, 보드만)
    {"spec": "/home/claude/td/A.json", "keep": [1, 2, 3]},
    {"spec": "/home/claude/td/B.json", "keep": [1, 2]},
    {"spec": "/home/claude/td/C.json", "keep": [2]}
  ],
  "hook": {"part": 1, "img": "b1", "oy": 300, "badge": "끝까지 보기", "kicker": "키 작은 남자라면",
           "title": "이 3개만\n바꾸세요", "body": "마지막이 제일 쉬워요 ↓", "dur": 2.8},
  "cta": {"kicker": "내일 아침 7시 30분에도", "title": "팔로우하고\n1분 코디 받기", "body": "@zzebi.st"},   # 선택
  "seed": 31,
  "en": {"hook": "...", "scenes": ["보드마다 영어 한 문장", ...], "cta": "Follow @zzebi.st for 1-min style tips"}   # --en 일 때
}
결과: out.mp4, out_thumb.jpg(0초 화면 = 썸네일), out_title.txt(제목 = 후킹 제목 그대로)
"""
import json, os, sys, subprocess, tempfile, copy
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_tiktok_comp as C  # sub_png, SUB_Y, dur 재사용


def sh(cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def build(ns):
    paintings, scenes = {}, []
    boards = []  # (part_idx, scene)
    for pi, part in enumerate(ns["parts"]):
        sp = json.load(open(part["spec"], encoding="utf-8")); base = os.path.dirname(os.path.abspath(part["spec"]))
        for k, v in sp["paintings"].items():
            paintings[f"p{pi}_{k}"] = v if os.path.isabs(v) else os.path.join(base, v)
        keep = part.get("keep") or [i for i, s in enumerate(sp["scenes"]) if s.get("type") == "wboard"]
        for i in keep:
            s = copy.deepcopy(sp["scenes"][i])
            for key in ("img", "left", "right"):
                if key in s: s[key] = f"p{pi}_{s[key]}"
            for tb in s.get("thumbs", []): tb["img"] = f"p{pi}_{tb['img']}"
            boards.append(s)
    n = len(boards)
    for j, s in enumerate(boards, 1):  # 번호를 1/N 으로 새로 매겨 '한 편'처럼
        if s.get("type") == "wboard":
            if s.get("head"):
                s["head"]["num"] = f"{j:02d}"; s["head"]["total"] = f"{n:02d}"
                s["chip"] = f"{j:02d} · " + s.get("chip", "").split("·", 1)[-1].strip()
            else:
                lab = s.get("label", "")
                lab = lab.split("·", 1)[-1].strip() if "·" in lab else lab
                s["label"] = f"{j} / {n} · {lab}"
    h = ns["hook"]
    hook = {"type": "whook", "img": f"p{h.get('part', 0)}_{h['img']}", "oy": h.get("oy", 300),
            "focus": h.get("focus", [520, 700]), "dur": h.get("dur", 2.8), "badge": h.get("badge", "끝까지 보기"),
            "kicker": h.get("kicker", ""), "title": h["title"], "body": h.get("body", ""), "title_size": h.get("title_size", 112)}
    scenes = [hook] + boards
    c = ns.get("cta", {})
    scenes.append({"type": "text", "dur": c.get("dur", 2.4), "bg": "#00A8A8", "fg": "#ffffff", "accent": "#ffffff",
                   "kicker": c.get("kicker", "내일 아침에도 1분 코디"), "title": c.get("title", "팔로우하고\n내일도 보기"),
                   "body": c.get("body", "@zzebi.st"), "source": c.get("source", ""), "no_wipe": True})
    return {"brand": ns.get("brand", "@zzebi.st"), "paintings": paintings, "scenes": scenes}


def main(path, out, en=False):
    ns = json.load(open(path, encoding="utf-8"))
    tmp = tempfile.mkdtemp(); spec = build(ns)
    sp_path = os.path.join(tmp, "merged.json"); json.dump(spec, open(sp_path, "w"), ensure_ascii=False, indent=1)
    silent = os.path.join(tmp, "silent.mp4")
    r = subprocess.run(["python3", os.path.join(ns["tools_dir"], "make_webtoon.py"), sp_path, silent], capture_output=True, text=True)
    if r.returncode: print(r.stderr); sys.exit(1)
    durs = [s.get("dur", 3) for s in spec["scenes"]]; total = sum(durs)
    v = silent
    if en and ns.get("en"):
        e = ns["en"]; texts = [e.get("hook", "")] + list(e.get("scenes", [])) + [e.get("cta", "Follow @zzebi.st for 1-min style tips")]
        inputs, fl, t, last = ["-i", silent], [], 0.0, "0:v"
        for j, (d, txt) in enumerate(zip(durs, texts)):
            if txt:
                png = f"{tmp}/s{j}.png"; C.sub_png(txt, png); inputs += ["-i", png]; k = len(inputs) // 2 - 1
                fl.append(f"[{last}][{k}:v]overlay=0:{C.SUB_Y}:enable='between(t,{t + 0.05:.2f},{t + d:.2f})'[o{j}]"); last = f"o{j}"
            t += d
        if fl:
            v = f"{tmp}/sub.mp4"
            sh(["ffmpeg", "-y", *inputs, "-filter_complex", ";".join(fl), "-map", f"[{last}]", "-c:v", "libx264",
                "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", v])
    bgm = f"{tmp}/bgm.wav"
    sh(["python3", os.path.join(HERE, "chill_bgm.py"), bgm, f"{total + 0.5:.2f}", str(ns.get("seed", 1))])
    sh(["ffmpeg", "-y", "-i", v, "-i", bgm, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
        "-af", f"afade=t=out:st={total - 1.2:.2f}:d=1.2,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100,alimiter=limit=0.6:level=false,volume=0.8",
        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out])
    stem = out.rsplit(".", 1)[0]
    sh(["ffmpeg", "-y", "-ss", "0", "-i", silent, "-frames:v", "1", "-q:v", "2", stem + "_thumb.jpg"])  # 썸네일 = 0초 화면(자막 없음)
    ko = " ".join(l.strip() for l in ns["hook"]["title"].split("\n"))
    title = ko + (f" | {ns['en']['hook']}" if en and ns.get("en", {}).get("hook") else "") + (" #shorts" if en else "")
    if len(title) > 100: title = ko + (" #shorts" if en else "")
    open(stem + "_title.txt", "w").write(title)
    print(f"{out} {C.dur(out):.1f}s · 장면 {len(spec['scenes'])}개")
    print(f"썸네일 {stem}_thumb.jpg · 제목 {title}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], en="--en" in sys.argv[3:])
