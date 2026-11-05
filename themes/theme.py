#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""SWS's themes: palettes.toml's colours held to GFSS's contrast, and the files they make. The sites (wimsy-core) and
ScarletNX's GUI take these files as they are; a colour changes here and nowhere else.

    theme.py --table                 every role, where it came from, and every pair checked
    theme.py --core WIMSY_CORE       writes wimsy-core's: Tracer's style.css block, Forgejo's themes, Gatus's colour lines
    theme.py --gui SCARLETNX         writes ScarletNX's built-in GUI themes made here (src/gui/themes/<id>/theme.ini)
    theme.py --check --core D --gui D   writes nothing: fails when a file there is not what the palettes make
    theme.py --preview FILE          the preview's classes, between "/* tokens:begin */" and "/* tokens:end */"
    theme.py --wimsy WIMSY_SVG       fails when Wimsy's fills that the Wimsy theme names are no longer hers

Every run fails (exit 1) on a pair that reads under its contrast; a pair is never loosened to pass.
"""
import colorsys
import pathlib
import re
import sys
import tomllib

HERE = pathlib.Path(__file__).resolve().parent
FONTS = {"sans": 'system-ui,-apple-system,"Segoe UI",Roboto,sans-serif',
         "mono": "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"}
MONO = FONTS["mono"]
TRACER, STATUS, FORGE_DEFAULT = "sepia", "sepia", "sepia-auto"
# Gatus draws with shadcn's variables, "H S% L%": each one's role
GATUS = {"background": "bg", "foreground": "ink", "card": "surface", "card-foreground": "ink", "popover": "raised",
         "popover-foreground": "ink", "primary": "accent", "primary-foreground": "on-accent", "secondary": "raised",
         "secondary-foreground": "ink", "muted": "raised", "muted-foreground": "soft", "accent": "raised",
         "accent-foreground": "ink", "destructive": "bad-fill", "destructive-foreground": "on-bad", "border": "faint",
         "input": "rule", "ring": "ink"}
GATUS_OURS = ("bg", "raised", "faint", "ink", "soft", "accent", "on-accent", "ok-fill", "warn-fill", "bad-fill")
MADE = "made by wimsy-dist's themes/theme.py from palettes.toml: change the colours there, then run it again"


def rgb(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


def hexa(c):
    return "#" + "".join(f"{round(max(0.0, min(1.0, v)) * 255):02x}" for v in c)


def luminance(h):
    lin = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb(h)]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def mix(a, b, t):
    return hexa([x + (y - x) * t for x, y in zip(rgb(a), rgb(b))])


def fit(src, against, need, step):
    """src with its HSL lightness moved by step until it reads at need on every colour of against"""
    h, l, s = colorsys.rgb_to_hls(*rgb(src))
    out = src
    while min(contrast(out, a) for a in against) < need:
        l = round(l + step, 4)
        if not 0 <= l <= 1:
            raise SystemExit(f"{src} cannot read at {need}:1 on {', '.join(against)}")
        out = hexa(colorsys.hls_to_rgb(h, l, s))
    return out


class Mode:
    """one theme in one mode: its roles, how each came, and the pairs held to their contrast"""

    def __init__(self, theme, mode, spec):
        self.theme, self.mode, self.r, self.how = theme, mode, {}, {}
        self.spec = spec

        def value(text):
            text = text.strip()
            if re.fullmatch(r"#[0-9a-fA-F]{6}", text):
                return text.lower()
            if text in self.r:
                return self.r[text]
            m = re.fullmatch(r"mix\(([^,]+),([^,]+),([^)]+)\)", text)
            if m:
                return mix(value(m.group(1)), value(m.group(2)), float(m.group(3)))
            raise SystemExit(f"{theme}.{mode}: {text!r} is neither #rrggbb, mix(A, B, T) nor a role given before it")

        def put(name, out, src):
            self.r[name] = out
            self.how[name] = src if out == value(src) else f"{src} -> {out}, its lightness moved to read"

        for name in ("bg", "faint", "ink"):
            put(name, value(spec[name]), spec[name])
        self.r["surface"] = mix(self.r["bg"], self.r["faint"], 0.25)
        self.r["raised"] = mix(self.r["bg"], self.r["faint"], 0.5)
        self.how["surface"], self.how["raised"] = "mix(bg, faint, 25%)", "mix(bg, faint, 50%)"
        pages = [self.r["bg"], self.r["surface"], self.r["raised"]]
        step = -0.001 if luminance(self.r["bg"]) > 0.18 else 0.001  # a light page darkens its colours to read
        for name in ("soft", "accent", "ok", "warn", "bad"):
            put(name, fit(value(spec[name]), pages, 4.5, step), spec[name])
        put("rule", fit(value(spec["rule"]), pages, 3.0, step), spec["rule"])
        put("on-accent", value(spec["on-accent"]), spec["on-accent"])
        for name in ("ok", "warn", "bad"):
            on = value(spec["on-" + name])
            put("on-" + name, on, spec["on-" + name])
            # the fill moves away from its text: darker under a light one, lighter under a dark one
            put(name + "-fill", fit(value(spec[name + "-fill"]), [on], 4.5, -0.001 if luminance(on) > 0.18 else 0.001),
                spec[name + "-fill"])
        self.pairs = [(fg, bg, 4.5) for fg in ("ink", "soft", "accent", "ok", "warn", "bad")
                      for bg in ("bg", "surface", "raised")]
        self.pairs += [("rule", bg, 3.0) for bg in ("bg", "surface", "raised")]
        self.pairs += [("on-accent", "accent", 4.5)] + [("on-" + n, n + "-fill", 4.5) for n in ("ok", "warn", "bad")]
        # the GUI's: a filled box is faint under ink, the focused box the accent under the page
        self.pairs += [("ink", "faint", 4.5), ("bg", "accent", 4.5)]

    def failures(self):
        return [(f, b, need, contrast(self.r[f], self.r[b])) for f, b, need in self.pairs
                if contrast(self.r[f], self.r[b]) < need]

    def decl(self, font):
        return ";".join([f"--font:{FONTS[font]}", f"--mono:{MONO}"] + [f"--{k}:{v}" for k, v in self.r.items()])


def load(path=HERE / "palettes.toml"):
    themes = {}
    for name, t in tomllib.loads(path.read_text()).items():
        modes = {m: Mode(name, m, t[m]) for m in ("light", "dark") if m in t}
        themes[name] = {"name": t["name"], "font": t["font"], "gui": t.get("gui"), "svg": t.get("svg", []),
                        "modes": modes}
    return themes


def roots(t, mode):
    """the roles as a page takes them: one mode, or (auto) light with dark when the system asks"""
    m = t["modes"]
    if mode == "auto" and len(m) == 2:
        return (f":root{{color-scheme:light dark;{m['light'].decl(t['font'])}}}\n"
                f"@media (prefers-color-scheme:dark){{:root{{{m['dark'].decl(t['font'])}}}}}\n")
    one = m.get(mode) or next(iter(m.values()))
    return f":root{{color-scheme:{one.mode};{one.decl(t['font'])}}}\n"


def mark(key, mode=None):
    """the selector's links to the theme and mode in effect, filled: the page says which it shows without a script"""
    links = [f'.sws a[href$="/sws/{key}"]'] + ([f'.sws a[href$="/sws/{mode}"]'] if mode and key != "default" else [])
    return ",".join(links) + "{background:var(--accent);color:var(--on-accent)}\n"


