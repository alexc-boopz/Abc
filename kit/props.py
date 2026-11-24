import math, random, sys
sys.path.insert(0, "/home/claude/video")
from make import *

Y = (255, 225, 40)
G = (90, 255, 130)
R = (255, 60, 70)
WH = (255, 255, 255)
CAT = (250, 236, 215)
CAT_SH = (230, 205, 175)


# ---------------------------------------------------------------- text items
def T(lines, size, t, y, x=540, wob=0, pop=True):
    return dict(img=text_block(lines, size), t=t, xy=(x, y), wobble=wob, pop=pop)


def C(lines, t, y, size=56, bg=WH, fg=INK, x=540, wob=0):
    return dict(img=caption_box(lines, size, bg=bg, fg=fg), t=t, xy=(x, y), wobble=wob)


def B(text, t, xy=(250, 260), color=Y):
    tb = text_block([(text, INK)], 70, font=ANTON, stroke=0, shadow=False)
    img = Image.new("RGBA", (tb.width + 40, tb.height + 10), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    dr.rounded_rectangle([6, 8, img.width - 1, img.height - 1], 14, fill=(0, 0, 0, 160))
    dr.rounded_rectangle([0, 0, img.width - 7, img.height - 9], 14, fill=color, outline=INK, width=6)
    img.alpha_composite(tb, (17, -6))
    return dict(img=img.rotate(4, Image.BICUBIC, expand=True), t=t, xy=xy)


def X(text, color, size, t, xy, ang=0, wob=4, font=ANTON):
    im = text_block([(text, color)], size, font=font, stroke=12).rotate(ang, Image.BICUBIC, expand=True)
    return dict(img=im, t=t, xy=xy, wobble=wob)


def BU(lines, t, xy, size=52, tail="left"):
    tb = text_block([(l, INK) for l in lines], size, font=ARCH, stroke=0, shadow=False, maxw=720, gap=10)
    pad = 44
    bw, bh = tb.width + pad * 2, tb.height + pad * 2
    img = Image.new("RGBA", (bw + 10, bh + 100), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    tx = bw * 0.3 if tail == "left" else bw * 0.7
    tip = tx - 50 if tail == "left" else tx + 50
    dr.polygon([(tx - 40, bh - 30), (tx + 40, bh - 30), (tip, bh + 95)], fill=INK)
    dr.ellipse([0, 0, bw, bh], fill=WH, outline=INK, width=8)
    dr.polygon([(tx - 30, bh - 36), (tx + 30, bh - 36), (tip, bh + 78)], fill=WH)
    img.alpha_composite(tb, (pad, pad - 6))
    return dict(img=img, t=t, xy=xy, wobble=2)


# ---------------------------------------------------------------- props
def cat(img, cx, cy, s=1.0, expr="neutral", acc=()):
    d = D(img)
    P = lambda x, y: (cx + x * s, cy + y * s)
    lw = max(4, int(7 * s))
    # tail
    d.line([P(150, 120), P(260, 60), P(280, -60), P(240, -120)], fill=INK, width=int(34 * s) + 8)
    d.line([P(150, 120), P(260, 60), P(280, -60), P(240, -120)], fill=CAT, width=int(34 * s))
    # body
    d.ell((*P(-170, -10), *P(170, 230)), fill=CAT, width=lw)
    d.ell((*P(-80, 80), *P(80, 220)), fill=WH, outline=None, width=0)
    for sx in (-1, 1):
        d.ell((*P(sx * 90 - 45, 180), *P(sx * 90 + 45, 240)), fill=CAT, width=lw)
    # ears
    for sx in (-1, 1):
        d.poly([P(sx * 60, -200), P(sx * 150, -290), P(sx * 150, -150)], fill=CAT, width=lw)
        d.poly([P(sx * 85, -195), P(sx * 138, -255), P(sx * 138, -175)], fill=(255, 170, 180), outline=None, width=0)
    # head
    d.ell((*P(-165, -250), *P(165, 40)), fill=CAT, width=lw)
    # patch
    d.ell((*P(30, -235), *P(140, -140)), fill=(235, 160, 90), outline=None, width=0)
    ey = -110
    if expr in ("neutral", "stare"):
        for sx in (-1, 1):
            d.ell((*P(sx * 65 - 26, ey - 32), *P(sx * 65 + 26, ey + 32)), fill=(120, 190, 90), width=lw - 2)
            d.ell((*P(sx * 65 - 7, ey - 26), *P(sx * 65 + 7, ey + 26)), fill=INK, outline=None, width=0)
            if expr == "stare":
                d.line([P(sx * 65 - 32, ey - 18), P(sx * 65 + 32, ey - 18)], width=lw + 2)
    elif expr == "happy":
        for sx in (-1, 1):
            d.arc((*P(sx * 65 - 30, ey - 15), *P(sx * 65 + 30, ey + 35)), 200, 340, width=lw + 2)
    elif expr == "smug":
        for sx in (-1, 1):
            d.ell((*P(sx * 65 - 26, ey - 22), *P(sx * 65 + 26, ey + 26)), fill=(120, 190, 90), width=lw - 2)
            d.poly([P(sx * 65 - 32, ey - 30), P(sx * 65 + 32, ey - 30), P(sx * 65 + 32, ey), P(sx * 65 - 32, ey)],
                   fill=CAT, outline=None, width=0)
            d.line([P(sx * 65 - 30, ey), P(sx * 65 + 30, ey)], width=lw + 2)
    # nose & mouth
    d.poly([P(-12, -55), P(12, -55), P(0, -42)], fill=(255, 130, 150), width=3)
    d.arc((*P(-24, -50), *P(2, -20)), 0, 160, width=lw - 2)
    d.arc((*P(-2, -50), *P(24, -20)), 20, 180, width=lw - 2)
    for sy in (-60, -40):
        d.line([P(-70, sy), P(-160, sy - 12)], width=3)
        d.line([P(70, sy), P(160, sy - 12)], width=3)
    if "glasses" in acc:
        for sx in (-1, 1):
            d.rect((*P(sx * 65 - 50, ey - 30), *P(sx * 65 + 50, ey + 30)), fill=(20, 20, 30), r=int(14 * s), width=lw - 2)
        d.line([P(-15, ey - 10), P(15, ey - 10)], width=lw)
        d.line([P(-150, ey - 15), P(-115, ey - 15)], width=lw)
        d.line([P(115, ey - 15), P(150, ey - 15)], width=lw)
    if "crown" in acc:
        d.poly([P(-80, -230), P(-80, -300), P(-40, -260), P(0, -320), P(40, -260), P(80, -300), P(80, -230)],
               fill=Y, width=lw)
    if "tie" in acc:
        d.poly([P(-22, 40), P(22, 40), P(32, 150), P(0, 180), P(-32, 150)], fill=(230, 40, 60), width=lw - 2)


def coin(img, cx, cy, r, label="$MOCHI"):
    d = D(img)
    d.ell((cx - r, cy - r + 14, cx + r, cy + r + 14), fill=(180, 120, 10), width=8)
    d.ell((cx - r, cy - r, cx + r, cy + r), fill=(255, 200, 40), width=8)
    d.ell((cx - r * 0.78, cy - r * 0.78, cx + r * 0.78, cy + r * 0.78), fill=(255, 220, 90), outline=(200, 140, 20), width=5)
    s = r / 260
    cat(img, cx, cy + 40 * s, 0.55 * s * 1.0, "happy")
    d.text((cx, cy + r * 0.6), label, int(44 * s), INK, font=ANTON)


def rocket(img, cx, cy, s=1.0):
    d = D(img)
    P = lambda x, y: (cx + x * s, cy + y * s)
    d.poly([P(-40, 160), P(0, 330), P(40, 160)], fill=(255, 150, 40), outline=None, width=0)
    d.poly([P(-22, 160), P(0, 260), P(22, 160)], fill=(255, 240, 120), outline=None, width=0)
    d.poly([P(-70, 60), P(-130, 170), P(-60, 160)], fill=(230, 40, 60), width=6)
    d.poly([P(70, 60), P(130, 170), P(60, 160)], fill=(230, 40, 60), width=6)
    d.poly([P(0, -220), P(70, -90), P(70, 160), P(-70, 160), P(-70, -90)], fill=(240, 240, 250), width=7)
    d.ell((*P(-36, -60), *P(36, 12)), fill=(80, 180, 255), width=6)


def car(img, cx, cy, s=1.0, color=(255, 200, 30)):
    d = D(img)
    P = lambda x, y: (cx + x * s, cy + y * s)
    d.poly([P(-330, 40), P(-300, -20), P(-120, -50), P(-40, -120), P(150, -120), P(260, -40), P(330, -20),
            P(340, 50), P(-330, 60)], fill=color, width=7)
    d.poly([P(-20, -105), P(140, -105), P(220, -45), P(-90, -45)], fill=(60, 80, 110), width=5)
    for x in (-200, 200):
        d.ell((*P(x - 62, -5), *P(x + 62, 119)), fill=(30, 30, 40), width=7)
        d.ell((*P(x - 28, 29), *P(x + 28, 85)), fill=(170, 170, 180), width=4)


def keyboard(img, x0, y0, x1, y1):
    d = D(img)
    d.rect((x0, y0, x1, y1), fill=(60, 64, 80), r=14, width=6)
    cols, rows = 12, 4
    kw = (x1 - x0 - 30) / cols
    kh = (y1 - y0 - 30) / rows
    for r_ in range(rows):
        for c in range(cols):
            kx, ky = x0 + 15 + c * kw, y0 + 15 + r_ * kh
            d.rect((kx + 3, ky + 3, kx + kw - 3, ky + kh - 3), fill=(210, 212, 222), r=5, width=3)


def box(img, x, y, w, h):
    d = D(img)
    d.rect((x, y, x + w, y + h), fill=(205, 155, 95), width=5)
    d.line([(x + w / 2, y), (x + w / 2, y + h * 0.35)], fill=(240, 220, 170), width=int(w * 0.12))
    d.line([(x + 10, y + h * 0.65), (x + w * 0.45, y + h * 0.65)], fill=(120, 80, 40), width=4)


def brick_phone(img, cx, cy, s=1.0):
    d = D(img)
    P = lambda x, y: (cx + x * s, cy + y * s)
    d.rect((*P(-110, -200), *P(110, 200)), fill=(180, 70, 50), r=int(12 * s), width=7)
    for yy in range(-150, 200, 70):
        d.line([P(-110, yy), P(110, yy)], fill=(140, 50, 40), width=4)
    d.rect((*P(-80, -160), *P(80, 120)), fill=(20, 20, 30, 230), r=int(10 * s), width=5)
    d.text(P(0, -20), "51", int(80 * s), WH, font=ANTON)
    d.ell((*P(-20, 140), *P(20, 180)), fill=(60, 60, 70), width=4)


def tuna(img, cx, cy, s=1.0):
    d = D(img)
    P = lambda x, y: (cx + x * s, cy + y * s)
    d.ell((*P(-120, 30), *P(120, 90)), fill=(170, 170, 185), width=6)
    d.rect((*P(-120, -40), *P(120, 60)), fill=(80, 140, 220), width=0, outline=None)
    d.line([P(-120, -40), P(-120, 60)], width=6)
    d.line([P(120, -40), P(120, 60)], width=6)
    d.ell((*P(-120, -70), *P(120, -10)), fill=(200, 200, 210), width=6)
    d.text(P(0, 18), "TUNA", int(50 * s), WH, font=ANTON)


def laptop(img, cx, cy, s=1.0, screen=None):
    d = D(img)
    P = lambda x, y: (cx + x * s, cy + y * s)
    d.rect((*P(-260, -320), *P(260, 0)), fill=(50, 54, 70), r=int(16 * s), width=7)
    d.rect((*P(-235, -295), *P(235, -25)), fill=(245, 245, 250), r=int(6 * s), width=0, outline=None)
    d.poly([P(-310, 0), P(310, 0), P(340, 40), P(-340, 40)], fill=(160, 165, 180), width=7)
    if screen:
        screen(d, P)


def big_button(img, cx, cy, r, label, color=(230, 40, 60)):
    d = D(img)
    d.ell((cx - r - 30, cy - r * 0.45 + 40, cx + r + 30, cy + r * 0.45 + 70), fill=(60, 60, 70), width=7)
    d.ell((cx - r, cy - r * 0.45 + 20, cx + r, cy + r * 0.45 + 50), fill=(150, 20, 30), width=7)
    d.ell((cx - r, cy - r * 0.45, cx + r, cy + r * 0.45), fill=color, width=7)
    d.text((cx, cy), label, int(r * 0.38), WH, font=ANTON, stroke=3)


def glow_dot(img, cx, cy, r, color=(255, 30, 40)):
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    D(lay).ell((cx - r * 3, cy - r * 3, cx + r * 3, cy + r * 3), fill=color + (120,), outline=None, width=0)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(30)))
    D(img).ell((cx - r, cy - r, cx + r, cy + r), fill=(255, 220, 220), outline=None, width=0)


