# imgreq — 이미지 생성 요청 브랜치 (Zapier 대체, 2026-11-10)
req/<id>.json 을 올리면 GitHub Actions가 OpenAI(저장소 Secret OPENAI_API_KEY)로 그림을 만들어 out/<id>/ 에 올립니다.
형식: {"images":[{"name":"01","prompt":"...","size":"1024x1536","quality":"medium"}]}
사용: main 브랜치 tools/gen_image.sh
