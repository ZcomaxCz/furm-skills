"""Namluví repliky z tabulky „Voice sheet“ v dokumentu epizody přes ElevenLabs (eleven_v3).

Použití: python3 voices_ep.py <doc.md> <voices.json> <out_dir> [soubor ...]
Bez výčtu souborů namluví všechny repliky. Existující mp3 vždy přeskočí (šetří kvótu); pro nové namluvení soubor smažte.
API klíč doplňuje síťová proxy prostředí (hlavička xi-api-key), skript ho nečte.
"""
import json, re, sys, urllib.request
from pathlib import Path

doc, vmap, out = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text()), Path(sys.argv[3])
only = set(sys.argv[4:])
out.mkdir(parents=True, exist_ok=True)
lines = []
for l in doc.read_text(encoding="utf-8").splitlines():
    if not re.match(r"\| s\d\d_\d\d_", l):
        continue
    f, spk, text, deliv = [x.strip().replace("\\|", "|") for x in re.split(r"(?<!\\)\|", l)[1:-1]]
    tags = " ".join(re.findall(r"\[[^\]]+\]", deliv))
    lines.append((f, spk, f"{tags} {text}".strip()))
for f, spk, text in lines:
    dest = out / f"{f}.mp3"
    if (only and f not in only) or dest.exists():
        continue
    v = vmap[spk]
    body = {"text": text, "model_id": "eleven_v3", "voice_settings": {"stability": v.get("stability", 0.5)}}
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{v['id']}?output_format=mp3_44100_128",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    dest.write_bytes(urllib.request.urlopen(req, timeout=300).read())
    print(f, spk, len(text), "zn.", flush=True)
