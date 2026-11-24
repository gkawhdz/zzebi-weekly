from PIL import Image, ImageDraw, ImageFont, ImageFilter
F='/usr/share/fonts/opentype/noto/'
def f(w,s): return ImageFont.truetype(F+f'NotoSansCJK-{w}.ttc',s,index=1)  # KR
def sf(s): return ImageFont.truetype(F+'NotoSerifCJK-Bold.ttc',s,index=1)
W,H=1080,1920; TEAL=(0,168,168); INK=(24,26,30); BG=(244,240,233)
im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
src=Image.open('/home/claude/work/img52.jpg')
# photo: right-half neck/muffler close-up, full width
ph=src.crop((560,200,1000,640)).resize((W,1074),Image.LANCZOS)
im.paste(ph.crop((0,180,W,180+700)),(0,250))
# serif title on photo bottom gradient
g=Image.new('L',(W,300),0); gd=ImageDraw.Draw(g)
for y in range(300): gd.line((0,y,W,y),fill=int(200*y/300))
im.paste(Image.new('RGB',(W,300),(10,12,16)),(0,650),g)
d.text((60,680),'셀럽 스냅 해부 #52 · 릴스에 없는 한 가지',font=f('Bold',34),fill=(220,240,240))
d.text((60,735),'검정 코트 위 머플러,',font=sf(70),fill='white')
d.text((60,820),'이 3색부터 골라 보세요',font=sf(70),fill='white')
d.rectangle((60,912,240,918),fill=TEAL)
chips=[((38,52,92),'네이비 체크','오늘 룩 · 검정과 가까워 차분하게',True),
       ((150,150,150),'라이트 그레이','얼굴 아래를 한 톤 밝게',False),
       ((176,128,82),'카멜','검정 위 가장 따뜻한 대비',False)]
y=975
for col,name,why,today in chips:
    d.rounded_rectangle((60,y,W-60,y+150),28,fill='white',outline=TEAL if today else (225,220,212),width=5 if today else 2)
    d.rounded_rectangle((90,y+25,190,y+125),20,fill=col)
    if today:
        for k in range(0,100,26): d.line((90+k,y+25,90+k,y+125),fill=(120,130,150),width=3); d.line((90,y+25+k,190,y+25+k),fill=(120,130,150),width=3)
    d.text((220,y+22),name,font=f('Black',50),fill=INK)
    d.text((220,y+88),why,font=f('Medium',36),fill=(90,90,90))
    if today:
        d.rounded_rectangle((W-230,y+48,W-90,y+102),27,fill=TEAL); d.text((W-206,y+52),'오늘 룩',font=f('Bold',34),fill='white')
    y+=160
d.text((60,1462),'색은 목에 하나만 → 4개 포인트는 릴스에서 ↑',font=f('Bold',44),fill=INK)
d.text((60,1530),'@zzebi.st',font=f('Black',44),fill=TEAL)
d.text((W-60-230,1540),'AI 재현 이미지',font=f('Regular',30),fill=(120,120,120))
im.save('/home/claude/work/story/20261125_story_52.jpg',quality=92)
