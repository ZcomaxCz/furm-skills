# Belumo Studio ⭐ – project handoff for Claude Code

Summary of the previous chat ("přechod na nový kanál"): what the project is, decisions made, how videos are built, current state and what to do next. The user writes in Czech; all video content is in English (US audience).

Files in this folder:
- `CLAUDE.md` – this handoff (loaded automatically when working in `belumo/`)
- `ep02-first-contact/ep02-doc.md` – full Ep2 doc (script, voice sheet, image prompts, Flow prompts, music brief, upload metadata), exported from the Docs artifact
- `pipeline/` – Ep1 build code (epcore, fxshots, build_ep, build_short, teaser2, mix.sh). Paths still point to the old Claude workspace (`/mnt/user-data/...`, `/home/claude/work/...`) and must be adjusted.

## 0. Changes in this environment (Claude Code cloud, 2026-11-09)
- `api.elevenlabs.io` IS reachable here (key injected by the proxy, no key in code). Claude can generate voices directly; see `videa/tools/tts.py` for the request pattern. Check plan and character quota before a large run (`GET /v1/user/subscription`). Free-plan rules (attribution, no commercial use) still apply.
- ffmpeg 6.1 is installed; OpenCV / numpy / Pillow come from pip (`pip install opencv-python-headless numpy pillow`). Poppins font may need to be downloaded (Google Fonts) and `fontsdir` adjusted.
- Ep1 source media (Flow clips, voice files, music/SFX, start frames, `audio_v4.m4a`) are NOT in this repo. Ask the user to upload what is needed.
- 4 CPU cores; long renders should run in the background.

## 1. Project
- **YouTube channel:** Belumo Studio ⭐ (handle belumostudio). Adult animated stories, black comedy / sci-fi, US audience. Long-form 3–4 min episodes + Shorts/Reels/TikTok clips.
- **Series:** *Department of Unfortunate Outcomes*. Deadpan office satire about the people who deal with the worst outcomes and make them slightly worse.
- **Division of work:** the user makes images (own image generator), voices (ElevenLabs free plan, Voice Library voices) and AI clips (Google Flow / Veo, ~950 credits). Claude writes scripts and prompts, edits, adds effects, subtitles, music mix and exports, and writes upload metadata.
- **Constraints:** no monetization for now. ElevenLabs free plan needs attribution "elevenlabs.io", no commercial use. AI-content label required on every upload. Music only from YouTube Audio Library (or licensed).
- **User preferences:** prefers Claude to edit static shots with effects instead of re-animating them in Flow (Ep1 shots 1, 3, 4, 12, 13 are effects-only). Dislikes shaking doors/tables/camera and anything making Dolores look like a schoolgirl. Complained about blocky/choppy video, so the high-quality pipeline below is mandatory.

## 2. Characters (consistent blocks, keep exactly)
- **GARY:** 52-year-old tired man, thinning gray-brown hair, heavy dark circles under his eyes, rumpled beige short-sleeve shirt, loosened mustard-yellow tie, lanyard with ID badge, permanently unimpressed expression.
- **VERA:** office AI shown as a glowing teal ring mounted on the ceiling, with a single narrow horizontal light slit in the middle like an eye, soft teal glow.
- **DOLORES:** 22-year-old intern, chin-length pastel pink bob, huge unsettling smile, oversized gray blazer, intern lanyard, holding a thick binder, wide bright eyes. (Adult styling only.)
- **BRENDA:** mid-40s accountant, messy brown bun, round glasses, olive cardigan, coffee stain on her sleeve, exhausted and panicked expression.
- **HOLE (Ep1):** perfectly black floating sphere with thin bright orange ring of light, small objects bending toward it.
- **IXX (Ep2, new):** tall thin alien ambassador, smooth pale sage-green skin, narrow elongated head, two large round glossy black eyes, no nose, small calm mouth, stiff dark-teal ceremonial robe with mustard-yellow sash, six-fingered long hands, tiny paper VISITOR badge, serene polite expression.
- **Style line:** `2D adult animated series style, flat colors with subtle film grain, thick slightly uneven black outlines, muted retro-corporate palette of teal, mustard yellow, beige and dusty orange, 1960s sci-fi office aesthetic, deadpan mood, flat lighting, cinematic 16:9, no text, no logos, no watermark`
- **Voices:** Narrator (deep dry corporate-training male), Gary (tired gravelly baritone), VERA (cool clipped female AI), Dolores (bright manic early-20s), Brenda (frazzled mid-40s), Vendor (call-center recording), Ixx (calm formal male, Ep2).

