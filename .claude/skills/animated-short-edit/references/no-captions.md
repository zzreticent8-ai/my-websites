# Videos without burned captions or a logo

Used on "Cat, explain AI" (720x1280 @ 24 fps, no captions, no logo, no end card,
speech to the last 0.2 s). Recognise the case from `events.jpg`: no caption box in any
frame, and `caption_changes` in `analysis.json` just repeat scene cuts or fire in bursts
during camera motion. Everything else in the skill still applies; this adds a
transcript, a caption layer, a logo bug and a written CTA.

## 1. Transcript and timing (no ASR service needed)

```bash
python3 scripts/transcribe.py <video> <outdir>          # rough pocketsphinx hypothesis + times
```

pocketsphinx installs from PyPI with its own English model, so it works when Hugging
Face and OpenAI hosts are blocked. Its hypothesis is rough ("complicated were easy you
get a i a job…"). Correct it into the real script using the frames, context and the
video's file name, then write one caption phrase per line:

```
Explain AI without using | explain a i without using
complicated words.
Easy.
You give AI a job, | you give a i a job
```

When a stretch of the hypothesis could be several wordings, rank them against the audio
before committing:

```bash
python3 scripts/score_candidates.py <video> 3.6 5.0 "Then learn AI too. | then learn a i too" \
    "Then learn AI. | then learn a i" "So learn AI too. | so learn a i too"
```

Take the window from `transcribe.py`'s word times, with ~0.1 s margin. Higher is better
within one window. "Could not align" means the wording doesn't fit the audio at all
("For real?", "Fair enough." at the end of the bookstore clip). Gaps under ~0.005 are a
tie ("Fair." vs "Oh, fair."); settle it from the frames and prefer the simpler caption.
On the bookstore clip this settled every doubtful line: "them learn a guy to" → "Then learn
AI too.", "no one would a guy can do" → "knowing what AI can do".

Text after `|` is what was *spoken*, for acronyms, numbers and brand names
("AI" → `a i`, "$20" → `twenty dollars`, "ChatGPT" → `chat g p t`). Then:

```bash
python3 scripts/align_captions.py <video> phrases.txt <outdir> --end <T.cut>
```

It force-aligns the script, stops with a list of any words missing from the dictionary
(respell them after `|`), and writes `words.json`, `phrases.json` and `captions.html`
(ready-made `.cap` clips on track 3). Sanity-check it: the gaps between phrases should
line up with `silences_-30dB` from `analyze.py`. The aligner can start a phrase inside
the preceding pause ("Because" at 1.86 when speech resumed at 2.07); move that caption's
start to the silence end and extend the previous caption to meet it. A word that aligns to under ~0.1 s at
the very start was probably never spoken; drop it.

Say in VERIFY.md and to the user that the words are a corrected recognizer pass and
need proofreading. You cannot hear the audio.

Phrase groups: 2–5 words, break at commas and speaker changes, one speaker per
caption. Speaker attribution comes from open mouths and who is on screen.

## 2. Caption layer (series style)

Place captions in the root composition, outside `#cam`, so punch-ins don't scale them.

```css
.cap{position:absolute;left:0;top:1500px;width:1080px;display:flex;justify-content:center;z-index:7}
.cap span{max-width:860px;text-align:center;font-weight:600;font-size:50px;line-height:1.12;color:#8cf5c4;
  background:rgba(0,0,0,.86);padding:4px 20px 6px;border-radius:14px}
```

```js
document.querySelectorAll('.cap').forEach(el => {
  tl.from(`#${el.id} span`, { scale: 0.9, opacity: 0, duration: 0.12, ease: 'back.out(2)' }, parseFloat(el.dataset.start));
});
```

Ten or so caption clips on one track trigger lint's `timeline_track_too_dense` warning;
that is fine for a short reel.

## 3. Logo bug

For Her Startup Ideas videos, `assets/her-startup-ideas-logo.png` is the series logo
(transparent, cropped from a series end card). Place it where the series puts it:

```html
<img id="logoBug" class="clip" src="assets/logo.png" data-start="0" data-duration="<T.cut>" data-track-index="6"
     style="position:absolute;left:785px;top:1595px;width:250px;height:250px;z-index:6">
```

For any other brand, use a logo the user supplies. Never draw one.

## 4. End card and CTA

With no creator CTA to keep, write one in the series' voice: a short question on the
video's claim plus "Comment below" ("Could you explain AI this simply?"). Tell the user
you wrote it. When speech runs to the end of the source, start the end card on the last
word's end and cross-fade over ~0.15 s. The push must *land* inside that fade (end it at
`T.cut + 0.1`), not at the source end: a push timed to 10.0 left the real book 170 px
off the end-card cover at the swap. Keep the video clip
running to the source end.

## 5. Frame rate and size

Keep the source frame rate: set `meta.json` `fps` and pass `--fps` to render (24 for
this series' AI clips). Converting 24 → 30 adds judder. Compose at 1080x1920 with
`object-fit: cover`; 720p sources upscale acceptably.
