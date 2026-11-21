#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news frontpage, 1024x1024 PNG.

Deterministic: fixed layout, fixed strings, fixed colours, no timestamps,
no randomness. Renders the same bytes on every run.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

INK = (24, 24, 28)
PAPER = (250, 247, 238)
RED = (178, 34, 34)
DARKRED = (128, 20, 20)
NAVY = (28, 48, 88)
GREY = (96, 96, 100)
LINE = (180, 175, 162)
GOLD = (176, 132, 30)
TEAL = (18, 110, 110)
SKY = (214, 230, 240)
SAND = (238, 226, 200)

MARGIN = 44


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_MAST = font("DejaVuSerif-Bold.ttf", 48)
F_DATE = font("DejaVuSans-Bold.ttf", 26)
F_LEAD_H = font("DejaVuSerif-Bold.ttf", 32)
F_LEAD_B = font("DejaVuSans.ttf", 22)
F_NUM = font("DejaVuSans-Bold.ttf", 24)
F_HEAD = font("DejaVuSans-Bold.ttf", 22)
F_BODY = font("DejaVuSans.ttf", 20)
F_SRC = font("DejaVuSans-Bold.ttf", 16)
F_FOOT = font("DejaVuSans.ttf", 17)

LEAD = (
    "Russian missiles land in Poland",
    "Two Kh-101 missiles and a drone crash in SE Poland amid allied drills; "
    "Tusk: \u201cintentional provocation\u201d. 8 killed in Ukraine overnight.",
    "AP / The Times",
)

STORIES = [
    ("Wall Street plunge",
     "S&P 500 -3.7% into correction; Nasdaq -5.28%, Nvidia -14%; Dow -950.",
     "Reuters"),
    ("COP31 runs into overtime",
     "Antalya draft drops all fossil-fuel mentions; Panama may block it.",
     "Reuters / AP"),
    ("After the Myanmar verdict",
     "Swiss hail the ICJ ruling; Malaysia to resettle 10,000 Rohingya.",
     "AP"),
    ("Trilateral ends in Shenzhen",
     "First-ever three-way summit ends with symbolism, little substance.",
     "AP"),
    ("Nvidia in turmoil",
     "Trump wants Huang back; SEC probes the chipmaker\u2019s accounting.",
     "Reuters"),
    ("Missiles over Riyadh",
     "Saudi coalition stops 3 Houthi missiles, hits Hodeidah; debris in Riyadh.",
     "Reuters / AP"),
    ("900,000 AI chips to China",
     "US approves Nvidia/AMD chip exports to China over six months.",
     "AP"),
    ("Plane crash in Siberia",
     "Russian military transport crashes in Siberia; all 19 aboard killed.",
     "AP"),
    ("Paris police convicted",
     "Three officers convicted over the 2020 beating of Michel Zecler.",
     "AP"),
    ("Aid call for flooded Gaza",
     "Australia, Canada, Italy, UK urge Israel to open aid to flooded Gaza.",
     "AP"),
    ("Israel picks a new PM",
     "Herzog asks ex-army chief Eisenkot to form a government, not Netanyahu.",
     "AP"),
    ("Venezuela\u2019s $12bn oil cash",
     "US details $12bn of oil cash handled a year after Maduro\u2019s capture.",
     "AP"),
    ("France protests again",
     "Fourth straight weekend of cost-of-living protests across France.",
     "AP"),
    ("India fight back in Test",
     "India 159/1 at stumps, day two in Wellington; Nicholls hits 113*.",
     "AP"),
    ("Sensex surges 898 points",
     "Sensex +898 to 83,919.71; NSE now the world\u2019s 5th-largest exchange.",
     "Reuters"),
]


def wrap(draw, text, fnt, width):
    """Wrap text to fit pixel width, returning lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top rule + masthead ---
    d.rectangle([0, 0, W, 10], fill=RED)
    d.text((MARGIN, 22), "THE WORLD IN ONE DAY", font=F_MAST, fill=INK)
    d.text((MARGIN, 82), "SATURDAY 21 NOVEMBER 2026", font=F_DATE, fill=RED)
    d.line([(MARGIN, 120), (W - MARGIN, 120)], fill=INK, width=3)

    # --- lead story ---
    y = 132
    d.rectangle([MARGIN, y, W - MARGIN, y + 152], fill=SKY)
    d.rectangle([MARGIN, y, MARGIN + 8, y + 152], fill=NAVY)
    lx = MARGIN + 24
    d.text((lx, y + 8), "LEAD", font=F_NUM, fill=NAVY)
    d.text((lx, y + 38), LEAD[0], font=F_LEAD_H, fill=INK)
    for i, ln in enumerate(wrap(d, LEAD[1], F_LEAD_B, W - 2 * MARGIN - 48)):
        d.text((lx, y + 80 + i * 26), ln, font=F_LEAD_B, fill=INK)
    d.text((lx, y + 128), "Source: " + LEAD[2], font=F_SRC, fill=NAVY)
    y += 152 + 10
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=LINE, width=2)
    y += 10

    # --- numbered stories: two columns ---
    col_w = (W - 2 * MARGIN - 24) // 2
    col_x = [MARGIN, MARGIN + col_w + 24]
    per_col = 8  # 8 left (1-8), 7 right (9-15)
    row_h = 84
    for idx, (head, body, src) in enumerate(STORIES):
        col = 0 if idx < per_col else 1
        row = idx if col == 0 else idx - per_col
        x = col_x[col]
        yy = y + row * row_h
        # number badge
        d.ellipse([x, yy + 2, x + 34, yy + 36], fill=RED)
        num = str(idx + 1)
        tw = d.textlength(num, font=F_NUM)
        d.text((x + 17 - tw / 2, yy + 5), num, font=F_NUM, fill=PAPER)
        tx = x + 44
        d.text((tx, yy), head, font=F_HEAD, fill=INK)
        blines = wrap(d, body, F_BODY, col_w - 44)
        for j, ln in enumerate(blines[:2]):
            d.text((tx, yy + 26 + j * 21), ln, font=F_BODY, fill=(60, 60, 66))
        d.text((tx, yy + 68),
               "Source: " + src, font=F_SRC, fill=GOLD)

    # --- footer ---
    fy = y + per_col * row_h + 4
    d.line([(MARGIN, fy), (W - MARGIN, fy)], fill=INK, width=2)
    d.text((MARGIN, fy + 8),
           "16 stories  \u00b7  6 continents  \u00b7  Compiled from wire reports "
           "published on 21 November 2026",
           font=F_FOOT, fill=GREY)
    return img


if __name__ == "__main__":
    import sys

    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    draw().save(out, "PNG", optimize=True)
    print("wrote", out)
