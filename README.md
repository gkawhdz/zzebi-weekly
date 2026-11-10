# imgreq — 이미지 생성 요청 브랜치 (Zapier 대체, 2026-11-10)
req/<id>.json 을 올리면 GitHub Actions가 OpenAI(저장소 Secret OPENAI_API_KEY)로 그림을 만들어 out/<id>/ 에 올립니다.
형식: {"images":[{"name":"01","prompt":"...","size":"1024x1536","quality":"medium"}]}
사용: main 브랜치 tools/gen_image.sh

## 전속 모델 (2026-11-10)
- models/model_W.jpg — 여자 전속 모델(후보 여2), 키 168cm
- models/model_M.jpg — 남자 전속 모델(후보 남1), 키 182cm
- 같은 인물로 만들려면 요청 항목에 "refs": ["models/model_W.jpg"] 추가 → OpenAI edits(input_fidelity high)로 생성
