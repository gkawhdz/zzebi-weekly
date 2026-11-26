# 셀럽 스냅 #54 스토리: '덮을 곳 3곳' 착장 콜아웃 지도 (정지 jpg)
from PIL import Image, ImageDraw, ImageFont
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; R='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; K='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
f=lambda p,s: ImageFont.truetype(p,s,index=1)
TEAL=(0,168,168); INK=(28,26,24); GR=(105,99,92)
W,H=1080,1920
src=Image.open('img54.jpg').convert('RGB')
c=Image.new('RGB',(W,H),(242,238,231)); d=ImageDraw.Draw(c)
# 제목
d.rounded_rectangle((60,262,470,322),16,fill=TEAL); d.text((80,268),'셀럽 스냅 해부 #54',font=f(B,38),fill='white')
d.text((60,340),'청바지 날, 덮을 곳 3곳',font=f(K,70),fill=INK)
d.rectangle((60,432,360,440),fill=TEAL)
# 착장 사진 (오른쪽 절반 크롭, 크게)
x0,y0,x1,y1=555,278,1005,1350; PX,PY,PH=50,470,1060
s=PH/(y1-y0); PW=int((x1-x0)*s)
ph=src.crop((x0,y0,x1,y1)).resize((PW,PH)); c.paste(ph,(PX,PY))
d.rectangle((PX,PY,PX+PW,PY+PH),outline='white',width=8)
M=lambda x,y:(PX+(x-x0)*s,PY+(y-y0)*s)
pts=[((770,300),'목','머플러로 감싸기'),((905,980),'허벅지','무릎 아래 코트'),((765,1225),'발목','바지 길이로 덮기')]
cx=PX+PW+40; ys=[500,760,1020]
for ((x,y),t,sub),yy in zip(pts,ys):
    px,py=M(x,y)
    d.line((px,py,cx-10,yy+40),fill=TEAL,width=5); d.ellipse((px-14,py-14,px+14,py+14),fill=TEAL,outline='white',width=4)
    d.text((cx,yy),t,font=f(K,60),fill=INK)
    d.text((cx,yy+82),sub,font=f(B,44),fill=GR)
# 릴스에 없는 한 가지
by=1235
d.rounded_rectangle((cx-14,by,W-40,by+215),22,fill='white',outline=(220,214,205),width=2)
d.text((cx+10,by+18),'+ 릴스에 없는 팁',font=f(B,36),fill=TEAL)
d.text((cx+10,by+66),'구두가 추운 날엔',font=f(B,44),fill=INK)
d.text((cx+10,by+130),'빨간 앵클부츠로',font=f(B,44),fill=INK)
d.text((cx,1478),'포인트 4개는 릴스 ↑',font=f(B,44),fill=TEAL)
d.text((W-60,1590),'@zzebi.st · AI 재현 이미지',font=f(R,30),fill=(120,114,108),anchor='rs')
c.save('story_54.jpg',quality=92)
