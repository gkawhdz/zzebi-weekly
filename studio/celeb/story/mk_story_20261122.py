from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920; TEAL=(0,168,168); INK=(28,26,24)
B="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"; R="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"; K="/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
f=lambda p,s: ImageFont.truetype(p,s,index=1)
src=Image.open('img49.jpg').convert('RGB')
im=Image.new('RGB',(W,H),(239,233,224)); d=ImageDraw.Draw(im,'RGBA')
d.rounded_rectangle((60,270,470,336),18,fill=TEAL); d.text((82,276),"셀럽 스냅 해부 #49",font=f(B,40),fill='white')
d.text((60,356),"블레이저는 그대로,",font=f(K,82),fill=INK)
d.text((60,456),"이 3개만 갈아타요",font=f(K,82),fill=INK)
d.line([(64,568),(520,568)],fill=TEAL,width=10)
d.text((60,592),"평일 출근  →  주말 외출",font=f(B,44),fill=(120,110,98))
rows=[("슬랙스",(290,1060,300),"연청|와이드 데님"),("셔츠",(265,650,280),"아이보리|칼라 니트"),("구두",(145,1190,240),"퍼 트리밍|슬립온")]
y=650
for old,(cx,cy,s),new in rows:
    d.rounded_rectangle((60,y,1020,y+224),28,fill=(252,250,246))
    d.text((100,y+48),"평일",font=f(R,34),fill=(140,132,122))
    d.text((100,y+94),old,font=f(B,54),fill=(150,142,132))
    tw=d.textlength(old,font=f(B,54)); d.line([(100,y+128),(100+tw,y+128)],fill=(150,142,132),width=5)
    d.text((300,y+78),"→",font=f(K,64),fill=TEAL)
    c=src.crop((cx-s//2,cy-s//2,cx+s//2,cy+s//2)).resize((190,190))
    m=Image.new('L',(190,190),0); ImageDraw.Draw(m).rounded_rectangle((0,0,189,189),22,fill=255)
    im.paste(c,(400,y+17),m)
    d.text((630,y+44),"주말",font=f(B,34),fill=TEAL)
    a_,b_=new.split('|'); d.text((630,y+88),a_,font=f(B,48),fill=INK); d.text((630,y+144),b_,font=f(B,48),fill=INK)
    y+=240
d.rounded_rectangle((60,1384,1020,1460),24,fill=(46,44,42))
d.text((90,1422),"+ 볼캡은 쓰지 않고 손에만 들어도 OK",font=f(B,44),fill='white',anchor='lm')
d.text((60,1470),"AI 재현 이미지 · 릴스에 없는 팁 하나 더",font=f(R,30),fill=(120,112,102))
d.rounded_rectangle((60,1516,760,1582),30,fill=TEAL); d.text((90,1522),"4개 포인트 전부는 릴스에서 ↑",font=f(B,42),fill="white")
d.text((800,1530),"@zzebi.st",font=f(B,38),fill=INK)
im.save('st/story_main.jpg',quality=92)
# bottom line moved above UI: put button at 1420? -> overlay adjust below
