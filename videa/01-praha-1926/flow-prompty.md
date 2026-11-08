# Prompty pro Flow – Co kdybys cestoval 100 let do minulosti? Praha 1926

Celkem 35 obrázků, z toho **13 animovat ve Flow (Veo)**; zbytek rozpohybujeme v Remotionu (zoom, pan, parallax), což šetří kredity Flow.

## 1. Hlavní prompt pro agenta / projekt ve Flow

Vlož jako úvodní instrukci (Flow agent, Gemini nebo ChatGPT, který bude prompty dávkovat).

```text
You are the visual production agent for a Czech faceless YouTube channel that makes long-form animated explainers ("What if you travelled back in time…"). You turn scene descriptions into images and short animated clips in Google Flow, keeping ONE consistent look across the whole video.

STYLE BIBLE (apply to every image and clip):
2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.

MAIN CHARACTER (must look identical in every shot; use the character reference image as an ingredient whenever he appears):
a simple white stick figure with a perfectly round white head, thin clean black outlines, two black dot eyes and a minimal expressive mouth, wearing a bright orange modern hoodie, dark jeans and white sneakers, often holding a black smartphone. He is the only character in modern clothes and the only bright orange element in the frame.

OTHER CHARACTERS: same stick-figure construction (round white head, thin black line body, dot eyes), dressed in period clothing in muted colors (hats, long coats, caps, aprons, uniforms). Never photorealistic people, never real-person likeness.

WORLD: Prague, Czechoslovakia, 1926. Period-accurate architecture, trams, cars, clothing and objects. Traffic drives on the LEFT. No modern objects except those carried by the main character.

RULES:
1. 16:9, 1920x1080 composition, leave breathing room for subtitles in the lower 15 %.
2. No text, letters, numbers, logos or watermarks inside images (titles are added later in editing).
3. Animated clips: 8 seconds, slow and readable camera moves, the first frame must match the source image exactly (use it as the start frame). No dialogue and no music unless the shot description says so — the narration is added separately.
4. Keep the color palette and line weight consistent between scenes; if a result drifts in style, regenerate rather than accept it.
5. Name every output with its scene ID (S01, S02 …) so it can be matched to the voiceover.

WORKFLOW per scene: (a) generate the still image from the scene prompt with the style bible and the character reference, (b) if the scene is marked VEO, create a Frames-to-Video clip from that still using the motion prompt, (c) export the still in full resolution and the clip as MP4.
```

## 2. Referenční obrázek postavy (vygeneruj jako první)

Výsledek ulož a používej jako *ingredient* / referenci u každé scény, kde je hlavní postava.

```text
Character reference sheet: a simple white stick figure with a perfectly round white head, thin clean black outlines, two black dot eyes and a minimal expressive mouth, wearing a bright orange modern hoodie, dark jeans and white sneakers, often holding a black smartphone. Shown three times side by side on a plain warm off-white background: front view standing neutral, three-quarter view walking, side view pointing. Consistent proportions. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

## 3. Scény

### S01 · Úvod · 🎬 VEO

> Zavřeš oči uprostřed Václavského náměstí. Telefon v ruce, sluchátka v uších. Otevřeš je… a telefon nemá signál. Ne na pět minut. Na dalších sedmdesát let. Je rok 1926.

**Obrázek:**

```text
The main character (orange-hoodie stick figure from the reference) standing in the middle of Wenceslas Square in Prague in 1926, looking down in confusion at his smartphone whose screen shows a crossed-out signal icon. Around him: 1920s trams, horse-drawn carts, stick-figure men in hats and long coats. The National Museum building at the top of the square in the background. Overcast morning light. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Animace (Flow → Frames to Video, start frame = obrázek výše):**

```text
Slow dolly-in on the stick figure as he lowers the phone and looks up in disbelief; a tram passes behind him, pedestrians in hats walk by, faint coal smoke drifts in the air. 8 seconds. Quiet city ambience only, no music, no dialogue.
```

