# 실사 릴스 렌더 도구 (2026-11-10~, 트렌드 데일리 기본)
- make_real.py : 실사 사진 릴스. make_short.py·make_lookbook.py 를 같은 폴더에서 import (이 폴더 그대로 복사해서 쓰기)
- 장면: rcompare(훅 비교 2장) · rboard(사진 + 01/03 머리글 + 아이템 확대 카드) · rformula(공식 3줄 + 썸네일) · text(CTA)
- 예시: real_example.json (2026-11-10 '옷 2벌로 4일 돌려입기', 사장님 승인본)
- rboard "home": [0.86, 512, 440] → 첫 화면에서 머리가 제목 판 아래로 옴(인물 머리 y≈180~200 기준)
- 아이템 xy = 원본 1024x1536 픽셀. 발밑 아이템은 "zoom":1.4, "sy":1660 (화면 아래쪽에 링)
- 미리보기: python3 make_real.py preview X.json p.jpg '{"0":[1.0],"1":[0.3,3.8],"2":[0.3,3.8,6.2]}'
- 렌더: python3 make_real.py X.json X_silent.mp4 → make_bgm.py <길이> bgm.wav <BPM> [mood] → ffmpeg 합치기
