"""Shorts 9:16 (1080×1920) z Ep2. Výřezy jsou celé záběry, takže střihy padají do tichých mezer.

Použití: python3 build_shorts_ep02.py <název>   (yt1 | yt2 | yt3 | tiktok)
Vstup: build/mix.wav, build/timing.json, snímky a klipy (přes build_ep02.shot_frames)
Výstup: build/short_<název>.mp4
"""
import subprocess, sys, time
import cv2, numpy as np
import build_ep02 as E

FPS, END = 24, 3.0
SHORTS = {
 "yt1": dict(shots=[2, 3], t3="CASE #002  ·  WRONG ADDRESS", cx={2: .52, 3: .5}),
 "yt2": dict(shots=[6, 7], t3="CASE #002  ·  IT'S A TUESDAY", cx={6: .5, 7: .48}),
 "yt3": dict(shots=[9, 10, 11], t3="CASE #002  ·  OUT OF TONER", cx={9: .55, 10: .45, 11: .5}),
 "tiktok": dict(shots=[5, 7, 10], t3="CASE #002  ·  FIRST CONTACT", cx={5: .45, 7: .48, 10: .45}, tiktok=True),
}
name = sys.argv[1]; S = SHORTS[name]; TT = S.get("tiktok", False)
SEG = [(k, *E.SH[k]) for k in S["shots"]]
noise = np.random.RandomState(1).normal(0, 2.2, (1920, 1080, 1)).astype(np.float32)
FG_Y = 400 + (90 if TT else 0)


def compose(f, cx):
    x0 = max(0.0, min(840.0, 1920 * cx - 540))
    fg = cv2.warpAffine(f, np.float32([[1, 0, -x0], [0, 1, 0]]), (1080, 1080), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    fg = cv2.addWeighted(fg, 1.3, cv2.GaussianBlur(fg, (0, 0), 1.2), -0.3, 0)
    sm = cv2.GaussianBlur(cv2.resize(f, (427, 240), interpolation=cv2.INTER_AREA)[:, 146:281], (0, 0), 5)
    bg = cv2.resize(sm, (1080, 1920), interpolation=cv2.INTER_CUBIC).astype(np.float32) * 0.72 + noise
    c = np.clip(bg, 0, 255).astype(np.uint8); c[FG_Y:FG_Y + 1080] = fg; return c


def frames():
    last = None
    for k, a, b in SEG:
        for f in E.shot_frames(k): last = compose(f, S["cx"][k]); yield last
    ec = np.clip(cv2.GaussianBlur(last, (0, 0), 16).astype(np.float32) * 0.62, 0, 255).astype(np.uint8)
    for _ in range(int(END * FPS)): yield ec


# ---- časy: každý záběr v shortu začíná tam, kde skončil předchozí
offs, t = {}, 0.0
for k, a, b in SEG: offs[k] = (a, t); t += E.NF[k] / FPS
D = t; TOTAL = D + END
# ---- zvuk: výřezy z mixu s krátkými přechody
parts, fl = [], []
for i, (k, a, b) in enumerate(SEG):
    d = E.NF[k] / FPS
    fl.append(f"[0:a]atrim={a:.3f}:{a + d:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.08,afade=t=out:st={d - 0.12:.3f}:d=0.12[s{i}]")
    parts.append(f"[s{i}]")
fl.append("".join(parts) + f"concat=n={len(parts)}:v=0:a=1,apad=whole_dur={TOTAL:.3f},loudnorm=I=-14:TP=-1.5:LRA=9,aformat=sample_rates=44100:channel_layouts=stereo[o]")
wav = E.OUT / f"short_{name}.wav"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(E.OUT / "mix.wav"), "-filter_complex", ";".join(fl), "-map", "[o]", "-t", f"{TOTAL:.3f}", str(wav)], check=True)
# ---- titulky
mv_sub = 1250 if TT else 1525; dy = 90 if TT else 0
hdr = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Sub,Poppins,62,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,1,8,60,60,{mv_sub},1
Style: T1,Poppins,44,&H003AB3E8,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,3,0,1,4,0,8,40,40,{95 + dy},1
Style: T2,Poppins,70,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,0,8,30,30,{148 + dy},1
Style: T3,Poppins,34,&H00C9E3F2,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,8,30,30,{262 + dy},1
Style: End,Poppins,80,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,0,5,40,40,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
tf = E.tf
ev = [f"Dialogue: 0,{tf(0)},{tf(D)},T1,,0,0,0,,DEPARTMENT OF", f"Dialogue: 0,{tf(0)},{tf(D)},T2,,0,0,0,,UNFORTUNATE OUTCOMES",
      f"Dialogue: 0,{tf(0)},{tf(D)},T3,,0,0,0,,{S['t3']}"]
for l in E.TM["lines"]:
    for k, a, b in SEG:
        if a <= l["start"] < b:
            o = offs[k][1] - a
            ev.append(f"Dialogue: 0,{tf(l['start'] + o)},{tf(min(l['end'] + 0.12, b) + o)},Sub,,0,0,0,,{{\\c{E.COL.get(l['speaker'], '&H00FFFFFF&')}}}{l['text']}")
end1, end2 = ("LINK IN BIO", "@belumostudio") if TT else ("FULL EPISODE\\NON YOUTUBE", "belumostudio")
ev.append(f"Dialogue: 0,{tf(D + 0.15)},{tf(TOTAL)},End,,0,0,0,,{{\\an5\\pos(540,{820 + dy})\\fad(250,0)}}{end1}")
ev.append(f"Dialogue: 0,{tf(D + 0.4)},{tf(TOTAL)},End,,0,0,0,,{{\\an5\\pos(540,{1075 + dy})\\fs52\\c&H003AB3E8&\\fad(250,0)}}{end2}")
ass = E.OUT / f"short_{name}.ass"; ass.write_text(hdr + "\n".join(ev) + "\n", encoding="utf-8")
vf = f"ass={ass}:fontsdir={E.FONTS},fade=t=in:st=0:d=0.3,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"
out = E.OUT / f"short_{name}.mp4"
cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-r", "24", "-i", "-", "-i", str(wav), "-vf", vf,
       "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-x264-params", "aq-mode=3", "-profile:v", "high",
       "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
       "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE); t0 = time.time(); n = 0
for fr in frames(): p.stdin.write(fr.tobytes()); n += 1
p.stdin.close(); p.wait(); print(name, "done", n, "frames", round(time.time() - t0), "s rc", p.returncode, flush=True)
