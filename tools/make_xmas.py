#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 the wimsy-dist contributors
"""make_xmas.py: Christmas Wimsys. Wimsy herself in candy cane: Liz's original (tools/wimsy.svg, the bytes of
ScarletNX's dist/wimsy.svg) with, as Liz asked, her upper wings red with white dots and her head and the two leaves
below a candy cane's tilted stripes. Aogo (make_aogo.py's drawing) in a Santa hat: its cone a red leaf whose tip
droops back, the fur a white leaf along the head's upper edge (nothing runs across a leaf), a white pompom at the
tip. Writes out/wimsy-xmas.svg and out/wimsy-aogo-xmas.svg."""
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # beside it, also under python3 -I
sys.dont_write_bytecode = True  # no __pycache__ left beside the drawings

from make_aogo import AOGO, clip, glasses  # noqa: E402
from make_vocaloid import HEAD, vocaloid  # noqa: E402

RED = ("#EE3B43", "#B21E2B")
FUR = ("#FFFFFF", "#E4E2EA")


R_EDGE = 330.76661  # the radius of the head's upper edge, the arc from the centre to the tip (wimsy.svg, wimsy-teto.svg)


def edge(x):
    """the head's upper edge at x, in the head's frame: the arc through (0,0), (175,-42) and (325,0)"""
    half = 162.5
    return -(math.sqrt(R_EDGE ** 2 - (x - half) ** 2) - math.sqrt(R_EDGE ** 2 - half ** 2))


def leaf(x1, y1, x2, y2, bulge_out, bulge_in):
    """a leaf from (x1,y1) to (x2,y2): two quadratic arcs whose controls stand bulge_out and bulge_in above the
    chord's middle (negative y is up in the head's frame)"""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    return (f"M {x1:.1f},{y1:.1f} Q {mx:.1f},{my - bulge_out:.1f} {x2:.1f},{y2:.1f} "
            f"Q {mx:.1f},{my - bulge_in:.1f} {x1:.1f},{y1:.1f} Z")


def hat(start=150, end=300, tip=(118, -120), uid="hat"):
    """the Santa hat in the head's frame: the fur a white leaf along the head's upper edge from x=start to x=end,
    the red cone standing on it with its tip drooping back to tip, the pompom there; uid keeps its gradients apart
    from another drawing's"""
    x1, x2 = start, end
    y1, y2 = edge(x1) + 3, edge(x2) + 3
    sag = edge((x1 + x2) / 2) - (y1 + y2) / 2  # how far the arc stands above the chord, at the middle
    fur = leaf(x1, y1, x2, y2, 2 * (14 - sag) + 2 * 14, 2 * (-sag))
    # the cone: from the fur's top near its front end, up and over to the tip, back down to the fur's back end
    cx1, cx2 = x1 + 14, x2 - 14
    cy1, cy2 = edge(cx1) - 10, edge(cx2) - 10
    tx, ty = tip
    cone = (f"M {cx2:.1f},{cy2:.1f} Q {cx2 - 30:.1f},{ty - 40:.1f} {tx:.1f},{ty:.1f} "
            f"Q {cx1 + 4:.1f},{(ty + cy1) / 2 - 6:.1f} {cx1:.1f},{cy1:.1f} "
            f"Q {(cx1 + cx2) / 2:.1f},{edge((cx1 + cx2) / 2) - 30:.1f} {cx2:.1f},{cy2:.1f} Z")
    return f'''  <!-- the Santa hat: a red leaf whose tip droops back, a white leaf of fur along the head's edge, a white
       pompom at the tip -->
  <g transform="{HEAD}">
    <defs>
      <linearGradient id="{uid}-red" x1="0" y1="1" x2="0.4" y2="0">
        <stop offset="0" stop-color="{RED[0]}"/><stop offset="1" stop-color="{RED[1]}"/>
      </linearGradient>
      <linearGradient id="{uid}-fur" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="{FUR[0]}"/><stop offset="1" stop-color="{FUR[1]}"/>
      </linearGradient>
    </defs>
    <path fill="url(#{uid}-red)" stroke="#FFFFFF" stroke-width="4.5" stroke-linejoin="round" d="{cone}"/>
    <path fill="url(#{uid}-fur)" stroke="#FFFFFF" stroke-width="3.5" stroke-linejoin="round" d="{fur}"/>
    <path fill="url(#{uid}-fur)" stroke="#FFFFFF" stroke-width="3" stroke-linejoin="round"
          transform="translate({tx:.1f},{ty:.1f}) rotate(-35)" d="M -19,0 Q 0,-27 19,0 Q 0,27 -19,0 Z"/>
  </g>
'''


