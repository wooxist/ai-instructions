#!/bin/bash

# AI 협업 프로젝트 초기 설정 스크립트
# Usage: ./setup.sh

set -e

echo "🚀 AI 협업 프로젝트 초기 설정"
echo "================================"
echo ""

# 프로젝트명 입력
read -p "프로젝트명을 입력하세요: " PROJECT_NAME
if [ -z "$PROJECT_NAME" ]; then
    echo "❌ 프로젝트명은 필수입니다."
    exit 1
fi

# 오늘 날짜
TODAY=$(date +%Y-%m-%d)
echo ""
echo "📅 오늘 날짜: $TODAY"

# 첫 세션 파일 생성
SESSION_FILE=".session/${TODAY}.md"
echo ""
echo "📝 첫 세션 파일 생성: $SESSION_FILE"

cat > "$SESSION_FILE" << EOF
# 세션 $TODAY

**시작**: $(date +%H:%M)
**종료**: (진행 중)
**타입**: 프로젝트 초기 설정

---

## 관련 작업 (TODO 링크)
- 프로젝트 초기 설정
- ROADMAP 작성
- TODO 설정

---

## 이 세션에서 한 것

- [x] 프로젝트 구조 설정 (setup.sh 실행)
- [ ] ROADMAP 작성
- [ ] TODO 첫 작업 추가

## 다음 세션에서 할 것

1. ROADMAP.md에 Phase 계획 작성
2. TODO.md에 이번 주 작업 추가
3. 첫 번째 작업 시작

---

## 관련 파일

- .work/ROADMAP.md
- .work/TODO.md
- .instructions.md

## 중요 메모 / 결정사항

- 프로젝트명: $PROJECT_NAME
- 시작일: $TODAY

---

<!-- 
자동 생성됨 by setup.sh
-->
EOF

# 플레이스홀더 치환
echo ""
echo "🔧 프로젝트 설정 파일 업데이트 중..."

# README.md 업데이트
if [ -f "README.md" ]; then
    sed -i.bak "s/\[프로젝트명\]/$PROJECT_NAME/g" README.md
    rm README.md.bak 2>/dev/null || true
fi

# .work/ROADMAP.md 업데이트
if [ -f ".work/ROADMAP.md" ]; then
    sed -i.bak "s/\[프로젝트명\]/$PROJECT_NAME/g" .work/ROADMAP.md
    sed -i.bak "s/YYYY-MM-DD/$TODAY/g" .work/ROADMAP.md
    rm .work/ROADMAP.md.bak 2>/dev/null || true
fi

# .work/TODO.md 업데이트
if [ -f ".work/TODO.md" ]; then
    sed -i.bak "s/\[프로젝트명\]/$PROJECT_NAME/g" .work/TODO.md
    sed -i.bak "s/YYYY-MM-DD/$TODAY/g" .work/TODO.md
    rm .work/TODO.md.bak 2>/dev/null || true
fi

# .instructions.md 업데이트
if [ -f ".instructions.md" ]; then
    sed -i.bak "s/YYYY-MM-DD/$TODAY/g" .instructions.md
    rm .instructions.md.bak 2>/dev/null || true
fi

echo "✅ 설정 완료!"
echo ""
echo "================================"
echo "🎉 프로젝트 초기 설정이 완료되었습니다!"
echo ""
echo "📁 생성된 파일:"
echo "  - $SESSION_FILE (첫 세션)"
echo "  - .work/ROADMAP.md (업데이트됨)"
echo "  - .work/TODO.md (업데이트됨)"
echo ""
echo "🚀 다음 단계:"
echo "  1. .work/ROADMAP.md 를 열어 Phase 계획을 작성하세요"
echo "  2. .work/TODO.md 를 열어 이번 주 작업을 추가하세요"
echo "  3. AI와 대화를 시작하세요: '세션 시작' 또는 '이어서'"
echo ""
echo "📚 참고:"
echo "  - .instructions.md: AI 협업 지침"
echo "  - .project_template/workflows/: 워크플로우 가이드"
echo ""
echo "행복한 협업 되세요! 🤝"
echo "================================"
