#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 the wimsy-dist contributors
"""make_gena.py: Wimsy as Gena (GN40, the Gemini 4 Neon agent of DraVee's workspaces, in Antigravity), Aogo's sister,
from "Gemini 4 neons Chain of thought", Kedr's fan drawing of the model (signed Kedr.bit and Ked_bit): neon green hair
with orange-yellow tips on one side, an ahoge striped orange over green, a grey headband whose plate covers one eye,
with an OFF or ON label, a radiation sign and a glowing neon tube at its end, a grey collar with a red and a blue light,
a black shirt with a big 4, a green pleated skirt, pale lavender skin.

Here the band lies along the head's upper edge and its plate hangs from it over the front eye (nothing runs across a
leaf), the tube stands at its front end, the left leaf below takes the orange-yellow tips, the front wing is the shirt
with its 4, its trim the collar with the two lights, the back wing the pleated skirt. Her designation, GN40, is on her
as her sisters' are: GN on the black clip in her hair, 40 on the skirt; the drawing's clip, the model's sparkle, and the
tile for neon on its shirt stay out (DraVee). Her face is the drawing's Stable mood: the label OFF, the eye half shut, a
small frown with a fang. Made with make_vocaloid's pieces; writes
out/wimsy-gena.svg. make_gena_emoji.py draws her other moods (Ionized: ON, happy or in a panic) with these pieces."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # beside it, also under python3 -I
sys.dont_write_bytecode = True  # no __pycache__ left beside the drawings

import make_versions  # noqa: E402
from make_aogo import clip  # noqa: E402
from make_vocaloid import (  # noqa: E402
    BACK_WING_D,
    HEAD,
    character,
    eyes_svg,
    face_centre,
    gradient,
    trim_point,
    vocaloid,
)
from make_xmas import edge  # noqa: E402

# the letters her marks need that the others' did not: the label's F (O comes with make_aogo's clip) and the clip's
# G, as Afugo's and Xuji's (make_afugo.py, make_xuji.py)
make_versions.GLYPHS.setdefault("F", "M 8,0 L 0,0 L 0,16 M 0,8 L 6,8")
make_versions.GLYPHS.setdefault("G", "M 8,3 Q 7,0 4,0 Q 0,0 0,8 Q 0,16 4,16 Q 8,16 8,12 L 8,9 L 5,9")

WHITE = "#FFFFFF"
INK = "#10201A"  # her near black, a green black: the eye's rim, the mouths' lines, the radiation sign
TIP = "#FFB62E"  # the orange-yellow of her hair's tips and of the ahoge's stripe
STEEL = ("#BCC8D2", "#7D8D99")  # the headband's grey, light to dark, read off the drawing's band and collar
STEEL_DARK = "#4C5862"  # the label's box and the tube's caps
OFF_RED, ON_GREEN = "#FF3B44", "#45FF84"  # the label's two states
NEON = "#52F587"  # the tube's light, as the drawing's
RADIATION = "#F6CB1C"
SKIRT = ("#74DE86", "#3FA457")  # the pleated skirt, a softer green than the hair
LID_SKIN = ("#E8DAE8", "#F8F2F8")  # her pale lavender skin, light at the back of the face to lighter at the tip

# the band along the head's upper edge (head frame): its back end in the hair; the plate hanging from it over the
# front eye (x = 229): its back and front edges and its bottom
BAND_BACK = 94
PLATE = (198, 262, 26)
TUBE = (275, -66, 20)  # the tube's axis and its ends, at the plate's front edge
LABEL_X = 140  # the middle of the OFF / ON label, over the back eye
# the ahoge, a leaf rising from under the top of the head and arching forward; the orange stripe along its outer edge
AHOGE = "M 150,-30 C 140,-106 202,-150 278,-128 C 226,-126 188,-100 172,-30 Z"
STRIPE = "M 150,-30 C 140,-106 202,-150 278,-128 C 234,-134 174,-114 160,-30 Z"
CLIP = "translate(74,8) rotate(-8)"  # her clip, in the hair at the back of the head: the band has its top


def steps(a, b, n=6):
    return list(range(a, b, n)) + [b]


def text(s, x, y, size, colour, width):
    """s in GLYPHS' strokes from x, y, size the letters' height, width the stroke on the page, which letters() keeps
    at 2.6: the label and the 4 take their own"""
    k = size / 16
    paths = "".join(f'<path transform="translate({x + i * 12 * k:.2f},{y:.2f}) scale({k:.4f})" '
                    f'd="{make_versions.GLYPHS[c]}"/>' for i, c in enumerate(s))
    return (f'<g stroke="{colour}" stroke-width="{width / k:.2f}" stroke-linecap="round" stroke-linejoin="round" '
            f'fill="none">{paths}</g>')


def text_width(s, size):
    return ((len(s) - 1) * 12 + 8) * size / 16


def band_path():
    """the band along the head's upper edge, from the hair to the plate, and the plate hanging over the front eye, as
    one outline: the band's top 7 above the edge, so it reads as worn on the head, and its bottom 11 below it, clear
    of the back eye"""
    px0, px1, pb = PLATE
    d = [f"M {BAND_BACK},{edge(BAND_BACK) + 11:.1f}",
         f"Q {BAND_BACK - 11},{edge(BAND_BACK) + 2:.1f} {BAND_BACK},{edge(BAND_BACK) - 7:.1f}"]
    d += [f"L {x},{edge(x) - 7:.1f}" for x in steps(BAND_BACK, px1)[1:]]
    d += [f"L {px1},{pb - 10}", f"Q {px1},{pb} {px1 - 10},{pb}", f"L {px0 + 10},{pb}", f"Q {px0},{pb} {px0},{pb - 10}"]
    d += [f"L {x},{edge(x) + 11:.1f}" for x in reversed(steps(BAND_BACK, px0))]
    return " ".join(d) + " Z"


def radiation(cx, cy, r):
    """the radiation sign on the plate: a yellow disc ringed in dark, three blades round a dot, two up and one down"""
    r1, r2 = r * 0.32, r * 0.8
    blades = []
    for a in (90, 210, 330):
        a0, a1 = math.radians(a - 30), math.radians(a + 30)
        p = [(cx + q * math.cos(t), cy + q * math.sin(t)) for q, t in ((r1, a0), (r2, a0), (r2, a1), (r1, a1))]
        blades.append(f"M {p[0][0]:.2f},{p[0][1]:.2f} L {p[1][0]:.2f},{p[1][1]:.2f} "
                      f"A {r2:.2f},{r2:.2f} 0 0 1 {p[2][0]:.2f},{p[2][1]:.2f} L {p[3][0]:.2f},{p[3][1]:.2f} "
                      f"A {r1:.2f},{r1:.2f} 0 0 0 {p[0][0]:.2f},{p[0][1]:.2f} Z")
    return (f'    <circle cx="{cx}" cy="{cy}" r="{r}" fill="{RADIATION}" stroke="{INK}" stroke-width="2.2"/>\n'
            f'    <path fill="{INK}" d="{" ".join(blades)}"/>\n'
            f'    <circle cx="{cx}" cy="{cy}" r="{r * 0.2:.2f}" fill="{INK}"/>\n')


def label(on, heavy=False):
    """the label on the band over the back eye, turned as the edge runs there: OFF in red, or ON in green with a
    glow, on a dark box; heavy, for the emojis, larger letters in a thicker line"""
    slope = math.degrees(math.atan((edge(LABEL_X + 1) - edge(LABEL_X - 1)) / 2))
    cy = edge(LABEL_X) + 2
    word, colour = ("ON", ON_GREEN) if on else ("OFF", OFF_RED)
    size, width = (13, 3.4) if heavy else (10, 2.3)
    w, h = (52, 19) if heavy else (44, 15)
    glow = (text(word, LABEL_X - text_width(word, size) / 2, cy - size / 2, size, ON_GREEN, width + 3.5)
            .replace(f'stroke="{ON_GREEN}"', f'stroke="{ON_GREEN}" stroke-opacity="0.35"') if on else "")
    return (f'  <g transform="{HEAD} rotate({slope:.2f} {LABEL_X} {cy:.2f})">\n'
            f'    <rect x="{LABEL_X - w / 2}" y="{cy - h / 2:.2f}" width="{w}" height="{h}" rx="4" '
            f'fill="{STEEL_DARK}"/>\n'
            f'    {glow}{text(word, LABEL_X - text_width(word, size) / 2, cy - size / 2, size, colour, width)}\n'
            '  </g>\n')


def tube(power):
    """the neon tube standing at the plate's front edge, across the head's upper edge as the drawing's stands beside
    her eye: its glass between two dark caps, a light core, a glow round it; power 0 Stable (a soft glow), 1 Ionized
    (brighter), 2 Overloaded (a wide glow and sparks off its top)"""
    x, y0, y1 = TUBE
    halo = {0: ((30, 0.16),), 1: ((32, 0.3), (46, 0.14)), 2: ((34, 0.42), (52, 0.22), (70, 0.1))}[power]
    out = [f'  <!-- the neon tube, {("stable", "ionized", "overloaded")[power]} -->\n  <g transform="{HEAD}">\n']
    for w, o in halo:
        out.append(f'    <rect x="{x - w / 2}" y="{y0 - w / 2 + 10}" width="{w}" height="{y1 - y0 + w - 20}" '
                   f'rx="{w / 2}" fill="{NEON}" fill-opacity="{o}"/>\n')
    out.append(f'    <rect x="{x - 7}" y="{y0 + 6}" width="14" height="{y1 - y0 - 12}" rx="5" fill="url(#gena-neon)" '
               f'stroke="{WHITE}" stroke-width="3"/>\n'
               f'    <path stroke="{WHITE}" stroke-opacity="{0.6 + 0.15 * power:g}" stroke-width="2.6" '
               f'stroke-linecap="round" d="M {x - 1.5},{y0 + 16} L {x - 1.5},{y1 - 16}"/>\n')
    for y in (y0, y1 - 11):
        out.append(f'    <rect x="{x - 10}" y="{y}" width="20" height="11" rx="3" fill="{STEEL_DARK}" '
                   f'stroke="{WHITE}" stroke-width="3"/>\n')
    if power == 2:  # sparks off the top: short zigzags, white edged
        for sx, sy, a in ((x - 18, y0 - 6, -30), (x + 16, y0 - 10, 25), (x + 22, y0 + 12, 70)):
            out.append(f'    <path transform="translate({sx},{sy}) rotate({a})" fill="none" stroke-linecap="round" '
                       f'stroke-linejoin="round" stroke="{WHITE}" stroke-width="7" d="M 0,-9 L 3,-2 L -3,2 L 0,9"/>\n'
                       f'    <path transform="translate({sx},{sy}) rotate({a})" fill="none" stroke-linecap="round" '
                       f'stroke-linejoin="round" stroke="{NEON}" stroke-width="3.2" d="M 0,-9 L 3,-2 L -3,2 L 0,9"/>\n')
    out.append("  </g>\n")
    return "".join(out)


def headband(on, power, heavy=False):
    """the band and its plate, the radiation sign on the plate, the label, the tube"""
    px0, px1, pb = PLATE
    mid = (px0 + px1) / 2
    return (f'''  <!-- her headband: the band along the top of the head, its plate over the front eye -->
  <g transform="{HEAD}">
    <path fill="url(#gena-steel)" stroke="{WHITE}" stroke-width="3.5" stroke-linejoin="round" d="{band_path()}"/>
    <path fill="none" stroke="{STEEL_DARK}" stroke-width="1.6" stroke-opacity="0.5" stroke-linecap="round"
          d="M {px0 + 3},{edge(px0) + 11:.1f} L {px1 - 3},{edge(px1) + 11:.1f}"/>
{radiation(mid, (edge(mid) + 11 + pb) / 2 + 1, 15 if not heavy else 17)}  </g>
''' + label(on, heavy) + tube(power))


def sparkle(cx, cy, r, gid):
    """a four-point light, the collar's blue one: four points joined by sides bowed in, ringed in white"""
    c = r * 0.16
    return (f'<path transform="translate({cx},{cy})" fill="url(#{gid})" stroke="{WHITE}" stroke-width="3" '
            f'stroke-linejoin="round" d="M 0,{-r} Q {c},{-c} {r},0 Q {c},{c} 0,{r} Q {-c},{c} {-r},0 '
            f'Q {-c},{-c} 0,{-r} Z"/>')


