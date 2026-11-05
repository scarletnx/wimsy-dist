#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 the wimsy-dist contributors
"""make_vocaloid.py: Wimsy as other singing voices, from the Teto drawing (make_versions.version), each with her hair,
her colours and her look in the eyes. Hatsune Miku (piapro's official illustration), Akita Neru (her first
illustration), Utane Uta / Defoko (Renta's), Adachi Rei (missile39's and Kitsune's), GUMI (the Megpoid V4 box). A tail
or a lock is a long leaf of two arcs, as the wings are."""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # beside it, also under python3 -I
sys.dont_write_bytecode = True  # no __pycache__ left beside the drawings
from make_versions import GLYPHS, version  # noqa: E402

TAIL_LEAF = "M -22,6 Q -42,120 2,236 Q 34,118 22,6 Q 0,-6 -22,6 Z"
# the head's own frame: the base of the leaves, the head's axis toward its tip
HEAD = "translate(217.8,336.7) rotate(-26.68)"
# the eyes as Wimsy has them, in her eyes' rotated frame: centres, the rim's radius
EYE_TURN = 24.165289
EYES = ((434.99091, 99.701668), (485.51288, 44.356552))
RIM = 23.114985
# Teto's curl on top of the head, in the head's frame: what an ahoge of a design's own replaces
TETO_CURL = ("M 126,-38 C 110,-100 180,-126 196,-88 C 204,-68 184,-54 172,-66 C 180,-78 168,-96 150,-86 "
             "C 136,-78 138,-56 142,-38 Z")


def tail_group(gid, light, tie, band, tie_h, vein=None):
    """a tail pointing down from its tie at 0,0: one long leaf, a light vein along it (vein, its colour), the tie on
    top (none for a lock)"""
    tie_svg = ""
    if tie:
        tie_svg = (f'      <rect x="-30" y="{-tie_h / 2:g}" width="60" height="{tie_h}" rx="{tie_h / 2:g}" fill="{tie}" '
                   'stroke="#FFFFFF" stroke-width="3"/>\n'
                   f'      <rect x="-23" y="-2" width="46" height="4" rx="2" fill="{band}"/>\n')
    vein_svg = (f'      <path d="M 2,14 Q -6,120 3,214" fill="none" stroke="{vein}" stroke-width="3.5" '
                'stroke-linecap="round" stroke-opacity="0.6"/>\n' if vein else "")
    return (f'    <g id="{gid}">\n'
            f'      <path fill="url(#{light})" stroke="#FFFFFF" stroke-width="4.5" stroke-linejoin="round" d="{TAIL_LEAF}"/>\n'
            + vein_svg + tie_svg + '    </g>\n')


def face_centre(i):
    """eye i's centre on the page"""
    x, y = EYES[i]
    t = math.radians(EYE_TURN)
    return x * math.cos(t) - y * math.sin(t), x * math.sin(t) + y * math.cos(t)


def frame_shift(gx, gy):
    """a shift on the page, in the eyes' rotated frame"""
    t = math.radians(EYE_TURN)
    return gx * math.cos(t) + gy * math.sin(t), -gx * math.sin(t) + gy * math.cos(t)


