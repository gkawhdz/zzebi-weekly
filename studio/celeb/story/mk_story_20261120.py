from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
W,H=1080,1920; TEAL=(0,168,168)
B="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"; R="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"; K="/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc"
f=lambda p,s: ImageFont.truetype(p,s,index=1)
src=Image.open('img47.jpg').convert('RGB')
im=Image.new('RGB',(W,H),(236,234,230)); d=ImageDraw.Draw(im,'RGBA')
d.rounded_rectangle((60,270,470,336),18,fill=TEAL); d.text((82,276),"셀럽 스냅 해부 #47",font=f(B,40),fill='white')
d.text((60,360),"같은 가죽 재킷,",font=f(K,88),fill=(22,22,24))
d.text((60,465),"바지 색만 달라요",font=f(K,88),fill=(22,22,24))
d.line([(64,580),(560,580)],fill=TEAL,width=10)
# tile crop: jacket hem + jeans (right half)
box=(600,450,940,1010)  # 340x560
real=src.crop(box)
a=np.asarray(real).astype(float); lum=a.mean(axis=2,keepdims=True)
# indigo recolor of denim zone (lower part) only: below hem y~620 in orig -> 170 in crop
ind=np.clip(lum*np.array([0.62,0.78,1.3])+np.array([0,10,38]),0,255)
from PIL import ImageFilter
pts=[(712,588),(835,588),(845,648),(895,660),(905,1010),(645,1010),(648,695),(705,680)]
pm=Image.new('L',real.size,0); ImageDraw.Draw(pm).polygon([(x-box[0],y-box[1]) for x,y in pts],fill=255)
pm=pm.filter(ImageFilter.GaussianBlur(2))
l=lum[...,0]; mask=(np.asarray(pm)/255.0)*(l<125)
fake=(a*(1-mask[...,None])+ind*mask[...,None]).astype('uint8')
tw,th=460,758
L=Image.fromarray(fake).resize((tw,th)); Rr=real.resize((tw,th))
y0=630
im.paste(L,(60,y0)); im.paste(Rr,(560,y0))
d.rectangle((60,y0,60+tw,y0+th),outline=(150,150,150),width=4)
d.rectangle((556,y0-4,564+tw,y0+th+4),outline=TEAL,width=10)
for x,lab,col in [(60,"X  진청",(90,90,95)),(560,"O  짙은 회색",TEAL)]:
    d.rounded_rectangle((x+20,y0+20,x+20+(220 if 'X' in lab else 300),y0+90),16,fill=col); d.text((x+40,y0+24),lab,font=f(B,44),fill='white')
yb=y0+th+22
d.text((60,yb),"재킷과 끊겨 보여요",font=f(B,44),fill=(90,90,95))
d.text((560,yb),"위아래가 이어져요",font=f(B,44),fill=TEAL)
d.text((60,1490),"왼쪽은 비교용으로 색만 바꾼 AI 재현 이미지",font=f(R,30),fill=(110,110,110))
d.rounded_rectangle((60,1530,760,1596),30,fill=TEAL); d.text((90,1536),"4개 포인트 전부는 릴스에서 ↑",font=f(B,42),fill='white')
d.text((800,1544),"@zzebi.st",font=f(B,38),fill=(22,22,24))
im.save('20261120_story_47.jpg',quality=92)
