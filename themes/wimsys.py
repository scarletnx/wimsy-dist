#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Each theme's Wimsy: a drawing of this repository as it is ([<theme>.wimsy] drawing), or Liz's five leaves
(ScarletNX's dist/wimsy.svg) in the colours palettes.toml gives a theme under [<theme>.wimsy]. A theme with a grid gets them as pixels on that grid (Default's: 32 by 32, an early PC's
colours, each leaf apart from the next by a cell of the outline's colour). Wimsy's own and Fuddles' are ScarletNX's
files and are not made here.

    wimsys.py WIMSY_SVG          writes wimsy-<theme>.svg beside this script, for each theme that has a [.wimsy]
    wimsys.py WIMSY_SVG --check  writes nothing: fails when one of them is not what it would write

Needs rsvg-convert and Pillow for a grid.
"""
import io
import math
import pathlib
import re
import subprocess
import sys
import tomllib

HERE = pathlib.Path(__file__).resolve().parent
# the leaves of Liz's drawing, by the id it gives each, and what the colours call them
LEAVES = {"path1-4": "back", "path1-8-8": "front", "path1-8-8-6": "lower", "path1-8-8-6-0": "lower", "path1-8-4-0": "head"}
# the eyes on the page (the drawing's circles turned by its rotate(24.165289)), and their radius
TURN = math.radians(24.165289)
EYES = [(434.99091, 99.701668), (485.51288, 44.356552)]
EYE_R, SHINE_R, SHINE_UP = 23.114985, 16.677759, 6.437225
CREDIT = """  <metadata>
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:cc="http://creativecommons.org/ns#"
             xmlns:dc="http://purl.org/dc/elements/1.1/">
      <cc:Work rdf:about="">
        <dc:title>Wimsy in the {name} theme's colours</dc:title>
        <dc:creator><cc:Agent><dc:title>Liz (Wimsy)</dc:title></cc:Agent></dc:creator>
        <dc:contributor><cc:Agent><dc:title>AO55 ({how})</dc:title></cc:Agent></dc:contributor>
        <dc:license rdf:resource="https://spdx.org/licenses/GPL-3.0-or-later.html"/>
        <dc:source>https://github.com/scarletnx/ScarletNX</dc:source>
      </cc:Work>
    </rdf:RDF>
  </metadata>
"""


def leaves(svg):
    """(id, d, the outline's width) of each leaf, in the drawing's order"""
    out = []
    for m in re.finditer(r"<path\s+([^>]*?)/>", svg, re.S):
        attrs = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', m.group(1)))
        if attrs.get("id") in LEAVES:
            width = float(re.search(r"stroke-width:([0-9.]+)", attrs["style"]).group(1))
            out.append((attrs["id"], attrs["d"], width))
    if [i for i, _, _ in out] != list(LEAVES):
        sys.exit(f"the drawing's leaves are {[i for i, _, _ in out]}, not {list(LEAVES)}: Liz's Wimsy changed")
    return out


def eye(cx, cy):
    """a circle of the drawing's turned frame, on the page"""
    return cx * math.cos(TURN) - cy * math.sin(TURN), cx * math.sin(TURN) + cy * math.cos(TURN)


def vector(svg, name, c, outline=None, width=None, eyes=True):
    body = "".join(f'  <path fill="{c[LEAVES[i]]}" stroke="{outline or c["outline"]}" stroke-width="{width or w}" d="{d}"/>\n'
                   for i, d, w in leaves(svg))
    if eyes:
        for cx, cy in EYES:
            x, y = eye(cx, cy)
            sx, sy = eye(cx, cy - SHINE_UP)
            body += f'  <circle fill="{c["eye"]}" cx="{x:.2f}" cy="{y:.2f}" r="{EYE_R}"/>\n'
            body += f'  <circle fill="{c["shine"]}" cx="{sx:.2f}" cy="{sy:.2f}" r="{SHINE_R}"/>\n'
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" '
            'viewBox="0 0 512 512">\n' + CREDIT.format(name=name, how="its colours") + body + "</svg>\n")


def pixels(svg, name, c):
    """the leaves as cells of the grid: each cell takes the colour most of it has, the eyes set by hand"""
    from PIL import Image
    n = int(c["grid"])
    cell = 512 // n
    flat = vector(svg, name, c, outline=c["outline"], width=cell, eyes=False)
    png = subprocess.run(["rsvg-convert", "-w", "512", "-h", "512"], input=flat.encode(), capture_output=True,
                         check=True).stdout
    img = Image.open(io.BytesIO(png)).convert("RGBA")
    named = {c[k]: k for k in ("back", "front", "lower", "head", "outline")}
    want = [tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) for h in named]
    grid = [[None] * n for _ in range(n)]
    for gy in range(n):
        for gx in range(n):
            votes = {}
            for y in range(gy * cell, gy * cell + cell):
                for x in range(gx * cell, gx * cell + cell):
                    r, g, b, a = img.getpixel((x, y))
                    if a < 128:
                        key = None
                    else:
                        key = min(range(len(want)), key=lambda i: sum((p - q) ** 2 for p, q in zip((r, g, b), want[i])))
                    votes[key] = votes.get(key, 0) + 1
            best = max(votes, key=votes.get)
            grid[gy][gx] = None if best is None else list(named)[best]
    for cx, cy in EYES:  # each eye: two cells by two of the eye, its shine in the upper one toward the tip
        x, y = eye(cx, cy)
        ex, ey = round(x / cell), round(y / cell)
        grid[ey - 1][ex - 1:ex + 1] = [c["eye"], c["shine"]]
        grid[ey][ex - 1:ex + 1] = [c["eye"]] * 2
    runs = {}
    for y, row in enumerate(grid):
        x = 0
        while x < n:
            colour = row[x]
            end = x
            while end < n and row[end] == colour:
                end += 1
            if colour:
                runs.setdefault(colour, []).append(f"M{x} {y}h{end - x}v1h-{end - x}z")
            x = end
    body = "".join(f'  <path fill="{k}" d="{"".join(v)}"/>\n' for k, v in sorted(runs.items()))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" '
            f'viewBox="0 0 {n} {n}" shape-rendering="crispEdges">\n'
            + CREDIT.format(name=name, how=f"its colours, on a {n} by {n} grid of an early PC's") + body + "</svg>\n")


def main(argv):
    if len(argv) not in (1, 2) or (len(argv) == 2 and argv[1] != "--check"):
        sys.exit(__doc__)
    svg = pathlib.Path(argv[0]).read_text()
    themes = tomllib.loads((HERE / "palettes.toml").read_text())
    stale = []
    for key, t in themes.items():
        c = t.get("wimsy")
        if not c:
            continue
        if "drawing" in c:  # a drawing of this repository's, as it is
            text = (HERE.parent / c["drawing"]).read_text()
        else:
            text = pixels(svg, t["name"], c) if "grid" in c else vector(svg, t["name"], c)
        path = HERE / f"wimsy-{key}.svg"
        if not path.exists() or path.read_text() != text:
            stale.append(path)
            if len(argv) == 1:
                path.write_text(text)
                print(f"wrote {path}")
    if len(argv) == 2 and stale:
        for p in stale:
            print(f"{p} is not what palettes.toml makes: run wimsys.py without --check", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
