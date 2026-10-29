#!/usr/bin/env python3
"""Zzebi.St 위클리 비밀 링크 발행·갱신

  python3 tools/weekly_link.py issue   DATA_DIR [OG_URL]        # 월요일 새 호: 새 slug·새 키, 지난 링크 폴더 삭제
  python3 tools/weekly_link.py refresh DATA_DIR SLUG KEY [OG_URL]  # 수·금 점검: 같은 링크 그대로 내용만 갱신
  python3 tools/weekly_link.py open    SLUG KEY OUT_DIR          # 저장소의 암호화 데이터(vault/current.enc)를 풀어 DATA_DIR 만들기

결과 JSON: {"slug","key","url"}  → url 을 ManyChat DM 버튼에 넣고, key 는 비공개 저장소(구글 드라이브)에만 보관.
공개 저장소에는 암호문만 올라갑니다(r/<slug>/index.html, vault/current.enc). 평문 DATA_DIR·평문 HTML은 커밋 금지.
"""
import sys, os, json, shutil, subprocess, secrets, base64
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build_report as B
SITE = 'https://gkawhdz.github.io/zzebi-weekly'

def build(data_dir, slug, key, og):
    meta = json.load(open(os.path.join(data_dir, 'meta.json')))
    doc, T = B.render(data_dir)
    miss = [k for k, v in zip(T.keys, T.table()['en']) if not v]
    plain = os.path.join(data_dir, '_plain.html')
    open(plain, 'w').write(doc)
    out = os.path.join(ROOT, 'r', slug, 'index.html')
    B.seal(plain, out, key, f'Zzebi.St 위클리 · {meta["week"]}', og or f'{SITE}/og.jpg')
    os.makedirs(os.path.join(ROOT, 'vault'), exist_ok=True)
    B.pack(data_dir, os.path.join(ROOT, 'vault', 'current.enc'), key)
    for f in ('landing.html', '404.html'):
        shutil.copy(os.path.join(ROOT, 'tools', 'site', f), os.path.join(ROOT, 'index.html' if f == 'landing.html' else f))
    return {'slug': slug, 'key': key, 'url': f'{SITE}/r/{slug}/#k={key}', 'untranslated': len(miss), 'plain': plain}

if __name__ == '__main__':
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit(1)
    if a[0] == 'issue':
        slug, key = secrets.token_hex(6), B.b64u(secrets.token_bytes(32))
        rdir = os.path.join(ROOT, 'r')
        if os.path.isdir(rdir):
            for d in os.listdir(rdir):           # 지난 링크 폴더 삭제 → 옛 주소는 404(링크 닫힘)
                shutil.rmtree(os.path.join(rdir, d))
        print(json.dumps(build(a[1], slug, key, a[2] if len(a) > 2 else None), ensure_ascii=False))
    elif a[0] == 'refresh':
        print(json.dumps(build(a[1], a[2], a[3], a[4] if len(a) > 4 else None), ensure_ascii=False))
    elif a[0] == 'open':
        B.unpack(os.path.join(ROOT, 'vault', 'current.enc'), a[3], a[2]); print('opened', a[3])
    else:
        print(__doc__); sys.exit(1)
