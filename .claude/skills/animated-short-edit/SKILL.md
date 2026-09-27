---
name: animated-short-edit
description: Polish a short vertical AI-animated or cartoon skit (Reels/Shorts/TikTok, usually 8–30 s) into a finished reel, whether it already has burned-in captions, a corner logo and a plain CTA end screen, or is raw with none of those (captions from an offline transcript, logo and end card get added), using the HyperFrames student kit — story overlays that make the invisible idea visible (notification cards, counters), camera punch-ins on reactions, reaction bursts, a callback push-in into an animated end card, synthesized SFX, loudness mastering and frame-level verification. Use this whenever the user uploads or points to a short character/cartoon/AI-generated video and asks to edit it, "make it pop", add captions or motion graphics, improve the hook or ending, redo the CTA, or "edit it like the bus video", even if they don't name HyperFrames or this skill.
---

# Animated short edit

Turns an already-captioned short skit into a reel with a visible story layer, sound
design and a designed end card, without re-cutting the dialogue. Built from the
"checking leads on the bus" edit (woman + cat, AI answering leads); that project is the
worked example in `assets/composition-template.html`.

The source footage is usually finished animation: the captions and logo are burned in
and the dialogue is tight. The job is **adding a layer the viewer can follow muted**,
not re-editing performance. Only trim dead holds (silent tails, static end screens).

## 0. Setup (once per session)

```bash
bash .claude/skills/animated-short-edit/scripts/setup.sh [kit_dir]   # default: $SCRATCH/hyperframes-student-kit
```

It installs ffmpeg if missing, clones `nateherkai/hyperframes-student-kit`, runs `npm ci`,
and prints the `export PRODUCER_HEADLESS_SHELL_PATH=…` line that HyperFrames needs to
find Chromium. Put that export in front of every `npx hyperframes render`.
Read the kit's `CLAUDE.md` and `.claude/skills/short-form-edit/SKILL.md` once; this skill
is a specialisation of that workflow and defers to its rules on timelines and media.

## 1. Analyze the footage

```bash
python3 .claude/skills/animated-short-edit/scripts/analyze.py <video> <outdir>
```

Writes `analysis.json` (streams, scene cuts, caption-change times, speech gaps,
loudness) plus `contact.jpg` and `events.jpg` (a labelled frame at every detected event).
Look at both images, then establish:

- **Captions burned in?** If no frame shows a caption box (caption changes only echo
  cuts or fire during camera motion), follow `references/no-captions.md`: rough
  transcript with `scripts/transcribe.py`, correct it (rank doubtful lines with
  `scripts/score_candidates.py`), `scripts/align_captions.py` for
  word-timed caption clips, series logo bug, a written CTA. The rest of this workflow
  is unchanged.

- **Dialogue + timing map.** Read each caption off `events.jpg` and pair it with its
  change time. That map is your word-timing source when no ASR is available (Hugging
  Face / OpenAI model hosts are often blocked; ElevenLabs needs a key). If the caption
  box sits somewhere unusual, pass `--caption-box x,y,w,h`. Captions often lag shot cuts
  by ~0.25 s, so anchor graphics to caption changes, camera moves to scene cuts.
- **Who speaks each line** and the one-sentence story (setup → doubt → proof → reaction).
- **The invisible thing** the dialogue talks about but never shows (the AI replying,
  money arriving, a booking landing). The overlay layer exists to show it.
- **Keep-out zones:** faces in each shot, the burned caption band, the logo corner.
- **Callback props:** signs, screens, notebooks, cups with text in the world. A prop
  that already carries a message (a bus sign reading "NEXT STOP: NEW OPPORTUNITIES")
  makes the best bridge into the end card. If the last shot has no such prop (open
  beach, plain room), the overlay card itself is the callback: it returns on the end
  card in its fulfilled state (see beat-library §4b).
- **Dead holds:** silent wide shots and static black CTA cards (`silence_start` near
  the end, black frames). These are what you trim or replace.
- **Brand assets:** crop the logo from a clean frame (black end card is ideal) — never
  redraw it. `ffmpeg -ss T -i v.mp4 -frames:v 1 -vf crop=W:H:X:Y logo-crop.png`, then
  `-vf colorkey=0x000000:0.06:0.08,format=rgba logo.png` for transparency. View the crop.
  For Her Startup Ideas videos the series logo is bundled as
  `assets/her-startup-ideas-logo.png`.

## 2. Plan (write before HTML)

Create the project: `cd <kit> && npm run new-video -- <slug>`, copy the source to
`assets/source.mp4`, and set `meta.json` to `1080x1920`, `id: "main"`, and `fps` to the
source frame rate (pass the same `--fps` to every render; 24 → 30 adds judder).

Write `DESIGN.md` with a palette **sampled from the footage** (seat fabric, character
colours, caption colour) so overlays look native, 1–2 fonts, and a "what not to do"
list (don't restate captions, don't cover faces/captions/logo). Then a beat sheet:

