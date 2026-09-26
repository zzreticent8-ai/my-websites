# Gotchas hit on real edits

Each of these cost a render cycle once. Check them before rendering.

## Environment
- **Renderer can't find Chrome.** `hyperframes doctor` says "Chrome Headless Shell is
  required". Set `PRODUCER_HEADLESS_SHELL_PATH` and `HYPERFRAMES_BROWSER_PATH` to the
  Playwright `headless_shell` binary (`setup.sh` finds it under `/opt/pw-browsers`).
- **Transcription models blocked.** `faster-whisper` (huggingface.co) and `openai-whisper`
  (openaipublic.azureedge.net) downloads get a 403 from the proxy. Don't burn time;
  derive timing from caption changes (`analyze.py`) and read text off frames.
- **Fonts via jsdelivr are blocked**, fonts.googleapis.com works: use `fonts.sh`.
- **Kie.ai** needs `KIE_API_KEY` in the cloud environment's variables and `api.kie.ai`
  in allowed network domains. Tell the user where; never ask for the key in chat.
- Don't `rm -f $VAR/*`: the safety check blocks it. Use `"${VAR:?}"/*` or a literal path.

## Composition
- **Root `data-start` conflict.** The kit's `preflight.mjs` fails "root has data-start AND an
  inline video", but `hyperframes lint` errors *without* root `data-start="0"`. Keep
  `data-start="0"` (lint wins; the kit's own `claude-edit-intro` does the same with the video
  inside a non-timed wrapper) and note the preflight flag as a known false positive.
- Animate the `#cam` wrapper, never the `<video>`. The video is `muted`; audio is a
  separate `<audio>` (a pre-trimmed `dialogue.wav`).
- Same `data-track-index` clips must not overlap: give each SFX type its own track and
  reuse a track only for sequential cues (ticks).
- `transform-origin` zoom keeps the origin point fixed on screen. To push *into* a prop
  and centre it, tween `x/y` together with `scale` (see beat-library §4a).
- `tl.set` a new `transformOrigin` at the cut where it changes. Seeking backwards
  reverts it correctly.

## Look
- **`back.in` exits linger.** A 0.4 s `back.in` first dips the other way, so the card
  still sat in place ~0.2 s after the line and covered the reaction burst. Exit with
  0.3 s `power2.in` starting ~0.05 s early, then check a keyframe 0.15 s after the line.
- Burned captions **lag scene cuts by ~0.25 s** (the previous line lingers into the next
  shot). Anchor overlay state changes to caption changes and camera resets to cuts.
- Silkscreen/LED text **wraps** at 60 px with letter-spacing in a 900 px panel. Use
  `nowrap`, no letter-spacing, and ~56 px for 17 characters.
- A dense LED dot mask made the sign text unreadable. Keep the mask light (≤40 %).
- A translucent card (84 % alpha) let busy background text show through; 92 % is clean.
- End-card content looks sparse at small sizes: question ≈88 px, pill 60 px, logo 300 px.

## Audio
- `lavfi sine` generates at 1/8 amplitude (-18 dBFS). Un-normalized SFX at data-volume
  0.3–0.4 measured -33 dBFS in the mix, which is inaudible. `make_sfx.sh` normalizes.
- The source's music often stops ~1 s before its own end screen; a replacement end card
  needs its own bed (pad) or it plays in dead silence.
- After mastering, the AAC stream can run ~60 ms past the video. `master.sh` trims with `-t`.
- Level checks are measurement, not listening. Say so in VERIFY.md.
