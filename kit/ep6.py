import sys
sys.path.insert(0, "/home/claude/video")
from safe import *
from run_ep import run

D45 = 4.5
SL = lambda cx=465, cy=1150, c=(255, 255, 255, 150), inner=380: dict(cx=cx, cy=cy, color=c, inner=inner)
FRIDGE = (225, 235, 240)


def fridge(img, cx, cy, s=1.0, tag=None, open_=False):
    d = D(img)
    P = lambda x, y: (cx + x * s, cy + y * s)
    d.rect((*P(-170, -380), *P(170, 380)), fill=FRIDGE, width=8, r=int(30 * s))
    d.line([P(-170, -90), P(170, -90)], width=7)
    d.rect((*P(110, -300), *P(130, -170)), fill=(150, 160, 170), width=4, r=6)
    d.rect((*P(110, -40), *P(130, 140)), fill=(150, 160, 170), width=4, r=6)
    if open_:
        d.rect((*P(-150, -70), *P(150, 360)), fill=(255, 250, 220), width=6)
        for y in (60, 200):
            d.line([P(-150, y), P(150, y)], fill=(170, 170, 180), width=6)
    if tag:
        d.rect((*P(-150, -360), *P(90, -260)), fill=(255, 225, 40), width=5, r=10)
        d.text(P(-30, -310), tag, int(54 * s), INK, font=ANTON)


def phone_listing(img, cx, cy, s, title, price):
    d = D(img)
    P = lambda x, y: (cx + x * s, cy + y * s)
    d.rect((*P(-200, -360), *P(200, 360)), fill=(25, 25, 35), width=8, r=int(40 * s))
    d.rect((*P(-175, -320), *P(175, 320)), fill=WH, width=0, r=int(20 * s))
    d.rect((*P(-175, -320), *P(175, -230)), fill=(255, 90, 95), width=0, r=int(20 * s))
    d.text(P(0, -275), "AirBnK", int(52 * s), WH, font=ANTON)
    d.rect((*P(-150, -200), *P(150, 40)), fill=(200, 225, 245), width=4)
    fridge(img, P(0, -80)[0], P(0, -80)[1], 0.27 * s)
    d.text(P(0, 110), title, int(42 * s), INK, font=ANTON)
    d.text(P(0, 200), price, int(70 * s), (40, 160, 80), font=ANTON)


def floorplan(img):
    d = D(img)
    d.rect((70, 760, 870, 1460), fill=(245, 240, 225), width=10)
    d.line([(470, 760), (470, 1460)], width=8)
    d.line([(70, 1110), (870, 1110)], width=8)
    for (x, y, a, b) in [(270, 935, "CLOSET", "$600"), (670, 935, "BATHTUB", "$500"),
                         (270, 1285, "FRIDGE SHELF", "$400"), (670, 1285, "BALCONY", "$350")]:
        d.text((x, y - 40), a, 50, INK, font=ANTON)
        d.text((x, y + 40), b, 64, (40, 160, 80), font=ANTON)


def tenant(img, cx, cy, s, col):
    d = D(img)
    d.rect((cx - 70 * s, cy, cx + 70 * s, cy + 260 * s), fill=col, width=6, r=int(40 * s))
    d.ell((cx - 60 * s, cy - 120 * s, cx + 60 * s, cy + 5 * s), fill=SKIN, width=6)
    d.ell((cx - 25 * s, cy - 70 * s, cx - 10 * s, cy - 50 * s), fill=INK, width=0)
    d.ell((cx + 10 * s, cy - 70 * s, cx + 25 * s, cy - 50 * s), fill=INK, width=0)


def bug(d, cx, cy, s=1.0):
    d.ell((cx - 22 * s, cy - 14 * s, cx + 22 * s, cy + 14 * s), fill=(60, 50, 40), width=3)
    for dx in (-12, 0, 12):
        d.line([(cx + dx * s, cy - 10 * s), (cx + (dx - 6) * s, cy - 26 * s)], width=3)
        d.line([(cx + dx * s, cy + 10 * s), (cx + (dx + 6) * s, cy + 26 * s)], width=3)


