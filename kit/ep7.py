import sys
sys.path.insert(0, "/home/claude/video")
from safe import *
from run_ep import run

D45 = 4.5
SL = lambda cx=465, cy=1150, c=(255, 255, 255, 150), inner=380: dict(cx=cx, cy=cy, color=c, inner=inner)


def screen_text(lines, col=INK, size=54, bg=WH, head=None):
    def scr(d, P):
        d.rect((*P(-235, -295), *P(235, 0)), fill=bg, width=0, outline=None)
        y0 = -230
        if head:
            d.rect((*P(-235, -295), *P(235, -235)), fill=(90, 70, 220), width=0, outline=None)
            d.text(P(0, -265), head, 40, WH, font=ANTON)
            y0 = -180
        for i, l in enumerate(lines):
            d.text(P(0, y0 + i * (size + 14)), l, size, col, font=ANTON)
    return scr


def closet(img):
    d = D(img)
    d.rect((80, 380, 880, 1960), fill=(70, 50, 40), width=10)
    d.rect((120, 420, 840, 1960), fill=(35, 25, 25), width=0)
    d.line([(140, 520), (820, 520)], fill=(150, 150, 160), width=10)
    for x in (220, 330, 640, 760):
        d.line([(x, 520), (x - 40, 600), (x + 40, 600), (x, 520)], fill=(150, 150, 160), width=5)


def server_rack(img, x, y):
    d = D(img)
    d.rect((x, y, x + 200, y + 500), fill=(40, 45, 60), width=7, r=10)
    for i in range(6):
        yy = y + 30 + i * 78
        d.rect((x + 20, yy, x + 180, yy + 56), fill=(70, 75, 95), width=4)
        d.ell((x + 145, yy + 18, x + 165, yy + 38), fill=(255, 60, 70), width=0)


def star_row(d, cx, cy, n=5, r=34):
    for i in range(n):
        x = cx + (i - (n - 1) / 2) * r * 2.3
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            rr = r if k % 2 == 0 else r * 0.45
            pts.append((x + rr * math.cos(a), cy + rr * math.sin(a)))
        d.poly(pts, fill=(255, 210, 40), width=4)


def p_hook(img):
    laptop(img, 640, 1300, 1.2, screen_text(["KenjiGPT", "thinking..."], head="AI"))


def p_recap(img):
    d = D(img)
    d.rect((470, 820, 870, 1420), fill=(200, 140, 110), width=8)
    for yy in range(870, 1320, 120):
        for xx in (510, 640, 760):
            d.rect((xx, yy, xx + 80, yy + 70), fill=(255, 235, 150), width=4)
    d.rect((480, 740, 860, 810), fill=Y, width=5, r=10)
    d.text((670, 775), "RENT: +300%", 44, INK, font=ANTON)
    cat(img, 250, 1300, 0.5, "smug", acc=("crown", "glasses"))


def p_idea(img):
    laptop(img, 620, 1050, 1.2, screen_text(["KenjiGPT"], (90, 70, 220), 80))


def p_pitch(img):
    d = D(img)
    d.rect((90, 650, 840, 1150), fill=WH, width=10, r=12)
    d.text((465, 900), "AI", 300, (90, 70, 220), font=ANTON)
    d.line([(465, 1150), (465, 1300)], width=10)
    for x in (180, 330, 600, 750):
        tenant_head(d, x, 1450)


def tenant_head(d, x, y):
    d.rect((x - 60, y, x + 60, y + 200), fill=(40, 40, 55), width=5, r=30)
    d.ell((x - 50, y - 100, x + 50, y + 5), fill=SKIN, width=5)
    d.rect((x - 40, y - 60, x - 5, y - 40), fill=INK, width=0)
    d.rect((x + 5, y - 60, x + 40, y - 40), fill=INK, width=0)


def p_noai(img):
    server_rack(img, 600, 820)
    d = D(img)
    d.text((700, 1380), "(empty)", 46, (200, 200, 210), font=ARCH)


def p_closet(img):
    closet(img)
    laptop(img, 465, 1420, 0.9, screen_text(["user: what's 2+2", "kenji: 4? i think"], INK, 34))


def p_rush(img):
    for x, y in [(220, 960), (710, 960)]:
        laptop(img, x, y, 0.6, screen_text(["NEW QUESTION"], (220, 40, 60), 50))


def p_mochi_keys(img):
    laptop(img, 465, 1000, 1.25, screen_text(["asdfjk;;;;;", "mrrp"], INK, 70))
    cat(img, 560, 1420, 0.6, "neutral")


def p_reviews(img):
    d = D(img)
    star_row(d, 465, 740)
    for i, (txt, y) in enumerate([("\"Finally, an honest AI.\"", 900), ("\"It said mrrp. I felt seen.\"", 1060),
                                  ("\"10/10 would ask again\"", 1220)]):
        d.rect((90, y - 60, 840, y + 60), fill=WH, width=5, r=16)
        d.text((465, y), txt, 40, INK, font=ARCH)


def p_unicorn(img):
    cat(img, 620, 1200, 0.65, "smug", acc=("crown", "glasses", "tie"))
    d = D(img)
    d.rect((470, 1420, 830, 1520), fill=(255, 210, 40), width=6, r=14)
    d.text((650, 1470), "CEO", 60, INK, font=ANTON)


