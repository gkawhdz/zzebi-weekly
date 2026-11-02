# 셀럽 스냅 해부 스토리 2026-11-02 — ① 실착 가격표 태그(정지) ② 필름 스트립 세로 스크롤 모션 + 기장 팁
import os, shutil, subprocess, math
from PIL import Image, ImageDraw, ImageFont
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
def chip(d,x,y,s,f,bg,fg=WHITE,pad=30,h=66):
    w=d.textlength(s,font=f); d.rounded_rectangle([x,y,x+w+2*pad,y+h],h//2,fill=bg); d.text((x+pad,y+h/2),s,font=f,fill=fg,anchor="lm"); return w+2*pad
def footer(d):
    d.text((64,1590),"@zzebi.st",font=F(34,"Bold"),fill=WHITE,anchor="ls")
    d.text((1016,1590),"AI 재현 이미지",font=F(30,"Medium"),fill=(215,215,215),anchor="rs")

def story1():
    # 사진을 위로 끌어올려 로퍼·토트가 화면 가운데 오게(아래 빈칸은 인스타 답장창 영역이라 어둡게)
    src=Image.open(WK+"img26.jpg").convert("RGB"); s=1.6
    big=src.resize((int(src.width*s),int(src.height*s)),Image.LANCZOS)
    top=int(1400*s)-1330; x0=int(380*s)-W//2
    fr=Image.new("RGBA",(W,H),(18,16,14,255))
    fr.paste(big.crop((x0,top,x0+W,min(big.height,top+H))),(0,0))
    fr=vgrad(fr,0,620,225,0); fr=vgrad(fr,1150,1548,0,255,(18,16,14))
    d=ImageDraw.Draw(fr)
    d.text((64,272),"셀럽 스냅 해부 #26 · 릴스에 없는 한 가지",font=F(40,"Bold"),fill=(200,240,238),stroke_width=2,stroke_fill=(0,0,0))
    d.line([(64,332),(184,332)],fill=TEAL,width=6)
    d.text((64,350),"이 로퍼, 얼마일까?",font=SF(88),fill=WHITE,stroke_width=3,stroke_fill=(10,10,12))
    d.text((64,474),"실착은 Miu Miu 스웨이드 로퍼",font=F(46,"Bold"),fill=WHITE,stroke_width=2,stroke_fill=(0,0,0))
    # 가격표 태그(살짝 기울임) — 실끈은 틸, 로퍼 쪽으로 늘어뜨림
    tg=Image.new("RGBA",(500,270),(0,0,0,0)); td=ImageDraw.Draw(tg)
    td.polygon([(0,40),(40,0),(500,0),(500,270),(40,270),(0,230)],fill=PAPER+(250,))
    td.ellipse([22,108,52,138],fill=(60,58,54))
    td.text((80,24),"Marie Claire 기준 가격",font=F(34,"Bold"),fill=(110,104,96))
    td.text((80,70),"$1,150",font=SF(104),fill=INK)
    td.text((80,198),"실착 로퍼 기준",font=F(44,"Bold"),fill=(90,84,76))
    tg=tg.rotate(-6,expand=True,resample=Image.BICUBIC)
    tx,ty=500,700
    d.line([(tx+40,ty+150),(735,1230)],fill=TEAL,width=5)
    fr.alpha_composite(tg,(tx,ty))
    d=ImageDraw.Draw(fr)
    d.ellipse([722,1217,748,1243],fill=TEAL,outline=WHITE,width=4)
    # 메모 카드: 릴스에 없는 팁
    card=Image.new("RGBA",(560,330),(14,14,16,0)); m=Image.new("L",card.size,0)
    ImageDraw.Draw(m).rounded_rectangle([0,0,559,329],28,fill=225); card=Image.new("RGBA",card.size,(14,14,16,225)); card.putalpha(m)
    cd=ImageDraw.Draw(card); cd.rounded_rectangle([0,0,559,329],28,outline=TEAL,width=4)
    cd.text((34,30),"비싼 건 값,",font=F(50),fill=(120,220,216))
    cd.text((34,96),"예뻐 보이는 건 색",font=F(50),fill=WHITE)
    cd.text((34,176),"브라운 스웨이드 로퍼 +",font=F(40,"Bold"),fill=(225,225,225))
    cd.text((34,232),"같은 톤 가방이면 OK",font=F(40,"Bold"),fill=(225,225,225))
    fr.alpha_composite(card,(56,1010))
    d=ImageDraw.Draw(fr)
    chip(d,64,1440,"바꾼 3곳 전부는 릴스에서 ↑",F(42,"Bold"),TEAL)
    footer(d)
    fr.convert("RGB").save(WK+"story_26.jpg",quality=94)

def story2():
    src=Image.open(WK+"img27.jpg").convert("RGB")
    # 배경: 사진 풀스크린(살짝 어둡게) + 오른쪽 필름 스트립이 위로 흘러감
    s=H/src.height; bgimg=src.resize((int(src.width*s),H),Image.LANCZOS); bx=(bgimg.width-W)//2
    base=bgimg.crop((bx,0,bx+W,H)).convert("RGBA")
    shade=Image.new("RGBA",(W,H),(8,10,24,120)); base.alpha_composite(shade)
    crops=[(520,1290,440),(490,270,620),(620,240,340),(510,760,660),(520,1290,440)]  # 힐→코트→가방→청바지→힐(루프)
    FW,FH=380,500; tiles=[]
    for cx,cy,sz in crops:
        c=src.crop((cx-sz//2,cy-int(sz*FH/FW)//2,cx+sz//2,cy+int(sz*FH/FW)//2)).resize((FW,FH),Image.LANCZOS)
        tiles.append(c)
    stripW=FW+70; pitch=FH+40
    strip=Image.new("RGBA",(stripW,pitch*len(tiles)+40),(14,14,16,255)); sd=ImageDraw.Draw(strip)
    for i,t in enumerate(tiles):
        strip.paste(t,(35,20+i*pitch))
    for y in range(8,strip.height,44):
        sd.rounded_rectangle([9,y,25,y+22],4,fill=(235,232,226)); sd.rounded_rectangle([stripW-25,y,stripW-9,y+22],4,fill=(235,232,226))
    strip=strip.rotate(3,expand=True,resample=Image.BICUBIC)
    DUR=7.0; N=int(DUR*FPS)
    OUT=WK+"story_fr2"; shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT)
    for k in range(N):
        ts=k/FPS
        fr=base.copy()
        sy=int(260-ease(ts/6.5)*(pitch*3.0))     # 힐에서 시작해 위로 스크롤
        fr.alpha_composite(strip,(W-stripW-30,sy))
        fr=vgrad(fr,0,560,215,0); fr=vgrad(fr,1180,H,0,240)
        d=ImageDraw.Draw(fr)
        d.text((64,272),"셀럽 스냅 해부 #27 · 릴스에 없는 한 가지",font=F(40,"Bold"),fill=(200,240,238),stroke_width=2,stroke_fill=(0,0,0))
        d.line([(64,332),(184,332)],fill=TEAL,width=6)
        a=ease((ts-0.2)/0.5)
        d.text((64-int((1-a)*40),350),"무늬 힐은",font=SF(96),fill=WHITE+(int(255*a),),stroke_width=3,stroke_fill=(10,10,12))
        d.text((64-int((1-a)*40),466),"기장이 반",font=SF(96),fill=WHITE+(int(255*a),),stroke_width=3,stroke_fill=(10,10,12))
        b=ease((ts-1.4)/0.6)
        if b>0:
            card=Image.new("RGBA",(560,420),PAPER+(int(246*b),)); m=Image.new("L",card.size,0)
            ImageDraw.Draw(m).rounded_rectangle([0,0,559,419],28,fill=int(246*b)); card.putalpha(m)
            cd=ImageDraw.Draw(card); cd.rectangle([0,30,10,390],fill=TEAL)
            cd.text((36,30),"청바지 밑단은",font=F(48),fill=INK)
            cd.text((36,94),"발목뼈 위로",font=F(48),fill=TEAL)
            cd.text((36,180),"발등을 덮으면",font=F(44,"Bold"),fill=(60,58,54))
            cd.text((36,238),"지브라 무늬가 가려져요.",font=F(44,"Bold"),fill=(60,58,54))
            cd.text((36,306),"길면 한 번 접어 입기",font=F(44,"Bold"),fill=(60,58,54))
            fr.alpha_composite(card,(56,880+int((1-b)*40)))
        d=ImageDraw.Draw(fr)
        c2=ease((ts-2.6)/0.5)
        if c2>0: chip(d,64,1440,"핵심 한 곳은 릴스 마지막에 ↑",F(42,"Bold"),TEAL+(int(255*c2),))
        footer(d)
        fr.convert("RGB").save(f"{OUT}/{k:04d}.jpg",quality=92)
        if k==150: fr.convert("RGB").save(WK+"story_27_frame.jpg",quality=92)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",OUT+"/%04d.jpg","-f","lavfi","-i","anullsrc=r=44100:cl=stereo","-shortest","-c:v","libx264","-pix_fmt","yuv420p","-crf","18","-c:a","aac","-movflags","+faststart",WK+"story_27.mp4"],check=True)
    shutil.rmtree(OUT)
import sys
if "1" in sys.argv[1:]: story1()
if "2" in sys.argv[1:]: story2()
print("ok")
