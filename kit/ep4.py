import sys
sys.path.insert(0, "/home/claude/video")
from props import *
from run_ep import run

D45 = 4.5
SL = lambda cx=540, cy=1150, c=(255, 255, 255, 150), inner=380: dict(cx=cx, cy=cy, color=c, inner=inner)


def box_wall(img, y0=900, rows=5, seed=2):
    rnd = random.Random(seed)
    for r_ in range(rows):
        y = y0 + r_ * 170
        x = -60 + (r_ % 2) * 90
        while x < 1100:
            w = rnd.choice([170, 190, 210])
            box(img, x, y, w, 160)
            x += w + 8


def store_screen(text_top, text_big, big_col=INK):
    def scr(d, P):
        d.rect((*P(-235, -295), *P(235, -230)), fill=(255, 110, 60), width=0, outline=None)
        d.text(P(0, -262), text_top, 40, WH, font=ANTON)
        d.text(P(0, -140), text_big, 72, big_col, font=ANTON)
        d.rect((*P(-120, -90), *P(120, -40)), fill=(40, 160, 80), r=10, width=0, outline=None)
        d.text(P(0, -65), "BUY NOW", 34, WH, font=ANTON)
    return scr


def p_hook(img):
    box_wall(img, 1250, 4, 1)


def p_recap(img):
    tuna(img, 760, 1150, 1.3)


def p_store(img):
    laptop(img, 540, 1050, 1.3, store_screen("KENJI MART", "PHONE CASES"))


def p_typo(img):
    laptop(img, 540, 1100, 1.3, store_screen("KENJI MART", "PHONE 51 CASE", (230, 40, 60)))


def p_boxes(img):
    box_wall(img, 600, 8, 4)


def p_brick(img):
    brick_phone(img, 540, 1050, 1.6)
    d = D(img)
    for x, y, r in [(220, 760, 50), (870, 820, 60)]:
        sparkle(d, x, y, r)


def p_ship(img):
    box_wall(img, 1150, 5, 7)
    brick_phone(img, 540, 900, 0.8)


def p_drop(img):
    d = D(img)
    d.rect((60, 400, 420, 1960), fill=(150, 150, 170), width=8)
    for yy in range(480, 1900, 220):
        d.rect((120, yy, 220, yy + 130), fill=(120, 190, 240), width=5)
        d.rect((260, yy, 360, yy + 130), fill=(120, 190, 240), width=5)
    d.rect((-20, 1750, 1100, 1960), fill=(120, 120, 130), width=6)
    brick_phone(img, 720, 1580, 0.6)
    for i in range(4):
        d.line([(690 + i * 20, 1250 - i * 10), (690 + i * 20, 1150 - i * 10)], fill=WH, width=6)


def p_sold(img):
    cat(img, 830, 1180, 0.55, "smug", acc=("glasses", "tie"))
    d = D(img)
    d.rect((700, 1330, 960, 1520), fill=WH, width=5)
    for i in range(4):
        d.line([(730, 1370 + i * 34), (930, 1370 + i * 34)], fill=(150, 150, 160), width=4)
    d.text((830, 1490), "50%", 40, (230, 40, 60), font=ANTON)


