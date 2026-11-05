#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 the wimsy-dist contributors
"""make_versions.py: Wimsy with twin drills in the colours of Kasane Teto's Synthesizer V and VOICEPEAK designs, from
wimsy-teto.svg (the UTAU colours) beside it. Colours read off kasaneteto.jp's official illustrations."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = open(os.path.join(HERE, "wimsy-teto.svg")).read()


# the letters of the marks on the arm, as strokes in a box 8 wide and 16 high: no font, so it draws the same anywhere
GLYPHS = {
    "0": "M 4,0 A 4,8 0 1 1 4,16 A 4,8 0 1 1 4,0",
    "1": "M 2,3 L 5,0 L 5,16",
    "2": "M 0,4 Q 1,0 4,0 Q 8,0 8,4 Q 8,7 4,10 L 0,16 L 8,16",
    "4": "M 6,16 L 6,0 L 0,11 L 8,11",
    "A": "M 0,16 L 4,0 L 8,16 M 1.6,10 L 6.4,10",
    "D": "M 0,0 L 0,16 L 3,16 Q 8,16 8,8 Q 8,0 3,0 Z",
    "T": "M 0,0 L 8,0 M 4,0 L 4,16",
    "U": "M 0,0 L 0,11 Q 0,16 4,16 Q 8,16 8,11 L 8,0",
    "E": "M 8,0 L 0,0 L 0,16 L 8,16 M 0,8 L 6,8",
    "N": "M 0,16 L 0,0 L 8,16 L 8,0",
    "Y": "M 0,0 L 4,8 L 8,0 M 4,8 L 4,16",
    "I": "M 1,0 L 7,0 M 4,0 L 4,16 M 1,16 L 7,16",
}


def arm_mark(text, colour="#E6354B"):
    """the mark she has on her arm, in red on the sleeves' wing, slanted as the wing is"""
    x = 196 - (len(text) * 12 - 4) / 2  # centred where the wing is wide enough
    glyphs = "".join(f'    <path transform="translate({i * 12},0)" d="{GLYPHS[c]}"/>\n' for i, c in enumerate(text))
    return ("  <!-- the mark on her arm -->\n"
            f'  <g transform="rotate(-8 192 100) translate({x:g},92)" stroke="{colour}" stroke-width="2.6" '
            'stroke-linecap="round" stroke-linejoin="round" fill="none">\n' + glyphs + "  </g>\n")


def grad(name, a, b, vertical=False):
    x2, y2 = ("0", "1") if vertical else ("1", "1")
    return (f'    <linearGradient id="{name}" x1="0" y1="0" x2="{x2}" y2="{y2}">\n'
            f'      <stop offset="0" stop-color="{a}"/>\n      <stop offset="1" stop-color="{b}"/>\n'
            f'    </linearGradient>\n')


def swap_block(s, start, end, new):
    a = s.index(start)
    b = s.index(end, a) + len(end)
    return s[:a] + new + s[b:]


def replace(s, old, new, count=1):
    assert s.count(old) >= 1, old[:80]
    return s.replace(old, new) if count == 0 else s.replace(old, new, count)