def eyes_svg(p):
    """the eyes: Wimsy's circles in her colours, and over them in each eye's own frame (x along the head toward its
    tip, -y toward the top of the face) what the look needs. round: as drawn; tsundere: lids slanting down to the
    inner corners, a frowning brow, the eyes turned aside; deadpan: a flat lid over the upper half, no sparkle; lens:
    a camera's lens for an iris, a dark ring and a dot, wide open, small glints only; lens-soft: the lens under a
    gently arched lid; lens-cool: the lens under a flat lid half way down; sly: a dark iris with a small light at its
    middle (pupil), turned aside under a heavy lid that droops to the outer corner, the white showing at that corner,
    two short tired lines under it; caret: shut in a smile, each eye a ^ (Yi Xi's ^q^); tired: open under a heavy lid
    that sags to the outer corner, a dull small glint, a dark crescent under each eye (bags); wink: the back eye open
    with its big glint, the front one shut in an arc with a flick of lashes at its outer corner; meh: the back eye under
    the bangs (a hair_path that covers it), not drawn, the front one half shut under a lid that sags to the outer
    corner, a dull small glint, its brow raised at the inner end"""
    look = p.get("eyes", "round")
    lens = look.startswith("lens")
    # the eyes turned aside, toward the back of the head, for the tsundere's look away
    a = math.radians(-26.68)
    sx, sy = frame_shift(-4 * math.cos(a), -4 * math.sin(a)) if look in ("tsundere", "sly") else (0, 0)
    out = [f"  <!-- the eyes, where Wimsy has them, {p['eyes_word']} -->\n"]
    if p["iris2"]:  # the front eye of its own colour
        out.append('  <radialGradient id="iris2" cx="0.5" cy="0.62" r="0.6">'
                   f'<stop offset="0" stop-color="{p["iris2"][0]}"/><stop offset="0.7" stop-color="{p["iris2"][1]}"/>'
                   f'<stop offset="1" stop-color="{p["iris2"][2]}"/></radialGradient>\n')
    lids = [p["lid"]] * 2
    if p["lid"] == "skin":  # the lid in the face's own gradient, laid on the page where the head's is: no edge shows
        skin = p["skin"] or ("#F7D9CE", "#FDEDE6")
        for i in range(2):
            cx, cy = face_centre(i)
            out.append(f'  <linearGradient id="lid-{i}" gradientUnits="userSpaceOnUse" x1="217.78" y1="0" x2="508.05" '
                       f'y2="0" gradientTransform="rotate(26.68) translate({-cx:.2f},{-cy:.2f})">'
                       f'<stop offset="0" stop-color="{skin[0]}"/><stop offset="1" stop-color="{skin[1]}"/>'
                       '</linearGradient>\n')
            lids[i] = f"url(#lid-{i})"
    out.append(f'  <g transform="rotate({EYE_TURN})">\n')
    for i, (x, y) in enumerate(EYES):
        if look == "caret":  # shut: no eye to draw, its ^ comes below
            continue
        if (look, i) in (("wink", 1), ("meh", 0)):  # shut, its arc comes below; or under the bangs
            continue
        ix, iy = x + sx, y - 3.5 + sy
        iris = "iris2" if p["iris2"] and i == 1 else "iris"
        out.append(f'    <circle cx="{x}" cy="{y}" r="{RIM}" fill="{p["rim"]}"/>\n')
        out.append(f'    <circle cx="{ix:.2f}" cy="{iy:.2f}" r="17.5" fill="url(#{iris})"/>\n')
        if lens:  # the lens: its ring and its dot
            out.append(f'    <circle cx="{ix:.2f}" cy="{iy:.2f}" r="9.5" fill="none" stroke="{p["ring"]}" stroke-width="2.4"/>\n')
            out.append(f'    <circle cx="{ix:.2f}" cy="{iy:.2f}" r="4.2" fill="{p["ring"]}"/>\n')
            out.append(f'    <circle cx="{ix - 5:.2f}" cy="{iy - 7:.2f}" r="3.4" fill="#FFFFFF"/>\n')
            out.append(f'    <circle cx="{ix + 4.5:.2f}" cy="{iy + 4.5:.2f}" r="1.8" fill="#FFFFFF" fill-opacity="0.85"/>\n')
            continue
        if look == "sly":  # no glint: the small light at the middle comes with the lid, below it
            continue
        dull = look in ("deadpan", "tired", "meh")  # no big glint: the lid covers where it would be
        if not dull:
            out.append(f'    <circle cx="{x - 4.6 + sx:.2f}" cy="{y - 10.3 + sy:.2f}" r="7" fill="#FFFFFF"/>\n')
        out.append(f'    <circle cx="{x + 5.4 + sx:.2f}" cy="{y + 3.9 + sy:.2f}" r="3" fill="#FFFFFF" '
                   f'fill-opacity="{0.55 if dull else 0.85}"/>\n')
    out.append("  </g>\n")
    if p["mole"]:  # a beauty mark, in the head's frame
        out.append(f'  <circle transform="{HEAD}" cx="{p["mole"][0]}" cy="{p["mole"][1]}" r="2.6" fill="{p["rim"]}"/>\n')
    if p["mouth"]:  # a smile below the back eye, toward the back of the face
        out.append(f'  <path transform="{HEAD}" d="M 74,14 Q 88,27 104,16" fill="none" stroke="{p["mouth"]}" '
                   'stroke-width="4" stroke-linecap="round"/>\n')
    if look in ("round", "lens"):
        return "".join(out)
    out.append('  <clipPath id="eye-clip"><circle r="24.5"/></clipPath>\n')
    for i in range(2):
        cx, cy = face_centre(i)
        g = [f'  <g transform="translate({cx:.2f},{cy:.2f}) rotate(-26.68)" stroke-linecap="round">\n']
        if look == "tsundere":  # the inner corner is toward the other eye
            hi, lo = (-13, -3) if i == 0 else (-3, -13)
            g.append(f'    <path clip-path="url(#eye-clip)" fill="{p["lid"]}" d="M -30,-40 L 30,-40 L 30,{lo if i == 0 else hi} '
                     f'L -30,{hi if i == 0 else lo} Z"/>\n')
            g.append(f'    <path stroke="{p["rim"]}" stroke-width="3.5" fill="none" d="M -22,{hi + (1 if i == 0 else 0)} '
                     f'L 22,{lo + (0 if i == 0 else 1)}"/>\n')
            bl, br = (-27, -19) if i == 0 else (-19, -27)
            g.append(f'    <path stroke="{p["brow"]}" stroke-width="4.5" fill="none" d="M -17,{bl} L 17,{br}"/>\n')
        elif look == "deadpan":
            g.append(f'    <path clip-path="url(#eye-clip)" fill="{p["lid"]}" d="M -30,-40 L 30,-40 L 30,-2 L -30,-2 Z"/>\n')
            g.append(f'    <path stroke="{p["rim"]}" stroke-width="3.5" fill="none" d="M -22,-2 L 22,-2"/>\n')
        elif look == "lens-soft":  # a lid arched at the middle: calm, about to smile
            g.append(f'    <path clip-path="url(#eye-clip)" fill="{p["lid"]}" d="M -30,-40 L 30,-40 L 30,-6 Q 0,-22 -30,-6 Z"/>\n')
            g.append(f'    <path stroke="{p["rim"]}" stroke-width="3.5" fill="none" d="M -22,-9 Q 0,-20 22,-9"/>\n')
        elif look == "lens-cool":
            g.append(f'    <path clip-path="url(#eye-clip)" fill="{p["lid"]}" d="M -30,-40 L 30,-40 L 30,-5 L -30,-5 Z"/>\n')
            g.append(f'    <path stroke="{p["rim"]}" stroke-width="3.5" fill="none" d="M -22,-5 L 22,-5"/>\n')
        elif look == "sly":  # half shut under a heavy lid; the light low in the iris, turned aside; a sliver of
            # white at the outer corner; two tired lines under the eye
            g.append(f'    <path clip-path="url(#eye-clip)" fill="#FFFFFF" d="M 12,6 Q 19,5 22,11 Q 16,12 12,6 Z"/>\n')
            g.append(f'    <circle cx="-4" cy="9" r="6.5" fill="{p["pupil"]}" fill-opacity="0.3"/>\n')
            g.append(f'    <circle cx="-4" cy="9" r="3.6" fill="{p["pupil"]}"/>\n')
            g.append(f'    <path clip-path="url(#eye-clip)" fill="{p["lid"]}" d="M -30,-40 L 30,-40 L 30,4 Q 0,-4 -30,1 Z"/>\n')
            g.append(f'    <path stroke="{p["rim"]}" stroke-width="4.5" fill="none" d="M -23,1 Q 0,-4 23,3 L 27,0"/>\n')
            g.append(f'    <path stroke="{p["rim"]}" stroke-width="2" fill="none" d="M -12,29 L 4,30 M -6,34 L 10,35"/>\n')
        elif look == "tired":  # the lid sags to the outer corner, away from the other eye; the bags under it
            left, right = (0, -8) if i == 0 else (-8, 0)  # the lid's edge at x = -23 and at x = 23
            g.append(f'    <path fill="{p["bags"]}" fill-opacity="0.55" '
                     'd="M -21,13 A 25,25 0 0 0 21,13 Q 0,49 -21,13 Z"/>\n')
            g.append(f'    <path clip-path="url(#eye-clip)" fill="{lids[i]}" '
                     f'd="M -30,-40 L 30,-40 L 30,{right} L 23,{right} Q 0,-10 -23,{left} L -30,{left} Z"/>\n')
            g.append(f'    <path stroke="{p["rim"]}" stroke-width="4.5" fill="none" '
                     f'd="M -23,{left} Q 0,-10 23,{right}"/>\n')
        elif look == "wink" and i == 1:  # shut in an arc bowed up, the lashes flicking out at the outer corner
            g.append(f'    <path stroke="{p["rim"]}" stroke-width="5.5" fill="none" d="M -17,4 Q 0,-14 17,4"/>\n')
            g.append(f'    <path stroke="{p["rim"]}" stroke-width="3.2" fill="none" '
                     'd="M 12,-2 L 18,-10 M 17,3 L 26,-1"/>\n')
        elif look == "meh" and i == 1:  # half shut, sagging away from the hidden eye; the brow up at the inner end
            g.append(f'    <path clip-path="url(#eye-clip)" fill="{lids[i]}" '
                     'd="M -30,-40 L 30,-40 L 30,1 L 23,1 Q 0,-5 -23,-4 L -30,-4 Z"/>\n')
            g.append(f'    <path stroke="{p["rim"]}" stroke-width="4.5" fill="none" d="M -23,-4 Q 0,-5 23,1"/>\n')
            g.append(f'    <path stroke="{p["brow"]}" stroke-width="3.2" fill="none" d="M -12,-34 Q 1,-31 12,-21"/>\n')
        elif look == "caret":  # a ^ standing upright as it is typed, whatever the head's tilt: shut in a smile
            out.append(f'  <path transform="translate({cx:.2f},{cy:.2f})" stroke="{p["rim"]}" stroke-width="5.5" '
                       'stroke-linejoin="round" stroke-linecap="round" fill="none" d="M -15,7 L 0,-9 L 15,7"/>\n')
        g.append("  </g>\n")
        if len(g) > 2:
            out += g
    return "".join(out)


