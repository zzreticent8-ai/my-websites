#!/usr/bin/env bash
# Labelled contact sheet of frames at given times.
# Usage: keyframes.sh <video> <out.jpg> t1 t2 ... [--cols N] [--width PX]
set -euo pipefail
VIDEO="$1"; OUT="$2"; shift 2
COLS=5; WIDTH=300; TIMES=()
while [ $# -gt 0 ]; do
  case "$1" in
    --cols) COLS="$2"; shift 2 ;;
    --width) WIDTH="$2"; shift 2 ;;
    *) TIMES+=("$1"); shift ;;
  esac
done
TMP="$(mktemp -d)"
trap 'rm -rf -- "${TMP:?}"' EXIT
i=0
for t in "${TIMES[@]}"; do
  ffmpeg -v error -y -ss "$t" -i "$VIDEO" -frames:v 1 \
    -vf "scale=${WIDTH}:-2,drawtext=text='${t}':x=8:y=8:fontsize=26:fontcolor=red:box=1:boxcolor=black@0.5" \
    "$TMP/f$(printf %03d $i).png"
  i=$((i+1))
done
N=${#TIMES[@]}
[ "$N" -lt "$COLS" ] && COLS=$N
ROWS=$(( (N + COLS - 1) / COLS ))
ffmpeg -v error -y -i "$TMP/f%03d.png" -vf "tile=${COLS}x${ROWS}" -frames:v 1 "$OUT"
echo "wrote $OUT ($N frames)"