| time | anchor (caption/cut) | beat | overlay action | SFX |
|---|---|---|---|---|

Pick beats from `references/beat-library.md`. The default arc that worked:

1. **Hook 0–2 s** — a UI element drops in at ~0.05 s, planting the open question
   ("New lead: Is this still available?"). First frame stays the clean source frame.
2. **Answer** — on the line that answers it, the element *changes state*
   (lead → "AI replied ✓"). Show the outcome, don't caption it.
3. **Escalation** — on the "wait, really?" line, a punch-in on the reactor and
   the element scales up the claim (single reply → a counter climbing).
4. **Confirmation** — pulse/check on the "yes" line.
5. **Reaction** — burst (hearts, sparks) on the emotional line; UI tucks away *fast*
   (0.3 s `power2.in`, starting ~0.05 s before the line) so the burst owns the frame.
6. **Callback transition** — push the camera into a world prop that becomes the end card,
   or, with no prop, push into the characters and cross-fade to an end card where the
   hook's card drops back in, resolved (toggle on, check, "on autopilot").
7. **End card 3–3.5 s** — keep the creator's original CTA wording, add a pill button and
   the cropped logo. Enough time to read; original black cards are usually too short.

Give every card state at least ~1 s on screen; if two states crowd one line, switch
earlier or hold the last state into the next shot instead of cutting it short. When
several items share one caption ("More customers, better systems"), estimate each
item's spoken time (~0.25 s per syllable) or align it with `align_captions.py`.

Keep the illustrative content plausible and label it as illustrative in VERIFY.md (the
counter number and message text are invented).

## 3. Build

- Start from `assets/composition-template.html`: copy it to the project's `index.html`
  and edit the `T` timing object, texts, colours and the audio list. Every tween reads
  its time from `T`, so retiming a new video is mostly editing that object.
- Fonts: `bash scripts/fonts.sh <project>/assets "Baloo+2:wght@600;800" "Silkscreen:wght@400;700"`
  (downloads woff2 locally; the render must not depend on CDNs).
- Dialogue audio: `ffmpeg -i assets/source.mp4 -t <cut_end> -vn -af "afade=t=out:st=<cut_end-0.35>:d=0.35" -ar 44100 -ac 2 assets/dialogue.wav`.
- SFX: `bash scripts/make_sfx.sh <project>/assets` synthesizes notify, success, tick,
  rise, whoosh, bell and pad, all normalized to -1 dBFS, so `data-volume` alone sets the
  level. Starting volumes that sat right under dialogue are in `references/beat-library.md`.
- If the user wants generated images/B-roll, Kie.ai is the kit's provider: it needs
  `KIE_API_KEY` in the environment (cloud env settings → Edit → environment variables)
  and `api.kie.ai` allowed in network access. Never ask for the key in chat. The default
  arc needs no generated assets.

## 4. Check, render, look

```bash
cd <project> && npx hyperframes lint          # must be 0 errors (rules in gotchas.md)
node ../../scripts/preflight.mjs .            # see gotcha about root data-start
<export line from setup> npx hyperframes render --quality draft --output renders/draft-v1.mp4
bash .claude/skills/animated-short-edit/scripts/keyframes.sh renders/draft-v1.mp4 /tmp/sheet.jpg 0.3 1.9 3.35 5 6.9 7.7 9.4 9.55 10.4 12.7
```

Pick keyframe times at every beat and on both sides of every transition. Look for:
overlays touching faces/captions/logo, text overflow or wrapping (LED fonts wrap
easily), dim text, the push-in target drifting off-centre, and a jump in scale between
the zoomed prop and the end card (the push must finish as the card takes over; check
frames just before, at and just after `T.cut`), and effects positioned for one shot that
are still on screen after its cut (check a frame just after every cut). Crop full-res regions to check small UI text.
Read `references/gotchas.md` before the first render — it lists the failures already hit.

## 5. Final

```bash
npx hyperframes render --quality high --output renders/render-vN.mp4
bash .claude/skills/animated-short-edit/scripts/master.sh renders/render-vN.mp4 renders/<slug>-final.mp4
bash .claude/skills/animated-short-edit/scripts/sfx_levels.sh renders/<slug>-final.mp4 0.12:0.2 1.72:0.25 9.58:0.5
```

`master.sh` does two-pass linear loudnorm to -16 LUFS / -1.5 dBTP, trims audio to video
length and prints the hash. `sfx_levels.sh` prints peak level in each window; SFX that
read below about -30 dBFS are inaudible on a phone.

Write `VERIFY.md` in the project: final path + sha256, edit decisions in source time,
the timing map, lint/preflight results, loudness, SFX peaks, and honest limits (timing
from captions not ASR; audio checked by measurement, not listening; illustrative
numbers). Send the final MP4 to the user with SendUserFile and summarise the beats.
Personal footage and renders stay out of git unless the user asks.
