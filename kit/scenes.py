import sys, random, math
sys.path.insert(0, "/home/claude/video")
from make import *



def bill(d, x, y, ang, s=1.0):
    ca, sa = math.cos(ang), math.sin(ang)
    pts = [(-90, -45), (90, -45), (90, 45), (-90, 45)]
    P = [(x + (px * ca - py * sa) * s, y + (px * sa + py * ca) * s) for px, py in pts]
    d.poly(P, fill=(120, 200, 110), outline=(30, 90, 40), width=5)
    d.ell((x - 28 * s, y - 28 * s, x + 28 * s, y + 28 * s), fill=(200, 240, 190), outline=(30, 90, 40), width=4)
    d.text((x, y + 2 * s), "$", int(44 * s), (30, 90, 40), font=ARCH)


def monitor(d, box, kind="up", frame=(40, 44, 60)):
    x0, y0, x1, y1 = box
    d.rect(box, fill=frame, r=14, width=6)
    d.rect((x0 + 14, y0 + 14, x1 - 14, y1 - 14), fill=(12, 18, 30), outline=None, width=0, r=6)
    w, h = x1 - x0 - 40, y1 - y0 - 40
    rnd = random.Random(hash(box) & 0xffff)
    pts, v = [], 0.5
    for i in range(12):
        if kind == "up":
            v = min(0.95, max(0.05, v - rnd.uniform(-0.03, 0.12)))
        elif kind == "down":
            v = min(0.95, max(0.05, v + rnd.uniform(-0.03, 0.12)))
        else:
            v = min(0.95, max(0.05, v + rnd.uniform(-0.15, 0.15)))
        pts.append((x0 + 20 + w * i / 11, y0 + 20 + h * (1 - (1 - v))))
    col = (70, 230, 120) if kind == "up" else (255, 70, 80) if kind == "down" else (255, 200, 60)
    d.line(pts, fill=col, width=5)


def microwave(d, box):
    x0, y0, x1, y1 = box
    d.rect(box, fill=(225, 225, 215), r=12, width=6)
    d.rect((x0 + 18, y0 + 20, x0 + (x1 - x0) * 0.68, y1 - 20), fill=(50, 60, 50), r=6, width=5)
    d.rect((x1 - 70, y0 + 24, x1 - 18, y0 + 56), fill=(20, 30, 20), r=4, width=3)
    d.text((x1 - 44, y0 + 40), "0:30", 22, (120, 255, 120), font=ARCH)
    for i in range(3):
        for j in range(2):
            d.ell((x1 - 64 + j * 26, y0 + 72 + i * 26, x1 - 46 + j * 26, y0 + 90 + i * 26), fill=(180, 180, 170),
                  width=3)


def ramen(d, x, y):
    d.poly([(x - 95, y - 60), (x + 95, y - 60), (x + 70, y + 110), (x - 70, y + 110)], fill=(255, 255, 255), width=6)
    d.poly([(x - 88, y - 10), (x + 88, y - 10), (x + 82, y + 30), (x - 82, y + 30)], fill=(230, 50, 50),
           outline=None, width=0)
    d.ell((x - 95, y - 85, x + 95, y - 35), fill=(250, 220, 150), width=6)
    for i in range(3):
        d.line([(x - 40 + i * 40, y - 100), (x - 50 + i * 40, y - 150), (x - 35 + i * 40, y - 200)],
               fill=(255, 255, 255, 170), width=6)
    d.line([(x + 30, y - 70), (x + 150, y - 260)], fill=(200, 150, 90), width=10)
    d.line([(x + 50, y - 70), (x + 175, y - 250)], fill=(200, 150, 90), width=10)


