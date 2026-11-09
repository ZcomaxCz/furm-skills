"""Vygeneruje hudbu a zvukové efekty Ep2 přes ElevenLabs (Music + Sound Effects API) do sfx/.
Existující soubory přeskočí. Klíč doplňuje proxy."""
import json, sys, urllib.request
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "ep02-first-contact" / "sfx"; OUT.mkdir(exist_ok=True)
MUSIC = {
 "music_tension": ("Instrumental only, no vocals. Retro 1960s sci-fi office comedy, ticking-clock tension underscore: pizzicato strings, ticking woodblock, muted brass stabs, low theremin, nervous but deadpan, tempo around 110 BPM, builds slowly, stays quiet enough for dialogue.", 58000),
 "music_outro": ("Instrumental only, no vocals. Retro 1960s sci-fi office comedy outro: slow vibraphone and Rhodes reprise with a gentle theremin, resigned and wry, like hold music in space, ends on a soft final chord.", 24000),
}
SFX = {
 "saucer_hum": ("Low smooth flying saucer hum, soft retro sci-fi engine drone, steady, distant", 10),
 "saucer_leave": ("Retro flying saucer rising and flying away, soft whooshing hum fading into the distance", 8),
 "transmission": ("Retro sci-fi incoming transmission beeps, soft electronic chirps and a gentle computer chime", 4),
 "glyphs": ("Soft shimmering sci-fi hologram glyphs swirling, airy crystalline tones", 6),
 "door_burst": ("Office door swung open quickly and bumping the wall, quick footsteps", 2),
 "desk_bell": ("Single ding of a brass reception desk bell", 2),
 "cube_hum": ("Mysterious glowing energy cube humming softly, gentle pulsing sci-fi tone", 10),
 "hologram": ("Hologram projector powering on, rising sci-fi shimmer and soft whoosh", 4),
 "paper_stack": ("Heavy thick stack of paper forms dropped on a table, thud and paper rustle", 2),
 "printer_error": ("Old office printer error beeping three times then a weak grinding stop", 4),
 "countdown_tick": ("Soft sci-fi countdown timer ticking, electronic clicks, steady", 8),
 "phone_pickup": ("Old desk phone handset picked up, click and dial tone", 2),
 "phone_button": ("Single press of a phone keypad button, beep", 1),
 "stamp": ("Rubber stamp slammed onto paper on a table, firm thud with a tiny sci-fi zap", 2),
 "room_tone": ("Quiet office room tone, faint fluorescent light hum and distant air conditioning", 15),
}
def post(url, body, dest):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    dest.write_bytes(urllib.request.urlopen(req, timeout=600).read()); print(dest.name, flush=True)
for name, (p, ms) in MUSIC.items():
    d = OUT / f"{name}.mp3"
    if not d.exists(): post("https://api.elevenlabs.io/v1/music?output_format=mp3_44100_128", {"prompt": p, "music_length_ms": ms}, d)
for name, (p, s) in SFX.items():
    d = OUT / f"{name}.mp3"
    if not d.exists(): post("https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128", {"text": p, "duration_seconds": s, "prompt_influence": 0.5}, d)
