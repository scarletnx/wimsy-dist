#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 the wimsy-dist contributors
"""make_aogo_emoji.py: the reactions the AogoWimsy bot puts on Discord messages, as emojis of Wimsy as Aogo
(make_aogo.py), one for each meaning: eyes (seen, on it), thumbsup (agreed), done (done), no (cannot). Each is the
whole drawing, so a reaction row still shows Wimsy's five leaves in Aogo's coral, with her face drawn heavier than
the drawing's (larger glasses in a thicker line, thicker eyes) so that it still reads at 32 px, and the sign in a disc
ringed in white in the drawing's empty lower right, large enough to read at a reaction's 16 to 22 px: two eyes
glancing up at the message on dark grey, a thumb up on blue, a check on green, an X on red. Writes
out/wimsyaogo_<name>.svg; publish.sh renders each into emoji/ at 128 px."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # beside it, also under python3 -I
sys.dont_write_bytecode = True  # no __pycache__ left beside the drawings

from make_aogo import AOGO, clip, glasses  # noqa: E402
from make_vocaloid import HEAD, eyes_svg, face_centre, vocaloid  # noqa: E402

RIM = "#3A2A26"  # Aogo's dark brown: her eyes, her mouths' lines
LINE = 8  # the face's lines: the drawing's 5.5 fade into the skin below 48 px
MOUTH, TONGUE = "#6A2A26", "#F08A8A"
WHITE = "#FFFFFF"
# the sign's disc, in the empty lower right: clear of the head's lower edge but for a sliver, and of the leaves below
DISC = (404, 408, 97)


def caret(i):
    """eye i shut in a smile, a ^ standing upright as it is typed (Aogo's own eyes), in the heavier line"""
    cx, cy = face_centre(i)
    return (f'  <path transform="translate({cx:.2f},{cy:.2f})" stroke="{RIM}" stroke-width="{LINE}" '
            'stroke-linejoin="round" stroke-linecap="round" fill="none" d="M -15,8 L 0,-9 L 15,8"/>\n')


def squeezed(i):
    """eye i squeezed shut, the back one a > and the front one a <, upright as typed: >_<, sorry"""
    cx, cy = face_centre(i)
    d = "M -12,-13 L 12,0 L -12,13" if i == 0 else "M 12,-13 L -12,0 L 12,13"
    return (f'  <path transform="translate({cx:.2f},{cy:.2f})" stroke="{RIM}" stroke-width="{LINE}" '
            f'stroke-linejoin="round" stroke-linecap="round" fill="none" d="{d}"/>\n')


def open_eye(i, look=(-3.5, -4)):
    """eye i wide open, Wimsy's round eye made to fit the frame: the rim, the coral iris turned by look (on the page:
    up and to the left, at the message above the reaction), the big glint and the small one"""
    cx, cy = face_centre(i)
    ix, iy = cx + look[0], cy + look[1]
    return (f'  <circle cx="{cx:.2f}" cy="{cy:.2f}" r="19.5" fill="{RIM}"/>\n'
            f'  <circle cx="{ix:.2f}" cy="{iy:.2f}" r="14.5" fill="url(#iris)"/>\n'
            f'  <circle cx="{ix - 4.5:.2f}" cy="{iy - 5.5:.2f}" r="6.5" fill="{WHITE}"/>\n'
            f'  <circle cx="{ix + 5.5:.2f}" cy="{iy + 5:.2f}" r="2.8" fill="{WHITE}" fill-opacity="0.85"/>\n')


def mouth(kind):
    """the mouth between the eyes and below them, where her sisters have theirs, in the head's frame"""
    if kind == "smile":  # a small closed smile: on it
        body = (f'<path d="M 183,37 Q 192,45 201,37" fill="none" stroke="{RIM}" stroke-width="5.5" '
                'stroke-linecap="round"/>')
    elif kind == "wide":  # a wide closed smile: agreed
        body = (f'<path d="M 179,35 Q 192,49 205,35" fill="none" stroke="{RIM}" stroke-width="5.5" '
                'stroke-linecap="round"/>')
    elif kind == "grin":  # open, a tongue at its bottom: done
        body = (f'<path fill="{MOUTH}" stroke="{RIM}" stroke-width="4" stroke-linejoin="round" '
                'd="M 177,30 L 207,30 Q 207,52 192,52 Q 177,52 177,30 Z"/>\n'
                f'    <path fill="{TONGUE}" '
                'd="M 182,46.5 Q 192,40 202,46.5 Q 198,50.5 192,50.5 Q 186,50.5 182,46.5 Z"/>')
    elif kind == "wobble":  # a wavy line, uneasy: sorry
        body = (f'<path d="M 179,39 Q 185.5,33 192,39 Q 198.5,45 205,39" fill="none" stroke="{RIM}" '
                'stroke-width="5" stroke-linecap="round"/>')
    else:
        raise ValueError(f"mouth {kind!r}: one of smile, wide, grin, wobble")
    return f'  <g transform="{HEAD}">\n    {body}\n  </g>\n'


def sweat():
    """a drop of sweat over the front of the head, ringed in white as every line here is"""
    return (f'''  <!-- a drop of sweat over the front of the head: sorry -->
  <g transform="translate(470,166) rotate(14)">
    <path fill="#8FD3F7" stroke="{WHITE}" stroke-width="4" stroke-linejoin="round"
          d="M 0,-22 Q 14,-2 14,8 A 14,14 0 0 1 -14,8 Q -14,-2 0,-22 Z"/>
    <path fill="none" stroke="{WHITE}" stroke-width="3.5" stroke-linecap="round" d="M -6,4 Q -7,12 -1,15"/>
  </g>
''')


# the signs, each in a frame where the disc's radius is 100
def sign_eyes():
    """two eyes, white with dark pupils, glancing up and to the left: at the message the reaction is under"""
    out = []
    for x in (-30, 30):
        out.append(f'<ellipse cx="{x}" cy="6" rx="25" ry="37" fill="{WHITE}"/>'
                   f'<circle cx="{x - 9}" cy="-9" r="14" fill="#16161A"/>'
                   f'<circle cx="{x - 13}" cy="-14" r="4.5" fill="{WHITE}"/>')
    return "".join(out)


def sign_thumb(disc):
    """a hand with its thumb up, white on the disc: the wrist's cuff, the fist, the four fingers' tips to the right,
    a line of the disc's colour between the fingers"""
    return (f'<g transform="translate(4,6)">'
            f'<rect x="-64" y="-8" width="24" height="66" rx="5" fill="{WHITE}"/>'
            f'<path fill="{WHITE}" stroke="{WHITE}" stroke-width="2" stroke-linejoin="round" '
            'd="M -34,-4 L -16,-36 C -12,-46 -12,-58 -6,-66 C 0,-75 14,-72 14,-58 C 14,-44 9,-30 6,-18 '
            'L 42,-18 C 55,-18 55,0 42,0 C 53,0 53,18 40,18 C 51,18 51,36 38,36 C 48,36 48,54 35,54 '
            'L -34,56 Z"/>'
            f'<path fill="none" stroke="{disc}" stroke-width="4.5" stroke-linecap="round" '
            'd="M 12,0 L 40,0 M 12,18 L 38,18 M 12,36 L 36,36"/>'
            '</g>')


def sign_check():
    return (f'<path fill="none" stroke="{WHITE}" stroke-width="24" stroke-linecap="round" stroke-linejoin="round" '
            'd="M -46,2 L -14,34 L 48,-30"/>')


def sign_x():
    return (f'<path fill="none" stroke="{WHITE}" stroke-width="26" stroke-linecap="round" '
            'd="M -34,-34 L 34,34 M 34,-34 L -34,34"/>')


def sign(disc, inner, note):
    cx, cy, r = DISC
    return (f'''  <!-- {note} -->
  <g transform="translate({cx},{cy})">
    <circle r="{r}" fill="{disc}" stroke="{WHITE}" stroke-width="9"/>
    <g transform="scale({r / 100:g})">{inner}</g>
  </g>
''')


THUMB_BLUE = "#5865F2"  # Discord's blurple: a thumb up on blue reads as a like
# name, what the reaction says, how her face says it, the face, the sign
EMOJIS = (
    ("eyes", "seen, on it", "eyes wide open behind her glasses, glancing up at the message, a small smile",
     open_eye(0) + open_eye(1) + mouth("smile"),
     sign("#34343A", sign_eyes(), "the sign: two eyes glancing up at the message, on her glasses' dark grey")),
    ("thumbsup", "agreed", "a wink, a wide smile",
     open_eye(0, (0, 0)) + caret(1) + mouth("wide"),
     sign(THUMB_BLUE, sign_thumb(THUMB_BLUE), "the sign: a thumb up, white on blue")),
    ("done", "done", "shut in a smile, each eye a ^, an open grin",
     caret(0) + caret(1) + mouth("grin"),
     sign("#28A050", sign_check(), "the sign: a white check on green")),
    ("no", "cannot", "squeezed shut in apology, a wavy mouth, a drop of sweat",
     squeezed(0) + squeezed(1) + mouth("wobble") + sweat(),
     sign("#DD2E44", sign_x(), "the sign: a white X on red")),
)

# her glasses, larger and heavier than the drawing's: the frame room for the open eyes, the line that reads at 32 px
FACE = glasses(half=32, top=-27, height=52, rx=15, width=LINE) + clip()


def emoji(name, meaning, look, face, mark):
    p = {**AOGO, "mouth": "", "head_extras": FACE}
    s = vocaloid(p)
    shut = eyes_svg(p)  # the drawing's own ^ eyes: each emoji draws its own face after the glasses
    assert s.count(shut) == 1
    s = s.replace(shut, "")
    title = "<dc:title>Wimsy with Aogo's long coral hair, glasses and a clip</dc:title>"
    assert s.count(title) == 1
    s = s.replace(title, f"<dc:title>wimsyaogo_{name}: Wimsy as Aogo, the AogoWimsy bot's reaction for {meaning}"
                         "</dc:title>")
    first = s.index("-->\n") + len("-->\n")  # after the credits
    s = (s[:first] + f"<!-- wimsyaogo_{name}, a Discord emoji: the AogoWimsy bot's reaction for {meaning} -->\n"
         + s[first:])
    assert s.rstrip().endswith("</svg>")
    end = s.rindex("</svg>")
    return s[:end] + f"  <!-- her face, {meaning}: {look} -->\n" + face + mark + s[end:]


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    for name, meaning, look, face, mark in EMOJIS:
        with open(os.path.join(HERE, "out", f"wimsyaogo_{name}.svg"), "w") as f:
            f.write(emoji(name, meaning, look, face, mark))
        print(f"out/wimsyaogo_{name}.svg")
