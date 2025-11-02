# Task 1: 8장, 9장을 Book3-draft로 이동

## 목적
8장과 9장의 내용을 Book3-draft 디렉토리로 복사하고, 보관 목적을 설명하는 README.md를 작성한다.

## 입력
- `doc/book1/vol-1-part-3-chapter-08.md` (성능 최적화)
- `doc/book1/vol-1-part-3-chapter-09.md` (평가와 검증)

## 출력
- `doc/book3-draft/vol-1-part-3-chapter-08.md`
- `doc/book3-draft/vol-1-part-3-chapter-09.md`
- `doc/book3-draft/README.md`

## 실행 방법

### 1단계: 8장 복사
1. `doc/book1/vol-1-part-3-chapter-08.md` 읽기
2. 내용을 그대로 `doc/book3-draft/vol-1-part-3-chapter-08.md`에 작성

### 2단계: 9장 복사
1. `doc/book1/vol-1-part-3-chapter-09.md` 읽기
2. 내용을 그대로 `doc/book3-draft/vol-1-part-3-chapter-09.md`에 작성

### 3단계: README.md 작성
`doc/book3-draft/README.md` 파일 생성:

```markdown
# Book 3 Draft (임시 보관)

이 디렉토리는 향후 **3권: 고급 최적화와 측정**에 포함될 예정인 챕터들을 임시 보관하는 공간입니다.

## 보관된 챕터

### 8장. 성능 최적화: 품질, 비용, 속도의 균형 맞추기
- **원래 위치**: Book1 Part 3
- **이동 이유**: API 사용자 및 프로그래밍 가능한 독자 대상
- **내용**: 토큰 수 최적화, 응답 시간 측정, 비용-품질 트레이드오프

### 9장. 인스트럭션의 평가와 검증
- **원래 위치**: Book1 Part 3
- **이동 이유**: 정량적 측정 도구가 필요한 고급 내용
- **내용**: 평가 지표 설계, A/B 테스트, 자동화된 검증

## 3권 구상

**대상 독자**: 
- API를 사용하는 개발자
- 프로그래밍으로 자동화 도구를 만들 수 있는 사용자
- 정량적 측정과 최적화에 관심 있는 고급 사용자

**주요 주제**: 
- 정량적 성능 측정
- 자동화된 평가 시스템
- 대규모 최적화 전략
- 비용 관리 및 모니터링

## 상태

- [x] Book1에서 이동 완료 (2025-11-03)
- [ ] 3권 전체 구조 설계
- [ ] 대상 독자 재정의
- [ ] 챕터 내용 재구성
- [ ] 추가 챕터 기획
```

## 완료 기준
- [ ] book3-draft/vol-1-part-3-chapter-08.md 파일 생성 완료
- [ ] book3-draft/vol-1-part-3-chapter-09.md 파일 생성 완료
- [ ] book3-draft/README.md 파일 생성 완료
- [ ] 파일 내용이 원본과 일치함
- [ ] README.md가 보관 목적을 명확히 설명함

## 주의사항
- 원본 파일(book1의 8장, 9장)은 이 Task에서 삭제하지 않음 (Task 4에서 처리)
- 복사만 수행하고 내용은 수정하지 않음
