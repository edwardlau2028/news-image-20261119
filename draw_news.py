#!/usr/bin/env python3
"""Draw the news-image-20261119 entry: a 1024x1024 newspaper front page
summing up Thursday 19 November 2026, rendered with PIL and Noto fonts."""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 242, 231)      # warm off-white
NAVY = (20, 38, 74)          # masthead band
GOLD = (201, 162, 39)        # gold rule and date line
INK = (24, 24, 24)           # headline / body text
GREY = (110, 108, 100)       # footer text
CARD_BG = (255, 255, 255)
CARD_BORDER = (205, 198, 184)

FONT_DIR = "/usr/share/fonts/truetype/noto"

def serif_bold(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "NotoSerif-Bold.ttf"), size)

def sans_bold(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "NotoSans-Bold.ttf"), size)

def sans_regular(size):
    return ImageFont.truetype(os.path.join(FONT_DIR, "NotoSans-Regular.ttf"), size)

# (tag, chip colour, headline, summary)
STORIES = [
    ("SUMMIT", (31, 78, 121),
     "Trump, Xi and Putin hold first three-way summit",
     "Leaders issue a 'peace declaration' in Shenzhen; no Ukraine deal, no arms cuts."),
    ("JUSTICE", (139, 26, 26),
     "World court: Myanmar committed genocide",
     "ICJ rules the 2017 crackdown on the Rohingya was state-sponsored genocide."),
    ("MIDDLE EAST", (180, 83, 9),
     "Houthi missile hits Riyadh's tallest tower",
     "PIF Tower windows blown out across seven floors; no injuries reported."),
    ("ASIA", (22, 101, 52),
     "Bangladesh lockdown turns violent",
     "Four killed in clashes; Nobel laureate Yunus's family home set on fire."),
    ("MARKETS", (14, 116, 144),
     "Anthropic debuts in record $81bn IPO",
     "Shares open on Nasdaq as ANT; largest listing ever, valued near $1.5tn."),
    ("EUROPE", (67, 56, 202),
     "Denmark backs Greenland deal 109\u20130",
     "Parliament approves U.S. security pact; more bases, Danish sovereignty kept."),
    ("AMERICAS", (157, 23, 77),
     "U.S. and Venezuela sign military pact",
     "Hegseth visits Caracas; joint training and intelligence sharing agreed."),
    ("MIGRATION", (87, 83, 78),
     "Migrant boat capsizes off Senegal",
     "Dozens missing after a boat carrying 50\u2013100 people overturns near Yenne."),
]

def wrap(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines, each within max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines

def layout_cards(draw, headline_size, summary_size):
    """Wrap every story at the given sizes; return per-card line lists."""
    head_font = serif_bold(headline_size)
    sum_font = sans_regular(summary_size)
    inner = 434  # card inner text width
    cards = []
    for tag, colour, headline, summary in STORIES:
        head_lines = wrap(draw, headline, head_font, inner)
        sum_lines = wrap(draw, summary, sum_font, inner)
        cards.append((tag, colour, head_lines, sum_lines))
    return cards

def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    draw.rectangle([0, 0, W, 160], fill=NAVY)
    title_font = serif_bold(56)
    title = "THE WORLD IN ONE DAY"
    tw = draw.textlength(title, font=title_font)
    draw.text(((W - tw) / 2, 26), title, font=title_font, fill=(255, 255, 255))
    date_font = sans_bold(30)
    dateline = "THURSDAY \u00b7 19 NOVEMBER 2026"
    dw = draw.textlength(dateline, font=date_font)
    draw.text(((W - dw) / 2, 100), dateline, font=date_font, fill=GOLD)
    draw.rectangle([0, 160, W, 164], fill=GOLD)

    # ---- Story grid ------------------------------------------------------
    margin = 40
    gutter = 20
    grid_top = 176
    grid_bottom = 962
    cols, rows = 2, 4
    grid_w = W - 2 * margin
    grid_h = grid_bottom - grid_top
    card_w = (grid_w - (cols - 1) * gutter) // cols
    card_h = (grid_h - (rows - 1) * gutter) // rows
    pad = 12
    inner_w = card_w - 2 * pad

    # Adaptive sizing: shrink headline/summary until every card fits.
    chosen = None
    for headline_size, summary_size in [(30, 22), (28, 21), (25, 19)]:
        cards = layout_cards(draw, headline_size, summary_size)
        head_lh = int(headline_size * 1.18)
        sum_lh = int(summary_size * 1.25)
        chip_h = 24
        ok = True
        for _tag, _colour, head_lines, sum_lines in cards:
            assert len(head_lines) <= 3, "headline exceeds 3 lines"
            assert len(sum_lines) <= 2, "summary exceeds 2 lines"
            need = (pad + chip_h + 7 + len(head_lines) * head_lh
                    + 6 + len(sum_lines) * sum_lh + pad)
            if need > card_h:
                ok = False
                break
        if ok:
            chosen = (cards, headline_size, summary_size, head_lh, sum_lh, chip_h)
            break
    assert chosen is not None, "no font size fits the cards"
    cards, headline_size, summary_size, head_lh, sum_lh, chip_h = chosen

    head_font = serif_bold(headline_size)
    sum_font = sans_regular(summary_size)
    tag_font = sans_bold(17)

    for i, (tag, colour, head_lines, sum_lines) in enumerate(cards):
        r, c = divmod(i, cols)
        x0 = margin + c * (card_w + gutter)
        y0 = grid_top + r * (card_h + gutter)
        x1 = x0 + card_w
        y1 = y0 + card_h
        draw.rounded_rectangle([x0, y0, x1, y1], radius=10,
                               fill=CARD_BG, outline=CARD_BORDER, width=1)

        # Vertically centre the card's content block: short cards (one-line
        # headlines) otherwise leave a dead band at the bottom.
        content_h = (chip_h + 7 + len(head_lines) * head_lh
                     + 6 + len(sum_lines) * sum_lh)
        y = y0 + (card_h - content_h) // 2

        # Tag chip.
        tag_w = int(draw.textlength(tag, font=tag_font)) + 20
        chip_y = y
        draw.rounded_rectangle([x0 + pad, chip_y, x0 + pad + tag_w,
                                chip_y + chip_h], radius=chip_h // 2, fill=colour)
        draw.text((x0 + pad + 10, chip_y + 3), tag, font=tag_font,
                  fill=(255, 255, 255))

        # Headline.
        y = chip_y + chip_h + 7
        for line in head_lines:
            draw.text((x0 + pad, y), line, font=head_font, fill=INK)
            y += head_lh

        # Summary.
        y += 6
        for line in sum_lines:
            draw.text((x0 + pad, y), line, font=sum_font, fill=(74, 72, 66))
            y += sum_lh
        assert y <= y1 - pad + sum_lh, "card content overflow"

    # ---- Footer ----------------------------------------------------------
    foot_font = sans_regular(15)
    sources = "Sources: Reuters \u00b7 AP \u00b7 USA Today \u00b7 Defense News \u00b7 BBC \u00b7 NDTV"
    sw = draw.textlength(sources, font=foot_font)
    draw.text(((W - sw) / 2, 972), sources, font=foot_font, fill=GREY)
    note = "All events happened, or were first reported, on 19 November 2026."
    nw = draw.textlength(note, font=foot_font)
    draw.text(((W - nw) / 2, 994), note, font=foot_font, fill=GREY)

    img.save(OUT, format="PNG", optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {W}x{H}, {size} bytes")
    assert size <= 1048576, "entry.png exceeds 1 MiB"

if __name__ == "__main__":
    main()
