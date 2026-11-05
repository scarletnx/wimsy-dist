#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 the wimsy-dist contributors
"""make_edenprobe.py: Wimsy as edenprobe, the test program ScarletNX and rEden are held to: Eden's sunset colours
(its pink, purple and blue, the cyan of its mark's edge) and a test probe, its needle out toward the empty corner,
its cable curling after it. Writes out/wimsy-edenprobe.svg, and out/edenprobe-icon.svg: the drawing on the banded
sun edenprobe's cover already had (its static/icon.svg), with the program's name, which edenprobe's `make icon`
turns into icon.jpg. Made with make_vocaloid's pieces, as the other designs are."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # beside it, also under python3 -I
sys.dont_write_bytecode = True  # no __pycache__ left beside the drawings

from make_vocaloid import character, gradient, vocaloid  # noqa: E402

PINK, PURPLE, BLUE = "#FF2E88", "#BF42F6", "#5DA5ED"  # Eden's sunset, top to bottom (dist/dev.eden_emu.eden.svg)
CYAN, DARK, GREY = "#03FFFF", "#252525", "#D1D1D1"  # the rest of its mark's colours
GROUND = "#1B1B1F"  # edenprobe's cover's dark ground

# the probe along one line from the leaves' meeting point toward the empty lower right: its back end, its angle
PROBE_AT, PROBE_TURN = (236, 352), 28


def probe():
    """a test probe as a meter's or a scope's is: the cable out of a tapered boot at its back, the dark grip with two
    rings in the sunset's colours, the wide guard that keeps a finger off the metal, the long needle; white round
    each as every line here is"""
    cable = "M -14,0 C -40,8 -42,48 -14,64 C 14,80 8,114 -24,126"
    return f'''  <!-- the test probe: its cable, the boot, the dark grip ringed in the sunset, the guard, the needle -->
  <g transform="translate({PROBE_AT[0]},{PROBE_AT[1]}) rotate({PROBE_TURN})" stroke-linejoin="round">
    <path d="{cable}" fill="none" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round"/>
    <path d="{cable}" fill="none" stroke="{DARK}" stroke-width="8" stroke-linecap="round"/>
    <path d="M -18,-7 L 4,-12 L 4,12 L -18,7 Z" fill="{DARK}" stroke="#FFFFFF" stroke-width="4"/>
    <rect x="2" y="-14" width="112" height="28" rx="8" fill="{DARK}" stroke="#FFFFFF" stroke-width="4.5"/>
    <rect x="22" y="-14" width="12" height="28" fill="url(#probe-ring)"/>
    <rect x="44" y="-14" width="12" height="28" fill="url(#probe-ring)"/>
    <rect x="2" y="-14" width="112" height="28" rx="8" fill="none" stroke="#FFFFFF" stroke-width="4.5"/>
    <path d="M 112,-27 L 124,-27 Q 128,-27 128,-23 L 128,23 Q 128,27 124,27 L 112,27 Q 108,27 108,23 L 108,-23
             Q 108,-27 112,-27 Z" fill="url(#probe-ring)" stroke="#FFFFFF" stroke-width="4"/>
    <path d="M 128,-6 L 150,-4.5 L 236,-1.5 L 250,0 L 236,1.5 L 150,4.5 L 128,6 Z" fill="url(#probe-needle)"
          stroke="#FFFFFF" stroke-width="3"/>
  </g>
'''


DEFS = (gradient("eden-sun", (PINK, PURPLE, BLUE)) +
        '''    <linearGradient id="probe-ring" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FF2E88"/>
      <stop offset="1" stop-color="#BF42F6"/>
    </linearGradient>
    <linearGradient id="probe-needle" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#FFFFFF"/>
      <stop offset="1" stop-color="#9A9AA6"/>
    </linearGradient>
''')

EDENPROBE = character(
    name="edenprobe", who="edenprobe", who_full="edenprobe", hair_word="sunset and a test probe",
    hair_colour="sunset", trim_word="cyan", eyes_word="blue, as the sunset's foot",
    source="Eden's sunset colours (Eden's dist/dev.eden_emu.eden.svg)",
    palette_note="edenprobe: Eden's sunset, pink hair going purple, the leaves below down to its blue, a white "
                 "front with cyan trim, a dark arm, a test probe toward the empty corner",
    hair=(PINK, PURPLE), tail=(PURPLE, BLUE), tail_dark=("#9B3DD9", "#3F7BD0"),
    far=(PURPLE, "#8A3BD0"), far_dark=("#7A33C0", "#4A2A90"),
    outfit=("#FFFFFF", "#ECE6F7"), back_wing=DARK, trim=CYAN, trim_width=6,
    iris=("#9FE9FF", BLUE, "#2E3C9E"), rim="#1B1B3A", shine="#E6F7FF",
    tails_note="no tail: the head's back and the two leaves below, in the sunset",
    defs_extra=DEFS, lower_fills=("url(#eden-sun)", "url(#eden-sun)"),
    front_extras=probe(),
)

# the cover: edenprobe's static/icon.svg as it was (the banded sun on the dark ground, the name below), the drawing
# over the sun. The drawing's frame is 512; its figure fills it but for the lower right, where the probe is.
SCALE, AT = 0.40, (24, 2)


def icon(drawing):
    inner = drawing[drawing.index(">", drawing.index("<svg")) + 1:drawing.rindex("</svg>")]
    inner = re.sub(r"\s*<metadata>.*?</metadata>", "", inner, flags=re.S)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 256 256">
  <metadata>
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:cc="http://creativecommons.org/ns#"
             xmlns:dc="http://purl.org/dc/elements/1.1/">
      <cc:Work rdf:about="">
        <dc:title>edenprobe's cover: Wimsy as edenprobe over the banded sun</dc:title>
        <dc:creator><cc:Agent><dc:title>Liz (Wimsy)</dc:title></cc:Agent></dc:creator>
        <dc:contributor><cc:Agent><dc:title>AO55 (sunset and a test probe, edenprobe's colours, its cover)</dc:title></cc:Agent></dc:contributor>
        <dc:license rdf:resource="https://spdx.org/licenses/GPL-3.0-or-later.html"/>
        <dc:source>https://github.com/scarletnx/ScarletNX/blob/main/dist/wimsy.svg</dc:source>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <!-- edenprobe's cover: Wimsy as edenprobe (Wimsy is Liz's, ScarletNX's dist/wimsy.svg, GPL-3.0-or-later), in
       Eden's sunset colours with a test probe, over the reden mark (the Eden sunset without the palm, cut by its
       bands) on the dark ground, with the program's name. Made by wimsy-dist's tools/make_edenprobe.py; the source
       of icon.jpg: make icon. -->
  <defs>
    <linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{PINK.lower()}"/>
      <stop offset="0.45" stop-color="{PURPLE.lower()}"/>
      <stop offset="0.9" stop-color="{BLUE.lower()}"/>
    </linearGradient>
    <mask id="bands">
      <rect width="256" height="256" fill="#fff"/>
      <rect x="0" y="103" width="256" height="6" fill="#000"/>
      <rect x="0" y="128" width="256" height="9" fill="#000"/>
      <rect x="0" y="153" width="256" height="12" fill="#000"/>
      <rect x="0" y="178" width="256" height="15" fill="#000"/>
    </mask>
  </defs>
  <rect width="256" height="256" fill="{GROUND.lower()}"/>
  <circle cx="128" cy="112" r="90" fill="url(#sun)" mask="url(#bands)"/>
  <g fill="none" transform="translate({AT[0]},{AT[1]}) scale({SCALE})">{inner}</g>
  <text x="128" y="238" text-anchor="middle" font-family="DejaVu Sans, Liberation Sans, sans-serif" font-weight="bold" font-size="30" letter-spacing="1" fill="#e8e8ec">edenprobe</text>
</svg>
'''


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    drawing = vocaloid(EDENPROBE)
    with open(os.path.join(HERE, "out", "wimsy-edenprobe.svg"), "w") as f:
        f.write(drawing)
    print("out/wimsy-edenprobe.svg")
    with open(os.path.join(HERE, "out", "edenprobe-icon.svg"), "w") as f:
        f.write(icon(drawing))
    print("out/edenprobe-icon.svg")
