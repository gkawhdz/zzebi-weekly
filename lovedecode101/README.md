# lovedecode101 콘텐츠 큐
- queue.json: 미전송 에피소드 목록(순서대로). 각 dir에 slide_01~10.png + caption.txt
- pipeline/: 제작 파이프라인 (head.html 템플릿, BRIEF.md 작가 규칙, build.py 렌더러, book_full.txt 원문 전체, body_NN.html 완성 원고)
- 새 에피소드 제작: body_NN.html 작성 → python3 -I pipeline/build.py NN → pipeline/out_NN/ 에 PNG 10장 → queue/epNN 로 복사 후 queue.json에 추가
- 규칙: 마지막 장 "다음 편:" 문구는 반드시 다음 에피소드 제목과 일치
