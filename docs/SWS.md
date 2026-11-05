# SWS: the Simple Wimsy Style

The rule ScarletNX's own pages follow (Tracer's site, the forge, the status page) and the colours of the launcher's
themes. Its grammar is GFSS's (the Golden Fetchero Standard Style): what is on a screen, where it sits and what it
does. Its look is the theme's: the palette, the shapes below and the theme's Wimsy. Where the two speak of the same
thing, the theme wins on how it looks and GFSS on what is there, as rESS (rEden's) splits them. Over both sits *Pra
Leigo Ver*: a page is for someone who has never read its manual.

## Index

- [The themes](#the-themes)
- [Colour](#colour)
- [Shape and type](#shape-and-type)
- [For a lay reader](#for-a-lay-reader)
- [Picking a theme](#picking-a-theme)
- [Each theme's Wimsy](#each-themes-wimsy)
- [Making the files](#making-the-files)
- [Checking a page](#checking-a-page)

## The themes

| Theme | Light | Dark | Its colours |
|---|---|---|---|
| Sepia | yes | yes | the launcher's warm built-in (`yorha`): paper and ink, dark sepia text, muted warm greys |
| Wimsy | yes | yes | Wimsy's own fills (ScarletNX's `dist/wimsy.svg`): petal, head, leaf, wine |
| Fuddles | yes | yes | Fuddles' Wimsy (`dist/splash/wimsy-fuddles.svg`): navy, blue, violet, cyan, rose |
| Default | no | yes | the launcher's Default: black and the 16 colours of an early PC, in the system's monospace |

A page follows the system's light or dark unless its reader picked one. Sepia is the default everywhere.

## Colour

- **Only by role.** A rule asks for a role (`var(--accent)`), never a colour: the theme gives the value. The roles:
  `bg` (the page), `surface` and `raised` (a card, and what sits a step above it: a header band, a table head, code),
  `faint` (hairlines; a filled box in the launcher), `rule` (borders of what is touched), `ink` and `soft` (text and
  secondary text), `accent` and `on-accent` (links, and what is filled for "yes"), and `ok`, `warn`, `bad` with their
  `-fill` and `on-` (a state's colour as text or a mark, its fill, the text on that fill).
- **Contrast, in every mode.** Text 4.5:1 on `bg`, `surface` and `raised`; borders 3:1; each fill and its text 4.5:1.
  `themes/theme.py` moves a colour's lightness until it reads, says so, and refuses to write a theme that does not.
- **Elevation is colour**, a step of `surface` or `raised`. A shadow only on what floats (a menu, a dialog).
- **Filled is "yes", outlined is "not yet"**: the chosen item, the current page, a state that holds.
- **The colour never speaks alone.** A state says its word and carries a mark (a check, a "!", an X); a down bar in a
  row of bars is hatched.

## Shape and type

- **Square corners.** A border is 1px. GFSS's pill for what is touched is the one rule SWS sets aside.
- **Spacing** on 4, 8, 12, 16, 24 and 32 px; a page uses the window's width, the text a measure (`70ch`) where it is
  read.
- **Quiet labels**: navigation, table heads, field names and state pills in capitals spaced 0.08em. Titles and names
  stay as written.
- **The system's font**, and its monospace for code (Default: for everything). Nothing is downloaded.
- **Targets** of 24px at least, 40px for buttons and links in a bar; letters of 11px at least, 12px where they are read
  on the move.
- **No motion.** A state changes at once; hover changes a colour or an underline, nothing moves.

## For a lay reader

- Little text: a title, a one-line subtitle, short hints. An explanation goes behind a "?" beside the title.
- A word of the house shows as its pill (with its mark and colour), never explained in a sentence.
- One word per screen: a page's title, its tab and the link to it say the same word.
- A link looks like a link (underlined), a button like a button (filled or outlined, never bare text).

## Picking a theme

Every page has the picker at its top: the themes and Auto, Light and Dark, plain links, the pick in effect filled. A
pick is kept for the next visit in a cookie of all of scarletnx.dev, and nothing on the page runs a script: how each
site keeps and reads it is in wimsy-core's `docs/THEMES.md`. The launcher picks in Settings > App > Theme, and in the
setup's first step.

## Each theme's Wimsy

Each theme has Wimsy in its colours: Liz's five leaves (GPL-3.0-or-later; every drawing's metadata credits her).

| Theme | Its Wimsy |
|---|---|
| Sepia | `themes/wimsy-sepia.svg`: the leaves in ink and warm greys, the head ochre |
| Wimsy | ScarletNX's `dist/wimsy.svg` itself |
| Fuddles | ScarletNX's `dist/splash/wimsy-fuddles.svg` |
| Default | `themes/wimsy-default.svg`: the leaves on a 32 by 32 grid in an early PC's colours |

## Making the files

`themes/palettes.toml` holds every colour; nothing else does. From it:

    python3 themes/theme.py --table                  # every role, where it came from, every pair checked
    python3 themes/theme.py --core ../wimsy-core     # Tracer's style.css block, Forgejo's themes, Gatus's lines
    python3 themes/theme.py --gui ../ScarletNX       # the launcher's built-ins made here (sepia-dark, wimsy...)
    python3 themes/theme.py --check --core ../wimsy-core --gui ../ScarletNX
    python3 themes/wimsys.py <ScarletNX>/dist/wimsy.svg   # each theme's Wimsy

The sites and the launcher take these files as they are; a colour changes in `palettes.toml` and the files are made
again. wimsy-core's `scripts/check-theme.sh` holds its rules to the roles.

## Checking a page

- Both modes of every theme, at 360 and 1280 px of width: no sideways scroll, nothing over anything else.
- `theme.py --table` passes; a pair under its contrast is a colour to change, never a check to loosen.
- A rule with a colour of its own, or a role no theme gives, fails the site's check.
