#!/usr/bin/env python3
"""make_platforms.py: Wimsy as the systems ScarletNX ships for, the icons beside each download in ReiWimsy's cards:
Linux (Tux), Windows, Android, macOS and iOS. Each takes its system's colours and one detail of its mark, as the
singers take theirs: Tux's white front and orange feet, Windows' four panes on the arm, Android's antennas, the
apple's leaf over the head of macOS's and iOS's. Made with make_vocaloid's pieces; writes out/wimsy-<system>.svg."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # beside it, also under python3 -I
sys.dont_write_bytecode = True  # no __pycache__ left beside the drawings

from make_vocaloid import HEAD, character, gradient, vocaloid  # noqa: E402


def panes(colour):
    """Windows' four panes on the arm, where the singers' marks are, slanted as the wing is"""
    squares = "".join(f'    <rect x="{x}" y="{y}" width="11" height="11" fill="{colour}"/>\n'
                      for x in (0, 13) for y in (0, 13))
    return ("  <!-- Windows' four panes on the arm -->\n"
            '  <g transform="rotate(-8 192 100) translate(184,88)">\n' + squares + "  </g>\n")


def antennas(colour):
    """Android's two antennas, out of the top of the head, white round them as every line here is"""
    d = "M 186,-40 L 172,-84 M 236,-38 L 250,-82"  # from the head's upper edge, above the eyes
    return (f'''  <!-- Android's two antennas, out of the top of the head -->
  <g transform="{HEAD}" stroke-linecap="round" fill="none">
    <path stroke="#FFFFFF" stroke-width="11" d="{d}"/>
    <path stroke="{colour}" stroke-width="6" d="{d}"/>
  </g>
''')


def apple_leaf(fill):
    """the apple's leaf over the head, a leaf as everything here is, where Teto's curl sits"""
    return (f'''  <!-- the apple's leaf over the head -->
  <path transform="{HEAD} translate(150,-34) rotate(-62)" fill="{fill}" stroke="#FFFFFF" stroke-width="4.5"
        stroke-linejoin="round" d="M 0,0 A 52,52 0 0 1 74,0 A 52,52 0 0 1 0,0 Z"/>
''')


COMMON = dict(tails_note="no tail: the head's back and the two leaves below", source="the system's own colours")

LINUX = character(**{**COMMON, **dict(
    name="Linux", who="Tux", who_full="Tux", hair_word="black and white, as Tux",
    hair_colour="black", trim_word="yellow", eyes_word="Tux's: dark, with the round glint",
    palette_note="Linux, as Tux: black hair and sleeves, a white front, yellow trim, orange feet",
    hair=("#3A3A3C", "#111113"), tail=("#2C2C2E", "#0B0B0C"), tail_dark=("#1C1C1E", "#050506"),
    far=("#1C1C1E", "#050506"), far_dark=("#111113", "#000000"),
    outfit=("#FFFFFF", "#E4E4E8"), back_wing="#1C1C1E", trim="#F5B400", trim_width=6,
    iris=("#6E6E73", "#2C2C2E", "#000000"), rim="#000000", shine="#C7C7CC",
    defs_extra=gradient("tux-feet", ("#FFCB2B", "#F59A00", "#E07B00")),
    lower_fills=("url(#tux-feet)", "url(#tux-feet)"),
)})

WINDOWS = character(**{**COMMON, **dict(
    name="Windows", who="Windows", who_full="Windows", hair_word="blue, with the four panes",
    hair_colour="blue", trim_word="light blue", eyes_word="blue",
    palette_note="Windows: blue hair and sleeves, a pale blue front, light blue trim, the four panes on the arm",
    hair=("#2B9AF3", "#0067C0"), tail=("#1E88E5", "#005BB0"), tail_dark=("#0067C0", "#004A8F"),
    far=("#0067C0", "#004A8F"), far_dark=("#005BB0", "#003C76"),
    outfit=("#FFFFFF", "#D6EBFA"), back_wing="#0067C0", trim="#4CC2FF", trim_width=6,
    iris=("#8FD3FF", "#0078D4", "#003C76"), rim="#002A54", shine="#CDEBFF",
    wing_extras=panes("#FFFFFF"),
)})

ANDROID = character(**{**COMMON, **dict(
    name="Android", who="Android", who_full="Android", hair_word="green, with the antennas",
    hair_colour="green", trim_word="white", eyes_word="green",
    palette_note="Android: green hair, front and sleeves, white trim, two antennas",
    hair=("#5BE69A", "#2BB36A"), tail=("#3DDC84", "#20A35C"), tail_dark=("#2BB36A", "#1A8048"),
    far=("#2BB36A", "#1A8048"), far_dark=("#20A35C", "#146638"),
    outfit=("#7FEBAE", "#3DDC84"), back_wing="#1A8048", trim="#FFFFFF", trim_width=6,
    iris=("#A8F5C8", "#2BB36A", "#0F5A31"), rim="#073A1E", shine="#D6FBE5",
    head_extras=antennas("#3DDC84"),
)})

MACOS = character(**{**COMMON, **dict(
    name="macOS", who="macOS", who_full="macOS", hair_word="space grey, with the apple's leaf",
    hair_colour="space grey", trim_word="silver", eyes_word="grey",
    palette_note="macOS: space grey hair and sleeves, a silver front, silver trim, the apple's leaf",
    hair=("#6E6E73", "#2C2C2E"), tail=("#5A5A5F", "#232325"), tail_dark=("#3A3A3C", "#18181A"),
    far=("#3A3A3C", "#18181A"), far_dark=("#2C2C2E", "#101011"),
    outfit=("#F2F2F7", "#C7C7CC"), back_wing="#2C2C2E", trim="#A2AAAD", trim_width=6,
    iris=("#C7C7CC", "#636366", "#1C1C1E"), rim="#111113", shine="#E5E5EA",
    head_extras=apple_leaf("url(#hair)"),
)})

IOS = character(**{**COMMON, **dict(
    name="iOS", who="iOS", who_full="iOS", hair_word="light grey and blue, with the apple's leaf",
    hair_colour="light grey", trim_word="white", eyes_word="blue",
    palette_note="iOS: light grey hair, a blue front, dark sleeves, white trim, the apple's leaf",
    hair=("#E5E5EA", "#AEAEB2"), tail=("#D1D1D6", "#9A9AA0"), tail_dark=("#AEAEB2", "#7C7C82"),
    far=("#AEAEB2", "#7C7C82"), far_dark=("#9A9AA0", "#636366"),
    outfit=("#5AC8FA", "#0A84FF"), back_wing="#1C1C1E", trim="#FFFFFF", trim_width=6,
    iris=("#9FD8FF", "#0A84FF", "#003E8A"), rim="#002A5E", shine="#D8EEFF",
    head_extras=apple_leaf("url(#hair)"),
)})

SYSTEMS = ((LINUX, "wimsy-linux.svg"), (WINDOWS, "wimsy-windows.svg"), (ANDROID, "wimsy-android.svg"),
           (MACOS, "wimsy-macos.svg"), (IOS, "wimsy-ios.svg"))

if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    for p, out in SYSTEMS:
        with open(os.path.join(HERE, "out", out), "w") as f:
            f.write(vocaloid(p))
        print("out/" + out)
