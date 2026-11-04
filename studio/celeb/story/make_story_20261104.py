# 셀럽 스냅 해부 스토리 2026-11-04 — ① 에디터 메모 대화(말풍선이 차례로 뜨는 7초 모션) ② '이러면 등산룩' 체크리스트(정지 jpg)
import os, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H,FPS=1080,1920,30
FD="/usr/share/fonts/opentype/noto/"
def F(s,w="Black"): return ImageFont.truetype(FD+f"NotoSansCJK-{w}.ttc",s,index=1)
def SF(s,w="Black"): return ImageFont.truetype(FD+f"NotoSerifCJK-{w}.ttc",s,index=1)
TEAL=(0,168,168); WHITE=(255,255,255); INK=(17,17,19); PAPER=(247,244,238)
WK="/home/claude/work/"
def ease(t): t=max(0,min(1,t)); return 1-(1-t)**3
def vgrad(img,y0,y1,a0,a1,col=(0,0,0)):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    for y in range(y0,y1):
        t=(y-y0)/max(1,(y1-y0-1)); d.line([(0,y),(W,y)],fill=col+(int(a0+(a1-a0)*t),))
    img.alpha_composite(ov); return img
def chip(d,x,y,s,f,bg,fg=WHITE,pad=30,h=70):
    w=d.textlength(s,font=f); d.rounded_rectangle([x,y,x+w+2*pad,y+h],h//2,fill=bg); d.text((x+pad,y+h/2),s,font=f,fill=fg,anchor="lm"); return w+2*pad
def footer(d):
    d.text((64,1580),"@zzebi.st",font=F(34,"Bold"),fill=WHITE,anchor="ls")
    d.text((1016,1580),"AI 재현 이미지",font=F(30,"Medium"),fill=(215,215,215),anchor="rs")
def wrap(d,s,f,maxw):
    out=[];line=""
    for wd in s.split(" "):
        c=(line+" "+wd).strip()
        if d.textlength(c,font=f)>maxw and line: out.append(line); line=wd
        else: line=c
    out.append(line); return out

def base28(k):
    src=Image.open(WK+"img28.jpg").convert("RGB")
    s=1.25+0.06*k/(7*FPS)  # 아주 천천히 밀어 들어감
    big=src.resize((int(src.width*s),int(src.height*s)),Image.LANCZOS)
    cx,cy=int(520*s),int(900*s); x0=max(0,min(big.width-W,cx-W//2)); y0=max(0,min(big.height-H,cy-H//2))
    fr=Image.new("RGBA",(W,H),(14,16,20,255)); fr.paste(big.crop((x0,y0,x0+W,y0+H)),(0,0))
    ov=Image.new("RGBA",(W,H),(10,14,20,120)); fr.alpha_composite(ov)
    fr=vgrad(fr,0,700,230,40,(10,14,20)); fr=vgrad(fr,1150,1920,0,235,(10,14,20))
    return fr

BUB=[("q","정장 재킷엔 어떤 청바지가 좋아요?",0.6),
     ("a","진청이나 미드블루 일자핏이요. 너무 연한 청은 따로 놀아요.",1.6),
     ("q","기장은 어디까지요?",3.0),
     ("a","로퍼 등에 살짝 닿을 만큼. 바닥에 쌓이면 다시 캐주얼해져요.",4.0)]

def story1():
    out=WK+"story_frames1"; shutil.rmtree(out,ignore_errors=True); os.makedirs(out)
    N=7*FPS
    for k in range(N):
        t=k/FPS; fr=base28(k); d=ImageDraw.Draw(fr)
        d.text((64,272),"셀럽 스냅 해부 #28 · 에디터 메모",font=F(40,"Bold"),fill=(200,240,238))
        d.line([(64,334),(184,334)],fill=TEAL,width=6)
        d.text((64,356),"청바지 고를 때",font=SF(92),fill=WHITE)
        d.text((64,470),"딱 2가지만",font=SF(92),fill=WHITE)
        y=640
        for role,s,t0 in BUB:
            a=ease((t-t0)/0.35)
            f=F(44,"Bold") if role=="q" else F(44,"Medium")
            lines=wrap(d,s,f,640); bh=len(lines)*62+56; bw=max(d.textlength(l,font=f) for l in lines)+64
            if a>0:
                lay=Image.new("RGBA",(W,H),(0,0,0,0)); ld=ImageDraw.Draw(lay)
                dy=int((1-a)*40)
                if role=="q":
                    x=64; ld.rounded_rectangle([x,y+dy,x+bw,y+dy+bh],34,fill=PAPER+(int(245*a),))
                    for i,l in enumerate(lines): ld.text((x+32,y+dy+28+i*62),l,font=f,fill=INK+(int(255*a),))
                else:
                    x=W-64-bw; ld.rounded_rectangle([x,y+dy,x+bw,y+dy+bh],34,fill=TEAL+(int(245*a),))
                    for i,l in enumerate(lines): ld.text((x+32,y+dy+28+i*62),l,font=f,fill=WHITE+(int(255*a),))
                fr.alpha_composite(lay)
            y+=bh+30
        d=ImageDraw.Draw(fr)
        if t>5.0:
            chip(d,64,1420,"4개 포인트 전부는 오늘 릴스에서 ↑",F(40,"Bold"),TEAL)
        footer(d)
        fr.convert("RGB").save(f"{out}/{k:04d}.jpg",quality=92)
    subprocess.run(["ffmpeg","-loglevel","error","-y","-framerate",str(FPS),"-i",f"{out}/%04d.jpg","-c:v","libx264","-pix_fmt","yuv420p","-crf","18","-movflags","+faststart",WK+"20261104_story_01.mp4"],check=True)
    shutil.copy(f"{out}/{N-1:04d}.jpg",WK+"story_01_last.jpg")

def xmark(d,x,y,s,col,w=8):
    d.line([(x,y),(x+s,y+s)],fill=col,width=w); d.line([(x+s,y),(x,y+s)],fill=col,width=w)
def story2():
    src=Image.open(WK+"img29b.jpg").convert("RGB"); s=1.32
    big=src.resize((int(src.width*s),int(src.height*s)),Image.LANCZOS)
    x0=int(560*s)-W//2-120; y0=int(820*s)-H//2
    x0=max(0,min(big.width-W,x0)); y0=max(0,min(big.height-H,y0))
    fr=Image.new("RGBA",(W,H),(16,16,18,255)); fr.paste(big.crop((x0,y0,x0+W,y0+H)),(0,0))
    fr=vgrad(fr,0,760,235,30,(12,12,14)); fr=vgrad(fr,1100,1920,0,240,(12,12,14))
    d=ImageDraw.Draw(fr)
    d.text((64,272),"셀럽 스냅 해부 #29 · 릴스에 없는 한 가지",font=F(40,"Bold"),fill=(200,240,238))
    d.line([(64,334),(184,334)],fill=TEAL,width=6)
    d.text((64,356),"이러면 등산룩",font=SF(96),fill=WHITE)
    d.text((64,476),"이 3개만 피하세요",font=SF(96),fill=WHITE)
    chip(d,720,668,"비교용 연출",F(32,"Bold"),(40,40,44),pad=22,h=56)
    # 체크리스트 카드 (오른쪽 140px 비움)
    items=["바지까지 나일론","발에는 등산화","지퍼는 턱 끝까지"]
    y=650
    for s_ in items:
        lay=Image.new("RGBA",(W,H),(0,0,0,0)); ld=ImageDraw.Draw(lay)
        ld.rounded_rectangle([64,y,700,y+104],26,fill=(20,20,24,200))
        lay=lay; fr.alpha_composite(lay); d=ImageDraw.Draw(fr)
        d.rounded_rectangle([92,y+24,148,y+80],10,outline=WHITE,width=5)
        xmark(d,104,y+36,32,TEAL,8)
        d.text((176,y+52),s_,font=F(50,"Bold"),fill=WHITE,anchor="lm")
        y+=124
    # 릴스에 없는 팁 카드(종이)
    cy=1060
    d.rounded_rectangle([64,cy,940,cy+300],30,fill=PAPER)
    d.text((104,cy+40),"하나 더",font=F(36,"Bold"),fill=TEAL)
    tip="소매 고무단은 팔꿈치 쪽으로 살짝 밀어 올리세요. 손목이 보이면 운동복 느낌이 줄어요."
    for i,l in enumerate(wrap(d,tip,F(44,"Bold"),790)): d.text((104,cy+96+i*64),l,font=F(44,"Bold"),fill=INK)
    chip(d,64,1400,"해결법 2개는 오늘 릴스에서 ↑",F(40,"Bold"),TEAL)
    d.text((64,1580),"@zzebi.st",font=F(34,"Bold"),fill=WHITE,anchor="ls")
    d.text((1016,1580),"AI 재현 · 비교용 연출(실제 착장 아님)",font=F(30,"Medium"),fill=(215,215,215),anchor="rs")
    fr.convert("RGB").save(WK+"20261104_story_02.jpg",quality=94)

if __name__=="__main__":
    story1(); story2()