def badge(text, color=(255, 220, 40)):
    t = text_block([(text, INK)], 70, font=ANTON, stroke=0, shadow=False)
    img = Image.new("RGBA", (t.width + 40, t.height + 10), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    dr.rounded_rectangle([6, 8, img.width - 1, img.height - 1], 14, fill=(0, 0, 0, 160))
    dr.rounded_rectangle([0, 0, img.width - 7, img.height - 9], 14, fill=color, outline=INK, width=6)
    img.alpha_composite(t, (17, -6))
    return img.rotate(4, Image.BICUBIC, expand=True)


def bubble(lines, size=60, tail=(-1, 1)):
    t = text_block([(l, INK) for l in lines], size, font=ARCH, stroke=0, shadow=False, maxw=760, gap=10)
    pad = 40
    bw, bh = t.width + pad * 2, t.height + pad * 2
    img = Image.new("RGBA", (bw + 20, bh + 110), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    tx = bw * 0.3 if tail[0] < 0 else bw * 0.7
    dr.polygon([(tx - 40, bh - 20), (tx + 30, bh - 20), (tx - 60 * -tail[0] * -1 + tx * 0, bh + 100)], fill=INK)
    dr.ellipse([0, 0, bw, bh], fill=(255, 255, 255), outline=INK, width=8)
    dr.polygon([(tx - 30, bh - 30), (tx + 22, bh - 30), (tx - 52 * -tail[0] * -1, bh + 82)], fill=(255, 255, 255))
    img.alpha_composite(t, (pad, pad - 6))
    return img


def sfx(text, color, size=150, ang=0, font=ANTON):
    im = text_block([(text, color)], size, font=font, stroke=12)
    return im.rotate(ang, Image.BICUBIC, expand=True)


scenes = []

# 1 HOOK -------------------------------------------------------------------
def s1():
    img = gradient((70, 20, 120), (255, 70, 140))
    halftone(img, (255, 255, 255, 40))
    d = D(img)
    rnd = random.Random(3)
    for i in range(14):
        bill(d, rnd.uniform(60, 1020), rnd.uniform(700, 1800), rnd.uniform(-0.8, 0.8), rnd.uniform(0.8, 1.3))
    kenji(img, 540, 1230, 1.0, "intense", glow_eyes=True)
    for x, y, r in [(180, 900, 50), (900, 980, 40), (840, 760, 30), (230, 1150, 35)]:
        sparkle(d, x, y, r)
    items = [
        dict(img=text_block([("HE TURNED $500", (255, 255, 255))], 130), t=0.05, xy=(540, 300)),
        dict(img=text_block([("INTO $1,000,000", (255, 225, 40))], 150), t=0.7, xy=(540, 470)),
        dict(img=text_block([("IN 30 DAYS.", (255, 255, 255))], 110), t=1.4, xy=(540, 630)),
        dict(img=caption_box(["here's how..."], 54), t=2.2, xy=(540, 1560), wobble=2),
    ]
    return finish(img), 3.4, items, dict(zoom=(1.08, 1.0), shake=(0, 0.35, 18),
                                         speed=dict(cx=540, cy=1150, color=(255, 255, 255, 150)))

# 2 MEET KENJI ---------------------------------------------------------------
def s2():
    img = gradient((15, 18, 45), (40, 40, 90))
    d = D(img)
    # window + moon
    d.rect((60, 470, 330, 760), fill=(25, 35, 80), width=8)
    d.ell((180, 510, 280, 610), fill=(255, 245, 200), outline=None, width=0)
    d.line([(195, 470), (195, 760)], width=8)
    d.line([(60, 615), (330, 615)], width=8)
    # monitors
    boxes = [(360, 470, 620, 640), (640, 470, 900, 640), (360, 660, 620, 830), (640, 660, 900, 830),
             (880, 560, 1025, 710), (60, 790, 330, 960)]
    kinds = ["up", "chaos", "down", "up", None, "chaos"]
    for b, k in zip(boxes, kinds):
        if k is None:
            microwave(d, b)
        else:
            monitor(d, b, k)
    # desk
    d.rect((-20, 1500, 1100, 1960), fill=(110, 70, 50), width=8, r=0)
    kenji(img, 540, 1280, 0.82, "neutral")
    d.rect((-20, 1560, 1100, 1960), fill=(110, 70, 50), width=8, r=0)
    ramen(d, 830, 1600)
    # monitor glow overlay
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    D(lay).ell((140, 700, 940, 1500), fill=(80, 200, 255, 35), outline=None, width=0)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(80)))
    arrow = Image.new("RGBA", (420, 230), (0, 0, 0, 0))
    ad = ImageDraw.Draw(arrow)
    ad.line([(60, 40), (330, 190)], fill=(255, 225, 40), width=14)
    ad.polygon([(330, 190), (275, 195), (310, 150)], fill=(255, 225, 40))
    items = [
        dict(img=badge("MEET KENJI."), t=0.1, xy=(540, 250)),
        dict(img=caption_box(["3AM. Instant ramen.", "Six monitors."], 58), t=0.8, xy=(540, 1730)),
        dict(img=arrow, t=2.2, xy=(800, 470), pop=False),
        dict(img=caption_box(["(one is a microwave)"], 44, bg=(255, 225, 40)), t=2.2, xy=(620, 380), wobble=3),
    ]
    return finish(img), 4.4, items, dict(zoom=(1.0, 1.06))

