import sys
sys.path.insert(0, "/home/claude/video")
from props import *
from run_ep import run

D45 = 4.5
SL = lambda cx=540, cy=1150, c=(255, 255, 255, 150), inner=380: dict(cx=cx, cy=cy, color=c, inner=inner)


def p_hook(img):
    rnd = random.Random(5)
    for i in range(7):
        coin(img, rnd.uniform(80, 1000), rnd.uniform(760, 1100), rnd.uniform(60, 90))


def p_recap(img):
    d = D(img)
    d.rect((90, 520, 990, 1000), fill=(250, 250, 255), r=10, width=8)
    d.text((540, 610), "HOW I LOST IT ALL", 78, INK, font=ANTON)
    d.text((540, 730), "SOLD OUT", 120, (230, 40, 60), font=ANTON, stroke=0)
    d.text((540, 880), "$997,000 EARNED", 70, (40, 160, 80), font=ANTON)


def p_coin_monitor(img):
    chart_monitor(img, (90, 520, 990, 1020), "chaos", 4, label="CRYPTO")


def p_coin_big(img):
    coin(img, 540, 950, 330)
    d = D(img)
    for x, y, r in [(150, 650, 50), (930, 700, 60), (180, 1250, 40), (910, 1230, 45)]:
        sparkle(d, x, y, r)


def p_room(img):
    d = D(img)
    d.rect((-20, 1480, 1100, 1960), fill=(110, 70, 50), width=8)


def p_rocket(img):
    rocket(img, 860, 900, 1.1)
    d = D(img)
    d.ell((80, 520, 260, 700), fill=(240, 240, 220), width=6)
    for x, y, r in [(170, 580, 18), (210, 650, 12), (120, 640, 10)]:
        d.ell((x - r, y - r, x + r, y + r), fill=(200, 200, 185), outline=None, width=0)


def p_lambo(img):
    car(img, 540, 1000, 1.25)
    d = D(img)
    for x, y, r in [(160, 820, 45), (930, 860, 55)]:
        sparkle(d, x, y, r)


def p_keyboard_cat(img):
    keyboard(img, 80, 1250, 1000, 1600)
    cat(img, 540, 1050, 0.95, "neutral")


def p_sell(img):
    keyboard(img, 80, 1400, 1000, 1750)
    big_button(img, 540, 980, 300, "SELL ALL")
    cat(img, 850, 1330, 0.5, "smug")


def p_crash(img):
    chart_monitor(img, (90, 440, 990, 900), "crash", 7)


def p_toy(img):
    d = D(img)
    d.rect((-20, 1300, 1100, 1960), fill=(170, 140, 110), width=6)
    d.rect((300, 1180, 780, 1320), fill=(205, 155, 95), width=6)
    car(img, 540, 1150, 0.22)


def p_rich_cat(img):
    money_pile(img, 540, 1380, 1.5)
    cat(img, 540, 1150, 1.0, "smug", acc=("glasses", "crown"))


def p_ken_small(img):
    kenji(img, 220, 1560, 0.45, "shock")


