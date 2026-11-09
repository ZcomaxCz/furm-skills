import numpy as np, cv2, math, random, subprocess, sys
from PIL import Image, ImageDraw
W,H,FPS=1920,1080,25
FR="/mnt/user-data/outputs/frames/"
S={1:(0.0,13.214),3:(25.216,44.419),4:(44.419,56.319),12:(161.045,180.895),13:(180.895,196.017)}
Z={1:(1.0,1.10,.55,.62,.5,.5),3:(1.0,1.08,.5,.5,.4,.45),4:(1.08,1.08,.3,.7,.5,.5),12:(1.0,1.08,.4,.55,.5,.5),13:(1.1,1.0,.5,.5,.5,.5)}
EFF={1:["leaves"],3:["teal","flick"],4:["dolores"],12:["teal","flick","dust"],13:["teal","flick","dust"]}
yy,xx=np.mgrid[0:H,0:W].astype(np.float32)
def load(k): return cv2.cvtColor(cv2.imread(f"{FR}shot{k:02d}_start.png"),cv2.COLOR_BGR2RGB)
def teal_setup(base,ymax=330):
    r,g,b=[base[...,i].astype(np.int16) for i in range(3)]
    m=((g>185)&(b>170)&(r<150)&(g-r>60)).astype(np.float32); m[ymax:,:]=0
    return np.clip(cv2.GaussianBlur(m,(0,0),22)+0.6*cv2.GaussianBlur(m,(0,0),6),0,1)[...,None], m
_m=np.zeros((H,W),np.float32); cv2.fillPoly(_m,[np.array([(802, 705), (834, 468), (900, 495), (997, 562), (1035, 435), (997, 345), (1002, 195), (1080, 112), (1275, 97), (1410, 150), (1432, 255), (1425, 360), (1477, 397), (1552, 495), (1593, 600), (1575, 750), (1522, 840), (1485, 870), (1477, 960), (1440, 1035), (1230, 1038), (1200, 915), (1110, 855), (1057, 750), (960, 735), (840, 742)],np.int32)],1.0)
DM=cv2.GaussianBlur(_m,(0,0),4)[...,None]
random.seed(11)
dust=[dict(x=random.uniform(0,W),y=random.uniform(0,H),r=random.uniform(2,5),vx=random.uniform(4,12),vy=random.uniform(-14,-5),ph=random.uniform(0,6.28)) for _ in range(46)]
def leaf_sprite():
    im=Image.new("RGBA",(44,26),(0,0,0,0)); d=ImageDraw.Draw(im)
    pts=[(2,13),(14,3),(32,5),(42,13),(32,21),(14,23)]
    d.polygon(pts,fill=(205,125,32,255)); d.line(pts+[pts[0]],fill=(45,28,10,255),width=3); d.line([(6,13),(36,13)],fill=(120,70,20,255),width=2)
    return im
LS=leaf_sprite()
leaves=[dict(off=random.uniform(0,6),life=random.uniform(5,7.5),x0=random.uniform(20,420),sw=random.uniform(.8,1.6),ph=random.uniform(0,6.28),sp=random.uniform(-120,120),sc=random.uniform(.8,1.3)) for _ in range(8)]
def make(k):
    base=load(k); st={}
    if "teal" in EFF[k]: st["glow"],st["m"]=teal_setup(base)
    return base,st
def frame(k,n,N,base,st):
    t=n/FPS; eff=EFF[k]; f=base.astype(np.float32)
    if "dolores" in eff:
        dx=1.2*math.sin(2*math.pi*7*t)+0.6*math.sin(2*math.pi*13*t+1); dy=2.5*math.sin(2*math.pi*1.8*t)
        sh=cv2.warpAffine(base,np.float32([[1,0,dx],[0,1,dy]]),(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
        f=f*(1-DM)+sh*DM
    if "teal" in eff:
        p=0.5+0.5*math.sin(2*math.pi*0.7*t); f+=st["glow"]*np.array([60,255,225],np.float32)*(0.16+0.26*p)
    if "flick" in eff:
        s=math.sin(2*math.pi*0.55*t); f*=np.array([1+0.02*s,1+0.011*s,1-0.006*s],np.float32)
    if "dust" in eff:
        lay=np.zeros((H,W),np.float32)
        for d in dust:
            x=(d["x"]+d["vx"]*t+14*math.sin(0.8*t+d["ph"]))%W; y=(d["y"]+d["vy"]*t)%H
            cv2.circle(lay,(int(x),int(y)),int(d["r"]),0.7+0.3*math.sin(1.3*t+d["ph"]),-1,cv2.LINE_AA)
        lay=cv2.GaussianBlur(lay,(0,0),1.6); f+=lay[...,None]*np.array([255,230,170],np.float32)*0.55
    f=np.clip(f,0,255).astype(np.uint8)
    if "leaves" in eff:
        pil=Image.fromarray(f)
        for l in leaves:
            u=((t+l["off"])%l["life"])/l["life"]; x=l["x0"]+190*u+34*math.sin(2*math.pi*l["sw"]*t+l["ph"]); y=-30+760*u
            s=l["sc"]; sp=LS.resize((int(LS.width*s),int(LS.height*s)),Image.BILINEAR).rotate(l["sp"]*t+l["ph"]*40,expand=True,resample=Image.BICUBIC)
            pil.paste(sp,(int(x-sp.width/2),int(y-sp.height/2)),sp)
        f=np.array(pil)
    z0,z1,fx0,fx1,fy0,fy1=Z[k]; a=n/max(1,N-1); z=z0+(z1-z0)*a; fx=fx0+(fx1-fx0)*a; fy=fy0+(fy1-fy0)*a
    cw,ch=W/z,H/z; x0=(W-cw)*fx; y0=(H-ch)*fy
    return cv2.warpAffine(f,np.float32([[z,0,-x0*z],[0,z,-y0*z]]),(W,H),flags=cv2.INTER_LINEAR)
if __name__=="__main__":
    if sys.argv[1]=="test":
        ims=[]
        for k in (1,3,4,12,13):
            base,st=make(k); N=round((S[k][1]-S[k][0])*FPS); n=int(1.2*FPS)
            im=Image.fromarray(frame(k,n,N,base,st)).resize((640,360)); ImageDraw.Draw(im).text((6,6),f"shot {k}",fill="white"); ims.append(im)
        s=Image.new("RGB",(640*3,360*2))
        for i,im in enumerate(ims): s.paste(im,((i%3)*640,(i//3)*360))
        s.save("fx_test.png")
    else:
        for k in map(int,sys.argv[1:]):
            base,st=make(k); N=round((S[k][1]-S[k][0])*FPS)
            p=subprocess.Popen(["ffmpeg","-y","-v","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p",f"fx{k:02d}.mp4"],stdin=subprocess.PIPE)
            for n in range(N): p.stdin.write(frame(k,n,N,base,st).tobytes())
            p.stdin.close(); p.wait(); print("shot",k,"done",N,flush=True)
