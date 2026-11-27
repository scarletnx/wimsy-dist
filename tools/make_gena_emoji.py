#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 the wimsy-dist contributors
"""make_gena_emoji.py: the GenaWimsy bot's emojis, of Wimsy as Gena (make_gena.py): wimsygena, her own, and the
reactions eyes (seen, on it), thumbsup (agreed), done (done), no (cannot), with the names, meanings and signs of
Aogo's (make_aogo_emoji.py) so the bots' reactions read alike. Each is the whole drawing in her moods from Kedr's
drawing: Stable (the label OFF, the tube's soft glow) for her own and for seen; Ionized (ON, the tube brighter, a
blush) for agreed and done; Ionized in a panic (ON, the tube overloaded, sparks off it) for cannot. The plate covers
her front eye, so each face is the bare eye and the mouth under it, drawn heavier than the drawing's as Aogo's are,
with the label's letters larger and thicker. Writes out/wimsygena.svg and out/wimsygena_<name>.svg; publish.sh renders
each into emoji/ at 128 px."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # beside it, also under python3 -I
sys.dont_write_bytecode = True  # no __pycache__ left beside the drawings

import make_aogo_emoji as aogo  # noqa: E402
from make_gena import blush, eye_caret, eye_half, eye_wide, gena, heart, mouth, sweat  # noqa: E402

LINE = aogo.LINE  # the face's lines, heavier than the drawing's 4.5, as Aogo's emojis draw them

# name, what it says, how her face says it, the face, the label ON, the tube's power, the sign and what goes with it
EMOJIS = (
    ("", "her own, Stable", "the label OFF, the eye half shut, a small frown with a fang",
     eye_half(LINE) + mouth("pout", LINE), False, 0, ""),
    ("eyes", "seen, on it", "Stable: the label OFF, the eye half shut glancing up at the message, a small frown",
     eye_half(LINE, look=(-4, -3), lid=-10, droop=2) + mouth("pout", LINE), False, 0,
     aogo.sign("#34343A", aogo.sign_eyes(), "the sign: two eyes glancing up at the message, on dark grey")),
    ("thumbsup", "agreed", "Ionized: the label ON, a knowing look under the lid, a blush, a :3 with a fang",
     eye_half(LINE, look=(1, 2), lid=-8, droop=2, glint=True) + mouth("cat", LINE) + blush(LINE), True, 1,
     aogo.sign(aogo.THUMB_BLUE, aogo.sign_thumb(aogo.THUMB_BLUE), "the sign: a thumb up, white on blue")),
    ("done", "done", "Ionized: the label ON, the eye a ^, a blush, an open grin on her green tongue, a heart",
     eye_caret(LINE) + mouth("grin", LINE) + blush(LINE), True, 1,
     heart(486, 136, 1.15) + aogo.sign("#28A050", aogo.sign_check(), "the sign: a white check on green")),
    ("no", "cannot", "Ionized, in a panic: the label ON, the tube overloaded, the eye wide, a gasp, a drop of sweat",
     eye_wide(LINE) + mouth("gasp", LINE), True, 2,
     sweat() + aogo.sign("#DD2E44", aogo.sign_x(), "the sign: a white X on red")),
)


def emoji(name, meaning, look, face, on, power, mark):
    full = "wimsygena" + (f"_{name}" if name else "")
    what = "her own emoji" if not name else f"the GenaWimsy bot's reaction for {meaning}"
    s = gena(f"  <!-- her face, {meaning}: {look} -->\n" + face, on=on, power=power, heavy=True, extras=mark)
    s, titles = re.subn(r"<dc:title>Wimsy with Gena's[^<]*</dc:title>",  # the work's; the others name its makers
                        f"<dc:title>{full}: Wimsy as Gena, {what}</dc:title>", s)
    assert titles == 1
    first = s.index("-->\n") + len("-->\n")  # after the credits
    return s[:first] + f"<!-- {full}, a Discord emoji: {what} -->\n" + s[first:]


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    for name, meaning, look, face, on, power, mark in EMOJIS:
        full = "wimsygena" + (f"_{name}" if name else "")
        with open(os.path.join(HERE, "out", f"{full}.svg"), "w") as f:
            f.write(emoji(name, meaning, look, face, on, power, mark))
        print(f"out/{full}.svg")
