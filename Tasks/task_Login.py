import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging

from Pages.page_Login import LoginPage, LoginPage_MessageBox
from Pages.page_Main import MainPage


class Task_Login:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.login_message_box = LoginPage_MessageBox(driver)
        self.main_page = MainPage(driver)

    ############"""Check Functions"""############

    def check_Login_Page(self):
        """
        Login 화면에 정상적으로 진입 했는지를 확인 하기 위한 기능
        """
        checks = {
            'lookaround': self.login_page.check_element(self.login_page.qa_Login_Lookaround_Button),
            'kakao': self.login_page.check_element(self.login_page.qa_Login_KakaoLogin_Button),
            'apple': self.login_page.check_element(self.login_page.qa_Login_AppleLogin_Button),
            'naver': self.login_page.check_element(self.login_page.qa_Login_NaverLogin_Button),
            'facebook': self.login_page.check_element(self.login_page.qa_Login_FacebookLogin_Button),
            'emailLogin': self.login_page.check_element(self.login_page.qa_Login_EmailLogin_Button),
            'createAccount': self.login_page.check_element(self.login_page.qa_Login_CreateNewAccount_Button),
            'help': self.login_page.check_element(self.login_page.qa_Login_Help_Button)
        }
        missing = [name for name, ok in checks.items() if not ok]
        assert not missing, f"Login 화면 요소 미노출: {', '.join(missing)}"
        logging.info("정상적으로 Login 화면에 진입 되었습니다.")

    def check_EmailLogin_Page(self):
        """
        이메일로 로그인 화면에 정상적으로 진입 했는지를 확인하기 위한 기능
        """
        checks = {
            'email text field': self.login_page.check_element(self.login_page.qa_Login_EmailAddress),
            'pw text field': self.login_page.check_element(self.login_page.qa_Login_Password),
            'complete button': self.login_page.check_element(self.login_page.qa_Login_Complete_Button),
            'Help Button': self.login_page.check_element(self.login_page.qa_Login_Help_Button)
        }
        missing = [name for name, ok in checks.items() if not ok]
        assert not missing, f"이메일로 로그인 화면 요소 미노출: {', '.join(missing)}"
        logging.info("정상적으로 이메일로 로그인 화면에 진입 되었습니다.")

    def check_LoginMessage(self, message_type: str):
        """
        로그인 페이지의 다양한 메시지 노출 여부 확인
        Args:
            message_type: 'required_field', 'invalid_email_format', 'unregistered_email', 'login_attempt_limit' 등
        """
        message_map = {
            'required_field': (self.login_message_box.qa_Login_RequiredFieldMessage_Text, "필수 입력 항목"),
            'invalid_email_format': (self.login_message_box.qa_Login_InvalidEmailFormatMessage_Text, "이메일 형식 오류"),
            'unregistered_email': (self.login_message_box.qa_Login_UnregisteredEmailMessage_Text, "미등록 이메일"),
            'login_attempt_limit': (self.login_message_box.qa_Login_LoginAttemptLimitMessage_Text, "로그인 시도 제한")
        }
        if message_type not in message_map:
            raise ValueError(f"지원하지 않는 메시지 타입: {message_type}")
        
        locator, msg_name = message_map[message_type]
        ok = self.login_message_box.check_element(locator)
        assert ok, f"{msg_name} 메시지가 노출되지 않았습니다."
        logging.info(f"정상적으로 {msg_name} 메시지가 노출되었습니다.")
    

    def check_LoginMessage_NotDisplayed(self, message_type: str = 'all'):
        """
        로그인 페이지의 메시지가 나타나지 않는 것을 확인
        Args:
            message_type: 'required_field', 'invalid_email_format', 'unregistered_email', 'login_attempt_limit', 'all' (기본값)
        """
        message_map = {
            'required_field': (self.login_message_box.qa_Login_RequiredFieldMessage_Text, "필수 입력 항목"),
            'invalid_email_format': (self.login_message_box.qa_Login_InvalidEmailFormatMessage_Text, "이메일 형식 오류"),
            'unregistered_email': (self.login_message_box.qa_Login_UnregisteredEmailMessage_Text, "미등록 이메일"),
            'login_attempt_limit': (self.login_message_box.qa_Login_LoginAttemptLimitMessage_Text, "로그인 시도 제한")
        }
        
        # 'all'이면 모든 메시지 체크
        if message_type == 'all':
            check_types = message_map.keys()
        else:
            if message_type not in message_map:
                raise ValueError(f"지원하지 않는 메시지 타입: {message_type}")
            check_types = [message_type]
        
        # 각 메시지 타입별로 확인
        displayed_messages = []
        for msg_type in check_types:
            locator, msg_name = message_map[msg_type]
            # timeout을 짧게 설정하여 메시지가 없는지 확인
            if self.login_message_box.check_element(locator, timeout=2):
                displayed_messages.append(msg_name)
        assert not displayed_messages, f"다음 메시지가 예상치 않게 노출되었습니다: {', '.join(displayed_messages)}"
        
        if message_type == 'all':
            logging.info("정상적으로 모든 에러 메시지가 노출되지 않았습니다.")
        else:
            logging.info(f"정상적으로 {message_map[message_type][1]} 메시지가 노출되지 않았습니다.")
    
    def check_Complete_Button_State(self, expected_state: bool = True):
        """
        완료 버튼의 활성화/비활성화 상태를 확인
        Args:
            expected_state: True(활성화), False(비활성화) 기대 상태
        """
        is_enabled = self.login_page.is_element_enabled(self.login_page.qa_Login_Complete_Button)
        
        if expected_state:
            assert is_enabled, "완료 버튼이 비활성화 상태입니다. (활성화 상태 기대)"
            logging.info("정상적으로 완료 버튼이 활성화 상태입니다.")
        else:
            assert not is_enabled, "완료 버튼이 활성화 상태입니다. (비활성화 상태 기대)"
            logging.info("정상적으로 완료 버튼이 비활성화 상태입니다.")


    ############"""Control Functions"""############

    def click_Lookaround_Button(self):
        """둘러보기 버튼 클릭 (보이지 않으면 실패)"""
        ok = self.login_page.click(self.login_page.qa_Login_Lookaround_Button)
        assert ok, "둘러보기 버튼이 표시되지 않아 클릭할 수 없습니다."
        logging.info("정상적으로 둘러보기 버튼이 클릭 되었습니다.")
    
    def click_EmailLogin_Button(self):
        """이메일로 로그인 버튼 클릭 (보이지 않으면 실패)"""
        ok = self.login_page.click(self.login_page.qa_Login_EmailLogin_Button)
        assert ok, "이메일로 로그인 버튼이 표시되지 않아 클릭할 수 없습니다."
        logging.info("정상적으로 이메일로 로그인 버튼이 클릭 되었습니다.")

    def click_Complete_Button(self):
        """완료 버튼 클릭 (보이지 않으면 실패)"""
        ok = self.login_page.click(self.login_page.qa_Login_Complete_Button)
        assert ok, "완료 버튼이 표시되지 않아 클릭할 수 없습니다."
        logging.info("정상적으로 완료 버튼이 클릭 되었습니다.")

    def input_Id(self, email: str):
        """ 아이디 입력 """
        self.login_page.send_keys(self.login_page.qa_Login_EmailAddress, email)
        logging.info("정상적으로 id가 입력 되었습니다.")
    
    def input_Password(self, pw: str):
        """ 비밀번호 입력 """
        self.login_page.send_keys(self.login_page.qa_Login_Password, pw)
        logging.info("정상적으로 pw가 입력 되었습니다.")
    
    def input_Id_next(self, email: str):
        """ 아이디 입력 후 Next/Return 클릭 """
        self.login_page.send_keys_and_next(self.login_page.qa_Login_EmailAddress, email)
        logging.info("정상적으로 id가 입력 되었습니다.")

    def input_Password_next(self, pw: str):
        """ 비밀번호 입력 후 Next/Return 클릭 """
        self.login_page.send_keys_and_next(self.login_page.qa_Login_Password, pw)
        logging.info("정상적으로 pw가 입력 되었습니다.")