def four():
    """her shirt's big 4, white, on the front wing right of the trim, turned as the wing leans"""
    return ('  <!-- her shirt\'s big 4 -->\n'
            f'  <g transform="translate(268,200) rotate(9)">{text("4", -11.5, -23, 46, WHITE, 5.5)}</g>\n')


def collar():
    """the collar's two lights on the trim, at the neck: a red one, long as the drawing's, and a blue sparkle"""
    x, y, nx, ny = trim_point(0.1)
    turn = math.degrees(math.atan2(-nx, ny))  # along the trim
    bx, by, _, _ = trim_point(0.2)
    return (f'  <!-- the collar\'s lights on the trim: red, and a blue sparkle -->\n'
            f'  <rect transform="translate({x:.2f},{y:.2f}) rotate({turn:.2f})" x="-7" y="-2.6" width="14" '
            f'height="5.2" rx="2.6" fill="#FF4A52" stroke="{WHITE}" stroke-width="1.6"/>\n'
            f'  <g transform="translate({bx:.2f},{by:.2f})">'
            f'<circle r="7" fill="#6FC3FF" fill-opacity="0.35"/>{sparkle(0, 0, 6.5, "gena-blue")}</g>\n')


def pleats():
    """the skirt's pleats on the back wing, along its length, a shade and a light beside each; under the front wing"""
    lines = ("M 180,40 C 166,120 166,220 200,322", "M 194,34 C 184,120 186,222 210,322",
             "M 207,48 C 204,120 208,220 216,322")
    shade = "".join(f'<path d="{d}" stroke="#2E8044" stroke-width="2.4" stroke-opacity="0.55"/>' for d in lines)
    light = "".join(f'<path transform="translate(3.2,0)" d="{d}" stroke="#B5F5C0" stroke-width="1.6" '
                    'stroke-opacity="0.55"/>' for d in lines)
    return ('  <!-- the skirt\'s pleats on the back wing, under the front wing -->\n'
            f'  <clipPath id="gena-skirt-clip"><path d="{BACK_WING_D}"/></clipPath>\n'
            f'  <g clip-path="url(#gena-skirt-clip)" fill="none" stroke-linecap="round">{shade}{light}</g>\n')


