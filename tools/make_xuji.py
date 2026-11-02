#!/usr/bin/env python3
"""make_xuji.py: Wimsy as Xuji (XG47, the Grok Build agent of DraVee's workspaces), Aogo's sister, from the picture Xuji
has on accord.dravee.dev (drawn by Kedr, Kedr_bit on X): long black hair with a violet sheen and a big loop rising
off the top, a fringe swept over one eye, the other half shut and unimpressed under a raised brow, a :3 mouth, pale
lavender skin, a black tee, a studded black choker, a white clip in the hair. Here the loop is a thin crescent
arching over the head, the choker is the front wing's trim with white studs along it, the bare lavender arms are the
back wing. Made with make_vocaloid's pieces and Aogo's clip; writes out/wimsy-xuji.svg. The clip carries XG, 47 the
sleeve, not the vendor's marks the picture has: the bot is not the vendor's."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # beside it, also under python3 -I
sys.dont_write_bytecode = True  # no __pycache__ left beside the drawings

import make_versions  # noqa: E402
from make_aogo import clip  # noqa: E402
from make_vocaloid import HEAD, character, trim_point, vocaloid  # noqa: E402

# the letters the marks need that the others' did not: the clip's X and G, the sleeve's 7
make_versions.GLYPHS.setdefault("X", "M 0,0 L 8,16 M 8,0 L 0,16")
make_versions.GLYPHS.setdefault("G", "M 8,3 Q 7,0 4,0 Q 0,0 0,8 Q 0,16 4,16 Q 8,16 8,12 L 8,9 L 5,9")
make_versions.GLYPHS.setdefault("7", "M 0,0 L 8,0 L 3,16")

INK = "#1A171D"  # her near black: the eye's rim, the mouth, the clip's letters
# the blush of the back cheek, which her fringe covers: drawn over the hair, it would show on it
BACK_BLUSH = '<ellipse cx="160" cy="34" rx="15" ry="7" fill="#F28C9C" fill-opacity="0.6"/>'


def studs():
    """the white studs of her choker, along the front wing's trim, one every few pixels of the curve"""
    dots = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.3"/>'
                   for x, y, _, _ in (trim_point(0.06 + 0.88 * k / 15) for k in range(16)))
    return f'  <!-- the white studs of her choker, along the trim -->\n  <g fill="#F4F2F6">{dots}</g>\n'


def mouth():
    """her :3 mouth, toward the front of the face, past the fringe"""
    return (f'''  <!-- her :3 mouth -->
  <path transform="{HEAD}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"
        d="M 196,38 Q 200,44 204,38 Q 208,44 212,38"/>
''')


XUJI = character(
    name="Xuji", who="Xuji", who_full="Xuji", hair_word="long black hair, a loop and a fringe over one eye",
    hair_colour="black", trim_word="studded black", eyes_word="Xuji's: one under the fringe, the other half shut and "
                                                              "unimpressed under a raised brow",
    source="colours from Xuji's picture on accord.dravee.dev, drawn by Kedr (Kedr_bit on X)",
    palette_note="Xuji: long black hair with a violet sheen and a loop on top, a fringe over the back eye, pale "
                 "lavender skin and arms, a black tee with a studded choker for its trim, 47 on the arm, grey violet "
                 "eyes, a :3 mouth, a white clip with XG in black",
    hair=("#4B4352", "#211E24"), tail=("#3D3841", "#18161A"), tail_dark=("#2A262D", "#0E0D10"),
    far=("#2E2A31", "#141216"), far_dark=("#1E1B21", "#0A090B"),
    outfit=("#3A3540", "#18161A"), back_wing="#CBC4D1", trim="#4A4352", trim_width=8,
    iris=("#BDB4CC", "#6E6680", "#2E2836"), rim=INK, shine="#7A6E88", skin=("#E3DCE9", "#F5F2F8"),
    # XG on the clip, 47 on the arm: her designation, XG47
    eyes="meh", lid="skin", brow="#2A262D", mark="47", mark_colour="#272528",
    tails_note="her long hair, loose: the head's back and the two leaves below, no tail",
    # the fringe swept from the parting down over the back eye to the jaw, in pointed locks as the bangs are; the front
    # of the face bare
    hair_path="M -40,-200 L 340,-200 L 340,-44 L 208,-44 L 212,-6 L 197,-16 L 202,28 L 185,16 L 182,66 L 102,90 "
              "L -40,90 Z",
    # the loop off the top of her head: a thin crescent arching over it toward the tip, its root under the head
    ahoge="M 146,-36 C 138,-122 250,-152 292,-72 C 246,-130 166,-112 170,-36 Z",
    wing_extras=studs(),
    head_extras=mouth() + clip("XG", fill="#F4F2F6", ink=INK, place="translate(166,-8) rotate(-30)",
                               note="the white clip on her fringe, XG on it"),
)


def xuji():
    svg = vocaloid(XUJI)
    assert BACK_BLUSH in svg
    return svg.replace(BACK_BLUSH, "")


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    with open(os.path.join(HERE, "out", "wimsy-xuji.svg"), "w") as f:
        f.write(xuji())
    print("out/wimsy-xuji.svg")
