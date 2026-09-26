# Beat library

Reusable overlay beats for captioned animated shorts. Each one is in
`assets/composition-template.html`; the ids below match that file. Choose beats by what
the line *means*, not to fill time. Every beat should change something the viewer
can see (a state, a number, a scale), not just appear.

## Safe zones (1080x1920)

- UI card band: y 186–330, x 110–970. Sits above most faces in medium shots, overlaps
  ear tips in close-ups (shrink to 0.92 during close-ups instead of moving it).
- Burned captions usually y 1530–1670; logo usually bottom-right ~x 790–1040, y 1600–1850.
- Reaction bursts: around the reactor's head, left x 120–320 / right x 780–960.
- Keep everything within x 90–990 for the platform UI.

## 1. State-machine notification card (`#inbox`, `#st1..#st3`)

One card, stacked states cross-faded in place. Planting → answer → scale-up is the arc.

- **st1 plant** (≈0.05 s): drop from above, `back.out(1.6)`, plus the notify SFX. Content is
  the problem arriving: "New lead · 'Hi! Is this still available?'", orange icon.
- **st2 answer** (on the line that answers it): old state goes up and out 0.25 s, new state
  comes up from below with `back.out(2)`, icon spins in, border flashes mint. Success SFX.
- **st3 escalate** (on the "really? all of them?" line): becomes a counter + progress bar.
  Count with an `onUpdate` tween (deterministic on seek) and `power1.in` so it
  accelerates. Ticks every ~0.3–0.4 s, not every increment.
- **Pulse** on the confirmation ("Yup"): counter scale 1→1.25 yoyo, border flash.
- **Exit** on the emotional line: `y:-260, opacity:0`, 0.3 s `power2.in`, starting ~0.05 s
  before the line so the card is gone by the time the burst peaks. Not `back.in` (see gotchas).

Other contents that fit the same card: payment received → "$ paid" → revenue counter;
booking request → "Booked ✓" → calendar filling; DM → auto-reply → inbox zero.

## 1b. Other card shapes that worked

- **Checklist chips** (plan / recipe): title + 3 chips with empty check circles. Each
  chip turns mint with a check and a 0.1 s scale pop on its own spoken noun, plus a
  tick SFX (0.2). Chips use short nouns ("Customers", "Systems", "Automation"), not
  the caption line.
- **Jargon strike-through** (hook for "without complicated words"): coral chips
  ("LLM", "neural net", "tokens") get a red line drawn across (`scaleX` 0→1, 0.14 s,
  0.16 s stagger) and dim to 45 %.
- **Meter vs capacity** (warning): an orders bar races (`scaleX`, `power2.in`) past a
  white capacity marker while a counter climbs; an "overloaded" tag pops in coral. On
  the answer line, a mint capacity fill grows under it and the marker fades.
- **Countdown** (work gets faster): a "min" counter falling 60 → 2 with `power2.in` while
  a bar fills orange→mint; the number turns mint and pulses on "faster".
- **Timer fast-forward** (see §4b): m:ss → h:mm:ss on "an hour ago".

## 2. Camera moves (`#cam`, non-timed wrapper around the video)

- **Punch-in** on a surprised line: scale 1→1.08 over 0.16 s `power3.out`, 4-step x
  shake of 8 px (`yoyo, repeat:3` ends at 0), settle to 1.04, slow drift to 1.07.
- **Reset on the cut** back to the other character with `tl.set` at the scene-cut time.
- **Slow push** through a reaction shot: 1→1.06 linear across the shot.
- Keep scale ≤1.08 while burned captions/logo are on screen, or they crop. Captions and
  the logo bug that *you* add live outside `#cam`, so punch-ins can go to ~1.12.
- **Punch-in toward a character in a wide shot:** set `transformOrigin` to that
  character's head for the shot ("Easy." → origin on the cat at (780,1000)).

## 3. Reaction marks and bursts

- **Surprise marks** (`#wow`): four short rounded strokes at the reactor's temples,
  `scaleY` from 0 with `back.out(3)`, 0.03 s stagger, fade at +0.55 s. Rise SFX.