def door(img, cx, cy):
    d = D(img)
    d.rect((cx - 230, cy - 520, cx + 230, cy + 520), fill=(120, 70, 40), width=10)
    d.rect((cx - 180, cy - 460, cx + 180, cy - 80), fill=None, outline=(80, 45, 25), width=6)
    d.rect((cx - 180, cy + 20, cx + 180, cy + 460), fill=None, outline=(80, 45, 25), width=6)
    d.ell((cx + 150, cy - 20, cx + 190, cy + 20), fill=(230, 190, 70), width=5)


def building(img, cx, cy, s=1.0, sign=None):
    d = D(img)
    P = lambda x, y: (cx + x * s, cy + y * s)
    d.rect((*P(-260, -520), *P(260, 520)), fill=(200, 140, 110), width=8)
    for yy in range(-460, 400, 140):
        for xx in (-200, -60, 80):
            d.rect((*P(xx, yy), *P(xx + 100, yy + 90)), fill=(255, 235, 150), width=5)
    d.rect((*P(-70, 400), *P(70, 520)), fill=(90, 60, 40), width=6)
    if sign:
        d.rect((*P(-230, -620), *P(230, -530)), fill=(255, 225, 40), width=6, r=12)
        d.text(P(0, -575), sign, int(50 * s), INK, font=ANTON)


def p_hook(img):
    fridge(img, 720, 1250, 1.0, tag="$400/MO", open_=True)


def p_recap(img):
    d = D(img)
    d.rect((520, 950, 880, 1250), fill=(250, 248, 238), width=6)
    d.text((700, 1010), "COURT FEES", 44, INK, font=ANTON)
    d.text((700, 1150), "-$48,000", 70, (220, 40, 60), font=ANTON)


def p_listing(img):
    phone_listing(img, 640, 1100, 1.0, "Cozy fridge shelf", "$400/mo")


def p_tenants(img):
    floorplan(img)
    for x, c in [(200, (90, 160, 230)), (470, (240, 120, 160)), (740, (120, 200, 120))]:
        tenant(img, x, 1590, 0.8, c)


def p_box(img):
    d = D(img)
    d.rect((-20, 1500, 1100, 1960), fill=(160, 160, 175), width=0)
    box(img, 250, 1150, 520, 400)
    d.text((510, 1300), "THIS SIDE UP", 36, (120, 80, 40), font=ANTON)


def p_mochi(img):
    cat(img, 600, 1250, 0.7, "smug", acc=("glasses",))
    d = D(img)
    for x, y in [(250, 1450), (330, 1490), (410, 1440)]:
        bug(d, x, y, 1.4)


def p_complaints(img):
    for x, c in [(200, (90, 160, 230)), (470, (240, 120, 160)), (740, (120, 200, 120))]:
        tenant(img, x, 1300, 0.9, c)


def p_door(img):
    door(img, 640, 1180)


def p_fans(img):
    phone_listing(img, 465, 900, 1.2, "Mochi's nap spot", "$900/night")


def p_owner(img):
    building(img, 600, 1150, 0.9, sign="MOCHI PROPERTIES")