def letters(text, x, y, size, colour):
    """text in GLYPHS' strokes, size the letters' height, from x, y in the frame it is drawn in"""
    k = size / 16
    paths = "".join(f'<path transform="translate({x + i * 12 * k:.2f},{y}) scale({k:.3f})" d="{GLYPHS[c]}"/>'
                    for i, c in enumerate(text))
    return (f'<g stroke="{colour}" stroke-width="{2.6 / k:.2f}" stroke-linecap="round" stroke-linejoin="round" '
            f'fill="none">{paths}</g>')


def vocaloid(p):
    s = version(p)
    # the drills' turns and groups give way to the tails, or to nothing
    a = s.index('    <g id="drill-turns">')
    b = s.index('  </defs>')
    tails = tail_group("drill", "tail", p["tie"], p["band"], p["tie_h"], p["tail_vein"]) if p["near_use"] else ""
    if p["far_use"]:  # a second tail, behind the head
        tails += tail_group("drill-far", "far", p["tie"], p["band"], p["tie_h"], p["tail_vein"])
    s = s[:a] + f'    <!-- {p["tails_note"]} -->\n' + tails + s[b:]
    far = '  <use xlink:href="#drill-far" transform="translate(256,300) rotate(5) scale(0.62,0.48)"/>'
    near = '  <use xlink:href="#drill" transform="translate(322,320) rotate(-10) scale(0.66,0.5)"/>'
    assert far in s and near in s
    s = s.replace(far + "\n" if not p["far_use"] else far, p["far_use"])
    s = s.replace(near + "\n" if not p["near_use"] else near, p["near_use"])
    s = s.replace("  <!-- the far drill, behind the head, in darker crimsons -->\n", p["far_note"])
    s = s.replace("  <!-- the near drill, in front -->\n", p["near_note"])
    if not p["ahoge"]:
        a = s.index("  <!-- Teto's curl on top of the head")
        b = s.index("  <!-- the wings in the outfit's grey -->")
        s = s[:a] + s[b:]
    else:
        s = s.replace("Teto's curl on top of the head", f"{p['who']}'s curl on top of the head")
    if isinstance(p["ahoge"], str):  # a curl of the design's own, in the head's frame, in place of Teto's
        assert TETO_CURL in s
        s = s.replace(TETO_CURL, p["ahoge"])
    # what a design draws its own way: gradients of its own, a wing or each leaf below in one of them, its face's
    # colour, its hair's outline over the head
    if p["defs_extra"]:
        s = s.replace("  </defs>", p["defs_extra"] + "  </defs>", 1)
    if p["back_extras"]:  # between the wings: the front wing covers what lies under it
        old = '  <path fill="url(#outfit)" stroke="#FFFFFF" stroke-width="5.47474"'
        assert old in s
        s = s.replace(old, p["back_extras"] + old, 1)
    if p["front_fill"]:
        old = '<path fill="url(#outfit)" stroke="#FFFFFF" stroke-width="5.47474"'
        assert old in s
        s = s.replace(old, f'<path fill="{p["front_fill"]}" stroke="#FFFFFF" stroke-width="5.47474"', 1)
    for fill in p["lower_fills"]:
        old = '<path fill="url(#tail)" stroke="#FFFFFF" stroke-width="3.64433"'
        assert old in s
        s = s.replace(old, f'<path fill="{fill}" stroke="#FFFFFF" stroke-width="3.64433"', 1)
    if p["skin"]:
        old = '<stop offset="0" stop-color="#F7D9CE"/>\n      <stop offset="1" stop-color="#FDEDE6"/>'
        assert old in s
        s = s.replace(old, f'<stop offset="0" stop-color="{p["skin"][0]}"/>\n      <stop offset="1" stop-color="{p["skin"][1]}"/>')
    if p["hair_path"]:
        old = ('<path fill="url(#hair)"\n            d="M -40,-200 L 340,-200 L 340,-40 L 300,-36 L 274,-8 L 258,-32 L 222,-28 '
               'L 194,-4 L 178,-30 L 134,-28 L 114,28 L 102,90 L -40,90 Z"/>')
        assert old in s
        s = s.replace(old, f'<path fill="{p["hair_fill"] or "url(#hair)"}"\n            d="{p["hair_path"]}"/>')
    # the eyes, each one's look
    a = s.index("  <!-- the eyes, where Wimsy has them")
    b = s.index("  </g>\n", a) + len("  </g>\n")
    s = s[:a] + eyes_svg(p) + s[b:]
    # what the drawing says it is
    s = s.replace("with Kasane Teto's twin drills and colours.", f"with {p['who_full']}'s {p['hair_word']} and colours.")
    s = s.replace(f"<dc:title>Wimsy with twin drills, {p['name']}</dc:title>",
                  f"<dc:title>Wimsy with {p['who_full']}'s {p['hair_word']}</dc:title>")
    s = s.replace(f"(twin drills, Kasane Teto's {p['name']} colours)", f"({p['hair_word']}, {p['who_full']}'s colours)")
    s = s.replace(f"the {p['name']} design's colours; fan art.", f"{p['source']}; fan art.")
    s = s.replace("the outfit's red trim along the front wing", f"the outfit's {p['trim_word']} trim along the front wing")
    s = s.replace("<!-- the two leaves below, in crimson -->", f"<!-- the two leaves below, in the hair's {p['hair_colour']} -->")
    s = s.replace("<!-- Teto: crimson hair and its shade, red eyes, a near-black grey outfit with red trim -->",
                  f"<!-- {p['palette_note']} -->")
    return s


