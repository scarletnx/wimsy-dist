#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 the wimsy-dist contributors
"""make_accord.py: Wimsy as Accord, DraVee's forge (accord.dravee.dev), and the avatar of the AccordWimsy bot, from the
forge's own mark (its assets/img/logo.svg): black and white, a disc ringed by a twisted rope, a cross of four petals
with a dot between each two. Here the rope is the front wing's trim, small white leaves slanted across a black band,
and the cross is on the arm, its petals four leaves, where the singers' marks are. Made with make_vocaloid's pieces;
writes out/wimsy-accord.svg and out/accordwimsy-avatar.svg, the drawing on the mark's disc, the rope a band round
its black edge and the drawing on its white middle, so Discord's and Forgejo's round crops keep it whole."""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # beside it, also under python3 -I
sys.dont_write_bytecode = True  # no __pycache__ left beside the drawings

from make_vocaloid import character, trim_point, vocaloid  # noqa: E402

# the mark's two colours, and the greys its edges are drawn with, read off the forge's logo.png
BLACK = "#010101"
WHITE = "#FFFFFF"
GREYS = ("#5E5E5E", "#9F9F9F", "#D1D1D1")


def leaf(length, width, fill):
    """a leaf from (0,0) to (length,0), two arcs meeting in points, width its widest"""
    s = width / 2
    r = (length * length / 4 + s * s) / (2 * s)
    return (f'<path fill="{fill}" d="M 0,0 A {r:.2f},{r:.2f} 0 0 1 {length:g},0 '
            f'A {r:.2f},{r:.2f} 0 0 1 0,0 Z"/>')


def rope():
    """the rope of the forge's mark along the front wing's trim: small white leaves slanted across the black band,
    one every few pixels of the curve, as the rope's strands are"""
    out = ["  <!-- the rope of Accord's mark on the trim: white leaves slanted across it -->\n"]
    n = 30
    for k in range(n):
        t = 0.05 + 0.9 * k / (n - 1)
        x, y, nx, ny = trim_point(t)
        tangent = math.degrees(math.atan2(-nx, ny))  # the normal turned back a quarter
        out.append(f'  <g transform="translate({x:.2f},{y:.2f}) rotate({tangent + 50:.1f}) translate(-4.6,0)">'
                   f'{leaf(9.2, 3.4, WHITE)}</g>\n')
    return "".join(out)


def cross(cx, cy, colour, petal=11.0):
    """the cross of Accord's mark: four leaves from one point, a dot between each two"""
    petals = "".join(f'<g transform="rotate({a})">{leaf(petal, petal * 0.48, colour)}</g>' for a in (0, 90, 180, 270))
    d = petal * 0.62
    dots = "".join(f'<circle cx="{d * math.cos(math.radians(a)):.2f}" cy="{d * math.sin(math.radians(a)):.2f}" '
                   f'r="{petal * 0.13:.2f}" fill="{colour}"/>' for a in (45, 135, 225, 315))
    return f'<g transform="translate({cx:g},{cy:g})">{petals}{dots}</g>'


def arm_cross():
    """the cross on the arm, where the singers' marks are, slanted as the wing is"""
    return ("  <!-- Accord's cross on the arm: four leaves from one point, a dot between each two -->\n"
            f'  <g transform="rotate(-8 192 100)">{cross(196, 100, WHITE)}</g>\n')


ACCORD = character(
    name="Accord", who="Accord", who_full="Accord", hair_word="rope and cross",
    hair_colour="black", trim_word="rope", eyes_word="black, with the round glint",
    source="the colours and the shapes of Accord's mark, accord.dravee.dev/assets/img/logo.svg",
    palette_note="Accord: black hair, sleeves and leaves below, a white front, the rope of its mark on the trim, "
                 "its cross on the arm",
    hair=(GREYS[0], BLACK), tail=("#3A3A3A", BLACK), tail_dark=("#262626", BLACK),
    far=("#262626", BLACK), far_dark=("#141414", "#000000"),
    outfit=(WHITE, GREYS[2]), back_wing=BLACK, trim=BLACK, trim_width=10,
    iris=(GREYS[1], GREYS[0], BLACK), rim=BLACK, shine=GREYS[2],
    tails_note="no tail: the head's back and the two leaves below, black as the mark's disc",
    wing_extras=rope() + arm_cross(),
)

