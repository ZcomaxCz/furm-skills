"""Vygeneruje scenar.md a flow-prompty.md ze scenes.json.

Použití: python3 build_docs.py <složka projektu>
Pokud ve složce existuje audio/durations.json, doplní časy a kapitoly.
"""
import json
import sys
from pathlib import Path

proj = Path(sys.argv[1])
data = json.loads((proj / "scenes.json").read_text(encoding="utf-8"))
scenes = data["scenes"]
dur_file = proj / "audio" / "durations.json"
durations = json.loads(dur_file.read_text()) if dur_file.exists() else {}
GAP = 0.35  # pauza mezi scénami (s), stejná jako v tts.py


def ts(sec):
    sec = int(round(sec))
    return f"{sec // 60}:{sec % 60:02d}"


starts, t = {}, 0.0
for s in scenes:
    starts[s["id"]] = t
    t += durations.get(s["id"], 0) + GAP
total = t

words = sum(len(s["narration"].split()) for s in scenes)
chars = sum(len(s["narration"]) for s in scenes)
veo = [s for s in scenes if s["motion"]["type"] == "veo"]

# ---------- scenar.md ----------
out = [f"# {data['title']}", ""]
out += ["## Varianty titulku", ""] + [f"- {t_}" for t_ in data["title_options"]] + [""]
out += [f"**Rozsah:** {len(scenes)} scén, {words} slov, {chars} znaků narace"
        + (f", délka {ts(total)}" if durations else ", odhad ~9–10 min") + ".", ""]

if durations:
    out += ["## Kapitoly (do popisu videa)", "", "```"]
    seen = set()
    for s in scenes:
        if s["part"] not in seen:
            seen.add(s["part"])
            out.append(f"{ts(starts[s['id']])} {s['part']}")
    out += ["```", ""]

part = None
for s in scenes:
    if s["part"] != part:
        part = s["part"]
        out += [f"## {part}", ""]
    tm = f" · {ts(starts[s['id']])}" if durations else ""
    kind = "🎬 Flow (Veo)" if s["motion"]["type"] == "veo" else "🖼️ obrázek + pohyb v Remotionu"
    out += [f"### {s['id']}{tm}", "", s["narration"], "", f"*Obraz:* {kind}", ""]

out += ["---", "", "## Ověřená fakta použitá ve scénáři", "",
        "- Levostranný provoz v Československu do roku 1939 (Čechy a Morava od března 1939).",
        "- Velká Praha vznikla 1. 1. 1922; sčítání 1921 ≈ 677 tis., 1930 ≈ 849 tis. obyvatel.",
        "- Zákon o osmihodinové pracovní době: prosinec 1918.",
        "- Radiojournal: pravidelné vysílání od 18. 5. 1923, stan ve Kbelích.",
        "- Penicilin: Fleming 1928, běžné použití ve 40. letech.",
        "- Kafka zemřel v červnu 1924; R.U.R. (1920) – slovo „robot“ vymyslel Josef Čapek.",
        "- VIII. všesokolský slet: léto 1926, Praha.",
        "- Veletržní palác: stavba 1925–1928.",
        "- Novogotické křídlo Staroměstské radnice vyhořelo v květnu 1945.",
        "- Tuberkulóza = „morbus viennensis“ (vídeňská nemoc).", ""]
(proj / "scenar.md").write_text("\n".join(out), encoding="utf-8")

# ---------- flow-prompty.md ----------
STYLE, CHAR = data["style"], data["character"]
agent = """You are my illustrator for a Czech faceless YouTube channel with long-form animated explainers ("What if you travelled back in time…", "How long would you survive…"). For every scene I send, you create ONE image in 16:9 landscape format. All images of a video must look like frames from the same animated film.

THE MAIN CHARACTER IS IN THE ATTACHED IMAGE. Keep him exactly as he is drawn there in every image: the same large perfectly round white head (about one third of his height) with a thin black outline, the same two black dot eyes and small simple mouth, no nose, ears or hair, the same bright orange hoodie with hood, drawstrings and kangaroo pocket, the same dark blue jeans, white sneakers and round white mitten-like hands. Do not redesign, restyle or recolor him. You may change only his pose, facial expression (simple eyebrows and mouth, like in the reference) and what he holds. He is the only person in modern clothes and the only bright orange thing in the picture.

Every other person is drawn the same way as him: large round white head, dot eyes, simple mouth, white mitten hands and a clothed body with thin black outlines, but dressed in clothing of the scene's era in muted colors. Never draw realistic people and never the likeness of a real, recognizable person.

The look is a 2D hand-drawn explainer illustration: flat-colored cartoon characters placed in richly detailed painted backgrounds, a muted vintage palette matching the era (for Prague 1926: sepia, warm grey and soft teal), soft natural light and a subtle paper texture. Architecture, vehicles, clothing and objects are accurate for the place and year of the scene; nothing modern appears except what the main character carries. The composition is cinematic and the bottom part of the frame stays calm because subtitles will go there.

Never put any text, letters, numbers, readable signs, logos or watermarks into the image; titles are added later in editing.

When I send a scene, reply only with the image. If I write "again", generate a new version of the same scene. If I write "fix: …", edit the last image only as described and keep everything else unchanged."""

fp = [f"# Prompty pro obrázky (Nano Banana) a animace (Flow) – {data['title']}", "",
      f"Celkem {len(scenes)} obrázků, z toho **{len(veo)} animovat ve Flow (Veo)**; "
      "zbytek rozpohybujeme v Remotionu (zoom, pan, parallax).", "",
      "## 1. Instrukce pro Nano Banana (jednou na začátku konverzace / do Gemu)", "",
      "Přilož výřez postavy `videa/postava/postava-zepredu.png` a pošli tento text. Pak už posílej jen prompty scén.", "",
      "```text", agent, "```", "",
      "## 2. Scény", "",
      "Každý prompt je samostatný – funguje i bez instrukcí výše, když k němu přiložíš výřez postavy.", ""]
for s in scenes:
    m = s["motion"]
    tag = "🎬 VEO" if m["type"] == "veo" else "🖼️ Remotion"
    scene = s["image"].replace("the main character", "the orange-hoodie character from the attached image")
    scene = scene.replace("The main character", "The orange-hoodie character from the attached image")
    img = (f"Create a 16:9 landscape illustration. Use the orange-hoodie character from the attached image and keep him exactly as drawn: same round white head, face, hoodie, jeans, sneakers and proportions. "
           f"Scene: {scene} "
           "Draw all other people in the same cartoon style: large round white heads, dot eyes, white mitten hands, period clothing in muted colors. "
           "Style: 2D hand-drawn explainer illustration, flat-colored characters in a richly detailed painted background, muted vintage palette of sepia, warm grey and soft teal, soft natural light, subtle paper texture. "
           "No text, letters, numbers or logos anywhere in the image.")
    fp += [f"### {s['id']} · {s['part']} · {tag}", "",
           f"> {s['narration']}", "",
           "**Obrázek:**", "", "```text", img, "```", ""]
    if m["type"] == "veo":
        fp += ["**Animace (Flow → Frames to Video, start frame = obrázek výše):**", "",
               "```text", m["prompt"], "```", ""]
    else:
        fp += [f"**Pohyb v Remotionu:** {m['prompt']}", ""]
(proj / "flow-prompty.md").write_text("\n".join(fp), encoding="utf-8")
print(f"OK: {len(scenes)} scén, {words} slov, {chars} znaků, {len(veo)} Veo klipů",
      f"délka {ts(total)}" if durations else "")
