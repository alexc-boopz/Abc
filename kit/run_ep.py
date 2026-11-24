import sys, os, subprocess, wave, glob
import numpy as np
sys.path.insert(0, "/home/claude/video")
import make
from make import render_scene, FPS
from PIL import Image

SR = 44100


def build_audio(path, starts, end, tension, fail, twist, dings=(), booms=(), seed=0):
    N = int(SR * end)
    mix = np.zeros(N)
    rng = np.random.default_rng(seed)

    def add(sig, t, g=1.0):
        i = int(t * SR)
        if i >= N or i < 0:
            return
        j = min(N, i + len(sig))
        mix[i:j] += sig[: j - i] * g

    def env(n):
        e = np.exp(-np.linspace(0, 6, n))
        na = max(1, int(0.005 * SR))
        e[:na] *= np.linspace(0, 1, na)
        return e

    def tone(f, dur, kind="sq"):
        t = np.arange(int(dur * SR)) / SR
        ph = 2 * np.pi * f * t
        s = np.sign(np.sin(ph)) * 0.5 if kind == "sq" else (2 * ((f * t) % 1) - 1 if kind == "saw" else np.sin(ph))
        return s * env(len(t))

    def kick():
        t = np.arange(int(0.25 * SR)) / SR
        f = 50 + 120 * np.exp(-t * 30)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 14)

    def hat():
        n = int(0.05 * SR)
        s = np.diff(np.concatenate([[0], rng.standard_normal(n)]))
        return s * np.exp(-np.linspace(0, 8, n)) * 0.25

    def snare():
        t = np.arange(int(0.18 * SR)) / SR
        return (rng.standard_normal(len(t)) * 0.5 + np.sin(2 * np.pi * 190 * t) * 0.5) * np.exp(-t * 22)

    def whoosh(d=0.35):
        n = int(d * SR)
        s = rng.standard_normal(n)
        out = np.zeros(n)
        a = 0.0
        for i in range(n):
            a += (0.02 + 0.5 * i / n) * (s[i] - a)
            out[i] = a
        return out * np.sin(np.linspace(0, np.pi, n)) * 0.9

    def boom():
        t = np.arange(int(1.2 * SR)) / SR
        f = 40 + 80 * np.exp(-t * 8)
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.5) + rng.standard_normal(len(t)) * np.exp(-t * 18) * 0.4

    def ding():
        return tone(1568, 0.5, "sine") * 0.5 + tone(2093, 0.5, "sine") * 0.35

    note = lambda m: 440 * 2 ** ((m - 69) / 12)
    beat = 60 / 132

    def groove(t0, t1, root, scale, sd):
        r = np.random.default_rng(sd)
        b, t = 0, t0
        pat = [0, 0, 7, 0, 10, 0, 7, 5]
        while t < t1 - 0.01:
            add(kick(), t, 0.9) if b % 2 == 0 else add(snare(), t, 0.45)
            add(hat(), t, 0.4)
            add(hat(), t + beat / 2, 0.6)
            add(tone(note(root + pat[b % 8] - 12), beat * 0.9, "saw") * 0.22, t)
            for k in range(2):
                if r.random() < 0.7:
                    add(tone(note(root + 12 + scale[r.integers(len(scale))]), beat * 0.45) * 0.11, t + k * beat / 2)
            b += 1
            t += beat

    groove(0, tension[0], 45, (0, 3, 5, 7, 10, 12), seed + 2)
    td = tension[1] - tension[0]
    tt = np.arange(int(td * SR)) / SR
    f = 55 * 2 ** (tt / td)
    drone = (np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25 + (2 * ((np.cumsum(f * 1.01) / SR) % 1) - 1) * 0.08)
    add(drone * np.linspace(0.3, 1, len(tt)), tension[0])
    k = 0
    while tension[0] + k * 0.55 < tension[1]:
        add(kick(), tension[0] + k * 0.55, 0.8)
        add(kick(), tension[0] + k * 0.55 + 0.16, 0.5)
        k += 1
    add(boom(), fail, 1.2)
    for i, (m, dd) in enumerate([(58, 0.45), (57, 0.45), (56, 0.45), (55, 1.4)]):
        n = int(dd * SR)
        tq = np.arange(n) / SR
        fr = np.ones(n) * note(m) * (1 + (0.012 * np.sin(2 * np.pi * 6 * tq) if i == 3 else 0))
        s = 2 * ((np.cumsum(fr) / SR) % 1) - 1
        s *= np.minimum(1, tq / 0.04) * np.minimum(1, (dd - tq) / 0.1)
        add(s * 0.22, fail + 0.8 + i * 0.48)
    groove(twist, end - 0.3, 48, (0, 2, 4, 7, 9, 12), seed + 5)
    for s in starts[1:]:
        add(whoosh(), s - 0.2, 0.7)
    add(boom(), 0.0, 1.0)
    for t in booms:
        add(boom(), t, 1.0)
    for t in dings:
        add(ding(), t)
    fo = int(0.6 * SR)
    mix[-fo:] *= np.linspace(1, 0, fo)
    mix = np.tanh(mix * 1.1)
    mix /= np.max(np.abs(mix)) + 1e-9
    pcm = (mix * 0.89 * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())


def run(tag, scenes, tension_idx, fail_idx, twist_idx, dings=(), booms=(), check=False):
    """dings/booms: list of (scene_idx, t_in_scene)."""
    out = f"/home/claude/video/{tag}"
    os.makedirs(out, exist_ok=True)
    make.OUT = out
    built = [fn() for fn in scenes]
    durs = [b[1] for b in built]
    starts = list(np.cumsum([0] + durs[:-1]))
    end = float(sum(durs))
    if check:
        for f in glob.glob(f"{out}/../check_{tag}_*.jpg"):
            os.remove(f)
        ims = []
        for i, (base, dur, items, kw) in enumerate(built):
            name = f"{tag}_{i:02d}"
            n = int(round(dur * FPS))
            render_scene(name, base, dur, items, frames_only={n - 5}, **kw)
            ims.append(Image.open(f"{out}/../check_{name}_{n - 5}.jpg").resize((270, 480)))
        cols = 7
        rows = (len(ims) + cols - 1) // cols
        sheet = Image.new("RGB", (270 * cols, 480 * rows), "white")
        for i, im in enumerate(ims):
            sheet.paste(im, ((i % cols) * 270, (i // cols) * 480))
        sheet.save(f"/home/claude/video/sheet_{tag}.jpg", quality=80)
        print(tag, "total", end)
        return
    names = []
    for i, (base, dur, items, kw) in enumerate(built):
        name = f"{tag}_{i:02d}"
        render_scene(name, base, dur, items, **kw)
        names.append(name)
    with open(f"{out}/list.txt", "w") as fh:
        for n in names:
            fh.write(f"file '{out}/{n}.mp4'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{out}/list.txt",
                    "-c", "copy", f"{out}/video.mp4"], check=True)
    S = lambda p: starts[p[0]] + p[1]
    build_audio(f"{out}/audio.wav", starts, end, (starts[tension_idx], starts[tension_idx + 1]),
                starts[fail_idx] + 0.15, starts[twist_idx], [S(p) for p in dings], [S(p) for p in booms])
    final = f"/home/claude/video/{tag}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{out}/video.mp4", "-i", f"{out}/audio.wav",
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    final], check=True)
    print(tag, "done", end)