# the avatar: the rope a band round the disc's edge, the drawing inside it. The drawing's smallest enclosing circle,
# measured on its render (centre 247.3,282.3, radius 280 in its 512 frame), is set on the inner disc's.
FIG_CENTRE, FIG_RADIUS = (247.3, 282.3), 280.0
INNER = 196  # the inner disc's radius; the rope runs from it to the edge
STRANDS, STRAND, STRAND_W, SLANT = 40, 60, 13, 40


def avatar(drawing, inner_fill=WHITE):
    """the drawing on the mark's black disc, the rope round the edge in white leaves slanted as its strands are, and
    inside it the mark's white disc, where the drawing's black reads against white as the cross's does"""
    inner = drawing[drawing.index(">", drawing.index("<svg")) + 1:drawing.rindex("</svg>")]
    inner = re.sub(r"\s*<metadata>.*?</metadata>", "", inner, flags=re.S)
    ring = []
    for k in range(STRANDS):
        a = 360 * k / STRANDS
        ring.append(f'    <g transform="rotate({a:.2f} 256 256) translate(256,{256 - (INNER + 252) / 2:g}) '
                    f'rotate({SLANT}) translate({-STRAND / 2:g},0)">{leaf(STRAND, STRAND_W, WHITE)}</g>\n')
    scale = (INNER - 2) / FIG_RADIUS
    tx, ty = 256 - FIG_CENTRE[0] * scale, 256 - FIG_CENTRE[1] * scale
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<!-- The AccordWimsy bot's avatar: Wimsy as Accord (wimsy-accord.svg) on the disc of Accord's mark, its rope round
     the black edge as white leaves, the drawing on the white middle. Wimsy is Liz's (ScarletNX's dist/wimsy.svg), GPL-3.0-or-later; the disc, the
     rope and the cross are Accord's mark (accord.dravee.dev/assets/img/logo.svg), drawn again as leaves. -->
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="512" height="512"
     viewBox="0 0 512 512">
  <metadata>
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:cc="http://creativecommons.org/ns#"
             xmlns:dc="http://purl.org/dc/elements/1.1/">
      <cc:Work rdf:about="">
        <dc:title>AccordWimsy: Wimsy as Accord, on its mark's disc</dc:title>
        <dc:creator><cc:Agent><dc:title>Liz (Wimsy)</dc:title></cc:Agent></dc:creator>
        <dc:contributor><cc:Agent><dc:title>AO55 (Accord's colours, rope and cross)</dc:title></cc:Agent></dc:contributor>
        <dc:license rdf:resource="https://spdx.org/licenses/GPL-3.0-or-later.html"/>
        <dc:source>https://github.com/scarletnx/ScarletNX/blob/main/dist/wimsy.svg</dc:source>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <!-- the mark's black disc, white round its edge as every line here is -->
  <circle cx="256" cy="256" r="252" fill="{BLACK}" stroke="{WHITE}" stroke-width="5"/>
  <!-- the rope round the edge: white leaves slanted as its strands are -->
  <g>
{"".join(ring)}  </g>
  <!-- the inner disc, the rope's white edge round it -->
  <circle cx="256" cy="256" r="{INNER}" fill="{inner_fill}" stroke="{WHITE}" stroke-width="4"/>
  <!-- Wimsy as Accord, its smallest enclosing circle on the inner disc's -->
  <g fill="none" transform="translate({tx:.2f},{ty:.2f}) scale({scale:.4f})">{inner}</g>
</svg>
'''


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    drawing = vocaloid(ACCORD)
    with open(os.path.join(HERE, "out", "wimsy-accord.svg"), "w") as f:
        f.write(drawing)
    print("out/wimsy-accord.svg")
    with open(os.path.join(HERE, "out", "accordwimsy-avatar.svg"), "w") as f:
        f.write(avatar(drawing))
    print("out/accordwimsy-avatar.svg")
