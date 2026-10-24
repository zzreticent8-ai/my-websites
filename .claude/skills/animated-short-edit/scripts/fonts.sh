#!/usr/bin/env bash
# Download Google Fonts as local woff2 + fonts.css (renders must not hit CDNs).
# Usage: fonts.sh <assets_dir> "Baloo+2:wght@600;800" "Silkscreen:wght@400;700" ...
# Link from the composition with: <link rel="stylesheet" href="assets/fonts/fonts.css">
set -euo pipefail
DIR="$1/fonts"; shift
mkdir -p "$DIR"; cd "$DIR"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
: > fonts.css
for fam in "$@"; do
  curl -fsS -A "$UA" "https://fonts.googleapis.com/css2?family=$fam&display=swap" >> fonts.css
done
grep -oE "https://fonts.gstatic.com[^)]+" fonts.css | sort -u | while read -r u; do curl -fsS -O "$u"; done
sed -i 's#https://fonts.gstatic.com/s/[^)]*/\([^/)]*\.woff2\)#\1#g' fonts.css
echo "$(grep -c @font-face fonts.css) faces in $DIR/fonts.css"
