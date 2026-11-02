#!/bin/bash
# 공개 사이트(https://zzebi-st.github.io) 반영: zzebi-weekly 에서 만든 사이트 파일만 zzebi-st/zzebi-st.github.io 저장소로 복사·푸시
# 사용: bash tools/publish_site.sh "커밋 메시지"   (먼저 /home/claude/zzebi-st.github.io 에 clone 되어 있어야 함)
set -e
SRC=$(cd "$(dirname "$0")/.." && pwd)
DST=${SITE_REPO:-/home/claude/zzebi-st.github.io}
[ -d "$DST/.git" ] || { echo "사이트 저장소 없음: $DST (add_repo zzebi-st/zzebi-st.github.io push 후 clone)"; exit 1; }
cd "$DST"; git pull -q origin main || true
rm -rf r now; rm -f index.html 404.html og*.jpg .push_test
cp -r "$SRC/r" "$SRC/index.html" "$SRC/404.html" "$SRC"/og*.jpg .
[ -d "$SRC/now" ] && cp -r "$SRC/now" .
touch .nojekyll
printf '# zzebi-st.github.io\nZzebi.St 위클리 공개 사이트 (자동 생성 — 직접 수정하지 마세요).\n' > README.md
git add -A
git commit -qm "${1:-위클리 사이트 갱신}

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" || echo "변경 없음"
git push -q origin HEAD:main
echo "published → https://zzebi-st.github.io/now/"