## 3. Episode 1 "Black Hole in Accounting" – state: finished and delivered
13 shots, 196.0 s, 24 fps. Docs artifact with script, prompts, 39-line voice sheet: https://claude.ai/artifact/18JyacWpKSAduPczL4Pjmo
Delivered files (user has them as downloads): `episode1_full_v8_music.mp4` (final, 1920×1080, with music/SFX), `episode1_full_v7.mp4` (no music), `episode1_subtitles.srt` (absolute timeline), `thumbnail_ep1.jpg`, `episode1_teaser_9x16_v3.mp4` (40.5 s YT teaser with music), `short2_phone_9x16_music.mp4`, `short3_paperwork_9x16_music.mp4`, `ep1_teaser_tiktok_instagram.mp4` (safe-zone layout, "LINK IN BIO" end card), cover images for Shorts, channel banner and avatar (`banner_belumo_studio.jpg`, `avatar_option_A_star.jpg`), `frames/shotNN_start.png` (13 start frames).
Shot timing (s): 1: 0–13.214, 2: –25.216, 3: –44.419, 4: –56.319, 5: –72.011, 6: –89.935, 7: –101.413, 8: –116.233, 9: –133.854, 10: –153.145, 11: –161.045, 12: –180.895, 13: –196.017.
Flow clips used (1280×720, 24 fps, ~7.93 s): shots 2, 5, 6, 7, 8, 9, 10, 11. Clips were cut early and last frame held, because Veo changed expressions/added objects at clip ends.

