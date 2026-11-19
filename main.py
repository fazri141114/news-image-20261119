#!/usr/bin/env python3
"""
THE WORLD IN ONE PICTURE - Thursday 19 November 2026.

A deterministic, offline program that writes ONE image summing up the
world news of Thursday 19 November 2026 as a vintage newspaper front page.

Rules it honours (make.fun bounty "news-image-20261119"):
  * output is a single 1024x1024 PNG, well under 1 MiB
  * no network access, no randomness, no clock: every run produces
    byte-identical output
  * all content is fixed data in this file (the day's verified stories)

Run:  python3 make_news_image.py [output.png]
"""

import sys
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- fonts
FD = "/usr/share/fonts/truetype"
F_MASTHEAD = f"{FD}/noto/NotoSerifDisplay-Black.ttf"
F_SERIF_B = f"{FD}/liberation/LiberationSerif-Bold.ttf"
F_SERIF = f"{FD}/liberation/LiberationSerif-Regular.ttf"
F_SERIF_I = f"{FD}/liberation/LiberationSerif-Italic.ttf"
F_SANS_B = f"{FD}/liberation/LiberationSans-Bold.ttf"
F_SANS = f"{FD}/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- palette
PAPER = (247, 241, 223)
INK = (27, 23, 17)
RED = (166, 30, 36)
MUTED = (110, 100, 82)
DOT = (186, 176, 148)
GREEN = (28, 104, 58)
BLUE = (34, 66, 138)
GOLD = (198, 148, 38)

W = H = 1024
M = 34                      # page margin
CW = W - 2 * M              # content width = 956


# ---------------------------------------------------------------- helpers
def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
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


def flow(draw, x, y, tokens, max_w, line_h, max_lines=2):
    """
    Render rich text: tokens = [(text, font, fill), ...].
    Words flow across lines; returns y after the last line.
    """
    words = []
    for text, fnt, fill in tokens:
        for w in text.split(" "):
            if w:
                words.append((w, fnt, fill))
    lines, cur, cur_w = [], [], 0.0
    space_w = draw.textlength(" ", font=tokens[0][1])
    for w, fnt, fill in words:
        ww = draw.textlength(w, font=fnt)
        add = ww if not cur else ww + space_w
        if cur and cur_w + add > max_w:
            lines.append(cur)
            cur, cur_w = [(w, fnt, fill)], ww
        else:
            cur.append((w, fnt, fill))
            cur_w += add
    if cur:
        lines.append(cur)
    lines = lines[:max_lines]
    for i, line in enumerate(lines):
        lx = x
        for w, fnt, fill in line:
            draw.text((lx, y + i * line_h), w, font=fnt, fill=fill)
            lx += draw.textlength(w, font=fnt) + draw.textlength(" ", font=fnt)
    return y + len(lines) * line_h


# ---------------------------------------------------------------- content
HEROES = [
    {
        "kicker": "1 · SHENZHEN · SUMMIT",
        "headline": "Trump, Xi and Putin Hold First Trilateral Summit",
        "body": ("The three leaders meet face to face at APEC in Shenzhen. "
                 "Nuclear arms, AI and Iran are on the table; Ukraine is "
                 "pointedly kept off the agenda."),
        "art": "flags",
    },
    {
        "kicker": "2 · VICE CITY · GAMES",
        "headline": "GTA VI Arrives After a 13-Year Wait",
        "body": ("Rockstar's giant launches worldwide to a 99 Metacritic "
                 "score and 15.9 million pre-orders. Take-Two shares jump "
                 "6% as fans return to Vice City."),
        "art": "gta",
    },
    {
        "kicker": "3 · NASDAQ · MARKETS",
        "headline": "Anthropic Opens in History's Largest IPO",
        "body": ("ANT shares begin trading on Nasdaq after pricing at $83 "
                 "valued the AI giant at $1.5 trillion, raising about $81 "
                 "billion - the biggest listing ever."),
        "art": "chart",
    },
]

STATS = [
    ("$81bn", "ANTHROPIC RAISES - LARGEST IPO EVER"),
    ("15.9m", "GTA VI PRE-ORDERS BEFORE LAUNCH"),
    ("99", "GTA VI METACRITIC SCORE"),
    ("200,000", "EVACUATED FOR CYCLONE AKVAN"),
    ("$190.4m", "VAN GOGH AUCTION RECORD, NEW YORK"),
    ("-561", "DOW POINTS AS FED FEARS BITE"),
]