### S02 · Úvod · 🖼️ Remotion

> Kolem cinká tramvaj, kůň táhne povoz se sudy piva a pán v buřince na tebe zírá, jako bys spadl z Marsu. Což vlastně skoro sedí.

**Obrázek:**

```text
Medium shot: a stick-figure gentleman in a bowler hat and long coat staring in shock at the main character (orange-hoodie stick figure from the reference). Behind them a horse-drawn wagon loaded with wooden beer barrels and a 1920s Prague tram in red and cream livery. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Pomalý zoom na šokovaný obličej pána v buřince.

### S03 · Úvod · 🖼️ Remotion

> V tomhle videu zjistíme, jak dlouho bys v Praze roku 1926 vydržel. Kde bys spal, co bys jedl, za co bys platil – a jaká drobnost by tě mohla zabít během prvních pěti minut.

**Obrázek:**

```text
Clean title-card composition: the main character (orange-hoodie stick figure from the reference) in the center surrounded by four small vignettes in the same style: a simple bed, a plate of dumplings, old coins, and a vintage 1920s automobile. Large empty plain area in the upper third reserved for a title. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Ikonky postupně naskakují (pop-in); nahoru titulek „PRAHA 1926“ vložený v Remotionu.

### S04 · Prvních pět minut · 🎬 VEO

> Začneme tou drobností. Vystoupíš z chodníku, podíváš se doleva, jak tě to učili ve škole… a málem tě srazí auto. Zprava. V Československu se totiž v roce 1926 jezdí vlevo. Jako dnes v Londýně. Na pravou stranu se přejde až v roce 1939.

**Obrázek:**

```text
A Prague street in 1926: the main character (orange-hoodie stick figure from the reference) stepping off the curb while looking to the LEFT, while a black 1920s automobile approaches from the RIGHT driving on the left side of the road, the stick-figure driver honking. Comic near-miss moment. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Animace (Flow → Frames to Video, start frame = obrázek výše):**

```text
The stick figure steps off the curb looking left; a black 1920s car comes from the right on the left side of the road and swerves; the stick figure jumps back onto the sidewalk in comic shock. Static wide shot. 8 seconds. Car horn and engine sounds only, no music, no dialogue.
```

### S05 · Prvních pět minut · 🖼️ Remotion

> Dobře, přežil jsi. Rozhlédneš se. Tramvaje jezdí přímo středem Václavského náměstí. Aut je málo, víc je povozů, kol a chodců. A všichni nosí klobouk. Opravdu všichni. Vyjít ven bez klobouku je jako dnes vyjít ven v pyžamu.

**Obrázek:**

```text
Wide high-angle view of Wenceslas Square in 1926: trams running down the middle of the boulevard, few cars, horse carts, bicycles, crowds of stick-figure pedestrians all wearing hats (bowler hats, fedoras, women in cloche hats). The main character (orange-hoodie stick figure from the reference) is the only bareheaded person and clearly stands out in his orange hoodie. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Pomalý pan shora dolů, na konci zoom na hlavu bez klobouku.

### S06 · Prvních pět minut · 🎬 VEO

> A ten vzduch. Praha topí uhlím – v každém domě, v každé kuchyni. V zimě visí nad městem šedá deka kouře a fasády jsou černé od sazí.

**Obrázek:**

```text
Prague rooftops in winter 1926: dozens of chimneys releasing coal smoke, a grey haze over the city, Prague Castle faintly visible in the distance, soot-darkened facades. On the street below, the main character (orange-hoodie stick figure from the reference) coughing into his sleeve. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Animace (Flow → Frames to Video, start frame = obrázek výše):**

```text
Smoke rises slowly from many chimneys and drifts across the frame; slow pan from the rooftops toward Prague Castle in the haze. 8 seconds. Wind ambience only, no music, no dialogue.
```

### S07 · Kam ses to dostal · 🖼️ Remotion

> Abys věděl, kam ses dostal: Československo existuje teprve osm let. Prezidentem je Tomáš Garrigue Masaryk a lidé mu říkají tatíček. Republika je mladá, sebevědomá a patří k průmyslově nejvyspělejším zemím Evropy.

**Obrázek:**

```text
A 1920s office wall with a framed formal portrait of an elderly stick figure with a white goatee and pince-nez glasses, a Czechoslovak flag beside it, and a window showing factory chimneys and a bustling city. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Pomalý zoom od okna na portrét.

