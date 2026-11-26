"""Safe-zone text helpers: keep text out of the bottom 350 px and the right 150 px.
Usable area: x 0..930, y 0..1570. Centered on x=465 with narrower max widths."""
import sys
sys.path.insert(0, "/home/claude/video")
from props import *

SX = 465          # center of the safe column
SAFE_R, SAFE_B = 930, 1570


def TS(lines, size, t, y, x=SX, wob=0, pop=True, maxw=780):
    return dict(img=text_block(lines, size, maxw=maxw), t=t, xy=(x, y), wobble=wob, pop=pop)


def CS(lines, t, y, size=50, bg=WH, fg=INK, x=SX, wob=0, maxw=740):
    tb = text_block([(l, fg) for l in lines], size, font=ARCH, stroke=0, shadow=False, maxw=maxw, gap=14)
    pad = 26
    img = Image.new("RGBA", (tb.width + pad * 2, tb.height + pad * 2 - 10), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    dr.rounded_rectangle([8, 10, img.width - 1, img.height - 1], 18, fill=(0, 0, 0, 150))
    dr.rounded_rectangle([0, 0, img.width - 9, img.height - 11], 18, fill=bg, outline=INK, width=6)
    img.alpha_composite(tb, (pad - 4, pad - 14))
    return dict(img=img, t=t, xy=(x, y), wobble=wob)


def XS(text, color, size, t, xy, ang=0, wob=4, maxw=760):
    im = text_block([(text, color)], size, font=ANTON, stroke=12, maxw=maxw).rotate(ang, Image.BICUBIC, expand=True)
    return dict(img=im, t=t, xy=xy, wobble=wob)


def BS(lines, t, xy, size=46, tail="left"):
    tb = text_block([(l, INK) for l in lines], size, font=ARCH, stroke=0, shadow=False, maxw=560, gap=10)
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


def endcard_safe(next_lines, dur=4.2, mochi=True, acc=("glasses",)):
    def front(img):
        if mochi:
            cat(img, 760, 1430, 0.55, "smug", acc=acc)
    return scene(((70, 20, 120), (20, 10, 40)), dur, ht=(255, 255, 255, 30),
                 kenji_=dict(cx=340 if mochi else 465, cy=1420, s=0.62, expr="smug"), front=front,
                 items=[TS(next_lines, 110, 0.1, 470),
                        CS(["FOLLOW so you don't miss it"], 0.9, 870, 46, bg=(255, 70, 110), fg=WH, wob=3),
                        dict(img=text_block([("not financial advice. obviously.", (230, 230, 240))], 42, font=ARCH,
                                            stroke=4, shadow=False, maxw=760), t=1.5, xy=(SX, 1040), pop=False)])


def check_safe(scenes):
    """Print any text item whose box (with a small wobble/pop margin) leaves the safe zone."""
    bad = 0
    for i, fn in enumerate(scenes):
        _, _, items, _ = fn()
        for j, it in enumerate(items):
            w, h = it["img"].size
            cx, cy = it["xy"]
            m = 12 if it.get("wobble") else 0
            x1, y1 = cx + w / 2 + m, cy + h / 2 + m
            x0, y0 = cx - w / 2 - m, cy - h / 2 - m
            if x1 > SAFE_R or y1 > SAFE_B or x0 < 0 or y0 < 0:
                bad += 1
                print(f"scene {i} item {j}: box ({x0:.0f},{y0:.0f})-({x1:.0f},{y1:.0f}) outside safe zone")
    print("safe-zone issues:", bad)
    return bad
