==============================================
오늘의집 iOS 자동화 테스트 과제
==============================================

[과제 개요]
iOS 기기의 자동화 테스트 코드를 Page Object Model 패턴으로 작성했습니다.
실제 기기 연결 및 Appium 서버 관리 로직은 테스트 케이스 작성 능력을 
평가하는데 복잡도만 높일 수 있어 최소화했습니다.


[프로젝트 구조]
Config/         : 환경 변수, 계정 정보 관리
Pages/          : 페이지별 Locator 정의 (Page Object Model)
Tasks/          : 테스트 비즈니스 로직 (Check/Control Functions)
Tests/          : 실제 테스트 케이스 (test_Login.py)
TestBase/       : Appium 드라이버 설정
conftest.py     : pytest fixture 및 설정
main.py         : 테스트 실행 스크립트
requirements.txt: 필요한 Python 패키지 목록/필요한 파일을 지속적으로 설치 및 업데이트를 위해 사용 합니다.


[설계 구조]
Tests (테스트 시나리오)
  ↓ 호출
Tasks (비즈니스 로직 - check_xxx, click_xxx 등)
  ↓ 사용
Pages (UI 요소 정의 - locator)
  ↓ 상속
BasePage (공통 기능 - click, send_keys, check_element)

[주요 특징]
- Page Object Model 패턴으로 유지보수성 확보
- 테스트 레이어 분리 (Tests → Tasks → Pages → BasePage)
- 각 테스트는 Test Step과 Expected Result로 명확히 구분