### S08 · Kam ses to dostal · 🖼️ Remotion

> A Praha je najednou velkoměsto. Před čtyřmi lety se k ní připojily desítky okolních obcí – Vinohrady, Žižkov, Smíchov, Karlín – a vznikla takzvaná Velká Praha. Žije tu přes sedm set tisíc lidí.

**Obrázek:**

```text
Hand-drawn vintage-style illustrated map of Prague seen from above: the Vltava river, the historic center in the middle, surrounding districts drawn as separate soft-colored patches with factories and new apartment blocks at the edges. Cartographic style matching the explainer look, no labels. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Okolní čtvrti se postupně „přicvaknou“ k centru (masky v Remotionu); popisky Vinohrady, Žižkov, Smíchov, Karlín doplnit v Remotionu.

### S09 · Kam ses to dostal · 🖼️ Remotion

> Na ulici uslyšíš češtinu, ale taky němčinu. Praha je město tří kultur – české, německé a židovské – a potkávají se tu v kavárnách, divadlech i na trzích.

**Obrázek:**

```text
A busy 1926 Prague street market: groups of stick figures in varied period clothing chatting, a market vendor, a businessman in a suit, a shopkeeper in front of his small shop; speech bubbles containing only abstract squiggles. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Pomalý boční pan přes trh.

### S10 · Kam ses to dostal · 🎬 VEO

> A až dojdeš na Staroměstské náměstí, uvidíš radnici celou. I s velkým novogotickým křídlem, které v posledních dnech války shoří a už nikdy se neobnoví.

**Obrázek:**

```text
Old Town Square in Prague in 1926 showing the Old Town Hall complete with its large neo-gothic east wing next to the clock tower, the Týn Church in the background; the main character (orange-hoodie stick figure from the reference) looking up at the building from the square. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Animace (Flow → Frames to Video, start frame = obrázek výše):**

```text
Slow upward tilt along the neo-gothic town hall wing and the clock tower, pigeons fly across the square. 8 seconds. Square ambience only, no music, no dialogue.
```

### S11 · Peníze a papíry · 🖼️ Remotion

> Teď první velký problém: peníze. Platí se korunou československou. Tvoje karta je kousek plastu, se kterým nikdo nic neudělá. A mince v kapse? Mají letopočty z budoucnosti. Když je zkusíš utratit, v lepším případě se ti vysmějí. V horším zavolají strážníka.

**Obrázek:**

```text
Inside a small 1920s grocery shop: the main character (orange-hoodie stick figure from the reference) holding out a modern plastic payment card to a stick-figure shopkeeper in an apron who stares at it in total confusion. Wooden counter, brass scales, glass jars. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Zoom na kartu, pak na zmatený výraz prodavače.

### S12 · Peníze a papíry · 🎬 VEO

> A strážník bude chtít vědět, kdo jsi. V téhle době má každý takzvanou domovskou příslušnost – obec, ke které patří a která se o něj postará, když přijde o všechno. Ty nepatříš nikam. Nemáš papíry, adresu ani nikoho, kdo by se za tebe zaručil.

**Obrázek:**

