# 틱톡 1분+ 몰아보기 (zzebi.st)
틱톡 수익화는 1분 이상 영상만 대상이라, 인스타 릴스를 그대로 올리지 않고 몰아보기로 묶어 올린다.
- make_tiktok_comp.py spec.json out.mp4  (인트로 → 챕터+영상 반복 → (요약) → (투표) → 저장&팔로우, 최소 62초)
- chill_bgm.py 가 같은 폴더(또는 studio/celeb/)에 있어야 함: 실행 전 cp ../celeb/chill_bgm.py .
- 예시: example_celeb.json(셀럽 3개 + 요약 + 투표), example_trend.json(트렌드 2개)
- 카드 글자에 이모지 쓰지 말 것(폰트에 없어 네모로 나옴). 화살표 → ↓ 는 OK.

## 유튜브 쇼츠용 영어 자막 버전 (--en)
python3 make_tiktok_comp.py spec_yt.json out_yt.mp4 --en
- 틱톡 spec에 영어 필드만 더하면 됨: intro_en, segments[].chapter_en, segments[].en = [[시작초, 끝초, "영어 문장"], …] (각 영상 안에서의 상대 시각 = 그 영상 대본 JSON의 장면 길이 누적), recap_en, vote_en, outro_en
- 자막은 한글 카드 바로 아래(띠 아래 끝 y=1570)에 작은 반투명 띠로 들어감. 한 장면당 한 문장, 90자 이내 권장.
- 예시: example_celeb_yt.json, example_trend_yt.json
- 유튜브 설명란은 한글 단락 → 빈 줄 → 같은 내용 영어 단락 순서. 채널 핸들은 @zzebi_st (인스타·틱톡은 @zzebi.st).