def character(**kw):
    base = {"tie_mark": "", "band": "#000000", "tie_h": 16, "tie": None, "far_use": "", "near_use": "",
            "far_note": "", "near_note": "", "ahoge": False, "mark": "", "wing_extras": "", "head_extras": "",
            "front_extras": "", "eyes": "round", "lid": "#FCE9E1", "brow": "#000000", "trim_width": 5,
            "ring": "#000000", "defs_extra": "", "front_fill": "", "lower_fills": (), "skin": None, "hair_path": "",
            "hair_fill": "", "iris2": None, "mouth": "", "back_extras": "", "tail_vein": None, "pupil": "#FFFFFF",
            "mole": None, "bags": "#82728C"}
    base.update(kw)
    return base


MIKU = character(
    name="Hatsune Miku", who="Miku", who_full="Hatsune Miku", hair_word="twintails",
    hair_colour="teal", trim_word="teal", eyes_word="Miku's teal",
    source="colours from piapro's official illustration",
    palette_note="Miku: teal hair and its shade, teal eyes, a grey top, black sleeves with teal trim",
    hair=("#5CCBC8", "#2EA7A9"), tail=("#51BDC0", "#18959B"), tail_dark=("#2BA3A6", "#136567"),
    far=("#3AA8AB", "#147A7E"), far_dark=("#1E8A8E", "#0F5658"),
    outfit=("#B9BDC1", "#8F9398"), back_wing="#2B2E30", trim="#39C5BB",
    iris=("#8AE3E0", "#1FA3A8", "#0D5E62"), rim="#0E3236", shine="#A8ECEA",
    # her hair ties: near black squares with a pink line
    tie="#2F3133", band="#E0457B", tie_h=16,
    tails_note="her twintails: a single long leaf each, one on each side, where Teto's drills are: the far one behind "
               "the head, the near one in front, a black tie with pink",
    far_use='  <use xlink:href="#drill-far" transform="translate(256,300) rotate(5) scale(0.72,0.44)"/>',
    near_use='  <use xlink:href="#drill" transform="translate(322,320) rotate(-10) scale(0.78,0.47)"/>',
    far_note="  <!-- the far twintail, behind the head, in darker teals -->\n",
    near_note="  <!-- the near twintail, in front -->\n",
    mark="01",
)

NERU = character(
    name="Akita Neru", who="Neru", who_full="Akita Neru", hair_word="side ponytail",
    hair_colour="gold", trim_word="yellow", eyes_word="Neru's amber, a tsundere's glare turned aside",
    source="colours from her first illustration",
    palette_note="Neru: golden hair and its shade, amber eyes, a warm grey top, dark sleeves with yellow trim",
    hair=("#F8D86E", "#E3AF46"), tail=("#F6D267", "#DA9D36"), tail_dark=("#E5B34E", "#B38836"),
    far=("#E5B34E", "#B38836"), far_dark=("#C99A3E", "#987444"),
    outfit=("#B8B1A8", "#918A82"), back_wing="#3A342E", trim="#F2C230",
    iris=("#F5CF7A", "#C98A2E", "#7A5420"), rim="#3A2812", shine="#FFF2B8",
    # the blue scrunchie her one tail is tied with
    tie="#5C7695", band="#3F5A80", tie_h=20,
    tails_note="her one side ponytail: a single long leaf, so it reads as one, tied in a blue scrunchie",
    near_use='  <use xlink:href="#drill" transform="translate(322,318) rotate(-8) scale(0.9,0.48)"/>',
    near_note="  <!-- the side ponytail, in front -->\n",
    ahoge=True, mark="DEN2", eyes="tsundere", brow="#9A6A1E",
)

DEFOKO = character(
    name="Utane Uta", who="Defoko", who_full="Utane Uta (Defoko)", hair_word="short hair and beret",
    hair_colour="purple", trim_word="purple", eyes_word="Defoko's purple, half shut and blank",
    source="colours from Renta's illustration",
    palette_note="Defoko: purple hair and its shade, purple eyes, a white shirt, black sleeves with purple trim",
    hair=("#A66BB8", "#7E4A98"), tail=("#9161A1", "#74438F"), tail_dark=("#74438F", "#4E2F66"),
    far=("#74438F", "#4E2F66"), far_dark=("#5E3878", "#3E2552"),
    outfit=("#F5F3F7", "#D6D1DD"), back_wing="#26202F", trim="#9161A1",
    iris=("#C9A6E0", "#8E5BB0", "#4E2F66"), rim="#2A1B33", shine="#E6CDF2",
    tails_note="her short hair has no tail",
    eyes="deadpan",
    # her black beret with UTAU on it, and her white headphones ringed in blue
    head_extras=f'''  <!-- her black beret with UTAU on it, and her white headphones ringed in blue -->
  <g transform="{HEAD}">
    <path fill="#2B2532" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round"
          d="M 76,-30 Q 150,-118 250,-40 Q 160,-50 76,-30 Z"/>
    {letters("UTAU", 136, -72, 15, "#FFFFFF")}
    <circle cx="102" cy="22" r="13" fill="#F2F2F4" stroke="#57A9E2" stroke-width="3"/>
    <circle cx="102" cy="22" r="5" fill="#57A9E2"/>
  </g>
''',
)

