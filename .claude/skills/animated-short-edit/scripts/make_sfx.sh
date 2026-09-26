#!/usr/bin/env bash
# Synthesize a small SFX kit and normalize every file to -1 dBFS peak,
# so data-volume in the composition alone sets each cue's level.
# (lavfi sine defaults to 1/8 amplitude, which is why normalizing matters.)
# Usage: make_sfx.sh <assets_dir> [pad_seconds]
set -euo pipefail
cd "$1"
PAD="${2:-3.3}"
FMT="aformat=channel_layouts=stereo:sample_rates=44100"

# notification: two quick rising blips
ffmpeg -v error -y -f lavfi -i "sine=f=1320:d=0.07" -f lavfi -i "sine=f=1760:d=0.09" \
  -filter_complex "[0]afade=t=out:st=0.02:d=0.05[a];[1]adelay=60|60,afade=t=out:st=0.08:d=0.07[b];[a][b]amix=2:normalize=0,$FMT" sfx-notify.wav
# success: bright C-major chime
ffmpeg -v error -y -f lavfi -i "sine=f=1046.5:d=0.5" -f lavfi -i "sine=f=1568:d=0.5" -f lavfi -i "sine=f=2093:d=0.5" \
  -filter_complex "[0][1][2]amix=3:normalize=0,afade=t=in:d=0.004,afade=t=out:st=0.03:d=0.45,$FMT" sfx-success.wav
# tick: tiny pop for counters
ffmpeg -v error -y -f lavfi -i "sine=f=900:d=0.06" -af "afade=t=in:d=0.003,afade=t=out:st=0.01:d=0.05,$FMT" sfx-tick.wav
# rise: quick upward chirp for surprise / punch-in
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.5*sin(2*PI*(300*t+900*t*t))':d=0.22:s=44100" \
  -af "afade=t=in:d=0.005,afade=t=out:st=0.08:d=0.14,$FMT" sfx-rise.wav
# whoosh: swelling band-passed pink noise, peak ~0.45 s in
ffmpeg -v error -y -f lavfi -i "anoisesrc=c=pink:d=0.6:a=0.6" \
  -af "highpass=f=300,lowpass=f=4000,afade=t=in:d=0.45:curve=exp,afade=t=out:st=0.45:d=0.15,$FMT" sfx-whoosh.wav
# bell: two-tone stop bell for the end card landing
ffmpeg -v error -y -f lavfi -i "sine=f=659.3:d=0.9" -f lavfi -i "sine=f=880:d=0.9" \
  -filter_complex "[0]afade=t=out:st=0.02:d=0.8[a];[1]adelay=180|180,afade=t=out:st=0.2:d=0.7[b];[a][b]amix=2:normalize=0,$FMT" sfx-bell.wav
# pad: soft A-major bed so the end card is not dead silent
ffmpeg -v error -y -f lavfi -i "sine=f=220:d=$PAD" -f lavfi -i "sine=f=277.2:d=$PAD" -f lavfi -i "sine=f=329.6:d=$PAD" -f lavfi -i "sine=f=440:d=$PAD" \
  -filter_complex "amix=4:normalize=0,tremolo=f=3:d=0.25,lowpass=f=1800,afade=t=in:d=0.5,afade=t=out:st=$(python3 -c "print(max(0.5,$PAD-0.9))"):d=0.9,$FMT" sfx-pad.wav

for f in sfx-*.wav; do
  m=$(ffmpeg -hide_banner -i "$f" -af volumedetect -f null - 2>&1 | grep -oE "max_volume: [-0-9.]+" | awk '{print $2}')
  g=$(python3 -c "print(-1-($m))")
  ffmpeg -v error -y -i "$f" -af "volume=${g}dB" "n-$f" && mv "n-$f" "$f"
  echo "$f  peak $m dB -> -1 dB"
done
