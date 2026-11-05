import sys,subprocess,os,re
from PIL import Image, ImageDraw
n=sys.argv[1]  # e.g. 02
here=os.path.dirname(os.path.abspath(__file__))
head=open(f'{here}/head.html').read(); body=open(f'{here}/body_{n}.html').read()
html=head+body+'\n</body></html>'
os.makedirs(f'{here}/render_{n}',exist_ok=True); os.makedirs(f'{here}/out_{n}',exist_ok=True)
open(f'{here}/render_{n}/slides.html','w').write(html)
subprocess.run(['node',f'{here}/shot.js',f'{here}/render_{n}/slides.html',f'{here}/out_{n}'],check=True)
ims=[]
for i in range(1,11):
    im=Image.open(f'{here}/out_{n}/slide_{i:02d}.png').convert('RGB'); d=ImageDraw.Draw(im)
    d.rectangle([0,135,1079,1214],outline=(0,200,255),width=4); ims.append(im.resize((360,450)))
sheet=Image.new('RGB',(360*5+40,450*2+30),'black')
for i,im in enumerate(ims): sheet.paste(im,((i%5)*370,(i//5)*460))
sheet.save(f'{here}/contact_{n}.png'); print('built',n)
