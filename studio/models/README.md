# zzebi 전속 모델 (2026-11-10 사장님 선택)

트렌드 실사 릴스에서 얼굴이 보이는 인물은 항상 이 두 사람으로 고정한다.

| 구분 | 기준 사진 | 키 | 특징 (그림 문장에 그대로 넣기) |
|---|---|---|---|
| 여자 (후보 여2) | models/model_W.jpg | 168cm | the same Korean woman as in the reference photo (same face, same long straight black hair with see-through bangs, same slender build, 168cm tall) |
| 남자 (후보 남1) | models/model_M.jpg | 182cm | the same Korean man as in the reference photo (same face, same short two-block black hair, same slim build, 182cm tall) |

## 쓰는 법
- tools/gen_image.sh 요청 항목에 "refs": ["models/model_W.jpg"] (남자는 model_M.jpg, 둘 다면 두 개) 추가.
  (refs 경로는 imgreq 브랜치 기준. 같은 파일이 main의 studio/models/ 에도 보관됨)
- 둘이 함께 나오면 "the man clearly about 14cm taller than the woman" 를 넣어 키 차이 유지.
- 헤어스타일·얼굴은 바꾸지 않는다. 옷·배경·포즈·조명만 바꾼다.
- 시험(11/10): 새 옷·새 배경에서도 얼굴·머리·체형 유지 확인.
