"""Sestaví Ep2 (16:9, 1920×1080, 24 fps) z počátečních snímků, Flow klipů a hlasové stopy.

Použití: python3 build_ep02.py [test]
  test  – uloží jen náhledový obrázek efektů (build/fx_test.png), nic nerenderuje
Vstup:  ep02-first-contact/frames/shotNN_start.png, clips/shotNN.mp4, build/voice.wav, build/timing.json
Výstup: ep02-first-contact/build/episode2_v1.mp4 (bez hudby), build/ep.ass

Pravidla kvality z Ep1: žádný zoompan, pohyb kamery jen sub-pixel warpAffine, jeden x264 encode.
"""
import json, math, subprocess, sys, time
from pathlib import Path
import cv2, numpy as np

ROOT = Path(__file__).resolve().parent.parent
EP = ROOT / "ep02-first-contact"; OUT = EP / "build"; FONTS = ROOT / "fonts"
W, H, FPS = 1920, 1080, 24
TM = json.loads((OUT / "timing.json").read_text())
SH = {int(k): v for k, v in TM["shots"].items()}
NF = {k: round(b * FPS) - round(a * FPS) for k, (a, b) in SH.items()}

# ---------- Flow klipy: (přehrát od, do) a pak ping-pong v rozsahu (od, do); zoom na celý záběr
CL = {2: dict(play=(0, 170), pp=(100, 170), zoom=(1.0, 1.04), c=(.55, .45)),
      5: dict(play=(0, 190), pp=(60, 190), zoom=(1.0, 1.04), c=(.45, .45)),
      6: dict(play=(0, 190), pp=(0, 190), zoom=(1.0, 1.05), c=(.5, .45)),
      8: dict(play=(48, 190), pp=(100, 190), zoom=(1.0, 1.05), c=(.45, .45)),
      11: dict(play=(0, 190), pp=(60, 190), zoom=(1.0, 1.05), c=(.5, .4))}
# ---------- efektové záběry: zoom (od, do), střed (fx, fy), efekty
FX = {1: dict(zoom=(1.0, 1.08), c=(.62, .4), fx=["teal"], tealbox=(1300, 200, 1920, 340)),
      3: dict(zoom=(1.0, 1.10), c=(.5, .35), fx=["teal", "shimmer"]),
      4: dict(zoom=(1.0, 1.06), c=(.35, .45), fx=["teal"], tealbox=(1000, 0, 1920, 300)),
      7: dict(zoom=(1.0, 1.10), c=(.3, .45), fx=["teal", "shimmer"]),
      9: dict(zoom=(1.0, 1.08), c=(.55, .65), fx=["teal"]),
      10: dict(zoom=(1.0, 1.06), c=(.6, .5), fx=["teal", "beacon"]),
      12: dict(zoom=(1.0, 1.08), c=(.35, .6), fx=["teal", "flash"]),
      13: dict(zoom=(1.0, 1.0), c=(.5, .5), fx=["saucer"])}


def load_frame(k):
    im = cv2.cvtColor(cv2.imread(str(EP / "frames" / f"shot{k:02d}_start.png")), cv2.COLOR_BGR2RGB)
    return cv2.resize(im, (W, H), interpolation=cv2.INTER_LANCZOS4)


def cam(f, z, cx, cy):
    if abs(z - 1) < 1e-6: return f
    x0 = (W - W / z) * cx; y0 = (H - H / z) * cy
    return cv2.warpAffine(f, np.float32([[z, 0, -x0 * z], [0, z, -y0 * z]]), (W, H), flags=cv2.INTER_CUBIC)


