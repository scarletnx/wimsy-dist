# Wimsy: how to make one

Wimsy is ScarletNX's mascot (drawn by Liz, GPL-3.0-or-later, `dist/wimsy.svg` there): five leaves meeting at one point, the
head being the leaf with the eyes. Here Wimsy becomes singing voices and friends: Teto (UTAU, SV, VOICEPEAK), Miku,
Neru, Defoko, Adachi Rei (UTAU, V5, V6), GUMI, Fuddles and Yi Xi (SV, as BUTCHER VANITY draws her, and SV2,
VIMALION PROJECT's design). Each one changes the colours, the hair, the eyes and a
detail or two of the outfit, and nothing else: Wimsy's shapes stay.

## What is in this folder

- `wimsy-*.svg` and `wimsy-*.png`: the drawings. The PNGs are 1024x1024 with a transparent background.
- `wimsy-versions.png` (all of them, five a row) and `wimsy-teto-versions.png` (the three Tetos): the sheets.
- `tools/wimsy-teto.svg`: Teto UTAU, drawn by hand. Every other drawing is made from it.
- `tools/make_versions.py`: Teto SV and Teto VOICEPEAK, from the base. It also holds the letters of the marks.
- `tools/make_vocaloid.py`: everyone else, built on what `make_versions.py` makes.
- `tools/publish.sh`: checks each SVG, renders the PNGs and the sheets, and copies them all into this folder.
- `tools/make_platforms.py`: the systems ScarletNX ships for, as Wimsy: Linux (Tux: black, a white front, orange
  feet), Windows (blue, the four panes on the arm), Android (green, two antennas), macOS (space grey) and iOS (light
  grey, a blue front), the last two with the apple's leaf over the head. `wimsy-<system>.svg` and `.png` here, and
  `emoji/wimsy_<system>.png` at 128 px: the ReiWimsy application's emojis, beside each download in its cards. Not on
  the sheets: they are not singers.
- `tools/make_aogo.py`: Aogo (AO55, DraVee's agent), from her drawing on accord.dravee.dev
  (drawn by Kedr, Kedr_bit on X): long coral hair, glasses, a black clip with AO, 55 on the sleeve. `wimsy-aogo.svg`
  and `.png` here, as publish.sh makes the others, and `aogowimsy-avatar.png`, the AogoWimsy bot's avatar: the drawing
  at 74% on a dark disc, so Discord's round crop keeps it whole. Not on the sheets: she is not a singer.
- `tools/make_afugo.py`: Afugo (AF51, DraVee's Fable agent), Aogo's sister, from her drawing on accord.dravee.dev (drawn
  by Kedr, Kedr_bit on X): long messy rust hair with two spikes on top, tired eyes over grey lilac shadows, a yawn, a
  black clip with AF, 51 on the sleeve. The rust is her drawing's, redder and darker than Aogo's coral, and the lilac
  her drawing shades her white shirt and her tired eyes with takes the wings, where Aogo's are white and grey.
  `wimsy-afugo.svg` and `.png` here. Not on the sheets: she is not a singer.
- `tools/make_asugo.py`: Asugo (AS55, DraVee's Sonnet agent), Aogo's carefree sister. She has no drawing of her own
  (the forge shows only Gravatar's pattern for her), so she takes her sisters' colours: apricot hair, Aogo's coral made
  lighter and more golden, in a ponytail swinging out, a white top with apricot trim, lilac grey sleeves, amber eyes,
  one of them shut in a wink over an open grin, the black clip with AS, 55 on the sleeve. `wimsy-asugo.svg` and `.png`
  here. Not on the sheets: she is not a singer.
- `tools/make_xuji.py`: Xuji (XG47, DraVee's Grok Build agent), Aogo's sister, from her picture on accord.dravee.dev
  (drawn by Kedr, Kedr_bit on X): long black hair with a violet sheen, its big loop a thin crescent arching over the
  head, a fringe swept over the back eye in pointed locks, the other eye half shut and unimpressed under a raised brow,
  a `:3` mouth, pale lavender skin, a black tee with her studded choker as its trim, her bare lavender arms as the back
  wing, a white clip with XG, 47 on the arm. `wimsy-xuji.svg` and `.png` here. Not on the sheets: she is not a singer.
- `tools/make_edenprobe.py`: edenprobe, the test program ScarletNX and rEden are held to, in Eden's sunset colours
  (its pink, purple and blue, the cyan of its mark; Eden's `dist/dev.eden_emu.eden.svg`) with a test probe, its needle
  out toward the drawing's empty lower right and its cable curling after it. `wimsy-edenprobe.svg` and `.png` here,
  and `edenprobe-icon.svg` and `.png`, edenprobe's cover: the drawing over the banded sun its `static/icon.svg` had,
  with the program's name; edenprobe's `make icon` turns it into the NRO's icon.jpg. Not on the sheets: it is a
  program.
- `tools/make_accord.py`: Accord, DraVee's forge (accord.dravee.dev), from its mark (the forge's
  `assets/img/logo.svg`): black and white, the mark's rope as small white leaves slanted across the black trim, its cross
  of four petals, four leaves with a dot between each two, on the arm. `wimsy-accord.svg` and `.png` here, and
  `accordwimsy-avatar.png`, the AccordWimsy bot's avatar: the mark's disc, its rope a band of white leaves round the black
  edge, the drawing on the white middle, centred on its smallest enclosing circle. Not on the sheets: it is a forge.

## Making them all again

You need `python3`, `rsvg-convert` (librsvg), `xmllint` (libxml2) and `magick` (ImageMagick 7) with the DejaVu Sans
font (only for the names on the sheets).

    cd tools
    python3 -I make_versions.py
    python3 -I make_vocaloid.py
    python3 -I make_platforms.py
    python3 -I make_aogo.py
    python3 -I make_afugo.py
    python3 -I make_asugo.py
    python3 -I make_xuji.py
    python3 -I make_accord.py
    sh publish.sh

The generators write into `tools/out/`, and `publish.sh` copies from there into this folder. Teto UTAU is
`tools/wimsy-teto.svg` itself: changing it changes the base of every drawing.

## The anatomy (viewBox 0 0 512 512)

- **The centre**, `(217.78, 336.65)`: where the five leaves meet.
- **The head**: the leaf from the centre to its tip at `(508, 191)`. To draw on it, use the head's frame,
  `translate(217.8,336.7) rotate(-26.68)`: there `x` runs from the centre to the tip and negative `y` goes to the top
  of the face. The upper edge passes near `y = -42` (at `x = 175`), the lower one near `y = +62` (at `x = 153`). The
  hair covers the back of the head (up to about `x = 110`) and the bangs sit above the eyes.
- **The eyes**: centres at `(356.1, 269.0)` and `(424.8, 239.2)` on the page, radius 23.1. In the head's frame they
  are at `x = 154` and `x = 229`, on the axis.
- **The wings**: the back one is the sleeves or what is worn under; the front one is the top or the jacket. The front
  wing's trim follows `M 279,40 C 246,92 226,170 224,300`.
- **The two leaves below**: in the hair's colour. They are not a tail: Wimsy has no tail.
- **The hanging hair**: the near tail at `translate(322,320) rotate(-10)`, the far one at `translate(256,300)
  rotate(5)`, behind the head. That is where Teto's drills hang, and where any twintail goes.

## The rules of the style

Each rule comes from a change asked for on one of the drawings.

1. **Everything is a leaf**: two arcs meeting in points, a gradient, a white outline. The outline is 5.47 on the
   wings and the head, 3.64 on the leaves below, 4.5 on the hair and 3 to 4 on the details.
2. **The hair is short**: a tail or a drill is about 110 px long, Fuddles' size, and still a leaf. The drills scale
   to `(0.66, 0.5)`; a tail leaf to about `(0.7 to 0.9, 0.44 to 0.52)`.
3. **One tail is one leaf.** Twintails are one on each side, one in front and one behind, where Teto's drills are. A
   side tail (Neru, Adachi Rei) uses only the near place. Two leaves for one tail read as two tails; two straight
   leaves side by side under the body read as legs.
4. **A drill**: each turn is a leaf lying down, slanted as a helix winds, the turns getting smaller toward the tip,
   with a transparent gap between one turn and the next.
5. **Nothing runs across a leaf.** A strap from side to side reads as a bandana. Outfit details follow the curve:
   the trim, Adachi Rei V6's piano keys and V5's sound wave sit on it. A circuit trace like Fuddles' may run on
   behind another leaf, drawn under it (`back_extras`), but never over it: one drawn over a leaf in front reads as
   passing from one leaf to the next.
6. **A hair accessory sits on a turn or a tail, made of leaves**: Teto SV's bow is on the first turn of the drill,
   its loops and tails leaves too.
7. **A mark on the arm** (04, 0401, 01, DEN2, 00): letters in strokes, no font, on the back wing.
8. **The colours come from the official art**, read off the image (below), never from memory. Versions of one
   character change what their art changes: Adachi Rei changes jacket and eyes with each version.
9. **The eyes tell the character**: Neru is tsundere, Defoko stares blankly, Adachi Rei has lens eyes, Fuddles has
   one cyan eye and one blue eye, and a smile.
10. **The credits stay**: Wimsy is Liz's (ScarletNX's `dist/wimsy.svg`), GPL-3.0-or-later. Each SVG's metadata says so, and
    where its colours came from.

## Making a new character

Copy a `character(...)` from `tools/make_vocaloid.py`, change its fields, and add the character to the list at the
end of that file and to the `ALL` list in `publish.sh`. Here is an example with twintails and round eyes:

    EXAMPLE = character(
        name="Example", who="Example", who_full="Example", hair_word="twintails",
        hair_colour="blue", trim_word="blue", eyes_word="Example's blue",
        source="colours made up for the README",
        palette_note="Example: blue hair, blue eyes, a grey top, black sleeves with blue trim",
        hair=("#6FA8E8", "#3F78C0"), tail=("#5E98DC", "#2E62A8"), tail_dark=("#3F78C0", "#244E88"),
        far=("#3F78C0", "#244E88"), far_dark=("#2E62A8", "#1C3E70"),
        outfit=("#C4C7CC", "#9A9EA4"), back_wing="#2A2C30", trim="#3F78C0",
        iris=("#9CC8F4", "#3F78C0", "#1C3E70"), rim="#14243C", shine="#CFE3FA",
        tie="#2A2C30", band="#6FA8E8", tie_h=16,
        tails_note="her twintails: one leaf each, where Teto's drills are",
        far_use='  <use xlink:href="#drill-far" transform="translate(256,300) rotate(5) scale(0.72,0.44)"/>',
        near_use='  <use xlink:href="#drill" transform="translate(322,320) rotate(-10) scale(0.78,0.47)"/>',
        far_note="  <!-- the far twintail, behind the head -->\n",
        near_note="  <!-- the near twintail, in front -->\n",
        mark="02",
    )

In the list at the end of `make_vocaloid.py`:

    (EXAMPLE, "wimsy-example.svg"),

In the `ALL` list of `publish.sh` (separated by `|`):

    example:Example

Then run `python3 -I make_vocaloid.py` and `sh publish.sh`.

### The fields

| Field | What it is |
| --- | --- |
| `name`, `who`, `who_full` | The name in the metadata, short and full |
| `hair_word`, `hair_colour`, `trim_word`, `eyes_word`, `source`, `palette_note`, `tails_note` | What the SVG's comments and metadata say |
| `hair` | The gradient of the bangs and the back of the head (light, dark) |
| `tail` | The near tail and the two leaves below |
| `tail_dark` | The darker tone: the alternate turns of Teto's drills; needed even without a drill |
| `far`, `far_dark` | The far tail, darker for being behind, and its dark tone (as `tail_dark`) |
| `outfit`, `back_wing` | The front wing (a gradient) and the back wing (a colour, or `url(#id)` of a gradient of yours) |
| `trim`, `trim_width` | The front wing's trim |
| `iris`, `rim`, `ring`, `shine` | The eye: the iris (centre, middle, edge), the dark rim, the lens' ring, the light on the hair |
| `eyes`, `lid`, `brow` | The look (table below), the colour of the lid (`skin`: the face's own gradient, so no disc shows round the eye) and of the brow |
| `bags` | The colour of the shadows under `tired` eyes |
| `iris2` | The front eye's iris, for eyes of two colours (`None`: both alike) |
| `pupil` | The colour of the small light in a `sly` eye |
| `mole` | A beauty mark, `(x, y)` in the head's frame (`None`: none) |
| `mouth` | The colour of a smile below the back eye (empty: no mouth) |
| `tie`, `band`, `tie_h` | The tail's tie, its band and its height; `tie=None` is a loose tail |
| `tail_vein` | The colour of a light vein along each tail (`None`: no vein) |
| `near_use`, `far_use`, `near_note`, `far_note` | Where the tails hang (empty: none) |
| `ahoge` | The curl on top of the head: `True` is Teto's; a path in the head's frame is one of your own (Afugo's spikes), drawn under the wings and the head as Teto's is |
| `mark`, `mark_colour` | The mark on the arm and its colour |
| `skin` | The face's gradient (light, lighter) in place of the warm one |
| `hair_path`, `hair_fill` | The hair's outline over the head, in the head's frame, and its fill: Fuddles' band of hair |
| `defs_extra` | Gradients of your own (`gradient(id, stops)` writes one with any number of stops) |
| `front_fill`, `lower_fills` | The front wing and each leaf below in one of those gradients |
| `back_extras` | More SVG on the back wing, drawn before the front wing so that the front wing covers it |
| `wing_extras`, `head_extras`, `front_extras` | More SVG over both wings, over the head and the leaves below, or in front of everything |

### The eyes

| `eyes` | How it looks | Who uses it |
| --- | --- | --- |
| `round` | Wimsy's eye, with the big glint | Teto, Miku, GUMI, Fuddles |
| `tsundere` | Lids slanting down to the inner corners, a frowning brow, a look aside | Neru |
| `deadpan` | A flat lid over the upper half, no glint | Defoko |
| `lens` | A camera's lens (a ring and a dot), wide open, small glints | Adachi Rei UTAU |
| `lens-soft` | The lens under a gently arched lid, calm | Adachi Rei V5 |
| `lens-cool` | The lens under a flat lid half way down | Adachi Rei V6 |
| `sly` | Half shut under a heavy lid, a dark iris turned aside with a small light at its middle (`pupil`), a sliver of white at the outer corner, two tired lines under it | Yi Xi SV2 |
| `caret` | Shut in a smile, each eye a `^` standing upright as it is typed (Yi Xi's `^q^`) | Yi Xi SV, Aogo |
| `tired` | Open under a heavy lid that sags to the outer corner, a dull small glint, a crescent of shadow under each eye (`bags`) | Afugo |
| `wink` | The back eye open with its big glint, the front one shut in an arc bowed up, two lashes flicking out at its outer corner | Asugo |
| `meh` | The back eye under the bangs (a `hair_path` that covers it), not drawn; the front one half shut under a lid that sags to the outer corner, a dull small glint, its brow raised at the inner end | Xuji |

A new look goes into `eyes_svg()` in `make_vocaloid.py`. Head accessories (beret, goggles, antennas) go into
`head_extras`, drawn in the head's frame: see Defoko's beret and GUMI's goggles. Circuit traces like Fuddles' are
made with `trace(path, colour, dots)`, and the light lines along a leaf with `vein(path, colour, opacity)`, each
inside its leaf with a `clipPath` of that leaf.

## Reading the colours off a reference

Use the official art: the character's or the product's site, or the creator's own drawing. The main colours of the
image:

    magick ref.png -background white -alpha remove -colors 12 -format %c histogram:info:- | sort -rn | head -12

The colour of one point (x, y in the image's pixels). On an image with transparency the last two digits are the
opacity (`FFFEEDFF` is an opaque `#FFFEED`):

    magick ref.png -format "%[hex:p{300,150}]" info:

The hair gives `hair`, `tail` and `far`, and its darkest tones `tail_dark` and `far_dark`. The outfit gives the wings
and the trim, and the art's eyes give the iris.

## License

The drawings, the generators and their PNGs are GPL-3.0-or-later, as Wimsy is (`LICENSE`).

## The references

The colours were read from Yi Xi's art: the BUTCHER VANITY music video (FLAVOR FOLEY, drawn by ricedeity) and
VIMALION PROJECT's designs (vimalion.pro/yixi), which they let anyone use with credit. Those images are their owners'
and stay out of this repo: put them in `ref/`, which git leaves out, to read the colours again.

Aogo, Afugo and Xuji come from their pictures on accord.dravee.dev, drawn by Kedr (Kedr_bit on X); Asugo, who has
none, takes her sisters' colours. Those pictures are Kedr's and stay out of this repo too, in `ref/` beside the others.

## Checking before sending

`publish.sh` already refuses an invalid SVG (`xmllint`) or one that embeds or links to something outside
(`<image>`, `href="http`). Then look at `wimsy-versions.png`: that is where a tail that reads as a leg, a strap that
became a bandana or an accessory lost in the outline shows.