def rei_head(lamp):
    """the black router on her head, its two antennas, and on the UTAU and V5 headsets the headlamp"""
    lamp_svg = ('    <circle cx="160" cy="-51" r="5" fill="#FFF4C8" stroke="#2C2A28" stroke-width="2"/>\n' if lamp else "")
    return (f'''  <!-- the black router on her head, its two antennas -->
  <g transform="{HEAD}" stroke-linecap="round">
    <path stroke="#2C2A28" stroke-width="3.5" fill="none" d="M 134,-54 L 126,-86 M 166,-56 L 174,-88"/>
    <circle cx="126" cy="-86" r="3.5" fill="#FFFFFF" stroke="#2C2A28" stroke-width="2"/>
    <circle cx="174" cy="-88" r="3.5" fill="#FFFFFF" stroke="#2C2A28" stroke-width="2"/>
    <rect x="120" y="-60" width="58" height="18" rx="6" fill="#2C2A28" stroke="#FFFFFF" stroke-width="3"/>
    <rect x="128" y="-53" width="10" height="3" rx="1.5" fill="#ED7029"/>
''' + lamp_svg + "  </g>\n")


def trim_wave():
    """the sound wave along the front wing's trim, as her jacket has it on its orange stripes: a zigzag on the curve"""
    pts = []
    for k in range(41):
        t = 0.08 + 0.84 * k / 40
        x = (1 - t) ** 3 * 279 + 3 * (1 - t) ** 2 * t * 246 + 3 * (1 - t) * t ** 2 * 226 + t ** 3 * 224
        y = (1 - t) ** 3 * 40 + 3 * (1 - t) ** 2 * t * 92 + 3 * (1 - t) * t ** 2 * 170 + t ** 3 * 300
        dx = -3 * (1 - t) ** 2 * 279 + 3 * (1 - 4 * t + 3 * t * t) * 246 + 3 * (2 * t - 3 * t * t) * 226 + 3 * t * t * 224
        dy = -3 * (1 - t) ** 2 * 40 + 3 * (1 - 4 * t + 3 * t * t) * 92 + 3 * (2 * t - 3 * t * t) * 170 + 3 * t * t * 300
        n = math.hypot(dx, dy)
        off = (2.6 if k % 2 else -2.6) * (0 if k in (0, 40) else 1)
        pts.append(f"{x - dy / n * off:.1f},{y + dx / n * off:.1f}")
    return ("  <!-- the sound wave on her jacket's orange stripes, along the trim -->\n"
            f'  <polyline points="{" ".join(pts)}" fill="none" stroke="#FFFFFF" stroke-width="1.6" '
            'stroke-linejoin="round" stroke-linecap="round"/>\n')


def trim_point(t):
    """the front wing's trim at t: the point and its unit normal"""
    x = (1 - t) ** 3 * 279 + 3 * (1 - t) ** 2 * t * 246 + 3 * (1 - t) * t ** 2 * 226 + t ** 3 * 224
    y = (1 - t) ** 3 * 40 + 3 * (1 - t) ** 2 * t * 92 + 3 * (1 - t) * t ** 2 * 170 + t ** 3 * 300
    dx = -3 * (1 - t) ** 2 * 279 + 3 * (1 - 4 * t + 3 * t * t) * 246 + 3 * (2 * t - 3 * t * t) * 226 + 3 * t * t * 224
    dy = -3 * (1 - t) ** 2 * 40 + 3 * (1 - 4 * t + 3 * t * t) * 92 + 3 * (2 * t - 3 * t * t) * 170 + 3 * t * t * 300
    n = math.hypot(dx, dy)
    return x, y, -dy / n, dx / n


def trim_keys():
    """the black keys on the white trim, two then three as on a keyboard, from one side of the trim to past its
    middle"""
    keys, k = [], 0
    for octave in range(5):
        for j, step in enumerate((0, 1, 3, 4, 5)):
            t = 0.1 + 0.16 * octave + 0.024 * step
            if t > 0.9:
                break
            x, y, nx, ny = trim_point(t)
            keys.append(f"M {x - nx * 4.5:.1f},{y - ny * 4.5:.1f} L {x + nx * 0.5:.1f},{y + ny * 0.5:.1f}")
            k += 1
    return ("  <!-- the piano keys on her jacket, black on the white trim -->\n"
            f'  <path d="{" ".join(keys)}" stroke="#1E2122" stroke-width="2.6" stroke-linecap="butt" fill="none"/>\n')


FRONT_WING_D = ("M 283.32464,18.471579 A 330.76661,330.76661 0 0 0 211.63417,156.44085 330.76661,330.76661 0 0 0 "
                "217.7827,336.65055 244.08293,244.08293 0 0 0 309.08124,199.29137 244.08293,244.08293 0 0 0 "
                "283.32464,18.471579 Z")
REI_BASE = dict(
    who="Rei", who_full="Adachi Rei", hair_word="side tail and antennas", hair_colour="orange",
    hair=("#F59A3A", "#E0701F"), tail=("#F18F2A", "#DA771B"), tail_dark=("#DA771B", "#A05330"),
    far=("#DA771B", "#A05330"), far_dark=("#B8611E", "#7E4020"),
    rim="#3A1E0E", shine="#FFD7A8", ring="#3A1E0E",
    near_use='  <use xlink:href="#drill" transform="translate(322,318) rotate(-8) scale(0.9,0.47)"/>',
    near_note="  <!-- the side tail, in front -->\n",
)

REI_UTAU = character(**{**REI_BASE, **dict(
    name="Adachi Rei UTAU", trim_word="orange", eyes_word="Rei's UTAU eyes: orange camera lenses, wide open, silly",
    source="colours from missile39's first illustration (2017)",
    palette_note="Rei UTAU: orange hair, orange lens eyes, a white jacket with orange stripes, a black turtleneck "
                 "with 00 on it",
    outfit=("#F4F4F4", "#D3D3D7"), back_wing="#232325", trim="#F18F2A",
    iris=("#F7B060", "#E0761F", "#8A3C10"), eyes="lens",
    tie="#F4F4F4", band="#D0D0D4", tie_h=14,
    tails_note="her short side tail: one leaf, tied in a white ribbon",
    mark="00", mark_colour="#F4F4F4", head_extras=rei_head(True),
)})

