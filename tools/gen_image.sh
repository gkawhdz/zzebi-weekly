#!/usr/bin/env bash
# 이미지 생성 (Zapier 대체, 2026-11-10). GitHub imgreq 브랜치에 요청을 올리면 Actions가 OpenAI로 생성.
# 사용: bash tools/gen_image.sh <요청.json> <받을 폴더>
#   요청.json = {"images":[{"name":"01","prompt":"...","size":"1024x1536","quality":"medium"}, ...]}  (최대 8장)
#   같은 인물(전속 모델)로: 항목에 "refs":["models/model_W.jpg"] 추가 — studio/models/README.md 참고
# 결과: <받을 폴더>/<name>.jpg, 실패 목록은 <받을 폴더>/_done.json. 끝까지 기다림(최대 8분).
set -euo pipefail
REQ="$1"; OUT="$2"; REPO=gkawhdz/zzebi-weekly
ID="$(TZ=Asia/Seoul date +%Y%m%d_%H%M%S)_$RANDOM"
mkdir -p "$OUT"
python3 - "$REQ" <<'PY'
import json,sys; d=json.load(open(sys.argv[1])); assert d.get("images"), "images 비어 있음"
for j in d["images"]: assert j.get("name") and j.get("prompt"), "name·prompt 필요"
PY
W="$(mktemp -d)"; trap 'rm -rf "$W"' EXIT
git clone -q --depth 1 --single-branch -b imgreq "https://github.com/$REPO.git" "$W/r"
cp "$REQ" "$W/r/req/$ID.json"
( cd "$W/r" && git add "req/$ID.json" && git -c user.name=zzebi-team -c user.email=team@users.noreply.github.com commit -qm "image request $ID" \
  && for k in 1 2 3 4 5; do git pull -q --rebase origin imgreq && git push -q origin HEAD:imgreq && break; sleep 3; done )
echo "요청 올림: $ID (생성 대기...)"
for i in $(seq 1 96); do
  sleep 5
  ( cd "$W/r" && git fetch -q --depth 1 origin imgreq ) || continue
  if ( cd "$W/r" && git cat-file -e "FETCH_HEAD:out/$ID/_done.json" 2>/dev/null ); then
    ( cd "$W/r" && git show "FETCH_HEAD:out/$ID/_done.json" ) > "$OUT/_done.json"
    for f in $(python3 -c "import json,sys;print(' '.join(json.load(open(sys.argv[1]))['ok']))" "$OUT/_done.json"); do
      ( cd "$W/r" && git show "FETCH_HEAD:out/$ID/$f" ) > "$OUT/$f"
    done
    cat "$OUT/_done.json"; exit 0
  fi
done
echo "시간 초과: $ID 결과 없음 (GitHub Actions 확인 필요)" >&2; exit 1