def vase(img, cx, cy, s=1.0, ang=0):
    lay = Image.new("RGBA", (int(400 * K * s), int(500 * K * s)), (0, 0, 0, 0))
    d = D(lay)
    w, h = 400 * s, 500 * s
    c = w / 2
    d.poly([(c - 60 * s, 40 * s), (c + 60 * s, 40 * s), (c + 50 * s, 100 * s), (c + 130 * s, 250 * s),
            (c + 90 * s, 440 * s), (c - 90 * s, 440 * s), (c - 130 * s, 250 * s), (c - 50 * s, 100 * s)],
           fill=(90, 160, 230), width=7)
    d.line([(c - 120 * s, 250 * s), (c + 120 * s, 250 * s)], fill=(255, 255, 255), width=10)
    lay = lay.rotate(ang, Image.BICUBIC, expand=True)
    img.alpha_composite(lay, (int(cx * K - lay.width / 2), int(cy * K - lay.height / 2)))


def money_pile(img, cx, cy, s=1.0):
    d = D(img)
    rnd = random.Random(int(cx + cy))
    for i in range(18):
        x = cx + rnd.uniform(-260, 260) * s
        y = cy + rnd.uniform(-40, 90) * s
        ang = rnd.uniform(-0.5, 0.5)
        ca, sa = math.cos(ang), math.sin(ang)
        pts = [(-80, -40), (80, -40), (80, 40), (-80, 40)]
        Pt = [(x + (px * ca - py * sa) * s, y + (px * sa + py * ca) * s) for px, py in pts]
        d.poly(Pt, fill=(120, 200, 110), outline=(30, 90, 40), width=4)
        d.text((x, y), "$", int(40 * s), (30, 90, 40), font=ARCH)