def forge_ids(themes):
    for key, t in themes.items():
        if len(t["modes"]) == 2:
            yield from ((f"{key}-{m}", key, m) for m in ("auto", "light", "dark"))
        else:
            yield key, key, "dark"


def triplet(h):
    """h as Gatus's "H S% L%", with as few decimals as give h back"""
    hh, l, s = colorsys.rgb_to_hls(*rgb(h))
    for n in (1, 2, 3):
        hs, ss, ls = round(hh * 360, n), round(s * 100, n), round(l * 100, n)
        if hexa(colorsys.hls_to_rgb(hs / 360, ls / 100, ss / 100)) == h:
            return f"{hs:.{n}f} {ss:.{n}f}% {ls:.{n}f}%"
    raise SystemExit(f"{h} does not come back from HSL")


def between(text, begin, end, body, path):
    pat = re.compile(re.escape(begin) + r"\n.*?" + re.escape(end), re.S)
    if len(pat.findall(text)) != 1:
        raise SystemExit(f"{path} has no one {begin} ... {end} block")
    return pat.sub(lambda _: begin + "\n" + body + end, text)


def core_files(themes, core):
    """wimsy-core's files, path -> text"""
    out = {}
    style = core / "tracer/site/style.css"
    out[style] = between(style.read_text(), "/* theme:begin */", "/* theme:end */",
                         roots(themes[TRACER], "auto") + mark(TRACER, "auto"), style)
    mapping = (HERE / "forgejo.css").read_text()
    for fid, key, mode in forge_ids(themes):
        base = {"auto": "theme-forgejo-auto.css", "light": "theme-forgejo-light.css", "dark": "theme-forgejo-dark.css"}
        out[core / f"dist/forge/public/assets/css/theme-{fid}.css"] = (
            f'@import "./{base[mode]}";\n/* {themes[key]["name"]} ({mode}): {MADE} */\n'
            + roots(themes[key], mode) + mapping)
    # each theme's roles alone, for the reader's pick: dist/freebsd/build.sh puts each in style.css's block
    for fid, key, mode in forge_ids(themes):
        out[core / f"tracer/site/sws/{fid}.css"] = roots(themes[key], mode) + mark(key, mode)
    for key in themes:
        art = HERE / f"wimsy-{key}.svg"
        if art.exists():
            out[core / f"tracer/site/sws/logo-{key}.svg"] = art.read_text()
    yml = core / "dist/status/gatus.yaml.in"
    text = yml.read_text()
    old = re.findall(r"^    html:root(?:\.dark)?\{--.*\}$", text, re.M)
    if len(old) != 2:
        raise SystemExit(f"{yml} has no two html:root{{...}} colour lines")
    for o, n in zip(old, gatus_lines(themes[STATUS])):
        text = text.replace(o, "    " + n)
    marks = re.findall(r"^    \.sws a\[href.*$", text, re.M)
    if len(marks) != 1:
        raise SystemExit(f"{yml} has no one .sws a[href...] line")
    text = text.replace(marks[0], "    " + mark(STATUS).rstrip("\n"))
    out[yml] = text
    # the page's custom.css in each theme, for the status jail's nginx to give by the reader's pick (render.sh fills
    # in its @NAME@s as it does gatus.yaml's)
    block = re.search(r"^  custom-css: \|\n((?:    .*\n|\n)+)", text, re.M).group(1)
    css = "".join(l[4:] if l.startswith("    ") else l for l in block.splitlines(True)).rstrip("\n") + "\n"
    for key, t in themes.items():
        body = css
        for o, n in zip(re.findall(r"^html:root(?:\.dark)?\{--.*\}$", css, re.M), gatus_lines(t)):
            body = body.replace(o, n)
        body = re.sub(r"^\.sws a\[href.*$", mark(key).rstrip("\n"), body, count=1, flags=re.M)
        out[core / f"dist/status/sws/{key}.css.in"] = body
    return out


