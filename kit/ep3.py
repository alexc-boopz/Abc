import sys
sys.path.insert(0, "/home/claude/video")
from props import *
from run_ep import run

D45 = 4.5
SL = lambda cx=540, cy=1150, c=(255, 255, 255, 150), inner=380: dict(cx=cx, cy=cy, color=c, inner=inner)


def desk(img, y=1350):
    d = D(img)
    d.rect((-20, y, 1100, 1960), fill=(120, 80, 55), width=8)
    d.line([(-20, y + 40), (1100, y + 40)], fill=(95, 60, 40), width=8)


def nametag(img, cx, cy):
    d = D(img)
    d.rect((cx - 120, cy - 45, cx + 120, cy + 45), fill=WH, r=10, width=6)
    d.text((cx, cy), "INTERN", 52, (230, 40, 60), font=ANTON)


def cup(img, cx, cy, ang=0):
    lay = Image.new("RGBA", (300 * K, 300 * K), (0, 0, 0, 0))
    d = D(lay)
    d.poly([(90, 60), (210, 60), (195, 250), (105, 250)], fill=WH, width=6)
    d.rect((95, 110, 205, 170), fill=(140, 80, 50), width=0, outline=None)
    d.arc((190, 100, 260, 190), 270, 90, width=10)
    lay = lay.rotate(ang, Image.BICUBIC, expand=True)
    img.alpha_composite(lay, (int(cx * K - lay.width / 2), int(cy * K - lay.height / 2)))


def p_hook(img):
    cat(img, 820, 1080, 0.55, "smug", acc=("glasses", "tie"))


def p_recap(img):
    money_pile(img, 540, 1400, 1.4)
    cat(img, 540, 1170, 0.95, "smug", acc=("glasses", "crown"))


def p_office(img):
    d = D(img)
    d.rect((90, 470, 990, 760), fill=(240, 240, 250), r=10, width=8)
    d.text((540, 560), "MOCHI CAPITAL", 96, INK, font=ANTON)
    d.text((540, 680), "est. last week", 44, (120, 120, 140), font=ARCH)


def f_tag(img):
    nametag(img, 400, 1640)


def p_ceo(img):
    desk(img, 1300)
    cat(img, 480, 1080, 0.95, "smug", acc=("tie",))
    cup(img, 820, 1230)


def p_market_up(img):
    chart_monitor(img, (90, 500, 990, 1060), "up", 3, label="MARKET")
    cup(img, 760, 1350, 70)
    d = D(img)
    d.line([(600, 1230), (680, 1290)], fill=(140, 80, 50), width=10)


def p_vases(img):
    vase(img, 160, 1000, 0.6, 40)
    vase(img, 920, 900, 0.55, -55)
    vase(img, 870, 1500, 0.5, 120)


def p_nap(img):
    desk(img, 1450)
    cat(img, 540, 1180, 1.05, "happy", acc=("tie",))


def p_laser(img):
    glow_dot(img, 540, 1020, 34)


def p_chase(img):
    keyboard(img, 60, 1300, 1020, 1650)
    cat(img, 420, 1080, 0.85, "neutral")
    glow_dot(img, 860, 1450, 22)
    d = D(img)
    for i in range(6):
        d.line([(120 + i * 30, 1000 + i * 25), (40 + i * 30, 1000 + i * 25)], fill=WH, width=6)


def p_crash(img):
    chart_monitor(img, (90, 440, 990, 900), "crash", 11)


def p_fired(img):
    cat(img, 830, 1060, 0.55, "stare", acc=("tie",))
    tuna(img, 540, 1300, 1.6)