scenes = [
    scene(((70, 20, 120), (255, 70, 140)), 4.0, ht=(255, 255, 255, 40), props=p_hook,
          kenji_=dict(cx=540, cy=1280, s=0.95, expr="intense", glow_eyes=True),
          items=[T([("HE PUT HIS RENT", WH)], 130, 0.05, 300), T([("INTO A COIN", Y)], 150, 0.6, 460),
                 T([("NAMED AFTER HIS CAT.", WH)], 110, 1.2, 610), C(["here's what happened..."], 2.3, 1580, 52, wob=2)],
          fx=dict(zoom=(1.08, 1.0), shake=(0, 0.35, 18), speed=SL(cy=1200))),
    scene(((15, 15, 30), (35, 30, 60)), D45, props=p_recap, kenji_=dict(cx=540, cy=1480, s=0.6, expr="joy", outfit="suit"),
          items=[B("LAST TIME", 0.05), C(["Kenji lost 99.8% day trading..."], 0.4, 420, 50),
                 C(["...then sold a course about it."], 1.8, 1180, 50, bg=Y)]),
    scene(((20, 60, 70), (20, 120, 110)), D45, ht=(255, 255, 255, 30), props=p_coin_monitor,
          kenji_=dict(cx=300, cy=1520, s=0.62, expr="smug"),
          items=[B("DAY 1", 0.05), C(["New plan: put ALL of it", "into crypto."], 0.4, 400, 52),
                 BU(["Real money is", "for boomers."], 1.6, (720, 1300))]),
    scene(((255, 170, 30), (255, 80, 40)), D45, kenji_=dict(cx=540, cy=1200, s=1.05, expr="intense", glow_eyes=True),
          items=[T([("NO WAIT.", WH)], 130, 0.1, 330), T([("I'LL MAKE MY", WH), ("OWN COIN.", Y)], 140, 0.9, 560, wob=2)],
          fx=dict(zoom=(1.0, 1.1), shake=(0.9, 1.5, 14), speed=SL())),
    scene(((40, 20, 70), (120, 40, 140)), D45, props=p_coin_big,
          items=[C(["Introducing..."], 0.1, 330, 54), T([("$MOCHI", Y)], 200, 0.8, 520, wob=3),
                 C(["Named after his cat. Backed by nothing."], 2.0, 1500, 46, bg=Y)]),
    scene(((250, 210, 220), (240, 160, 190)), D45, ht=(255, 255, 255, 50), props=p_room,
          front=lambda img: cat(img, 540, 1150, 1.1, "stare"),
          items=[C(["This is Mochi."], 0.1, 380, 58), C(["Mochi does not care", "about crypto."], 1.6, 1650, 52)]),
    scene(((10, 10, 40), (60, 20, 100)), D45, props=p_rocket, kenji_=dict(cx=400, cy=1300, s=0.9, expr="shout"),
          items=[B("DAY 3", 0.05), X("+12,000%", G, 200, 1.4, (540, 560), ang=-6),
                 C(["WE'RE GOING TO THE MOON!!"], 2.4, 1640, 52)],
          fx=dict(zoom=(1.0, 1.08), shake=(1.4, 2.0, 14), speed=SL(c=(255, 255, 220, 120)))),
    scene(((255, 220, 120), (255, 150, 60)), D45, props=p_lambo, kenji_=dict(cx=820, cy=1620, s=0.45, expr="smug"),
          items=[B("DAY 5", 0.05), C(["Orders a Lambo.", "Pays in $MOCHI."], 0.4, 450, 54)]),
    scene(((40, 50, 80), (20, 25, 45)), D45, props=p_keyboard_cat,
          items=[B("DAY 6", 0.05, color=(255, 255, 255)), C(["3AM. Mochi walks", "across the keyboard."], 0.4, 450, 52),
                 X("*tap tap tap*", WH, 90, 1.8, (540, 1700), wob=5)]),
    scene(((20, 0, 10), (140, 10, 30)), D45, ht=(255, 60, 80, 70), props=p_sell,
          items=[C(["Mochi's paw lands on..."], 0.2, 420, 54), X("*CLICK*", WH, 170, 2.2, (540, 1250), ang=-8)],
          fx=dict(zoom=(1.0, 1.12), shake=(2.2, 2.8, 16), speed=SL(cy=980, c=(0, 0, 0, 120), inner=420))),
    scene(((60, 70, 90), (25, 30, 45)), D45, props=p_crash, kenji_=dict(cx=540, cy=1320, s=0.92, expr="shock"),
          front=lambda img: (sweat(D(img), 830, 1100, 1.4), sweat(D(img), 250, 1160, 1.0)),
          items=[X("-100%", R, 230, 0.15, (540, 300), ang=-4, wob=3), C(["Everything. Sold.", "At the bottom."], 1.8, 1720, 54)],
          fx=dict(zoom=(1.0, 1.04), shake=(0.15, 1.0, 22))),
    scene(((90, 100, 120), (50, 55, 70)), D45, props=p_toy, kenji_=dict(cx=540, cy=1500, s=0.5, expr="shock"),
          items=[B("DAY 7", 0.05, color=(255, 255, 255)), C(["The Lambo arrives."], 0.4, 420, 56),
                 C(["It's 1:64 scale."], 1.9, 650, 56, bg=Y), X("*squeak*", WH, 80, 2.6, (800, 1050), wob=6)]),
    scene(((15, 15, 30), (60, 40, 10)), D45, props=p_rich_cat, front=p_ken_small,
          items=[C(["Plot twist: Mochi sold", "at the TOP."], 0.2, 400, 52),
                 X("+$1,000,000", G, 150, 1.4, (540, 640), ang=-5),
                 BU(["...teach me."], 2.6, (330, 1250), tail="left")]),
    endcard([("PART 3:", Y), ("KENJI BECOMES", WH), ("MOCHI'S INTERN", G)], 4.2, mochi=True),
]

if __name__ == "__main__":
    run("ep2", scenes, tension_idx=9, fail_idx=10, twist_idx=12, dings=[(6, 1.4), (12, 1.4)], booms=[(3, 0.9), (9, 2.2)],
        check="--check" in sys.argv)
