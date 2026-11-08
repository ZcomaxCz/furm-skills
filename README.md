# FURM skills

Skilly pro Claude Code pro tvorbu YouTube obsahu na český a slovenský kanál.

| Skill | Účel |
|---|---|
| `brand-voice` | Profil stylu psaní ze skutečných textů a přepisů |
| `content-engine` | Scénáře, obsahové plány, přizpůsobení pro platformy |
| `video-editing` | Střih videa (FFmpeg, Remotion, ElevenLabs, fal.ai, Descript/CapCut), efekty pro DaVinci Resolve Fusion |
| `remotion-video-creation` | Pravidla pro tvorbu videí v Reactu pomocí Remotionu |
| `security-review` | Bezpečnostní checklist pro kód a cloud |

## Instalace

V relaci Claude Code s tímto repozitářem se skilly z `.claude/skills/` načtou automaticky. Pro použití mimo repozitář je zkopírujte ručně:

```bash
mkdir -p ~/.claude/skills && cp -r .claude/skills/* ~/.claude/skills/
```
