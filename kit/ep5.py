import sys
sys.path.insert(0, "/home/claude/video")
from safe import *
from run_ep import run

D45 = 4.5
SL = lambda cx=465, cy=1150, c=(255, 255, 255, 150), inner=380: dict(cx=cx, cy=cy, color=c, inner=inner)
WOOD, WOOD_D = (150, 95, 55), (105, 62, 35)


def wood_wall(img):
    d = D(img)
    for x in range(-40, 1100, 180):
        d.rect((x, 0, x + 170, 1250), fill=(125, 80, 45), width=4, outline=WOOD_D)


def bench(img, x0, y0, x1, y1, label=None):
    d = D(img)
    d.rect((x0, y0, x1, y1), fill=WOOD, width=7)
    d.rect((x0 - 20, y0 - 30, x1 + 20, y0 + 10), fill=WOOD_D, width=7)
    for x in range(x0 + 40, x1 - 60, 160):
        d.rect((x, y0 + 50, x + 110, y1 - 40), fill=None, outline=WOOD_D, width=5)
    if label:
        d.text(((x0 + x1) / 2, y0 + 90), label, 44, (255, 225, 140), font=ANTON)


def gavel(img, cx, cy, s=1.0, ang=-30):
    d = D(img)
    a = math.radians(ang)
    R = lambda x, y: (cx + (x * math.cos(a) - y * math.sin(a)) * s, cy + (x * math.sin(a) + y * math.cos(a)) * s)
    d.poly([R(-12, 0), R(12, 0), R(12, 230), R(-12, 230)], fill=WOOD)
    d.poly([R(-90, -50), R(90, -50), R(90, 40), R(-90, 40)], fill=WOOD_D)
    d.poly([R(-100, -55), R(-80, -55), R(-80, 45), R(-100, 45)], fill=(220, 180, 60))
    d.poly([R(80, -55), R(100, -55), R(100, 45), R(80, 45)], fill=(220, 180, 60))


def paper(img, cx, cy, w, h, title, lines=3, sign=None, ang=0):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = D(layer)
    x0, y0 = cx - w / 2, cy - h / 2
    d.rect((x0, y0, x0 + w, y0 + h), fill=(250, 248, 238), width=6)
    d.text((cx, y0 + 60), title, 46, INK, font=ANTON)
    for i in range(lines):
        d.line([(x0 + 40, y0 + 130 + i * 44), (x0 + w - 40, y0 + 130 + i * 44)], fill=(160, 160, 170), width=4)
    if sign:
        d.text((cx, y0 + h - 60), sign, 40, (40, 60, 200), font=ARCH)
    if ang:
        layer = layer.rotate(ang, Image.BICUBIC, center=(cx * 2, cy * 2))
    img.alpha_composite(layer)


def paw(d, cx, cy, s=1.0, col=(200, 60, 80)):
    d.ell((cx - 40 * s, cy - 20 * s, cx + 40 * s, cy + 50 * s), fill=col, width=0)
    for dx, dy in [(-48, -45), (-17, -70), (17, -70), (48, -45)]:
        d.ell((cx + (dx - 15) * s, cy + (dy - 18) * s, cx + (dx + 15) * s, cy + (dy + 18) * s), fill=col, width=0)


def p_hook(img):
    wood_wall(img)
    bench(img, -40, 1300, 1120, 1960)
    gavel(img, 820, 1180, 1.1)


def p_recap(img):
    brick_phone(img, 260, 1150, 0.9)
    cat(img, 700, 1250, 0.5, "smug", acc=("glasses", "tie"))
    paper(img, 700, 1480, 260, 150, "50%", lines=0)


def p_file(img):
    paper(img, 465, 1120, 520, 560, "KENJI v. MOCHI", lines=6, ang=-4)


def p_lawyer(img):
    d = D(img)
    d.rect((480, 520, 900, 900), fill=(30, 40, 60), width=7, r=14)
    d.text((690, 610), "ATTORNEY", 50, (220, 190, 110), font=ANTON)
    d.text((690, 760), "$900/HR", 96, (255, 90, 90), font=ANTON)


