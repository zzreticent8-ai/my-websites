# Gotchas hit on real edits

Each of these cost a render cycle once. Check them before rendering.

## Environment
- **Renderer can't find Chrome.** `hyperframes doctor` says "Chrome Headless Shell is
  required". Set `PRODUCER_HEADLESS_SHELL_PATH` and `HYPERFRAMES_BROWSER_PATH` to the
  Playwright `headless_shell` binary (`setup.sh` finds it under `/opt/pw-browsers`).
- **Transcription models blocked.** `faster-whisper` (huggingface.co), `openai-whisper`
  (openaipublic.azureedge.net), vosk (alphacephei.com) and whisper.cpp release downloads
  are blocked by the proxy. PyPI is reachable: `pocketsphinx` ships its own English model.
  With burned captions, time from caption changes (`analyze.py`); without them, use
  `transcribe.py` + `align_captions.py` (see no-captions.md).
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

## Lint rules that fired
- `gsap_non_transform_motion` (error): tweening `left`/`top`/`width` snaps to pixels and
  stutters under frame capture. Use only transforms (`x`, `y`, `scale`, `rotation`),
  `opacity` and colours. A capacity marker sliding via `left` became a fade.
- `overlapping_gsap_tweens` (warning): two tweens on the same property of the same element
  overlap in time, e.g. a pop-in scale and a pulse scale. Start the second after the first ends.
- `gsap_exit_missing_hard_kill` (error): an element faded out right at its clip's end
  needs `tl.set(sel, { opacity: 0 }, clipEnd)` after the fade, so non-linear seeking
  can't land on stale visibility.
- `timeline_track_too_dense` (warning): ~10 caption clips on one track. Acceptable for a reel.
- Lint errors don't stop `render`, so read the lint output before trusting a draft.

## Look
- **A state shown for 0.3 s doesn't register.** "Built to handle growth" appeared at
  answer+0.6 and exited at the wide cut. Switch states as the line starts and keep
  the card through the next shot if needed; exit before the push.
- A chip's scale pop (1.1–1.12) briefly overlaps its neighbour in the chip row. It's
  transient and fine, but don't judge spacing from a frame mid-pop.
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
