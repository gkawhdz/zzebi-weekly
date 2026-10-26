#!/usr/bin/env bash
# 컴퓨터 없이 미디어(릴스·이미지)를 공개 주소로 올리는 도구
# 사용: bash tools/media_push.sh 파일1 [파일2 ...]
# 결과: 각 파일의 공개 주소 https://raw.githubusercontent.com/gkawhdz/zzebi-weekly/media/<파일명> 출력
# 방식: 'media' 브랜치에 커밋 1개만 유지(매번 force push) → 저장소가 커지지 않음.
#       2일 지난 파일은 자동 삭제. Metricool은 예약할 때 파일을 자기 서버로 복사하므로 원본은 금방 지워도 됨.
set -euo pipefail
REPO=https://github.com/gkawhdz/zzebi-weekly.git
W=$(mktemp -d)
git clone -q --single-branch --branch media "$REPO" "$W" 2>/dev/null || { git init -q "$W"; git -C "$W" checkout -q --orphan media; git -C "$W" remote add origin "$REPO"; }
find "$W" -maxdepth 1 -type f ! -name '.*' -mtime +2 -delete 2>/dev/null || true
for f in "$@"; do cp "$f" "$W/"; touch "$W/$(basename "$f")"; done
cd "$W"
git checkout -q --orphan tmp-media && git add -A
git -c user.name=zzebi-bot -c user.email=gkawhdz@gmail.com commit -qm "media $(date +%F_%H%M)"
git push -qf origin HEAD:media 2>&1 | grep -v -e '^remote:' -e 'negotiat' || true
for f in "$@"; do echo "https://raw.githubusercontent.com/gkawhdz/zzebi-weekly/media/$(basename "$f")"; done
