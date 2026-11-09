import os, subprocess, importlib.util, numpy as np, cv2
U="/mnt/user-data/uploads/"; FPS=24
spec=importlib.util.spec_from_file_location("fx","/home/claude/work/fxshots.py"); fx=importlib.util.module_from_spec(spec); spec.loader.exec_module(fx); fx.FPS=24
T={1:(0.0,13.214),2:(13.214,25.216),3:(25.216,44.419),4:(44.419,56.319),5:(56.319,72.011),6:(72.011,89.935),7:(89.935,101.413),8:(101.413,116.233),9:(116.233,133.854),10:(133.854,153.145),11:(153.145,161.045),12:(161.045,180.895),13:(180.895,196.017)}
B={k:(round(a*FPS),round(b*FPS)) for k,(a,b) in T.items()}   # frame boundaries
TOTAL=B[13][1]
# shot -> (clip file, clip frames used, zoom end, fx, fy)
CL={2:("Stapler_slides_toward_black_hole_28f59c83.mp4",89,1.06,.5,.6),7:("Gary_pulling_vacuum_hose_d23873f2.mp4",146,1.06,.5,.55),
    6:("Characters_in_office_with_black_a844b6c4.mp4",125,1.05,.4,.5),5:("Characters_orbit_black_hole_148ec6c1.mp4",190,1.05,.5,.55),
    8:("Gary_slumps_at_phone_desk_14ae73b2.mp4",190,1.05,.5,.55),9:("Characters_pointing_toward_black__cefe22c3.mp4",190,1.05,.55,.6),
    10:("Characters_react_near_black_hole_f1df2967.mp4",190,1.05,.4,.5),11:("Black_hole_vanishes_and_confetti__1be32342.mp4",190,1.0,.5,.5)}
_fxcache={}
def _fx(k):
    if k not in _fxcache: _fxcache[k]=fx.make(k)
    return _fxcache[k]
def prep(fr):
    up=cv2.resize(fr,(1920,1080),interpolation=cv2.INTER_LANCZOS4)
    return cv2.addWeighted(up,1.25,cv2.GaussianBlur(up,(0,0),1.1),-0.25,0)
def shot_frames(k,i0=0,i1=None):
    """yield RGB 1920x1080 frames i0..i1-1 of shot k (24 fps)"""
    a,b=B[k]; N=b-a; i1=N if i1 is None else min(i1,N)
    if k in fx.EFF:
        base,st=_fx(k)
        for i in range(i0,i1): yield fx.frame(k,i,N,base,st)
        return
    name,n,zend,fxp,fyp=CL[k]
    p=subprocess.Popen(["ffmpeg","-v","error","-i",U+name,"-frames:v",str(n),"-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
    last=None; sz=1280*720*3
    for j in range(n):
        raw=p.stdout.read(sz)
        if len(raw)<sz: break
        if j>=i0 and j<i1: last=prep(np.frombuffer(raw,np.uint8).reshape(720,1280,3)); yield last
        elif j<i0: pass
        if j>=i1-1 and i1<=n: break
        if j==n-1 and last is None and i0>=n:   # need last frame only
            last=prep(np.frombuffer(raw,np.uint8).reshape(720,1280,3))
    p.stdout.close(); p.kill()
    if i1>n:
        if last is None:
            p=subprocess.Popen(["ffmpeg","-v","error","-i",U+name,"-frames:v",str(n),"-f","rawvideo","-pix_fmt","rgb24","-"],stdout=subprocess.PIPE)
            raw=b""
            for j in range(n): raw=p.stdout.read(sz)
            p.stdout.close(); p.kill(); last=prep(np.frombuffer(raw,np.uint8).reshape(720,1280,3))
        Nh=max(1,N-n)
        for i in range(max(i0,n),i1):
            j=i-n; z=1.0+(zend-1.0)*(j/max(1,Nh-1)); 
            if z==1.0: yield last; continue
            x0=(1920-1920/z)*fxp; y0=(1080-1080/z)*fyp
            yield cv2.warpAffine(last,np.float32([[z,0,-x0*z],[0,z,-y0*z]]),(1920,1080),flags=cv2.INTER_LINEAR)