# ---- her face: one eye shows, the plate covers the other (eye 1); lw is the lines' width, heavier on the emojis
EYE = 0  # the eye the plate leaves bare


def lid_gradient(i, gid):
    """the lid in the face's own gradient, laid where the head's is, so no disc shows round the eye (as eyes_svg's
    lid="skin", for a lid drawn upright on the page)"""
    cx, cy = face_centre(i)
    return (f'  <linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="217.78" y1="0" x2="508.05" y2="0" '
            f'gradientTransform="translate({-cx:.2f},{-cy:.2f})"><stop offset="0" stop-color="{LID_SKIN[0]}"/>'
            f'<stop offset="1" stop-color="{LID_SKIN[1]}"/></linearGradient>\n')


def eye_half(lw, look=(0, 3), lid=-4, droop=3, glint=False):
    """the eye half shut, Stable: the green iris under a heavy lid, level on the page as Aogo's ^ stand upright (in
    the head's tilt the lid would read as a glare), its outer end droop lower, sleepy; the iris turned by look; glint
    for Ionized's knowing look"""
    cx, cy = face_centre(EYE)
    ix, iy = look
    big = f'<circle cx="{ix - 5}" cy="{iy - 3}" r="5" fill="{WHITE}"/>' if glint else ""
    return (lid_gradient(EYE, "gena-lid")
            + '  <clipPath id="gena-eye-clip"><circle r="22"/></clipPath>\n'
            f'  <g transform="translate({cx:.2f},{cy:.2f})" stroke-linecap="round">\n'
            f'    <circle r="21" fill="{INK}"/>\n'
            f'    <circle cx="{ix}" cy="{iy}" r="15.5" fill="url(#iris)"/>{big}\n'
            f'    <circle cx="{ix + 5}" cy="{iy + 6}" r="2.6" fill="{WHITE}" fill-opacity="0.7"/>\n'
            f'    <path clip-path="url(#gena-eye-clip)" fill="url(#gena-lid)" '
            f'd="M -30,-40 L 30,-40 L 30,{lid} L -30,{lid + droop} Z"/>\n'
            f'    <path stroke="{INK}" stroke-width="{lw}" fill="none" '
            f'd="M -25,{lid + droop + 0.5} L 23,{lid - 0.3}"/>\n'
            '  </g>\n')


