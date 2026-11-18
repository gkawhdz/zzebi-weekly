from PIL import Image, ImageDraw, ImageFont, ImageFilter
W,H=1080,1920; TEAL=(0,168,168)
B="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"; R="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"; K="/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
f=lambda p,s: ImageFont.truetype(p,s,index=1)  # KR
src=Image.open('img46.jpg').convert('RGB')
# full-bleed close crop of right half around bag/coat
box=(560,430,1000,1210)  # 440x780 ~ 9:16
bg=src.crop(box).resize((W,int(W*780/440)),Image.LANCZOS)
im=Image.new('RGB',(W,H),(30,26,24)); im.paste(bg,(0,(H-bg.height)//2))
d=ImageDraw.Draw(im,'RGBA')
# top dark gradient for title
for y in range(250,700): d.line([(0,y),(W,y)],fill=(15,12,10,int(190*max(0,1-(y-250)/450)**0.8)))
d.rounded_rectangle((60,270,470,336),18,fill=TEAL); d.text((82,276),"셀럽 스냅 해부 #46",font=f(B,40),fill='white')
d.text((60,360),"퍼 코트엔",font=f(K,96),fill='white')
d.text((60,470),"'손바닥 가방'",font=f(K,112),fill='white')
d.line([(64,608),(700,608)],fill=TEAL,width=10)
# bag position in crop coords: orig (660,730) -> scaled
sx=W/440; oy=(H-bg.height)//2
bx=(660-560)*sx; by=(730-430)*sx+oy
r=190; d.ellipse((bx-r,by-r*0.85,bx+r,by+r*0.85),outline=TEAL,width=9)
# memo card
mx,my=430,1180
d.rounded_rectangle((mx,my,1020,my+330),26,fill=(250,247,240,240))
d.text((mx+34,my+28),"큰 숄더백 X",font=f(B,52),fill=(120,110,100))
d.line([(mx+34,my+60),(mx+330,my+60)],fill=(120,110,100),width=5)
d.text((mx+34,my+108),"작고 납작한 크로스백",font=f(B,50),fill=(25,22,20))
d.text((mx+34,my+180),"털이 안 눌려 덜 부해 보이고,",font=f(R,38),fill=(60,55,50))
d.text((mx+34,my+228),"대각선 끈이 몸을 갈라줘요",font=f(R,38),fill=(60,55,50))
d.line([(bx+r*0.6,by+r*0.7),(mx+60,my)],fill=TEAL,width=6)
# bottom guide (above 1600)
d.rounded_rectangle((60,1540,760,1600-0),30,fill=TEAL)
d.text((90,1543),"4개 포인트 전부는 릴스에서 ↑",font=f(B,40),fill='white')
d.text((800,1552),"@zzebi.st",font=f(B,36),fill='white')
d.text((60,1500-0),"AI 재현 이미지",font=f(R,28),fill=(235,230,225))
im.save('20261119_story_46.jpg',quality=92)
