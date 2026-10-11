#!/usr/bin/env python3
"""Analyze a short captioned video for editing.

Usage: analyze.py <video> <outdir> [--caption-box x,y,w,h] [--threshold 6]

Writes to <outdir>:
  analysis.json  streams, scene cuts, caption-change times, speech gaps, loudness
  contact.jpg    overview grid (1.5 fps)
  events.jpg     labelled full frames at every scene cut / caption change
"""
import argparse, json, os, re, subprocess
import numpy as np


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(video):
    out = run(["ffprobe", "-v", "error", "-show_entries",
               "format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
               "-of", "json", video]).stdout
    return json.loads(out)


def scene_cuts(video, thresh=0.25):
    err = run(["ffmpeg", "-hide_banner", "-i", video, "-vf",
               f"select='gt(scene,{thresh})',showinfo", "-f", "null", "-"]).stderr
    return [round(float(t), 3) for t in re.findall(r"pts_time:([0-9.]+)", err)]


def silences(video, noise="-30dB", dur=0.12):
    err = run(["ffmpeg", "-hide_banner", "-i", video, "-af",
               f"silencedetect=n={noise}:d={dur}", "-f", "null", "-"]).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", err)]
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", err)]
    return [{"start": round(s, 3), "end": round(e, 3) if i < len(ends) else None}
            for i, (s, e) in enumerate(zip(starts, ends + [None] * len(starts)))]


def loudness(video):
    err = run(["ffmpeg", "-hide_banner", "-i", video, "-af", "ebur128=peak=true",
               "-f", "null", "-"]).stderr
    i = re.findall(r"I:\s+(-?[0-9.]+) LUFS", err)
    p = re.findall(r"Peak:\s+(-?[0-9.]+) dBFS", err)
    return {"integrated_lufs": float(i[-1]) if i else None,
            "true_peak_dbfs": float(p[-1]) if p else None}


def caption_changes(video, box, fps, thresh):
    x, y, w, h = box
    sw, sh = 180, max(8, int(180 * h / w))
    data = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vf",
                           f"crop={w}:{h}:{x}:{y},scale={sw}:{sh},format=gray",
                           "-f", "rawvideo", "-"], capture_output=True).stdout
    frames = np.frombuffer(data, dtype=np.uint8).reshape(-1, sh, sw).astype(float)
    events, last = [], -1.0
    for i in range(1, len(frames)):
        d = np.abs(frames[i] - frames[i - 1]).mean()
        t = i / fps
        if d > thresh and t - last > 0.1:  # merge fade frames into one event
            events.append({"t": round(t, 3), "diff": round(float(d), 1)})
            last = t
    return events


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("outdir")
    ap.add_argument("--caption-box", help="x,y,w,h in source pixels (default: lower band)")
    ap.add_argument("--threshold", type=float, default=6.0)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)

    info = probe(a.video)
    v = next(s for s in info["streams"] if s["codec_type"] == "video")
    W, H = v["width"], v["height"]
    num, den = map(int, v["r_frame_rate"].split("/"))
    fps = num / den
    dur = float(info["format"]["duration"])
    box = (tuple(int(n) for n in a.caption_box.split(",")) if a.caption_box
           else (int(W * 0.083), int(H * 0.77), int(W * 0.833), int(H * 0.115)))

    cuts = scene_cuts(a.video)
    caps = caption_changes(a.video, box, fps, a.threshold)
    result = {
        "video": os.path.abspath(a.video), "width": W, "height": H, "fps": fps,
        "duration": round(dur, 3), "streams": info["streams"],
        "caption_box": box, "scene_cuts": cuts, "caption_changes": caps,
        "silences_-30dB": silences(a.video), "loudness": loudness(a.video),
    }
    with open(os.path.join(a.outdir, "analysis.json"), "w") as f:
        json.dump(result, f, indent=1)

    run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-vf",
         "fps=1.5,scale=270:-1,tile=6x4", "-frames:v", "1",
         os.path.join(a.outdir, "contact.jpg")])

    times = sorted({0.05, *cuts, *[c["t"] + 0.1 for c in caps], max(0, dur - 0.3)})
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(["bash", os.path.join(here, "keyframes.sh"), a.video,
                    os.path.join(a.outdir, "events.jpg"), *[f"{t:.2f}" for t in times]])

    print(f"{W}x{H} @ {fps:g} fps, {dur:.2f}s, loudness {result['loudness']}")
    print("scene cuts:", cuts)
    print("caption changes:", [c["t"] for c in caps])
    print("silences:", result["silences_-30dB"])
    print("wrote", a.outdir)


if __name__ == "__main__":
    main()
