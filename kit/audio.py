import numpy as np, wave

SR = 44100
starts = [0, 3.4, 7.8, 12.2, 16.4, 20.6, 25.0, 29.4, 34.4]
END = 37.8
N = int(SR * END)
mix = np.zeros(N)
rng = np.random.default_rng(1)


def add(sig, t, g=1.0):
    i = int(t * SR)
    j = min(N, i + len(sig))
    if i < N:
        mix[i:j] += sig[: j - i] * g


def env(n, a=0.005, r=None):
    e = np.ones(n)
    na = max(1, int(a * SR))
    e[:na] = np.linspace(0, 1, na)
    if r is None:
        e *= np.exp(-np.linspace(0, 6, n))
    return e


def tone(freq, dur, kind="sq", decay=True):
    t = np.arange(int(dur * SR)) / SR
    ph = 2 * np.pi * (np.cumsum(np.broadcast_to(freq, t.shape)) / SR if np.ndim(freq) else freq * t)
    if kind == "sq":
        s = np.sign(np.sin(ph)) * 0.5
    elif kind == "saw":
        s = 2 * ((ph / (2 * np.pi)) % 1) - 1
    else:
        s = np.sin(ph)
    return s * (env(len(t)) if decay else 1)


def kick():
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    f = 50 + 120 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)


def hat():
    n = int(0.05 * SR)
    s = rng.standard_normal(n)
    s = np.diff(np.concatenate([[0], s]))
    return s * np.exp(-np.linspace(0, 8, n)) * 0.25


def snare():
    n = int(0.18 * SR)
    t = np.arange(n) / SR
    return (rng.standard_normal(n) * 0.5 + np.sin(2 * np.pi * 190 * t) * 0.5) * np.exp(-t * 22)


def whoosh(d=0.35):
    n = int(d * SR)
    s = rng.standard_normal(n)
    out = np.zeros(n)
    a = 0.0
    for i in range(n):  # sweeping one-pole lowpass
        c = 0.02 + 0.5 * (i / n)
        a += c * (s[i] - a)
        out[i] = a
    return out * np.sin(np.linspace(0, np.pi, n)) * 0.9


def boom():
    n = int(1.2 * SR)
    t = np.arange(n) / SR
    f = 40 + 80 * np.exp(-t * 8)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.5)
    s += rng.standard_normal(n) * np.exp(-t * 18) * 0.4
    return s


def ding():
    return tone(1568, 0.5, "sine") * 0.5 + tone(2093, 0.5, "sine") * 0.35


def note(m):
    return 440 * 2 ** ((m - 69) / 12)


bpm = 132
beat = 60 / bpm


def groove(t0, t1, root=45, scale=(0, 3, 5, 7, 10, 12), mel=True, seed=0):
    r = np.random.default_rng(seed)
    b = 0
    t = t0
    bass_pat = [0, 0, 7, 0, 10, 0, 7, 5]
    while t < t1 - 0.01:
        if b % 2 == 0:
            add(kick(), t, 0.9)
        else:
            add(snare(), t, 0.45)
        add(hat(), t + beat / 2, 0.6)
        add(hat(), t, 0.4)
        bn = bass_pat[b % 8]
        add(tone(note(root + bn - 12), beat * 0.9, "saw") * 0.22, t)
        if mel:
            for k in range(2):
                if r.random() < 0.7:
                    m = root + 12 + scale[r.integers(len(scale))]
                    add(tone(note(m), beat * 0.45, "sq") * 0.11, t + k * beat / 2)
        b += 1
        t += beat


# music
groove(0.0, 20.6, seed=2)
# tension (s6): rising drone + heartbeat
tt = np.arange(int(4.4 * SR)) / SR
f = 55 * 2 ** (tt / 4.4 * 1.0)
drone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25 + (2 * ((np.cumsum(f * 1.01) / SR) % 1) - 1) * 0.08
drone *= np.linspace(0.3, 1, len(tt))
add(drone, 20.6)
for k in range(8):
    add(kick(), 20.6 + k * 0.55, 0.8)
    add(kick(), 20.6 + k * 0.55 + 0.16, 0.5)
# crash: sad trombone
add(boom(), 25.1, 1.2)
for i, (m, d) in enumerate([(58, 0.45), (57, 0.45), (56, 0.45), (55, 1.4)]):
    t0 = 25.9 + i * 0.48
    n = int(d * SR)
    tq = np.arange(n) / SR
    vib = 1 + (0.012 * np.sin(2 * np.pi * 6 * tq) if i == 3 else 0)
    fr = np.ones(n) * note(m) * vib * (1 - (0.06 * tq / d if i == 3 else 0))
    s = (2 * ((np.cumsum(fr) / SR) % 1) - 1)
    s *= np.minimum(1, tq / 0.04) * np.minimum(1, (d - tq) / 0.1)
    add(s * 0.22, t0)
# twist: brighter groove in major
groove(29.4, END - 0.3, root=48, scale=(0, 2, 4, 7, 9, 12), seed=5)

# sfx
for s in starts[1:]:
    add(whoosh(), s - 0.2, 0.7)
add(boom(), 0.0, 1.0)
add(boom(), 22.8, 1.1)
add(ding(), 10.4)
add(ding(), 18.1)
add(ding(), 31.4)
add(ding(), 31.55)
# fade out
fo = int(0.6 * SR)
mix[-fo:] *= np.linspace(1, 0, fo)

mix = np.tanh(mix * 1.1)
mix /= np.max(np.abs(mix)) + 1e-9
mix *= 0.89
pcm = (mix * 32767).astype(np.int16)
st = np.repeat(pcm[:, None], 2, axis=1)
with wave.open("/home/claude/video/audio.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(st.tobytes())
print("ok", END)
