"""Hudba pro díl: vygeneruje skladby přes ElevenLabs Music podle úseků a smíchá je pod naraci.

Použití: python3 music.py <složka projektu>
Úseky a nálady jsou v hudba/plan.json. Skladby se ukládají do hudba/<id>.mp3 (existující se negenerují znovu).
Výstup: audio/mix.wav (narace + hudba s automatickým ztišením pod hlasem).
"""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

proj = Path(sys.argv[1])
plan = json.loads((proj / "hudba" / "plan.json").read_text(encoding="utf-8"))
XF = 3.0  # překryv sousedních skladeb (s)

for i, tr in enumerate(plan["tracks"]):
    dest = proj / "hudba" / f"{tr['id']}.mp3"
    if dest.exists():
        continue
    length = tr["end"] - tr["start"] + XF + 1
    body = {"prompt": tr["prompt"] + " Instrumental only, no vocals, steady background music for a documentary voiceover.",
            "music_length_ms": int(length * 1000)}
    req = urllib.request.Request("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128",
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    dest.write_bytes(urllib.request.urlopen(req, timeout=600).read())
    print("hotovo", tr["id"], round(length), "s", flush=True)

# hudební stopa: každá skladba na své místo, prolínání XF sekund
args, filt, labels = ["ffmpeg", "-y", "-v", "error", "-i", str(proj / "audio" / "narace.wav")], [], []
for i, tr in enumerate(plan["tracks"], start=1):
    args += ["-i", str(proj / "hudba" / f"{tr['id']}.mp3")]
    start = max(0, tr["start"] - (XF if i > 1 else 0))
    dur = tr["end"] - start + (XF if i < len(plan["tracks"]) else 2)
    fin = XF if i > 1 else 1.5
    filt.append(
        f"[{i}:a]atrim=0:{dur},asetpts=PTS-STARTPTS,aresample=44100,aformat=channel_layouts=stereo,"
        f"afade=t=in:d={fin},afade=t=out:st={dur - XF}:d={XF},volume={tr.get('gain', 1.0)},"
        f"adelay={int(start * 1000)}|{int(start * 1000)}[m{i}]")
    labels.append(f"[m{i}]")
n = len(labels)
filt.append("".join(labels) + f"amix=inputs={n}:normalize=0,volume={plan['music_level']}[music]")
# narace do sterea, hudba se pod hlasem ztiší (sidechain)
filt.append("[0:a]aresample=44100,aformat=channel_layouts=stereo,asplit=2[voice][key]")
filt.append("[music][key]sidechaincompress=threshold=0.03:ratio=6:attack=40:release=500[ducked]")
filt.append("[voice][ducked]amix=inputs=2:normalize=0:duration=longest,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=44100[out]")
subprocess.run(args + ["-filter_complex", ";".join(filt), "-map", "[out]", str(proj / "audio" / "mix.wav")], check=True)
print("mix hotový")