## 4. Episode 2 "First Contact, Wrong Address" – state: script written, assets not made
Docs artifact: https://claude.ai/artifact/GxttHhw4WuXyGK6Z159bqG (copy in `ep02-first-contact/ep02-doc.md`).
Premise: day after Ep1 (Gary is an unpaid intern, Department legally doesn't exist). Alien Ambassador Ixx arrives at the wrong address. Earth has 11 minutes to file Form 7-J (14 pages, notarized) or is "reassigned to a mining company". Printer is out of toner, Dave the notary is in Portugal. Resolution: a non-existent entity cannot be rejected, only "pending": Earth placed on hold for 600 years. Next-episode tease: "Dolores Files a Complaint".
Plan: Flow-animate shots 6, 8, 5, 10, 2, 11; effects-only shots 1, 3, 4, 7, 9, 12, 13.
**Next steps for the user:** generate the Ixx character sheet, then 13 start frames, 44 voice files (`s{shot}_{nn}_{speaker}.mp3`), Flow clips, pick music/SFX. Then Claude builds the episode (rebuild shot timing table from final voice files), subtitles, mix, thumbnail, Shorts, TikTok/IG version.

## 5. Production pipeline (what worked; reuse it)
**Video rendering rules (quality):**
- Never use ffmpeg `zoompan` (jittery). Do pans/zooms with OpenCV `warpAffine` (sub-pixel, `INTER_CUBIC`) on frames, pipe raw RGB into ONE ffmpeg x264 encode.
- Encode: `-preset medium -crf 15–17 -x264-params aq-mode=3 -profile:v high`, bt709 tags, `-vf scale=out_color_matrix=bt709:out_range=tv,format=yuv420p`, 24 fps native. One render at a time; long renders in the background.
- Flow clips are 720p: upscale with Lanczos + mild unsharp (`addWeighted(up,1.25,blur,-0.25)`), hold last frame with slow sub-pixel zoom. Advise user to download highest resolution Flow offers.
- 9:16 layout (1080×1920): 1080×1080 foreground window panned sub-pixel at y=400 over a blurred, darkened (×0.72), noise-dithered background; title block at top; subtitles lower. For TikTok/IG, subtitles at MarginV 1250 and titles shifted down ~90 px to avoid UI.
- Subtitles via ASS (`ass=file.ass:fontsdir=<poppins dir>`), font Poppins, colors per speaker: VERA &H00D0E04D&, Dolores &H00AA8CFF&, Vendor &H00C8C8C8&, others white. Use plain `\N` for line breaks in ASS.
- Fade in 0.6 s / out 0.9 s on full episodes. Shorts end with a 3 s end card ("FULL EPISODE ON YOUTUBE / belumostudio").

**Audio:**
- Voice mix `audio_v4.m4a` (mono 44.1 kHz) = ElevenLabs voices + Flow clip audio under voices; its build scripts were lost (rebuild a voice-assembly script for Ep2). Music mix `pipeline/mix.sh` adds: main bed (−28 dB), tension track (−27 dB, shots 7–11), ambient hum (−8 dB), stinger-track tail (−27 dB at the end), phone ring (+8 dB), paper rustle (+2 dB, 130–153 s), window smash as final "bum" (−6 dB at 186.6 s). Final loudness `loudnorm=I=-15:TP=-1.5:LRA=9`.
- Music/SFX come from YouTube Audio Library (user-selected). Music is ~18 dB under voices on purpose.
- Shorts cut points must be in silent gaps of the voice track (found via silencedetect).

**Veo/Flow prompt lessons:** pin the camera in words, keep facial expressions, describe only small movements, avoid "grows/pulled in/yanked" (causes explosions or extra objects), keep black hole unchanged, mouths closed unless stated. Master prefix is in the Ep2 doc.

**Design assets:** thumbnails 1280×720 with a bottom dark gradient, yellow headline + white second line + "CASE #00N" badge. Shorts cover 1080×1920 with text top and "FULL EPISODE ON THE CHANNEL / belumostudio". Channel banner 2560×1440 with text kept in the 1546×423 safe area. Covers: crop a 1080×1080 window from the start frame, blurred darkened background, Poppins-Bold, gold #E8B33A, yellow #FFD640. Banner: shot 5 start frame resized to 2560×1440, ×0.42 darkening, centre vignette band, star polygon (10 points, inner radius 0.42·R), "BELUMO STUDIO" at 122 px in the safe area.

## 6. Upload checklist and templates
- Order: full episode first, then teaser Short right after (set "Related video"), pinned comment, other Shorts a few days later. Playlists: "Full Episodes" and "Shorts". Set "altered or synthetic content" = Yes, "made for kids" = No, monetization off.
- Description footer: "This video is AI-generated: visuals, voices and music were created with AI tools and licensed audio. Voices: elevenlabs.io. Music and sound effects: YouTube Audio Library." Add author attribution if a track requires it.
- Ep1 title: "A Black Hole Appeared in Accounting. Nobody Filed the Paperwork. | Department of Unfortunate Outcomes S1E1". Ep2 title/description/tags/pinned comment are in the Ep2 doc.
- TikTok/IG: the link goes in bio (no clickable link in video or caption); enable AI-generated labels; check the YouTube Audio Library licence covers those platforms.
- Channel description short version: "Belumo Studio ⭐ adult animated stories: black comedy and sci-fi. Series: Department of Unfortunate Outcomes. New cases regularly. AI-generated visuals and voices."

## 7. Ep1 source files (reconstruct if needed)
Flow clips (`Stapler_slides…`, `Gary_pulling_vacuum…`, `Characters_in_office…`, `Characters_orbit…`, `Gary_slumps_at_phone…`, `Characters_pointing…`, `Characters_react…`, `Black_hole_vanishes…`), ElevenLabs voice files, and the music/SFX mp3s (main bed "hlavní podkres", tension "napětí", ambient hum, stinger track, phone ring, radiation suit rustle, smashing car window). Ask the user to re-attach what is needed; `pipeline/` shows exactly how everything was assembled.
