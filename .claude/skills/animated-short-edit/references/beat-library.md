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
- **When the defaults are taken, move them for the whole video:**
  - Head in the top band (long full-body wide, e.g. mopping): compact card top-right over
    background (x 560–1050, y 230, ~490×210, `transform-origin: 100% 0`), grid rows
    with a label column wide enough for the longest label (176 px for "Important work" at 24 px).
  - Subject, mop or prop in the caption band: captions low-left (`top:1700–1720px`,
    `justify-content:flex-start; padding-left:60–90px; max-width:720px`), which stays clear
    of the logo corner (x 785+). For one shot only, add a `.cap.low` class to just those captions.
    The cat's sock in its basket close-ups (three shots) sent the laundry captions low-left
    for the whole video.
- **One shot only:** when a face sits in the card band for a single shot (her head behind
  the walking cat), shrink and slide the card for that shot (`scale: 0.7, x: 150`, 0.3 s
  `power2.out` at the cut) and restore it at the next cut. For cat close-ups whose ear tips
  reach y≈265, use `scale: 0.86, y: -40` instead of the usual 0.88 / −24.

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

- **Select-all → reset → split chips** ("automate everything?"): four task chips all go amber
  on "everything", the card shakes and they reset on "No.", then the repetitive ones turn
  mint ✓ and one stays human (pink ♥). Swap the title in place (two stacked titles,
  cross-fade) when the advice reframes the question.
- **Two-bar split** (time budget): "Small tasks" vs "Important work" bars fill on the
  key word, the small bar swells while the important one collapses to coral with a falling
  tone (`sfx-fall`). The end card shows the same bars flipped (object callback).

- **Idea pots** (plant everything vs focus): five SVG pots with labels drop in staggered
  0.1 s with ticks while a "Time each" counter falls 100% → 20%. Three wilt on the "won't
  grow" line (green sprout and drooping coral sprout stacked, cross-faded, `svgOrigin` at
  the soil). On "focus" the wilted ones drop out, the two survivors slide together
  (`x`, scale 1.12) and bloom (`back.out(3)`), and time goes up to 50%.
- **Jagged → smooth line** (the roller-coaster business): a coral up-and-down sparkline draws
  on (`pathLength=1`, dashoffset 1→0) on "roller coaster". Later the same card redraws a smooth
  mint climb over a 22 % ghost of the jagged one ("enjoying the ride").
- **Toggle + auto counter** ("would automation help?" → "imagine…"): a switch sits off with
  "Would it help?". On the answer the knob slides (`x`), the track and icon turn mint, the gear
  spins, the subtitle cross-fades to "Leads on autopilot", and a "+N new leads" counter
  climbs by itself.
- **Hours needed vs capacity**: each spoken task ("answer / schedule / follow up everyone")
  lights its chip and bumps an hours counter (8 → 22 → 38 → 56) against "you have 40h"; the
  number turns coral past 40 and an "overloaded" stamp lands with a card shake.
- **Stamp tag**: `fromTo(tag, {opacity:0, scale:1.8, rotation:-12}, {opacity:1, scale:1,
  rotation:-4, back.out(2.5)})` for "100% manual", "too high", "overloaded".
- **Two-column verdict** ("not a customer problem → a capacity problem"): Customers ✓ in
  mint next to a dimmed Capacity "?". On the realization the badge turns coral with ✗ and the
  word gets a hand-drawn ring. Size the ring's own box to the *word*, not the column.
- **Scanned items** (checkout theme): "Done by hand" chips slide in on scanner-beep ticks,
  one per spoken word, then a coral "+24 more" pops on "A lot.".
- **Icon swap**: stack two SVGs in the icon tile (person and robot) and cross-fade them on
  the word, with a title swap the same way ("Your hours" → "Robot work · paid by you").

- **Version flip** ("so a plan can change too?"): stacked version labels `v1` → `v2?` (gold)
  → `v2 ✓` (mint) on the confirmation, with the subtitle swapping "a draft, not a contract"
  → "changes with the market". The end card shows v1 · v2 · **v3 ✓** chips.
- **Sunk-cost counter**: "Time invested · 0 → 6 months" with a "sunk cost" stamp, on "I spent
  months creating it".
- **Chips that each change**: each chip turns sky blue with its ↻ icon spinning 360° on its
  own word ("The weather changes / you change / the market changes").
- **Repeat counter** ("every week"): ×1 → ×52 "times a year".
- **Manual → automated chips**: stack two icons in each chip (coral ↻ and a check), then flip
  them one by one 0.1 s apart on "automate" as the hours count down to 0.