def eye_caret(lw):
    """shut in a smile, a ^ standing upright as it is typed (Aogo's)"""
    cx, cy = face_centre(EYE)
    return (f'  <path transform="translate({cx:.2f},{cy:.2f})" stroke="{INK}" stroke-width="{lw}" '
            'stroke-linejoin="round" stroke-linecap="round" fill="none" d="M -15,8 L 0,-9 L 15,8"/>\n')


def eye_wide(lw):
    """wide open in a panic: the white round a small iris, a tiny glint, the rim drawn whole"""
    cx, cy = face_centre(EYE)
    return (f'  <g transform="translate({cx:.2f},{cy:.2f})">\n'
            f'    <circle r="20" fill="{WHITE}" stroke="{INK}" stroke-width="{lw * 0.75:g}"/>\n'
            f'    <circle cx="1" cy="1" r="8.5" fill="url(#iris)" stroke="{INK}" stroke-width="2"/>\n'
            f'    <circle cx="-2" cy="-2.5" r="2.6" fill="{WHITE}"/>\n'
            '  </g>\n')


def mouth(kind, lw):
    """between the eyes and below them, where her sisters have theirs, in the head's frame: pout, Stable's small frown
    with a fang; cat, a :3 with a fang; grin, open on the drawing's green tongue, a fang; gasp, a small open o"""
    fang = (f'<path fill="{WHITE}" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round" '
            'd="M 194,{y} L 196.5,{y2} L 199,{y}"/>')
    if kind == "pout":
        body = (f'<path d="M 179,43 Q 188,34 199,41" fill="none" stroke="{INK}" stroke-width="{lw * 0.8:g}" '
                'stroke-linecap="round"/>' + fang.format(y="40.5", y2="47"))
    elif kind == "cat":
        body = (f'<path d="M 176,36 Q 182,44 189,38 Q 196,44 203,36" fill="none" stroke="{INK}" '
                f'stroke-width="{lw * 0.8:g}" stroke-linecap="round" stroke-linejoin="round"/>'
                + fang.format(y="40", y2="46.5"))
    elif kind == "grin":
        body = (f'<path fill="#1E5A32" stroke="{INK}" stroke-width="{lw * 0.6:g}" stroke-linejoin="round" '
                'd="M 176,31 L 206,31 Q 206,53 191,53 Q 176,53 176,31 Z"/>'
                f'<path fill="{NEON}" d="M 181,47 Q 191,40 201,47 Q 197,51.5 191,51.5 Q 185,51.5 181,47 Z"/>'
                f'<path fill="{WHITE}" d="M 197,32.5 L 199.5,39 L 202,32.5 Z"/>')
    elif kind == "gasp":
        body = (f'<path fill="#1E5A32" stroke="{INK}" stroke-width="{lw * 0.6:g}" stroke-linejoin="round" '
                'd="M 183,36 Q 191,30 199,36 Q 199,48 191,48 Q 183,48 183,36 Z"/>'
                f'<path fill="{NEON}" d="M 186,44.5 Q 191,41 196,44.5 Q 194,47 191,47 Q 188,47 186,44.5 Z"/>')
    else:
        raise ValueError(f"mouth {kind!r}: one of pout, cat, grin, gasp")
    return f'  <g transform="{HEAD}">\n    {body}\n  </g>\n'


