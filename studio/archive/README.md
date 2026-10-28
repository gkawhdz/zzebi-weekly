# zzebi 책 자료 아카이브 (2026-10-28 사장님 지시)

목적: 1년 뒤 인스타 릴스(Trend Daily)·패피 스트릿 릴스(셀럽 스냅 해부)를 모아 **계절별 옷 스타일 책**(전자책·실물책)을 만들기 위한 원본 자료 보관.
매일 밤 '책 자료 아카이브' 작업이 그날 게시물을 정리해 여기에 쌓는다.

## 저장 위치
- 글 정보(룩·아이템·색·후킹·캡션): 이 폴더 `YYYY/MM/YYYYMMDD.json`
- 전체 목록: `index.json` (날짜·계절·종류·성별·제목 한 줄씩)
- 원본 그림(글자 없는 AI 일러스트 1024x1536): 구글 드라이브 폴더 `zzebi_책자료_아카이브` (id 1-6Ab28F11HVlO85v_G6UkLiqYySCP4Dp) / `YYYY-MM` 하위 폴더
- 완성 영상: GitHub `media` 브랜치 (YYYYMMDD_A.mp4 등)

## 계절 구분 (한국 기준)
봄 3~5월 · 여름 6~8월 · 가을 9~11월 · 겨울 12~2월. 간절기(3·11월)는 `transition: true` 표시.

## 게시물 1건 형식
{"date","season","transition","series":"trend|celeb","format":"정보형|코디룩북|셀럽스냅","gender":"여자|남자|공용",
 "title","hook","hook_type","situation":"출근·데이트·하객 등","weather":"기온·날씨(있으면)",
 "looks":[{"name","items":[{"part":"아우터|상의|하의|신발|가방|액세서리","desc":"색+소재+종류","color_hex","tip"}],
          "palette":["#HEX"],"formula":"코디 공식 한 줄"}],
 "caption","sources":[...],
 "images":[{"drive_id","name","kind":"원본일러스트|커버"}],
 "video":"media 브랜치 파일명","instagram_url":null,
 "metrics":{"views","saves","shares"}(그로스랩 데이터 있으면),
 "book_notes":"책에 쓸 때 주의(셀럽 이름·초상권 등)"}

## 책 만들 때 주의
- 셀럽 스냅: 셀럽 이름·실존 인물 닮은 이미지는 상업 출판 시 퍼블리시티권·초상권 문제 가능 → 책에는 '스타일 공식'만 쓰고 그림은 새 웹툰풍 일러스트로 다시 그리는 것을 기본으로.
- AI 일러스트는 1024x1536이라 실물책 전면 사진으로 쓰려면 업스케일 필요(전자책은 그대로 OK).
