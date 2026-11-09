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


SHORT = {"a", "i", "v", "ve", "s", "se", "z", "ze", "k", "ke", "o", "u", "na", "do", "že"}  # nekončit řádek předložkou/spojkou


def split_long(sent):
    """Dlouhou větu rozdělí na části do MAXLEN, řez hledá co nejblíž středu."""
    if len(sent) <= MAXLEN:
        return [sent]
    mid = len(sent) // 2
    ok = lambda i: min(i, len(sent) - i) >= 25  # žádné krátké zbytky
    cands = [i for i in range(len(sent)) if sent.startswith((", ", " – "), i) and ok(i)] or \
            [i for i, c in enumerate(sent) if c == " " and ok(i)
             and sent[:i].split()[-1].lower() not in SHORT]
    cut = min(cands, key=lambda i: abs(i - mid))
    left, right = sent[:cut].strip(" ,"), sent[cut:].strip(" ,–")
    return split_long(left) + split_long(right)


def chunks(text):
    text = text.replace("R.U.R.", "R\u2024U\u2024R\u2024")  # zkratka nesmí ukončit větu
    out = []
    for sent in re.split(r"(?<=[.!?…])\s+", text.strip()):
        out += [p.replace("\u2024", ".") for p in split_long(sent) if p]
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
