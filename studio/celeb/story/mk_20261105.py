from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess, os, math
W,H=1080,1920; TEAL=(0,168,168)
def F(sz,kind="SansB"):
    p={"SansB":"/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc","Sans":"/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc","Serif":"/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc","Black":"/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"}[kind]
    return ImageFont.truetype(p,sz,index=1)
def halves(path):
    im=Image.open(path).convert("RGB")
    A=im.crop((0,345,512,1255)).resize((W,H),Image.LANCZOS)
    B=im.crop((512,345,1024,1255)).resize((W,H),Image.LANCZOS)
    return A,B
def grad(img, top=(0,700,190), bot=(1250,1920,200)):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    for y in range(top[0],top[1]):
        a=int(top[2]*(1-(y-top[0])/(top[1]-top[0]))); d.line([(0,y),(W,y)],fill=(10,10,12,a))
    for y in range(bot[0],bot[1]):
        a=int(bot[2]*((y-bot[0])/(bot[1]-bot[0]))); d.line([(0,y),(W,y)],fill=(10,10,12,a))
    o=img.convert("RGBA"); o.alpha_composite(ov); return o
def foot(d, ep):
    # 아래 320px 안전영역 위(1600 이하)에 작은 표기
    d.text((60,1500),f"셀럽 스냅 해부 #{ep} · @zzebi.st",font=F(36,"SansB"),fill=(255,255,255))
    d.text((60,1542),"AI 재현 이미지",font=F(30,"Sans"),fill=(225,225,225))
def button(d, s, y=1420):
    f=F(46,"SansB"); w=d.textlength(s,font=f)
    d.rounded_rectangle([60,y,60+w+64,y+92],46,fill=TEAL)
    d.text((92,y+46),s,font=f,fill=(255,255,255),anchor="lm")
def ease(t): t=max(0,min(1,t)); return t*t*(3-2*t)

# ---- 스토리 1: 플랫레이 → 착장 와이프 리빌 모션 (7초)
A,B=halves("/home/claude/work/img30.jpg")
os.makedirs("/home/claude/work/story/f1",exist_ok=True)
FPS=30; N=7*FPS
for k in range(N):
    t=k/FPS
    z=1.0+0.03*t/7
    def zoom(im):
        w2,h2=int(W/z),int(H/z); x0=(W-w2)//2; y0=(H-h2)//2
        return im.crop((x0,y0,x0+w2,y0+h2)).resize((W,H),Image.BILINEAR)
    a=zoom(A); b=zoom(B)
    p=ease((t-1.6)/1.8); dx=int(W*p)
    fr=a.copy()
    if dx>0: fr.paste(b.crop((0,0,dx,H)),(0,0))
    fr=grad(fr); d=ImageDraw.Draw(fr)
    if 0<dx<W: d.line([(dx,0),(dx,H)],fill=(255,255,255,255),width=8); d.ellipse([dx-30,960-30,dx+30,960+30],fill=TEAL+(255,),outline=(255,255,255,255),width=4)
    # 위 250px 아래부터 글자
    chip=F(40,"SansB"); cs="옷만" if p<0.5 else "입으면"
    cw=d.textlength(cs,font=chip); d.rounded_rectangle([60,280,60+cw+48,346],33,fill=(255,255,255,235)); d.text((84,313),cs,font=chip,fill=(20,20,22),anchor="lm")
    hl=["펼쳐 둔 아이템 5개,","입으면 이렇게"] if p<0.5 else ["같은 5개,","바지 밑단만 다르면?"]
    pan=Image.new("RGBA",(W,H),(0,0,0,0)); pd=ImageDraw.Draw(pan)
    pw=max(pd.textlength(l_,font=F(84,"Serif")) for l_ in hl)
    pd.rounded_rectangle([36,366,60+pw+40,606],22,fill=(10,10,12,150)); pd.rectangle([36,366,46,606],fill=TEAL+(255,))
    fr.alpha_composite(pan); d=ImageDraw.Draw(fr)
    y=380
    for ln in hl:
        d.text((60,y),ln,font=F(84,"Serif"),fill=(255,255,255)); y+=112
    if t>3.6:
        al=int(255*ease((t-3.6)/0.6))
        lay=Image.new("RGBA",(W,H),(0,0,0,0)); ld=ImageDraw.Draw(lay)
        f=F(46,"SansB"); s="밑단 정답은 오늘 릴스 3번에서 ↑"; w=ld.textlength(s,font=f)
        ld.rounded_rectangle([60,1400,60+w+64,1492],46,fill=TEAL+(al,)); ld.text((92,1446),s,font=f,fill=(255,255,255,al),anchor="lm")
        fr.alpha_composite(lay); d=ImageDraw.Draw(fr)
    foot(d,"30")
    fr.convert("RGB").save(f"/home/claude/work/story/f1/{k:04d}.jpg",quality=90)
subprocess.run(["ffmpeg","-loglevel","error","-y","-framerate","30","-i","/home/claude/work/story/f1/%04d.jpg","-c:v","libx264","-pix_fmt","yuv420p","-crf","20","-movflags","+faststart","/home/claude/work/story/20261105_story_30.mp4"],check=True)

# ---- 스토리 2: 매거진 표지형 큰 숫자 '1' (정지)
A,B=halves("/home/claude/work/img31.jpg")
fr=B.convert("RGBA")
ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
for x in range(0,760):
    od.line([(x,0),(x,H)],fill=(8,10,16,int(205*(1-x/760)**1.3)))
fr.alpha_composite(ov); fr=grad(fr,top=(0,500,150),bot=(1300,1920,190)); d=ImageDraw.Draw(fr)
d.text((40,250),"1",font=F(560,"Serif"),fill=TEAL+(255,))
d.text((70,900),"비싸 보이는 데",font=F(78,"Serif"),fill=(255,255,255))
d.text((70,1004),"필요한 광택은",font=F(78,"Serif"),fill=(255,255,255))
d.text((70,1108),"딱 한 곳",font=F(78,"Serif"),fill=(255,255,255))
d.line([(72,1222),(232,1222)],fill=TEAL,width=7)
d.text((70,1250),"상의도, 치마도 아니에요",font=F(48,"SansB"),fill=(235,235,235))
button(d,"어디인지는 오늘 릴스 3번에서 ↑",y=1340)
d.text((60,1462),"셀럽 스냅 해부 #31 · @zzebi.st",font=F(36,"SansB"),fill=(255,255,255))
d.text((60,1512),"AI 재현 이미지",font=F(30,"Sans"),fill=(225,225,225))
fr.convert("RGB").save("/home/claude/work/story/20261105_story_31.jpg",quality=92)
