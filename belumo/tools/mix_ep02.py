"""Mix Ep2: hlas (build/voice.wav) + hudba + SFX z sfx/ -> build/mix.wav
Každý zdroj se nejdřív srovná na −23 LUFS, pak dostane relativní hlasitost níže.
Vendor (telefonní nahrávka) dostane pásmový filtr 300–3400 Hz."""
import json, subprocess
from pathlib import Path
EP = Path(__file__).resolve().parent.parent / "ep02-first-contact"; B = EP / "build"; S = EP / "sfx"; N = B / "norm"; N.mkdir(exist_ok=True)
T = json.loads((B / "timing.json").read_text()); END = T["shots"]["13"][1]
ven = [l for l in T["lines"] if l["speaker"] == "Vendor"][0]
# (soubor, začátek s, délka s nebo None, dB vůči −23 LUFS, fade in, fade out, smyčka)
CUES = [
 ("room_tone", 8.2, 150.4, -12, 2, 2, True),
 ("saucer_hum", 0.0, 8.6, -4, 1.0, 1.5, False),
 ("music_main", 0.3, 88.5, -10, 1.5, 3.0, True),
 ("music_tension", 88.0, 53.4, -10, 2.0, 2.0, False),
 ("music_outro", 155.0, 15.8, -8, 2.5, 2.0, False),
 ("transmission", 8.3, None, -2, 0, 0.3, False),
 ("glyphs", 19.3, None, -6, 0.5, 1.0, False),
 ("door_burst", 33.1, None, 0, 0, 0.2, False),
 ("desk_bell", 43.0, None, -2, 0, 0.3, False),
 ("cube_hum", 57.7, 19.0, -8, 1.5, 2.0, True),
 ("hologram", 76.7, None, -4, 0.2, 0.8, False),
 ("paper_stack", 109.0, None, 0, 0, 0.3, False),
 ("printer_error", 121.0, None, -2, 0, 0.3, False),
 ("countdown_tick", 123.9, 6.5, -8, 0.3, 1.0, False),
 ("phone_pickup", 130.7, None, -2, 0, 0.2, False),
 ("phone_button", ven["end"] + 0.25, None, 0, 0, 0.1, False),
 ("stamp", 141.8, None, 2, 0, 0.3, False),
 ("saucer_leave", 159.5, None, -4, 0.5, 2.0, False),
]
def norm(name):
    o = N / f"{name}.wav"
    if not o.exists():
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(S / f"{name}.mp3"), "-af", "loudnorm=I=-23:TP=-2:LRA=11", "-ar", "44100", "-ac", "1", str(o)], check=True)
    return o
ins = ["-i", str(B / "voice.wav")]; fc = []
a, b = ven["start"] - 0.1, ven["end"] + 0.1
fc.append(f"[0:a]asplit=3[v0][v1][v2];[v0]atrim=0:{a},asetpts=PTS-STARTPTS[va];"
          f"[v1]atrim={a}:{b},asetpts=PTS-STARTPTS,highpass=f=300,lowpass=f=3400,acompressor=threshold=-20dB:ratio=4,volume=1dB[vb];"
          f"[v2]atrim={b},asetpts=PTS-STARTPTS[vc];[va][vb][vc]concat=n=3:v=0:a=1[voice]")
labels = ["[voice]"]
for i, (name, st, dur, db, fi, fo, loop) in enumerate(CUES, 1):
    ins += (["-stream_loop", "-1"] if loop else []) + ["-i", str(norm(name))]
    ch = f"[{i}:a]"
    tr = f"atrim=0:{dur}," if dur else ""
    d = dur if dur else float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(N / f"{name}.wav")]))
    f = f"{ch}{tr}asetpts=PTS-STARTPTS,volume={db}dB"
    if fi: f += f",afade=t=in:d={fi}"
    if fo: f += f",afade=t=out:st={max(0, d - fo):.3f}:d={fo}"
    f += f",adelay={int(st * 1000)}|{int(st * 1000)}[c{i}]"
    fc.append(f); labels.append(f"[c{i}]")
fc.append("".join(labels) + f"amix=inputs={len(labels)}:duration=first:normalize=0,alimiter=limit=0.95[o]")
subprocess.run(["ffmpeg", "-y", "-v", "error", *ins, "-filter_complex", ";".join(fc), "-map", "[o]", "-t", f"{END:.3f}", "-ar", "44100", str(B / "mix.wav")], check=True)
print("mix.wav", END)