def version(p):
    s = BASE
    # the gradients: hair, the drills' and tail's two crimsons, the far drill's, the front wing, the eyes
    gradients = (grad("hair", *p["hair"], vertical=True) + grad("tail", *p["tail"]) + grad("tail-dark", *p["tail_dark"])
                 + grad("far", *p["far"]) + grad("far-dark", *p["far_dark"]) + grad("outfit", *p["outfit"]))
    for gid in ("hair", "tail", "tail-dark", "far", "far-dark", "outfit"):
        s = swap_block(s, f'    <linearGradient id="{gid}"', '    </linearGradient>\n', "")
    s = replace(s, '    <linearGradient id="skin"', gradients + '    <linearGradient id="skin"')
    s = swap_block(s, '    <radialGradient id="iris"', '    </radialGradient>\n',
                   '    <radialGradient id="iris" cx="0.5" cy="0.62" r="0.6">\n'
                   f'      <stop offset="0" stop-color="{p["iris"][0]}"/>\n'
                   f'      <stop offset="0.7" stop-color="{p["iris"][1]}"/>\n'
                   f'      <stop offset="1" stop-color="{p["iris"][2]}"/>\n    </radialGradient>\n')
    # the back wing, the front wing's trim, the drills' ties, the light on the hair, the rims of the eyes
    s = replace(s, '<path fill="#3B3B40" stroke="#FFFFFF" stroke-width="5.47474"',
                f'<path fill="{p["back_wing"]}" stroke="#FFFFFF" stroke-width="5.47474"')
    s = replace(s, '<path fill="none" stroke="#D6334C" stroke-width="4" stroke-linecap="round"\n        d="M 279,40',
                f'<path fill="none" stroke="{p["trim"]}" stroke-width="{p["trim_width"]}" stroke-linecap="round"\n'
                '        d="M 279,40')
    s = replace(s, 'fill="#3B3B40" stroke="#FFFFFF" stroke-width="3"/>', f'fill="{p["tie"]}" stroke="#FFFFFF" stroke-width="3"/>', 0)
    s = replace(s, '<rect x="-25" y="-2" width="50" height="4" rx="2" fill="#D6334C"/>', p["tie_mark"], 0)
    s = replace(s, 'stroke="#F48A9B"', f'stroke="{p["shine"]}"', 0)
    s = replace(s, 'fill="#2B0A12"', f'fill="{p["rim"]}"', 0)
    s = replace(s, "<dc:title>Wimsy with twin drills</dc:title>", f"<dc:title>Wimsy with twin drills, {p['name']}</dc:title>")
    s = replace(s, "(twin drills, Kasane Teto's colours)", f"(twin drills, Kasane Teto's {p['name']} colours)")
    s = replace(s, "     The leaves keep Wimsy's own shapes; fan art. -->",
                f"     The leaves keep Wimsy's own shapes; the {p['name']} design's colours; fan art. -->")
    # the mark on her arm, each design's own
    a = s.index("  <!-- the mark on her arm -->")
    b = s.index("  </g>\n", a) + len("  </g>\n")
    s = s[:a] + (arm_mark(p["mark"], p.get("mark_colour", "#E6354B")) if p.get("mark") else "") + s[b:]
    # what the design adds over the wings, and over the head
    s = replace(s, "  <!-- the two leaves below, in crimson -->", p["wing_extras"] + "  <!-- the two leaves below, in crimson -->")
    s = replace(s, "  <!-- the eyes, where Wimsy has them", p["head_extras"] + "  <!-- the eyes, where Wimsy has them")
    # and over the near drill, drawn after it
    s = replace(s, "</svg>", p["front_extras"] + "</svg>")
    s = replace(s, '    <linearGradient id="skin"', grad("ribbon", "#F7F4F5", "#D3CCCF") + '    <linearGradient id="skin"')
    return s


# the front wing, for what is drawn on it to stay in it
FRONT_WING = ("M 283.32464,18.471579 A 330.76661,330.76661 0 0 0 211.63417,156.44085 330.76661,330.76661 0 0 0 "
              "217.7827,336.65055 244.08293,244.08293 0 0 0 309.08124,199.29137 244.08293,244.08293 0 0 0 283.32464,18.471579 Z")
BACK_WING = ("M 192.28931,12.793038 A 330.76661,330.76661 0 0 0 161.77932,165.25345 330.76661,330.76661 0 0 0 "
             "217.7827,336.65055 244.08293,244.08293 0 0 0 267.29749,179.3252 244.08293,244.08293 0 0 0 192.28931,12.793038 Z")

