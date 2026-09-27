#!/usr/bin/env python3
"""Rank candidate wordings of one line against the audio (pocketsphinx forced alignment).

Use when transcribe.py's hypothesis is ambiguous ("them learn a guy to" = "then learn AI too"?).
Each candidate is force-aligned to the same time window; a higher score means the audio
fits that wording better. Only compare scores from the same window; gaps under ~0.005
are a tie (decide from frames and context, and prefer the simpler caption).

Usage:
  score_candidates.py <video> <start> <end> "then learn AI too | then learn a i too" "so learn AI too | so learn a i too"
  score_candidates.py <video> <start> <end> --file candidates.txt     # one candidate per line

Candidates use the phrases.txt convention: display text, optionally "| spoken tokens".
Pick a window from transcribe.py's word times with ~0.1 s margin on each side, and make it
cover the *whole* doubtful stretch: start at the first garbled word, not where you think the
line begins. A window starting 0.4 s late cut off "Besides" and ranked the wrong wording first.
"""
import argparse, os, re, subprocess, sys, tempfile, wave


def ensure_pocketsphinx():
    try:
        import pocketsphinx  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pocketsphinx"], check=True)


def tokens(cand):
    disp, _, spoken = cand.partition("|")
    return disp.strip(), re.sub(r"[^a-z' ]+", " ", (spoken.strip() or disp).lower()).split()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("start", type=float); ap.add_argument("end", type=float)
    ap.add_argument("candidates", nargs="*")
    ap.add_argument("--file")
    a = ap.parse_args()
    cands = list(a.candidates)
    if a.file:
        cands += [l.strip() for l in open(a.file) if l.strip() and not l.startswith("#")]
    if not cands:
        sys.exit(__doc__)
    ensure_pocketsphinx()
    from pocketsphinx import Decoder

    with tempfile.TemporaryDirectory() as td:
        wav = os.path.join(td, "seg.wav")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(a.start), "-to", str(a.end), "-i", a.video,
                        "-ac", "1", "-ar", "16000", "-af", "highpass=f=80,loudnorm", wav], check=True)
        with wave.open(wav, "rb") as w:
            data = w.readframes(w.getnframes())

    rows = []
    for c in cands:
        disp, toks = tokens(c)
        d = Decoder(samprate=16000, bestpath=False, logfn=os.devnull)
        oov = [t for t in toks if d.lookup_word(t) is None]
        if oov:
            rows.append((None, disp, "OOV: " + ", ".join(oov) + " (respell after '|')")); continue
        d.set_align_text(" ".join(toks))
        d.start_utt(); d.process_raw(data, full_utt=True); d.end_utt()
        h = d.hyp()
        rows.append((h.score if h else None, disp, "" if h else "could not align (wording doesn't fit the audio)"))
    rows.sort(key=lambda r: (1, 0) if r[0] is None else (0, -r[0]))
    print(f"window {a.start:.2f}-{a.end:.2f}s, best first")
    for score, disp, note in rows:
        print(f"  {'   n/a' if score is None else f'{score:8.4f}'}  {disp}  {note}")


if __name__ == "__main__":
    main()
