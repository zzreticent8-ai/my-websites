#!/usr/bin/env bash
# Two-pass linear loudnorm to -16 LUFS / -1.5 dBTP, video stream copied,
# audio trimmed to the video length. Prints final loudness and sha256.
# Usage: master.sh <in.mp4> <out.mp4> [target_lufs]
set -euo pipefail
IN="$1"; OUT="$2"; I="${3:--16}"
J=$(ffmpeg -hide_banner -i "$IN" -af "loudnorm=I=$I:TP=-1.5:LRA=11:print_format=json" -f null - 2>&1 | sed -n '/^{/,/^}/p')
M=$(echo "$J" | python3 -c "import json,sys;d=json.load(sys.stdin);print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
VDUR=$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 "$IN")
ffmpeg -v error -y -i "$IN" -t "$VDUR" -c:v copy \
  -af "loudnorm=I=$I:TP=-1.5:LRA=11:$M:linear=true,aresample=44100" -c:a aac -b:a 192k "$OUT"
ffmpeg -hide_banner -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I:|Peak:)"
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,duration -of compact "$OUT"
sha256sum "$OUT"
