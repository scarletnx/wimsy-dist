#!/bin/sh
# publish.sh: the drawings made beside it into the folder above it: each SVG, its PNG (1024, transparent), the sheet of
# the three Tetos and the sheet of all of them, five a row. Run after make_versions.py and make_vocaloid.py, which
# write into out/; the Teto UTAU is wimsy-teto.svg itself.
set -eu
S=$(dirname "$(readlink -f "$0")")
D=$(dirname "$S")
mkdir -p "$D"
cp "$S/wimsy-teto.svg" "$D/wimsy-teto-utau.svg"
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
    [ "$f" = teto-utau ] || cp "$S/out/wimsy-$f.svg" "$D/wimsy-$f.svg"
    xmllint --noout "$D/wimsy-$f.svg"
    if grep -q '<image\|href="http' "$D/wimsy-$f.svg"; then echo "publish.sh: wimsy-$f.svg embeds or links something" >&2; exit 1; fi
    rsvg-convert -w 1024 -h 1024 "$D/wimsy-$f.svg" -o "$D/wimsy-$f.png"
    rsvg-convert -w 512 -h 512 -b white "$D/wimsy-$f.svg" -o "$T/$f.png"
    magick "$T/$f.png" -gravity north -background white -splice 0x40 -font DejaVu-Sans -pointsize 26 \
        -fill '#333333' -annotate +0+6 "$label" "$T/$f.png"
done
unset IFS
magick "$T/teto-utau.png" "$T/teto-sv.png" "$T/teto-voicepeak.png" +append "$D/wimsy-teto-versions.png"
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
magick $rows -append "$D/wimsy-versions.png"
# Aogo (make_aogo.py), the AogoWimsy bot's: her SVG and PNG, not on the sheets either
cp "$S/out/wimsy-aogo.svg" "$D/wimsy-aogo.svg"
xmllint --noout "$D/wimsy-aogo.svg"
rsvg-convert -w 1024 -h 1024 "$D/wimsy-aogo.svg" -o "$D/wimsy-aogo.png"
# Accord (make_accord.py): its SVG and PNG, and the AccordWimsy bot's avatar, the drawing on Accord's disc ringed by
# its rope; not on the sheets: Accord is a forge, not a singer
for f in wimsy-accord accordwimsy-avatar; do
    xmllint --noout "$S/out/$f.svg"
    if grep -q '<image\|href="http' "$S/out/$f.svg"; then echo "publish.sh: $f.svg embeds or links something" >&2; exit 1; fi
done
cp "$S/out/wimsy-accord.svg" "$D/wimsy-accord.svg"
rsvg-convert -w 1024 -h 1024 "$D/wimsy-accord.svg" -o "$D/wimsy-accord.png"
rsvg-convert -w 1024 -h 1024 "$S/out/accordwimsy-avatar.svg" -o "$D/accordwimsy-avatar.png"
# the systems' Wimsys (make_platforms.py): each SVG, its PNG, and its 128 px emoji, the icon beside each download in
# ReiWimsy's cards. Not on the sheets: they are not singers
mkdir -p "$D/emoji"
for f in linux windows android macos ios; do
    cp "$S/out/wimsy-$f.svg" "$D/wimsy-$f.svg"
    xmllint --noout "$D/wimsy-$f.svg"
    if grep -q '<image\|href="http' "$D/wimsy-$f.svg"; then echo "publish.sh: wimsy-$f.svg embeds or links something" >&2; exit 1; fi
    rsvg-convert -w 1024 -h 1024 "$D/wimsy-$f.svg" -o "$D/wimsy-$f.png"
    rsvg-convert -w 128 -h 128 "$D/wimsy-$f.svg" -o "$D/emoji/wimsy_$f.png"
done
ls -la "$D"