def gatus_lines(t):
    """a theme's two lines of Gatus's custom-css: its light under html:root, its dark under html:root.dark"""
    lines = []
    for sel, mode in (("html:root", "light"), ("html:root.dark", "dark")):
        m = t["modes"].get(mode) or next(iter(t["modes"].values()))
        gat = ";".join(f"--{k}:{triplet(m.r[v])}" for k, v in GATUS.items())
        ours = ";".join(f"--{k}:{m.r[k]}" for k in GATUS_OURS)
        lines.append(f"{sel}{{{gat};--radius:0px;{ours}}}")
    return lines


def set_key(text, section, key, value):
    """text with key = value in [section], the line it had replaced"""
    sec = re.search(r"^\[" + re.escape(section) + r"\]\n.*?(?=^\[|\Z)", text, re.M | re.S)
    line = re.compile(r"^" + re.escape(key) + r" = .*$", re.M)
    if not sec or len(line.findall(sec.group(0))) != 1:
        raise SystemExit(f"YoRHa's theme.ini has no one [{section}] {key}: its layout changed, look at gui_ini()")
    body = line.sub(lambda _: f"{key} = {value}", sec.group(0))
    return text[:sec.start()] + body + text[sec.end():]


def gui_ini(t, key, mode, yorha):
    """a GUI theme: YoRHa's file whole (a built-in sets every key itself, src/gui/theme.c reads it over nothing), its
    name and colours the theme's: its menus in one mode, the run in the dark, as YoRHa's"""
    m, d = t["modes"][mode].r, t["modes"]["dark"].r
    # the item chosen takes the accent, or the warning's colour where the accent is the ink
    active = m["warn"] if m["accent"] == m["ink"] else m["accent"]
    text = yorha
    text = set_key(text, "theme", "name", t["name"] + (" dark" if mode == "dark" else ""))
    for k, role in (("page", "bg"), ("ink", "ink"), ("soft", "soft"), ("focus", "accent"), ("failure", "bad"),
                    ("dim", "faint"), ("warning", "warn"), ("added", "ok")):
        text = set_key(text, "colors", k, m[role].upper())
    text = set_key(text, "colors", "active", active.upper())
    for k, role in (("page", "bg"), ("ink", "ink"), ("soft", "soft"), ("dim", "faint"), ("failure", "bad"),
                    ("warning", "warn")):
        text = set_key(text, "run", k, d[role].upper())
    text = set_key(text, "splash", "page", m["bg"].upper())
    return (f"; {t['name']}{' dark' if mode == 'dark' else ''}: YoRHa's layout in the colours of SWS's {t['name']} "
            "theme,\n; made by wimsy-dist's themes/theme.py from palettes.toml: change the colours there, then run it "
            "again.\n" + text)


