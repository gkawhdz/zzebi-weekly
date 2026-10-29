#!/usr/bin/env python3
"""링크 미리보기 이미지 1200x630 (v3 베이지·틸). 사용: python3 tools/make_og.py OUT.jpg "10월 5주" img1 img2 ... [--generic]"""
import sys, subprocess
from PIL import Image, ImageDraw, ImageFont
fc=lambda q: subprocess.check_output(['fc-match','-f','%{file}',q]).decode()
B=fc('Noto Sans CJK KR:weight=900'); M=fc('Noto Sans CJK KR:weight=500'); SER=fc('Noto Serif CJK KR:weight=700')
F=lambda p,n: ImageFont.truetype(p,n)
BG=(245,241,234); INK=(20,20,20); TEAL=(0,124,124); MUT=(87,83,76)
args=[a for a in sys.argv[1:] if a!='--generic']; generic='--generic' in sys.argv
out,week,imgs=args[0],args[1],args[2:]
W,H=1200,630; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
# 오른쪽 사진 띠 (세로 사진 6장, 2줄 엇갈림 없이 한 줄)
n=len(imgs); ph=H; pw=int((W*0.56)/n); x0=W-pw*n
for i,p in enumerate(imgs):
    s=Image.open(p).convert('RGB'); s=s.resize((int(s.width*ph/s.height),ph),Image.LANCZOS)
    cx=(s.width-pw)//2; im.paste(s.crop((cx,0,cx+pw,ph)),(x0+i*pw,0))
    d.line([(x0+i*pw,0),(x0+i*pw,H)],fill=BG,width=4)
L=64
d.rectangle([0,0,x0-1,H],fill=BG)
d.text((L,60),'zzebi',font=F(SER,52),fill=INK); w=d.textlength('zzebi',font=F(SER,52)); d.text((L+w,60),'.st',font=F(SER,52),fill=(0,168,168))
chip='구독자 전용' if generic else f'WEEKLY · {week}'
cf=F(B,24); cw=d.textlength(chip,font=cf)
d.rounded_rectangle([L,170,L+cw+36,214],radius=22,fill=TEAL); d.text((L+18,176),chip,font=cf,fill=(255,255,255))
d.text((L,240),'이번 주 셀럽 스냅,',font=F(B,50),fill=INK); d.text((L,306),'지금 사는 법',font=F(B,50),fill=INK)
for k,t in enumerate(['명품·중가·가성비 3단 가격','랭킹 · 핫딜 · 크림 신발','한국어 · EN · 中文']):
    d.text((L,400+k*40),t,font=F(M,26),fill=MUT)
d.text((L,H-70),'@zzebi.st',font=F(M,24),fill=TEAL)
im.save(out,quality=88); print(out)