scenes = [
    scene(((20, 60, 120), (255, 110, 60)), 4.0, ht=(255, 255, 255, 40), props=p_hook,
          kenji_=dict(cx=540, cy=1150, s=0.9, expr="intense", glow_eyes=True),
          items=[T([("HE SOLD 10,000 PHONES", WH)], 120, 0.05, 300), T([("THAT DON'T EXIST.", Y)], 140, 0.8, 460),
                 C(["here's how..."], 2.2, 1720, 52, wob=2)],
          fx=dict(zoom=(1.08, 1.0), shake=(0, 0.35, 18), speed=SL(cy=1150))),
    scene(((230, 235, 245), (170, 180, 200)), D45, props=p_recap, kenji_=dict(cx=330, cy=1350, s=0.65, expr="shock", outfit="suit"),
          items=[B("LAST TIME", 0.05), C(["Fired by his own cat.", "Paid in tuna."], 0.4, 440, 54)]),
    scene(((20, 60, 70), (20, 120, 110)), D45, ht=(255, 255, 255, 30), props=p_store,
          kenji_=dict(cx=820, cy=1650, s=0.42, expr="smug"),
          items=[B("DAY 1", 0.05), C(["New hustle: dropshipping.", "Zero inventory. Zero effort."], 0.4, 420, 48)]),
    scene(((40, 20, 70), (120, 40, 140)), D45, props=p_typo,
          items=[C(["One tiny typo..."], 0.2, 380, 56), X("PHONE 51", R, 170, 1.4, (540, 1500), ang=-5),
                 C(["(there is no Phone 51)"], 2.4, 1720, 46, bg=Y)]),
    scene(((255, 170, 30), (255, 80, 40)), D45, kenji_=dict(cx=540, cy=1250, s=1.0, expr="shout"),
          items=[B("DAY 3", 0.05, color=WH), X("+10,000 ORDERS", G, 150, 0.4, (540, 470), ang=-4),
                 T([("I'M A CEO!!", WH)], 140, 1.6, 700, wob=2)],
          fx=dict(zoom=(1.0, 1.08), shake=(0.4, 1.0, 14), speed=SL())),
    scene(((90, 100, 120), (50, 55, 70)), D45, props=p_boxes,
          front=lambda img: kenji(img, 540, 1650, 0.45, "shock"),
          items=[B("DAY 5", 0.05, color=WH), C(["\"Zero inventory.\""], 0.4, 400, 56),
                 C(["10,000 boxes arrive", "at his apartment."], 1.8, 1500, 52, bg=Y)]),
    scene(((60, 70, 90), (25, 30, 45)), D45, kenji_=dict(cx=540, cy=1350, s=0.85, expr="shock"),
          front=lambda img: sweat(D(img), 800, 1150, 1.3),
          items=[BU(["Where's my", "Phone 51??"], 0.2, (300, 420), 46), BU(["It's been", "3 days!!"], 1.0, (800, 640), 46, tail="right"),
                 BU(["IS THIS", "A SCAM"], 1.8, (290, 880), 46)]),
    scene(((20, 0, 10), (90, 10, 60)), D45, ht=(200, 60, 255, 60), kenji_=dict(cx=540, cy=1250, s=1.4, expr="intense", glow_eyes=True),
          items=[BU(["Then... I'll MAKE", "the Phone 51."], 0.4, (540, 470))],
          fx=dict(zoom=(1.0, 1.1), speed=SL(c=(0, 0, 0, 110), inner=520))),
    scene(((40, 20, 70), (120, 40, 140)), D45, props=p_brick,
          items=[C(["Introducing: the Phone 51."], 0.2, 380, 52), C(["(it's a brick)"], 1.9, 1600, 58, bg=Y)]),
    scene(((15, 0, 5), (110, 0, 15)), D45, ht=(255, 60, 80, 60), props=p_ship,
          items=[B("DAY 7", 0.05, color=(255, 80, 90)), C(["He ships 10,000 bricks."], 0.4, 420, 56)],
          fx=dict(zoom=(1.0, 1.1), shake=(2.5, 3.2, 12))),
    scene(((60, 70, 90), (25, 30, 45)), D45, kenji_=dict(cx=540, cy=1320, s=0.92, expr="shock"),
          front=lambda img: (sweat(D(img), 830, 1100, 1.4), sweat(D(img), 250, 1160, 1.0)),
          items=[X("REFUND REQUESTS:", R, 120, 0.15, (540, 300), wob=2), X("10,000", R, 230, 0.6, (540, 520), ang=-4, wob=3)],
          fx=dict(zoom=(1.0, 1.04), shake=(0.15, 1.0, 22))),
    scene(((120, 180, 240), (200, 230, 255)), D45, props=p_drop,
          items=[C(["Then a reviewer drops one", "off a building."], 0.2, 380, 50), X("*THUD*", WH, 140, 1.8, (760, 1380), ang=-8),
                 C(["Not. A. Scratch."], 2.6, 1000, 54, x=740, bg=Y)]),
    scene(((15, 15, 30), (60, 40, 10)), D45, props=p_sold, kenji_=dict(cx=360, cy=1380, s=0.75, expr="joy"),
          items=[C(["\"World's first UNBREAKABLE phone.\""], 0.1, 360, 46), X("SOLD OUT", G, 170, 0.9, (540, 560), ang=-5),
                 C(["Mochi takes 50%."], 2.4, 1720, 56, bg=Y)]),
    endcard([("PART 5:", Y), ("KENJI VS MOCHI:", WH), ("THE LAWSUIT", R)], 4.2, mochi=True),
]

if __name__ == "__main__":
    run("ep4", scenes, tension_idx=9, fail_idx=10, twist_idx=11, dings=[(4, 0.4), (12, 0.9)], booms=[(7, 0.4)],
        check="--check" in sys.argv)