def setup_fx(k):
    base = load_frame(k); st = {}; cfg = FX[k]
    r, g, b = [base[..., i].astype(np.int16) for i in range(3)]
    if "teal" in cfg["fx"]:
        m = ((g > 170) & (b > 150) & (r < 160) & (g - r > 50)).astype(np.float32)
        if "tealbox" in cfg:
            x0, y0, x1, y1 = cfg["tealbox"]; keep = np.zeros_like(m); keep[y0:y1, x0:x1] = 1; m *= keep
        st["glow"] = np.clip(cv2.GaussianBlur(m, (0, 0), 18) + 0.6 * cv2.GaussianBlur(m, (0, 0), 5), 0, 1)[..., None]
        st["core"] = cv2.GaussianBlur(m, (0, 0), 2)[..., None]
    if "beacon" in cfg["fx"]:
        m = ((r > 190) & (g < 110) & (b < 110)).astype(np.float32); keep = np.zeros_like(m); keep[230:400, 1600:1900] = 1; m *= keep
        st["red"] = np.clip(cv2.GaussianBlur(m, (0, 0), 20) * 1.5 + cv2.GaussianBlur(m, (0, 0), 4), 0, 1)[..., None]
        st["redcore"] = cv2.GaussianBlur(m, (0, 0), 3)[..., None]
    if "saucer" in cfg["fx"]:
        x0, y0, x1, y1 = 1570, 115, 1820, 215
        roi = base[y0:y1, x0:x1].astype(np.float32)
        sky = np.median(np.concatenate([roi[:6].reshape(-1, 3), roi[-6:].reshape(-1, 3)]), axis=0)
        m = (np.linalg.norm(roi - sky, axis=2) > 28).astype(np.uint8)
        m = cv2.dilate(cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)), np.ones((5, 5), np.uint8))
        full = np.zeros((H, W), np.uint8); full[y0:y1, x0:x1] = m
        st["bg"] = cv2.inpaint(base, full * 255, 7, cv2.INPAINT_TELEA)
        st["spr"] = base[y0:y1, x0:x1].copy(); st["sm"] = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.2)[..., None]
        st["pos"] = (x0, y0)
    return base, st