REI_V5 = character(**{**REI_BASE, **dict(
    name="Adachi Rei V5", trim_word="orange", eyes_word="Rei's V5 eyes: orange lenses under a calm lid",
    source="colours from missile39's VOCALOID5 illustration",
    palette_note="Rei V5: orange hair, orange lens eyes, a white jacket whose orange stripes carry a sound wave, a "
                 "black turtleneck",
    outfit=("#F6F6F6", "#D6D6DA"), back_wing="#232325", trim="#F18F2A", trim_width=7,
    iris=("#F7B060", "#E0761F", "#8A3C10"), eyes="lens-soft",
    tie="#F4F4F4", band="#D0D0D4", tie_h=14,
    tails_note="her short side tail: one leaf, tied in a white ribbon",
    wing_extras=trim_wave(), head_extras=rei_head(True),
)})

REI_V6 = character(**{**REI_BASE, **dict(
    name="Adachi Rei V6", trim_word="white", eyes_word="Rei's V6 eyes: lenses navy at the middle and orange at "
                                                       "the edge, under a level lid",
    source="colours from Kitsune's VOCALOID6 illustration and missile39's design sheet",
    palette_note="Rei V6: orange hair, navy and orange lens eyes, a black jacket with white stripes and piano keys, "
                 "a white hood",
    outfit=("#34383A", "#1E2122"), back_wing="#E2E2E4", trim="#F4F4F4",
    iris=("#26305A", "#6A5A78", "#E58A3E"), ring="#141A33", eyes="lens-cool",
    tie="#2C2A28", band="#EDEDED", tie_h=16,
    tails_note="her short side tail: one leaf, tied in her black and white device",
    # the jacket's piano keys on the trim, along its curve
    trim_width=9, wing_extras=trim_keys(), head_extras=rei_head(False),
)})

GUMI = character(
    name="GUMI", who="GUMI", who_full="GUMI", hair_word="short hair and goggles",
    hair_colour="green", trim_word="orange", eyes_word="GUMI's green",
    source="colours from the Megpoid V4 box",
    palette_note="GUMI: green hair and its shade, green eyes, a white top, an orange vest with red-orange trim",
    hair=("#86D46E", "#4DAE5C"), tail=("#7ACB6A", "#3E9E58"), tail_dark=("#4DAE5C", "#2E7F44"),
    far=("#4DAE5C", "#2E7F44"), far_dark=("#3E9450", "#256A38"),
    outfit=("#F8F7F1", "#DCD9CC"), back_wing="#EE8A2A", trim="#E2562E",
    iris=("#A8E07A", "#4E9A2E", "#26561A"), rim="#1E3A18", shine="#D6F5B8",
    # a long lock beside her face, untied
    tails_note="her long lock beside the face: one leaf, untied",
    near_use='  <use xlink:href="#drill" transform="translate(326,322) rotate(-12) scale(0.7,0.45)"/>',
    near_note="  <!-- the lock beside her face, in front -->\n",
    # her red goggles up on her head, on their strap
    head_extras=f'''  <!-- her red goggles up on her head, on their strap -->
  <g transform="{HEAD}">
    <path stroke="#3A2A26" stroke-width="7" stroke-linecap="round" fill="none" d="M 96,-34 Q 156,-56 220,-44"/>
    <rect x="118" y="-66" width="82" height="34" rx="16" fill="#3A2A26" stroke="#FFFFFF" stroke-width="3"/>
    <circle cx="139" cy="-49" r="13" fill="#E03A2E"/>
    <circle cx="179" cy="-49" r="13" fill="#E03A2E"/>
    <path fill="#FFFFFF" fill-opacity="0.75" d="M 131,-55 Q 136,-60 142,-58 Q 136,-56 133,-51 Z M 171,-55 Q 176,-60 182,-58 Q 176,-56 173,-51 Z"/>
  </g>
''',
)

BACK_WING_D = ("M 192.28931,12.793038 A 330.76661,330.76661 0 0 0 161.77932,165.25345 330.76661,330.76661 0 0 0 "
               "217.7827,336.65055 244.08293,244.08293 0 0 0 267.29749,179.3252 244.08293,244.08293 0 0 0 "
               "192.28931,12.793038 Z")
UPPER_LEAF_D = ("M 3.1326032,310.41929 A 220.1792,220.1792 0 0 0 98.555722,350.50134 220.1792,220.1792 0 0 0 "
                "217.7827,336.65055 162.47705,162.47705 0 0 0 121.7011,283.52647 162.47705,162.47705 0 0 0 "
                "3.1326032,310.41929 Z")
LOWER_LEAF_D = ("M 80.650839,503.85583 A 220.1792,220.1792 0 0 0 165.61247,444.74858 220.1792,220.1792 0 0 0 "
                "217.7827,336.65055 162.47705,162.47705 0 0 0 121.45529,389.32762 162.47705,162.47705 0 0 0 "
                "80.650839,503.85583 Z")


def gradient(gid, stops, vertical=True):
    """a linear gradient of any number of stops, top to bottom (or left to right)"""
    x2, y2 = ("0", "1") if vertical else ("1", "0")
    n = len(stops) - 1
    body = "".join(f'<stop offset="{i / n:g}" stop-color="{c}"/>' for i, c in enumerate(stops))
    return f'    <linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">{body}</linearGradient>\n'


def trace(d, colour, dots):
    """a circuit's trace: a line of right angles, a white dot at each of its ends (dots)"""
    ends = "".join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#FFFFFF"/>' for x, y in dots)
    return (f'    <path d="{d}" fill="none" stroke="{colour}" stroke-width="2" stroke-linejoin="round" '
            f'stroke-linecap="round"/>{ends}\n')


def vein(d, colour, opacity, width=1.6):
    """a light line along a leaf, following its curve"""
    return (f'    <path d="{d}" fill="none" stroke="{colour}" stroke-width="{width}" stroke-linecap="round" '
            f'stroke-opacity="{opacity}"/>\n')