def p_court(img):
    wood_wall(img)
    bench(img, 140, 780, 940, 1150, "THE HONORABLE COURT")
    bench(img, -40, 1450, 1120, 1960)
    cat(img, 520, 1310, 0.5, "smug", acc=("glasses", "tie"))
    for x in (180, 760, 900):
        cat(img, x, 1360, 0.32, "stare", acc=("tie",))


def p_exhibit_a(img):
    bench(img, -40, 1280, 1120, 1960)
    paper(img, 360, 1180, 320, 230, "EXHIBIT A", lines=2, ang=12)
    cat(img, 700, 1160, 0.55, "neutral", acc=("tie",))


def p_exhibit_b(img):
    paper(img, 465, 1030, 600, 620, "INTERN CONTRACT", lines=5, sign="signed: Kenji")
    d = D(img)
    paw(d, 690, 1170, 0.7)
    d.text((465, 940), "ALL PROFITS", 48, (200, 40, 60), font=ANTON)
    d.text((465, 1000), "GO TO THE CAT", 48, (200, 40, 60), font=ANTON)


def p_verdict(img):
    wood_wall(img)
    bench(img, -40, 1300, 1120, 1960)
    gavel(img, 700, 1150, 1.0, ang=10)


def p_live(img):
    d = D(img)
    d.rect((110, 420, 820, 1000), fill=(20, 20, 30), width=8, r=20)
    d.rect((140, 450, 790, 970), fill=(150, 95, 55), width=0)
    cat(img, 465, 820, 0.45, "smug", acc=("glasses", "tie"))
    d.rect((150, 465, 300, 525), fill=(230, 30, 50), width=0, r=10)
    d.text((225, 495), "LIVE", 40, WH, font=ANTON)
    for i, (x, y) in enumerate([(160, 1080), (470, 1120), (760, 1070)]):
        d.ell((x - 50, y - 50, x + 50, y + 50), fill=(255, 80, 110), width=5)
        d.text((x, y + 2), ["LOL", "!!", "LOL"][i], 34, WH, font=ANTON)


def p_show(img):
    d = D(img)
    d.rect((60, 330, 870, 560), fill=(255, 200, 40), width=8, r=20)
    d.text((465, 445), "JUDGE MOCHI", 110, INK, font=ANTON)
    bench(img, 140, 980, 900, 1300)
    cat(img, 520, 900, 0.55, "smug", acc=("crown", "glasses"))
    gavel(img, 760, 960, 0.6)