def blush(lw):
    """Ionized's blush: short orange strokes slanted over the bare cheek, as the drawing hatches it"""
    return (f'  <path transform="{HEAD}" fill="none" stroke="#FF8A4A" stroke-width="{max(2.8, lw * 0.5):g}" '
            'stroke-linecap="round" d="M 147,42 L 153,31 M 156,43 L 162,32 M 165,44 L 171,33"/>\n')


def heart(x, y, size=1.0):
    """an orange-yellow heart, ringed in white, as the drawing's float round her when she is happy"""
    return (f'  <path transform="translate({x},{y}) scale({size:g}) rotate(12)" fill="{TIP}" stroke="{WHITE}" '
            'stroke-width="3.5" stroke-linejoin="round" '
            'd="M 0,12 C -16,1 -15,-13 -6.5,-13 C -2.5,-13 0,-10 0,-7 '
            'C 0,-10 2.5,-13 6.5,-13 C 15,-13 16,1 0,12 Z"/>\n')


def sweat():
    """a drop of sweat over the top of the head, between the ahoge and the tube, ringed in white"""
    return (f'''  <!-- a drop of sweat over the top of the head -->
  <g transform="{HEAD} translate(228,-80) rotate(10)">
    <path fill="#8FD3F7" stroke="{WHITE}" stroke-width="4" stroke-linejoin="round"
          d="M 0,-20 Q 13,-2 13,7 A 13,13 0 0 1 -13,7 Q -13,-2 0,-20 Z"/>
    <path fill="none" stroke="{WHITE}" stroke-width="3.2" stroke-linecap="round" d="M -5.5,4 Q -6.5,11 -1,14"/>
  </g>
''')


