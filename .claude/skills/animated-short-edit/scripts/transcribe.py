#!/usr/bin/env python3
"""Rough offline transcript with pocketsphinx (bundled en-us model, installs from PyPI).

Use when the video has no burned captions and no ASR service is reachable. The
hypothesis is rough; read it next to the frames, write the corrected script as a
phrases file, then run align_captions.py for accurate timings.

Usage: transcribe.py <video> <outdir>
Writes <outdir>/audio16k.wav, hyp.txt, hyp-words.json
"""
import json, os, subprocess, sys, wave


def ensure_pocketsphinx():
    try:
        import pocketsphinx  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "pocketsphinx"], check=True)


def prep_audio(video, outdir):
    wav = os.path.join(outdir, "audio16k.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-ac", "1", "-ar", "16000",
                    "-af", "highpass=f=80,loudnorm", wav], check=True)
    return wav


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    video, outdir = sys.argv[1:]
    os.makedirs(outdir, exist_ok=True)
    ensure_pocketsphinx()
    from pocketsphinx import Decoder

    wav = prep_audio(video, outdir)
    with wave.open(wav, "rb") as w:
        data = w.readframes(w.getnframes())
    d = Decoder(samprate=16000)
    d.start_utt(); d.process_raw(data, full_utt=True); d.end_utt()
    hyp = d.hyp().hypstr if d.hyp() else ""
    words = [{"text": s.word, "start": round(s.start_frame / 100, 2), "end": round((s.end_frame + 1) / 100, 2)}
             for s in d.seg() if s.word not in ("<s>", "</s>", "<sil>", "[NOISE]")]
    open(os.path.join(outdir, "hyp.txt"), "w").write(hyp + "\n")
    json.dump(words, open(os.path.join(outdir, "hyp-words.json"), "w"), indent=1)
    print("HYPOTHESIS:", hyp)
    for x in words:
        print(f'{x["start"]:6.2f}-{x["end"]:6.2f} {x["text"]}')


if __name__ == "__main__":
    main()