scenes = [
    scene(((20, 90, 140), (120, 210, 240)), 4.0, ht=(255, 255, 255, 40), props=p_hook,
          kenji_=dict(cx=300, cy=1200, s=0.85, expr="intense", glow_eyes=True),
          items=[TS([("HE RENTED OUT", WH), ("HIS FRIDGE.", Y)], 140, 0.05, 330), TS([("TO A STRANGER.", R)], 110, 0.9, 630),
                 CS(["here's how..."], 2.2, 1480, 50, wob=2)],
          fx=dict(zoom=(1.08, 1.0), shake=(0, 0.35, 18), speed=SL(cy=1150))),
    scene(((230, 235, 245), (170, 180, 200)), D45, props=p_recap,
          front=lambda img: cat(img, 260, 1250, 0.5, "smug", acc=("crown", "glasses")),
          items=[B("LAST TIME", 0.05), CS(["Sued his cat. Lost.", "Owes $48,000."], 0.4, 460, 52)]),
    scene(((255, 220, 200), (255, 160, 150)), D45, props=p_listing, kenji_=dict(cx=250, cy=1400, s=0.6, expr="smug"),
          items=[B("DAY 1", 0.05), CS(["New plan: be a landlord.", "Passive income!"], 0.4, 440, 48)]),
    scene(((235, 225, 205), (200, 185, 160)), D45, props=floorplan,
          items=[CS(["He doesn't own a building..."], 0.2, 380, 48),
                 CS(["so he rents out his", "apartment. Piece by piece."], 1.8, 580, 46, bg=Y)]),
    scene(((255, 170, 30), (255, 80, 40)), D45, kenji_=dict(cx=465, cy=1250, s=1.0, expr="shout"),
          items=[B("DAY 3", 0.05, color=WH), XS("FULLY BOOKED", G, 150, 0.4, (465, 430), ang=-4),
                 TS([("I'M A LANDLORD!!", WH)], 120, 1.6, 680, wob=2)],
          fx=dict(zoom=(1.0, 1.08), shake=(0.4, 1.0, 14), speed=SL())),
    scene(((40, 40, 70), (15, 15, 30)), D45, props=p_box,
          front=lambda img: kenji(img, 520, 1240, 0.45, "shock"),
          items=[B("DAY 4", 0.05, color=WH), CS(["Kenji now sleeps in a box."], 0.4, 420, 50),
                 CS(["(the box is also listed)"], 2.2, 620, 46, bg=Y)]),
    scene(((250, 230, 200), (230, 190, 150)), D45, props=p_mochi,
          items=[B("DAY 6", 0.05), CS(["New tenant: Mochi."], 0.4, 420, 52),
                 CS(["Rent paid in: bugs."], 2.0, 620, 50, bg=Y), XS("*crunch*", WH, 90, 3.0, (330, 1330), wob=5)]),
    scene(((60, 70, 90), (25, 30, 45)), D45, props=p_complaints,
          items=[BS(["Why is my room", "cold?"], 0.2, (300, 420), 42),
                 BS(["Someone's in", "my bathtub!"], 1.1, (640, 640), 42, tail="right"),
                 BS(["My bed has", "MILK in it."], 2.0, (300, 900), 42)]),
    scene(((20, 0, 10), (90, 10, 60)), D45, ht=(200, 60, 255, 60), props=p_door,
          kenji_=dict(cx=300, cy=1300, s=0.9, expr="shock"),
          items=[XS("*KNOCK KNOCK*", WH, 120, 0.3, (465, 380), wob=6),
                 BS(["City Housing.", "Who rents out", "a FRIDGE?"], 1.5, (500, 700), 42, tail="right")],
          fx=dict(zoom=(1.0, 1.1), shake=(0.3, 0.8, 16), speed=SL(c=(0, 0, 0, 110), inner=520))),
    scene(((60, 70, 90), (25, 30, 45)), D45, kenji_=dict(cx=465, cy=1300, s=0.92, expr="shock"),
          front=lambda img: (sweat(D(img), 750, 1080, 1.4), sweat(D(img), 190, 1140, 1.0)),
          items=[B("DAY 7", 0.05, color=(255, 80, 90)), XS("CITY FINE:", R, 120, 0.4, (465, 400), wob=2),
                 XS("-$12,000", R, 200, 1.0, (465, 600), ang=-4, wob=3)],
          fx=dict(zoom=(1.0, 1.04), shake=(1.0, 1.9, 22))),
    scene(((15, 15, 30), (60, 40, 10)), D45, props=p_fans,
          items=[CS(["Then Judge Mochi's 40M fans", "find the listing."], 0.2, 330, 44),
                 XS("SOLD OUT", G, 150, 1.8, (465, 1430), ang=-5)]),
    scene(((120, 180, 240), (200, 230, 255)), D45, props=p_owner,
          front=lambda img: kenji(img, 200, 1500, 0.38, "joy"),
          items=[CS(["Kenji pays off his debt!"], 0.2, 330, 48),
                 CS(["Mochi buys the building.", "Raises Kenji's rent."], 2.0, 1400, 44, bg=Y, x=520)]),
    endcard_safe([("PART 7:", Y), ("KENJI LAUNCHES", WH), ("AN AI STARTUP", G)], 4.2, acc=("crown", "glasses")),
]

if __name__ == "__main__":
    if check_safe(scenes) and "--force" not in sys.argv:
        sys.exit("fix safe-zone issues first")
    run("ep6", scenes, tension_idx=8, fail_idx=9, twist_idx=10, dings=[(4, 0.4), (10, 1.8)], booms=[(8, 0.3)],
        check="--check" in sys.argv)
