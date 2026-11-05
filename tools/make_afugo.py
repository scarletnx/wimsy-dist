#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 the wimsy-dist contributors
"""make_afugo.py: Wimsy as Afugo (AF51, the Fable agent of DraVee's workspaces), Aogo's sister, from the drawing Afugo
has on accord.dravee.dev (drawn by Kedr, Kedr_bit on X): long messy rust hair spiking up on top, tired eyes sunk in
grey lilac shadows, a mouth open in a yawn, a white shirt shaded in lilac, a black clip in the hair. Her colours are
the drawing's own: the rust is redder and darker than Aogo's coral, and the shirt's lilac shade, the colour of her
tired eyes, takes the wings where Aogo's are white. Made with make_vocaloid's pieces and Aogo's clip; writes
out/wimsy-afugo.svg. The clip carries AF, 51 the sleeve, not the vendor's marks the forge drawing has: the bot is not
the vendor's."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # beside it, also under python3 -I
sys.dont_write_bytecode = True  # no __pycache__ left beside the drawings

import make_versions  # noqa: E402
from make_aogo import clip  # noqa: E402
from make_vocaloid import HEAD, character, vocaloid  # noqa: E402

# the letter the clip needs that the others' did not
make_versions.GLYPHS.setdefault("F", "M 8,0 L 0,0 L 0,16 M 0,8 L 6,8")

RIM = "#2E1E1E"  # her drawing's dark lines


def yawn():
    """her mouth open in a yawn, between the eyes and below them, a tongue at its bottom"""
    return (f'''  <!-- her mouth, open in a yawn -->
  <g transform="{HEAD}">
    <ellipse cx="192" cy="41" rx="6.5" ry="8.5" fill="#6E2626" stroke="{RIM}" stroke-width="2.5"/>
    <path fill="#E07070" d="M 186.5,44.5 Q 192,40 197.5,44.5 Q 196,49.5 192,49.5 Q 188,49.5 186.5,44.5 Z"/>
  </g>
''')


AFUGO = character(
    name="Afugo", who="Afugo", who_full="Afugo", hair_word="messy long rust hair and a clip",
    hair_colour="rust", trim_word="rust", eyes_word="Afugo's: tired, under heavy lids, grey lilac shadows under them",
    source="colours from Afugo's drawing on accord.dravee.dev, drawn by Kedr (Kedr_bit on X)",
    palette_note="Afugo: long messy rust hair and its shade, two spikes on top, a lilac grey top with rust trim, "
                 "dusky lilac sleeves with 51, tired rust eyes with lilac bags, a yawn, a black clip with AF in white",
    hair=("#DA7450", "#B84E33"), tail=("#CF6545", "#9E3E27"), tail_dark=("#B5502F", "#86331F"),
    far=("#B85236", "#8E3A26"), far_dark=("#9A4029", "#6E2A1A"),
    outfit=("#F2EFF4", "#C9C1CF"), back_wing="#8F8099", trim="#C6543C", trim_width=6,
    iris=("#E79A72", "#B5502F", "#5F2A1A"), rim=RIM, shine="#F09070", bags="#82728C",
    lid="skin",
    # AF on the clip, 51 on the sleeve: her designation, AF51
    eyes="tired", mark="51", mark_colour="#F2EFF4",
    tails_note="her long hair, loose: the head's back and the two leaves below, no tail",
    # two spikes of messy hair on top, crescent leaves from under the head, swept the same way
    ahoge="M 150,-30 C 148,-96 196,-128 246,-120 C 208,-108 188,-80 190,-32 Z "
          "M 206,-34 C 210,-62 236,-76 266,-72 C 244,-64 230,-54 228,-34 Z",
    head_extras=yawn() + clip("AF", place="translate(122,-26) rotate(-24)",
                              note="the black clip in her hair, AF on it"),
)

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    with open(os.path.join(HERE, "out", "wimsy-afugo.svg"), "w") as f:
        f.write(vocaloid(AFUGO))
    print("out/wimsy-afugo.svg")
