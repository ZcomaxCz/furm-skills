import os, sys, time, subprocess, importlib.util, numpy as np, cv2
os.chdir("/home/claude/work/tz")
spec=importlib.util.spec_from_file_location("fx","/home/claude/work/fxshots.py"); fx=importlib.util.module_from_spec(spec); spec.loader.exec_module(fx)
FPS=24; fx.FPS=24
MODE=sys.argv[1]; PRESET=sys.argv[2] if len(sys.argv)>2 else "medium"
OUT="/home/claude/work/tz/test_q.mp4" if MODE=="test" else "/mnt/user-data/outputs/episode1_teaser_9x16_v2.mp4"
NA,NB,NC,ND,NE=257,233,97,314,72
if MODE=="test": NA,NB,NC,ND,NE=40,40,0,0,0
noise=np.random.RandomState(1).normal(0,2.2,(1920,1080,1)).astype(np.float32)
b3,s3=fx.make(3); b12,s12=fx.make(12); N3=round(19.203*FPS); N12=round(19.85*FPS)
def clipframe(d,idx): 
    im=cv2.cvtColor(cv2.imread(f"{d}/f{idx+1:04d}.png"),cv2.COLOR_BGR2RGB)
    return cv2.resize(im,(1920,1080),interpolation=cv2.INTER_LANCZOS4)
def compose(f,cx):
    x0=max(0.0,min(840.0,1920*cx-540))
    fg=cv2.warpAffine(f,np.float32([[1,0,-x0],[0,1,0]]),(1080,1080),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
    fg=cv2.addWeighted(fg,1.35,cv2.GaussianBlur(fg,(0,0),1.2),-0.35,0)
    sm=cv2.resize(f,(427,240),interpolation=cv2.INTER_AREA)[:,146:281]
    sm=cv2.GaussianBlur(sm,(0,0),5)
    bg=cv2.resize(sm,(1080,1920),interpolation=cv2.INTER_CUBIC).astype(np.float32)*0.72+noise
    canvas=np.clip(bg,0,255).astype(np.uint8); canvas[400:1480]=fg
    return canvas
def cxB(t): return 0.46-0.04*t/3.6 if t<3.6 else (0.42-0.12*(t-3.6)/1.4 if t<5.0 else 0.30)
def gen():
    for i in range(NA):
        t=i/FPS; yield compose(fx.frame(3,7+i,N3,b3,s3),0.45+0.03*t/10.7)
    for i in range(NB):
        idx=132+i if i<58 else 188-(i-58); yield compose(clipframe("c5",idx),cxB(i/FPS))
    for i in range(NC):
        yield compose(clipframe("c11",i),0.50+0.12*(i/FPS)/4.05)
    last=None
    for i in range(ND):
        t=i/FPS; last=compose(fx.frame(12,4+i,N12,b12,s12),0.33+0.07*t/13.1); yield last
    if NE:
        ec=np.clip(cv2.GaussianBlur(last,(0,0),16).astype(np.float32)*0.62,0,255).astype(np.uint8)
        for i in range(NE): yield ec
vf="ass=teaser.ass:fontsdir=/usr/share/fonts/truetype/google-fonts,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"
cmd=["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s","1080x1920","-r","24","-i","-","-i","teaser_audio.wav","-vf",vf,
 "-c:v","libx264","-preset",PRESET,"-crf","15","-x264-params","aq-mode=3","-profile:v","high","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709",
 "-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",OUT]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE); t0=time.time(); n=0
for fr in gen():
    p.stdin.write(fr.tobytes()); n+=1
    if n%100==0: print(n,round(time.time()-t0),"s",flush=True)
p.stdin.close(); p.wait(); print("done",n,"frames",round(time.time()-t0),"s rc",p.returncode,flush=True)
