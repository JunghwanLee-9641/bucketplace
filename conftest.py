import pytest
import logging
from TestBase.webDriverSetup import WebDriverSetup
from Tasks.task_Common import Task_Common
from Tasks.task_Login import Task_Login
from Tasks.task_Main import Task_Main


logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)


@pytest.fixture(scope='module')
def driver():
    """
    테스트 모듈별로 Appium driver를 생성하고 관리합니다.
    각 테스트 파일 실행 시 한 번만 앱을 시작하고, 모든 테스트 완료 후 종료합니다.
    """
    drv = WebDriverSetup().get_driver()
    try:
        yield drv
    finally:
        try:
            drv.quit()
        except Exception:
            pass


@pytest.fixture(scope='module')
def task_login(driver):
    """로그인 관련 테스트 작업을 수행하는 Task 객체"""
    return Task_Login(driver)


@pytest.fixture(scope='module')
def task_main(driver):
    """메인 화면 관련 테스트 작업을 수행하는 Task 객체"""
    return Task_Main(driver)


@pytest.fixture(scope='module')
def task_common(driver):
    """공통 작업을 수행하는 Task 객체"""
    return Task_Common(driver)
