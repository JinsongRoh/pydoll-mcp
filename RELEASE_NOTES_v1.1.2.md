# 🚀 PyDoll MCP Server v1.1.2 - Korean Windows 완전 지원!

## 🐛 중요한 버그 수정

### Unicode 인코딩 오류 완전 해결
- **문제**: 한국어 Windows 환경(cp949)에서 이모지/유니코드 문자 출력 시 `UnicodeEncodeError` 발생
- **해결**: 포괄적인 인코딩 안전성 구현
  - 다중 레벨 fallback 시스템
  - 환경별 적응형 인코딩 감지
  - UTF-8 강제 설정 지원

### 패키지 실행 오류 해결
- **문제**: `python -m pydoll_mcp` 실행 시 `__main__.py` 누락으로 인한 실행 불가
- **해결**: 완전한 `__main__.py` 모듈 구현
  - 모듈 진입점 제공
  - 인코딩 사전 설정
  - 오류 처리 강화

## 🌍 국제화 개선

### 한국어 Windows 환경 완전 지원
- cp949, euc-kr 인코딩 환경에서 안전한 출력
- 자동 UTF-8 변환 및 fallback
- 콘솔 코드페이지 자동 설정

### 다국어 환경 호환성
- 모든 Windows 로케일 지원
- Linux/macOS 환경 호환성 유지
- 자동 인코딩 감지 및 적응

## 🔧 기술적 개선사항

### 인코딩 처리 시스템
```python
# 환경 변수 자동 설정
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'

# 다중 레벨 인코딩 안전성
try:
    print(banner_with_emojis)
except UnicodeEncodeError:
    print(safe_ascii_banner)
```

### Claude Desktop 통합 개선
```json
{
  "mcpServers": {
    "pydoll": {
      "command": "python",
      "args": ["-m", "pydoll_mcp.server"],
      "env": {
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUTF8": "1",
        "PYDOLL_LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## 🧪 테스트 통과

### 환경별 테스트 완료
- ✅ 한국어 Windows 10/11 (cp949)
- ✅ 영어 Windows (utf-8)
- ✅ Linux Ubuntu/CentOS
- ✅ macOS Intel/Apple Silicon

### 기능 테스트
- ✅ Health check 정상 작동
- ✅ 서버 시작/종료 정상
- ✅ Claude Desktop 연동 확인
- ✅ 모든 26개 도구 정상 작동

## 📦 설치 및 업데이트

### 새로 설치
```bash
pip install pydoll-mcp==1.1.2
```

### 기존 버전 업데이트
```bash
pip install --upgrade pydoll-mcp
```

### 수동 설치 (개발자용)
```bash
git clone https://github.com/JinsongRoh/pydoll-mcp.git
cd pydoll-mcp
pip install -e .
```

## 🔄 마이그레이션 가이드

### v1.1.1에서 업그레이드
1. 기존 설치 제거: `pip uninstall pydoll-mcp`
2. 새 버전 설치: `pip install pydoll-mcp==1.1.2`  
3. Claude Desktop 설정 업데이트 (환경 변수 추가)
4. 재시작 후 테스트: `python -m pydoll_mcp.server --test`

### 설정 파일 업데이트 필요
Claude Desktop 설정에 환경 변수 추가가 필요합니다. 자세한 내용은 README.md를 참조하세요.

## 🐛 알려진 이슈

### Windows PowerShell
일부 PowerShell 환경에서는 여전히 수동 환경 변수 설정이 필요할 수 있습니다:
```powershell
$env:PYTHONIOENCODING="utf-8"
$env:PYTHONUTF8="1"
```

### 해결 방법
이 문제는 향후 버전에서 완전히 자동화될 예정입니다.

## 🎯 다음 버전 계획

### v1.2.0 (예정)
- 자동 인코딩 설정 (환경 변수 불필요)
- GUI 설정 도구
- 고급 오류 복구 시스템
- 성능 최적화

## 💝 기여자

- **Jinsong Roh**: 메인 개발 및 버그 수정
- **커뮤니티**: 버그 리포트 및 피드백

## 🔗 링크

- **GitHub**: https://github.com/JinsongRoh/pydoll-mcp
- **PyPI**: https://pypi.org/project/pydoll-mcp/
- **문서**: https://github.com/JinsongRoh/pydoll-mcp/wiki
- **이슈 리포트**: https://github.com/JinsongRoh/pydoll-mcp/issues

---

**v1.1.2는 특히 한국어 Windows 사용자들을 위한 필수 업데이트입니다!** 🇰🇷✨