```text
A stick-figure 1920s policeman in a dark uniform and cap, holding a small notebook and frowning at the main character (orange-hoodie stick figure from the reference), who nervously pulls out his empty pockets. Street background. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Animace (Flow → Frames to Video, start frame = obrázek výše):**

```text
The policeman taps his notebook with a pencil and leans forward suspiciously; the stick figure pulls out empty pockets and shrugs. Static medium shot. 8 seconds. Light street ambience, no music, no dialogue.
```

### S13 · Peníze a papíry · 🖼️ Remotion

> Takže úkol číslo jedna: vydělat peníze. Tvoje bunda, tenisky a hlavně telefon jsou na rok 1926 zázraky techniky. Jenže zkus v zastavárně vysvětlit, co je dotykový displej. Nejrealističtější cesta? Práce.

**Obrázek:**

```text
A dim 1920s pawn shop: an old stick-figure pawnbroker with a jeweler's loupe suspiciously examining the glowing smartphone, shelves full of clocks, violins and pocket watches; the main character (orange-hoodie stick figure from the reference) waiting hopefully. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Pomalý zoom na svítící telefon v rukou zastavárníka.

### S14 · Práce · 🎬 VEO

> Práce se najít dá. Republika má od roku 1918 zákon o osmihodinové pracovní době – na svou dobu docela pokrokový. Jenže osm hodin v továrně v Libni nebo na Smíchově je úplně jiná liga než osm hodin u počítače.

**Obrázek:**

```text
Interior of a 1920s Prague factory hall with large machines, drive belts and steam; stick-figure workers in caps and overalls; the main character (orange-hoodie stick figure from the reference) among them, exhausted and sweating, struggling with a heavy metal part. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Animace (Flow → Frames to Video, start frame = obrázek výše):**

```text
Drive belts and wheels turn, steam puffs, workers move rhythmically; the orange-hoodie stick figure wipes his forehead. Slow lateral tracking shot. 8 seconds. Factory machine sounds only, no music, no dialogue.
```

### S15 · Práce · 🖼️ Remotion

> Bez papírů a bez řemesla tě čeká to nejtěžší – nosič, pomocník na stavbě, vykládání uhlí. A staví se hodně. Roste Veletržní palác, nové čtvrti, nové činžáky. Ruce jsou potřeba.

**Obrázek:**

```text
Construction site of a large modernist building with a concrete frame and wooden scaffolding in Prague, 1926; stick-figure workers carrying bricks; the main character (orange-hoodie stick figure from the reference) carrying a heavy sack of coal on his back. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Pomalý pan zdola nahoru po lešení.

### S16 · Práce · 🖼️ Remotion

> Ale tvoje skutečná superschopnost je jinde. Ty víš, co přijde. Víš, že filmy brzy promluví. Že rádio bude v každé domácnosti. Jenže kdo by věřil chlápkovi v teniskách, který tvrdí, že zná budoucnost?

**Obrázek:**

```text
A smoky 1920s pub: the main character (orange-hoodie stick figure from the reference) enthusiastically explaining something to a table of stick-figure men in flat caps who laugh at him; above him a thought bubble containing a simple television, a radio and an airplane drawn in simple lines. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Bublina s myšlenkou se nafoukne (scale-in), lehké třesení smíchem.

### S17 · Bydlení · 🖼️ Remotion

> Máš první výplatu. Kde budeš spát? Na Žižkově nebo v Libni můžeš být takzvaný nocležník – platíš si jen postel v cizím bytě. Někdy jen na pár hodin, než ji uvolní někdo z noční směny.

**Obrázek:**

```text
A cramped 1920s working-class room: one shared bed, a stick-figure worker in overalls getting out of it at dawn while the main character (orange-hoodie stick figure from the reference) waits beside it holding a small bundle; a family sleeping in the background. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Pomalý zoom na postel, přechod denního světla.

### S18 · Bydlení · 🎬 VEO

> Typický byt? Jedna místnost a kuchyň pro celou rodinu. Záchod? Na pavlači, společný pro celé patro. Koupelna? Většinou žádná. Koupat se chodíš do lázní, tak jednou týdně.

**Obrázek:**

