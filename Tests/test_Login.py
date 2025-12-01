import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import Config.config as config

#################Test Data################
#서버에 맞는 계정 정보 설정
if config.Test_Server_Env == 'Dev':
    Valid_ID = config.Valid_dev_ID
    Valid_PW = config.Valid_dev_PW
    Invalid_ID = config.Invalid_dev_ID
    Invalid_PW = config.Invalid_dev_PW
elif config.Test_Server_Env == 'Stage':
    Valid_ID = config.Valid_stage_ID
    Valid_PW = config.Valid_stage_PW
    Invalid_ID = config.Invalid_stage_ID
    Invalid_PW = config.Invalid_stage_ID_PW
else:   #Operation
    Valid_ID = config.Valid_operation_ID
    Valid_PW = config.Valid_operation_PW
    Invalid_ID = config.Invalid_operation_ID
    Invalid_PW = config.Invalid_operation_PW



#################Test Case################
def test_login_001(task_common):
    """
    App 최초 실행
    """
    #Expected Result
    task_common.check_Allow_Notification()

def test_login_002(task_common,task_login):
    """
    로그인 화면 진입
    """
    #Test Step
    task_common.click_Common_Allow_Button()
    #Expected Result
    task_login.check_Login_Page()

def test_login_003(task_login):
    """
    이메일로 로그인 페이지
    """
    #Test Step
    task_login.click_EmailLogin_Button()
    #Expected Result
    task_login.check_EmailLogin_Page()

def test_login_004(task_login):
    """
    로그인(공백)
    """
    #Test Step
    task_login.click_Complete_Button()
    #Expected Result
    task_login.check_LoginMessage('required_field')

def test_login_005(task_login):
    """
    로그인(이메일 필드 입력)
    """
    #Test Step
    invalid_id = Invalid_ID.split('@')[0]
    task_login.input_Id(invalid_id)
    #Expected Result
    task_login.check_LoginMessage('invalid_email_format')


def test_login_006(task_login):
    """
    로그인(이메일 필드 입력 - 이메일 형식)
    """
    #Test Step
    task_login.input_Id_next(Invalid_ID)
    #Expected Result
    task_login.check_LoginMessage('unregistered_email')

def test_login_007(task_login):
    """
    로그인(이메일 필드 입력 - 가입된 이메일)
    """
    #Test Step
    task_login.input_Id_next(Valid_ID)
    #Expected Result
    task_login.check_LoginMessage_NotDisplayed()

def test_login_008(task_login):
    """
    로그인(비밀번호 필드 입력)
    """
    #Test Step
    task_login.input_Password(Invalid_PW)
    #Expected Result
    task_login.check_Complete_Button_State(True)

def test_login_009(task_login):
    """
    로그인(Invalid 비밀번호 입력)
    """
    #Test Step
    task_login.input_Password_next(Invalid_PW)
    #Expected Result
    task_login.check_LoginMessage('login_attempt_limit')

def test_login_010(task_common, task_login):
    """
    로그인(Valid 비밀번호 입력)
    """
    #Test Step
    task_login.input_Password_next(Valid_PW)
    #Expected Result
    task_login.check_LoginMessage_NotDisplayed()
    task_common.check_Allow_Notification()

def test_login_011(task_common, task_main):
    """
    로그인 성공
    """
    #Test Step
    task_common.click_Common_Allow_Button()
    #Expected Result
    task_main.check_Event_Popup()
    

def test_login_012(task_common, task_main):
    """
    메인 페이지 진입
    """
    #Test Step
    task_common.click_Common_DoNotShowAgain_Button()
    #Expected Result
    task_main.check_Main_Page()
    