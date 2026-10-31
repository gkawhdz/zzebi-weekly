import math, os, subprocess, shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W,H,FPS,DUR=1080,1920,30,7.0
FD="/usr/share/fonts/opentype/noto/"
def F(s,w="Black"): return ImageFont.truetype(FD+f"NotoSansCJK-{w}.ttc",s,index=1)
def SF(s): return ImageFont.truetype(FD+"NotoSerifCJK-Black.ttc",s,index=1)
TEAL=(0,168,168); WHITE=(255,255,255)
src=Image.open("/home/claude/work/img23.jpg").convert("RGB")
sc=H/src.height; bg=src.resize((int(src.width*sc),H),Image.LANCZOS)
x0=(bg.width-W)//2; bg=bg.crop((x0,0,x0+W,H))
big=src.resize((int(src.width*sc*2.6),int(H*2.6)),Image.LANCZOS)
def ease(t): t=max(0,min(1,t)); return 1-(1-t)**3
def grad(img,top_h,bot_h,a1=200,a2=230):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    for y in range(top_h): d.line([(0,y),(W,y)],fill=(0,0,0,int(a1*(1-y/top_h)**1.3)))
    for y in range(bot_h): d.line([(0,H-bot_h+y),(W,H-bot_h+y)],fill=(0,0,0,int(a2*(y/bot_h)**1.2)))
    img.alpha_composite(ov); return img
# loupe path over the coat (screen coords)
path=[(250,720),(250,710),(300,820),(240,720)]
def lpos(t):
    seg=t*(len(path)-1); i=min(int(seg),len(path)-2); f=seg-i; f=0.5-0.5*math.cos(math.pi*f)
    return path[i][0]+(path[i+1][0]-path[i][0])*f, path[i][1]+(path[i+1][1]-path[i][1])*f
R=190
mask=Image.new("L",(2*R,2*R),0); ImageDraw.Draw(mask).ellipse([0,0,2*R-1,2*R-1],fill=255)
OUT="/home/claude/work/story/fr"; shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT)
N=int(DUR*FPS)
for k in range(N):
    t=k/(N-1); ts=k/FPS
    fr=bg.copy().convert("RGBA")
    fr=fr.filter(ImageFilter.GaussianBlur(0)) 
    fr=grad(fr,820,700)
    lx,ly=lpos(min(1,ts/6.0))
    # loupe content: 2.6x zoom of same point
    bx=int((lx+x0)*2.6-R); by=int(ly*2.6-R)
    lens=big.crop((bx,by,bx+2*R,by+2*R)).convert("RGBA"); lens.putalpha(mask)
    sh=Image.new("RGBA",(W,H),(0,0,0,0)); ImageDraw.Draw(sh).ellipse([lx-R-6,ly-R+10,lx+R+6,ly+R+22],fill=(0,0,0,110))
    fr.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
    fr.alpha_composite(lens,(int(lx-R),int(ly-R)))
    d=ImageDraw.Draw(fr)
    d.ellipse([lx-R,ly-R,lx+R,ly+R],outline=TEAL,width=10); d.ellipse([lx-R-5,ly-R-5,lx+R+5,ly+R+5],outline=WHITE,width=3)
    # top text (y 270~)
    d.text((64,272),"셀럽 스냅 해부 #23 · 릴스에 없는 한 가지",font=F(44,"Bold"),fill=(200,240,238),stroke_width=2,stroke_fill=(0,0,0))
    d.line([(64,334),(184,334)],fill=TEAL,width=6)
    d.text((64,358),"체크 코트가 없다면?",font=F(84),fill=WHITE,stroke_width=4,stroke_fill=(10,10,12))
    # bottom memo card y ~1180-1580
    a=ease((ts-0.4)/0.6)
    card=Image.new("RGBA",(W,H),(0,0,0,0)); cd=ImageDraw.Draw(card)
    cy=1210+int((1-a)*40)
    cd.rounded_rectangle([56,cy,940,cy+300],32,fill=(247,244,238,int(245*a)))
    cd.rectangle([56,cy+30,66,cy+270],fill=TEAL+(int(255*a),))
    cd.text((96,cy+34),"무늬 1개를 얼굴 가까이",font=F(50),fill=(17,17,19,int(255*a)))
    cd.text((96,cy+112),"체크 머플러·스카프만 둘러도",font=F(44,"Bold"),fill=(60,58,54,int(255*a)))
    cd.text((96,cy+170),"무지 코트가 덜 심심해 보여요",font=F(44,"Bold"),fill=(60,58,54,int(255*a)))
    card.putalpha(card.getchannel("A")); fr.alpha_composite(card)
    d=ImageDraw.Draw(fr)
    b=ease((ts-1.2)/0.6)
    if b>0:
        s="4개 포인트 전부는 오늘 릴스에서 →"; f=F(42,"Bold"); w=d.textlength(s,font=f)
        d.rounded_rectangle([64,1528-30,64+w+56,1528+44],37,fill=TEAL+(int(255*b),))
        d.text((92,1535),s,font=f,fill=WHITE+(int(255*b),),anchor="lm")
    d.text((64,1090),"@zzebi.st",font=F(44,"Bold"),fill=WHITE,stroke_width=2,stroke_fill=(0,0,0))
    d.text((920,1114),"AI 재현 이미지",font=F(26,"Medium"),fill=(230,230,230),anchor="rm",stroke_width=2,stroke_fill=(0,0,0))
    fr.convert("RGB").save(f"{OUT}/{k:04d}.jpg",quality=92)
    if k==int(3.0*FPS): fr.convert("RGB").save("/home/claude/work/story/story_23_frame.jpg",quality=94)
subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",f"{OUT}/%04d.jpg","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-movflags","+faststart","/home/claude/work/story/20261031_story_02b.mp4"],check=True)
shutil.rmtree(OUT); print("ok")
