import os, sys, time, subprocess
os.chdir("/home/claude/work/ep")
from epcore import *
# ---------- subtitles (16:9)
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
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Poppins,58,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,1,2,200,200,70,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
ev=[]
for b in open("/mnt/user-data/outputs/episode1_subtitles.srt",encoding="utf-8").read().strip().split("\n\n"):
    l=b.split("\n"); a,c=l[1].split(" --> "); t=" ".join(l[2:])
    ev.append(f"Dialogue: 0,{tf(tp(a))},{tf(tp(c)+0.12)},Default,,0,0,0,,{{\\c{col(t)}}}{t}\n")
open("ep.ass","w",encoding="utf-8").write(hdr+"".join(ev))
dur=TOTAL/FPS
vf=f"ass=ep.ass:fontsdir=/usr/share/fonts/truetype/google-fonts,fade=t=in:st=0:d=0.6,fade=t=out:st={dur-0.9:.2f}:d=0.9,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"
af=f"loudnorm=I=-15:TP=-1.5:LRA=9,afade=t=out:st={dur-1.0:.2f}:d=1.0,aformat=sample_rates=44100:channel_layouts=stereo"
OUT="/mnt/user-data/outputs/episode1_full_v7.mp4"
cmd=["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s","1920x1080","-r","24","-i","-","-i","../audio_v4.m4a","-vf",vf,"-af",af,
 "-c:v","libx264","-preset","medium","-crf","17","-x264-params","aq-mode=3","-profile:v","high","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709",
 "-c:a","aac","-b:a","256k","-t",f"{dur:.3f}","-movflags","+faststart",OUT]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE); t0=time.time(); n=0
for k in range(1,14):
    cnt=0
    for fr in shot_frames(k):
        p.stdin.write(fr.tobytes()); n+=1; cnt+=1
    exp=B[k][1]-B[k][0]
    print("shot",k,"frames",cnt,"expected",exp,"total",n,round(time.time()-t0),"s",flush=True)
p.stdin.close(); p.wait(); print("done",n,"of",TOTAL,"rc",p.returncode,round(time.time()-t0),"s",flush=True)