FUDDLES = character(
    name="Fuddles", who="Fuddles", who_full="Fuddles", hair_word="short tails and glowing circuits",
    hair_colour="cyan", trim_word="cyan", eyes_word="Fuddles' cyan and blue, one of each, and a smile",
    source="colours from Fuddles' own Wimsy",
    palette_note="Fuddles: navy to blue to violet wings with circuit traces, a pale blue face under a blue to pink "
                 "band of hair, one cyan eye and one blue",
    hair=("#3473DA", "#CF51AE"), tail=("#71B4F8", "#B452DF"), tail_dark=("#5E74F6", "#8168F6"),
    far=("#67E8F9", "#28BEF0"), far_dark=("#28BEF0", "#1C8FC0"),
    outfit=("#132A52", "#7968F7"), back_wing="url(#fuddles-back)", trim="#25CDEF", trim_width=3,
    iris=("#A5F5FF", "#37D7F0", "#0B7A93"), iris2=("#A9C8FF", "#4085F6", "#1E3FA8"), rim="#090E1B",
    shine="#C9B8FF", mouth="#050916", skin=("#DDF3FC", "#F2FAFF"),
    # the hair only as a band along the top of the head, blue at the back to pink at the tip
    hair_path="M -40,-200 L 360,-200 L 360,-2 L 320,1 L 300,-2 L 260,-17 L 220,-27 L 180,-32 L 140,-31 "
              "L 100,-26 L 60,-15 L 20,0 L -40,4 Z",
    hair_fill="url(#fuddles-band)", front_fill="url(#fuddles-front)", tail_vein="#FFFFFF",
    lower_fills=("url(#fuddles-leaf-cyan)", "url(#fuddles-leaf-violet)"),
    defs_extra=(gradient("fuddles-back", ("#0A122B", "#152B5C", "#1E5FA0"))
                + gradient("fuddles-front", ("#132A52", "#3575DE", "#7968F7"))
                + gradient("fuddles-band", ("#3473DA", "#9160F6", "#CF51AE"), vertical=False)
                + gradient("fuddles-leaf-cyan", ("#28BEF0", "#67E8F9"), vertical=False)
                + gradient("fuddles-leaf-violet", ("#9160F6", "#5E74F6", "#3F7FF4"))),
    # two short loose tails, one of each side: the far one cyan, the near one blue to violet
    tails_note="two short loose tails, one of each side, where Teto's drills are: the far one cyan, the near one blue "
               "to violet",
    far_use='  <use xlink:href="#drill-far" transform="translate(250,300) rotate(8) scale(0.76,0.52)"/>',
    near_use='  <use xlink:href="#drill" transform="translate(322,320) rotate(-10) scale(0.72,0.44)"/>',
    far_note="  <!-- the far tail, behind the head, cyan -->\n",
    near_note="  <!-- the near tail, in front, blue to violet -->\n",
    # the circuits: a trace in each leaf, dots on the front wing, three violet lines of code
    # the back wing's vein and trace, running on behind the front wing, which covers them
    back_extras=(f'  <!-- the vein and the circuit trace of the back wing, under the front wing -->\n'
                 f'  <clipPath id="fuddles-back-clip"><path d="{BACK_WING_D}"/></clipPath>\n'
                 '  <g clip-path="url(#fuddles-back-clip)">\n'
                 + vein("M 188,46 C 170,120 172,214 208,304", "#6A9BE6", 0.7)
                 + trace("M 180,152 L 202,152 L 210,170 L 210,218", "#22D3EE", ((180, 152), (210, 218)))
                 + '  </g>\n'),
    wing_extras=(f'  <!-- the circuits: a trace in each leaf, its dots, the lines of code on the front wing -->\n'
                 f'  <clipPath id="fuddles-front-clip"><path d="{FRONT_WING_D}"/></clipPath>\n'
                 f'  <clipPath id="fuddles-upper-clip"><path d="{UPPER_LEAF_D}"/></clipPath>\n'
                 f'  <clipPath id="fuddles-lower-clip"><path d="{LOWER_LEAF_D}"/></clipPath>\n'
                 '  <g clip-path="url(#fuddles-front-clip)">\n'
                 + trace("M 260,92 L 248,102 L 246,128 L 238,158", "#C084FC", ((260, 92), (238, 158)))
                 + trace("M 297,172 L 286,182 L 286,204", "#22D3EE", ((297, 172),))
                 + '    <circle cx="270" cy="118" r="4.5" fill="#22D3EE"/><circle cx="264" cy="147" r="3.5" '
                   'fill="#3B82F6"/><circle cx="261" cy="173" r="2.5" fill="#A855F7"/>\n'
                   '    <path d="M 250,215 L 284,215 M 246,224 L 276,224 M 244,233 L 268,233" stroke="#C084FC" '
                   'stroke-width="2" stroke-linecap="round"/>\n'
                 + '  </g>\n'),
    # the little pink tuft near the tip of the band
    # the traces of the leaves below, drawn after them, and the little pink tuft near the tip of the band
    head_extras=('  <!-- the traces of the leaves below -->\n'
                 '  <g clip-path="url(#fuddles-upper-clip)">\n'
                 + trace("M 92,316 L 125,316 L 136,325 L 168,325", "#22D3EE", ((92, 316),))
                 + vein("M 34,306 Q 120,290 204,332", "#E0FAFF", 0.75)
                 + '  </g>\n  <g clip-path="url(#fuddles-lower-clip)">\n'
                 + trace("M 165,388 L 150,400 L 146,418 L 133,430", "#22D3EE", ((165, 388),))
                 + trace("M 186,372 L 176,392 L 182,404", "#C084FC", ((186, 372),))
                 + vein("M 98,486 Q 118,404 206,346", "#C7D2FE", 0.65)
                 + '  </g>\n'
                 # the cyan sheen along the head's lower edge, as the face catches the glow
                 + f'  <g clip-path="url(#head-clip)"><path transform="{HEAD}" d="M 14,34 Q 110,66 214,50" fill="none" '
                   'stroke="#67E8F9" stroke-width="6" stroke-linecap="round" stroke-opacity="0.45"/></g>\n'
                 + f'''  <!-- the pink tuft at the end of the band of hair -->
  <path transform="{HEAD}" fill="#F43F5E" d="M 268,-12 L 292,-6 L 281,6 Z"/>
'''),
)

# ---- Yi Xi: Dreamtonics' voice has no face of its own. The first voice as rice drew her in BUTCHER VANITY (FLAVOR
# FOLEY: Vane Lily, Jamie Paige, ricedeity); Yi Xi 2 as VIMALION PROJECT designed her (vimalion.pro/yixi), free to use
YIXI_BLACK = dict(
    hair=("#3A3F40", "#070808"), tail=("#33383A", "#050606"), tail_dark=("#1F2323", "#020302"),
    far=("#262A2B", "#040505"), far_dark=("#151818", "#020302"),
    iris=("#2E2730", "#120E12", "#040304"), rim="#0B0A0B", shine="#5C666C", pupil="#CC164B",
    eyes="sly", lid="#FDD9C5", mole=(262, 4),
)


