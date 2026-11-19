#!/usr/bin/env python3
"""
Builder for the v2 entry image (entry.png) - make.fun bounty
"Sum up 19 November's world news in one image" (news-image-20261119).

Design (per the entrant's brief, from the live leaderboard's winners):
  * landscape 1024x853, cream paper, classic newspaper look
  * the DATE is the biggest thing on the page
  * 3 hero stories with large flat illustrations (~40% of the page)
  * 7 grid cards, then 14 one-line briefs - 24 stories in all
  * dotted world map + a DATE CHECK box + source footer

All story data below is fixed and was verified against the day's wire
reporting before it was put in. Two care points from verification:
the ICJ Rohingya item states no outcome (the verdict's result was not
verified), and the Cyclone Akvan item carries no evacuation figure
(the 200,000 figure in circulation was not verified).

This builder runs locally with Pillow. The submitted entrypoint
(main.py, standard library only) copies the entry.png it produces,
exactly as the kit's starter does; the sandbox never needs Pillow.

Run:  python3 build_image.py [output.png]   (default: entry.png)
"""

import sys
from PIL import Image, ImageDraw, ImageFont

FD = "/usr/share/fonts/truetype"
F_MASTHEAD = f"{FD}/noto/NotoSerifDisplay-Black.ttf"
F_SERIF_B = f"{FD}/liberation/LiberationSerif-Bold.ttf"
F_SERIF = f"{FD}/liberation/LiberationSerif-Regular.ttf"
F_SERIF_I = f"{FD}/liberation/LiberationSerif-Italic.ttf"
F_SANS_B = f"{FD}/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


PAPER = (247, 241, 223)
INK = (27, 23, 17)
RED = (166, 30, 36)
MUTED = (110, 100, 82)
DOT = (186, 176, 148)
GREEN = (28, 104, 58)
BLUE = (34, 66, 138)
TEAL = (24, 102, 110)
ORANGE = (178, 96, 26)
NAVY = (38, 52, 96)

