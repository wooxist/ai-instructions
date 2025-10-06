# 참조 자료

## 기술 문서

### React Hooks
- useState: 상태 관리 기본 훅
- useEffect: 부수 효과 처리 (LocalStorage 연동)
- 문서: https://react.dev/reference/react

### LocalStorage API
```javascript
// 저장
localStorage.setItem('key', JSON.stringify(data));

// 불러오기
const data = JSON.parse(localStorage.getItem('key'));

// 삭제
localStorage.removeItem('key');

// 전체 삭제
localStorage.clear();
```

### TailwindCSS 유틸리티 클래스
- 자주 사용할 클래스:
  - Container: `max-w-md`, `mx-auto`, `p-4`
  - Input: `border`, `rounded`, `px-3`, `py-2`
  - Button: `bg-blue-500`, `hover:bg-blue-600`, `text-white`
  - Checkbox: `w-5`, `h-5`, `rounded`

## 디자인 참고
- 미니멀한 할일 앱 디자인
- 컬러 스킴: 블루 계열 (완료), 그레이 (미완료)
- 완료 항목: 텍스트 스트라이크스루 + 투명도 감소

## 모범 사례
1. 컴포넌트는 단일 책임 원칙 준수
2. Props는 명확한 타입과 이름 사용
3. 상태 업데이트는 불변성 유지
4. 사용자 입력은 항상 검증