SV = {
    "name": "Synthesizer V", "mark": "0401",
    "hair": ("#E0566A", "#C23A50"), "tail": ("#D8475A", "#A8303F"), "tail_dark": ("#B83748", "#8C2535"),
    "far": ("#B03A4B", "#86283A"), "far_dark": ("#962E3F", "#6E1E2C"),
    "outfit": ("#D3CDD0", "#ABA3A6"), "back_wing": "#9E9598", "trim": "#C6354E", "trim_width": 5,
    "iris": ("#F07580", "#C6354E", "#8E2433"), "rim": "#3A1016", "shine": "#F28A97",
    # the cuffs: near black, a red band
    "tie": "#272221", "tie_mark": '<rect x="-25" y="-2" width="50" height="4" rx="2" fill="#C6354E"/>',
    "wing_extras": f'''  <!-- the jacket's grey pinstripes and its brass buttons -->
  <clipPath id="front-wing"><path d="{FRONT_WING}"/></clipPath>
  <g clip-path="url(#front-wing)" stroke="#6E6466" stroke-width="2" fill="none" stroke-linecap="round">
    <path d="M 224,258 Q 255,248 300,254"/>
    <path d="M 225,268 Q 255,258 298,264"/>
    <path d="M 226,278 Q 255,268 294,274"/>
  </g>
  <g fill="#B48C5E" stroke="#7A5A3C" stroke-width="1.5">
    <circle cx="270" cy="112" r="5.5"/>
    <circle cx="266" cy="158" r="5.5"/>
    <circle cx="260" cy="204" r="5.5"/>
  </g>
''',
    "head_extras": "",
    # the white ribbon tied on the near drill's first turn, as she wears it on a drill: its loops and tails are leaves
    # of two arcs as the wings and the turns are, white edged, a light grey shade so the white shows on white
    "front_extras": '''  <!-- the white ribbon on the near drill's first turn -->
  <g transform="translate(325,333) rotate(-10) scale(0.62)" fill="url(#ribbon)" stroke="#FFFFFF" stroke-width="3"
     stroke-linejoin="round">
    <path d="M 0,0 Q -12,8 -14,26 Q -2,14 0,0 Z"/>
    <path d="M 0,0 Q 12,8 16,24 Q 2,12 0,0 Z"/>
    <path d="M 0,0 Q -14,-30 -46,-14 Q -26,12 0,0 Z"/>
    <path d="M 0,0 Q 14,-30 46,-14 Q 26,12 0,0 Z"/>
    <circle r="6.5"/>
  </g>
''',
}

VP = {
    "name": "VOICEPEAK",
    "hair": ("#D94A5C", "#B8333F"), "tail": ("#C7394D", "#972735"), "tail_dark": ("#A93043", "#7E2030"),
    "far": ("#A53245", "#7A2231"), "far_dark": ("#8A2838", "#5E1824"),
    "outfit": ("#5E6455", "#42473A"), "back_wing": "#2F3128", "trim": "#C7394D", "trim_width": 5,
    "iris": ("#E8616E", "#C7394D", "#8A2230"), "rim": "#2E0B12", "shine": "#EF7E8A",
    # the collar's grey green, its red triangle
    "tie": "#7B8679", "tie_mark": '<path d="M -6,-4 L 6,-4 L 0,5 Z" fill="#D63A4E"/>',
    # the jacket's red as the wing's trim along its curve, as the other versions have it (straps across the leaves read
    # as a bandana), and the white sound wave across its chest
    "wing_extras": f'''  <!-- the white sound wave across the jacket's chest -->
  <clipPath id="front-wing"><path d="{FRONT_WING}"/></clipPath>
  <g clip-path="url(#front-wing)" stroke="#FFFFFF" stroke-opacity="0.6" stroke-width="2.5" stroke-linecap="round">
    <path d="M 236,150 v 4 M 242,146 v 12 M 248,141 v 22 M 254,145 v 14 M 260,138 v 28 M 266,144 v 16
             M 272,140 v 24 M 278,146 v 12 M 284,149 v 6"/>
  </g>
''',
    "head_extras": "", "front_extras": "",
}

if __name__ == "__main__":
    if len(sys.argv) > 1:  # a mark alone: make_versions.py 04
        print(arm_mark(sys.argv[1]), end="")
        sys.exit()
    for p, out in ((SV, "wimsy-teto-sv.svg"), (VP, "wimsy-teto-voicepeak.svg")):
        os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
        with open(os.path.join(HERE, "out", out), "w") as f:
            f.write(version(p))
        print("out/" + out)
