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

# 템플릿 디렉토리 확인
TEMPLATE_BASE="../.project_template"
if [ ! -d "$TEMPLATE_BASE" ]; then
    TEMPLATE_BASE="../../.project_template"
fi

if [ ! -d "$TEMPLATE_BASE" ]; then
    echo "⚠️  템플릿 디렉토리를 찾을 수 없습니다."
    echo "현재 위치에서 템플릿 없이 초기화합니다."
    TEMPLATE_BASE=""
fi

# 1. 첫 세션 파일 생성
SESSION_FILE=".session/${TODAY}.md"
echo ""
echo "📝 첫 세션 파일 생성: $SESSION_FILE"

if [ -f ".session/_template.md" ]; then
    # 템플릿에서 복사
    cp .session/_template.md "$SESSION_FILE"
    # 날짜 치환
    sed -i.bak "s/YYYY-MM-DD/$TODAY/g" "$SESSION_FILE"
    sed -i.bak "s/HH:MM/$(date +%H:%M)/g" "$SESSION_FILE"
    rm "${SESSION_FILE}.bak" 2>/dev/null || true
else
    # 템플릿이 없으면 기본 생성
    cat > "$SESSION_FILE" << EOF
# 세션 $TODAY

**시작**: $(date +%H:%M)
**종료**: (진행 중)
**타입**: 프로젝트 초기 설정

---

## 관련 작업 (TODO 링크)
- 프로젝트 초기 설정

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

## 중요 메모 / 결정사항

- 프로젝트명: $PROJECT_NAME
- 시작일: $TODAY
EOF
fi

# 2. ROADMAP.md 생성
echo ""
echo "📋 ROADMAP.md 생성..."

if [ -n "$TEMPLATE_BASE" ] && [ -f "$TEMPLATE_BASE/docs/ROADMAP.template.md" ]; then
    cp "$TEMPLATE_BASE/docs/ROADMAP.template.md" .work/ROADMAP.md
else
    cat > .work/ROADMAP.md << 'EOF'
# 프로젝트 로드맵

**프로젝트**: [프로젝트명]
**시작일**: YYYY-MM-DD
**상태**: 진행 중

---

## 🎯 프로젝트 목표

[이 프로젝트의 최종 목표]

---

## 📅 Phase별 계획

### Phase 1: [Phase 이름]
**목표**: [Phase 목표]

**세부 작업**:
- [ ] 1.1 - 작업 A
- [ ] 1.2 - 작업 B
- [ ] 1.3 - 작업 C

---

### Phase 2: [Phase 이름] (계획)
**목표**: [Phase 목표]

**세부 작업**:
- [ ] 2.1 - 작업 A
- [ ] 2.2 - 작업 B

---

## 📋 TODO 연동

각 Phase의 세부 작업은 [TODO.md](TODO.md)에서 관리됩니다.
EOF
fi

# 프로젝트명과 날짜 치환
sed -i.bak "s/\[프로젝트명\]/$PROJECT_NAME/g" .work/ROADMAP.md
sed -i.bak "s/YYYY-MM-DD/$TODAY/g" .work/ROADMAP.md
rm .work/ROADMAP.md.bak 2>/dev/null || true

# 3. TODO.md 생성
echo "📝 TODO.md 생성..."

if [ -n "$TEMPLATE_BASE" ] && [ -f "$TEMPLATE_BASE/tasks/TODO.template.md" ]; then
    cp "$TEMPLATE_BASE/tasks/TODO.template.md" .work/TODO.md
else
    cat > .work/TODO.md << 'EOF'
# TODO

**프로젝트**: [프로젝트명]
**마지막 업데이트**: YYYY-MM-DD

---

## 🎯 이번 주 우선순위

1. [ ] 
2. [ ] 
3. [ ] 

---

## 📋 ROADMAP 연계 작업

### Phase 1.1 - [작업명]
- [ ] 세부 작업 A (예상: 2h)
- [ ] 세부 작업 B (예상: 1h)

---

## ⚡ 즉흥 / 긴급 작업

- [ ] 

---

## ✅ 완료된 작업

### YYYY-MM-DD
- [x] 작업명 (소요: Xh) - [세션](../.session/YYYY-MM-DD.md)
EOF
fi

# 프로젝트명과 날짜 치환
sed -i.bak "s/\[프로젝트명\]/$PROJECT_NAME/g" .work/TODO.md
sed -i.bak "s/YYYY-MM-DD/$TODAY/g" .work/TODO.md
rm .work/TODO.md.bak 2>/dev/null || true

# 4. README.md 업데이트
if [ -f "README.md" ]; then
    echo "📄 README.md 업데이트..."
    sed -i.bak "s/\[프로젝트명\]/$PROJECT_NAME/g" README.md
    rm README.md.bak 2>/dev/null || true
fi

echo "✅ 설정 완료!"
echo ""
echo "================================"
echo "🎉 프로젝트 초기 설정이 완료되었습니다!"
echo ""
echo "📁 생성된 파일:"
echo "  - $SESSION_FILE (첫 세션)"
echo "  - .work/ROADMAP.md"
echo "  - .work/TODO.md"
echo ""
echo "🚀 다음 단계:"
echo "  1. .work/ROADMAP.md를 열어 Phase 계획을 작성하세요"
echo "  2. .work/TODO.md를 열어 이번 주 작업을 추가하세요"
echo "  3. AI와 대화를 시작하세요: '세션 시작' 또는 '이어서'"
echo ""
echo "📚 참고:"
echo "  - .instructions.md: AI 협업 지침"
echo ""
echo "행복한 협업 되세요! 🤝"
echo "================================"
