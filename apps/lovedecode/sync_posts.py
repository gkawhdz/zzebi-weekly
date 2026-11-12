# 저장소 queue의 게시물 이미지를 앱 public/posts로 복사(720x900)하고, POSTS 목록에 없는 편을 알려줘요.
import os, re, sys
from PIL import Image
here = os.path.dirname(os.path.abspath(__file__))
queue = os.path.join(here, '..', '..', 'lovedecode101', 'queue')
out = os.path.join(here, 'public', 'posts')
data = open(os.path.join(here, 'src', 'data.ts')).read()
listed = set(re.findall(r"ep: '(ep\d+)'", data))
for d in sorted(os.listdir(queue)):
    src = os.path.join(queue, d)
    if not os.path.isdir(src):
        continue
    os.makedirs(os.path.join(out, d), exist_ok=True)
    for i in range(1, 11):
        f = os.path.join(src, f'slide_{i:02d}.jpg')
        t = os.path.join(out, d, f'slide_{i:02d}.jpg')
        if os.path.exists(f) and not os.path.exists(t):
            Image.open(f).convert('RGB').resize((720, 900), Image.LANCZOS).save(t, quality=82)
    if d not in listed:
        print('POSTS에 추가 필요:', d)
