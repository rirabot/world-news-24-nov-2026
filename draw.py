#!/usr/bin/env python3
"""Draw the 24 November 2026 world-news front page (1024x1024 PNG).

Deterministic: fixed layout, fixed strings, no randomness, no time, no network.
Run: python3 draw.py  -> writes entry.png next to this file.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)      # warm newsprint
INK = (24, 24, 24)
NAVY = (20, 33, 61)
GOLD = (233, 196, 106)
CARD = (255, 255, 255)
BORDER = (216, 210, 196)
MUTED = (90, 88, 82)
STRIP = (237, 232, 220)

DJVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DJVU_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_chip(d, x, y, s, color):
    # green chip with pins and an up arrow
    d.rounded_rectangle([x + 10, y + 10, x + s - 10, y + s - 10], radius=4,
                        fill=color)
    for i in range(3):
        yy = y + 16 + i * 12
        d.rectangle([x + 2, yy, x + 10, yy + 5], fill=color)
        d.rectangle([x + s - 10, yy, x + s - 2, yy + 5], fill=color)
    d.polygon([(x + s / 2, y + 18), (x + s / 2 - 8, y + 30),
               (x + s / 2 - 3, y + 30), (x + s / 2 - 3, y + 40),
               (x + s / 2 + 3, y + 40), (x + s / 2 + 3, y + 30),
               (x + s / 2 + 8, y + 30)], fill=(255, 255, 255))


def draw_burst(d, x, y, s, color):
    # orange starburst (explosion) over a dark base line
    cx, cy, r1, r2 = x + s / 2, y + s / 2 - 2, s / 2 - 4, s / 5
    pts = []
    for i in range(16):
        r = r1 if i % 2 == 0 else r2
        a = math.pi * i / 8 - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=color)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 255, 255))
    d.rectangle([x + 4, y + s - 8, x + s - 4, y + s - 4], fill=(60, 60, 60))


def draw_buildings(d, x, y, s, color):
    # city blocks with smoke
    d.rectangle([x + 8, y + 26, x + 22, y + s - 6], fill=color)
    d.rectangle([x + 26, y + 14, x + 40, y + s - 6], fill=(90, 90, 90))
    d.rectangle([x + 44, y + 30, x + s - 8, y + s - 6], fill=color)
    for bx, by in ((x + 12, y + 30), (x + 30, y + 18), (x + 48, y + 34)):
        d.rectangle([bx, by, bx + 5, by + 5], fill=(255, 255, 255))
    d.ellipse([x + 34, y + 2, x + 46, y + 14], fill=(180, 180, 180))
    d.ellipse([x + 44, y + 6, x + 54, y + 16], fill=(200, 200, 200))


def draw_ship(d, x, y, s, color):
    # cargo ship on waves
    d.rectangle([x + 12, y + 16, x + 22, y + 28], fill=(200, 60, 40))
    d.rectangle([x + 24, y + 16, x + 34, y + 28], fill=(40, 90, 160))
    d.rectangle([x + 36, y + 16, x + 46, y + 28], fill=(220, 160, 40))
    d.polygon([(x + 8, y + 28), (x + s - 8, y + 28),
               (x + s - 14, y + 40), (x + 14, y + 40)], fill=color)
    for i in range(3):
        xx = x + 6 + i * 16
        d.arc([xx, y + 42, xx + 16, y + 52], 180, 360, fill=(60, 120, 180),
              width=3)


def draw_chart(d, x, y, s, color):
    # candlesticks with a falling trend arrow
    bars = [(x + 8, 18, 10, (46, 125, 50)), (x + 24, 26, 14, (200, 60, 40)),
            (x + 40, 12, 10, (46, 125, 50)), (x + 56 - 16, 30, 12,
                                               (200, 60, 40))]
    for bx, by, bh, col in bars:
        d.line([bx + 5, y + by - 6, bx + 5, y + by + bh + 6], fill=col, width=2)
        d.rectangle([bx, y + by, bx + 10, y + by + bh], fill=col)
    d.line([x + 6, y + 12, x + s - 8, y + 34], fill=color, width=4)
    d.polygon([(x + s - 8, y + 34), (x + s - 20, y + 30),
               (x + s - 16, y + 40)], fill=color)


def draw_globe(d, x, y, s, color):
    # globe: circle, meridians, two land blobs
    cx, cy, r = x + s / 2, y + s / 2, s / 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    d.ellipse([cx - r / 2, cy - r, cx + r / 2, cy + r], outline=color, width=2)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=2)
    d.polygon([(cx - 14, cy - 12), (cx - 2, cy - 16), (cx + 2, cy - 6),
               (cx - 8, cy - 2)], fill=(46, 125, 50))
    d.polygon([(cx - 2, cy + 6), (cx + 12, cy + 2), (cx + 14, cy + 12),
               (cx + 2, cy + 14)], fill=(46, 125, 50))


ICONS = {
    "chip": draw_chip,
    "burst": draw_burst,
    "buildings": draw_buildings,
    "ship": draw_ship,
    "chart": draw_chart,
    "globe": draw_globe,
}

# (kicker, accent color, icon, headline, summary)
STORIES = [
    ("NVIDIA", (46, 125, 50), "chip",
     "Huang returns as Nvidia CEO",
     "Jensen Huang is back days after announcing his retirement, "
     "after President Trump intervened. Shares jumped about 31%."),
    ("UKRAINE", (192, 57, 43), "burst",
     "Deadly strike on Zaporizhzhia",
     "A Russian strike kills 2 and wounds dozens, including children. "
     "Ukraine says it hit a Russian warship at a naval base in Benghazi, Libya; Libya seeks a UN inquiry."),
    ("GAZA", (125, 60, 152), "buildings",
     "Hamas security chief killed",
     "An Israeli strike kills Naeem Abu Nahel, Hamas's security chief, "
     "in Gaza City."),
    ("IRAN", (185, 119, 14), "ship",
     "Iran rules out US talks",
     "Tehran sets seven conditions for talks. The US sanctions Iranian "
     "exchange houses; Tehran vows to resist a naval blockade."),
    ("MARKETS", (26, 82, 118), "chart",
     "Dow tops 50,000; Bitcoin slides",
     "The Dow crosses 50,000 while Bitcoin falls below $60,000 and the "
     "Nasdaq slides in an AI sell-off. CrowdStrike buys Zscaler for $44bn."),
    ("WORLD", (20, 143, 119), "globe",
     "World backs Rohingya ruling",
     "Fourteen countries back the ICJ ruling that Myanmar committed "
     "genocide against the Rohingya. The UN chief urges AI rules within a "
     "year; a 5.6 quake hits Nepal; COP31 ends with no overall deal."),
]

ALSO = ("FIFA names USA, Mexico, Costa Rica and Jamaica as 2031 "
        "Women's World Cup hosts \u2022 Ariane 6 launches 36 Amazon "
        "satellites \u2022 Belgium hit by a national strike")
SOURCES = "Sources: Reuters, BBC, Al Jazeera, AP, AFP \u2014 24 Nov 2026"


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 124], fill=NAVY)
    f_small = font(DJVU_B, 28)
    f_date = font(DJVU_B, 52)
    t1 = "WORLD NEWS IN ONE IMAGE"
    d.text(((W - d.textlength(t1, font=f_small)) / 2, 12), t1,
           font=f_small, fill=GOLD)
    t2 = "TUESDAY, 24 NOVEMBER 2026"
    d.text(((W - d.textlength(t2, font=f_date)) / 2, 48), t2,
           font=f_date, fill=(255, 255, 255))
    d.rectangle([0, 124, W, 128], fill=GOLD)

    # ---- six story panels, 2 x 3 ----
    gx, gy = 24, 140
    pw, ph, gap = 480, 236, 14
    f_kick = font(DJVU_B, 20)
    f_head = font(DJVU_B, 27)
    f_body = font(DJVU, 19)
    for i, (kicker, color, icon, headline, summary) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = gx + col * (pw + gap)
        y0 = gy + row * (ph + gap)
        d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=6,
                            fill=CARD, outline=BORDER, width=2)
        d.rectangle([x0 + 6, y0, x0 + pw - 6, y0 + 6], fill=color)
        d.text((x0 + 16, y0 + 18), kicker, font=f_kick, fill=color)
        ICONS[icon](d, x0 + pw - 74, y0 + 12, 60, color)
        # headline, width leaves room for the icon
        lines = wrap(d, headline, f_head, pw - 32 - 72)
        yy = y0 + 50
        for ln in lines[:2]:
            d.text((x0 + 16, yy), ln, font=f_head, fill=INK)
            yy += 33
        # summary, full width
        lines = wrap(d, summary, f_body, pw - 32)
        yy = y0 + 50 + 2 * 33 + 4
        for ln in lines[:5]:
            d.text((x0 + 16, yy), ln, font=f_body, fill=(51, 51, 51))
            yy += 24

    # ---- bottom "Also" strip ----
    sy = 888
    d.rounded_rectangle([24, sy, W - 24, sy + 62], radius=6,
                        fill=STRIP, outline=BORDER, width=1)
    f_also_b = font(DJVU_B, 19)
    f_also = font(DJVU, 19)
    lines = wrap(d, ALSO, f_also, W - 48 - 70)
    yy = sy + 9
    d.text((40, yy), "Also:", font=f_also_b, fill=(192, 57, 43))
    for ln in lines[:2]:
        d.text((108, yy), ln, font=f_also, fill=INK)
        yy += 25

    # ---- footer sources line ----
    f_src = font(DJVU, 17)
    d.text(((W - d.textlength(SOURCES, font=f_src)) / 2, 968), SOURCES,
           font=f_src, fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
