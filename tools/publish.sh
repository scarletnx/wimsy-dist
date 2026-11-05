#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 the wimsy-dist contributors
# publish.sh: the drawings made beside it into dist/, the emojis into emoji/: each SVG with the licence REUSE.toml
# gives it (licences.py), its PNG (1024, transparent), the sheet of the three Tetos and the sheet of all the singers,
# five a row. Run after the make_*.py, which write into out/; the Teto UTAU is wimsy-teto.svg itself. Ends with
# check_dist.py.
set -eu
S=$(dirname "$(readlink -f "$0")")
R=$(dirname "$S")
D=$R/dist
E=$R/emoji
mkdir -p "$D" "$E"
# the PNGs carry no time, so the same drawing makes the same file
PNG="-define png:exclude-chunks=date,time"

# svg FROM TO: copies a drawing, stamps its licence, and refuses one that is not XML or embeds or links something
svg() {
    cp "$1" "$2"
    python3 -I "$S/licences.py" stamp "$2"
    xmllint --noout "$2"
    if grep -q '<image\|href="http' "$2"; then echo "publish.sh: $2 embeds or links something" >&2; exit 1; fi
}

ALL="teto-utau:Teto UTAU|teto-sv:Teto SV|teto-voicepeak:Teto VOICEPEAK|miku:Miku|neru:Neru|defoko:Defoko|adachi-rei-utau:Adachi Rei UTAU|adachi-rei-v5:Adachi Rei V5|adachi-rei-v6:Adachi Rei V6|gumi:GUMI|fuddles:Fuddles|yi-xi-sv:Yi Xi SV|yi-xi-sv2:Yi Xi SV2"
T=$(mktemp -d "$S/sheet.XXXXXX")
cleanup() {  # the tiles, also when a step fails
    for f in "$T"/*; do if [ -e "$f" ]; then rm -- "$f"; fi; done
    rmdir "$T"
}
trap cleanup EXIT
IFS='|'
for v in $ALL; do
    f=${v%%:*}
    label=${v#*:}
    if [ "$f" = teto-utau ]; then src="$S/wimsy-teto.svg"; else src="$S/out/wimsy-$f.svg"; fi
    svg "$src" "$D/wimsy-$f.svg"
    rsvg-convert -w 1024 -h 1024 "$D/wimsy-$f.svg" -o "$D/wimsy-$f.png"
    rsvg-convert -w 512 -h 512 -b white "$D/wimsy-$f.svg" -o "$T/$f.png"
    magick "$T/$f.png" -gravity north -background white -splice 0x40 -font DejaVu-Sans -pointsize 26 \
        -fill '#333333' -annotate +0+6 "$label" "$T/$f.png"
done
unset IFS
# shellcheck disable=SC2086
magick "$T/teto-utau.png" "$T/teto-sv.png" "$T/teto-voicepeak.png" +append $PNG "$D/wimsy-teto-versions.png"
# every one in ALL's order, five a row; a short last row padded with white
n=0 row=0 tiles=""
IFS='|'
for v in $ALL; do
    tiles="$tiles|$T/${v%%:*}.png"
    n=$((n + 1))
    if [ $((n % 5)) -eq 0 ]; then
        magick ${tiles#|} +append "$T/row$row.sheet"; row=$((row + 1)); tiles=""
    fi
done
if [ -n "$tiles" ]; then
    magick ${tiles#|} +append "$T/last.png"
    magick "$T/last.png" -background white -gravity west -extent $((512 * 5))x552 "$T/row$row.sheet"; row=$((row + 1))
fi
unset IFS
rows=""
i=0
while [ $i -lt $row ]; do rows="$rows $T/row$i.sheet"; i=$((i + 1)); done
# shellcheck disable=SC2086
magick $rows -append $PNG "$D/wimsy-versions.png"

# Aogo (make_aogo.py), the AogoWimsy bot's, and her sisters, DraVee's other agents (make_afugo.py, make_asugo.py,
# make_xuji.py): each SVG and PNG, not on the sheets: they are not singers. aogowimsy-avatar.png is drawn by hand from
# wimsy-aogo.png and stays as it is.
for f in aogo afugo asugo xuji; do
    svg "$S/out/wimsy-$f.svg" "$D/wimsy-$f.svg"
    rsvg-convert -w 1024 -h 1024 "$D/wimsy-$f.svg" -o "$D/wimsy-$f.png"
done
# Accord (make_accord.py): its SVG and PNG, and the AccordWimsy bot's avatar, the drawing on Accord's disc ringed by
# its rope (its SVG stays in out/); not on the sheets: Accord is a forge, not a singer
svg "$S/out/wimsy-accord.svg" "$D/wimsy-accord.svg"
rsvg-convert -w 1024 -h 1024 "$D/wimsy-accord.svg" -o "$D/wimsy-accord.png"
xmllint --noout "$S/out/accordwimsy-avatar.svg"
if grep -q '<image\|href="http' "$S/out/accordwimsy-avatar.svg"; then
    echo "publish.sh: accordwimsy-avatar.svg embeds or links something" >&2; exit 1
fi
rsvg-convert -w 1024 -h 1024 "$S/out/accordwimsy-avatar.svg" -o "$D/accordwimsy-avatar.png"
# edenprobe (make_edenprobe.py): its SVG and PNG, and its cover, which edenprobe keeps as static/icon.svg
for f in wimsy-edenprobe edenprobe-icon; do
    svg "$S/out/$f.svg" "$D/$f.svg"
    rsvg-convert -w 1024 -h 1024 "$D/$f.svg" -o "$D/$f.png"
done
# the systems' Wimsys (make_platforms.py): each SVG, its PNG, and its 128 px emoji, the icon beside each download in
# ReiWimsy's cards. Not on the sheets: they are not singers
for f in linux windows android macos ios; do
    svg "$S/out/wimsy-$f.svg" "$D/wimsy-$f.svg"
    rsvg-convert -w 1024 -h 1024 "$D/wimsy-$f.svg" -o "$D/wimsy-$f.png"
    rsvg-convert -w 128 -h 128 "$D/wimsy-$f.svg" -o "$E/wimsy_$f.png"
done
# Aogo's reactions (make_aogo_emoji.py), the AogoWimsy bot's Discord emojis: each SVG and its 128 px PNG in emoji/,
# under Discord's 256 KB for an emoji. Not on the sheets: they are emojis
for f in eyes thumbsup done no; do
    svg "$S/out/wimsyaogo_$f.svg" "$E/wimsyaogo_$f.svg"
    rsvg-convert -w 128 -h 128 "$E/wimsyaogo_$f.svg" -o "$E/wimsyaogo_$f.png"
    size=$(wc -c < "$E/wimsyaogo_$f.png" | tr -d " ")
    if [ "$size" -gt 262144 ]; then
        echo "publish.sh: emoji/wimsyaogo_$f.png is $size bytes, over Discord's 262144 for an emoji" >&2; exit 1
    fi
done
python3 -I "$S/check_dist.py"
