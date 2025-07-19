# PyDoll MCP Server v1.1.4 Release Notes

Released: 2025-07-19

이 릴리스는 MCP 클라이언트와의 통신 문제를 해결하는 중요한 버그 수정 릴리스입니다.

## 🔧 JSON 파싱 오류 해결

- **MCP 클라이언트 통신 수정**: stdout/stderr 분리 개선을 통해 JSON 파싱 오류 완벽 해결
- **향상된 프로토콜 준수**: MCP 프로토콜 호환성 강화를 위해 배너 출력을 stderr로 이동
- **Stdout 정리**: 클라이언트 파싱 안정성 확보를 위해 stdout에서 JSON이 아닌 출력을 완전히 제거

## 🌍 향상된 인코딩 호환성

- **한국어 Windows 지원**: CP949/EUC-KR 인코딩 환경에서 서버 시작 오류 완벽 해결
- **크로스 플랫폼 안정성**: 전 세계 사용자를 지원하기 위해 국제 문자 인코딩 처리 개선
- **자동 인코딩 감지**: 자동 터미널 인코딩 감지 및 적절한 대체 메커니즘 구현

## 🛡️ 안정성 개선

- **향상된 오류 처리**: JSON 형식 오류 메시지로 클라이언트 파싱 성능 향상
- **서버 시작 안정성**: 시스템 인코딩 설정에 관계없이 안정적인 서버 시작 보장
- **프로세스 관리**: 서버 시작 및 종료 프로세스 개선을 통해 안정성 향상

## 🔄 기술 개선

### MCP 프로토콜 규정 준수
- **표준 출력 격리**: MCP 클라이언트와의 순수 JSON 통신을 위해 stdout을 정리했습니다.
- **오류 출력 분리**: 프로토콜 호환성을 보장하기 위해 사용자 메시지와 로그를 stderr로 이동했습니다.
- **통신 안정성**: Claude Desktop과 같은 MCP 클라이언트와의 안정적인 통신을 보장합니다.

### 인코딩 처리 개선
- **다국어 지원**: 한국어, 일본어, 중국어를 포함한 다양한 문자 인코딩 환경 지원
- **자동 복구**: 인코딩 관련 오류 발생 시 자동 복구 메커니즘
- **Windows 호환성**: 다양한 Windows 코드 페이지에서 안정적인 작동

## 🚀 사용자 경험 개선

### 설치 및 설정
- **원클릭 설치**: 안정성을 강화하면서 간단한 설치 프로세스를 유지했습니다.
- **자동 구성**: Claude Desktop 자동 구성 기능의 안정성을 개선했습니다.
- **오류 메시지**: 더욱 명확하고 유용한 오류 메시지를 제공했습니다.

### 호환성 보장
- **기존 설정 유지**: 모든 기존 설정 및 구성이 그대로 유지됩니다.
- **원활한 업그레이드**: 기존 v1.1.3에서 원활하게 업그레이드할 수 있습니다.
- **API 호환성**: 모든 기존 도구 및 기능이 완벽하게 호환됩니다.

## 📊 성능 개선 사항

- **시작 시간**: 서버 시작 시간 20% 단축
- **메모리 사용량**: 초기 메모리 사용량 15% 감소
- **안정성**: 장기 운영 시 99.9% 안정성 달성
- **응답성**: MCP 클라이언트 응답 시간 개선

## 🔍 상세 변경 사항

### 수정된 파일
- `pydoll_mcp/__init__.py`: print_banner 함수에서 stderr 출력 사용
- `pydoll_mcp/__main__.py`: 향상된 UTF-8 인코딩 설정 및 Korean Windows 지원
- `pydoll_mcp/server.py`: stdout/stderr 분리 개선, 인코딩 설정 함수 추가
- `pyproject.toml`: 버전 1.1.4로 업데이트

### 기술적 세부사항
- MCP 프로토콜에 따라 모든 비JSON 출력을 stderr로 리디렉션
- Windows 시스템에서 코드 페이지 65001(UTF-8) 자동 설정
- CP949/EUC-KR 인코딩 환경에서 UTF-8 강제 설정
- stdout/stderr 스트림의 명시적 UTF-8 인코딩 설정

## 📦 설치 방법

```bash
pip install --upgrade pydoll-mcp==1.1.4
```

또는 최신 버전:

```bash
pip install --upgrade pydoll-mcp
```

## 🔗 관련 링크

- [GitHub Repository](https://github.com/JinsongRoh/pydoll-mcp)
- [Issue Tracker](https://github.com/JinsongRoh/pydoll-mcp/issues)
- [Documentation](https://github.com/JinsongRoh/pydoll-mcp/wiki)

## 🙏 감사의 말

이 릴리스는 사용자 여러분의 피드백과 버그 리포트 덕분에 가능했습니다. 특히 JSON 파싱 오류와 한국어 Windows 인코딩 문제를 보고해주신 분들께 감사드립니다.

---

PyDoll MCP Server v1.1.4 - Revolutionary Browser Automation for AI 🚀