CANE = ("#E3202D", "#FFFFFF")  # a candy cane's red and white
DOTS = {"front": "#D71F2B", "back": "#A8141F"}  # the upper wings' reds, the back one darker as Liz's teal is


def stripes():
    """a candy cane's red stripes, tilted, across the whole page: drawn over a white leaf and cut to it"""
    bands = "".join(f'<rect x="{x}" y="-400" width="20" height="1400" fill="{CANE[0]}"/>' for x in range(-440, 960, 40))
    return f'<g transform="rotate(-40 256 256)">{bands}</g>'


def dots():
    """white dots on a grid, turned a little, across the whole page: drawn over a red leaf and cut to it"""
    spots = "".join(f'<circle cx="{x + (18 if (y // 36) % 2 else 0)}" cy="{y}" r="5.5" fill="#FFFFFF"/>'
                    for y in range(-360, 900, 36) for x in range(-360, 900, 36))
    return f'<g transform="rotate(-20 256 256)">{spots}</g>'


# Liz's leaves by their ids in tools/wimsy.svg: what each takes at Christmas (Liz, 23/11: the upper wings red with
# white dots, the head and the two leaves below a candy cane), as (the leaf's own fill, what is drawn over it)
XMAS_LEAVES = {
    "path1-4": (DOTS["back"], dots),  # the back upper wing
    "path1-8-8": (DOTS["front"], dots),  # the front upper wing
    "path1-8-8-6": (CANE[1], stripes),  # the leaf below, to the left
    "path1-8-8-6-0": (CANE[1], stripes),  # the leaf below, downward
    "path1-8-4-0": (CANE[1], stripes),  # the head
}


def wimsy_xmas():
    """Liz's Wimsy in candy cane. Each leaf keeps one solid fill (white under the stripes, red under the dots); its
    stripes or dots are shapes cut to the leaf by a clipPath of its own outline, and its white outline is drawn again
    over them. No <pattern>: a renderer blends a pattern's tile seams, and the drawing has to stay opaque at every
    size as Wimsy is (ScarletNX's tests/splash.c checks that)"""
    with open(os.path.join(HERE, "wimsy.svg"), encoding="utf-8") as f:
        svg = f.read()
    # Inkscape breaks the licence's tag over lines; licences.py stamps the one-line form
    svg, n = re.subn(r'<dc:license\s+rdf:resource="([^"]*)"\s*/>', r'<dc:license rdf:resource="\1"/>', svg)
    if n != 1:
        raise SystemExit(f"tools/wimsy.svg: {n} dc:license tags in its metadata, where make_xmas.py expects 1")
    for pid, (base, over) in XMAS_LEAVES.items():
        element = re.search(r'<path\b[^>]*?\bid="' + re.escape(pid) + r'"[^>]*?/>', svg, re.S)
        if not element:
            raise SystemExit(f"tools/wimsy.svg: no path {pid}, which make_xmas.py colours")
        old = element.group(0)
        d = re.search(r'\bd="([^"]*)"', old)
        width = re.search(r"stroke-width:([0-9.]+)", old)
        if not d or not width:
            raise SystemExit(f"tools/wimsy.svg: path {pid} has no d or no stroke-width in its style")
        new, k = re.subn(r"fill:#[0-9a-fA-F]{6}", f"fill:{base}", old, count=1)
        if k != 1:
            raise SystemExit(f"tools/wimsy.svg: path {pid} has no fill:#rrggbb in its style to change")
        cut = f"xmas-cut-{pid}"
        svg = svg.replace(old, new
                          + f'<clipPath id="{cut}"><path d="{d.group(1)}"/></clipPath>'
                          + f'<g clip-path="url(#{cut})">{over()}</g>'
                          + f'<path d="{d.group(1)}" fill="none" stroke="#ffffff" stroke-width="{width.group(1)}"/>', 1)
    return svg


def aogo_xmas():
    """Aogo with the hat further toward the tip, so her AO clip still shows behind it"""
    a = dict(AOGO) if isinstance(AOGO, dict) else AOGO
    extras = glasses() + clip() + hat(start=178, end=305, tip=(150, -128), uid="aogo-hat")
    if isinstance(a, dict):
        a = dict(a, head_extras=extras, name="Aogo at Christmas")
        return vocaloid(a)
    raise SystemExit("make_aogo.AOGO is not a character dict: make_xmas.py does not know its shape")


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    for name, svg in (("wimsy-xmas.svg", wimsy_xmas()), ("wimsy-aogo-xmas.svg", aogo_xmas())):
        with open(os.path.join(HERE, "out", name), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"out/{name}")
