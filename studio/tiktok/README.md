# 틱톡 1분+ 몰아보기 (zzebi.st)
틱톡 수익화는 1분 이상 영상만 대상이라, 인스타 릴스를 그대로 올리지 않고 몰아보기로 묶어 올린다.
- make_tiktok_comp.py spec.json out.mp4  (인트로 → 챕터+영상 반복 → (요약) → (투표) → 저장&팔로우, 최소 62초)
- chill_bgm.py 가 같은 폴더(또는 studio/celeb/)에 있어야 함: 실행 전 cp ../celeb/chill_bgm.py .
- 예시: example_celeb.json(셀럽 3개 + 요약 + 투표), example_trend.json(트렌드 2개)
- 카드 글자에 이모지 쓰지 말 것(폰트에 없어 네모로 나옴). 화살표 → ↓ 는 OK.
