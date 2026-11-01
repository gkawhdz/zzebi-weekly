# 셀럽 스냅 해부 스토리 2026-11-01 — ① 목 높이 3단계 선화 카드 + 대체템(정지) ② 컬러 스와치 추출 모션
import os, sys, shutil, subprocess, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
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
def chip(d,x,y,s,f,bg,fg=WHITE,pad=26,h=74):
    w=d.textlength(s,font=f); d.rounded_rectangle([x,y,x+w+2*pad,y+h],h//2,fill=bg); d.text((x+pad,y+h/2),s,font=f,fill=fg,anchor="lm"); return w+2*pad
def footer(d):
    d.text((64,1584),"@zzebi.st",font=F(34,"Bold"),fill=WHITE,anchor="ls")
    d.text((1016,1584),"AI 재현 이미지",font=F(30,"Medium"),fill=(210,210,210),anchor="rs")

def neck_icon(w,h,kind,sel):
    ic=Image.new("RGBA",(w,h),(0,0,0,0)); d=ImageDraw.Draw(ic)
    d.rounded_rectangle([0,0,w-1,h-1],26,fill=(TEAL if sel else PAPER)+(240,))
    col=WHITE if sel else INK
    cx=w//2; top=60
    # 몸판(어깨선) + 목선 높이만 다르게 그린 단순 선화
    d.line([(cx-110,top+140),(cx-46,top+86),(cx+46,top+86),(cx+110,top+140)],fill=col,width=7,joint="curve")
    if kind==0: d.arc([cx-46,top+56,cx+46,top+120],0,180,fill=col,width=7)
    if kind==1:
        d.rectangle([cx-40,top+50,cx+40,top+88],outline=col,width=7)
    if kind==2:
        d.rectangle([cx-40,top+6,cx+40,top+88],outline=col,width=7)
        for yy in range(top+22,top+84,16): d.line([(cx-30,yy),(cx+30,yy)],fill=col,width=3)
    nm=["라운드","반폴라","터틀넥"][kind]
    d.text((cx,h-58),nm,font=F(44),fill=col,anchor="mm")
    return ic

def story1():
    on=Image.open(WK+"img24.jpg").convert("RGB")
    sc=H/on.height; bg=on.resize((int(on.width*sc*1.35),int(H*1.35)),Image.LANCZOS)
    x0=(bg.width-W)//2; bg=bg.crop((x0,0,x0+W,H))      # 리브 결이 보이게 상반신 확대
    fr=bg.convert("RGBA")
    fr=vgrad(fr,0,640,215,40); fr=vgrad(fr,1040,H,40,235)
    d=ImageDraw.Draw(fr)
    d.text((64,276),"셀럽 스냅 해부 #24 · 릴스에 없는 한 가지",font=F(40,"Bold"),fill=(200,240,238),stroke_width=2,stroke_fill=(0,0,0))
    d.line([(64,336),(184,336)],fill=TEAL,width=6)
    d.text((64,356),"목 높이 3단계",font=SF(92),fill=WHITE,stroke_width=3,stroke_fill=(10,10,12))
    d.text((64,486),"가죽재킷 안, 높을수록 단정해 보여요",font=F(44,"Bold"),fill=WHITE,stroke_width=2,stroke_fill=(0,0,0))
    for i in range(3):
        fr.alpha_composite(neck_icon(292,300,i,i==2),(64+i*306,590))
    d=ImageDraw.Draw(fr)
    d.text((64+2*306+146,912),"▲ 오늘 룩",font=F(40,"Bold"),fill=WHITE,anchor="mm",stroke_width=2,stroke_fill=(0,0,0))
    cy=1110
    card=Image.new("RGBA",(884,300),(14,14,16,215)); m=Image.new("L",(884,300),0); ImageDraw.Draw(m).rounded_rectangle([0,0,883,299],30,fill=215); card.putalpha(m)
    cd=ImageDraw.Draw(card); cd.rounded_rectangle([0,0,883,299],30,outline=TEAL,width=4)
    cd.text((40,34),"터틀넥이 답답하다면?",font=F(52),fill=(120,220,216))
    cd.text((40,116),"목이 반만 올라오는 블랙 반폴라",font=F(44,"Bold"),fill=WHITE)
    cd.text((40,176),"(모크넥)도 비슷한 효과예요",font=F(44,"Bold"),fill=WHITE)
    fr.alpha_composite(card,(56,cy))
    d=ImageDraw.Draw(fr)
    chip(d,64,1440,"4개 포인트 전부는 릴스에서 ↑",F(42,"Bold"),TEAL,pad=30,h=58)
    footer(d)
    fr.convert("RGB").save(WK+"story_24.jpg",quality=94)

def story2():
    src=Image.open(WK+"img25.jpg").convert("RGB")
    sc=H/src.height; big=src.resize((int(src.width*sc*1.1),int(H*1.1)),Image.LANCZOS)
    pts=[("진청",(640,330)),("블랙",(750,360)),("진청",(600,860))]
    cols=[]
    for nm,(x,y) in pts:
        px=[src.getpixel((x+i,y+j)) for i in range(-12,13,4) for j in range(-12,13,4)]
        cols.append((nm,tuple(sum(p[k] for p in px)//len(px) for k in range(3))))
    DUR=7.0; N=int(DUR*FPS)
    OUT=WK+"story/fr2"; shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT)
    for k in range(N):
        ts=k/FPS; t=k/(N-1)
        z=1.0+0.1*t                                  # 천천히 밀어 들어가는 프레임 모션
        bw,bh=int(W*z/1.1*1.1),int(H*z/1.1*1.1)
        s=z/1.1; vw,vh=int(W/s* (1)),int(H/s)
        cx=big.width/2+40; cy=big.height*0.44
        bx=int(cx-W/(2*s)*1.0); by=int(cy-H/(2*s))
        bx=max(0,min(big.width-int(W/s),bx)); by=max(0,min(big.height-int(H/s),by))
        fr=big.crop((bx,by,bx+int(W/s),by+int(H/s))).resize((W,H),Image.BILINEAR).convert("RGBA")
        fr=vgrad(fr,0,560,200,0); fr=vgrad(fr,1150,H,0,235)
        d=ImageDraw.Draw(fr)
        d.text((64,276),"셀럽 스냅 해부 #25 · 릴스에 없는 한 가지",font=F(40,"Bold"),fill=(200,240,238),stroke_width=2,stroke_fill=(0,0,0))
        d.line([(64,336),(184,336)],fill=TEAL,width=6)
        d.text((64,356),"청 · 검 · 청",font=SF(96),fill=WHITE,stroke_width=3,stroke_fill=(10,10,12))
        d.text((64,486),"사진에서 뽑은 오늘의 색 순서",font=F(44,"Bold"),fill=WHITE,stroke_width=2,stroke_fill=(0,0,0))
        for i,(nm,c) in enumerate(cols):
            a=ease((ts-0.3-i*0.35)/0.5)
            if a<=0: continue
            x=64+int((1-a)*-80); y=600+i*170
            sw=Image.new("RGBA",(330,146),(0,0,0,0)); sd=ImageDraw.Draw(sw)
            sd.rounded_rectangle([0,0,329,145],24,fill=PAPER+(int(240*a),))
            sd.rounded_rectangle([14,14,132,131],18,fill=c+(int(255*a),),outline=(255,255,255,int(255*a)),width=3)
            sd.text((154,73),nm,font=F(52),fill=INK+(int(255*a),),anchor="lm")
            fr.alpha_composite(sw,(x,y))
            if i<2:
                aa=ease((ts-0.9-i*0.35)/0.4)
                if aa>0: ImageDraw.Draw(fr).line([(64+165,y+146),(64+165,y+146+24*aa)],fill=TEAL+(255,),width=6)
        b=ease((ts-1.8)/0.6)
        if b>0:
            cy=1110+int((1-b)*40)
            card=Image.new("RGBA",(884,300),PAPER+(int(246*b),)); m=Image.new("L",(884,300),0); ImageDraw.Draw(m).rounded_rectangle([0,0,883,299],30,fill=int(246*b)); card.putalpha(m)
            cd=ImageDraw.Draw(card); cd.rectangle([0,30,10,270],fill=TEAL)
            cd.text((40,34),"블랙 소매 재킷이 없다면?",font=F(52),fill=INK)
            cd.text((40,116),"청바지에 검정 벨트 하나만",font=F(44,"Bold"),fill=(60,58,54))
            cd.text((40,176),"둘러 허리를 끊어도 OK",font=F(44,"Bold"),fill=(60,58,54))
            fr.alpha_composite(card,(56,cy))
        d=ImageDraw.Draw(fr)
        c2=ease((ts-2.6)/0.5)
        if c2>0: chip(d,64,1440,"4개 포인트 전부는 릴스에서 ↑",F(42,"Bold"),TEAL+(int(255*c2),),pad=30,h=58)
        footer(d)
        fr.convert("RGB").save(f"{OUT}/{k:04d}.jpg",quality=92)
        if abs(ts-4.0)<1e-6 or k==120: fr.convert("RGB").save(WK+"story_25_frame.jpg",quality=92)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",OUT+"/%04d.jpg","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-pix_fmt","yuv420p","-crf","18","-c:a","aac","-movflags","+faststart",WK+"story_25.mp4"],check=True)
    shutil.rmtree(OUT)
story1(); story2(); print("ok")