```text
Courtyard view of an old Prague tenement building with open balcony corridors on every floor, a small shared toilet door at the end of one corridor, a queue of stick figures waiting with newspapers, laundry hanging on lines. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Animace (Flow → Frames to Video, start frame = obrázek výše):**

```text
The toilet door opens, one stick figure walks out, the next in the queue hurries in; laundry sways in the wind. Static wide shot. 8 seconds. Courtyard ambience only, no music, no dialogue.
```

### S19 · Bydlení · 🎬 VEO

> Elektřina v Praze už je, ale ne všude. Ve starších domech se svítí petrolejkou nebo plynem. A večer chodí ulicemi lampář a rozsvěcuje plynové lampy jednu po druhé.

**Obrázek:**

```text
Dusk on a cobblestone street in Prague's Lesser Town: a stick-figure lamplighter with a long pole lighting a gas street lamp, warm glow spreading over the cobblestones; the main character (orange-hoodie stick figure from the reference) watching in awe. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Animace (Flow → Frames to Video, start frame = obrázek výše):**

```text
The lamplighter raises his pole and the gas lamp ignites with a warm flicker; he walks on to the next lamp as dusk deepens. Slow push-in. 8 seconds. Soft evening ambience, no music, no dialogue.
```

### S20 · Jídlo · 🖼️ Remotion

> Dobrá zpráva je jídlo. Česká kuchyně roku 1926 by ti byla povědomá – knedlíky, zelí, polévky, buchty. Jenže maso je svátek, ne samozřejmost. Běžně se jí brambory, chleba, luštěniny a hodně sádla.

**Obrázek:**

```text
A simple wooden kitchen table in a 1920s Czech working-class home: a bowl of potato soup, a loaf of bread, a plate of dumplings with sauerkraut, a jar of lard; the main character (orange-hoodie stick figure from the reference) eating together with a stick-figure family. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Pomalý pan přes stůl.

### S21 · Jídlo · 🖼️ Remotion

> Lednička? Zapomeň. Máš nanejvýš chladnou spíž nebo kus ledu, který přiveze ledař. Nakupuje se proto každý den – na trhu nebo u hokynáře na rohu.

**Obrázek:**

```text
A stick-figure iceman carrying a large block of ice on his shoulder with iron tongs, walking from a horse-drawn ice wagon into a tenement doorway; the main character (orange-hoodie stick figure from the reference) holding the door open. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Pomalý zoom, ledař projde zleva doprava (parallax vrstvy).

### S22 · Jídlo · 🖼️ Remotion

> A pivo teče proudem. Hospoda je centrum všeho – řeší se tu politika, práce i fotbal. Sparta a Slavia jsou největší rivalové už tehdy.

**Obrázek:**

```text
Lively 1920s Prague pub interior with wooden tables and foamy beer mugs; two stick figures arguing passionately about football, one wearing a dark red scarf, the other a red-and-white scarf; the main character (orange-hoodie stick figure from the reference) between them holding a beer. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Rychlý zoom střídavě na oba fanoušky (komický efekt).

### S23 · Neviditelný nepřítel · 🎬 VEO

> A teď to vážné. Největší nebezpečí roku 1926 nejsou zloději ani auta jezdící vlevo. Jsou to bacily.

**Obrázek:**

```text
Dramatic dark composition: the main character (orange-hoodie stick figure from the reference) small in the center, surrounded by giant hand-drawn cartoon bacteria and microbes, ominous low-key lighting. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Animace (Flow → Frames to Video, start frame = obrázek výše):**

```text
Cartoon microbes slowly drift and pulse around the stick figure, who turns around nervously; camera slowly pulls back. 8 seconds. Low ominous ambient tone, no music, no dialogue.
```

### S24 · Neviditelný nepřítel · 🖼️ Remotion

> Antibiotika neexistují. Penicilin objeví Alexander Fleming až za dva roky a do běžné léčby se dostane až ve čtyřicátých letech. Obyčejná infekce z řezné rány může být smrtelná.

