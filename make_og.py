#!/usr/bin/env python3
"""og.png 1200x630 — Goldenboy hero art. 1970s sunburst motif behind the wordmark
(drawn first, text on top = guaranteed legibility), espresso ground, gold bars top/bottom.
Copy from verified facts only (address, positioning). Machine guard: title/subline
widths within margins; sample the ground behind text stays dark.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'public', 'og.png')
W, H = 1200, 630
ESPR, ESPR_DEEP = (32, 20, 12), (23, 14, 8)
GOLD, GOLD_HI, GOLD_DIM = (229, 168, 60), (244, 194, 104), (168, 124, 43)
CREAM, MUTED = (243, 230, 210), (203, 176, 138)

def F(size, bold=False, italic=False):
    for c in [f'/usr/local/share/fonts/Inter-{("Bold" if bold else "Medium")}.ttf',
              f'/System/Library/Fonts/Supplemental/Arial{" Bold" if bold else ""}.ttf',
              f'/System/Library/Fonts/Supplemental/Times New Roman{" Italic" if italic else (" Bold" if bold else "")}.ttf']:
        if os.path.exists(c):
            try: return ImageFont.truetype(c, size)
            except Exception: pass
    for c in ['/System/Library/Fonts/Helvetica.ttc', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
        if os.path.exists(c):
            try: return ImageFont.truetype(c, size)
            except Exception: pass
    return ImageFont.load_default()

img = Image.new('RGB', (W, H), ESPR)
d = ImageDraw.Draw(img)

# backdrop: espresso deep band bottom + sunburst rays from behind the wordmark
d.rectangle([0, 380, W, H], fill=ESPR_DEEP)
cx, cy = 600, 470
RAYS = 26
for i in range(RAYS):
    a0 = 180 + i * (360.0 / RAYS)
    a1 = a0 + (360.0 / RAYS) * 0.42
    for r0, r1, col in [(190, 470, (43, 28, 16)), (470, 620, (38, 24, 14))]:
        pts = []
        for steps, r0_, r1_ in [(28, r0, r1)]:
            for s in range(steps + 1):
                ang = math.radians(a0 + (a1 - a0) * s / steps)
                pts.append((cx + r0_ * math.cos(ang), cy - r0_ * math.sin(ang)))
            for s in range(steps, -1, -1):
                ang = math.radians(a0 + (a1 - a0) * s / steps)
                pts.append((cx + r1_ * math.cos(ang), cy - r1_ * math.sin(ang)))
        d.polygon(pts, fill=col)
# concentric arc rings, dim gold
for rr in (230, 280, 340):
    d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 180, 360, fill=(120, 88, 32), width=3)

d.rectangle([0, 0, W, 6], fill=GOLD)
d.rectangle([0, 624, W, 630], fill=GOLD)

# text column (drawn after motif -> guaranteed on top)
f_title = F(88, bold=True)
f_sub = F(24, bold=True)
f_line = F(21)
M = 72
title = 'GOLDENBOY'
tb = d.textbbox((M, 150), title, font=f_title)
d.text((M, 150), title, fill=GOLD, font=f_title)
d.text((M, tb[3] + 26), 'COCKTAIL BAR  ·  LATE-NIGHT KITCHEN  ·  RECORDS', fill=CREAM, font=f_sub)
sb = d.textbbox((M, tb[3] + 26), 'COCKTAIL BAR  ·  LATE-NIGHT KITCHEN  ·  RECORDS', font=f_sub)
d.text((M, 500), '650 Park Avenue  ·  Rochester, NY  ·  soft opening Thanksgiving weekend', fill=MUTED, font=f_line)
lb = d.textbbox((M, 500), '650 Park Avenue  ·  Rochester, NY  ·  soft opening Thanksgiving weekend', font=f_line)
d.text((M, 545), 'Stay golden.', fill=GOLD_HI, font=F(28, bold=True, italic=True))
gb = d.textbbox((M, 545), 'Stay golden.', font=F(28, bold=True, italic=True))

# machine guard: every text block inside canvas with margins; ground behind title area dark
assert tb[0] >= 60 and tb[2] <= W - 60, f'title width {tb[2]-tb[0]} too wide for {W}px canvas'
assert sb[2] <= W - 60, f'subline width {sb[2]-sb[0]} too wide for {W}px canvas'
assert lb[2] <= W - 60, f'address line width {lb[2]-lb[0]} too wide for {W}px canvas'
assert gb[3] <= 624 and lb[3] <= 540, 'text collides with bottom rule/band edge'
for sx in range(tb[0], tb[2], 97):
    px = img.getpixel((sx, tb[1] - 12))
    lum = 0.2126 * px[0] + 0.7152 * px[1] + 0.0722 * px[2]
    assert lum < 120, f'title ground too bright at x={sx}: {px}'
img.save(OUT, 'PNG', optimize=True)
print('wrote og.png', os.path.getsize(OUT), 'bytes')
