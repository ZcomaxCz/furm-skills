"""Složí hlasovou stopu epizody z replik a spočítá časování záběrů a titulky.

Použití: python3 build_voice.py <složka epizody>
Vstup: <ep>/ep02-doc.md (tabulka Voice sheet), <ep>/audio/*.mp3
Výstup: <ep>/build/voice.wav (mono 44.1 kHz), timing.json, subtitles.srt
"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np

SR = 44100
LEAD, GAP, TAIL, MIN_SHOT = 0.6, 0.4, 0.9, 6.0   # sekundy
THR = 10 ** (-42 / 20)                            # práh ticha −42 dBFS

ep = Path(sys.argv[1]); doc = next(ep.glob("ep*-doc.md")); out = ep / "build"; out.mkdir(exist_ok=True)
rows = []
for l in doc.read_text(encoding="utf-8").splitlines():
    if re.match(r"\| s\d\d_\d\d_", l):
        f, spk, text, _ = [x.strip().replace("\\|", "|") for x in re.split(r"(?<!\\)\|", l)[1:-1]]
        rows.append((f, int(f[1:3]), spk, text))

def load(p):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"])
    a = np.frombuffer(raw, np.float32)
    env = np.convolve(np.abs(a), np.ones(441) / 441, "same")   # 10ms obálka
    idx = np.where(env > THR)[0]
    if not len(idx): return a
    s, e = max(0, idx[0] - int(0.04 * SR)), min(len(a), idx[-1] + int(0.08 * SR))
    a = a[s:e].copy(); n = int(0.01 * SR)
    a[:n] *= np.linspace(0, 1, n); a[-n:] *= np.linspace(1, 0, n)
    return a

def ts(v): return f"{int(v//3600):02d}:{int(v%3600//60):02d}:{int(v%60):02d},{int(round(v%1*1000)) % 1000:03d}"
track, t, shots, subs = [], 0.0, {}, []
for k in sorted({r[1] for r in rows}):
    start = t; seg = [np.zeros(int(LEAD * SR), np.float32)]; tt = start + LEAD
    lines = [r for r in rows if r[1] == k]
    for i, (f, _, spk, text) in enumerate(lines):
        a = load(ep / "audio" / f"{f}.mp3"); d = len(a) / SR
        subs.append((tt, tt + d, spk, text)); seg.append(a); tt += d
        if i < len(lines) - 1: seg.append(np.zeros(int(GAP * SR), np.float32)); tt += GAP
    tt += TAIL; tt = max(tt, start + MIN_SHOT)
    shot = np.concatenate(seg); shot = np.pad(shot, (0, int(round((tt - start) * SR)) - len(shot)))
    track.append(shot); t = start + len(shot) / SR; shots[k] = (round(start, 3), round(t, 3))
voice = np.concatenate(track)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                "-c:a", "pcm_s16le", str(out / "voice.wav")], input=voice.tobytes(), check=True)
(out / "timing.json").write_text(json.dumps({"shots": shots, "lines": [dict(start=round(a, 3), end=round(b, 3), speaker=s, text=x) for a, b, s, x in subs]}, indent=1, ensure_ascii=False))
(out / "subtitles.srt").write_text("\n".join(f"{i}\n{ts(a)} --> {ts(b + 0.12)}\n{x}\n" for i, (a, b, s, x) in enumerate(subs, 1)), encoding="utf-8")
for k, (a, b) in shots.items(): print(f"shot {k:2d}: {a:7.3f} – {b:7.3f}  ({b-a:5.2f} s)")
print("total", round(t, 2), "s")
