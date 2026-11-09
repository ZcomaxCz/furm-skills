"""Vytvoří titulky (SRT) z narace: každá scéna se rozdělí na krátké řádky,
časy se rozpočítají podle počtu znaků v rámci délky scény.

Použití: python3 srt.py <složka projektu>
"""
import json
import re
import sys
from pathlib import Path

proj = Path(sys.argv[1])
GAP = 0.35
MAXLEN = 84  # max znaků na titulek (2 řádky)
scenes = json.loads((proj / "scenes.json").read_text(encoding="utf-8"))["scenes"]
durs = json.loads((proj / "audio" / "durations.json").read_text())


def chunks(text):
    out = []
    for sent in re.split(r"(?<=[.!?…])\s+", text.strip()):
        while len(sent) > MAXLEN:
            cut = max(sent.rfind(sep, 0, MAXLEN) for sep in (", ", " – ", " "))
            out.append(sent[:cut].strip(" ,"))
            sent = sent[cut:].strip(" ,–")
        if sent:
            out.append(sent)
    return out


def ts(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


lines, t, n = [], 0.0, 1
for s in scenes:
    d = durs[s["id"]]
    parts = chunks(s["narration"])
    total = sum(len(p) for p in parts)
    cur = t
    for p in parts:
        dur = d * len(p) / total
        lines += [str(n), f"{ts(cur)} --> {ts(cur + dur - 0.05)}", p, ""]
        cur += dur
        n += 1
    t += d + GAP
(proj / "titulky.cs.srt").write_text("\n".join(lines), encoding="utf-8")
print(n - 1, "titulků")
