#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 the wimsy-dist contributors
"""make_xuji_emoji.py: the reactions the XujiWimsy bot puts on Discord messages, as emojis of Wimsy as Xuji
(make_xuji.py), one for each meaning: eyes (seen, on it), thumbsup (agreed), done (done), no (cannot). Each is the
whole drawing with the signs and discs of make_aogo_emoji.py, so the two bots' reactions read alike. Her fringe covers
the back eye, so each face is the front eye alone, drawn heavier as Aogo's are, in her near black; the mouth sits
toward the front of the face, past the fringe, where her :3 is, and seen keeps that :3. Writes out/wimsyxuji_<name>.svg;
publish.sh renders each into emoji/ at 128 px."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # beside it, also under python3 -I
sys.dont_write_bytecode = True  # no __pycache__ left beside the drawings

import make_aogo_emoji as aogo  # noqa: E402
from make_vocaloid import HEAD, eyes_svg, vocaloid  # noqa: E402
from make_xuji import BACK_BLUSH, INK, XUJI  # noqa: E402
from make_xuji import mouth as cat_mouth  # noqa: E402

aogo.RIM = INK  # the face pieces draw their lines in make_aogo_emoji's RIM: hers is her near black
AHEAD = 12  # her mouths' place: make_xuji's :3 is centred 12 px toward the front of Aogo's, past the fringe
FRONT = 1  # the eye the fringe leaves bare: make_vocaloid's "meh" hides eye 0 under the bangs


def mouth(kind):
    """her :3 for seen; the others make_aogo_emoji's, moved toward the front of the face"""
    if kind == "cat":
        return cat_mouth()
    moved = aogo.mouth(kind)
    assert moved.count(f'<g transform="{HEAD}">') == 1
    return moved.replace(f'<g transform="{HEAD}">', f'<g transform="{HEAD} translate({AHEAD},0)">')


# name, what the reaction says, how her face says it, the face, the sign: Aogo's signs, so both bots' read alike
EMOJIS = (
    ("eyes", "seen, on it", "her eye wide open, glancing up at the message, her :3",
     aogo.open_eye(FRONT) + mouth("cat"),
     aogo.sign("#34343A", aogo.sign_eyes(), "the sign: two eyes glancing up at the message, on dark grey")),
    ("thumbsup", "agreed", "her eye shut in a smile, a ^, a wide smile",
     aogo.caret(FRONT) + mouth("wide"),
     aogo.sign(aogo.THUMB_BLUE, aogo.sign_thumb(aogo.THUMB_BLUE), "the sign: a thumb up, white on blue")),
    ("done", "done", "her eye a ^, an open grin",
     aogo.caret(FRONT) + mouth("grin"),
     aogo.sign("#28A050", aogo.sign_check(), "the sign: a white check on green")),
    ("no", "cannot", "her eye squeezed shut, a <, a wavy mouth, a drop of sweat",
     aogo.squeezed(FRONT) + mouth("wobble") + aogo.sweat(),
     aogo.sign("#DD2E44", aogo.sign_x(), "the sign: a white X on red")),
)


def emoji(name, meaning, look, face, mark):
    head = XUJI["head_extras"]
    assert head.count(cat_mouth()) == 1  # her drawing's :3, which each emoji draws or replaces
    p = {**XUJI, "head_extras": head.replace(cat_mouth(), "")}
    s = vocaloid(p)
    assert BACK_BLUSH in s  # as make_xuji.py: the blush under her fringe would show on the hair
    s = s.replace(BACK_BLUSH, "")
    shut = eyes_svg(p)  # the drawing's half shut eye and raised brow: each emoji draws its own face
    assert s.count(shut) == 1
    s = s.replace(shut, "")
    s, titles = re.subn(r"<dc:title>Wimsy with Xuji's[^<]*</dc:title>",  # the work's; the others name its makers
                        f"<dc:title>wimsyxuji_{name}: Wimsy as Xuji, the XujiWimsy bot's reaction for {meaning}"
                        "</dc:title>", s)
    assert titles == 1
    first = s.index("-->\n") + len("-->\n")  # after the credits
    s = (s[:first] + f"<!-- wimsyxuji_{name}, a Discord emoji: the XujiWimsy bot's reaction for {meaning} -->\n"
         + s[first:])
    assert s.rstrip().endswith("</svg>")
    end = s.rindex("</svg>")
    return s[:end] + f"  <!-- her face, {meaning}: {look} -->\n" + face + mark + s[end:]


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    for name, meaning, look, face, mark in EMOJIS:
        with open(os.path.join(HERE, "out", f"wimsyxuji_{name}.svg"), "w") as f:
            f.write(emoji(name, meaning, look, face, mark))
        print(f"out/wimsyxuji_{name}.svg")