scenes = [
    scene(((30, 20, 80), (120, 60, 220)), 4.0, ht=(255, 255, 255, 40), props=p_hook,
          kenji_=dict(cx=300, cy=1250, s=0.85, expr="intense", glow_eyes=True),
          items=[TS([("HIS AI WAS", WH), ("JUST HIM.", Y)], 150, 0.05, 330), TS([("TYPING. FAST.", R)], 120, 0.9, 640),
                 CS(["here's how..."], 2.2, 1480, 50, wob=2)],
          fx=dict(zoom=(1.08, 1.0), shake=(0, 0.35, 18), speed=SL(cy=1150))),
    scene(((230, 235, 245), (170, 180, 200)), D45, props=p_recap,
          items=[B("LAST TIME", 0.05), CS(["Mochi bought the building.", "Kenji's rent: +300%."], 0.4, 460, 48)]),
    scene(((200, 220, 255), (140, 160, 240)), D45, props=p_idea, kenji_=dict(cx=230, cy=1450, s=0.55, expr="smug"),
          items=[B("DAY 1", 0.05), CS(["Rent is due.", "New plan: an AI startup."], 0.4, 440, 48)]),
    scene(((20, 30, 50), (50, 70, 110)), D45, props=p_pitch,
          items=[CS(["His pitch deck: one slide."], 0.2, 400, 48),
                 XS("+$20M RAISED", G, 130, 1.8, (465, 560), ang=-4)]),
    scene(((60, 70, 90), (25, 30, 45)), D45, props=p_noai, kenji_=dict(cx=280, cy=1300, s=0.7, expr="shock"),
          items=[B("DAY 2", 0.05, color=WH), CS(["Launch day. One problem:"], 0.4, 420, 48),
                 XS("THERE IS NO AI.", R, 110, 1.6, (465, 620), ang=-3)]),
    scene(((40, 30, 30), (15, 10, 10)), D45, props=p_closet,
          front=lambda img: kenji(img, 220, 1250, 0.36, "intense"),
          items=[B("DAY 3", 0.05, color=WH), CS(["So Kenji answers", "every question himself."], 0.4, 480, 46)]),
    scene(((255, 170, 30), (255, 80, 40)), D45, props=p_rush, kenji_=dict(cx=465, cy=1450, s=0.7, expr="shout"),
          front=lambda img: (sweat(D(img), 640, 1200, 1.2), sweat(D(img), 290, 1240, 0.9)),
          items=[B("DAY 5", 0.05, color=WH), XS("1,000,000 USERS", WH, 120, 0.4, (465, 420), ang=-4),
                 CS(["(he types 900 words a minute)"], 1.8, 620, 42, bg=Y)],
          fx=dict(zoom=(1.0, 1.08), shake=(0.4, 1.0, 14), speed=SL())),
    scene(((20, 0, 10), (90, 10, 60)), D45, ht=(200, 60, 255, 60),
          kenji_=dict(cx=465, cy=1250, s=1.3, expr="intense", glow_eyes=True),
          items=[BS(["I am...", "the algorithm."], 0.4, (465, 480), 50)],
          fx=dict(zoom=(1.0, 1.1), speed=SL(c=(0, 0, 0, 110), inner=520))),
    scene(((60, 70, 90), (25, 30, 45)), D45, kenji_=dict(cx=465, cy=1300, s=0.92, expr="shock"),
          front=lambda img: (sweat(D(img), 750, 1080, 1.4), sweat(D(img), 190, 1140, 1.0)),
          items=[B("DAY 6", 0.05, color=(255, 80, 90)), CS(["Kenji falls asleep. Site goes down."], 0.3, 380, 40),
                 XS("INVESTORS WANT", R, 100, 1.2, (465, 540), wob=2), XS("$20,000,000", R, 150, 1.6, (465, 700), ang=-4, wob=3)],
          fx=dict(zoom=(1.0, 1.04), shake=(1.6, 2.4, 22))),
    scene(((250, 230, 200), (230, 190, 150)), D45, props=p_mochi_keys,
          items=[CS(["Then Mochi walks across", "the keyboard."], 0.2, 330, 46),
                 XS("*SEND*", WH, 100, 2.2, (250, 1250), ang=8)]),
    scene(((15, 15, 30), (60, 40, 10)), D45, props=p_reviews,
          items=[CS(["Users LOVE it."], 0.2, 420, 52), XS("5 STARS", G, 120, 2.6, (465, 1420), ang=-5)]),
    scene(((120, 180, 240), (200, 230, 255)), D45, props=p_unicorn,
          front=lambda img: kenji(img, 220, 1480, 0.4, "shock"),
          items=[CS(["MochiGPT: valued at $1B."], 0.2, 380, 48),
                 CS(["Kenji's new job title:", "\"training data.\""], 2.0, 620, 44, bg=Y)]),
    endcard_safe([("PART 8:", Y), ("KENJI RUNS", WH), ("FOR MAYOR", G)], 4.2, acc=("crown", "glasses")),
]

if __name__ == "__main__":
    if check_safe(scenes) and "--force" not in sys.argv:
        sys.exit("fix safe-zone issues first")
    run("ep7", scenes, tension_idx=7, fail_idx=8, twist_idx=9, dings=[(3, 1.8), (10, 2.6)], booms=[(4, 1.6)],
        check="--check" in sys.argv)
