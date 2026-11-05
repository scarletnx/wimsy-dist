#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 the wimsy-dist contributors
"""licences.py: the licence of each file, from REUSE.toml, the one place that says it.

    licences.py stamp SVG...   writes into each SVG what REUSE.toml gives it: the SPDX lines on top and the
                               metadata's dc:license
    licences.py show PATH...   prints the licence and the copyright lines REUSE.toml gives each path

A path is relative to the folder above tools/. A path no annotation matches, or two match, is an error: each file has
one licence, said once.
"""
import pathlib
import re
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
URL = {"GPL-3.0-or-later": "https://spdx.org/licenses/GPL-3.0-or-later.html",
       "CC-BY-NC-SA-4.0": "https://spdx.org/licenses/CC-BY-NC-SA-4.0.html"}
# the tags written in pieces, so the tools that read SPDX lines do not take these for this file's own
LICENCE_TAG, COPYRIGHT_TAG = "SPDX-" + "License-Identifier", "SPDX-" + "FileCopyrightText"
SPDX_COMMENT = re.compile(r"^<!-- SPDX-(?:License-Identifier|FileCopyrightText): [^\n]* -->\n", re.M)
DC_LICENSE = re.compile(r'<dc:license rdf:resource="[^"]*"/>')


class LicenceError(Exception):
    pass


def glob_re(pattern):
    """REUSE.toml's globs: * stops at a /, ** does not, \\* is a star"""
    out, i = [], 0
    while i < len(pattern):
        if pattern.startswith("\\*", i):
            out.append(re.escape("*"))
            i += 2
        elif pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif pattern[i] == "*":
            out.append("[^/]*")
            i += 1
        else:
            out.append(re.escape(pattern[i]))
            i += 1
    return re.compile("".join(out) + r"\Z")


def annotations(root=ROOT):
    """REUSE.toml's [[annotations]], each as (its globs, the licence, the copyright lines)"""
    data = tomllib.loads((pathlib.Path(root) / "REUSE.toml").read_text())
    if data.get("version") != 1:
        raise LicenceError(f"REUSE.toml: version is {data.get('version')!r}; this reads version 1")
    out = []
    for n, a in enumerate(data.get("annotations", []), 1):
        paths = a.get("path")
        lic = a.get("SPDX-License-Identifier")
        cr = a.get("SPDX-FileCopyrightText")
        if not paths or not lic or not cr:
            raise LicenceError(f"REUSE.toml: annotation {n} needs path, SPDX-License-Identifier and "
                               "SPDX-FileCopyrightText")
        paths = [paths] if isinstance(paths, str) else paths
        cr = [cr] if isinstance(cr, str) else cr
        out.append(([glob_re(p) for p in paths], lic, cr))
    return out


def lookup(rel, notes):
    """the (licence, copyright lines) the one annotation matching rel gives it"""
    hits = [(lic, cr) for globs, lic, cr in notes if any(g.match(rel) for g in globs)]
    if len(hits) != 1:
        raise LicenceError(f"{rel}: {len(hits)} annotations of REUSE.toml match it; it needs exactly one")
    return hits[0]


def stamp_text(text, lic, copyrights, name):
    """the SVG with its SPDX lines and its dc:license set to lic"""
    if lic not in URL:
        raise LicenceError(f"{name}: REUSE.toml gives {lic}; licences.py knows {', '.join(URL)}")
    text = SPDX_COMMENT.sub("", text)
    head = "".join(f"<!-- {COPYRIGHT_TAG}: {c} -->\n" for c in copyrights)
    head += f"<!-- {LICENCE_TAG}: {lic} -->\n"
    if text.startswith("<?xml"):
        decl, _, rest = text.partition("\n")
        text = decl + "\n" + head + rest
    else:
        text = head + text
    text, n = DC_LICENSE.subn(f'<dc:license rdf:resource="{URL[lic]}"/>', text)
    if n != 1:
        raise LicenceError(f"{name}: has {n} <dc:license> in its metadata; it needs exactly one")
    return text


def rel_path(path, root=ROOT):
    p = pathlib.Path(path).resolve()
    try:
        return p.relative_to(pathlib.Path(root).resolve()).as_posix()
    except ValueError:
        raise LicenceError(f"{path}: not under {root}") from None


def main(argv):
    if len(argv) < 3 or argv[1] not in ("stamp", "show"):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    notes = annotations()
    try:
        for path in argv[2:]:
            rel = rel_path(path)
            lic, cr = lookup(rel, notes)
            if argv[1] == "show":
                print(f"{rel}: {lic}; " + "; ".join(cr))
                continue
            p = pathlib.Path(path)
            p.write_text(stamp_text(p.read_text(), lic, cr, rel))
    except LicenceError as e:
        print(f"licences.py: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
