# PyDoll MCP Server v1.2.0 Release Notes

Released: 2025-07-19

이 릴리스는 PyDoll 2.3.1 지원을 추가하고 새로운 기능들을 제공합니다.

## 🚀 PyDoll 2.3.1 업그레이드

- **의존성 업데이트**: PyDoll 2.2.1에서 2.3.1로 업그레이드
- **완벽한 호환성**: 모든 기존 기능과 100% 호환성 유지
- **향상된 안정성**: PyDoll 2.3.1의 버그 수정 및 개선사항 적용

## ✨ 새로운 기능

### 🔧 Chrome DevTools Protocol 도메인 명령어 조회
- **새로운 도구**: `fetch_domain_commands`
- Chrome DevTools Protocol의 사용 가능한 모든 명령어 조회
- 특정 도메인(Page, Network, DOM 등)의 명령어 필터링 지원
- 디버깅 및 고급 자동화에 유용

### 🎯 부모 요소 탐색
- **새로운 도구**: `get_parent_element`
- 선택한 요소의 부모 요소 정보 가져오기
- 모든 속성(attributes) 포함 옵션
- 바운딩 박스(bounds) 정보 포함 옵션
- DOM 트리 탐색 및 컨텍스트 이해에 유용

### ⏱️ 브라우저 시작 타임아웃 설정
- **새로운 옵션**: `start_timeout`
- 브라우저 시작 대기 시간을 커스터마이즈 가능 (1-300초)
- 느린 시스템이나 복잡한 설정에서 유용
- 기본값: 30초

## 🔄 기술적 개선사항

### 타입 힌팅 개선
- PyDoll 2.3.1의 향상된 타입 힌팅 지원
- 더 나은 IDE 자동완성 및 타입 체크
- 코드 가독성 및 유지보수성 향상

### 성능 최적화
- PyDoll 2.3.1의 성능 개선사항 적용
- 요소 선택 스크립트 최적화
- Windows 환경에서의 안정성 향상

## 📊 도구 통계

- **총 도구 수**: 79개 (이전 77개)
- **Navigation 도구**: 11개 (+1)
- **Element 도구**: 16개 (+1)
- **나머지 카테고리**: 변경 없음

## 🔧 설치 및 업그레이드

### 신규 설치
```bash
pip install pydoll-mcp==1.2.0
```

### 업그레이드
```bash
pip install --upgrade pydoll-mcp
```

### PyDoll 업그레이드 확인
```bash
pip install --upgrade pydoll-python>=2.3.1
```

## 💡 사용 예시

### Chrome DevTools Protocol 명령어 조회
```
"브라우저의 Page 도메인에서 사용 가능한 모든 명령어를 보여줘"
"Network 도메인의 Chrome DevTools Protocol 명령어 목록을 가져와"
```

### 부모 요소 탐색
```
"이 버튼의 부모 요소를 찾아서 모든 속성을 보여줘"
"선택한 입력 필드의 부모 컨테이너 정보를 가져와"
```

### 브라우저 시작 타임아웃
```
"느린 시스템을 위해 60초 타임아웃으로 브라우저를 시작해"
"start_timeout을 120초로 설정하여 Chrome을 실행해"
```

## 🐛 알려진 문제

- 일부 환경에서 PyDoll 2.3.1 자동 감지가 실패할 수 있음
- 이 경우 수동으로 PyDoll을 업그레이드하세요

## 🙏 감사의 말

이번 릴리스는 PyDoll 팀의 지속적인 개선과 커뮤니티의 피드백 덕분에 가능했습니다.

특히 PyDoll 2.3.1의 새로운 기능들을 제안하고 구현한 모든 기여자들께 감사드립니다.

---

PyDoll MCP Server v1.2.0 - Powered by PyDoll 2.3.1 🚀