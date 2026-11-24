import math, random, subprocess, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, K = 1080, 1920, 30, 2
ANTON = "/usr/share/fonts/truetype/google-fonts/ofl/anton/Anton-Regular.ttf"
ARCH = "/usr/share/fonts/truetype/google-fonts/ofl/archivoblack/ArchivoBlack-Regular.ttf"
CJK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
INK = (30, 20, 25)
SKIN = (255, 224, 199)
SKIN_SH = (240, 190, 165)
HAIR = (35, 38, 70)
HAIR_HI = (80, 90, 150)
OUT = "/home/claude/video/scenes"


class D:
    """1x-coordinate drawing on a 2x canvas (for smooth edges)."""
    def __init__(self, img):
        self.img = img
        self.d = ImageDraw.Draw(img)

    def _p(self, pts):
        return [(x * K, y * K) for x, y in pts]

    def poly(self, pts, fill=None, outline=INK, width=6):
        self.d.polygon(self._p(pts), fill=fill)
        if outline and width:
            p = self._p(pts)
            self.d.line(p + [p[0]], fill=outline, width=width * K, joint="curve")

    def ell(self, box, fill=None, outline=INK, width=6):
        x0, y0, x1, y1 = box
        self.d.ellipse([x0 * K, y0 * K, x1 * K, y1 * K], fill=fill,
                       outline=outline if width else None, width=width * K if width else 0)

    def line(self, pts, fill=INK, width=6):
        self.d.line(self._p(pts), fill=fill, width=width * K, joint="curve")

    def rect(self, box, fill=None, outline=INK, width=6, r=0):
        x0, y0, x1, y1 = box
        self.d.rounded_rectangle([x0 * K, y0 * K, x1 * K, y1 * K], radius=r * K, fill=fill,
                                 outline=outline if width else None, width=width * K if width else 0)

    def arc(self, box, a0, a1, fill=INK, width=6):
        x0, y0, x1, y1 = box
        self.d.arc([x0 * K, y0 * K, x1 * K, y1 * K], a0, a1, fill=fill, width=width * K)

    def text(self, xy, s, size, fill, font=ANTON, anchor="mm", stroke=0, sfill=INK):
        f = ImageFont.truetype(font, size * K)
        self.d.text((xy[0] * K, xy[1] * K), s, font=f, fill=fill, anchor=anchor,
                    stroke_width=stroke * K, stroke_fill=sfill)


def canvas(color=(0, 0, 0)):
    return Image.new("RGBA", (W * K, H * K), color + (255,))


def gradient(top, bot):
    a = np.linspace(0, 1, H * K)[:, None, None]
    arr = (np.array(top) * (1 - a) + np.array(bot) * a).astype(np.uint8)
    arr = np.repeat(arr, W * K, axis=1)
    img = Image.fromarray(arr, "RGB").convert("RGBA")
    return img