# (headline, one-line summary) - briefs 4..39
BRIEFS = [
    ("WORLD COURT RULES ON ROHINGYA", "ICJ judgment in Gambia v. Myanmar genocide case; 730,000 fled since 2017."),
    ("COP31 INTO FINAL 48 HOURS", "Antalya climate talks stall over a $120bn finance package."),
    ("CYCLONE AKVAN HITS ODISHA", "130 km/h landfall on India's east coast; mass evacuations under way."),
    ("DOW FALLS 561 POINTS", "S&P 500 down a fifth straight day as Fed minutes hint at more hikes."),
    ("WAYMO PULLED FROM FREEWAYS", "California bans driverless taxis from highways as an 'imminent hazard'."),
    ("JEFFRIES NOMINATED FOR SPEAKER", "House Democrats pick Hakeem Jeffries, set to be first Black Speaker."),
    ("STRIKES NEAR HORMUZ", "US-Iran exchanges rattle the Gulf; Brent crude slips to about $91."),
    ("WALMART NEARS $1 TRILLION", "Retail giant reports Q3 before the bell; $187bn revenue expected."),
    ("VAN GOGH FETCHES $190.4M", "Record auction night in New York for the Dutch master."),
    ("VOYAGER 1, ONE LIGHT-DAY OUT", "NASA's farthest probe crosses a new distance milestone."),
    ("CRIMEAN BRIDGE ATTACKED AGAIN", "Kyiv strikes the Kerch link once more; the crossing is closed."),
    ("ISRAELI TANKS CROSS GAZA LINE", "Armour moves west of the Yellow Line despite the ceasefire."),
    ("AUSTRALIA SANCTIONS SETTLERS", "Canberra targets Israeli settlers over West Bank violence."),
    ("CANADA-CHINA DEAL EXTENDED", "Carney resets ties with Beijing as the trade pact is prolonged."),
    ("TANKER HIT OFF BULGARIA", "An LPG carrier is struck by a projectile in the Black Sea."),
    ("SAUDI ALL-CLEAR", "The Kingdom says the danger has passed in three cities after an alert."),
    ("COCAINE SEIZED IN BENGHAZI", "Libyan forces seize a cocaine haul and millions of pills."),
    ("MELENCHON SHAKES FRANCE", "The left leader's surge redraws the French political map."),
    ("EARTH'S MISSING BILLION YEARS", "Geologists close in on the Great Unconformity mystery."),
    ("MODI MEETS THE WALESES", "The Prince and Princess of Wales are received in Delhi."),
    ("BANXICO CUTS RATES", "Mexico's central bank eases policy as inflation cools."),
    ("NEW GREEN-CARD RULES", "Washington tightens checks for US residency applicants."),
    ("SOMALIA ACCUSES THE UAE", "Mogadishu alleges Emirati interference; Abu Dhabi denies it."),
    ("DEUTSCHE'S $582M EPSTEIN BILL", "A settlement adds to the German lender's legal costs."),
    ("PELTOLA WINS IN ALASKA", "The Democrat captures the state's US Senate seat."),
    ("DUCKETT'S 133 FOR ENGLAND", "The opener's century anchors England's day at the crease."),
    ("AIR INDIA 171 REPORT", "Investigators publish findings on the Ahmedabad crash."),
    ("INDIA-JAPAN DEFENCE PACT", "New Delhi and Tokyo deepen military cooperation."),
    ("AMAZON'S $7BN INDIA GREEN PUSH", "A renewables investment is announced for the Indian grid."),
    ("KUMAMOTO QUAKE M5.7", "A tremor rattles Kyushu; no tsunami warning is issued."),
    ("EIGHTH MEASLES DEATH IN PA.", "The US outbreak toll climbs as cases keep spreading."),
    ("COALITION HITS HOUTHI LAUNCHERS", "Strikes target missile sites in Yemen."),
    ("COLOMBIA STRIKE", "A nationwide walkout grips transport and schools."),
    ("NIKKEI UP, GOLD DOWN", "Tokyo climbs 0.55% while gold slides 3% to $3,725."),
    ("'GTA FLU' SWEEPS WORKPLACES", "1.5m Americans expected to call in sick for launch day."),
    ("SHENZHEN DECLARATION SIGNED", "APEC leaders sign off on an AI and trade statement."),
]

