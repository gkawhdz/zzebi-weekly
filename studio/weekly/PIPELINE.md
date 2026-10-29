# Zzebi.St 위클리 운영 방식 (v3 · 2026-10-29~)

- 구독: 인스타 DM 전용(지금은 무료). 인스타 최신 위클리 게시물에 '리포트' 댓글 → ManyChat이 DM으로 이번 주 링크 발송.
- 일정(Asia/Seoul): **월요일 새 호 발행**(코디 사진·상품 전부 새로, 새 링크) → **수·금 점검**(같은 링크, 상품 링크·가격·할인·품절, 랭킹·핫딜·크림 갱신. 코디 사진은 그대로) → 일요일은 작업 없음.
- 링크: `https://zzebi-weekly.netlify.app/r/<slug>/#k=<key>` — 월요일마다 slug·key 새로. 지난 slug 폴더는 삭제(옛 링크 404 → 안내 페이지).
  - 공개 저장소에는 암호문만: `r/<slug>/index.html`(AES-GCM), `vault/current.enc`(이번 호 데이터·사진·번역).
  - key 는 `#` 뒤라 서버·저장소에 남지 않음. 구글 드라이브 비공개 폴더 `zzebi_weekly_private`(id 1oKsfYOS8xQbtBLjE8TiyBV84W0ERP-wR)에 `weekly_link_YYYYMMDD.txt`(내용: slug, key, url) 로만 보관.
- 언어: 리포트 오른쪽 위 한국어·EN·中文 전환. 번역은 `data/wNN/i18n.json` ({"한국어 문구":{"en","zh"}}), `python3 tools/build_report.py strings DATA_DIR` 로 번역할 문구 목록 생성.
- 도구: `tools/build_report.py`(렌더·암호화), `tools/weekly_link.py`(issue/refresh/open), `tools/make_og.py`(미리보기 이미지), `tools/shop.js`(쇼핑몰 읽기), 데이터 형식 `data/SCHEMA.md`.
- 평문 데이터 폴더(`data/wNN/`)와 평문 HTML은 커밋 금지(.gitignore).
