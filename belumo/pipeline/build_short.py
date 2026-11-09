import os, sys, time, subprocess, numpy as np, cv2
os.chdir("/home/claude/work/ep")
from epcore import *
SHORTS={
 "phone":dict(out="/mnt/user-data/outputs/short2_phone_9x16.mp4",a0=90.1,a1=115.0,
   cx=[(90.0,0.48),(101.40,0.62),(101.45,0.50),(115.0,0.53)],t3="CASE #001  ·  THE VACUUM CLEANER SOLUTION"),
 "paper":dict(out="/mnt/user-data/outputs/short3_paperwork_9x16.mp4",a0=116.4,a1=152.7,
   cx=[(116.4,0.40),(133.80,0.55),(133.85,0.35),(147.0,0.38),(152.7,0.62)],t3="CASE #001  ·  FEED IT"),
}
name=sys.argv[1]; S=SHORTS[name]; a0,a1=S["a0"],S["a1"]; END=3.0
g0,g1=round(a0*FPS),round(a1*FPS); NM=g1-g0; NE=int(END*FPS); D=NM/FPS
noise=np.random.RandomState(1).normal(0,2.2,(1920,1080,1)).astype(np.float32)
kt=[p[0] for p in S["cx"]]; kc=[p[1] for p in S["cx"]]
def compose(f,cx):
    x0=max(0.0,min(840.0,1920*cx-540))
    fg=cv2.warpAffine(f,np.float32([[1,0,-x0],[0,1,0]]),(1080,1080),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
    fg=cv2.addWeighted(fg,1.3,cv2.GaussianBlur(fg,(0,0),1.2),-0.3,0)
    sm=cv2.GaussianBlur(cv2.resize(f,(427,240),interpolation=cv2.INTER_AREA)[:,146:281],(0,0),5)
    bg=cv2.resize(sm,(1080,1920),interpolation=cv2.INTER_CUBIC).astype(np.float32)*0.72+noise
    c=np.clip(bg,0,255).astype(np.uint8); c[400:1480]=fg; return c
def frames():
    g=g0; last=None
    while g<g1:
        k=[kk for kk in B if B[kk][0]<=g<B[kk][1]][0]; a,b=B[k]; e=min(g1,b)
        for j,f in enumerate(shot_frames(k,g-a,e-a)):
            t=(g+j)/FPS; last=compose(f,float(np.interp(t,kt,kc))); yield last
        g=e
    ec=np.clip(cv2.GaussianBlur(last,(0,0),16).astype(np.float32)*0.62,0,255).astype(np.uint8)
    for i in range(NE): yield ec
# ---- audio
TOTAL=D+END
af=(f"[0:a]atrim={a0}:{a1},asetpts=PTS-STARTPTS,afade=t=in:d=0.05,afade=t=out:st={D-0.15:.3f}:d=0.15,apad=whole_dur={TOTAL:.3f},"
    f"loudnorm=I=-15:TP=-1.5:LRA=9,aformat=sample_rates=44100:channel_layouts=stereo[o]")
subprocess.run(["ffmpeg","-y","-v","error","-i","../audio_v4.m4a","-filter_complex",af,"-map","[o]","-t",f"{TOTAL:.3f}",f"{name}_audio.wav"],check=True)
# ---- subs
def tp(s):
    h,m,r=s.split(":"); sec,ms=r.split(","); return int(h)*3600+int(m)*60+int(sec)+int(ms)/1000
def tf(v): v=max(0,v); return f"{int(v//3600)}:{int(v%3600//60):02d}:{v%60:05.2f}"
VERA=("Gary.","Case number one","A black hole in an accounting","I haven","Every other","At the same time","It grows every","Dave is currently","It’s the first intelligent","Technically correct","A black hole forms when","Good news","The Department","We no longer","Worse.","You’re now an unpaid")
DOL=("Gary!","Hi!","I’m Dolores","I died","It slows down","Is that all of it","Welcome to the club")
VEN=("Thank you for calling","Returns are accepted","Press one to hear")
def col(t):
    if t.startswith(DOL): return "&H00AA8CFF&"
    if t.startswith(VEN): return "&H00C8C8C8&"
    if t.startswith(VERA): return "&H00D0E04D&"
    return "&H00FFFFFF&"
hdr="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Sub,Poppins,62,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,1,8,60,60,1525,1
Style: T1,Poppins,44,&H003AB3E8,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,3,0,1,4,0,8,40,40,95,1
Style: T2,Poppins,70,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,5,0,8,30,30,148,1
Style: T3,Poppins,34,&H00C9E3F2,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,8,30,30,262,1
Style: End,Poppins,80,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,0,5,40,40,0,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
ev=[f"Dialogue: 0,{tf(0)},{tf(D)},T1,,0,0,0,,DEPARTMENT OF",f"Dialogue: 0,{tf(0)},{tf(D)},T2,,0,0,0,,UNFORTUNATE OUTCOMES",f"Dialogue: 0,{tf(0)},{tf(D)},T3,,0,0,0,,{S['t3']}"]
for b in open("/mnt/user-data/outputs/episode1_subtitles.srt",encoding="utf-8").read().strip().split("\n\n"):
    l=b.split("\n"); a,c=l[1].split(" --> "); t=" ".join(l[2:]); s=tp(a); e=tp(c)+0.12
    if s>=a0-0.05 and s<a1-0.2: ev.append(f"Dialogue: 0,{tf(s-a0)},{tf(min(e,a1)-a0)},Sub,,0,0,0,,{{\\c{col(t)}}}{t}")
ev.append(f"Dialogue: 0,{tf(D+0.15)},{tf(TOTAL)},End,,0,0,0,,{{\\an5\\pos(540,800)\\fad(250,0)}}FULL EPISODE\\NON YOUTUBE")
ev.append(f"Dialogue: 0,{tf(D+0.4)},{tf(TOTAL)},End,,0,0,0,,{{\\an5\\pos(540,1075)\\fs52\\c&H003AB3E8&\\fad(250,0)}}belumostudio")
open(f"{name}.ass","w",encoding="utf-8").write(hdr+"\n".join(ev)+"\n")
vf=f"ass={name}.ass:fontsdir=/usr/share/fonts/truetype/google-fonts,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"
cmd=["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s","1080x1920","-r","24","-i","-","-i",f"{name}_audio.wav","-vf",vf,
 "-c:v","libx264","-preset","medium","-crf","15","-x264-params","aq-mode=3","-profile:v","high","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709",
 "-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",S["out"]]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE); t0=time.time(); n=0
for fr in frames():
    p.stdin.write(fr.tobytes()); n+=1
p.stdin.close(); p.wait(); print(name,"done",n,"frames",round(time.time()-t0),"s rc",p.returncode,flush=True)
