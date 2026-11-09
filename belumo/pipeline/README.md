# Ep1 pipeline (Belumo Studio)

Kód, kterým se v předchozím prostředí skládala epizoda 1. Cesty (`/mnt/user-data/...`, `/home/claude/work/...`) jsou z původního workspace – před použitím je přepište.

| Soubor | Účel |
|---|---|
| `epcore.py` | Časová osa záběrů, načítání Flow klipů (upscale 720p → 1080p, držení posledního snímku se sub-pixel zoomem) |
| `fxshots.py` | Efektové záběry ze statických obrázků (listí, teal glow, flicker, prach, „chvění“ Dolores) |
| `build_ep.py` | Celá epizoda 16:9 s ASS titulky a jedním x264 encodem |
| `build_short.py` | Shorts 9:16 z výřezu epizody, titulky, end card |
| `teaser2.py` | Teaser 9:16 z vybraných záběrů |
| `mix.sh` | Mix hudby a SFX pod hlasovou stopu `audio_v4.m4a` |

Skript na sestavení hlasové stopy (`audio_v4.m4a`) se ztratil – pro Ep2 je potřeba napsat nový.