- **Build vs forget split**: two columns. "Build it" lights mint on its word; on "forget it"
  the other side goes coral, its bulb dims to 25 % and "memory 100%" drains to 5%.
- **Typing note**: a Notes card types the idea in Caveat, one `<span>` per character
  (`opacity` 0→1, stagger ~0.04 s), with an inline caret hidden until typing ends and then
  blinking. A Save button sits beside it, and a coral "why?" bubble pops on the doubting
  line. Don't reveal text with a cover rectangle: on a translucent card the cover reads as a box.

- **Ballast bags** (tasks weighing a balloon down): five SVG sandbags in absolute slots
  ~102 px apart, labelled at 17 px, drop onto the card on "carrying everything" while an
  altitude counter sinks (1,200 → 120 ft). On the reply naming them, each bag falls out
  through the card's bottom edge (`y: 150, rotation: 25, opacity: 0`, 0.45 s `power2.in`; the
  card's `overflow:hidden` clips it) with a soft whoosh (0.2), and the altitude climbs. The bag
  that stays turns mint (`fill` tween on its body path).
- **Everything fades but one** ("if my business disappeared, what would I need?"): the chips
  shrink to 0.85 and fade to 18 % in a 0.1 s stagger, and the survivor lights mint on the question.
- **Shield ring**: a `pathLength` circle draws around the icon tile on "protect", and the
  system chips lock on staggered 0.15 s. Size the ring's radius to the tile (r ≈ tile/2 + 4) or
  the rounded corners poke through.
- **Badge pop** ("I'm a professional"): a gold radial-gradient "PRO" disc with a soft glow,
  `scale 0.3 → 1, rotation -30 → 0`, `back.out(3)`, plus a rise SFX. It returns on the end card's
  hero corner.

## 2. Camera moves (`#cam`, non-timed wrapper around the video)

- **Punch-in** on a surprised line: scale 1→1.08 over 0.16 s `power3.out`, 4-step x
  shake of 8 px (`yoyo, repeat:3` ends at 0), settle to 1.04, slow drift to 1.07.
- **Reset on the cut** back to the other character with `tl.set` at the scene-cut time.
- **Weight and lift**: a slow `y: +14` sag across "carrying everything" makes the frame feel
  heavy, and `y: -16` with the drift in the payoff shot reads as rising. Reset `y` at the next cut.
- **Repeated shots**: a small helper keeps the camera block short:
  `const shot = (o, t0, t1, s) => { tl.set('#cam', {scale: 1, x: 0, transformOrigin: …}, t0); tl.to('#cam', {scale: s, duration: t1 - t0, ease: 'none'}, t0); }`.
- **Source camera already moving** (a pan from a close-up into a two-shot): keep `#cam` to
  a gentle 1→1.04 drift there; a punch-in would fight the move.
- **Ride rumble** (roller coaster, vehicles): `tl.to('#cam', {y: 6, duration: 0.06, yoyo: true,
  repeat: 11})`. An odd repeat count ends back at 0. Start at scale ≥1.04 so edges stay covered.
- **Slow push** through a reaction shot: 1→1.06 linear across the shot.
- Keep scale ≤1.08 while burned captions/logo are on screen, or they crop. Captions and
  the logo bug that *you* add live outside `#cam`, so punch-ins can go to ~1.12.
- **Punch-in toward a character in a wide shot:** set `transformOrigin` to that
  character's head for the shot ("Easy." → origin on the cat at (780,1000)).

## 3. Reaction marks and bursts

- **Sweat drop** (embarrassed / "uncomfortably accurate"): a ~80×116 blue SVG teardrop with
  a navy outline beside the head plus two short dash lines; pops in with `back.out(3)`, then
  slides down 60 px over 0.9 s. A cheap way to land a self-aware punchline.

- **Question mark** ("How?"): a 130 px gold "?" with a dark outline (four text-shadows) beside
  the asker's head, popping in with `back.out(3)`, wiggling with rotation yoyo and gone in 1 s.
- **Surprise marks** (`#wow`): four short rounded strokes at the reactor's temples,
  `scaleY` from 0 with `back.out(3)`, 0.03 s stagger, fade at +0.55 s. Rise SFX.
- **Bursts belong to their shot.** Place sparkles/hearts for the shot they appear in and
  finish them by that shot's cut (fade at `cut - 0.1`, hard kill at the cut). A burst
  positioned around the cat's close-up face drifted into the next wide shot's empty sky.
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

