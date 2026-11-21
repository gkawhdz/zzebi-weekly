#!/usr/bin/env python3
"""사장님 노래 3곡 돌려쓰기 배경음 (2026-11-21 사장님 지시: "이거 3개 돌아가면서 써줘")
모든 릴스(트렌드·셀럽 스냅 해부·안전장치·긴급대응)의 배경음은 make_bgm.py·chill_bgm.py 대신 이 도구로 넣습니다.

사용:
  python3 tools/song_bgm.py <입력.mp4> <출력.mp4> --tag "<YYYY-MM-DD 슬롯 팀>" [--song 1|2|3] [--no-log]
- --song 을 안 주면 studio/music/rotation.json 의 next 곡을 쓰고 next 를 1→2→3→1 로 넘김(같은 저장소를 쓰는 모든 팀 공용 순번).
  → 쓰고 나면 rotation.json 을 커밋·푸시하세요(다른 팀이 다음 곡을 이어 쓰도록).
- 곡에서 영상 길이만큼 가장 소리가 꽉 찬 구간을 자동으로 골라(앞 8초·끝 6초 제외) 0.3초 페이드인, 끝 1.6초 페이드아웃.
- 입력 영상의 원래 소리는 버리고 노래로 교체. 음량: loudnorm -14 LUFS, 최대 -1.5dB 이하(alimiter).
- 출력 후 max_volume 을 출력해 줌(-1dB 이하인지 확인).
"""
import sys, os, json, subprocess, argparse, datetime
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC = os.path.join(ROOT, "studio", "music")
ROT = os.path.join(MUSIC, "rotation.json")

def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)

def best_start(song, need):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", song, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                         capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    sec = np.sqrt(np.add.reduceat(x ** 2, np.arange(0, len(x), 8000)) / 8000)  # 초당 RMS
    total = len(sec); lo, hi = 8, total - 6 - int(np.ceil(need))
    if hi <= lo: return max(0.0, (total - need) / 2)
    win = int(np.ceil(need)); c = np.convolve(sec, np.ones(win), "valid")
    s = lo + int(np.argmax(c[lo:hi + 1]))
    return float(s)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--tag", default=""); ap.add_argument("--song", type=int); ap.add_argument("--no-log", action="store_true")
    a = ap.parse_args()
    rot = json.load(open(ROT)) if os.path.exists(ROT) else {"next": 1, "log": []}
    n = a.song or rot["next"]
    song = os.path.join(MUSIC, f"song{n}.mp3"); assert os.path.exists(song), song
    D = dur(a.src); st = best_start(song, D)
    af = (f"atrim=start={st:.2f}:duration={D:.2f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.3,"
          f"afade=t=out:st={max(0, D - 1.6):.2f}:d=1.6,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100,"
          f"alimiter=limit=0.6:level=false,volume=0.8")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.src, "-i", song, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "192k", "-t", f"{D:.2f}", "-movflags", "+faststart", a.out], check=True)
    mv = subprocess.run(["ffmpeg", "-i", a.out, "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    mv = [l.split("max_volume:")[1].strip() for l in mv.splitlines() if "max_volume" in l]
    if not a.no_log:
        rot["log"] = ([{"at": datetime.datetime.now().isoformat(timespec="minutes"), "song": n, "start": st, "tag": a.tag}] + rot.get("log", []))[:60]
        if not a.song: rot["next"] = n % 3 + 1
        json.dump(rot, open(ROT, "w"), ensure_ascii=False, indent=1)
    print(f"done {a.out} song{n} from {st:.0f}s len {D:.1f}s max_volume {mv[0] if mv else '?'}")

if __name__ == "__main__": main()
