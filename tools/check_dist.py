#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 the wimsy-dist contributors
"""check_dist.py: what this repo publishes, checked before it goes out. Fails (exit 1, one line per problem) when

- a file has no licence in REUSE.toml, or two, or a licence LICENSES/ has no text for;
- a file's own SPDX line says another licence than REUSE.toml, or a drawing in dist/ or emoji/ has no SPDX line;
- an SVG's metadata names another licence (dc:license) than REUSE.toml gives it;
- a drawing (dist/, emoji/, themes/) is not named in docs/CREDITS.md;
- a text, or a PNG's text chunks, holds a path of a machine (a home folder, a temporary folder);
- a text holds a title ID, or the scanner --game-tag names (run on every text file) exits other than 0.

    check_dist.py [--root DIR] [--game-tag "COMMAND ARGS"]

The files are git's: tracked, and new ones git does not ignore.
"""
import pathlib
import re
import shlex
import struct
import subprocess
import sys
import zlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # licences.py beside it, also under python3 -I
sys.dont_write_bytecode = True
import licences  # noqa: E402

DRAWINGS = ("dist/", "emoji/", "themes/")
STAMPED = ("dist/", "emoji/")
SKIP = re.compile(r"(LICENSES/.*|LICENSE|REUSE\.toml)\Z")
# written in pieces, so this file does not match itself
TAG = "SPDX-" + "License-Identifier"
HEADER = re.compile(r"^\s*(?:#|<!--|//|/\*)\s*" + TAG + r":\s*(\S+)", re.M)
MACHINE = re.compile("|".join([r"/" + "home/[A-Za-z_]", r"/" + "Users/[A-Za-z_]", r"[A-Za-z]:\\" + "Users",
                               r"(?<![\w.])/" + "tmp/", "Build" + "Dir", "Work" + "Dir", "file" + "://", r"(?<![\w/])~" + "/"]))
TITLE_ID = re.compile(r"(?<![0-9A-Fa-f])01[0-9A-Fa-f]{14}(?![0-9A-Fa-f])")


def files(root):
    out = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                         capture_output=True, check=True).stdout.decode()
    return sorted({f for f in out.split("\0") if f and (root / f).is_file()})


def text_of(path):
    data = path.read_bytes()
    if b"\0" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def png_texts(data):
    """the text chunks of a PNG (tEXt, zTXt, iTXt), as text"""
    out, i = [], 8
    while i + 8 <= len(data):
        n, kind = struct.unpack(">I", data[i:i + 4])[0], data[i + 4:i + 8]
        body = data[i + 8:i + 8 + n]
        if kind == b"tEXt":
            out.append(body.replace(b"\0", b"=").decode("latin-1"))
        elif kind == b"zTXt":
            key, _, rest = body.partition(b"\0")
            out.append(key.decode("latin-1") + "=" + zlib.decompress(rest[1:]).decode("latin-1"))
        elif kind == b"iTXt":
            out.append(body.decode("utf-8", "replace"))
        i += 12 + n
    return out


def check(root, game_tag=None):
    root = pathlib.Path(root).resolve()
    errors = []
    notes = licences.annotations(root)
    credits_path = root / "docs" / "CREDITS.md"
    credits = credits_path.read_text() if credits_path.is_file() else ""
    if not credits:
        errors.append("docs/CREDITS.md: missing or empty")
    texts, checked = [], 0
    for rel in files(root):
        if SKIP.match(rel):
            continue
        checked += 1
        path = root / rel
        try:
            lic, _ = licences.lookup(rel, notes)
        except licences.LicenceError as e:
            errors.append(str(e))
            lic = None
        if lic and not (root / "LICENSES" / f"{lic}.txt").is_file():
            errors.append(f"{rel}: REUSE.toml gives {lic}, and LICENSES/{lic}.txt is not there")
        text = text_of(path)
        drawing = rel.startswith(DRAWINGS) and rel.endswith((".svg", ".png"))
        if drawing and not re.search(r"(?<![\w-])" + re.escape(pathlib.PurePath(rel).stem) + r"(?![\w-])", credits):
            errors.append(f"{rel}: docs/CREDITS.md does not name {pathlib.PurePath(rel).stem}")
        if text is None:
            if rel.endswith(".png"):
                for chunk in png_texts(path.read_bytes()):
                    if MACHINE.search(chunk):
                        errors.append(f"{rel}: a text chunk holds a path of a machine: {chunk[:120]}")
            continue
        texts.append(rel)
        own = HEADER.findall("\n".join(text.split("\n")[:30]))
        if lic and any(o != lic for o in own):
            errors.append(f"{rel}: its SPDX line says {', '.join(own)}; REUSE.toml gives {lic}")
        if rel.endswith(".svg") and rel.startswith(STAMPED) and not own:
            errors.append(f"{rel}: no SPDX line; publish.sh stamps it (licences.py stamp)")
        if lic and rel.endswith(".svg") and rel.startswith(DRAWINGS):
            named = re.findall(r'<dc:license rdf:resource="([^"]*)"', text)
            if named != [licences.URL.get(lic)]:
                errors.append(f"{rel}: its metadata's dc:license is {named or 'missing'}; REUSE.toml gives {lic} "
                              f"({licences.URL.get(lic)})")
        for n, line in enumerate(text.split("\n"), 1):
            m = MACHINE.search(line)
            if m:
                errors.append(f"{rel}:{n}: a path of a machine: {m.group(0)!r} in {line.strip()[:100]!r}")
            m = TITLE_ID.search(line)
            if m:
                errors.append(f"{rel}:{n}: a title ID: {m.group(0)}")
    if game_tag:
        cmd = shlex.split(game_tag) + [str(root / t) for t in texts]
        try:
            run = subprocess.run(cmd, capture_output=True, text=True)
        except OSError as e:
            errors.append(f"--game-tag {game_tag!r}: cannot run it: {e}")
        else:
            if run.returncode != 0:
                said = (run.stdout + run.stderr).strip().replace("\n", " | ")[:400]
                errors.append(f"--game-tag {game_tag!r} exits {run.returncode} on the texts: {said}")
    return errors, checked


def main(argv):
    root, game_tag, args = HERE.parent, None, argv[1:]
    while args:
        a = args.pop(0)
        if a == "--root" and args:
            root = pathlib.Path(args.pop(0))
        elif a == "--game-tag" and args:
            game_tag = args.pop(0)
        else:
            print(f"check_dist.py: {a!r} is not an option here\n\n{__doc__.strip()}", file=sys.stderr)
            return 2
    try:
        errors, n = check(root, game_tag)
    except licences.LicenceError as e:
        errors, n = [str(e)], 0
    for e in errors:
        print(f"check_dist.py: {e}", file=sys.stderr)
    if errors:
        print(f"check_dist.py: {len(errors)} problem(s) in {root}", file=sys.stderr)
        return 1
    scanned = f", scanned by {game_tag!r}" if game_tag else ", no --game-tag scan"
    print(f"check_dist.py: {n} files licensed, the drawings credited, no machine path or title ID{scanned}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
