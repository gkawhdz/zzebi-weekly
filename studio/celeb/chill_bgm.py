"""'느좋' 감성 오리지널 배경음 (시티팝·로파이 팝 느낌, 저작권 걱정 없음)
사용: python3 chill_bgm.py out.wav 길이초 [seed]
seed마다 키·코드진행·템포·멜로디가 바뀜.
"""
import numpy as np, wave, sys
out = sys.argv[1]; DUR = float(sys.argv[2]); seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
rng = np.random.default_rng(seed); SR = 44100; N = int(SR * (DUR + 0.5)); mix = np.zeros(N); mixR = np.zeros(N)
BPM = [88, 92, 96, 100][seed % 4]; B = 60 / BPM; BAR = 4 * B
key = [0, 2, 5, 7, -3, -1][seed % 6]
progs = [[[0, 4, 7, 11], [9, 12, 16, 19], [5, 9, 12, 16], [7, 11, 14, 17]],      # Imaj7 vi7 IVmaj7 V7
         [[5, 9, 12, 16], [4, 7, 11, 14], [2, 5, 9, 12], [0, 4, 7, 11]],         # IVmaj7 iii7 ii7 Imaj7
         [[2, 5, 9, 12], [7, 11, 14, 17], [0, 4, 7, 11], [9, 12, 16, 19]]]       # ii7 V7 Imaj7 vi7
prog = progs[seed % 3]
hz = lambda m: 440 * 2 ** ((m - 69) / 12)

def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    e = min(N, i + len(sig)); s = sig[:e - i] * g
    mix[i:e] += s * (1 - max(0, pan)); mixR[i:e] += s * (1 + min(0, pan))

def keys(m, ln):  # 로즈 피아노 느낌
    n = int(ln * SR); t = np.arange(n) / SR; f = hz(m)
    s = np.sin(2 * np.pi * f * t + 0.8 * np.sin(2 * np.pi * f * t) * np.exp(-t * 3)) * (1 + 0.15 * np.sin(2 * np.pi * 4.5 * t))
    return s * np.minimum(1, t / 0.01) * np.exp(-t * 1.1) * 0.07

def bass(m, ln):
    n = int(ln * SR); t = np.arange(n) / SR
    return np.tanh(1.4 * np.sin(2 * np.pi * hz(m) * t)) * np.minimum(1, t / 0.008) * np.exp(-t * 1.6) * 0.28

def kick():
    n = int(.3 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(45 + 90 * np.exp(-t * 30)) / SR) * np.exp(-t * 9) * 0.7

def snap():
    n = int(.18 * SR); t = np.arange(n) / SR
    return np.convolve(rng.uniform(-1, 1, n), [1, -.95], "same") * np.exp(-t * 26) * 0.22

def hat():
    n = int(.04 * SR); t = np.arange(n) / SR
    return np.convolve(rng.uniform(-1, 1, n), [1, -1], "same") * np.exp(-t * 90) * 0.07

def bell(m):
    n = int(.9 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * hz(m) * t) * np.minimum(1, t / .005) * np.exp(-t * 3.2) * 0.09

base = 60 + key; t = 0.0; b = 0
scale = [0, 2, 4, 7, 9, 12, 14, 16]
while t < DUR:
    ch = prog[b % 4]
    for k, m in enumerate(ch):
        add(keys(base + m, BAR * 0.95), t + k * 0.012, pan=-.3 + .2 * k)
        add(keys(base + m, B * 1.2), t + 2.5 * B + k * 0.01, .6, pan=.2)
    root = base - 24 + ch[0]
    for off, ln, iv in [(0, 1.4, 0), (1.5, .4, 0), (2, 1.2, 7), (3.5, .45, 12)]:
        add(bass(root + iv, ln * B), t + off * B)
    if t >= BAR * 0.5:
        for q in range(4):
            if q in (0, 2): add(kick(), t + q * B)
            if q == 2 and b % 2: add(kick(), t + 2.75 * B, .6)
            if q in (1, 3): add(snap(), t + q * B)
            for e in (0, .5): add(hat(), t + q * B + e * B * (1.08 if e else 1), .9, pan=.4)
    for i in range(3):
        if rng.random() < .75:
            add(bell(base + 12 + scale[rng.integers(0, len(scale))]), t + (rng.integers(0, 8) / 2) * B, pan=.35)
    t += BAR; b += 1

st = np.stack([mix, mixR], 1)
st += rng.normal(0, .0025, st.shape)  # 바이닐 노이즈
st = np.tanh(st * 1.3); st /= np.abs(st).max() + 1e-9; st *= .85
fi, fo = int(.4 * SR), int(1.2 * SR)
st[:fi] *= np.linspace(0, 1, fi)[:, None]; st[N - fo:] *= np.linspace(1, 0, fo)[:, None]
st = st[:int(DUR * SR)]
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print("ok", out, BPM, "bpm")
