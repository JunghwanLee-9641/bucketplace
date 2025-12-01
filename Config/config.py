""" 공통 변수 정의 """

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.normpath(os.path.join(BASE_DIR, '..'))

# 공용 변수
Test_Server_Env = ''


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
DEFAULT_TEST_PATHS = ["Tests/"]
DEFAULT_REPORT_DIR = "Report"
DEFAULT_Server_Env = "Operation"


# Appium 서버 설정
APPIUM_SERVER_CONFIG = {
    "host": os.environ.get("APPIUM_SERVER_HOST", "127.0.0.1"),
    "log_dir": os.path.join(PROJECT_ROOT, "logs"),
    "log_level": os.environ.get("APPIUM_LOG_LEVEL", "error"),
    "log_timestamp": True,
    "local_timezone": True,
    "extra_args": []
}