def halftone(img, color, spacing=34, rmax=9, fade_from_bottom=True):
    d = D(img)
    for y in range(0, H, spacing):
        for x in range(0, W, spacing):
            t = y / H if fade_from_bottom else 1 - y / H
            r = rmax * t
            if r > 1:
                ox = (spacing // 2) if (y // spacing) % 2 else 0
                d.ell((x + ox - r, y - r, x + ox + r, y + r), fill=color, outline=None, width=0)


def speed_lines(seed, cx=W / 2, cy=H / 2, color=(255, 255, 255, 200), n=90, inner=380):
    rnd = random.Random(seed)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(lay)
    R = 2400
    for i in range(n):
        a = rnd.uniform(0, 2 * math.pi)
        w = rnd.uniform(0.004, 0.018)
        r0 = inner + rnd.uniform(0, 260)
        p = [(cx + math.cos(a) * r0, cy + math.sin(a) * r0),
             (cx + math.cos(a - w) * R, cy + math.sin(a - w) * R),
             (cx + math.cos(a + w) * R, cy + math.sin(a + w) * R)]
        dr.polygon(p, fill=color)
    return lay


def sparkle(d, x, y, r, fill=(255, 255, 255)):
    pts = []
    for i in range(8):
        a = i * math.pi / 4 - math.pi / 2
        rr = r if i % 2 == 0 else r * 0.28
        pts.append((x + math.cos(a) * rr, y + math.sin(a) * rr))
    d.poly(pts, fill=fill, outline=None, width=0)


def sweat(d, x, y, s=1.0):
    pts = [(x, y - 60 * s)]
    for i in range(0, 181, 15):
        a = math.radians(i)
        pts.append((x + 32 * s * math.cos(a), y + 32 * s * math.sin(a)))
    d.poly(pts, fill=(140, 200, 255), outline=(40, 80, 160), width=4)
    d.ell((x + 8 * s, y - 10 * s, x + 18 * s, y + 10 * s), fill=(255, 255, 255), outline=None, width=0)


def kenji(img, cx, cy, s=1.0, expr="neutral", outfit="hoodie", glow_eyes=False):
    d = D(img)
    S = lambda x, y: (cx + x * s, cy + y * s)
    lw = max(4, int(7 * s))

    # body
    if outfit == "hoodie":
        body = (255, 110, 60)
        d.poly([S(-360, 520), S(-300, 300), S(-120, 240), S(120, 240), S(300, 300), S(360, 520),
                S(420, 1200), S(-420, 1200)], fill=body, width=lw)
        d.poly([S(-120, 240), S(0, 330), S(120, 240)], fill=(220, 80, 40), width=lw)
        d.line([S(-50, 300), S(-60, 450)], width=lw)
        d.line([S(50, 300), S(60, 450)], width=lw)
    elif outfit == "suit":
        d.poly([S(-360, 520), S(-300, 300), S(-120, 240), S(120, 240), S(300, 300), S(360, 520),
                S(420, 1200), S(-420, 1200)], fill=(45, 48, 62), width=lw)
        d.poly([S(-110, 245), S(0, 520), S(110, 245)], fill=(255, 255, 255), width=lw)
        d.poly([S(-25, 270), S(25, 270), S(40, 470), S(0, 530), S(-40, 470)], fill=(230, 40, 60), width=lw)
        d.poly([S(-120, 240), S(-40, 380), S(-150, 330)], fill=(35, 38, 50), width=lw)
        d.poly([S(120, 240), S(40, 380), S(150, 330)], fill=(35, 38, 50), width=lw)
    # neck
    d.poly([S(-70, 170), S(70, 170), S(80, 260), S(0, 300), S(-80, 260)], fill=SKIN_SH, width=lw)

    # back hair
    pts = []
    n = 13
    for i in range(n + 1):
        a = math.radians(165 + i * (210 / n))
        r = 330 if i % 2 == 0 else 245
        pts.append(S(math.cos(a) * r, -40 + math.sin(a) * r * 1.05))
    pts += [S(230, 40), S(-230, 40)]
    d.poly(pts, fill=HAIR, width=lw)

    # ears
    for sx in (-1, 1):
        d.ell((*S(sx * 228 - 35, -10), *S(sx * 228 + 35, 90)) if sx < 0 else
              (*S(sx * 228 - 35, -10), *S(sx * 228 + 35, 90)), fill=SKIN, width=lw)

    # face
    face = []
    for i in range(0, 181, 10):
        a = math.radians(180 + i)
        face.append(S(230 * math.cos(a), 250 * math.sin(a)))
    face += [S(225, 60), S(150, 205), S(0, 275), S(-150, 205), S(-225, 60)]
    d.poly(face, fill=SKIN, width=lw)

    # shading under bangs

    ey = 35
    # ---- eyes
    def normal_eye(sx, lid=0.0, iris=(60, 125, 215), glow=False):
        ex = sx * 105
        x0, y0, x1, y1 = S(ex - 68, ey - 62)[0], S(ex - 68, ey - 62)[1], S(ex + 68, ey + 62)[0], S(ex + 68, ey + 62)[1]
        d.ell((x0, y0, x1, y1), fill=(255, 255, 255), width=lw - 2)
        ic = (255, 200, 40) if glow else iris
        d.ell((*S(ex - 46, ey - 52), *S(ex + 46, ey + 60)), fill=ic, width=lw - 2)
        d.ell((*S(ex - 22, ey - 18), *S(ex + 22, ey + 34)), fill=(20, 20, 40) if not glow else (180, 90, 0),
              outline=None, width=0)
        d.ell((*S(ex - 34, ey - 42), *S(ex - 4, ey - 12)), fill=(255, 255, 255), outline=None, width=0)
        d.ell((*S(ex + 14, ey + 22), *S(ex + 28, ey + 36)), fill=(255, 255, 255), outline=None, width=0)
        if lid > 0:
            ly = ey - 62 + 124 * lid
            d.poly([S(ex - 80, ey - 75), S(ex + 80, ey - 75), S(ex + 80, ly), S(ex - 80, ly)], fill=SKIN,
                   outline=None, width=0)
            d.line([S(ex - 75, ly + 4), S(ex + 75, ly - 2)], width=lw + 5)
        else:
            d.arc((*S(ex - 72, ey - 66), *S(ex + 72, ey + 70)), 195, 345, width=lw + 6)
        if sx < 0:
            d.line([S(ex - 70, ey - 30), S(ex - 92, ey - 48)], width=lw)
        else:
            d.line([S(ex + 70, ey - 30), S(ex + 92, ey - 48)], width=lw)

    if expr in ("neutral", "smug", "intense"):
        lid = {"neutral": 0.0, "smug": 0.45, "intense": 0.38}[expr]
        for sx in (-1, 1):
            normal_eye(sx, lid, glow=glow_eyes)
    elif expr in ("shout", "joy"):
        for sx in (-1, 1):
            ex = sx * 105
            if expr == "shout":
                d.line([S(ex - 55 * sx, ey - 40), S(ex + 45 * sx, ey), S(ex - 55 * sx, ey + 40)], width=lw + 6)
            else:
                d.arc((*S(ex - 60, ey - 30), *S(ex + 60, ey + 60)), 200, 340, width=lw + 6)
    elif expr == "shock":
        for sx in (-1, 1):
            ex = sx * 105
            d.ell((*S(ex - 65, ey - 65), *S(ex + 65, ey + 65)), fill=(255, 255, 255), width=lw)
            d.ell((*S(ex - 9, ey - 9), *S(ex + 9, ey + 9)), fill=INK, outline=None, width=0)

    # ---- brows
    by = ey - 95
    if expr == "smug":
        d.line([S(-170, by + 10), S(-50, by + 20)], width=lw + 4)
        d.line([S(50, by - 10), S(170, by - 30)], width=lw + 4)
    elif expr in ("intense", "shout"):
        d.line([S(-175, by - 15), S(-50, by + 25)], width=lw + 6)
        d.line([S(50, by + 25), S(175, by - 15)], width=lw + 6)
    elif expr == "shock":
        d.line([S(-170, by - 25), S(-60, by - 45)], width=lw + 2)
        d.line([S(60, by - 45), S(170, by - 25)], width=lw + 2)
    else:
        d.arc((*S(-180, by - 10), *S(-50, by + 40)), 200, 330, width=lw + 3)
        d.arc((*S(50, by - 10), *S(180, by + 40)), 210, 340, width=lw + 3)

    # nose
    d.line([S(6, 105), S(-6, 125)], width=lw - 2)

    # ---- mouth
    my = 185
    if expr == "neutral":
        d.arc((*S(-40, my - 30), *S(40, my + 10)), 20, 160, width=lw)
    elif expr == "smug":
        d.line([S(-50, my), S(20, my + 4), S(60, my - 22)], width=lw)
    elif expr == "intense":
        d.line([S(-45, my + 5), S(45, my + 5)], width=lw)
    elif expr == "shout":
        d.poly([S(-90, my - 40), S(90, my - 40), S(55, my + 70), S(-55, my + 70)], fill=(160, 30, 50), width=lw)
        d.poly([S(-80, my - 38), S(80, my - 38), S(72, my - 15), S(-72, my - 15)], fill=(255, 255, 255),
               outline=None, width=0)
        d.ell((*S(-40, my + 25), *S(40, my + 65)), fill=(255, 110, 130), outline=None, width=0)
    elif expr == "joy":
        d.poly([S(-75, my - 30), S(75, my - 30), S(0, my + 55)], fill=(160, 30, 50), width=lw)
        d.poly([S(-68, my - 28), S(68, my - 28), S(55, my - 12), S(-55, my - 12)], fill=(255, 255, 255),
               outline=None, width=0)
    elif expr == "shock":
        pts = []
        for i in range(9):
            pts.append(S(-60 + i * 15, my - 15 + (8 if i % 2 else -8)))
        for i in range(9):
            pts.append(S(60 - i * 15, my + 50 + (8 if i % 2 else -8)))
        d.poly(pts, fill=(120, 30, 50), width=lw)

    # blush
    if expr in ("joy", "shout", "smug"):
        for sx in (-1, 1):
            for k in range(3):
                x = sx * 150 + k * 18 - 18
                d.line([S(x + 10, 100), S(x - 6, 128)], fill=(240, 110, 110), width=lw - 2)

    # bangs
    bang = [S(-250, -90)]
    xs = list(range(-240, 241, 60))
    for i, x in enumerate(xs):
        bang.append(S(x, -20 if i % 2 == 0 else -150))
    bang += [S(250, -90), S(240, -200), S(130, -290), S(0, -310), S(-130, -290), S(-240, -200)]
    d.poly(bang, fill=HAIR, width=lw)
    d.line([S(-120, -240), S(-60, -170)], fill=HAIR_HI, width=lw + 4)
    d.line([S(40, -260), S(90, -190)], fill=HAIR_HI, width=lw + 4)

    if expr == "shock":
        # gloom lines
        for i in range(7):
            x = -170 + i * 55
            d.line([S(x, -60), S(x, 0)], fill=(90, 110, 200), width=lw - 1)
    if expr == "intense":
        if glow_eyes:
            for sx in (-1, 1):
                d.ell((*S(sx * 105 - 20, ey - 10), *S(sx * 105 + 20, ey + 30)), fill=(255, 250, 200), outline=None,
                      width=0)


def finish(img):
    return img.resize((W, H), Image.LANCZOS)


def text_block(lines, size, font=ANTON, stroke=10, maxw=980, gap=8, shadow=True):
    """lines: list of (text, color). Returns RGBA."""
    fonts, rows = [], []
    for t, c in lines:
        sz = size
        f = ImageFont.truetype(font, sz)
        while f.getbbox(t, stroke_width=stroke)[2] > maxw and sz > 30:
            sz -= 4
            f = ImageFont.truetype(font, sz)
        bb = f.getbbox(t, stroke_width=stroke)
        rows.append((t, c, f, bb))
    hs = [r[3][3] - r[3][1] for r in rows]
    ws = [r[3][2] - r[3][0] for r in rows]
    bw, bh = max(ws) + 40, sum(hs) + gap * (len(rows) - 1) + 40
    img = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    y = 20
    for (t, c, f, bb), h in zip(rows, hs):
        x = (bw - (bb[2] - bb[0])) / 2 - bb[0]
        if shadow:
            dr.text((x + 8, y - bb[1] + 10), t, font=f, fill=(0, 0, 0, 160), stroke_width=stroke,
                    stroke_fill=(0, 0, 0, 160))
        dr.text((x, y - bb[1]), t, font=f, fill=c, stroke_width=stroke, stroke_fill=INK)
        y += h + gap
    return img


def caption_box(lines, size=62, bg=(255, 255, 255), fg=INK):
    t = text_block([(l, fg) for l in lines], size, font=ARCH, stroke=0, shadow=False, maxw=900, gap=14)
    pad = 26
    img = Image.new("RGBA", (t.width + pad * 2, t.height + pad * 2 - 10), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    dr.rounded_rectangle([8, 10, img.width - 1, img.height - 1], 18, fill=(0, 0, 0, 150))
    dr.rounded_rectangle([0, 0, img.width - 9, img.height - 11], 18, fill=bg, outline=INK, width=6)
    img.alpha_composite(t, (pad - 4, pad - 14))
    return img


# ---------------------------------------------------------------- scene renderer
def ease_out_back(t):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


def render_scene(name, base, dur, items, zoom=(1.0, 1.05), shake=None, speed=None, flash=True, frames_only=None):
    """items: list of dict(img, t, xy(center), pop=True, wobble=0)"""
    n = int(round(dur * FPS))
    tmp = f"{OUT}/{name}.tmp.mp4"
    proc = None
    if frames_only is None:
        proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                 "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "19",
                                 "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", str(FPS), tmp],
                                stdin=subprocess.PIPE)
    sl = [speed_lines(i, **(speed or {})) for i in range(3)] if speed is not None else None
    base = base.convert("RGBA")
    outframes = []
    for f in range(n):
        t = f / FPS
        p = f / max(1, n - 1)
        z = zoom[0] + (zoom[1] - zoom[0]) * p
        if shake and shake[0] <= t <= shake[1]:
            amp = shake[2] * (1 - (t - shake[0]) / (shake[1] - shake[0]) * 0.6)
            ox, oy = random.uniform(-amp, amp), random.uniform(-amp, amp)
        else:
            ox = oy = 0
        cw, ch = W / z, H / z
        x0 = (W - cw) / 2 - ox
        y0 = (H - ch) / 2 - oy
        fr = base.transform((W, H), Image.EXTENT, (x0, y0, x0 + cw, y0 + ch), Image.BILINEAR)
        if sl:
            fr.alpha_composite(sl[(f // 3) % 3])
        for it in items:
            if t < it["t"]:
                continue
            im = it["img"]
            lt = t - it["t"]
            sc = 1.0
            if it.get("pop", True):
                k = min(1.0, lt / 0.25)
                sc = 0.4 + 0.6 * ease_out_back(k)
            wob = it.get("wobble", 0)
            ang = math.sin(lt * 6) * wob
            if sc != 1.0 or ang:
                im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BILINEAR)
                if ang:
                    im = im.rotate(ang, Image.BICUBIC, expand=True)
            cx, cy = it["xy"]
            fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
        if flash and f < 3:
            wh = Image.new("RGBA", (W, H), (255, 255, 255, int(255 * (1 - f / 3))))
            fr.alpha_composite(wh)
        rgb = fr.convert("RGB")
        if frames_only is not None:
            if f in frames_only:
                rgb.save(f"/home/claude/video/check_{name}_{f}.jpg", quality=85)
            continue
        proc.stdin.write(rgb.tobytes())
    if proc:
        proc.stdin.close()
        if proc.wait() == 0:
            os.replace(tmp, f"{OUT}/{name}.mp4")
        else:
            sys.exit("ffmpeg failed " + name)
    return n / FPS