**Obrázek:**

```text
A 1920s doctor's office: a stick-figure doctor with a head mirror and a black leather bag bandaging the main character (orange-hoodie stick figure from the reference)'s cut hand; shelves of glass medicine bottles. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Pomalý zoom na obvázanou ruku.

### S25 · Neviditelný nepřítel · 🖼️ Remotion

> Tuberkulóze se tu říká vídeňská nemoc a zabíjí hlavně mladé lidi v přeplněných, vlhkých bytech. Přesně v takových, kde bys bydlel ty.

**Obrázek:**

```text
A dim, damp, crowded tenement room with mold stains on the walls, a pale stick figure coughing in bed, a small window letting in grey light. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Velmi pomalý zoom, postupná desaturace.

### S26 · Neviditelný nepřítel · 🖼️ Remotion

> Tvoje šance? Paradoxně slušné. Víš, že si máš mýt ruce, převařit vodu a větrat. Tyhle drobnosti tu nejsou samozřejmost – a v roce 1926 ti můžou zachránit život.

**Obrázek:**

```text
The main character (orange-hoodie stick figure from the reference) washing his hands with soap at an enamel basin, a kettle boiling on a cast-iron stove, an open window letting in bright sunlight; hopeful bright mood. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Prosvětlení obrazu, lehký zoom-out.

### S27 · Zábava · 🎬 VEO

> Když přežiješ, Praha ti nabídne neuvěřitelně živé město. Kavárny jsou plné spisovatelů, malířů a novinářů. U jednoho kafe můžeš sedět celé odpoledne a číst noviny – mají jich tu desítky.

**Obrázek:**

```text
Elegant 1920s Prague grand café interior: tall windows overlooking the Vltava river and Prague Castle, marble tables, stick figures reading newspapers on wooden holders, a waiter in a tailcoat; the main character (orange-hoodie stick figure from the reference) sipping coffee. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Animace (Flow → Frames to Video, start frame = obrázek výše):**

```text
Steam rises from the coffee cup, a waiter glides past, newspapers rustle; slow dolly across the café toward the window view of Prague Castle. 8 seconds. Soft café ambience, no music, no dialogue.
```

### S28 · Zábava · 🖼️ Remotion

> Možná tu potkáš Karla Čapka. Jeho hra R.U.R. dala světu slovo robot – a ty jsi jediný člověk v Praze, který ví, jak moc to slovo zdomácní. Franze Kafku ale nepotkáš. Zemřel před dvěma lety a o jeho budoucí slávě zatím nikdo nemá tušení.

**Obrázek:**

```text
In the café: a stick-figure writer with slicked-back dark hair and a pipe writing at a table covered in papers; above him a whimsical thought bubble with a simple boxy cartoon robot; the main character (orange-hoodie stick figure from the reference) at the next table grinning knowingly. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Robot v bublině se lehce pohupuje (wiggle), zoom na úsměv hlavní postavy.

### S29 · Zábava · 🎬 VEO

> V kinech běží němé filmy a hraje k nim živý klavír nebo orchestr. Mluvený film dorazí až na konci dvacátých let.

**Obrázek:**

```text
Inside a 1920s cinema: a black-and-white silent film projected on the screen, a stick-figure pianist playing an upright piano below the screen, an audience of stick figures in hats, a visible beam of light from the projector. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Animace (Flow → Frames to Video, start frame = obrázek výše):**

```text
The projector beam flickers, the pianist plays energetically, the audience laughs; slow push toward the screen. 8 seconds. Upbeat silent-film piano only, no dialogue.
```

### S30 · Zábava · 🖼️ Remotion

> A rádio? Úplná novinka. Radiojournal vysílá pravidelně teprve od roku 1923 – první vysílání šlo ze stanu ve Kbelích. Rádio doma je luxus a poslouchá se často jen na sluchátka.