- **Push math (translate + scale).** With `transformOrigin` on the prop at (px, py) and a
  translate to a target (tx, ty), the frame edge shows unless the scale covers it:
  bottom needs `s ≥ (1920 − ty) / (1920 − py)`, top `s ≥ ty / py`, and likewise for x with
  1080. Moving the coworking cup from y 1525 to 600 at 2.2× left a black band; the fix was
  to put the end-card question *above* the cup so its target dropped to y 883 (then 2.7×
  covers it) and let the end-card cup enter at ~1.25× to match.
- **Hold the end-card prop over the zoomed prop until the push lands.** The end-card version
  starts at the zoomed prop's size and position and only settles after `T.cut + 0.1`:
  `tl.from('#page', { y: 765, scale: 1.39, duration: 0.6, ease: 'power3.inOut' }, T.cut + 0.1)`.
  `from()` renders its start state immediately, so the page sits on the real notebook through
  the cross-fade. Started at `T.cut`, it had already risen 200 px above the notebook by the
  first end-card frame.
- **A prop low in the frame needs a low target.** The garden notebook sat at y 1780; centring
  it would need ~5.7×. With target (540, 1600) 2.4× covers the edges, the end-card page enters
  there at the matching size (1.39×) and then lifts into its layout slot. The lift reads as
  one move.
- **A prop at the side edge** (checkout screen at x≈985) needs `(1080 − tx)/(1080 − px)`,
  ~6× to centre it. Above ~3× the zoom turns to mush: use §4c instead.
- **Measure the target from a render,** not from layout arithmetic: render once, read the
  end-card prop's centre off a frame, set `T.propTarget`, re-check the handoff frames.
- Text props work well: the cup's own words (Focus / Plan / Automate / Grow) were redrawn
  on the end card with the key word circled (SVG path, `pathLength=1`, dashoffset 1→0)
  and handwritten notes (Caveat). Keep notes inside x 90–990; use two-line notes.

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

## 4c. Prop redrawn as the end-card hero (prop unreachable by a push)

When the prop is too close to an edge for §4a, push on the characters as in §4b and make
the end card's hero a clean redraw of the prop with the lesson applied:
- Self-checkout screen: dark bezel, teal glass, "THANK YOU!" flickers (opacity yoyo ×3), then
  swaps to "BORING STUFF / AUTOMATED ✓" (stacked lines, cross-fade). A receipt prints
  underneath (Space Mono, zig-zag `clip-path` bottom), with lines landing 0.14 s apart and ticks:
  Invoices AUTO / Emails AUTO / Scheduling AUTO / Robot work $0.
- Wall sign (GOOD VIBES, reachable at 2×, so it was pushed into as well): the redraw hangs on
  a string, swings once (`rotation -3→0`, `elastic.out(1,0.4)`, origin above the sign), and
  gets a handwritten Caveat addition in coral: "+ good systems".
- Notebook: "Grow what works" with the card's ideas, the wilted ones struck out
  (`scaleX` 0→1 coral bar) and the survivors circled.
- Clothesline (laundry): a sagging rope path with three mint T-shirt SVGs (Invoices /
  Follow-ups / Reports, "AUTO ✓") and a coral sock ("Laundry · still yours"). They drop onto
  pegs 0.14 s apart (`y: -420`, `back.out(1.6)`) and settle with an elastic swing. Put the labels
  *under* the clothes; inside a 230 px shirt they clip.

- Hot-air balloon: a striped SVG balloon rises from below (`y: 360`, 0.9 s `power2.out`) and
  bobs, while three labelled sandbags appear under the basket and fall off-screen in 0.9 s.
  Hide them (`tl.set opacity 0`) before the question animates in, or they fall through the
  text. Only a mint "Strategy ✓" tag stays, with an altitude badge beside it.
- Embers: eight glowing dots rising 2,000 px over 3.2 s behind the hero on a fire-glow radial
  background.

Decorations that drift across an end card (blowing leaves, a shooting star drawn with a
`pathLength` dash) go in a layer *below* the content: give `.scene-content` `z-index: 1`.
Draw leaves as a simple oval with a vein; a spiky maple path reads as an asterisk at 90 px.

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
| fall (value collapsing) | 0.22 | ≈ -4 with speech |
| whoosh | 0.28 | ≈ -12 |
| bell | 0.4 | ≈ -9 |
| pad (end card bed) | 0.09 | ≈ -24 |

Dialogue: the source's own audio, trimmed to the cut and faded over the last 0.35 s.