# 3 DAY 1 --------------------------------------------------------------------
def s3():
    img = gradient((20, 60, 70), (20, 120, 110))
    halftone(img, (255, 255, 255, 30))
    d = D(img)
    # big monitor with dragon chart
    d.rect((90, 500, 990, 1100), fill=(40, 44, 60), r=20, width=8)
    d.rect((115, 525, 965, 1075), fill=(10, 16, 28), r=10, width=0, outline=None)
    for gy in range(560, 1060, 70):
        d.line([(130, gy), (950, gy)], fill=(30, 50, 60), width=2)
    pts = []
    for i in range(41):
        x = 150 + i * 17.5
        y = 1000 - i * 9 + math.sin(i * 0.55) * 70
        pts.append((x, y))
    d.line(pts, fill=(70, 240, 120), width=12)
    hx, hy = pts[-1]
    # dragon head
    d.poly([(hx - 30, hy + 30), (hx + 40, hy - 50), (hx + 120, hy - 40), (hx + 70, hy + 10), (hx + 115, hy + 40),
            (hx + 20, hy + 55)], fill=(70, 240, 120), width=6)
    d.poly([(hx + 40, hy - 45), (hx + 20, hy - 110), (hx + 70, hy - 50)], fill=(255, 225, 40), width=5)
    d.ell((hx + 50, hy - 35, hx + 72, hy - 13), fill=(255, 60, 60), width=4)
    d.poly([(hx + 115, hy + 30), (hx + 170, hy + 5), (hx + 150, hy + 45), (hx + 190, hy + 50), (hx + 120, hy + 50)],
           fill=(255, 140, 40), outline=(255, 60, 40), width=4)
    kenji(img, 300, 1520, 0.62, "smug")
    items = [
        dict(img=badge("DAY 1"), t=0.05, xy=(250, 270)),
        dict(img=caption_box(["Strategy: vibes only."], 56), t=0.4, xy=(600, 400)),
        dict(img=bubble(["This chart looks", "like a DRAGON."], 54, tail=(-1, 1)), t=1.1, xy=(700, 1300), wobble=2),
        dict(img=sfx("+200%", (90, 255, 130), 190, 8), t=2.6, xy=(760, 700), wobble=4),
    ]
    return finish(img), 4.4, items, dict(zoom=(1.0, 1.05))

# 4 DAY 7 GENIUS -------------------------------------------------------------
def s4():
    img = gradient((255, 170, 30), (255, 80, 40))
    d = D(img)
    kenji(img, 540, 1180, 1.05, "shout")
    for x, y, r in [(150, 800, 60), (930, 850, 45), (880, 1350, 35), (170, 1300, 40)]:
        sparkle(d, x, y, r)
    items = [
        dict(img=text_block([("I AM A", (255, 255, 255)), ("FINANCIAL GENIUS!!", (255, 240, 60))], 140), t=0.1,
             xy=(540, 400), wobble=2),
        dict(img=badge("DAY 7", (255, 255, 255)), t=1.0, xy=(200, 1520)),
        dict(img=caption_box(["Quits his job. By email.", "In ALL CAPS."], 54), t=1.3, xy=(560, 1700)),
    ]
    return finish(img), 4.2, items, dict(zoom=(1.0, 1.08), shake=(0.1, 0.9, 14),
                                         speed=dict(cx=540, cy=1150, color=(255, 255, 220, 170)))

