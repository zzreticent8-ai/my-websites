#!/usr/bin/env python3
"""Force-align a corrected script to the audio and emit caption clips.

Usage: align_captions.py <video> <phrases.txt> <outdir> [--track 3] [--tail 0.25] [--end SECONDS] [--id-prefix c]

phrases.txt: one caption phrase per line, as it should appear on screen. When the
spoken form differs from the display form (acronyms, numbers), add the spoken
tokens after a "|":
    Explain AI without using | explain a i without using
    It costs $20 | it costs twenty dollars
Blank lines and lines starting with # are ignored.

Writes <outdir>/words.json, phrases.json and captions.html (timed .cap clips for
the root composition, all on one track, never overlapping). Out-of-vocabulary
words are reported so they can be respelled in the "|" part.
"""
import argparse, html, json, os, re, subprocess, sys, wave


def ensure_pocketsphinx():
    try:
        import pocketsphinx  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pocketsphinx"], check=True)


def read_phrases(path):
    out = []
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        disp, _, spoken = line.partition("|")
        disp = disp.strip()
        spoken = spoken.strip() or disp
        tokens = re.sub(r"[^a-z' ]+", " ", spoken.lower()).split()
        out.append({"display": disp, "tokens": tokens})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("phrases"); ap.add_argument("outdir")
    ap.add_argument("--track", type=int, default=3)
    ap.add_argument("--tail", type=float, default=0.25, help="hold after the last word of a phrase (s)")
    ap.add_argument("--end", type=float, help="clamp the last caption (e.g. the end-card start)")
    ap.add_argument("--id-prefix", default="c")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    ensure_pocketsphinx()
    from pocketsphinx import Decoder

    phrases = read_phrases(a.phrases)
    d = Decoder(samprate=16000, bestpath=False)
    oov = sorted({t for p in phrases for t in p["tokens"] if d.lookup_word(t) is None})
    if oov:
        sys.exit("Not in the pocketsphinx dictionary (respell after '|'): " + ", ".join(oov))

    wav = os.path.join(a.outdir, "audio16k.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-ac", "1", "-ar", "16000",
                    "-af", "highpass=f=80,loudnorm", wav], check=True)
    with wave.open(wav, "rb") as w:
        data = w.readframes(w.getnframes())

    d.set_align_text(" ".join(t for p in phrases for t in p["tokens"]))
    d.start_utt(); d.process_raw(data, full_utt=True); d.end_utt()
    words = [{"text": re.sub(r"\(\d+\)$", "", s.word), "start": round(s.start_frame / 100, 2),
              "end": round((s.end_frame + 1) / 100, 2)}
             for s in d.seg() if s.word not in ("<s>", "</s>", "<sil>")]
    n_tokens = sum(len(p["tokens"]) for p in phrases)
    if len(words) != n_tokens:
        sys.exit(f"Alignment returned {len(words)} words for {n_tokens} tokens; check the script.")

    i = 0
    for p in phrases:
        ws = words[i:i + len(p["tokens"])]
        i += len(p["tokens"])
        p["start"], p["last_word_end"] = ws[0]["start"], ws[-1]["end"]
    for k, p in enumerate(phrases):
        nxt = phrases[k + 1]["start"] if k + 1 < len(phrases) else None
        end = p["last_word_end"] + a.tail
        if nxt is None and a.end is not None:
            nxt = a.end
        p["end"] = round(min(end, nxt) if nxt is not None else end, 2)

    json.dump(words, open(os.path.join(a.outdir, "words.json"), "w"), indent=1)
    json.dump(phrases, open(os.path.join(a.outdir, "phrases.json"), "w"), indent=1)
    lines = []
    for k, p in enumerate(phrases, 1):
        dur = round(p["end"] - p["start"], 2)
        lines.append(f'<div id="{a.id_prefix}{k}" class="cap clip" data-start="{p["start"]}" '
                     f'data-duration="{dur}" data-track-index="{a.track}"><span>{html.escape(p["display"])}</span></div>')
    open(os.path.join(a.outdir, "captions.html"), "w").write("\n".join(lines) + "\n")
    for p in phrases:
        print(f'{p["start"]:6.2f}-{p["end"]:6.2f}  {p["display"]}')
    print("wrote", os.path.join(a.outdir, "captions.html"))


if __name__ == "__main__":
    main()
