"""Namluví každou scénu ze scenes.json přes ElevenLabs a složí celou stopu.

Použití: python3 tts.py <složka projektu> <voice_id> [model_id]
API klíč doplňuje síťová proxy prostředí (hlavička xi-api-key), skript ho nečte.
Výstup: audio/S01.mp3 …, audio/durations.json, audio/narace.mp3
"""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

proj, voice = Path(sys.argv[1]), sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else "eleven_multilingual_v2"
GAP = 0.35  # pauza mezi scénami (s)
scenes = json.loads((proj / "scenes.json").read_text(encoding="utf-8"))["scenes"]
out = proj / "audio"
out.mkdir(exist_ok=True)


def tts(text, prev, nxt, dest):
    body = {"text": text, "model_id": model,
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.15,
                               "use_speaker_boost": True, "speed": 1.0}}
    if model != "eleven_v3":
        body["previous_text"], body["next_text"] = prev, nxt
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_192",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    dest.write_bytes(urllib.request.urlopen(req, timeout=300).read())


def duration(p):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))


durs = {}
for i, s in enumerate(scenes):
    dest = out / f"{s['id']}.mp3"
    if not dest.exists():
        prev = scenes[i - 1]["narration"] if i else ""
        nxt = scenes[i + 1]["narration"] if i + 1 < len(scenes) else ""
        tts(s["narration"], prev, nxt, dest)
    durs[s["id"]] = round(duration(dest), 3)
    print(s["id"], durs[s["id"]], "s", flush=True)
(out / "durations.json").write_text(json.dumps(durs, indent=1))

# složení: scéna + ticho GAP, výstup MP3 i WAV
silence = out / "_gap.wav"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                "-t", str(GAP), str(silence)], check=True)
lst = out / "_concat.txt"
lst.write_text("".join(f"file '{s['id']}.mp3'\nfile '_gap.wav'\n" for s in scenes))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                "-ar", "44100", "-ac", "1", str(out / "narace.wav")], check=True)
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(out / "narace.wav"),
                "-b:a", "192k", str(out / "narace.mp3")], check=True)
silence.unlink()
lst.unlink()
print("Celkem", round(duration(out / "narace.mp3"), 1), "s")