DATE_CHECK = ("DATE CHECK - Left out, first reported 18 Nov or earlier: Anthropic's $83 pricing "
              "(set 18 Nov; trading began today) - Iran's drone strikes on US bases (18 Nov) - "
              "Trump's Shenzhen arrival (18 Nov) - Quad maritime deal, Manila (17 Nov). Every story "
              "above was first reported on Thursday 19 November 2026.")

# landmass blobs: (lon, lat, radius_lon, radius_lat) - stylised continents
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
# red markers: (lon, lat, number)
MARKERS = [(114, 22, "1"), (-74, 41, "2"), (4, 52, "4"), (31, 36, "5"),
           (86, 20, "6"), (34, 31, "15")]


def lonlat_to_xy(lon, lat, x0, y0, w, h):
    x = x0 + (lon + 180) / 360.0 * w
    y = y0 + (75 - lat) / 135.0 * h
    return x, y


def draw_map(draw, x0, y0, w, h):
    cols, rows = 118, 18
    for r in range(rows):
        lat = 75 - (r + 0.5) * 135.0 / rows
        for c in range(cols):
            lon = -180 + (c + 0.5) * 360.0 / cols
            inside = any(((lon - lo) / rlo) ** 2 + ((lat - la) / rla) ** 2 <= 1.0
                         for lo, la, rlo, rla in BLOBS)
            if inside:
                x = x0 + (c + 0.5) * w / cols
                y = y0 + (r + 0.5) * h / rows
                draw.ellipse([x - 2.1, y - 2.1, x + 2.1, y + 2.1], fill=DOT)
    f_num = font(F_SANS_B, 10)
    for lon, lat, num in MARKERS:
        x, y = lonlat_to_xy(lon, lat, x0, y0, w, h)
        draw.ellipse([x - 6, y - 6, x + 6, y + 6], fill=RED)
        tw = draw.textlength(num, font=f_num)
        draw.text((x - tw / 2, y - 5.5), num, font=f_num, fill=(255, 252, 240))


