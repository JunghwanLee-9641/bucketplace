""" 공통 변수 정의 """

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, '..'))

# Test Type
Test_Type = ''

# Teams Webhook (환경 변수 또는 직접 문자열 입력)
TEAMS_WEBHOOK_URL = os.environ.get(
    "TEAMS_WEBHOOK_URL",
    "https://meditcompany.webhook.office.com/webhookb2/4212587f-65cf-4c02-9e9c-760bf0a3e606@1a869239-5ca3-402e-bc04-c0cb308ef1ab/IncomingWebhook/2f4ed90baf8b4b9b8c8f6295be4dcd1a/5d926ea5-cc1c-4546-9770-a10389866788/V2kDvSMLosytUiYnF-M8u4OxhGHFsj6efNDFkIQq6A6Uk1"
)
 

# 계정 정보
##dev
Valid_dev_ID = 'test_QA_Valid@bucketplace.com'
Valid_dev_PW = 'qwer1234%'
Invalid_dev_ID = 'test_QA_Invalid@bucketplace.com'
Invalid_dev_PW = 'qwer12345'
##stage
Valid_stage_ID = 'test_QA_Valid@bucketplace.com'
Valid_stage_PW = 'qwer1234%'
Invalid_stage_ID = 'test_QA_Invalid@bucketplace.com'
Invalid_stage_ID_PW = 'qwer12345'
##operation
Valid_operation_ID = 'test_QA_Valid@bucketplace.com'
Valid_operation_PW = 'qwer1234%'
Invalid_operation_ID = 'test_QA_Invalid@bucketplace.com'
Invalid_operation_PW = 'qwer1234%'

 

# NAS 및 SMB 연결 정보
SMB_SERVER = ""
SHARE_NAME = ""
REMOTE_DIR = ""
APP_NAME = ""

# 실행 기본값
DEFAULT_TEST_PATHS = ["Tests/test_Login.py"]
DEFAULT_REPORT_DIR = "Report"

# Appium 서버 설정
APPIUM_SERVER_CONFIG = {
    "host": os.environ.get("APPIUM_SERVER_HOST", "127.0.0.1"),
    "log_dir": os.path.join(PROJECT_ROOT, "logs"),
    "log_level": os.environ.get("APPIUM_LOG_LEVEL", "error"),
    "log_timestamp": True,
    "local_timezone": True,
    "extra_args": []
}

# Appium 포트 설정 (실제 기기 기준)
APPIUM_BASE_PORT = int(os.environ.get("APPIUM_BASE_PORT", "4723"))
APPIUM_PORT_INCREMENT = 10

# 실제 기기 자동화 설정
REAL_DEVICE_CAPABILITIES = {
    "platformName": "iOS",
    "appium:automationName": "XCUITest",
    "appium:platformVersion": os.environ.get("PLATFORM_VERSION", "17.0"),
    "appium:deviceName": os.environ.get("DEVICE_NAME", "iOS Device"),
    "appium:bundleId": os.environ.get("BUNDLE_ID", ""),
    "appium:xcodeOrgId": os.environ.get("XCODE_ORG_ID", ""),
    "appium:xcodeSigningId": os.environ.get("XCODE_SIGNING_ID", "Apple Development"),
    "appium:allowProvisioningUpdates": True,
    "appium:allowProvisioningDeviceRegistration": True,
    "appium:wdaLaunchTimeout": 300000,
    "appium:wdaConnectionTimeout": 300000,
    "appium:shouldUseSingletonTestManager": True,
    "appium:showXcodeLog": True,
}

REAL_DEVICE_APP_PATH = os.environ.get("REAL_DEVICE_APP_PATH", "")

# 로컬 다운로드 폴더: 현재 사용자의 홈 디렉토리 기준의 automationTest 폴더 지정
LOCAL_FOLDER = os.path.join(os.path.expanduser("~"), "automationTest")