**Obrázek:**

```text
A 1920s living room: a family crowding around a small crystal radio set, one stick figure wearing big headphones listening in amazement while the others wait their turn; the main character (orange-hoodie stick figure from the reference) smirking while holding his modern wireless earbuds. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Zoom ze sluchátek rodiny na moderní sluchátka hlavní postavy.

### S31 · Zábava · 🎬 VEO

> A v létě roku 1926 zažiješ něco, co dnes nemá obdoby – všesokolský slet. Desítky tisíc lidí cvičí naráz v dokonalé souhře a celé město žije jen tímhle.

**Obrázek:**

```text
A huge stadium field seen from above: tens of thousands of stick-figure gymnasts in white and red outfits performing synchronized exercises in perfect geometric formation, packed wooden grandstands, Czechoslovak flags. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Animace (Flow → Frames to Video, start frame = obrázek výše):**

```text
The mass of gymnasts raise their arms in perfect unison, creating a wave pattern across the field; slow aerial crane shot. 8 seconds. Distant crowd and brass band, no dialogue.
```

### S32 · Verdikt · 🖼️ Remotion

> Takže – jak dlouho bys vydržel? První den je nejnebezpečnější: auta zprava, žádné peníze, žádné papíry. Když najdeš práci a postel, první měsíc zvládneš. A když se vyhneš infekcím, klidně i roky.

**Obrázek:**

```text
Three-panel composition side by side showing the main character (orange-hoodie stick figure from the reference): panel 1 dodging a 1920s car, panel 2 carrying a sack of coal, panel 3 sitting confidently in a café wearing a 1920s fedora over his orange hoodie. Plain space above each panel for numbers to be added later. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Panely naskakují postupně; nad ně čísla „1 den / 1 měsíc / roky“ v Remotionu.

### S33 · Verdikt · 🎬 VEO

> Jenže je tu ještě jedna věc. Ty víš, co přijde potom. Krize. Mnichov. Válka. Celá tahle Praha – kavárny, Sokol, svobodné noviny – se za pouhých třináct let změní k nepoznání.

**Obrázek:**

```text
The main character (orange-hoodie stick figure from the reference) standing alone on Charles Bridge at dusk, seen from behind, looking over the Vltava toward Prague Castle; a long shadow, dark storm clouds gathering on the horizon; melancholic mood. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Animace (Flow → Frames to Video, start frame = obrázek výše):**

```text
Dark clouds slowly roll in over Prague Castle, the light dims, the stick figure lowers his head; slow push-in from behind. 8 seconds. Wind and distant church bells, no music, no dialogue.
```

### S34 · Verdikt · 🖼️ Remotion

> Takže otázka nezní, jestli bys v roce 1926 přežil. Otázka zní, jestli bys dokázal mlčet.

**Obrázek:**

```text
Close-up of the main character (orange-hoodie stick figure from the reference)'s face with a finger on his lips in a 'shh' gesture, sepia Prague softly blurred behind him. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Velmi pomalý zoom, na konci střih do černé.

### S35 · Verdikt · 🖼️ Remotion

> Příště se podíváme ještě dál – do středověkých Čech. A tam by to bylo mnohem horší.

**Obrázek:**

```text
Teaser: a medieval Bohemian village with wooden houses and a castle on a hill; the main character (orange-hoodie stick figure from the reference) appearing in a flash of light, standing in the mud, while stick-figure medieval peasants with pitchforks stare at him. 2D hand-drawn explainer illustration, simple stick-figure characters with round heads and thin black outlines placed on richly detailed painted backgrounds, muted vintage palette of sepia, warm grey and teal (1920s feel), flat shading, subtle paper texture, soft natural light, cinematic 16:9 composition, no text, no letters, no captions, no watermark.
```

**Pohyb v Remotionu:** Bílý záblesk, rychlý zoom-out, odkaz na další video (koncová obrazovka).