scenes = [
    scene(((20, 30, 90), (90, 40, 160)), 4.0, ht=(255, 255, 255, 35), props=p_hook,
          kenji_=dict(cx=380, cy=1300, s=0.85, expr="shock"),
          items=[T([("HIS BOSS IS A CAT.", WH)], 130, 0.05, 320), T([("HIS OWN CAT.", Y)], 150, 0.8, 490),
                 C(["...and the cat is winning."], 2.2, 1660, 52, wob=2)],
          fx=dict(zoom=(1.08, 1.0), shake=(0, 0.35, 18), speed=SL(cy=1200))),
    scene(((15, 15, 30), (60, 40, 10)), D45, props=p_recap,
          items=[B("LAST TIME", 0.05), C(["Mochi the cat made $1,000,000", "on $MOCHI coin."], 0.4, 430, 48),
                 C(["Kenji lost everything."], 1.9, 1720, 52, bg=Y)]),
    scene(((230, 235, 245), (170, 180, 200)), D45, props=p_office,
          kenji_=dict(cx=540, cy=1280, s=0.85, expr="neutral", outfit="suit"), front=f_tag,
          items=[B("DAY 1", 0.05, xy=(250, 330)), C(["Kenji's first day", "as Mochi's intern."], 1.2, 880, 52)]),
    scene(((60, 40, 90), (30, 20, 50)), D45, props=p_ceo,
          items=[C(["Mochi's investing strategy:"], 0.2, 380, 52),
                 T([("KNOCK THINGS", Y), ("OFF THE TABLE.", WH)], 120, 1.4, 600, wob=2)]),
    scene(((20, 60, 70), (20, 120, 110)), D45, ht=(255, 255, 255, 30), props=p_market_up,
          items=[C(["*cup falls*"], 0.1, 380, 52), X("+300%", G, 200, 1.2, (540, 1700), ang=-6),
                 C(["...and the market goes UP."], 1.9, 1500, 50, bg=Y)]),
    scene(((255, 170, 30), (255, 80, 40)), D45, kenji_=dict(cx=540, cy=1200, s=1.05, expr="shout", outfit="suit"),
          items=[T([("SO WE JUST...", WH), ("KNOCK STUFF OVER?!", Y)], 130, 0.1, 420, wob=2)],
          fx=dict(zoom=(1.0, 1.08), shake=(0.1, 0.8, 12), speed=SL())),
    scene(((40, 20, 70), (120, 40, 140)), D45, props=p_vases, kenji_=dict(cx=540, cy=1260, s=0.9, expr="shout", outfit="suit"),
          items=[B("DAY 4", 0.05), X("*CRASH*", WH, 150, 0.4, (540, 560), ang=-8), X("+9,000%", G, 180, 2.0, (560, 760), ang=5)],
          fx=dict(zoom=(1.0, 1.06), shake=(0.4, 1.0, 18), speed=SL(c=(255, 255, 220, 120)))),
    scene(((40, 50, 80), (20, 25, 45)), D45, props=p_nap,
          items=[B("DAY 6", 0.05, color=WH), C(["Mochi takes a nap."], 0.4, 420, 56), X("Zzz", WH, 140, 1.0, (800, 820), wob=6),
                 C(["16 hours long."], 2.0, 1700, 56, bg=Y)]),
    scene(((20, 0, 10), (90, 10, 60)), D45, ht=(200, 60, 255, 60), kenji_=dict(cx=540, cy=1250, s=1.4, expr="intense", outfit="suit", glow_eyes=True),
          items=[BU(["Then...", "I'M in charge."], 0.4, (540, 470))],
          fx=dict(zoom=(1.0, 1.1), speed=SL(c=(0, 0, 0, 110), inner=520))),
    scene(((15, 0, 5), (110, 0, 15)), D45, ht=(255, 60, 80, 60), props=p_laser,
          items=[C(["He goes ALL IN on..."], 0.2, 420, 56), T([("LASER POINTER INC.", R)], 120, 1.8, 1500)],
          fx=dict(zoom=(1.0, 1.1), shake=(1.8, 2.4, 14))),
    scene(((40, 30, 60), (15, 10, 25)), D45, props=p_chase,
          items=[C(["Mochi wakes up.", "Sees the dot."], 0.2, 420, 54), X("*ZOOM*", WH, 150, 1.6, (700, 820), ang=-10)],
          fx=dict(shake=(1.6, 3.0, 16))),
    scene(((60, 70, 90), (25, 30, 45)), D45, props=p_crash, kenji_=dict(cx=540, cy=1320, s=0.92, expr="shock", outfit="suit"),
          front=lambda img: (sweat(D(img), 830, 1100, 1.4), sweat(D(img), 250, 1160, 1.0)),
          items=[X("-97%", R, 230, 0.15, (540, 300), ang=-4, wob=3),
                 C(["Mochi made 4,000 trades", "in 3 seconds."], 1.8, 1720, 52)],
          fx=dict(zoom=(1.0, 1.04), shake=(0.15, 1.0, 22))),
    scene(((230, 235, 245), (170, 180, 200)), D45, props=p_fired, kenji_=dict(cx=260, cy=1560, s=0.5, expr="shock", outfit="suit"),
          items=[C(["Kenji is fired."], 0.2, 400, 58), C(["Severance: one (1)", "can of tuna."], 1.6, 620, 54, bg=Y),
                 X("*meow*", WH, 90, 2.8, (840, 780), wob=5)]),
    endcard([("PART 4:", Y), ("KENJI STARTS A", WH), ("DROPSHIPPING EMPIRE", G)], 4.2),
]

if __name__ == "__main__":
    run("ep3", scenes, tension_idx=9, fail_idx=11, twist_idx=12, dings=[(4, 1.2), (6, 2.0)], booms=[(9, 1.8), (6, 0.4)],
        check="--check" in sys.argv)