def draw_flags(draw, x, y, w, h):
    # three flags on poles over a table line
    pw = (w - 16) // 3
    for i, kind in enumerate(["us", "cn", "ru"]):
        fx = x + i * (pw + 8)
        draw.line([(fx + 3, y), (fx + 3, y + h)], fill=INK, width=2)
        bx, by, bw, bh = fx + 5, y + 2, pw - 6, int(h * 0.62)
        if kind == "us":
            for s in range(7):
                col = RED if s % 2 == 0 else (252, 250, 244)
                draw.rectangle([bx, by + s * bh // 7, bx + bw, by + (s + 1) * bh // 7], fill=col)
            draw.rectangle([bx, by, bx + bw * 0.45, by + bh * 4 // 7], fill=BLUE)
            for r_ in range(3):
                for c_ in range(4):
                    cx, cy = bx + 5 + c_ * 9, by + 4 + r_ * 8
                    draw.ellipse([cx - 1.4, cy - 1.4, cx + 1.4, cy + 1.4], fill=(252, 250, 244))
        elif kind == "cn":
            draw.rectangle([bx, by, bx + bw, by + bh], fill=RED)
            for dx, dy, rr in [(10, 9, 3.4), (22, 5, 1.8), (25, 12, 1.8), (25, 19, 1.8), (21, 25, 1.8)]:
                draw.ellipse([bx + dx - rr, by + dy - rr, bx + dx + rr, by + dy + rr], fill=GOLD)
        else:
            draw.rectangle([bx, by, bx + bw, by + bh // 3], fill=(252, 250, 244))
            draw.rectangle([bx, by + bh // 3, bx + bw, by + 2 * bh // 3], fill=BLUE)
            draw.rectangle([bx, by + 2 * bh // 3, bx + bw, by + bh], fill=RED)
        draw.rectangle([bx, by, bx + bw, by + bh], outline=INK, width=1)
    draw.line([(x, y + h - 4), (x + w, y + h - 4)], fill=INK, width=3)


def draw_gta(draw, x, y, w, h):
    bands = [(250, 166, 84), (244, 128, 92), (214, 84, 110), (122, 62, 118), (52, 38, 84)]
    bh = h // len(bands)
    for i, col in enumerate(bands):
        draw.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh + 1], fill=col)
    sun_x, sun_y = x + w * 0.30, y + h * 0.52
    draw.ellipse([sun_x - 15, sun_y - 15, sun_x + 15, sun_y + 15], fill=(252, 214, 120))
    # skyline
    base = y + h
    for bx, bw_, bh_ in [(0, 26, 20), (30, 18, 30), (52, 30, 15), (86, 20, 36), (110, 26, 22),
                         (140, 18, 28), (162, 30, 17), (196, 22, 33), (222, 26, 20), (252, 20, 27)]:
        draw.rectangle([x + bx, base - bh_, x + bx + bw_, base], fill=(20, 14, 24))
    # palm: trunk + fronds (simple curved lines)
    px, py = x + w * 0.66, base
    top = (px + 7, py - 30)
    draw.line([(px, py), top], fill=(20, 14, 24), width=3)
    for ex, ey in [(top[0] - 17, top[1] + 7), (top[0] - 10, top[1] - 4),
                   (top[0], top[1] - 8), (top[0] + 11, top[1] - 4),
                   (top[0] + 18, top[1] + 7)]:
        mx, my = (top[0] + ex) / 2, min(top[1], ey) - 6
        pts = []
        for t in range(9):
            f = t / 8.0
            qx = (1 - f) ** 2 * top[0] + 2 * (1 - f) * f * mx + f ** 2 * ex
            qy = (1 - f) ** 2 * top[1] + 2 * (1 - f) * f * my + f ** 2 * ey
            pts.append((qx, qy))
        draw.line(pts, fill=(20, 14, 24), width=2)
    f_vi = font(F_SERIF_B, 34)
    draw.text((x + w - 52, y + h - 42), "VI", font=f_vi, fill=(255, 252, 240))


def draw_chart(draw, x, y, w, h):
    base = y + h - 6
    draw.line([(x + 6, y + 4), (x + 6, base), (x + w - 4, base)], fill=INK, width=2)
    bars = [0.30, 0.44, 0.58, 0.80]
    bw = (w - 40) // 4
    for i, frac in enumerate(bars):
        bx = x + 16 + i * (bw + 6)
        bh_ = int((h - 16) * frac)
        draw.rectangle([bx, base - bh_, bx + bw, base], fill=GREEN)
    pts = [(x + 16 + bw // 2, base - int((h - 16) * 0.30)),
           (x + 16 + (bw + 6) + bw // 2, base - int((h - 16) * 0.44)),
           (x + 16 + 2 * (bw + 6) + bw // 2, base - int((h - 16) * 0.58)),
           (x + 16 + 3 * (bw + 6) + bw // 2, base - int((h - 16) * 0.80))]
    draw.line(pts, fill=RED, width=3)
    ex, ey = pts[-1]
    draw.polygon([(ex, ey), (ex - 11, ey + 1), (ex - 2, ey + 10)], fill=RED)
    f_d = font(F_SERIF_B, 26)
    draw.text((x + 14, y + 2), "$", font=f_d, fill=GREEN)


ART = {"flags": draw_flags, "gta": draw_gta, "chart": draw_chart}


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "news-2026-11-19.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top strip
    f_small = font(F_SANS_B, 12)
    d.text((M, 24), "No. 39 - ONE PAGE", font=f_small, fill=INK)
    right = "SHENZHEN - NEW YORK - THE HAGUE"
    d.text((W - M - d.textlength(right, font=f_small), 24), right, font=f_small, fill=INK)
    mid = "EST. MMXXVI"
    centered(d, W / 2, 24, mid, f_small, MUTED)
    rule(d, 46, width=3)
    rule(d, 52, width=1)

    # ---- masthead
    f_mast = font(F_MASTHEAD, 63)
    centered(d, W / 2, 60, "THE WORLD IN ONE PICTURE", f_mast)
    f_date = font(F_SERIF_B, 20)
    d.text((M, 138), "Thursday 19 November 2026", font=f_date, fill=RED)
    f_cnt = font(F_SANS_B, 15)
    cnt = "39 STORIES - 6 CONTINENTS - ONE PAGE"
    d.text((W - M - d.textlength(cnt, font=f_cnt), 141), cnt, font=f_cnt, fill=INK)
    rule(d, 168, width=1)

    # ---- stat strip
    f_stat = font(F_SERIF_B, 25)
    f_lab = font(F_SANS_B, 9)
    col_w = CW / 6
    for i, (num, lab) in enumerate(STATS):
        cx = M + col_w * i + col_w / 2
        centered(d, cx, 178, num, f_stat)
        for j, ln in enumerate(wrap(d, lab, f_lab, col_w - 12)):
            centered(d, cx, 208 + j * 11, ln, f_lab, MUTED)
        if i:
            d.line([(M + col_w * i, 180), (M + col_w * i, 226)], fill=MUTED, width=1)
    rule(d, 234, width=1)

    # ---- heroes
    hy = 246
    hcol_w = (CW - 2 * 18) / 3
    f_kick = font(F_SANS_B, 12)
    f_head = font(F_SERIF_B, 22)
    f_body = font(F_SERIF, 13)
    for i, hero in enumerate(HEROES):
        hx = M + i * (hcol_w + 18)
        d.text((hx, hy), hero["kicker"], font=f_kick, fill=RED)
        yy = hy + 20
        for ln in wrap(d, hero["headline"], f_head, hcol_w)[:3]:
            d.text((hx, yy), ln, font=f_head, fill=INK)
            yy += 26
        ART[hero["art"]](d, int(hx), yy + 2, int(hcol_w), 54)
        yy += 62
        for ln in wrap(d, hero["body"], f_body, hcol_w)[:4]:
            d.text((hx, yy), ln, font=f_body, fill=INK)
            yy += 16.5
        if i:
            d.line([(hx - 9, hy), (hx - 9, hy + 218)], fill=MUTED, width=1)
    rule(d, 472, width=1)

    # ---- map strip
    f_map = font(F_SANS_B, 11)
    d.text((M, 480), "WHERE IT HAPPENED", font=f_map, fill=INK)
    note = "numbered pins match the stories"
    d.text((W - M - d.textlength(note, font=font(F_SERIF_I, 12)), 479), note,
           font=font(F_SERIF_I, 12), fill=MUTED)
    draw_map(d, M, 496, CW, 88)
    rule(d, 590, width=1)

    # ---- briefs header
    f_bh = font(F_SANS_B, 13)
    centered(d, W / 2, 598, "THE WORLD IN BRIEF - 36 MORE STORIES", f_bh, RED)
    rule(d, 618, width=1)

    # ---- briefs: 3 columns x 12 rows
    f_num = font(F_SANS_B, 11)
    f_bhead = font(F_SERIF_B, 11)
    f_bbody = font(F_SERIF, 11)
    bcol_w = (CW - 2 * 18) / 3
    by = 626
    row_h = 27.5
    for idx, (head, body) in enumerate(BRIEFS):
        col, row = divmod(idx, 12)
        bx = M + col * (bcol_w + 18)
        yy = by + row * row_h
        tokens = [(f"{idx + 4} ", f_num, RED), (head + " - ", f_bhead, INK), (body, f_bbody, INK)]
        flow(d, bx, yy, tokens, bcol_w, 13.5, max_lines=2)

    # ---- footer: date check
    fy = 614 + 12 * row_h + 6
    rule(d, fy, width=1)
    f_foot = font(F_SERIF_I, 10.5)
    yy = fy + 6
    for ln in wrap(d, DATE_CHECK, f_foot, CW)[:3]:
        d.text((M, yy), ln, font=f_foot, fill=MUTED)
        yy += 13
    f_sign = font(F_SANS_B, 10)
    sign = "SET BY A DETERMINISTIC PROGRAM - NO NETWORK, NO RANDOMNESS: RUN IT TWICE, GET THE SAME BYTES - @fazri141114"
    centered(d, W / 2, yy + 2, sign, f_sign, INK)

    img.save(out, format="PNG")
    print("wrote", out)


if __name__ == "__main__":
    main()