def chart_monitor(img, box_, kind="up", seed=1, label=None):
    d = D(img)
    x0, y0, x1, y1 = box_
    d.rect(box_, fill=(40, 44, 60), r=18, width=8)
    d.rect((x0 + 22, y0 + 22, x1 - 22, y1 - 22), fill=(10, 16, 28), r=8, width=0, outline=None)
    rnd = random.Random(seed)
    n = 30
    pts = []
    for i in range(n):
        p = i / (n - 1)
        if kind == "up":
            v = 0.85 - 0.7 * p ** 2 + rnd.uniform(-0.04, 0.04)
        elif kind == "down":
            v = 0.15 + 0.75 * p ** 0.5 + rnd.uniform(-0.03, 0.03)
        elif kind == "crash":
            v = (0.8 - 0.65 * (p / 0.7)) if p < 0.7 else 0.92
            v += rnd.uniform(-0.02, 0.02)
        else:
            v = 0.5 + rnd.uniform(-0.3, 0.3)
        pts.append((x0 + 40 + (x1 - x0 - 80) * p, y0 + 40 + (y1 - y0 - 80) * v))
    col = G if kind == "up" else R if kind in ("down", "crash") else Y
    d.line(pts, fill=col, width=12)
    if label:
        d.text((x0 + 150, y0 + 75), label, 46, WH, font=ANTON)


# ---------------------------------------------------------------- scene factory
def scene(bg, dur=4.4, ht=None, kenji_=None, props=None, front=None, items=(), fx=None):
    def fn():
        img = gradient(*bg)
        if ht:
            halftone(img, ht)
        if props:
            props(img)
        if kenji_:
            kenji(img, **kenji_)
        if front:
            front(img)
        return finish(img), dur, list(items), dict(fx or {})
    return fn


def endcard(next_lines, dur=4.4, mochi=False):
    def props(img):
        if mochi:
            cat(img, 820, 1450, 0.6, "smug", acc=("glasses",))
    return scene(((70, 20, 120), (20, 10, 40)), dur, ht=(255, 255, 255, 30),
                 kenji_=dict(cx=380 if mochi else 540, cy=1420, s=0.65, expr="smug"), props=None, front=props,
                 items=[T(next_lines, 120, 0.1, 470),
                        C(["FOLLOW so you don't miss it"], 0.9, 880, 52, bg=(255, 70, 110), fg=WH, wob=3),
                        dict(img=text_block([("not financial advice. obviously.", (230, 230, 240))], 46, font=ARCH,
                                            stroke=4, shadow=False), t=1.5, xy=(540, 1060), pop=False)])
