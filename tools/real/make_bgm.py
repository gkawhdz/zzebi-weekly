#!/usr/bin/env python3
"""오리지널 BGM 생성기 (직접 합성, 저작권 문제 없음): 하우스/로파이 패션 비트
사용법: python3 make_bgm.py 길이초 out.wav [bpm] [mood]
v2(2026-10-25): mood 선택 추가 — chill(기본, Am9 로파이) / warm(D장조 따뜻한 팝) / crisp(E단조 미니멀 하우스, 마림바풍 플럭) / cozy(F장조 재즈풍 로즈)"""
import sys, numpy as np, wave
SR = 44100
dur = float(sys.argv[1]); out = sys.argv[2]; bpm = float(sys.argv[3]) if len(sys.argv) > 3 else 112
mood = sys.argv[4] if len(sys.argv) > 4 else "chill"
beat = 60 / bpm; n = int(SR * (dur + 1)); mix = np.zeros((n, 2))
rng = np.random.default_rng(7)
def add(sig, t, pan=0.0, g=1.0):
    i = int(t * SR); j = min(n, i + len(sig))
    if i >= n: return
    s = sig[:j - i] * g
    mix[i:j, 0] += s * (1 - max(pan, 0)); mix[i:j, 1] += s * (1 + min(pan, 0))
def env(L, a=0.005, d=0.2):
    t = np.arange(L) / SR; e = np.minimum(t / a, 1) * np.exp(-t / d); return e
def kick():
    L = int(0.35 * SR); t = np.arange(L) / SR
    f = 50 + 90 * np.exp(-t * 30); ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 9)
def hat(open_=False):
    L = int((0.18 if open_ else 0.05) * SR); x = rng.standard_normal(L)
    x = np.diff(np.concatenate([[0], x]))  # 고역 강조
    return x * env(L, 0.001, 0.06 if open_ else 0.015) * 0.35
def clap():
    L = int(0.2 * SR); x = rng.standard_normal(L); return x * env(L, 0.002, 0.07) * 0.4
def note(freq, L, kind="pad"):
    t = np.arange(L) / SR
    if kind == "pad":
        s = sum(np.sin(2 * np.pi * freq * m * t + 0.3 * np.sin(2 * np.pi * 0.4 * t)) / m for m in (1, 2, 3))
        e = np.minimum(t / 0.25, 1) * np.minimum((L / SR - t) / 0.3, 1)
        return s * np.clip(e, 0, 1) * 0.12
    if kind == "bass":
        s = np.tanh(2.2 * np.sin(2 * np.pi * freq * t)); return s * env(L, 0.004, 0.35) * 0.35
    if kind == "mallet":  # 마림바풍: 빠른 감쇠 + 4배음
        s = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 4 * t) * np.exp(-t * 30)
        return s * env(L, 0.001, 0.12) * 0.18
    if kind == "rhodes":  # 로즈 피아노풍: 트레몰로 + 부드러운 감쇠
        s = (np.sin(2 * np.pi * freq * t) + 0.25 * np.sin(2 * np.pi * freq * 2 * t)) * (1 + 0.15 * np.sin(2 * np.pi * 5 * t))
        return s * env(L, 0.004, 0.5) * 0.10
    if kind == "pluck":
        s = np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 2 * t)
        return s * env(L, 0.002, 0.18) * 0.14
mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
# Am9 - Fmaj7 - Cmaj7 - Em7 (세련되고 차분한 무드)
MOODS = {
    "chill": ([[57, 60, 64, 67, 71], [53, 57, 60, 64], [48, 52, 55, 59], [52, 55, 59, 62]], [45, 41, 36, 40], "pluck"),
    "warm":  ([[62, 66, 69, 73], [59, 62, 66, 69], [55, 59, 62, 66], [57, 61, 64, 66]], [38, 47, 43, 45], "pluck"),
    "crisp": ([[52, 55, 59, 62], [48, 52, 55, 59], [55, 59, 62, 66], [50, 54, 57, 60]], [40, 36, 43, 38], "mallet"),
    "cozy":  ([[53, 57, 60, 64], [50, 53, 57, 60], [55, 58, 62, 65], [48, 52, 55, 58]], [41, 38, 43, 36], "rhodes"),
}
chords, roots, lead = MOODS.get(mood, MOODS["chill"])
bar = 4 * beat; nbars = int(np.ceil(dur / bar)) + 1
for b in range(nbars):
    t0 = b * bar; c = chords[b % 4]
    for m in c: add(note(mtof(m), int(bar * SR), "pad"), t0, pan=rng.uniform(-.3, .3))
    intro = b < 1  # 첫 마디는 패드+하이햇만 (훅 문장 집중)
    for k in range(4):
        tb = t0 + k * beat
        if not intro: add(kick(), tb, g=0.9)
        if k in (1, 3) and not intro: add(clap(), tb, pan=0.1)
        add(hat(), tb + beat / 2, pan=0.25)
        if not intro: add(note(mtof(roots[b % 4]), int(beat * 0.9 * SR), "bass"), tb + beat * 0.5 if k % 2 else tb)
    for k, m in enumerate([c[-1] + 12, c[-2] + 12, c[1] + 12, c[-1] + 12]):
        if not intro: add(note(mtof(m), int(0.4 * SR), lead), t0 + k * beat + beat * 0.75, pan=(-1) ** k * 0.4)
# 사이드체인 느낌 + 마스터
mix = mix[:int(dur * SR)]
t = np.arange(len(mix)) / SR
duck = 1 - 0.35 * np.exp(-((t % beat) / 0.12)); duck[t < bar] = 1
mix *= duck[:, None]
fade = np.minimum(1, np.minimum(t / 0.3, (dur - t) / 1.5))[:, None]
mix = np.tanh(mix * 1.4) * fade; mix /= np.max(np.abs(mix)) + 1e-9; mix *= 0.89
pcm = (mix * 32767).astype(np.int16)
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("bgm", out, dur, "s", bpm, "bpm", mood)