# 5 DAY 14 AURA --------------------------------------------------------------
def s5():
    img = gradient((40, 20, 70), (120, 40, 140))
    d = D(img)
    # aura flames
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ld = D(lay)
    rnd = random.Random(9)
    for layer, (col, R) in enumerate([((255, 200, 40, 200), 560), ((255, 240, 140, 220), 470)]):
        pts = []
        for i in range(29):
            a = math.radians(180 + i * (180 / 28))
            rr = R * (1.35 if i % 2 else 1.0) + rnd.uniform(-30, 30)
            pts.append((540 + math.cos(a) * rr * 0.75, 1150 + math.sin(a) * rr))
        pts += [(540 + R * 0.75, 1900), (540 - R * 0.75, 1900)]
        ld.poly(pts, fill=col, outline=None, width=0)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(10)))
    kenji(img, 540, 1200, 0.95, "smug", outfit="hoodie")
    for x, y, r in [(160, 700, 50), (920, 760, 60), (130, 1150, 35), (960, 1250, 40), (300, 520, 30)]:
        sparkle(d, x, y, r, fill=(255, 250, 200))
    items = [
        dict(img=badge("DAY 14"), t=0.05, xy=(250, 270)),
        dict(img=caption_box(["His aura is now visible."], 56), t=0.4, xy=(580, 410)),
        dict(img=sfx("+4,000%", (90, 255, 130), 200, -6), t=1.7, xy=(540, 640), wobble=4),
    ]
    return finish(img), 4.2, items, dict(zoom=(1.0, 1.06))

# 6 DAY 29 ALL IN ------------------------------------------------------------
def s6():
    img = gradient((20, 0, 10), (140, 10, 30))
    halftone(img, (255, 60, 80, 70), spacing=30, rmax=10)
    d = D(img)
    kenji(img, 540, 1250, 1.45, "intense", glow_eyes=True)
    items = [
        dict(img=badge("DAY 29", (255, 80, 90)), t=0.05, xy=(250, 260)),
        dict(img=caption_box(["He puts EVERYTHING", "on one trade."], 56), t=0.4, xy=(580, 430)),
        dict(img=sfx("ゴ", (200, 120, 255), 170, -12, font=CJK), t=1.2, xy=(130, 820), wobble=6),
        dict(img=sfx("ゴ", (200, 120, 255), 150, 10, font=CJK), t=1.35, xy=(960, 900), wobble=6),
        dict(img=sfx("ゴ", (200, 120, 255), 130, -6, font=CJK), t=1.5, xy=(120, 1100), wobble=6),
        dict(img=sfx("ALL IN.", (255, 255, 255), 230, 0), t=2.2, xy=(540, 1650)),
    ]
    return finish(img), 4.4, items, dict(zoom=(1.0, 1.12), shake=(2.2, 2.8, 16),
                                         speed=dict(cx=540, cy=1200, color=(0, 0, 0, 120), inner=520))

