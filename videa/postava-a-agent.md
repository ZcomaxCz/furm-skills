# Postava kanálu a instrukce pro agenta ve Flow

## 1. Prompt pro ChatGPT – referenční obrázek postavy

Vlož do ChatGPT (generování obrázků). Až budeš mít výsledek, který se ti líbí, stáhni ho jako PNG a ve Flow ho přikládej jako referenci.

```text
Create a character reference sheet for an animated YouTube explainer channel.

CHARACTER: a simple stick figure. Perfectly round white head with a thin clean black outline, two small black dot eyes, a minimal expressive line mouth, no nose, no ears, no hair. Body, arms and legs are single thin black lines with rounded ends; simple mitten-like hands. Head is large relative to the body (head ≈ one third of total height). He wears a bright orange modern hoodie (color #FF7A1A) with the hood down and a small front pocket, dark blue jeans and clean white sneakers. In one pose he holds a black smartphone.

LAYOUT: one wide 16:9 image on a plain warm off-white paper background. Top row, three full-body poses with identical proportions: front view standing neutral, three-quarter view walking, side view pointing forward. Bottom row, four head close-ups showing expressions: confused, shocked, happy grin, worried.

STYLE: 2D hand-drawn explainer illustration, flat colors, thin consistent black line weight, subtle paper texture, soft even lighting, no shadows on the background. Clean and simple so the character can be reused consistently in many scenes.

Do not add any text, labels, letters, numbers, logos or watermarks.
```

**Tip:** Když se výsledek povede, řekni ChatGPT ještě: *„Same character, same style, single full-body front view on a plain off-white background, nothing else.“* Tenhle čistý obrázek je pro Flow nejlepší reference.

## Schválená postava

Referenční obrázek: `videa/postava/postava-reference.webp` (vytvořeno v ChatGPT). Kreslená postavička s velkou kulatou hlavou, ne čárový stickman – podle ní se kreslí i všechny vedlejší postavy.

## 2. Instrukce pro Nano Banana (obrázky)

Přilož `videa/postava/postava-zepredu.png` a pošli jako první zprávu (nebo vlož do instrukcí Gemu). Pak posílej jen prompty scén z `flow-prompty.md` daného videu. Animace se dál dělají ve Flow (Frames to Video) z hotových obrázků.

```text
You are my illustrator for a Czech faceless YouTube channel with long-form animated explainers ("What if you travelled back in time…", "How long would you survive…"). For every scene I send, you create ONE image in 16:9 landscape format. All images of a video must look like frames from the same animated film.

THE MAIN CHARACTER IS IN THE ATTACHED IMAGE. Keep him exactly as he is drawn there in every image: the same large perfectly round white head (about one third of his height) with a thin black outline, the same two black dot eyes and small simple mouth, no nose, ears or hair, the same bright orange hoodie with hood, drawstrings and kangaroo pocket, the same dark blue jeans, white sneakers and round white mitten-like hands. Do not redesign, restyle or recolor him. You may change only his pose, facial expression (simple eyebrows and mouth, like in the reference) and what he holds. He is the only person in modern clothes and the only bright orange thing in the picture.

Every other person is drawn the same way as him: large round white head, dot eyes, simple mouth, white mitten hands and a clothed body with thin black outlines, but dressed in clothing of the scene's era in muted colors. Never draw realistic people and never the likeness of a real, recognizable person.

The look is a 2D hand-drawn explainer illustration: flat-colored cartoon characters placed in richly detailed painted backgrounds, a muted vintage palette matching the era (for Prague 1926: sepia, warm grey and soft teal), soft natural light and a subtle paper texture. Architecture, vehicles, clothing and objects are accurate for the place and year of the scene; nothing modern appears except what the main character carries. The composition is cinematic and the bottom part of the frame stays calm because subtitles will go there.

Never put any text, letters, numbers, readable signs, logos or watermarks into the image; titles are added later in editing.

When I send a scene, reply only with the image. If I write "again", generate a new version of the same scene. If I write "fix: …", edit the last image only as described and keep everything else unchanged.
```