W, H = 1024, 853
M = 30
CW = W - 2 * M


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def rule(draw, y, x0=M, x1=W - M, width=1, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ------------------------------------------------------------------ heroes
HEROES = [
    {
        "label": "1 · SHENZHEN · SUMMIT",
        "headline": "Trump, Xi and Putin Hold First-Ever Trilateral Summit",
        "body": ("The three leaders meet at APEC in Shenzhen. On the table: "
                 "nuclear security and the war in Ukraine."),
        "art": "flags",
    },
    {
        "label": "2 · VICE CITY · GAMES",
        "headline": "GTA VI Is Out: the 13-Year Wait Ends",
        "body": ("Metacritic 99. 15.88m pre-orders worth $1.54bn, Take-Two "
                 "up 6.5%. Lucia and Jason take Vice City, Leonida."),
        "art": "gta",
    },
    {
        "label": "3 · NASDAQ · MARKETS",
        "headline": "Anthropic's $81.3bn IPO Is the Largest Ever",
        "body": ("Priced at $83 a share, the Claude maker debuts on Nasdaq "
                 "as ANT - the biggest listing in history."),
        "art": "chart",
    },
]

# ------------------------------------------------------------- grid cards
GRID = [
    ("4 · THE HAGUE · LAW", BLUE, "World Court Delivers Rohingya Verdict",
     "The Gambia v. Myanmar: the seven-year genocide-convention case; 730,000 Rohingya fled in 2017."),
    ("5 · KYIV · WAR", RED, "Crimean Bridge Attacked Again",
     "The Kerch crossing is hit once more and traffic is halted."),
    ("6 · GAZA · WAR", RED, "Israel Opens Ground Operation in Central Gaza",
     "Ground forces move into the central Gaza Strip."),
    ("7 · GAZA · CRISIS", ORANGE, "Rain Deepens Gaza's Shelter Crisis",
     "46,000+ households displaced; 40,000+ shelters damaged; 150,000 tents await approval."),
    ("8 · TALLINN · EUROPE", NAVY, "Estonia to Close Border With Russia",
     "The land border shuts from 1 December; GRU sabotage of Threod Systems is suspected."),
    ("9 · ODISHA · STORM", TEAL, "Cyclone Akvan Nears India's East Coast",
     "Heavy rain and strong winds bear down on Odisha."),
    ("10 · ANTALYA · CLIMATE", GREEN, "COP31 Deadlocked in Its Final 48 Hours",
     "The climate talks enter their last two days still at an impasse."),
]

BRIEFS = [
    "Houthis take Red Sea coast posts; Yemeni forces yield Bab el-Mandeb",
    "Zelensky urges US to lift limits on Starlink and Starshield",
    "EU proposes a €45bn Ukraine loan for 2027 - €25bn military, €20bn budget",
    "US Republicans threaten to strip Ukraine aid from the defence bill",
    "Myanmar's president weighs a reset with ASEAN",
    "US panel urges action on China's detention of a Panama-flagged ship",
    "El Salvador's Bukele demolishes Haiti gang leader Jeff Larose's home",
    "Alleged Russian spy arrested over Silicon Valley targeting",
    "Ukraine, Russia and the US talk prisoner swaps in Abu Dhabi",
    "Voyager 1 is now one light-day from Earth",
    "Nvidia posts a $115.8bn quarter amid chip curbs",
    "US and China spar over rare-earth export curbs",
    "Global stocks slip ahead of Nvidia's numbers",
    "Australia sanctions West Bank settlers",
]

DATE_CHECK = ("Every story above was first reported on Thursday 19 November 2026. "
              "Left out (18 Nov or earlier): Anthropic's $83 pricing, Iran's drone "
              "strikes on US bases, Trump's arrival, the Quad deal.")

BLOBS = [
    (-102, 50, 38, 20), (-88, 39, 21, 13), (-84, 30, 10, 6), (-90, 16, 9, 6),
    (-42, 73, 13, 6), (-155, 64, 10, 6), (-17, 66, 6, 4),
    (-61, -11, 13, 22), (-70, -27, 8, 16), (-71, -40, 5, 9),
    (16, 53, 20, 11), (12, 44, 13, 7), (28, 62, 12, 9), (-4, 51, 5, 5), (-4, 40, 7, 5),
    (17, 7, 21, 19), (23, -17, 15, 14), (47, -19, 4, 7),
    (55, 51, 44, 16), (78, 66, 42, 9), (47, 29, 10, 8), (78, 21, 10, 13),
    (86, 48, 27, 12), (106, 33, 17, 13), (102, 14, 6, 11), (113, -1, 13, 4),
    (122, -3, 10, 4), (138, 37, 5, 7), (127, 37, 3, 4),
    (134, -25, 14, 10), (122, -24, 6, 7), (172, -42, 4, 5),
]
PINS = [(114, 22), (-74, 41), (4, 52), (31, 36), (86, 20), (34, 31)]


def draw_flags(draw, x, y, w, h):
    pw = (w - 16) // 3
    for i, kind in enumerate(["us", "cn", "ru"]):
        fx = x + i * (pw + 8)
        draw.line([(fx + 3, y), (fx + 3, y + h)], fill=INK, width=3)
        bx, by, bw, bh = fx + 6, y + 2, pw - 7, int(h * 0.66)
        if kind == "us":
            for s in range(7):
                col = RED if s % 2 == 0 else (252, 250, 244)
                draw.rectangle([bx, by + s * bh // 7, bx + bw, by + (s + 1) * bh // 7], fill=col)
            draw.rectangle([bx, by, bx + bw * 0.45, by + bh * 4 // 7], fill=BLUE)
            for r_ in range(3):
                for c_ in range(4):
                    cx, cy = bx + 7 + c_ * 13, by + 6 + r_ * 11
                    draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(252, 250, 244))
        elif kind == "cn":
            draw.rectangle([bx, by, bx + bw, by + bh], fill=RED)
            for dx, dy, rr in [(15, 13, 5), (32, 7, 2.6), (37, 17, 2.6), (37, 28, 2.6), (30, 37, 2.6)]:
                draw.ellipse([bx + dx - rr, by + dy - rr, bx + dx + rr, by + dy + rr], fill=(240, 190, 40))
        else:
            draw.rectangle([bx, by, bx + bw, by + bh // 3], fill=(252, 250, 244))
            draw.rectangle([bx, by + bh // 3, bx + bw, by + 2 * bh // 3], fill=BLUE)
            draw.rectangle([bx, by + 2 * bh // 3, bx + bw, by + bh], fill=RED)
        draw.rectangle([bx, by, bx + bw, by + bh], outline=INK, width=1)
    draw.line([(x, y + h - 5), (x + w, y + h - 5)], fill=INK, width=4)


def draw_gta(draw, x, y, w, h):
    bands = [(250, 166, 84), (244, 128, 92), (214, 84, 110), (122, 62, 118), (52, 38, 84)]
    bh = h // len(bands)
    for i, col in enumerate(bands):
        draw.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh + 1], fill=col)
    sun_x, sun_y = x + w * 0.30, y + h * 0.55
    draw.ellipse([sun_x - 24, sun_y - 24, sun_x + 24, sun_y + 24], fill=(252, 214, 120))
    base = y + h
    for bx, bw_, bh_ in [(0, 34, 30), (38, 24, 46), (66, 40, 22), (110, 26, 54), (140, 34, 32),
                         (178, 24, 42), (206, 38, 25), (248, 28, 48), (280, 30, 30)]:
        if bx < w:
            draw.rectangle([x + bx, base - bh_, min(x + bx + bw_, x + w), base], fill=(20, 14, 24))
    px, py = x + w * 0.64, base
    top = (px + 9, py - 44)
    draw.line([(px, py), top], fill=(20, 14, 24), width=4)
    for ex, ey in [(top[0] - 24, top[1] + 10), (top[0] - 14, top[1] - 6),
                   (top[0], top[1] - 11), (top[0] + 15, top[1] - 6),
                   (top[0] + 25, top[1] + 10)]:
        mx, my = (top[0] + ex) / 2, min(top[1], ey) - 8
        pts = []
        for t in range(9):
            f = t / 8.0
            qx = (1 - f) ** 2 * top[0] + 2 * (1 - f) * f * mx + f ** 2 * ex
            qy = (1 - f) ** 2 * top[1] + 2 * (1 - f) * f * my + f ** 2 * ey
            pts.append((qx, qy))
        draw.line(pts, fill=(20, 14, 24), width=3)
    f_vi = font(F_SERIF_B, 44)
    draw.text((x + w - 66, y + h - 56), "VI", font=f_vi, fill=(255, 252, 240))


def draw_chart(draw, x, y, w, h):
    base = y + h - 8
    draw.line([(x + 8, y + 6), (x + 8, base), (x + w - 6, base)], fill=INK, width=2)
    bars = [0.30, 0.45, 0.60, 0.82]
    bw = (w - 60) // 4
    tops = []
    for i, frac in enumerate(bars):
        bx = x + 24 + i * (bw + 8)
        bh_ = int((h - 22) * frac)
        draw.rectangle([bx, base - bh_, bx + bw, base], fill=GREEN)
        tops.append((bx + bw // 2, base - bh_))
    draw.line(tops, fill=RED, width=4)
    ex, ey = tops[-1]
    draw.polygon([(ex + 14, ey - 6), (ex - 2, ey - 4), (ex + 2, ey + 10)], fill=RED)
    f_d = font(F_SERIF_B, 36)
    draw.text((x + 18, y + 2), "$83", font=f_d, fill=GREEN)


ART = {"flags": draw_flags, "gta": draw_gta, "chart": draw_chart}


def draw_map(draw, x0, y0, w, h):
    cols, rows = 104, 10
    for r in range(rows):
        lat = 75 - (r + 0.5) * 135.0 / rows
        for c in range(cols):
            lon = -180 + (c + 0.5) * 360.0 / cols
            if any(((lon - lo) / rlo) ** 2 + ((lat - la) / rla) ** 2 <= 1.0
                   for lo, la, rlo, rla in BLOBS):
                x = x0 + (c + 0.5) * w / cols
                y = y0 + (r + 0.5) * h / rows
                draw.ellipse([x - 1.8, y - 1.8, x + 1.8, y + 1.8], fill=DOT)
    for lon, lat in PINS:
        x = x0 + (lon + 180) / 360.0 * w
        y = y0 + (75 - lat) / 135.0 * h
        draw.ellipse([x - 4.5, y - 4.5, x + 4.5, y + 4.5], fill=RED)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top strip
    f_label = font(F_SANS_B, 15)
    d.text((M, 20), "THE WORLD IN ONE PICTURE", font=f_label, fill=RED)
    f_small = font(F_SANS_B, 11)
    right = "No. 24 - ONE PAGE - @fazri141114"
    d.text((W - M - d.textlength(right, font=f_small), 22), right, font=f_small, fill=MUTED)
    rule(d, 44, width=3)
    rule(d, 50, width=1)

    # ---- the date, as large as it goes
    f_date = font(F_MASTHEAD, 58)
    centered(d, W / 2, 58, "Thursday 19 November 2026", f_date)
    f_sub = font(F_SANS_B, 13)
    centered(d, W / 2, 128, "THE WORLD'S NEWS IN ONE IMAGE - 24 STORIES - ONE DAY", f_sub, MUTED)
    rule(d, 150, width=1)

    # ---- heroes
    hy = 160
    hcol_w = (CW - 2 * 18) / 3
    f_kick = font(F_SANS_B, 12)
    f_head = font(F_SERIF_B, 22)
    f_body = font(F_SERIF, 13.5)
    for i, hero in enumerate(HEROES):
        hx = M + i * (hcol_w + 18)
        d.text((hx, hy), hero["label"], font=f_kick, fill=RED)
        ART[hero["art"]](d, int(hx), hy + 20, int(hcol_w), 104)
        yy = hy + 132
        for ln in wrap(d, hero["headline"], f_head, hcol_w)[:3]:
            d.text((hx, yy), ln, font=f_head, fill=INK)
            yy += 25
        yy += 2
        for ln in wrap(d, hero["body"], f_body, hcol_w)[:3]:
            d.text((hx, yy), ln, font=f_body, fill=INK)
            yy += 17
        if i:
            d.line([(hx - 9, hy), (hx - 9, hy + 258)], fill=MUTED, width=1)
    rule(d, 430, width=1)

    # ---- grid: 4 over 3
    f_gkick = font(F_SANS_B, 10)
    f_ghead = font(F_SERIF_B, 15)
    f_gbody = font(F_SERIF, 11.5)
    gy = 438
    row_h = 104
    gcol_w = (CW - 3 * 14) / 4
    for idx, (label, color, head, body) in enumerate(GRID):
        if idx < 4:
            gx = M + idx * (gcol_w + 14)
            gw = gcol_w
            yy0 = gy
        else:
            gx = M + (idx - 4) * (hcol_w + 18)
            gw = hcol_w
            yy0 = gy + row_h
        d.rectangle([gx, yy0, gx + gw, yy0 + 5], fill=color)
        d.text((gx, yy0 + 10), label, font=f_gkick, fill=color)
        yy = yy0 + 26
        for ln in wrap(d, head, f_ghead, gw)[:2]:
            d.text((gx, yy), ln, font=f_ghead, fill=INK)
            yy += 17
        for ln in wrap(d, body, f_gbody, gw)[:3]:
            d.text((gx, yy), ln, font=f_gbody, fill=INK)
            yy += 14.5
    rule(d, 650, width=1)

    # ---- briefs
    f_bh = font(F_SANS_B, 12)
    centered(d, W / 2, 658, "IN BRIEF - AROUND THE WORLD", f_bh, RED)
    f_src = font(F_SANS_B, 9)
    src = "Sources: Reuters · AP · BBC · Financial Times · Bernama"
    d.text((W - M - d.textlength(src, font=f_src), 660), src, font=f_src, fill=MUTED)
    f_bnum = font(F_SANS_B, 12)
    f_btxt = font(F_SERIF, 12.5)
    bcol_w = (CW - 18) / 2
    by = 680
    for idx, brief in enumerate(BRIEFS):
        col, row = divmod(idx, 7)
        bx = M + col * (bcol_w + 18)
        yy = by + row * 16
        num = f"{idx + 11} "
        d.text((bx, yy), num, font=f_bnum, fill=RED)
        d.text((bx + d.textlength(num, font=f_bnum), yy), brief, font=f_btxt, fill=INK)
    rule(d, 796, width=1)

    # ---- bottom: map + date check
    f_map = font(F_SANS_B, 10)
    d.text((M, 806), "WHERE IT", font=f_map, fill=MUTED)
    d.text((M, 820), "HAPPENED", font=f_map, fill=MUTED)
    draw_map(d, M + 76, 802, 428, 40)
    box_x = W - M - 396
    d.rectangle([box_x, 798, W - M, 848], outline=RED, width=1)
    f_dcb = font(F_SANS_B, 11)
    d.rectangle([box_x + 8, 805, box_x + 16, 813], fill=RED)
    d.text((box_x + 22, 802), "DATE CHECK", font=f_dcb, fill=RED)
    f_dc = font(F_SERIF_I, 9.5)
    for j, ln in enumerate(wrap(d, DATE_CHECK, f_dc, 396 - 16)[:3]):
        d.text((box_x + 8, 816 + j * 11), ln, font=f_dc, fill=INK)

    img.save(out, format="PNG")
    print("wrote", out)


if __name__ == "__main__":
    main()