def ini_colours(text, section):
    sec = re.search(r"^\[" + section + r"\]\n(.*?)(?=^\[|\Z)", text, re.M | re.S)
    return {k: v.lower() for k, v in re.findall(r"^(\w+) = (#[0-9A-Fa-f]{6})$", sec.group(1) if sec else "", re.M)}


def gui_files(themes, gui):
    """ScarletNX's built-ins made here, path -> text; and the two it has of its own, checked against their palettes"""
    out, wrong = {}, []
    root = gui / "src/gui/themes"
    yorha = (root / "yorha/theme.ini").read_text()
    for key, t in themes.items():
        if t["gui"]:
            text = (root / t["gui"] / "theme.ini").read_text()
            have = {"light": ini_colours(text, "colors"), "dark": ini_colours(text, "run")}
            want = {"bg": "page", "ink": "ink", "faint": "dim"}
            for mode, spec in ((m, t["modes"][m].spec) for m in t["modes"]):
                src = have["light"] if t["gui"] == "default" else have[mode]
                for role, k in want.items():
                    if src.get(k) != spec[role]:
                        wrong.append(f"{t['gui']}/theme.ini's {k} is {src.get(k)}, palettes.toml's {key}.{mode} {role} "
                                     f"is {spec[role]}")
            if key == "sepia":
                out[root / "sepia-dark/theme.ini"] = gui_ini(t, key, "dark", yorha)
            continue
        for mode in t["modes"]:
            out[root / (key if mode == "light" else f"{key}-dark") / "theme.ini"] = gui_ini(t, key, mode, yorha)
    return out, wrong


def table(themes):
    bad = False
    for key, t in themes.items():
        for m in t["modes"].values():
            print(f"## {key} {m.mode}")
            for k, v in m.r.items():
                print(f"  --{k:<10} {v}   {m.how[k]}")
            for f, b, need in m.pairs:
                c = contrast(m.r[f], m.r[b])
                bad |= c < need
                print(f"  {'ok  ' if c >= need else 'FAIL'} {f:>10} on {b:<11} {c:5.2f}:1 (needs {need})")
    return bad


def main(argv):
    args = {"--table": False, "--check": False}
    paths = {}
    it = iter(argv)
    for a in it:
        if a in args:
            args[a] = True
        elif a in ("--core", "--gui", "--preview", "--wimsy"):
            paths[a] = pathlib.Path(next(it, "") or sys.exit(f"{a} needs a path"))
        else:
            sys.exit(__doc__)
    if not (args["--table"] or paths):
        sys.exit(__doc__)
    themes = load()
    failed = [(t, m.mode, *f) for t, th in themes.items() for m in th["modes"].values() for f in m.failures()]
    for t, mode, f, b, need, c in failed:
        print(f"{t}.{mode}: {f} on {b} reads at {c:.2f}:1, under {need}:1", file=sys.stderr)
    if args["--table"] and table(themes):
        return 1
    if failed:
        return 1
    if "--wimsy" in paths:
        fills = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}", paths["--wimsy"].read_text())}
        lost = [c for c in themes["wimsy"]["svg"] if c not in fills]
        if lost:
            print(f"{paths['--wimsy']} has none of {', '.join(lost)}: Wimsy changed, choose her theme's colours again",
                  file=sys.stderr)
            return 1
    files, wrong = {}, []
    if "--core" in paths:
        files.update(core_files(themes, paths["--core"]))
    if "--gui" in paths:
        g, wrong = gui_files(themes, paths["--gui"])
        files.update(g)
    for w in wrong:
        print(w, file=sys.stderr)
    if "--preview" in paths:
        p = paths["--preview"]
        blocks = [f".{key}.{m.mode}{{color-scheme:{m.mode};{m.decl(t['font'])}}}" for key, t in themes.items()
                  for m in t["modes"].values()]
        files[p] = between(p.read_text(), "/* tokens:begin */", "/* tokens:end */", "\n".join(blocks) + "\n", p)
    stale = [p for p, text in files.items() if not p.exists() or p.read_text() != text]
    if args["--check"]:
        for p in stale:
            print(f"{p} is not what palettes.toml makes: run theme.py without --check", file=sys.stderr)
        return 1 if stale or wrong else 0
    for p in stale:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(files[p])
        print(f"wrote {p}")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
