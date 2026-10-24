#!/usr/bin/env bash
# Peak/mean level in time windows of a render (SFX audibility check).
# Usage: sfx_levels.sh <video> start:dur [start:dur ...]
set -euo pipefail
V="$1"; shift
for w in "$@"; do
  s="${w%%:*}"; d="${w##*:}"
  printf "%6s +%-5s " "$s" "$d"
  ffmpeg -hide_banner -ss "$s" -t "$d" -i "$V" -vn -af volumedetect -f null - 2>&1 \
    | grep -oE "(mean|max)_volume: [-0-9.]+ dB" | tr '\n' ' '
  echo
done
