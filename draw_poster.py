#!/usr/bin/env python3
"""Poster builder for the make.fun news-image-20261125 entry.

Draws "THE WORLD IN ONE PAGE — Wednesday 25 November 2026" in the DUSK
style: a dark slate broadsheet carrying the 38 verified stories locked in
FINAL38_20261125.md (3 heroes, 12 grid cells, 23 ticker lines), a numbered
dot-grid world map, a UTC timeline, a numbers strip and a DATE CHECK box.
All artwork is original and drawn programmatically with Pillow.

Outputs poster_full.png (2048x2660 design render) and entry.png, the same
poster scaled to fit the competition's 1024x1024 / 1 MiB limits.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
DISPLAY_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

PAGE_W, PAGE_H = 2048, 2660
MARGIN = 56

# DUSK palette
SLATE = (21, 32, 43)          # page background #15202B
PANEL_BG = (31, 47, 61)       # hero / grid panels #1F2F3D
PANEL_EDGE = (110, 130, 145)  # panel lines #6E8291
GOLD = (217, 164, 65)         # #D9A441
IVORY = (240, 236, 224)       # headlines #F0ECE0
BODY = (198, 208, 216)        # body text #C6D0D8
FAINT = (165, 179, 190)       # attribution #A5B3BE
DIVIDER = (96, 116, 132)      # separators #607484
CORAL = (230, 120, 100)       # number tokens / strap #E67864
INK = (24, 24, 24)
WHITE = (255, 255, 255)
ALERT = (196, 70, 58)         # pins, CLAIM chip #C4463A
ALERT_DARK = (146, 32, 32)    # DATE CHECK header #922020
ALERT_EDGE = (200, 90, 80)    # DATE CHECK frame #C85A50

TAG_FILL = {
    "CONFIRMED": (38, 120, 112),   # #267870
    "OFFICIAL": (70, 110, 170),    # #466EAA
    "REPORTED": (178, 128, 44),    # #B2802C
    "CLAIM": (196, 70, 58),        # #C4463A
}

canvas = Image.new("RGB", (PAGE_W, PAGE_H), SLATE)
pen = ImageDraw.Draw(canvas)


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(txt, fnt):
    return pen.textlength(txt, font=fnt)


def wrap_lines(txt, fnt, max_w):
    """Greedy word wrap; returns the list of lines that fit max_w."""
    out, current = [], ""
    for word in txt.split():
        trial = (current + " " + word).strip()
        if text_w(trial, fnt) <= max_w:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def shrink_to_fit(txt, path, size, max_w, floor=12):
    """Largest font at or below size whose single line fits max_w."""
    s = size
    while s > floor and text_w(txt, font(path, s)) > max_w:
        s -= 1
    return font(path, s)


def tag_chip(x, y, label, size=21):
    fnt = font(SANS_BOLD, size)
    w = text_w(label, fnt) + 22
    pen.rounded_rectangle([x, y, x + w, y + size + 14], radius=6,
                          fill=TAG_FILL[label])
    pen.text((x + 11, y + 6), label, font=fnt, fill=WHITE)
    return w


def gold_badge(x, y, number, radius=21):
    pen.ellipse([x, y, x + 2 * radius, y + 2 * radius], fill=GOLD)
    label = str(number)
    fnt = font(SANS_BOLD, 24 if number < 10 else 20)
    pen.text((x + radius - text_w(label, fnt) / 2, y + radius - 13),
             label, font=fnt, fill=INK)


def tracked_line(cx, y, txt, fnt, fill, tracking=6):
    """Draw text centred on cx with extra space between characters."""
    widths = [text_w(ch, fnt) for ch in txt]
    total = sum(widths) + tracking * (len(txt) - 1)
    x = cx - total / 2
    for ch, w in zip(txt, widths):
        pen.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


# ---------------------------------------------------------------- top bar
pen.rectangle([0, 0, PAGE_W, 64], fill=(10, 16, 22))
pen.rectangle([0, 64, PAGE_W, 68], fill=GOLD)
bar_f = font(SANS_BOLD, 29)
pen.text((MARGIN, 17), "THE WORLD IN ONE PAGE", font=bar_f, fill=WHITE)
centre = "38 STORIES · 5 REGIONS"
pen.text(((PAGE_W - text_w(centre, bar_f)) / 2, 17), centre,
         font=bar_f, fill=WHITE)
right = "EVERY STORY DATED WEDNESDAY 25 NOV"
pen.text((PAGE_W - MARGIN - text_w(right, bar_f), 17), right,
         font=bar_f, fill=WHITE)

# ---------------------------------------------------------------- masthead
masthead = "WEDNESDAY 25 NOVEMBER 2026"
mf = shrink_to_fit(masthead, DISPLAY_BOLD, 104,
                   PAGE_W - 2 * MARGIN - 6 * len(masthead))
tracked_line(PAGE_W / 2, 92, masthead, mf, GOLD, tracking=6)
pen.rectangle([MARGIN, 218, PAGE_W - MARGIN, 224], fill=GOLD)
pen.rectangle([MARGIN, 230, PAGE_W - MARGIN, 233], fill=PANEL_EDGE)

# ---------------------------------------------------------------- strap
strap = ("Iran says 2 more tankers hit mines in Hormuz — Asia's AI sell-off "
         "deepens — Zeeshan Ali boards Tiangong")
sf = shrink_to_fit(strap, SERIF, 37, PAGE_W - 2 * MARGIN)
pen.text(((PAGE_W - text_w(strap, sf)) / 2, 246), strap, font=sf, fill=CORAL)

# ---------------------------------------------------------------- region bar
region_segments = [
    ("ASIA-PACIFIC 10", (38, 110, 104)),    # teal #266E68
    ("EUROPE 11", (138, 109, 59)),          # ochre #8A6D3B
    ("AMERICAS 13", (150, 52, 46)),         # red #96342E
    ("MIDDLE EAST 2", (186, 96, 44)),       # orange #BA602C
    ("AFRICA 2", (110, 84, 140)),           # purple #6E548C
]
seg_w = (PAGE_W - 2 * MARGIN) / len(region_segments)
rf = font(SANS_BOLD, 28)
for i, (label, colour) in enumerate(region_segments):
    x0 = MARGIN + i * seg_w
    pen.rectangle([x0, 300, x0 + seg_w - 4, 348], fill=colour)
    pen.text((x0 + (seg_w - 4 - text_w(label, rf)) / 2, 310), label,
             font=rf, fill=WHITE)

# ---------------------------------------------------------------- timeline
timeline_text = (
    "00:18 Shenzhou-24 lifts off · 03:56 docks with Tiangong · 06:30 "
    "Colombia: all Cartagena hostages free · 13:30 US releases PCE, GDP & "
    "jobless claims · 15:00 Army detonates lead azide in Iowa · 18:30 "
    "Feijóo fills Madrid's Caja Mágica")
pen.rectangle([MARGIN, 364, MARGIN + 232, 428], fill=GOLD)
pen.text((MARGIN + 13, 384), "THE DAY IN UTC", font=font(SANS_BOLD, 23),
         fill=INK)
tl_f = font(SANS, 23)
tl_y = 368
for line in wrap_lines(timeline_text, tl_f, PAGE_W - 2 * MARGIN - 254)[:2]:
    pen.text((MARGIN + 250, tl_y), line, font=tl_f, fill=IVORY)
    tl_y += 28

# ---------------------------------------------------------------- numbers strip
numbers = [
    ("+4.3%", "US Q3 GDP"),
    ("3.8%", "PCE INFLATION"),
    ("189,000", "JOBLESS CLAIMS"),
    ("−6.16%", "KOSPI CLOSE"),
    ("81.5M", "THANKSGIVING TRAVELERS"),
    ("490,334", "RUSSIAN WAR DEATHS"),
    ("€199.7bn", "EU 2027 BUDGET"),
    ("$58,000", "BITCOIN BREAKS BELOW"),
]
NUM_Y = 448
cell_w = (PAGE_W - 2 * MARGIN) / len(numbers)
for i, (big, label) in enumerate(numbers):
    x0 = MARGIN + i * cell_w
    if i:
        pen.line([x0, NUM_Y + 6, x0, NUM_Y + 84], fill=DIVIDER, width=2)
    bf = shrink_to_fit(big, SERIF_BOLD, 50, cell_w - 16)
    pen.text((x0 + (cell_w - text_w(big, bf)) / 2, NUM_Y), big,
             font=bf, fill=IVORY)
    lf = shrink_to_fit(label, SANS_BOLD, 19, cell_w - 12, floor=13)
    pen.text((x0 + (cell_w - text_w(label, lf)) / 2, NUM_Y + 62), label,
             font=lf, fill=FAINT)
pen.line([MARGIN, NUM_Y + 100, PAGE_W - MARGIN, NUM_Y + 100],
         fill=DIVIDER, width=3)

# ---------------------------------------------------------------- heroes
HERO_Y, HERO_H = 572, 412
HERO_W = (PAGE_W - 2 * MARGIN - 2 * 20) / 3


def paint_hormuz(x, y, w, h):
    """Dusk roadstead: tanker silhouette, sea mines, red banner."""
    pen.rectangle([x, y, x + w, y + h], fill=(233, 206, 168))
    pen.rectangle([x, y + h - 52, x + w, y + h], fill=(43, 84, 118))
    pen.polygon([(x + 90, y + h - 52), (x + 120, y + h - 26),
                 (x + 420, y + h - 26), (x + 450, y + h - 52)],
                fill=(60, 60, 60))
    pen.rectangle([x + 150, y + h - 84, x + 210, y + h - 52], fill=(90, 90, 90))
    box_colours = [(179, 49, 42), (52, 84, 140), (150, 105, 30),
                   (31, 95, 95), (120, 92, 40)]
    for i, colour in enumerate(box_colours):
        pen.rectangle([x + 225 + i * 38, y + h - 76,
                       x + 258 + i * 38, y + h - 54], fill=colour)
    for mx, my in [(500, h - 34), (545, h - 18)]:
        cx, cy = x + mx, y + my
        pen.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=INK)
        for angle in range(0, 360, 45):
            dx = math.cos(math.radians(angle))
            dy = math.sin(math.radians(angle))
            pen.line([cx + dx * 12, cy + dy * 12, cx + dx * 19, cy + dy * 19],
                     fill=INK, width=3)
    pen.rectangle([x + w - 218, y + 12, x + w - 12, y + 52], fill=ALERT)
    pen.text((x + w - 202, y + 19), "2 MORE HIT", font=font(SANS_BOLD, 26),
             fill=WHITE)
    pen.text((x + 16, y + 12), "STRAIT OF HORMUZ", font=font(SANS_BOLD, 24),
             fill=INK)


def paint_selloff(x, y, w, h):
    """Falling index line on a deep-green chart panel."""
    pen.rectangle([x, y, x + w, y + h], fill=(16, 52, 52))
    for step in range(1, 5):
        gy = y + step * h / 5
        pen.line([x + 14, gy, x + w - 14, gy], fill=(40, 90, 90), width=1)
    pen.text((x + 16, y + 10), "AI", font=font(SANS_BOLD, 26),
             fill=(140, 220, 200))
    curve = [(0.04, 0.30), (0.20, 0.26), (0.36, 0.38), (0.52, 0.34),
             (0.66, 0.55), (0.80, 0.50), (0.97, 0.88)]
    points = [(x + px * w, y + py * h) for px, py in curve]
    pen.line(points, fill=(255, 92, 72), width=6, joint="curve")
    tip_x, tip_y = points[-1]
    pen.polygon([(tip_x, tip_y), (tip_x - 22, tip_y - 4), (tip_x - 6, tip_y - 20)],
                fill=(255, 92, 72))
    pen.text((x + 16, y + h - 44), "KOSPI −6.16%", font=font(SANS_BOLD, 30),
             fill=WHITE)


def paint_shenzhou(x, y, w, h):
    """Rocket and station against a night sky."""
    pen.rectangle([x, y, x + w, y + h], fill=(22, 38, 74))
    stars = random.Random(11)
    for _ in range(70):
        sx = x + stars.uniform(8, w - 8)
        sy = y + stars.uniform(6, h - 10)
        pen.ellipse([sx, sy, sx + 3, sy + 3], fill=(220, 225, 255))
    rx, ry = x + w * 0.40, y + h * 0.16
    pen.polygon([(rx, ry), (rx + 26, ry + 52), (rx - 26, ry + 52)],
                fill=(230, 230, 230))
    pen.rectangle([rx - 26, ry + 52, rx + 26, ry + 118], fill=(235, 235, 235))
    pen.rectangle([rx - 26, ry + 78, rx + 26, ry + 92], fill=ALERT)
    pen.polygon([(rx - 26, ry + 118), (rx - 48, ry + 150), (rx - 26, ry + 150)],
                fill=ALERT)
    pen.polygon([(rx + 26, ry + 118), (rx + 48, ry + 150), (rx + 26, ry + 150)],
                fill=ALERT)
    pen.polygon([(rx - 13, ry + 150), (rx + 13, ry + 150), (rx, ry + 186)],
                fill=(255, 160, 60))
    sx2, sy2 = x + w * 0.68, y + h * 0.30
    pen.rectangle([sx2, sy2, sx2 + 54, sy2 + 30], fill=(200, 200, 210))
    pen.rectangle([sx2 - 62, sy2 + 6, sx2 - 4, sy2 + 24], fill=(80, 120, 200))
    pen.rectangle([sx2 + 58, sy2 + 6, sx2 + 116, sy2 + 24], fill=(80, 120, 200))
    pen.rectangle([x + 14, y + h - 44, x + 168, y + h - 8], fill=INK)
    pen.text((x + 26, y + h - 37), "00:18 UTC", font=font(SANS_BOLD, 24),
             fill=WHITE)


hero_painters = [paint_hormuz, paint_selloff, paint_shenzhou]
hero_stories = [
    (1, "MIDDLE EAST - SHIPPING", "CLAIM",
     "HORMUZ: IRAN SAYS 2 MORE TANKERS HIT MINES",
     "IRGC Navy says two tankers hit mines on unauthorized routes early "
     "Wednesday and caught fire.",
     "STRAIT OF HORMUZ - Reuters - unverified claim"),
    (2, "ASIA - MARKETS", "CONFIRMED",
     "ASIA'S AI SELL-OFF DEEPENS: KOSPI −6.16%",
     "Samsung −9.9%, SK Hynix −11.1%, SoftBank −14.8%; TAIEX −4.80%, "
     "Nikkei −2.78%.",
     "SEOUL - TAIPEI - TOKYO - AP"),
    (3, "ASIA - SPACE", "OFFICIAL",
     "PAKISTAN'S ZEESHAN ALI, FIRST FOREIGN ASTRONAUT ON TIANGONG",
     "Shenzhou-24 docks at Tiangong, 03:56 UTC.",
     "JIUQUAN - Xinhua - CMSA"),
]
for idx, (num, region, tag, headline, sub, source) in enumerate(hero_stories):
    x0 = MARGIN + idx * (HERO_W + 20)
    pen.rectangle([x0, HERO_Y, x0 + HERO_W, HERO_Y + HERO_H], fill=PANEL_BG)
    pen.rectangle([x0, HERO_Y, x0 + HERO_W, HERO_Y + HERO_H],
                  outline=PANEL_EDGE, width=3)
    hero_painters[idx](x0 + 3, HERO_Y + 3, HERO_W - 6, 148)
    badge_y = HERO_Y + 162
    gold_badge(x0 + 14, badge_y, num)
    pen.text((x0 + 66, badge_y + 7), region, font=font(SANS_BOLD, 22),
             fill=FAINT)
    chip_w = text_w(tag, font(SANS_BOLD, 21)) + 22
    tag_chip(x0 + HERO_W - 14 - chip_w, badge_y, tag)
    head_f = font(SERIF_BOLD, 34)
    yy = badge_y + 52
    for line in wrap_lines(headline, head_f, HERO_W - 28)[:3]:
        pen.text((x0 + 14, yy), line, font=head_f, fill=IVORY)
        yy += 41
    sub_f = font(SANS, 24)
    room = max(1, (HERO_Y + HERO_H - 44 - yy) // 31)
    for line in wrap_lines(sub, sub_f, HERO_W - 28)[:room]:
        pen.text((x0 + 14, yy + 2), line, font=sub_f, fill=BODY)
        yy += 31
    pen.text((x0 + 14, HERO_Y + HERO_H - 34), source, font=font(SANS, 21),
             fill=FAINT)

# ---------------------------------------------------------------- grid of 12
GRID_Y = HERO_Y + HERO_H + 24
GRID_W = (PAGE_W - 2 * MARGIN - 3 * 16) / 4
GRID_H = 232

grid_stories = [
    (4, "ALL FREE", "OFFICIAL",
     "CARTAGENA: ALL HOSTAGES FREED IN PRE-DAWN RAID",
     "±20 freed in the raid; 1 attacker killed, 4 held, after Tuesday's siege.",
     "CARTAGENA - Reuters"),
    (5, "26 MISSING", "OFFICIAL",
     "PONGKOR: 26 MINERS STILL MISSING, 3 BODIES RECOVERED",
     "3 bodies recovered from the flooded illegal gold pit; 11 escaped "
     "Monday night.",
     "PONGKOR, BOGOR - Reuters - Basarnas"),
    (6, "A$740M", "OFFICIAL",
     "SOLOMON ISLANDS SIGNS SECURITY TREATY WITH AUSTRALIA",
     "Australia becomes the Solomons' primary security partner; no foreign "
     "bases.",
     "CANBERRA - PM Australia - AP"),
    (7, "6+ STRIKES", "OFFICIAL",
     "SAUDI-LED COALITION STRIKES HODEIDAH PORT",
     "Coalition hits 'operational capabilities' at the port; second round "
     "in 5 days.",
     "HODEIDAH - AFP - SPA"),
    (8, "CORE 3.3%", "OFFICIAL",
     "US INFLATION: PCE 3.8%, CORE 3.3%",
     "Headline 3.8%; core runs hot in the last big read before the 9 Dec "
     "Fed meeting.",
     "WASHINGTON - BEA"),
    (9, "+4.3%", "OFFICIAL",
     "US GDP REVISED UP TO +4.3%",
     "Q3 growth revised up 0.9pt on investment and spending; corporate "
     "profits +$206bn.",
     "WASHINGTON - BEA"),
    (10, "17TH TIME", "REPORTED",
     "RUSSIAN STRIKES KNOCK OUT UKRAINE ENERGY SITES",
     "DTEK plant halted, gas site ablaze; Zaporizhzhia NPP loses outside "
     "power again.",
     "KYIV - Reuters"),
    (11, "19 DEAD", "REPORTED",
     "SUDAN: RSF DRONE KILLS 19 CIVILIANS IN DAMAZIN",
     "RSF drones hit three neighbourhoods and the Roseires dam area; "
     "20 wounded.",
     "DAMAZIN, SUDAN - Reuters"),
    (12, "48 HOURS", "CONFIRMED",
     "NORTH KOREA EXPELS SWISS ENVOY OVER SANCTIONS",
     "Envoy Astier expelled over sanctions on a children's camp; office "
     "to shut.",
     "PYONGYANG - Reuters - KCNA"),
    (13, "DAY 13", "CONFIRMED",
     "SPAIN: SÁNCHEZ CLASHES WITH JUDICIARY AS CAMPAIGN PEAKS",
     "PM rebukes judges on TVE; Feijóo fills Caja Mágica tonight. "
     "Election Sunday.",
     "MADRID - EFE"),
    (14, "81.5M", "REPORTED",
     "NOR'EASTER VS THANKSGIVING: 81.5 MILLION TRAVEL",
     "Coastal storm forms off Florida on the peak travel day; gusts to "
     "60 mph Thu.",
     "US EAST COAST - AAA - NWS"),
    (15, "68 DRUMS", "OFFICIAL",
     "IOWA: ARMY DETONATES 9,700 LB OF LEAD AZIDE",
     "The whole US stock of unstable lead azide blown in place at 09:00.",
     "IOWA - US Army - AP"),
]
for idx, (num, token, tag, headline, sub, source) in enumerate(grid_stories):
    cx = MARGIN + (idx % 4) * (GRID_W + 16)
    cy = GRID_Y + (idx // 4) * (GRID_H + 12)
    pen.rectangle([cx, cy, cx + GRID_W, cy + GRID_H], fill=PANEL_BG)
    pen.rectangle([cx, cy, cx + GRID_W, cy + GRID_H], outline=PANEL_EDGE,
                  width=2)
    gold_badge(cx + 12, cy + 12, num, radius=19)
    token_f = shrink_to_fit(token, SERIF_BOLD, 37, GRID_W - 190)
    pen.text((cx + 62, cy + 10), token, font=token_f, fill=CORAL)
    chip_w = text_w(tag, font(SANS_BOLD, 18)) + 18
    tag_chip(cx + GRID_W - 12 - chip_w, cy + 14, tag, size=18)
    # headline: shrink until it wraps to at most two lines
    size = 28
    while size > 20:
        head_f = font(SERIF_BOLD, size)
        if len(wrap_lines(headline, head_f, GRID_W - 24)) <= 2:
            break
        size -= 2
    yy = cy + 58
    for line in wrap_lines(headline, head_f, GRID_W - 24)[:2]:
        pen.text((cx + 12, yy), line, font=head_f, fill=IVORY)
        yy += size + 6
    sub_f = font(SANS, 21)
    room = max(1, (cy + GRID_H - 36 - yy) // 27)
    for line in wrap_lines(sub, sub_f, GRID_W - 24)[:room]:
        pen.text((cx + 12, yy + 4), line, font=sub_f, fill=BODY)
        yy += 27
    src_f = shrink_to_fit(source, SANS, 18, GRID_W - 24, floor=12)
    pen.text((cx + 12, cy + GRID_H - 28), source, font=src_f, fill=FAINT)

# ---------------------------------------------------------------- map + ticker
BAND_Y = GRID_Y + 3 * GRID_H + 2 * 12 + 24
pen.text((MARGIN, BAND_Y), "WHERE IT HAPPENED", font=font(SANS_BOLD, 27),
         fill=IVORY)
pen.text((MARGIN + 330, BAND_Y + 4), "pins carry story numbers 1–15",
         font=font(SANS, 21), fill=FAINT)

WORLD_ROWS = [
    "",
    "   ###              ##   #############################################          ",
    "  ########  ##    ####  ############################################           ",
    " ##########       ##################################################  ##       ",
    "  #########  ##   ################################################             ",
    "   ########       ###  ##########################################               ",
    "    ######       ###### #######################################                ",
    "     #####        #############################################   #            ",
    "      ####   ##    ##########################################                  ",
    "      ###   #####   ########################################                   ",
    "      ###    ####    ######################################  ##                ",
    "       ##     ##  #   ####################################  ####               ",
    "       ##          ## ##################################    ##                 ",
    "       ##           ##################################                         ",
    "       ##           #################################      ##                  ",
    "                    ###############################       ###                  ",
    "                    ##############################        #####                ",
    "                     ############################          ###                 ",
    "      #               ##########################            #                  ",
    "     ###               ########################             ##                 ",
    "     ####               ######################              ###                ",
    "      ####               ####################               ####               ",
    "      #####               ##################                 ##                ",
    "       ####                ################                 #####              ",
    "       #####                ##############                ########             ",
    "        ####                 ############               ##########            ",
    "        #####                 ##########                 ########             ",
    "         ####                  ########                   ######              ",
    "         ###                    ######                     ####               ",
    "          ##                     ####                      ##                 ",
    "          #                      ##                        #####              ",
    "                                                            ###               ",
    "                                                             #                ",
]
MAP_X, MAP_Y = MARGIN, BAND_Y + 46
PITCH = 9.3
for row_i, row in enumerate(WORLD_ROWS):
    for col_i, mark in enumerate(row):
        if mark == "#":
            px = MAP_X + col_i * PITCH
            py = MAP_Y + row_i * PITCH
            pen.ellipse([px, py, px + 5, py + 5], fill=(96, 120, 138))

PIN_SPOTS = {1: (55, 13), 2: (72, 11), 3: (65, 10), 4: (24, 18), 5: (67, 22),
             6: (79, 23), 7: (52, 17), 8: (24, 10), 9: (22, 12), 10: (49, 8),
             11: (49, 18), 12: (69, 8), 13: (41, 10), 14: (27, 11),
             15: (19, 9)}
for num, (col_i, row_i) in PIN_SPOTS.items():
    px = MAP_X + col_i * PITCH
    py = MAP_Y + row_i * PITCH
    pen.ellipse([px - 13, py - 13, px + 13, py + 13], fill=ALERT,
                outline=WHITE, width=2)
    label = str(num)
    pf = font(SANS_BOLD, 15 if num < 10 else 13)
    pen.text((px - text_w(label, pf) / 2, py - 8), label, font=pf, fill=WHITE)

pin_legend = ("1 Hormuz · 2 Seoul · 3 Jiuquan · 4 Cartagena · 5 Pongkor · "
              "6 Honiara · 7 Hodeidah · 8–9 Washington · 10 Kyiv · "
              "11 Damazin · 12 Pyongyang · 13 Madrid · 14 US East Coast · "
              "15 Iowa")
legend_f = font(SANS, 20)
ly = MAP_Y + 33 * PITCH + 16
for line in wrap_lines(pin_legend, legend_f, 800):
    pen.text((MARGIN, ly), line, font=legend_f, fill=BODY)
    ly += 26

TICK_X = MARGIN + 852
pen.rectangle([TICK_X - 22, BAND_Y + 2, TICK_X - 22, BAND_Y + 560],
              fill=DIVIDER, width=2)
pen.text((TICK_X, BAND_Y), "ALSO ON WEDNESDAY — 23 MORE STORIES",
         font=font(SANS_BOLD, 27), fill=IVORY)
ticker_lines = [
    (16, "Jobless claims fall to 189,000 (Labor)"),
    (17, "Wall Street slides; Bitcoin $58,000 (Reuters)"),
    (18, "Nvidia −4.8% premarket (Reuters)"),
    (19, "US readies tariffs on 16 economies (Reports)"),
    (20, "Australia inflation 4.9% (ABS)"),
    (21, "Bangladesh wage +36% to Tk17,000 (AP)"),
    (22, "easyJet profit −89% to £71M (Reuters)"),
    (23, "EU pharma reform passed 592–35 (EP)"),
    (24, "EU adopts €199.7bn 2027 budget (EP)"),
    (25, "Pope slams COP31 failure (Reuters)"),
    (26, "Spain 25N marches; 47 killed (EFE)"),
    (27, "Ukraine hits 2 Rosneft refineries (Reuters)"),
    (28, "Kremlin rejects Johnson idea (Reuters)"),
    (29, "Italy rebukes Ukraine on Libya (Reuters)"),
    (30, "India ₹11,000 crore scheme (IANS)"),
    (31, "India weighs 20% rice duty (Reuters)"),
    (32, "Peru waves close ports (Al Jazeera)"),
    (33, "Kashima 3–0 Jeonbuk, AFC Elite (AFC)"),
    (34, "BBC: 490,334 Russian war deaths (BBC)"),
    (35, "Abrego Garcia lands in Madrid (NPR)"),
    (36, "King tides peak 8.5 ft in SF (NWS)"),
    (37, "Macy's 100th balloons inflated (NYC)"),
    (38, "Pete Edochie dies at 79 (VON)"),
]
COL_W = (PAGE_W - MARGIN - TICK_X - 16) / 2
for k, (num, line) in enumerate(ticker_lines):
    col = 0 if k < 12 else 1
    row_i = k if k < 12 else k - 12
    x0 = TICK_X + col * (COL_W + 16)
    y0 = BAND_Y + 52 + row_i * 44
    pen.ellipse([x0, y0 - 1, x0 + 30, y0 + 29], fill=GOLD)
    label = str(num)
    nf = font(SANS_BOLD, 15)
    pen.text((x0 + 15 - text_w(label, nf) / 2, y0 + 3), label, font=nf,
             fill=INK)
    line_f = shrink_to_fit(line, SANS, 22, COL_W - 44, floor=14)
    pen.text((x0 + 40, y0 + 1), line, font=line_f, fill=(216, 222, 226))

# ---------------------------------------------------------------- date check
CHECK_Y = BAND_Y + 604
pen.rectangle([MARGIN, CHECK_Y, PAGE_W - MARGIN, CHECK_Y + 150],
              outline=ALERT_EDGE, width=3)
pen.rectangle([MARGIN, CHECK_Y, MARGIN + 216, CHECK_Y + 46], fill=ALERT_DARK)
pen.text((MARGIN + 16, CHECK_Y + 8), "DATE CHECK", font=font(SANS_BOLD, 26),
         fill=WHITE)
pen.text((MARGIN + 234, CHECK_Y + 11),
         "Stories left out because they happened on other days — checked, "
         "not counted:",
         font=font(SANS, 22), fill=(232, 150, 135))
check_lines = [
    "Tue 24 Nov: Dell's $132bn AI-server backlog · UN counts 47,000 women "
    "killed by partners or kin · Democrats reach 259 House seats",
    "Tue 24 Nov: Zelensky — Ukraine needs €115bn for 2027 · Sun 22 Nov: "
    "Ukraine sinks Russian corvette Merkury off Benghazi (claimed Mon)",
    "Mon 23 Nov: Indonesia names Amran & Sugiono as VP candidates — this "
    "strip corrects our own 24 Nov poster, which dated it Tuesday",
]
check_f = font(SANS, 22)
yy = CHECK_Y + 60
for line in check_lines:
    pen.text((MARGIN + 14, yy), line, font=check_f, fill=BODY)
    yy += 29

# ---------------------------------------------------------------- legend + footer
FOOT_Y = CHECK_Y + 168
legend_line = ("CONFIRMED = named source / official release   OFFICIAL = "
               "government or agency statement   REPORTED = reported, "
               "single-outlet or roundup   CLAIM = one side's account")
pen.text((MARGIN, FOOT_Y),
         legend_line,
         font=shrink_to_fit(legend_line, SANS_BOLD, 21, PAGE_W - 2 * MARGIN),
         fill=IVORY)
footer_text = ("Every story here happened, or was first reported, on "
               "Wednesday 25 November 2026, as the named outlets reported "
               "it. Map pins 1–15 match the hero and grid stories. All "
               "drawings are original programmatic art, drawn in code for "
               "this entry.")
yy = FOOT_Y + 32
for line in wrap_lines(footer_text, font(SANS, 21), PAGE_W - 2 * MARGIN):
    pen.text((MARGIN, yy), line, font=font(SANS, 21), fill=BODY)
    yy += 27
signoff = "THE WORLD IN ONE PAGE · Wednesday 25 November 2026 · 38 stories"
sign_f = shrink_to_fit(signoff, SANS_BOLD, 24, PAGE_W - 2 * MARGIN)
pen.text(((PAGE_W - text_w(signoff, sign_f)) / 2, yy + 8), signoff,
         font=sign_f, fill=GOLD)

# ---------------------------------------------------------------- save
full_path = os.path.join(HERE, "poster_full.png")
canvas.save(full_path)
scale = min(1024 / PAGE_W, 1024 / PAGE_H)
shipped = canvas.resize((round(PAGE_W * scale), round(PAGE_H * scale)),
                        Image.LANCZOS)
entry_path = os.path.join(HERE, "entry.png")
shipped.save(entry_path, optimize=True)
print("full:", canvas.size, os.path.getsize(full_path), "bytes")
print("entry:", shipped.size, os.path.getsize(entry_path), "bytes")