# 7 CRASH --------------------------------------------------------------------
def s7():
    img = gradient((60, 70, 90), (25, 30, 45))
    d = D(img)
    d.rect((90, 440, 990, 900), fill=(40, 44, 60), r=20, width=8)
    d.rect((115, 465, 965, 875), fill=(10, 16, 28), r=10, width=0, outline=None)
    pts = [(150, 540), (300, 520), (420, 500), (520, 480), (560, 470)]
    pts += [(600, 820), (700, 840), (800, 850), (930, 855)]
    d.line(pts, fill=(255, 60, 70), width=12)
    kenji(img, 540, 1300, 0.95, "shock")
    sweat(d, 830, 1080, 1.4)
    sweat(d, 250, 1150, 1.0)
    # desaturate figure a touch
    items = [
        dict(img=sfx("-99.8%", (255, 60, 70), 230, -4), t=0.15, xy=(540, 300), wobble=3),
        dict(img=caption_box(["The chart...", "was not a dragon."], 58), t=1.7, xy=(560, 1720)),
    ]
    return finish(img), 4.4, items, dict(zoom=(1.0, 1.04), shake=(0.15, 1.0, 22))

# 8 TWIST --------------------------------------------------------------------
def s8():
    img = gradient((15, 15, 30), (35, 30, 60))
    d = D(img)
    # screen behind
    d.rect((80, 470, 1000, 960), fill=(250, 250, 255), r=10, width=8)
    d.text((540, 560), "MASTERCLASS", 70, (230, 40, 60), font=ANTON)
    d.text((540, 670), "HOW I LOST IT ALL", 82, INK, font=ANTON)
    d.text((540, 800), "ONLY $997", 96, (40, 160, 80), font=ANTON, stroke=0)
    d.line([(350, 870), (730, 870)], fill=(230, 40, 60), width=6)
    # spotlight
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    D(lay).poly([(470, 0), (610, 0), (980, 1920), (100, 1920)], fill=(255, 250, 220, 55), outline=None, width=0)
    img.alpha_composite(lay.filter(ImageFilter.GaussianBlur(25)))
    kenji(img, 540, 1340, 0.85, "joy", outfit="suit")
    # mic
    d.line([(760, 1500), (720, 1330)], fill=(60, 60, 70), width=14)
    d.ell((690, 1270, 750, 1340), fill=(120, 120, 130), width=6)
    for x, y, r in [(150, 1150, 40), (930, 1200, 50)]:
        sparkle(d, x, y, r)
    items = [
        dict(img=badge("DAY 30"), t=0.05, xy=(250, 280)),
        dict(img=caption_box(["Kenji IS a millionaire now."], 54), t=0.35, xy=(580, 400)),
        dict(img=caption_box(["...from selling a course", "about losing money."], 56, bg=(255, 225, 40)), t=2.0,
             xy=(540, 1720), wobble=2),
    ]
    return finish(img), 5.0, items, dict(zoom=(1.0, 1.05))

# 9 END ----------------------------------------------------------------------
def s9():
    img = gradient((70, 20, 120), (20, 10, 40))
    halftone(img, (255, 255, 255, 30))
    d = D(img)
    kenji(img, 540, 1400, 0.7, "smug")
    items = [
        dict(img=text_block([("PART 2:", (255, 225, 40)), ("KENJI DISCOVERS", (255, 255, 255)),
                             ("CRYPTO", (90, 255, 130))], 130), t=0.1, xy=(540, 480)),
        dict(img=caption_box(["FOLLOW so you don't miss it"], 52, bg=(255, 70, 110), fg=(255, 255, 255)), t=1.0,
             xy=(540, 860), wobble=3),
        dict(img=text_block([("not financial advice. obviously.", (230, 230, 240))], 46, font=ARCH, stroke=4,
                            shadow=False), t=1.6, xy=(540, 1050), pop=False),
    ]
    return finish(img), 3.4, items, dict(zoom=(1.0, 1.04))


if __name__ == '__main__':
    CHECK = '--check' in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    ALL = [("s1", s1), ("s2", s2), ("s3", s3), ("s4", s4), ("s5", s5), ("s6", s6), ("s7", s7), ("s8", s8), ("s9", s9)]
    total = 0
    for name, fn in ALL:
        if only and name not in only:
            continue
        base, dur, items, kw = fn()
        if CHECK:
            render_scene(name, base, dur, items, frames_only={int(dur * FPS) - 5}, **kw)
        else:
            total += render_scene(name, base, dur, items, **kw)
        print(name, dur, flush=True)
    print("total", total)
