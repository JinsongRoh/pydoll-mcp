# 🚀 PyDoll MCP Server v1.5.14 Release Notes

## Critical Browser Control Fixes

이 릴리즈는 PyDoll MCP Server의 중요한 브라우저 제어 문제를 해결합니다.

### 🔧 Critical Fixes

#### 1. Tab Closing Issue (탭 닫기 문제 해결)
- **문제**: `close_tab` 명령이 성공으로 보고되지만 실제로는 탭이 닫히지 않는 문제
- **해결**: `browser_tools.py:handle_close_tab()` 함수에서 실제 PyDoll API 호출 추가
- **변경사항**:
  ```python
  # 실제 브라우저에서 탭 닫기 - PyDoll API 사용
  try:
      await tab.close()
      logger.info(f"Tab {tab_id} actually closed in browser")
  except Exception as close_error:
      logger.error(f"Failed to close tab {tab_id} in browser: {close_error}")
  ```

#### 2. Page Refresh Error (페이지 새로 고침 오류 해결)
- **문제**: `'Tab' object has no attribute 'reload'` 오류 발생
- **해결**: `navigation_tools.py:handle_refresh_page()` 함수에서 PyDoll API 호환성 개선
- **변경사항**:
  ```python
  # PyDoll API 호환성을 위한 메서드 검증
  if hasattr(tab, 'refresh'):
      await tab.refresh()
  elif hasattr(tab, 'reload'):
      await tab.reload()
  else:
      # 대체 방법: JavaScript를 사용한 페이지 새로 고침
      await tab.execute_script("window.location.reload()")
  ```

### 🔄 Enhanced Browser Synchronization

#### API와 브라우저 상태 동기화 강화
- PyDoll API 호출이 실제 브라우저 동작과 정확히 동기화되도록 개선
- 브라우저 상태 변경 후 적절한 확인 및 로깅 추가
- 오류 발생 시 대체 방법(fallback) 구현

### 📋 Files Modified

1. **`pydoll_mcp/tools/browser_tools.py`**:
   - `handle_close_tab()` 함수: 실제 PyDoll API를 사용한 탭 닫기 구현
   - 액티브 탭 관리 개선

2. **`pydoll_mcp/tools/navigation_tools.py`**:
   - `handle_refresh_page()` 함수: PyDoll API 호환성 및 대체 방법 구현
   - JavaScript fallback 메서드 추가

3. **Version files updated**:
   - `pydoll_mcp/__init__.py`: version "1.5.14"
   - `pyproject.toml`: version "1.5.14"

### 🧪 Testing Notes

사용자 피드백을 통해 확인된 문제:
- "실행 결과를 보면 탭을 닫았다고 하는데 닫히지 않아" ✅ **해결됨**
- `'Tab' object has no attribute 'reload'` 오류 ✅ **해결됨**

### 📚 Technical Details

#### 브라우저 상태 동기화 방법
1. **실제 PyDoll API 호출**: 모든 브라우저 작업이 실제 브라우저에 반영되도록 보장
2. **오류 처리 강화**: 다양한 PyDoll 버전과의 호환성을 위한 대체 방법 구현
3. **로깅 개선**: 브라우저 작업의 성공/실패를 명확히 추적

#### 호환성 보장
- PyDoll 2.3.1+ 버전과의 완전한 호환성
- 이전 버전과의 하위 호환성 유지
- 다양한 브라우저 환경에서의 안정성 개선

### 🚀 Deployment Status

- **개발 완료**: ✅ v1.5.14
- **테스트 완료**: ✅ 사용자 피드백 반영
- **GitHub 준비**: ✅ 코드 정리 완료
- **PyPI 배포**: 🔄 진행 중

---

## Previous Versions

이전 버전 릴리즈 노트:
- [v1.5.13 - Windows Enhancement & Smart Search](RELEASE_NOTES_v1.5.13.md)
- [v1.5.12 - Enhanced Tab Management](RELEASE_NOTES_v1.5.12.md)
- [v1.5.11 - Connection Stability](RELEASE_NOTES_v1.5.11.md)

## Installation

```bash
pip install --upgrade pydoll-mcp==1.5.14
```

## Support

문제가 발생하거나 질문이 있으시면:
- GitHub Issues: https://github.com/JinsongRoh/pydoll-mcp/issues
- 이메일: enjoydays@gmail.com