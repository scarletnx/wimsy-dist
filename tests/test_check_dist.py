#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 the wimsy-dist contributors
"""check_dist.py on a small repo made for each case: the clean one passes, and each problem fails with a line that
names the file and what is wrong. Then this repo itself passes.

    python3 -I tests/test_check_dist.py
"""
import pathlib
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECK = ROOT / "tools" / "check_dist.py"
# written in pieces, so this file holds no SPDX line, machine path or title ID of its own
TAG, COPY = "SPDX-" + "License-Identifier", "SPDX-" + "FileCopyrightText"
CC, GPL = "CC-BY-NC-SA-4.0", "GPL-3.0-or-later"
URL = {CC: "https://spdx.org/licenses/CC-BY-NC-SA-4.0.html", GPL: "https://spdx.org/licenses/GPL-3.0-or-later.html"}
HOME_PATH = "/" + "home/someone/drawings"
TITLE_ID = "01" + "00" + "A1B2C3D4E5F6"
REUSE = f"""version = 1

[[annotations]]
path = ["dist/**"]
{COPY} = "the test"
{TAG} = "{CC}"

[[annotations]]
path = ["docs/**", "notes.txt"]
{COPY} = "the test"
{TAG} = "{GPL}"
"""


def svg(header=CC, metadata=CC):
    head = f"<!-- {COPY}: the test -->\n<!-- {TAG}: {header} -->\n" if header else ""
    return ('<?xml version="1.0" encoding="UTF-8"?>\n' + head
            + '<svg xmlns="http://www.w3.org/2000/svg" width="8" height="8">\n  <metadata>\n'
            + '    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" '
            + 'xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
            + f'      <dc:license rdf:resource="{URL[metadata]}"/>\n    </rdf:RDF>\n  </metadata>\n</svg>\n')


def png(*texts):
    def chunk(kind, body):
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 0, 0, 0, 0))
            + b"".join(chunk(b"tEXt", t.encode("latin-1")) for t in texts)
            + chunk(b"IDAT", zlib.compress(b"\0\0")) + chunk(b"IEND", b""))


class Fixture(unittest.TestCase):
    def setUp(self):
        self.dir = pathlib.Path(tempfile.mkdtemp(prefix="check_dist."))
        self.addCleanup(shutil.rmtree, self.dir)
        subprocess.run(["git", "init", "-q", str(self.dir)], check=True)
        self.write("REUSE.toml", REUSE)
        self.write(f"LICENSES/{CC}.txt", "the licence\n")
        self.write(f"LICENSES/{GPL}.txt", "the licence\n")
        self.write("docs/CREDITS.md", f"<!-- {TAG}: {GPL} -->\n| `wimsy-a` | what inspired it |\n")
        self.write("dist/wimsy-a.svg", svg())
        self.write("dist/wimsy-a.png", png())
        self.write("notes.txt", "a note\n")

    def write(self, rel, data):
        p = self.dir / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, bytes):
            p.write_bytes(data)
        else:
            p.write_text(data)

    def check(self, *options):
        run = subprocess.run([sys.executable, "-I", str(CHECK), "--root", str(self.dir), *options],
                             capture_output=True, text=True)
        return run.returncode, run.stdout + run.stderr

    def fails(self, *said, options=()):
        code, out = self.check(*options)
        self.assertEqual(code, 1, out)
        for s in said:
            self.assertIn(s, out)
        return out

    def test_the_clean_repo_passes(self):
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertIn("4 files licensed", out)
        self.assertIn("no --game-tag scan", out)

    def test_a_file_no_annotation_matches(self):
        self.write("stray.txt", "x\n")
        self.fails("stray.txt: 0 annotations of REUSE.toml match it")

    def test_a_file_two_annotations_match(self):
        self.write("REUSE.toml", REUSE + f'\n[[annotations]]\npath = "dist/wimsy-a.png"\n{COPY} = "x"\n{TAG} = "{GPL}"\n')
        self.fails("dist/wimsy-a.png: 2 annotations of REUSE.toml match it")

    def test_a_licence_without_its_text(self):
        (self.dir / "LICENSES" / f"{CC}.txt").unlink()
        self.fails(f"dist/wimsy-a.svg: REUSE.toml gives {CC}, and LICENSES/{CC}.txt is not there")

    def test_a_header_that_says_another_licence(self):
        self.write("dist/wimsy-a.svg", svg(header=GPL))
        self.fails(f"dist/wimsy-a.svg: its SPDX line says {GPL}; REUSE.toml gives {CC}")

    def test_a_drawing_publish_did_not_stamp(self):
        self.write("dist/wimsy-a.svg", svg(header=None))
        self.fails("dist/wimsy-a.svg: no SPDX line")

    def test_metadata_that_names_another_licence(self):
        self.write("dist/wimsy-a.svg", svg(metadata=GPL))
        self.fails(f"dist/wimsy-a.svg: its metadata's dc:license is ['{URL[GPL]}']; REUSE.toml gives {CC}")

    def test_a_drawing_the_credits_do_not_name(self):
        self.write("dist/wimsy-b.svg", svg())
        self.fails("dist/wimsy-b.svg: docs/CREDITS.md does not name wimsy-b")

    def test_a_longer_name_does_not_credit_a_shorter_one(self):
        self.write("docs/CREDITS.md", f"<!-- {TAG}: {GPL} -->\n| `wimsy-a-two` | what inspired it |\n")
        self.fails("dist/wimsy-a.svg: docs/CREDITS.md does not name wimsy-a")

    def test_a_path_of_a_machine_in_a_text(self):
        self.write("notes.txt", f"made in {HOME_PATH}\n")
        self.fails("notes.txt:1: a path of a machine")

    def test_a_title_id_in_a_text(self):
        self.write("notes.txt", f"the game {TITLE_ID}\n")
        self.fails(f"notes.txt:1: a title ID: {TITLE_ID}")

    def test_a_path_in_a_png_text_chunk(self):
        self.write("dist/wimsy-a.png", png(f"svg:base-uri\0file:{HOME_PATH}/wimsy-a.svg"))
        self.fails("dist/wimsy-a.png: a text chunk holds a path of a machine")

    def test_the_game_tag_scanner_decides(self):
        scanners = pathlib.Path(tempfile.mkdtemp(prefix="check_dist.scan."))
        self.addCleanup(shutil.rmtree, scanners)
        hit, clean = scanners / "hit.py", scanners / "clean.py"
        hit.write_text("import sys\nprint('game-1234abcd in', sys.argv[1])\nsys.exit(1)\n")
        clean.write_text("import sys\nsys.exit(0)\n")
        self.fails("exits 1 on the texts: game-1234abcd in", options=("--game-tag", f"{sys.executable} -I {hit}"))
        code, out = self.check("--game-tag", f"{sys.executable} -I {clean}")
        self.assertEqual(code, 0, out)
        self.assertIn("scanned by", out)

    def test_an_unknown_option_is_refused(self):
        code, out = self.check("--fix")
        self.assertEqual(code, 2, out)
        self.assertIn("'--fix' is not an option here", out)


class ThisRepo(unittest.TestCase):
    def test_this_repo_passes(self):
        run = subprocess.run([sys.executable, "-I", str(CHECK)], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)


if __name__ == "__main__":
    unittest.main()
