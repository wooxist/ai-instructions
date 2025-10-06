# 작업 계획: book/ 디렉토리 정리 및 문서 통합

**작업 ID**: cleanup_book_directory  
**작성일**: 2025-10-06  
**완료일**: 2025-10-06  
**담당자**: Claude  
**우선순위**: 높음  
**상태**: ✅ 완료

---

## 목표

book/ 디렉토리의 불필요한 파일을 제거하고, 작업 관련 문서를 .cache/todo/로 통합하여 SSOT 원칙을 준수하는 깔끔한 구조 확립

---

## 배경 및 문제 정의

### 현재 상황
- book/ 디렉토리에 작업 관리 문서(TODO.md)와 메타 문서(DOC-STRUCTURE.md, WRITER.md, visual-style-guide.md)가 혼재
- 프로젝트 전체 구조가 정비되면서 일부 문서의 역할이 중복됨
- _analysis/ 디렉토리가 book/ 안에 있어 역할이 불명확

### 문제점
1. **문서 중복**: TODO 관련 내용이 book/TODO.md와 .cache/todo/TODO.md에 분산
2. **역할 혼재**: book/은 콘텐츠, .cache/todo/는 작업 관리로 분리되어야 하는데 혼재
3. **집필 가이드 분산**: WRITER.md와 visual-style-guide.md 내용을 .instructions.md로 통합 필요

---

## 완료된 작업

### ✅ Task 1: book/TODO.md 내용 확인 및 이관
- [x] book/TODO.md 내용 분석 완료
- [x] Phase 2.1 완료 내역 .cache/todo/TODO.md에 반영
- [x] book/TODO.md → .cache/todo/context/book-phase-2-1-history.md로 이관
- [x] book/TODO.md 삭제 완료

### ✅ Task 2: _analysis/ 디렉토리 이관
- [x] book/_analysis/ 내용 확인
- [x] book/_analysis/*.md → .cache/todo/analysis/로 이동
- [x] book/_analysis/ 디렉토리 삭제 완료

### ✅ Task 3-4: 메타 문서 정리
- [x] DOC-STRUCTURE.md 확인 및 처리
- [x] 삭제 파일 목록 확정

---

## 산출물

1. **이관된 파일**:
   - `.cache/todo/context/book-phase-2-1-history.md`
   - `.cache/todo/analysis/7-10-gap.md`
   - `.cache/todo/analysis/bridge-content-options.md`

2. **업데이트된 파일**:
   - `.cache/todo/TODO.md` (Phase 2.1 완료 내역 반영)

3. **삭제된 파일**:
   - `book/TODO.md`
   - `book/_analysis/` 디렉토리

---

*작업 완료: 2025-10-06*