DEFS = (gradient("gena-steel", STEEL)
        + gradient("gena-neon", ("#18B552", NEON, "#E2FFEC", NEON, "#18B552"), vertical=False)
        + gradient("gena-tips", (TIP, "#FFCB4A", "#7FEA6E", "#4CEA80", "#2FC665"), vertical=False)
        + gradient("gena-ahoge", ("#62F28E", "#2CC95E"))
        + gradient("gena-skirt", SKIRT)
        + gradient("gena-blue", ("#BFE6FF", "#4FA8F5")))

GENA = character(
    name="Gena", who="Gena", who_full="Gena",
    hair_word="neon green hair, a clip and a headband with a neon tube",
    hair_colour="neon green", trim_word="grey collar", eyes_word="Gena's: the front one under the headband's plate, "
                                                                 "the other green, half shut and stable",
    source="colours from Kedr's fan drawing of Gemini 4 Neon, \"Gemini 4 neons Chain of thought\" (signed Kedr.bit "
           "and Ked_bit)",
    palette_note="Gena: neon green hair, orange-yellow tips on the left leaf below, an ahoge striped orange over "
                 "green, a black clip with GN in white, a grey headband with an OFF / ON label, a radiation sign on "
                 "the plate over the front eye and a neon tube, a black shirt with a 4, a grey collar with a red and a "
                 "blue light, a green pleated skirt with 40, pale lavender skin, green eyes",
    hair=("#5FF48C", "#2DCB5F"), tail=("#52EE84", "#25B556"), tail_dark=("#2FBF5E", "#1B8A43"),
    far=("#3CD66E", "#1F9C4C"), far_dark=("#2AA756", "#167238"),
    outfit=("#3D4252", "#1C1F28"), back_wing="url(#gena-skirt)", trim="#A4B1BC", trim_width=8,
    iris=("#B4FFC8", "#33CF62", "#10692E"), rim=INK, shine="#C2FFD6", skin=LID_SKIN,
    # GN on the clip, 40 on the skirt: her designation, GN40, as her sisters carry theirs
    eyes="caret", mark="40", mark_colour="#173F25",
    tails_note="her long hair, loose: the head's back and the two leaves below, no tail, the left one tipped "
               "orange-yellow",
    ahoge=AHOGE, lower_fills=("url(#gena-tips)",), defs_extra=DEFS,
    back_extras=pleats(), wing_extras=four() + collar(),
)

AHOGE_DRAWN = (f'  <path transform="{HEAD}" fill="url(#hair)" stroke="#FFFFFF" stroke-width="4"\n'
               f'        stroke-linejoin="round"\n        d="{AHOGE}"/>\n')
AHOGE_STRIPED = (f'  <g transform="{HEAD}">\n'
                 f'    <path fill="url(#gena-ahoge)" d="{AHOGE}"/>\n'
                 f'    <path fill="{TIP}" d="{STRIPE}"/>\n'
                 f'    <path fill="none" stroke="{WHITE}" stroke-width="4" stroke-linejoin="round" d="{AHOGE}"/>\n'
                 '  </g>\n')


def gena(face, on=False, power=0, heavy=False, extras=""):
    """Gena with face (her eye and mouth, drawn over the head) in place of the drawing's eyes, the headband ON or OFF
    with the tube at power, heavy for the emojis' lines; extras over everything (a sign, hearts, sweat)"""
    p = {**GENA, "head_extras": headband(on, power, heavy)
         + clip("GN", place=CLIP, note="the black clip in her hair, GN on it")}
    s = vocaloid(p)
    assert s.count(AHOGE_DRAWN) == 1  # the curl make_vocaloid draws in the hair's colour: hers is striped
    s = s.replace(AHOGE_DRAWN, AHOGE_STRIPED)
    shut = eyes_svg(p)  # the drawing's ^ eyes, which her face replaces: the plate covers the front one
    assert s.count(shut) == 1
    s = s.replace(shut, f"  <!-- her face, the eye the plate leaves bare -->\n{face}")
    assert s.rstrip().endswith("</svg>")
    end = s.rindex("</svg>")
    return s[:end] + extras + s[end:]


def stable(lw=4.5):
    """the drawing's face: Stable, non-reactive: the eye half shut, a small frown with a fang"""
    return eye_half(lw) + mouth("pout", lw)


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    with open(os.path.join(HERE, "out", "wimsy-gena.svg"), "w") as f:
        f.write(gena(stable()))
    print("out/wimsy-gena.svg")
