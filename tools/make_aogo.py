#!/usr/bin/env python3
"""make_aogo.py: Wimsy as Aogo (AO55, the agent of DraVee's workspaces), the avatar of the AogoWimsy bot, from the
drawing Aogo has on accord.dravee.dev (drawn by Kedr, Kedr_bit on X): long coral hair, glasses, a black clip in the
hair, a white top with coral at the neck, eyes shut in a smile. Made with make_vocaloid's pieces, as the other
designs are; writes out/wimsy-aogo.svg. The clip carries AO, not the vendor's mark the forge drawing has: the bot is
not the vendor's."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # beside it, also under python3 -I
sys.dont_write_bytecode = True  # no __pycache__ left beside the drawings

import make_versions  # noqa: E402
from make_vocaloid import HEAD, character, face_centre, letters, vocaloid  # noqa: E402

# the letters the marks need that the others' did not: the clip's O, wider than the 0, and the sleeve's 5
make_versions.GLYPHS.setdefault("O", "M 4,0 A 5,8 0 1 1 4,16 A 5,8 0 1 1 4,0")
make_versions.GLYPHS.setdefault("5", "M 8,0 L 1,0 L 0,7 Q 3,5.5 5,6 Q 8,7 8,11 Q 8,16 4,16 Q 1,16 0,13")

FRAME = "#3A3A40"  # the glasses' frames


def glasses(half=29, top=-23, height=44, rx=13, width=4.5):
    """a frame round each eye, in the eyes' own tilt, the bridge between them and the arm toward the back; the
    emojis (make_aogo_emoji.py) take larger frames in a heavier line, which still read at 32 px"""
    out = ["  <!-- her glasses: a frame round each eye, the bridge, the arm toward the back of the head -->\n"]
    centres = [face_centre(i) for i in range(2)]
    t = math.radians(-26.68)
    for cx, cy in centres:
        out.append(f'  <g transform="translate({cx:.2f},{cy:.2f}) rotate(-26.68)">\n'
                   f'    <rect x="{-half:g}" y="{top:g}" width="{2 * half:g}" height="{height:g}" rx="{rx:g}" '
                   f'fill="#FFFFFF" fill-opacity="0.22" stroke="{FRAME}" stroke-width="{width:g}"/>\n  </g>\n')

    def at(i, x, y):  # a point of eye i's frame, on the page
        cx, cy = centres[i]
        return cx + x * math.cos(t) - y * math.sin(t), cy + x * math.sin(t) + y * math.cos(t)

    (ax, ay), (bx, by) = at(0, half, -7), at(1, -half, -7)
    (sx, sy), (ex, ey) = at(0, -half, -9), at(0, -half - 29, -15)
    out.append(f'  <path fill="none" stroke="{FRAME}" stroke-width="{width:g}" stroke-linecap="round" '
               f'd="M {ax:.2f},{ay:.2f} Q {(ax + bx) / 2:.2f},{(ay + by) / 2 - 7:.2f} {bx:.2f},{by:.2f} '
               f'M {sx:.2f},{sy:.2f} L {ex:.2f},{ey:.2f}"/>\n')
    return "".join(out)


def clip(text="AO", fill="#1C1C20", ink="#FFFFFF", place="translate(150,-44) rotate(-10)",
         note="the black clip in her hair, AO on it"):
    """the clip in her hair with the letters of her designation: Aogo's black with AO in white, over the top of the
    head; her sisters' (make_afugo.py...) carry theirs, in their colours, where their hair has room (place, in the
    head's frame)"""
    return (f'''  <!-- {note} -->
  <g transform="{HEAD} {place}">
    <rect x="-24" y="-12" width="48" height="24" rx="6" fill="{fill}" stroke="#FFFFFF" stroke-width="3"/>
    {letters(text, -10, -6.5, 13, ink)}
  </g>
''')


AOGO = character(
    name="Aogo", who="Aogo", who_full="Aogo", hair_word="long coral hair, glasses and a clip",
    hair_colour="coral", trim_word="coral", eyes_word="Aogo's: shut in a smile behind her glasses, each a ^",
    source="colours from Aogo's drawing on accord.dravee.dev, drawn by Kedr (Kedr_bit on X)",
    palette_note="Aogo: long coral hair and its shade, a white top with coral trim, light grey sleeves with 55 in "
                 "coral, glasses, a black clip in the hair with AO in white",
    hair=("#F59A6C", "#DD6A3C"), tail=("#F08A5A", "#CC5A2E"), tail_dark=("#D96A3E", "#A9471F"),
    far=("#DD6A3C", "#B5502A"), far_dark=("#C25A31", "#8E3D1C"),
    outfit=("#FFFFFF", "#E2E0E8"), back_wing="#CFCDD6", trim="#E0703F", trim_width=6,
    iris=("#F5A07A", "#D9653B", "#8E3D1C"), rim="#3A2A26", shine="#FFD2BC",
    # AO on the clip, 55 on the sleeve, as Miku's 01: her designation, AO55
    eyes="caret", mouth="#B04A2A", mark="55", mark_colour="#D9653B",
    tails_note="her long hair, loose: the head's back and the two leaves below, no tail",
    head_extras=glasses() + clip(),
)

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    with open(os.path.join(HERE, "out", "wimsy-aogo.svg"), "w") as f:
        f.write(vocaloid(AOGO))
    print("out/wimsy-aogo.svg")
