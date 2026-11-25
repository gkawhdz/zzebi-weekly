# 셀럽 스냅 #53 스토리: 신발 대체 사다리 (정지 jpg)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; R='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; K='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
f=lambda p,s: ImageFont.truetype(p,s,index=1)
TEAL=(0,168,168); INK=(28,26,24)
W,H=1080,1920
src=Image.open('img53.jpg').convert('RGB')
c=Image.new('RGB',(W,H),(238,233,225)); d=ImageDraw.Draw(c)
# 위: 착장 하단(바지 밑단+로퍼) 큰 사진
ph=src.crop((560,1110,1024,1410)).resize((W-120,int((W-120)*300/464)))
c.paste(ph,(60,260)); d.rectangle((60,260,60+ph.width,260+ph.height),outline=(255,255,255),width=8)
y0=260+ph.height
# 사진 위 라벨
d.rounded_rectangle((90,290,520,360),18,fill=TEAL); d.text((112,298),'셀럽 스냅 해부 #53',font=f(B,40),fill='white')
# 제목
y=y0+30
d.text((70,y),'검정 니트엔 갈색 신발',font=f(K,62),fill=INK); y+=84
d.rectangle((70,y,70+300,y+8),fill=TEAL); y+=34
d.text((70,y),'이 순서로 골라 보세요',font=f(B,50),fill=INK); y+=78
rows=[('1','브라운 스웨이드 로퍼','오늘 룩',True),
      ('2','다크 브라운 가죽 로퍼','',False),
      ('3','베이지 스웨이드 스니커즈','캐주얼하게',False)]
for n,t,s,hi in rows:
    d.rounded_rectangle((60,y,W-60,y+112),24,fill='white',outline=TEAL if hi else (220,214,205),width=6 if hi else 2)
    d.ellipse((86,y+20,158,y+92),fill=TEAL if hi else INK); d.text((122,y+56),n,font=f(B,46),fill='white',anchor='mm')
    d.text((182,y+56),t,font=f(B,46),fill=INK,anchor='lm')
    if s: d.text((W-90,y+56),s,font=f(B,36),fill=TEAL if hi else (110,104,98),anchor='rm')
    y+=126
d.text((70,y+8),'포인트 4개 전부는 릴스에서 ↑',font=f(B,44),fill=TEAL)
d.text((W-70,1570),'@zzebi.st · AI 재현 이미지',font=f(R,30),fill=(120,114,108),anchor='rs')
c.save('story_53.jpg',quality=92); print(y+60)