def fx_frame(k, n, N, base, st):
    cfg = FX[k]; t = n / FPS; a = n / max(1, N - 1)
    f = base.astype(np.float32)
    if "saucer" in cfg["fx"]:
        f = st["bg"].astype(np.float32)
        u = min(1.0, max(0.0, (t - 1.0) / 8.0)); e = u * u * (3 - 2 * u)
        s = 1.0 - 0.75 * e; dx = -260 * e; dy = -95 * e + 3 * math.sin(2 * math.pi * 0.4 * t)
        spr = cv2.resize(st["spr"], None, fx=s, fy=s, interpolation=cv2.INTER_AREA).astype(np.float32)
        sm = cv2.resize(st["sm"], None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
        if sm.ndim == 2: sm = sm[..., None]
        sm = sm * (1 - e) ** 0.7
        x0, y0 = st["pos"]; h0, w0 = st["spr"].shape[:2]
        cx = x0 + w0 / 2 + dx; cy = y0 + h0 / 2 + dy
        M = np.float32([[1, 0, cx - spr.shape[1] / 2], [0, 1, cy - spr.shape[0] / 2]])
        L = cv2.warpAffine(spr, M, (W, H), flags=cv2.INTER_LINEAR)
        A = cv2.warpAffine(sm, M, (W, H), flags=cv2.INTER_LINEAR)[..., None]
        f = f * (1 - A) + L * A
    if "teal" in cfg["fx"]:
        p = 0.5 + 0.5 * math.sin(2 * math.pi * 0.6 * t)
        amp = 0.14 + 0.22 * p
        if "shimmer" in cfg["fx"]: amp += 0.06 * math.sin(2 * math.pi * 3.1 * t) * math.sin(2 * math.pi * 0.37 * t)
        if "flash" in cfg["fx"]: amp += 0.9 * math.exp(-((t - 0.45) / 0.18) ** 2)
        f += st["glow"] * np.array([60, 255, 225], np.float32) * amp + st["core"] * 40 * amp
    if "beacon" in cfg["fx"]:
        on = 0.5 + 0.5 * math.tanh(4 * math.sin(2 * math.pi * 1.1 * t))
        f += st["red"] * np.array([255, 40, 30], np.float32) * (0.15 + 0.55 * on) - st["redcore"] * 70 * (1 - on)
    s = math.sin(2 * math.pi * 0.5 * t); f *= np.array([1 + 0.012 * s, 1 + 0.007 * s, 1 - 0.004 * s], np.float32)
    f = np.clip(f, 0, 255).astype(np.uint8)
    z0, z1 = cfg["zoom"]; e = a * a * (3 - 2 * a)
    return cam(f, z0 + (z1 - z0) * e, *cfg["c"])


def prep(fr):
    up = cv2.resize(fr, (W, H), interpolation=cv2.INTER_LANCZOS4)
    return cv2.addWeighted(up, 1.25, cv2.GaussianBlur(up, (0, 0), 1.1), -0.25, 0)


def clip_frames(k):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", str(EP / "clips" / f"shot{k:02d}.mp4"), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       capture_output=True, check=True).stdout
    w, h = 1280, 720
    return np.frombuffer(p, np.uint8).reshape(-1, h, w, 3)


def shot_frames(k):
    N = NF[k]
    if k in FX:
        base, st = setup_fx(k)
        for n in range(N): yield fx_frame(k, n, N, base, st)
        return
    cfg = CL[k]; raw = clip_frames(k); last = len(raw) - 1
    a, b = cfg["play"]; b = min(b, last); seq = list(range(a, b + 1))
    c, d = cfg["pp"]; d = min(d, last); fwd = False
    while len(seq) < N:
        seg = list(range(c, d + 1)) if fwd else list(range(d, c - 1, -1))
        seq += seg[1:]; fwd = not fwd
    z0, z1 = cfg["zoom"]
    for n, i in enumerate(seq[:N]):
        e = n / max(1, N - 1); e = e * e * (3 - 2 * e)
        yield cam(prep(raw[i]), z0 + (z1 - z0) * e, *cfg["c"])


COL = {"VERA": "&H00D0E04D&", "Dolores": "&H00AA8CFF&", "Vendor": "&H00C8C8C8&", "Ixx": "&H00B4E6BE&"}


def tf(v): v = max(0, v); return f"{int(v // 3600)}:{int(v % 3600 // 60):02d}:{v % 60:05.2f}"


def write_ass():
    hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Poppins,58,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,1,2,200,200,70,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    ev = [f"Dialogue: 0,{tf(l['start'])},{tf(l['end'] + 0.12)},Default,,0,0,0,,{{\\c{COL.get(l['speaker'], '&H00FFFFFF&')}}}{l['text']}\n" for l in TM["lines"]]
    (OUT / "ep.ass").write_text(hdr + "".join(ev), encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        ims = []
        for k in FX:
            base, st = setup_fx(k); N = NF[k]; n = int(min(N - 1, 4.5 * FPS))
            ims.append(cv2.resize(fx_frame(k, n, N, base, st), (640, 360)))
        sheet = np.zeros((720, 640 * 4, 3), np.uint8)
        for i, im in enumerate(ims): sheet[(i // 4) * 360:(i // 4 + 1) * 360, (i % 4) * 640:(i % 4 + 1) * 640] = im
        cv2.imwrite(str(OUT / "fx_test.png"), cv2.cvtColor(sheet, cv2.COLOR_RGB2BGR)); print("fx_test.png"); sys.exit()
    write_ass()
    TOTAL = sum(NF.values()); dur = TOTAL / FPS
    vf = (f"ass={OUT / 'ep.ass'}:fontsdir={FONTS},fade=t=in:st=0:d=0.6,fade=t=out:st={dur - 0.9:.2f}:d=0.9,"
          "scale=out_color_matrix=bt709:out_range=tv,format=yuv420p")
    af = f"loudnorm=I=-15:TP=-1.5:LRA=9,afade=t=out:st={dur - 1.0:.2f}:d=1.0,aformat=sample_rates=44100:channel_layouts=stereo"
    out = OUT / "episode2_v1.mp4"
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-i", str(OUT / "voice.wav"), "-vf", vf, "-af", af,
           "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-x264-params", "aq-mode=3", "-profile:v", "high",
           "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-c:a", "aac", "-b:a", "256k", "-t", f"{dur:.3f}", "-movflags", "+faststart", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); t0 = time.time(); n = 0
    for k in sorted(SH):
        c = 0
        for fr in shot_frames(k): p.stdin.write(fr.tobytes()); n += 1; c += 1
        print("shot", k, "frames", c, "/", NF[k], round(time.time() - t0), "s", flush=True)
    p.stdin.close(); p.wait(); print("done", n, "frames rc", p.returncode, round(time.time() - t0), "s", flush=True)
