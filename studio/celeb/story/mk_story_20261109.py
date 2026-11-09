from PIL import Image, ImageDraw, ImageFilter, ImageFont
FD="/usr/share/fonts/opentype/noto/"
import os
def F(s,w="Black"):
    for p in [FD+f"NotoSansCJK-{w}.ttc","/usr/share/fonts/noto-cjk/NotoSansCJK-%s.ttc"%w]:
        if os.path.exists(p): return ImageFont.truetype(p,s,index=1)
def SF(s):
    for p in [FD+"NotoSerifCJK-Black.ttc","/usr/share/fonts/noto-cjk/NotoSerifCJK-Black.ttc"]:
        if os.path.exists(p): return ImageFont.truetype(p,s,index=1)
TEAL=(0,168,168)
src=Image.open("img38.jpg").convert("RGB")
r=src.crop((516,0,1024,1536))            # 오른쪽 착장 절반
sc=1080/r.width; r=r.resize((1080,int(r.height*sc)),Image.LANCZOS)
y0=int(330*sc)-250; bg=r.crop((0,y0,1080,y0+1920))
# 가방 영역(원본 x 880~1000, y 430~700) 가리기
bx0,by0,bx1,by1=[int(v) for v in ((880-516)*sc-30,430*sc-y0,(1004-516)*sc,700*sc-y0)]
bx1=min(bx1,1060)
bx0-=10; by0=-40
d0=ImageDraw.Draw(bg); d0.rounded_rectangle([bx0,by0,bx1,by1],26,fill=(34,36,40))
d=ImageDraw.Draw(bg,"RGBA")
d.rounded_rectangle([bx0,by0,bx1,by1],26,outline=TEAL,width=8)
q=F(150,"Black"); cx=(bx0+bx1)//2; cy=(560+by1)//2+40
d.text((cx,cy),"?",font=q,fill=(255,255,255),anchor="mm")
# 위쪽 제목 판
d.rounded_rectangle([50,262,690,560],28,fill=(250,247,240,236))
d.text((90,300),"가방만",font=SF(86),fill=(28,24,20))
d.text((90,404),"가려봤어요",font=SF(86),fill=(28,24,20))
d.line([(92,520),(470,520)],fill=TEAL,width=8)
d.rounded_rectangle([50,580,690,660],20,fill=(20,20,22,200))
d.text((80,620),"후드+청바지엔 무슨 색?",font=F(46,"Bold"),fill=(255,255,255),anchor="lm")
# 아래 안내
d.rounded_rectangle([50,1380,760,1480],50,fill=TEAL)
d.text((405,1430),"정답은 릴스 03번에서 ↑",font=F(48,"Black"),fill=(255,255,255),anchor="mm")
d.rounded_rectangle([50,1500,640,1580],18,fill=(20,20,22,190))
d.text((76,1540),"@zzebi.st · 셀럽 스냅 해부 #38",font=F(36,"Bold"),fill=(255,255,255),anchor="lm")
d.text((1030,1540),"AI 재현 이미지",font=F(26,"Medium"),fill=(255,255,255,220),anchor="rm")
bg.save("20261109_story_38.jpg",quality=92); print("ok",bg.size,(bx0,by0,bx1,by1))
