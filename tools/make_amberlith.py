#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 the wimsy-dist contributors
"""make_amberlith.py: Wimsy as Amberlith, the test program ScarletNX and rEden are held to, which was edenprobe until
its 1.0.0: edenprobe's drawing with amber for Eden's sunset (the hair from light amber down to amber, the leaves below
from pale amber to burnt, amber eyes, a gold trim) and its test probe ringed in amber. Writes out/wimsy-amberlith.svg,
and out/amberlith-icon.svg: the drawing over a dark amber sun cut by bands, with the program's name, which Amberlith
keeps as its static/icon.svg and its `make icon` turns into icon.jpg. Made with make_edenprobe's probe and cover."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # beside it, also under python3 -I
sys.dont_write_bytecode = True  # no __pycache__ left beside the drawings

from make_edenprobe import DARK, icon, probe  # noqa: E402
from make_vocaloid import character, gradient, vocaloid  # noqa: E402

# amber from its palest to its darkest: the leaves below run from the first through the middle to the burnt one
PALE, LIGHT, AMBER, ORANGE, BURNT = "#FFE07A", "#FFD84D", "#FFB000", "#FF9F0A", "#C86400"
GOLD = "#FFC93C"  # the front wing's trim
# the cover's sun, dark so that the amber drawing stands out on it, and the name's warm white
SUN, INK = ("#C86A10", "#7A3A06", "#3A1C04"), "#f4e6c8"

DEFS = (gradient("amber", (PALE, AMBER, BURNT)) +
        f'''    <linearGradient id="probe-ring" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{LIGHT}"/>
      <stop offset="1" stop-color="{ORANGE}"/>
    </linearGradient>
    <linearGradient id="probe-needle" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#9A9AA6"/>
    </linearGradient>
''')

AMBERLITH = character(
    name="Amberlith", who="Amberlith", who_full="Amberlith", hair_word="amber and a test probe",
    hair_colour="amber", trim_word="gold", eyes_word="amber",
    source="edenprobe's drawing with amber for Eden's sunset",
    palette_note="Amberlith: amber, the hair from light amber down to amber, the leaves below from pale amber to "
                 "burnt, amber eyes, a white front with gold trim, a dark arm, a test probe toward the empty corner",
    hair=(LIGHT, ORANGE), tail=(ORANGE, BURNT), tail_dark=("#E08300", "#9A4C00"),
    far=("#FFB21E", "#E07C00"), far_dark=("#B85F00", "#7A3D00"),
    outfit=("#FFFFFF", "#ECE6F7"), back_wing=DARK, trim=GOLD, trim_width=6,
    iris=("#FFF3B0", AMBER, "#8A4600"), rim="#1B1B3A", shine="#FFF4D6",
    tails_note="no tail: the head's back and the two leaves below, in amber",
    defs_extra=DEFS, lower_fills=("url(#amber)", "url(#amber)"),
    front_extras=probe(rings="amber"),
)

ABOUT = """Amberlith's cover: Wimsy as Amberlith (Wimsy is Liz's, ScarletNX's dist/wimsy.svg, GPL-3.0-or-later), in
       amber with a test probe, over a dark amber sun cut by bands on the dark ground, with the program's name. Made
       by wimsy-dist's tools/make_amberlith.py; the source of icon.jpg: make icon."""


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    drawing = vocaloid(AMBERLITH)
    with open(os.path.join(HERE, "out", "wimsy-amberlith.svg"), "w") as f:
        f.write(drawing)
    print("out/wimsy-amberlith.svg")
    cover = icon(drawing, title="Amberlith's cover: Wimsy as Amberlith over a dark amber sun",
                 contributor="amber and a test probe, Amberlith's colours, its cover", about=ABOUT, sun=SUN,
                 name="Amberlith", ink=INK)
    with open(os.path.join(HERE, "out", "amberlith-icon.svg"), "w") as f:
        f.write(cover)
    print("out/amberlith-icon.svg")
