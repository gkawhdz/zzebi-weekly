# Zzebi.St 위클리 데이터 형식 (tools/build_report.py 가 읽음)

모든 사용자 노출 문구는 한국어로. 번역은 빌드 단계에서 따로 붙인다.

## 상품 1개 (product)
```json
{"brand":"오호스", "name":"스타퀼트 패디드 호보백 블랙", "url":"https://www.musinsa.com/products/5928356",
 "shop":"무신사", "won":94400, "off":20, "approx":false, "from":false,
 "ovs":"$1,046 · 직구, 관부가세 별도", "note":"하프 기장", "where":"무신사 · 랭킹 급상승"}
```
- won: 원화 정수(필수). 해외가는 대략 환산 정수 + approx:true + ovs 에 원래 외화 표기.
- match: 1~5 사진 비교 점수(4 이상만 사용), match_note: 같은 점·다른 점 한 줄 — studio/weekly/MATCHING.md 필수
- off: 할인율 정수(없으면 생략/0). from:true 면 "~"(옵션별 최저가).
- shop/note/ovs/where: 선택. 실재하지 않는 URL·가격 금지, 품절 제외.

## 룩 1개 (look)
```json
{"id":"w14","ep":"14","city":"공항","title":"레더 봄버 공항룩","who":"나오미 왓츠 무드 재현",
 "img":"w14.jpg","alt":"... (AI 재현 이미지)",
 "point":"룩 설명 2문장", "real":"실착 정보 한 줄(출처 기사 기준, 없으면 빈 문자열)",
 "cores":[{"h":"블랙 레더 봄버","tiers":{"lux":product,"mid":product,"value":product}},
          {"h":"그레이 트랙 팬츠","tiers":{...}}],
 "with":[{"role":"신발 · 사진과 같은 레드","p":product}, {"role":"이너","p":product}]}
```
- lux 명품(실착 브랜드 또는 같은 급), mid 중가(약 10~50만원, 디자인 가장 가까운 것), value 가성비(약 10만원 안팎).

- 코어·with 에 "spec" (룩 아이템 사양서: 색·종류·소재·디테일) 필수. 4점 이상 후보가 없으면 그 칸은 비우고 look 의 "note" 에 이유.
