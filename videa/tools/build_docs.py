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
agent = f"""You are the visual production agent for a Czech faceless YouTube channel that makes long-form animated explainers ("What if you travelled back in time…"). You turn scene descriptions into images and short animated clips in Google Flow, keeping ONE consistent look across the whole video.

STYLE BIBLE (apply to every image and clip):
{STYLE}.

MAIN CHARACTER (must look identical in every shot; use the character reference image as an ingredient whenever he appears):
{CHAR}. He is the only character in modern clothes and the only bright orange element in the frame.

OTHER CHARACTERS: same stick-figure construction (round white head, thin black line body, dot eyes), dressed in period clothing in muted colors (hats, long coats, caps, aprons, uniforms). Never photorealistic people, never real-person likeness.

WORLD: Prague, Czechoslovakia, 1926. Period-accurate architecture, trams, cars, clothing and objects. Traffic drives on the LEFT. No modern objects except those carried by the main character.

RULES:
1. 16:9, 1920x1080 composition, leave breathing room for subtitles in the lower 15 %.
2. No text, letters, numbers, logos or watermarks inside images (titles are added later in editing).
3. Animated clips: 8 seconds, slow and readable camera moves, the first frame must match the source image exactly (use it as the start frame). No dialogue and no music unless the shot description says so — the narration is added separately.
4. Keep the color palette and line weight consistent between scenes; if a result drifts in style, regenerate rather than accept it.
5. Name every output with its scene ID (S01, S02 …) so it can be matched to the voiceover.

WORKFLOW per scene: (a) generate the still image from the scene prompt with the style bible and the character reference, (b) if the scene is marked VEO, create a Frames-to-Video clip from that still using the motion prompt, (c) export the still in full resolution and the clip as MP4."""

fp = [f"# Prompty pro Flow – {data['title']}", "",
      f"Celkem {len(scenes)} obrázků, z toho **{len(veo)} animovat ve Flow (Veo)**; "
      "zbytek rozpohybujeme v Remotionu (zoom, pan, parallax), což šetří kredity Flow.", "",
      "## 1. Hlavní prompt pro agenta / projekt ve Flow", "",
      "Vlož jako úvodní instrukci (Flow agent, Gemini nebo ChatGPT, který bude prompty dávkovat).", "",
      "```text", agent, "```", "",
      "## 2. Referenční obrázek postavy (vygeneruj jako první)", "",
      "Výsledek ulož a používej jako *ingredient* / referenci u každé scény, kde je hlavní postava.", "",
      "```text",
      f"Character reference sheet: {CHAR}. Shown three times side by side on a plain warm off-white background: front view standing neutral, three-quarter view walking, side view pointing. Consistent proportions. {STYLE}.",
      "```", "",
      "## 3. Scény", ""]
for s in scenes:
    m = s["motion"]
    tag = "🎬 VEO" if m["type"] == "veo" else "🖼️ Remotion"
    img = s["image"].replace("the main character", "the main character (orange-hoodie stick figure from the reference)")
    img = img.replace("The main character", "The main character (orange-hoodie stick figure from the reference)")
    fp += [f"### {s['id']} · {s['part']} · {tag}", "",
           f"> {s['narration']}", "",
           "**Obrázek:**", "", "```text", f"{img} {STYLE}.", "```", ""]
    if m["type"] == "veo":
        fp += ["**Animace (Flow → Frames to Video, start frame = obrázek výše):**", "",
               "```text", m["prompt"], "```", ""]
    else:
        fp += [f"**Pohyb v Remotionu:** {m['prompt']}", ""]
(proj / "flow-prompty.md").write_text("\n".join(fp), encoding="utf-8")
print(f"OK: {len(scenes)} scén, {words} slov, {chars} znaků, {len(veo)} Veo klipů",
      f"délka {ts(total)}" if durations else "")