- **Heart burst** (`#hearts`): 3–4 SVG hearts in palette colours, scale from 0 with
  rotation, float up 90 px, fade after ~0.7 s. Quiet notify pop.

## 4a. Callback push-in → end card (a prop with a message exists)

Find a prop in the last wide shot that carries a message (sign, screen, poster).

- Set `transformOrigin` to the prop centre at the cut, drift 1→1.08, then push to ~3.4x
  over 0.58 s `power2.in` **while translating** the prop centre to where the end-card
  element will sit: `x = targetX - propX`, `y = targetY - propY`. Scale around an
  origin keeps that point fixed; without the translate the prop stays in a corner.
- Whoosh starts ~0.45 s before the cut so its swell peaks on the cut.
- Time the push to finish where the end card takes over: at `T.cut` for a hard cut,
  at `T.cut + 0.1` when the card cross-fades in (the prop must be in place mid-fade).
  Check frames at `T.cut - 0.05`, `T.cut + 0.03` and `T.cut + 0.1`: the real prop should
  sit under its end-card version.
- A held object works as the prop too: the book in her arms became the end card's
  book cover ("The next chapter: Learn AI too"), with a small `rotationY` settle.
- The end card's version of the prop enters at a scale matching the zoomed prop's
  on-screen size (≈1.1), not a dramatic 1.9, so the handoff reads as one move.

## 4b. Object callback (no usable prop)

Used on the beach reel: the last wide shot was open sand and sea with nothing to zoom into.
The card planted at 0.05 s ("Out of office") is the object the story broke; the end card
shows it fixed.

- Camera: `transformOrigin` on the characters' midpoint, drift 1→1.1, then 1.1→1.5
  `power2.in` until `T.cut + 0.3`. Keep the video clip running 0.3 s past `T.cut`.
- End card fades in over those 0.3 s (`tl.from('#cta', {opacity:0, duration:0.3})`) so
  the push shows through. Dialogue audio still ends at `T.cut`.
- The hero card drops in (`y:-300`, `back.out(1.5)`), then its resolved state lands on its
  own beat: a toggle switching on (track colour tween + knob `x` from -60, tick SFX), a
  check, or "on autopilot ✓". Question, pill and logo follow as in §5.
- Timer variant of the escalation state: format seconds as m:ss / h:mm:ss, count slowly
  and linearly on the innocent line ("just one quick look": 0→4 s), then fast-forward
  `power2.in` on the callout ("an hour ago": →1:02:37), with ticks that speed up.

## 5. LED sign end card (`#cta`)

Dark radial background from the footage palette, then:
- LED panel: bezel + dark screen + amber Silkscreen text with glow and a light dot
  mask (`radial-gradient` transparent 2.2 px → 40 % dark 3.1 px, 7 px grid). Heavier
  masks make the text unreadable. Use `white-space:nowrap` and size so the longest line
  fits (~0.8 em per Silkscreen char). Lines flicker on (opacity yoyo ×3) one after another.
- The creator's own CTA question, word-staggered up, one keyword in accent colour.
- Mint pill "Comment below ↓" pops in with `back.out(2.2)` + notify SFX; arrow bobs.
- Cropped original logo scales in last. Hold ≥1.5 s on the finished card.

## SFX levels that sat right (files normalized to -1 dBFS)

| cue | data-volume | in-mix peak after mastering |
|---|---|---|
| notify / pill pop | 0.28 (0.2 for secondary pops) | ≈ -5 dBFS (sums with speech) |
| success | 0.28 | ≈ -2 dBFS with speech |
| rise | 0.22 | ≈ -12 |
| tick | 0.11 | ≈ -17 |
| whoosh | 0.28 | ≈ -12 |
| bell | 0.4 | ≈ -9 |
| pad (end card bed) | 0.09 | ≈ -24 |

Dialogue: the source's own audio, trimmed to the cut and faded over the last 0.35 s.
