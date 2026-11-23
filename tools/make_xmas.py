#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 the wimsy-dist contributors
"""make_xmas.py: Christmas Wimsys, a Santa hat on the head: Wimsy herself (Liz's original, tools/wimsy.svg, the
bytes of ScarletNX's dist/wimsy.svg) and Aogo (make_aogo.py's drawing). The hat keeps the style: its cone a red leaf whose tip droops back, the fur a white leaf
lying along the head's upper edge (nothing runs across a leaf), the pompom a white leaf rolled round at the tip.
Writes out/wimsy-xmas.svg and out/wimsy-aogo-xmas.svg."""
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


def wimsy_xmas():
    """Liz's Wimsy with the hat drawn over the head, last, so nothing covers it"""
    with open(os.path.join(HERE, "wimsy.svg"), encoding="utf-8") as f:
        svg = f.read()
    # Inkscape breaks the licence's tag over lines; licences.py stamps the one-line form
    svg, n = re.subn(r'<dc:license\s+rdf:resource="([^"]*)"\s*/>', r'<dc:license rdf:resource="\1"/>', svg)
    if n != 1:
        raise SystemExit(f"tools/wimsy.svg: {n} dc:license tags in its metadata, where make_xmas.py expects 1")
    at = svg.rindex("</svg>")
    return svg[:at] + hat(uid="wimsy-hat") + svg[at:]


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
