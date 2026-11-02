#!/usr/bin/env python3
"""make_asugo.py: Wimsy as Asugo (AS55, the Sonnet agent of DraVee's workspaces), Aogo's carefree sister. Asugo has no
drawing of her own (accord.dravee.dev shows only Gravatar's pattern for her), so she takes her sisters' colours, from
Kedr's drawings of them (Kedr_bit on X): apricot hair, Aogo's coral made lighter and more golden as Afugo's rust is
made darker, in a ponytail swinging out, a white top with apricot trim, lilac grey sleeves between Aogo's light grey
and Afugo's dusky lilac, amber eyes, one of them shut in a wink over an open grin, the black clip the three wear.
Made with make_vocaloid's pieces and Aogo's clip; writes out/wimsy-asugo.svg. The clip carries AS, 55 the sleeve: her
designation, not a vendor's mark."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # beside it, also under python3 -I
sys.dont_write_bytecode = True  # no __pycache__ left beside the drawings

import make_versions  # noqa: E402
from make_aogo import clip  # noqa: E402
from make_vocaloid import HEAD, character, vocaloid  # noqa: E402

# the letter the clip needs that the others' did not
make_versions.GLYPHS.setdefault("S", "M 8,2 Q 6.5,0 4,0 Q 0,0 0,4 Q 0,7.5 4,8 Q 8,8.5 8,12 Q 8,16 4,16 Q 1.5,16 0,14")

RIM = "#3A2A26"  # her sisters' dark brown: the eye's rim, the wink, the grin's edge
APRICOT = "#F0904A"  # her hair's deep tone: the trim and the scrunchie's band


def grin():
    """her mouth open in a grin, between the eyes and below them, a tongue at its bottom"""
    return (f'''  <!-- her mouth, open in a carefree grin -->
  <g transform="{HEAD}" stroke-linejoin="round">
    <path fill="#6A2A26" stroke="{RIM}" stroke-width="2.5" d="M 179,33 L 205,33 Q 205,51 192,51 Q 179,51 179,33 Z"/>
    <path fill="#F08A8A" d="M 184.5,46 Q 192,39.5 199.5,46 Q 197,49.5 192,49.5 Q 187,49.5 184.5,46 Z"/>
  </g>
''')


ASUGO = character(
    name="Asugo", who="Asugo", who_full="Asugo", hair_word="apricot ponytail and a clip",
    hair_colour="apricot", trim_word="apricot", eyes_word="Asugo's: amber, one of them shut in a wink",
    source="her sisters' colours, from Kedr's drawings of them (Kedr_bit on X), as she has no drawing: Aogo's coral "
           "made lighter and more golden",
    palette_note="Asugo: apricot hair and its shade in a ponytail swinging out, a white top with apricot trim, "
                 "lilac grey sleeves with 55, amber eyes, a wink, a grin, a black clip with AS in white",
    hair=("#FDBE86", "#F1924F"), tail=("#FAB073", "#E2803C"), tail_dark=("#E8914A", "#B8622A"),
    far=("#F1924F", "#C86E30"), far_dark=("#D27A3A", "#9A5222"),
    outfit=("#FFFFFF", "#ECE6EF"), back_wing="#B9ACC8", trim=APRICOT, trim_width=6,
    iris=("#FFC98E", "#E58B3A", "#8A4716"), rim=RIM, shine="#FFE2C6",
    # AS on the clip, 55 on the sleeve: her designation, AS55
    eyes="wink", mark="55", mark_colour="#FFFFFF",
    # her ponytail, swung out to the empty lower right as she turns: one leaf, tied in a black scrunchie as the
    # sisters' clips are black
    tie="#1C1C20", band=APRICOT, tie_h=18,
    tails_note="her ponytail, swinging out: one leaf, tied in a black scrunchie",
    near_use='  <use xlink:href="#drill" transform="translate(322,318) rotate(-28) scale(0.86,0.48)"/>',
    near_note="  <!-- her ponytail, in front, swung out -->\n",
    head_extras=grin() + clip("AS", note="the black clip in her hair, AS on it"),
)

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    with open(os.path.join(HERE, "out", "wimsy-asugo.svg"), "w") as f:
        f.write(vocaloid(ASUGO))
    print("out/wimsy-asugo.svg")
