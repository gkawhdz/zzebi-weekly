# 2026-11-15 #42 스토리: '간격 브래킷' 확대 컷 (정지 jpg)
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
src, out = sys.argv[1], sys.argv[2]
W,H=1080,1920; TEAL=(0,168,168)
B='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; R='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SB='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'; SE='/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
f=lambda p,s:ImageFont.truetype(p,s,index=1 if 'Serif' not in p else 1)
im=Image.open(src).convert('RGB')
# 오른쪽 착장: 쇼츠~부츠 구간 확대 (x 530-1024, y 520-1400)
PY0=600
crop=im.crop((540,PY0,1024,PY0+530)); s=W/crop.width
crop=crop.resize((W,int(crop.height*s)),Image.LANCZOS)
bg=Image.new('RGB',(W,H),(22,20,20)); y0=H-crop.height; bg.paste(crop,(0,y0))
# 위쪽 그라데이션
g=Image.new('L',(1,H)); 
for y in range(H): g.putpixel((0,y),int(255*max(0,min(1,(y0+120-y)/160))))
bg.paste(Image.new('RGB',(W,H),(22,20,20)),(0,0),g.resize((W,H)))
d=ImageDraw.Draw(bg)
def Y(py): return int(y0+(py-PY0)*s)
def X(px): return int((px-540)*s)
# 브래킷: 쇼츠 밑단(py≈740) ~ 부츠 윗단(py≈975), 오른쪽 다리 바깥 x≈905
x=X(912); ya,yb=Y(742),Y(972)
d.line([(x,ya),(x,yb)],fill=TEAL,width=8)
for yy in (ya,yb): d.line([(x-34,yy),(x+8,yy)],fill=TEAL,width=8)
d.rounded_rectangle([x-330,(ya+yb)//2-50,x-40,(ya+yb)//2+50],22,fill=TEAL)
d.text((x-185,(ya+yb)//2),"이 간격이 핵심",font=f(B,46),fill='white',anchor='mm')
# 상단 텍스트 (위 250px 비움)
d.text((70,262),"셀럽 스냅 해부 #42",font=f(SB,40),fill=TEAL)
d.text((70,318),"다리가 길어 보인\n진짜 이유",font=f(B,100),fill='white',spacing=12)
d.text((70,572),"쇼츠 밑단과 부츠 사이를 넉넉히 비우면\n다리 선이 위에서부터 이어져 보여요",font=f(R,44),fill=(235,232,228),spacing=14)
# 하단 버튼 (아래 320px 비움 → 1600 위)
by=1470; d.rounded_rectangle([70,by,760,by+96],48,fill=TEAL)
d.text((415,by+48),"4개 포인트 전부는 릴스에서 ↑",font=f(B,44),fill='white',anchor='mm')
d.text((1010,286),"@zzebi.st",font=f(SB,40),fill='white',anchor='rm')
d.text((76,by+108),"※ 실제 착장을 바탕으로 한 AI 재현 이미지",font=f(R,32),fill=(235,235,235),stroke_width=2,stroke_fill=(20,20,20))
bg.save(out,quality=92)