scenes = [
    scene(((40, 15, 10), (140, 70, 30)), 4.0, ht=(255, 255, 255, 40), props=p_hook,
          kenji_=dict(cx=420, cy=1100, s=0.9, expr="intense", outfit="suit", glow_eyes=True),
          items=[TS([("HE SUED", WH), ("HIS OWN CAT.", Y)], 140, 0.05, 330), TS([("AND LOST.", R)], 130, 0.9, 640),
                 CS(["here's how..."], 2.2, 1480, 50, wob=2)],
          fx=dict(zoom=(1.08, 1.0), shake=(0, 0.35, 18), speed=SL(cy=1100))),
    scene(((230, 235, 245), (170, 180, 200)), D45, props=p_recap,
          items=[B("LAST TIME", 0.05), CS(["Sold 10,000 bricks.", "Mochi took 50%."], 0.4, 460, 52)]),
    scene(((235, 225, 205), (200, 185, 160)), D45, props=p_file,
          front=lambda img: kenji(img, 220, 1520, 0.42, "shout", outfit="suit"),
          items=[B("DAY 1", 0.05), CS(["Kenji wants his 50% back."], 0.4, 430, 50),
                 XS("SUED.", R, 150, 1.8, (640, 1420), ang=-8)]),
    scene(((20, 30, 50), (50, 70, 110)), D45, props=p_lawyer, kenji_=dict(cx=280, cy=1350, s=0.62, expr="smug", outfit="suit"),
          items=[B("DAY 2", 0.05, color=WH), BS(["I'll represent", "myself."], 1.2, (330, 1000), 44),
                 CS(["(3 law videos at 2x speed)"], 2.5, 1480, 44, bg=Y)]),
    scene(((90, 55, 30), (50, 30, 15)), D45, props=p_court,
          items=[B("DAY 14", 0.05, color=WH), CS(["Mochi shows up with", "4 lawyers."], 0.4, 450, 50),
                 CS(["(all cats)"], 2.0, 640, 50, bg=Y)]),
    scene(((255, 170, 30), (255, 80, 40)), D45, kenji_=dict(cx=465, cy=1250, s=1.0, expr="shout", outfit="suit"),
          items=[XS("OBJECTION!!", WH, 160, 0.2, (465, 380), ang=-5),
                 BS(["Judge: to what?"], 1.6, (300, 640), 44),
                 BS(["...vibes."], 2.8, (640, 820), 50, tail="right")],
          fx=dict(zoom=(1.0, 1.08), shake=(0.2, 0.9, 14), speed=SL())),
    scene(((230, 220, 200), (180, 160, 130)), D45, props=p_exhibit_a,
          items=[CS(["Exhibit A: the contract."], 0.2, 380, 50),
                 XS("*swipe*", WH, 120, 1.4, (330, 860), ang=10),
                 CS(["Evidence: on the floor."], 2.5, 600, 50, bg=Y)],
          fx=dict(shake=(1.4, 1.8, 16))),
    scene(((20, 0, 10), (90, 10, 60)), D45, ht=(200, 60, 255, 60),
          kenji_=dict(cx=465, cy=1250, s=1.3, expr="intense", outfit="suit", glow_eyes=True),
          items=[BS(["Your Honor...", "he's a CAT.", "He can't even READ."], 0.4, (465, 480), 44)],
          fx=dict(zoom=(1.0, 1.1), speed=SL(c=(0, 0, 0, 110), inner=520))),
    scene(((235, 225, 205), (200, 185, 160)), D45, props=p_exhibit_b,
          items=[CS(["Mochi's lawyers present", "Exhibit B."], 0.2, 380, 48),
                 CS(["Kenji signed it as an intern."], 2.2, 1470, 44, bg=Y)]),
    scene(((60, 70, 90), (25, 30, 45)), D45, props=p_verdict,
          kenji_=dict(cx=330, cy=1250, s=0.85, expr="shock", outfit="suit"),
          front=lambda img: sweat(D(img), 560, 1050, 1.3),
          items=[B("DAY 15", 0.05, color=(255, 80, 90)), XS("COURT FEES:", R, 110, 0.4, (465, 400), wob=2),
                 XS("-$48,000", R, 200, 1.0, (465, 590), ang=-4, wob=3)],
          fx=dict(zoom=(1.0, 1.04), shake=(1.0, 1.9, 22))),
    scene(((15, 15, 30), (40, 20, 60)), D45, props=p_live,
          items=[CS(["But the trial was livestreamed."], 0.2, 300, 46),
                 XS("40M VIEWS", G, 150, 1.4, (465, 1290), ang=-5)]),
    scene(((70, 20, 30), (30, 10, 15)), D45, props=p_show,
          front=lambda img: kenji(img, 790, 1500, 0.38, "shock"),
          items=[CS(["Mochi gets his own court show."], 0.2, 680, 46),
                 CS(["Kenji plays the bailiff.", "Unpaid."], 2.0, 1420, 46, bg=Y, x=380)]),
    endcard_safe([("PART 6:", Y), ("KENJI BECOMES", WH), ("A LANDLORD", G)], 4.2, acc=("glasses", "tie")),
]

if __name__ == "__main__":
    if check_safe(scenes) and "--force" not in sys.argv:
        sys.exit("fix safe-zone issues first")
    run("ep5", scenes, tension_idx=7, fail_idx=9, twist_idx=10, dings=[(10, 1.4), (11, 0.3)], booms=[(5, 0.2)],
        check="--check" in sys.argv)
