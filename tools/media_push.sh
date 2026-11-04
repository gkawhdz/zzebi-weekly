#!/usr/bin/env bash
# 컴퓨터 없이 미디어(릴스·이미지)를 공개 주소로 올리는 도구
# 사용: bash tools/media_push.sh 파일1 [파일2 ...]       (인자 없이 실행하면 정리만 함)
# 결과: 각 파일의 공개 주소 https://raw.githubusercontent.com/gkawhdz/zzebi-weekly/media/<파일명> 출력
# 방식: 'media' 브랜치에 커밋 1개만 유지(매번 force push) → 저장소가 커지지 않음.
#
# 오래된 파일 자동 삭제 (2026-11-04 수정):
#   - 예전엔 `find -mtime +2`로 지웠는데, 매번 새로 clone 하면 모든 파일의 mtime이 '지금'이 되어
#     한 번도 삭제되지 않았음(10/27 파일까지 186개·1.3GB 누적). 그래서 파일명 속 날짜로 판단한다.
#   - 파일명에 든 YYYYMMDD(예: td20261104_a.mp4) 또는 MMDD(예: td1026_a.mp4 → 올해)를 읽어
#     KEEP_DAYS(기본 7일)보다 오래된 파일을 삭제. 날짜가 없는 파일(test_*.jpg 등)은 건드리지 않음.
#   - 삭제해도 게시에 영향 없음: Metricool은 예약 시 파일을 자기 서버(static.metricool.com/planner/…)로
#     복사해 두고 그 주소로 게시한다(getScheduledPosts의 media 필드가 모두 static.metricool.com 임을 11/4 확인).
#     raw.githubusercontent.com 주소는 예약 등록 순간에만 필요하다.
set -euo pipefail
REPO=https://github.com/gkawhdz/zzebi-weekly.git
KEEP_DAYS=${KEEP_DAYS:-7}
W=$(mktemp -d)
git clone -q --single-branch --branch media "$REPO" "$W" 2>/dev/null || { git init -q "$W"; git -C "$W" checkout -q --orphan media; git -C "$W" remote add origin "$REPO"; }

# 파일명 날짜 기준 정리
cutoff=$(date -d "-${KEEP_DAYS} days" +%Y%m%d)
year=$(date +%Y)
deleted=0
for f in "$W"/*; do
  [ -f "$f" ] || continue
  n=$(basename "$f")
  d=""
  if [[ $n =~ (20[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])) ]]; then
    d=${BASH_REMATCH[1]}
  elif [[ $n =~ ^[a-zA-Z]+((0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01]))[._-] ]]; then
    d="$year${BASH_REMATCH[1]}"
  fi
  if [ -n "$d" ] && [ "$d" -lt "$cutoff" ]; then rm -f "$f"; deleted=$((deleted+1)); fi
done
echo "cleanup: ${deleted}개 삭제 (파일명 날짜 < $cutoff), 남은 파일 $(find "$W" -maxdepth 1 -type f ! -name '.*' | wc -l)개" >&2

for f in "$@"; do cp "$f" "$W/"; done
cd "$W"
git checkout -q --orphan tmp-media && git add -A
git -c user.name=zzebi-bot -c user.email=gkawhdz@gmail.com commit -qm "media $(date +%F_%H%M)"
git push -qf origin HEAD:media 2>&1 | grep -v -e '^remote:' -e 'negotiat' || true
for f in "$@"; do echo "https://raw.githubusercontent.com/gkawhdz/zzebi-weekly/media/$(basename "$f")"; done