def yixi_cap(colour, under, forward):
    """her cap over the head: a crown made of a leaf on the head's top, two seams along its curve, a button; the
    visor a leaf to the front (forward) or turned to the back"""
    visor = ("M 222,-42 Q 296,-60 328,-14 Q 286,-22 222,-42 Z" if forward
             else "M 126,-40 Q 92,-66 56,-60 Q 88,-46 126,-40 Z")
    return (f'''  <!-- her cap, the visor {"to the front, over the eyes" if forward else "turned to the back"} -->
  <g transform="{HEAD}" stroke-linejoin="round" stroke-linecap="round">
    <path fill="{under}" stroke="#FFFFFF" stroke-width="4" d="{visor}"/>
    <path fill="url(#yixi-cap)" stroke="#FFFFFF" stroke-width="4" d="M 98,-34 Q 170,-126 256,-38 Q 176,-52 98,-34 Z"/>
    <path fill="none" stroke="{under}" stroke-width="2.2" d="M 174,-82 Q 152,-62 140,-42 M 178,-82 Q 202,-64 214,-44"/>
    <circle cx="176" cy="-83" r="4.5" fill="{colour}" stroke="#FFFFFF" stroke-width="2.2"/>
  </g>
''')


YIXI_SV = character(**{**YIXI_BLACK, **dict(
    name="Yi Xi SV", who="Yi Xi", who_full="Yi Xi", hair_word="long black hair and red cap",
    hair_colour="black", trim_word="black", eyes_word="Yi Xi's ^q^: shut in a smile, each a ^",
    source="colours from the BUTCHER VANITY music video (FLAVOR FOLEY, drawn by ricedeity)",
    palette_note="Yi Xi in BUTCHER VANITY: long black hair, a red cap worn backwards, a red vest open on a black top "
                 "with a red zip, white sleeves, a white face in the cap's salmon shade",
    outfit=("#FD3737", "#B8403F"), back_wing="url(#yixi-sleeves)", trim="#050404", trim_width=9,
    pupil="#FD3737", skin=("#FBB0B0", "#FFFFFF"), lid="#FDEEEE", eyes="caret", rim="#050404",
    defs_extra=(gradient("yixi-cap", ("#FF5A5A", "#FD3737", "#B8403F"))
                + gradient("yixi-sleeves", ("#F6F6F6", "#DCDCDC", "#BDBDBD"))),
    tails_note="her long hair, loose: the head's back and the two leaves below, no tail",
    # the zip down the black top, along the trim, and its pull
    wing_extras=("  <!-- the zip down her black top, along the trim, and its pull -->\n"
                 '  <path fill="none" stroke="#FD3737" stroke-width="2" stroke-linecap="round" d="M 279,40 C 246,92 226,170 224,300"/>\n'
                 '  <rect x="219" y="262" width="10" height="18" rx="3" fill="#FD3737" stroke="#FFFFFF" stroke-width="2"/>\n'),
    front_extras=yixi_cap("#FD3737", "#B8403F", forward=False),
)})

YIXI_SV2 = character(**{**YIXI_BLACK, **dict(
    name="Yi Xi SV2", who="Yi Xi", who_full="Yi Xi 2", hair_word="black ponytail, cap and mask",
    hair_colour="black", trim_word="crimson", eyes_word="Yi Xi 2's: dark, a small red light at the middle, half shut "
                                                       "in the cap's shade, tired lines under them",
    source="colours from VIMALION PROJECT's design of Yi Xi 2 (vimalion.pro/yixi), free to use",
    palette_note="Yi Xi 2: a long black ponytail, a dark grey cap, a black mask, a black dress with a crimson strap "
                 "and tag, dark grey long gloves, a face in the cap's lilac shade",
    outfit=("#3A383B", "#1E1D20"), back_wing="url(#yixi-gloves)", trim="#CC164B", trim_width=6,
    skin=("#BFA8C2", "#FDD9C5"), lid="#C9B3C9",
    defs_extra=(gradient("yixi-cap", ("#5A5D5A", "#424442", "#2C2E2C"))
                + gradient("yixi-gloves", ("#555855", "#424442", "#2E302E"))
                + '    <pattern id="yixi-dots" width="5" height="5" patternUnits="userSpaceOnUse">'
                  '<circle cx="2.5" cy="2.5" r="1.1" fill="#2E302E"/></pattern>\n'),
    tie="#424442", band="#CC164B", tie_h=14,
    tails_note="her long ponytail: one leaf, tied in dark grey with a crimson band",
    near_use='  <use xlink:href="#drill" transform="translate(322,318) rotate(-8) scale(0.86,0.5)"/>',
    near_note="  <!-- her ponytail, in front -->\n",
    # the crimson tag on her dress, on the curve near the trim
    wing_extras=("  <!-- the crimson tag on her dress -->\n"
                 '  <rect transform="rotate(-58 262 112)" x="250" y="106" width="24" height="10" rx="2" fill="#CC164B" '
                 'stroke="#FFFFFF" stroke-width="2"/>\n'),
    # the black mask over the lower face, under the eyes, its dots as the drawing has them
    head_extras=(f'''  <!-- her black mask, from under the eyes to the chin -->
  <g clip-path="url(#head-clip)">
    <path transform="{HEAD}" fill="#0A0B0A" d="M 112,40 Q 176,30 230,38 Q 290,40 340,22 L 340,140 L 112,140 Z"/>
    <path transform="{HEAD}" fill="url(#yixi-dots)" d="M 112,40 Q 176,30 230,38 Q 290,40 340,22 L 340,140 L 112,140 Z"/>
  </g>
'''),
    front_extras=yixi_cap("#424442", "#232523", forward=True),
)})


if __name__ == "__main__":
    for p, out in ((MIKU, "wimsy-miku.svg"), (NERU, "wimsy-neru.svg"), (DEFOKO, "wimsy-defoko.svg"),
                   (REI_UTAU, "wimsy-adachi-rei-utau.svg"), (REI_V5, "wimsy-adachi-rei-v5.svg"),
                   (REI_V6, "wimsy-adachi-rei-v6.svg"), (GUMI, "wimsy-gumi.svg"), (FUDDLES, "wimsy-fuddles.svg"),
                   (YIXI_SV, "wimsy-yi-xi-sv.svg"), (YIXI_SV2, "wimsy-yi-xi-sv2.svg")):
        os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
        with open(os.path.join(HERE, "out", out), "w") as f:
            f.write(vocaloid(p))
        print("out/" + out)
