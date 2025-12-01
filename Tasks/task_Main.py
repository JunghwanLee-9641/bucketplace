import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest,logging

from Pages.page_Login import LoginPage
from Pages.page_Main import MainPage



class Task_Main:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.main_page = MainPage(driver)
    

    ############"""Check Functions"""############

    def check_Main_Page(self):
        """
        Main 화면에 정상적으로 진입 했는지를 확인 하기 위한 기능
        """
        checks = {
            "menu": self.main_page.check_element(self.main_page.qa_Main_Menu_Button),
            "notification": self.main_page.check_element(self.main_page.qa_Main_Notification_Button),
            "scrapbook": self.main_page.check_element(self.main_page.qa_Main_Scrapbook_Button),
            "shoppingbasket": self.main_page.check_element(self.main_page.qa_Main_Shopping_Button),
            "home": self.main_page.check_element(self.main_page.qa_Main_Home_Button),
            "community": self.main_page.check_element(self.main_page.qa_Main_Community_Button),
            "interior": self.main_page.check_element(self.main_page.qa_Main_Interior_Button),
            "mypage": self.main_page.check_element(self.main_page.qa_Main_Mypage_Button),
        }
        missing = [name for name, ok in checks.items() if not ok]
        assert not missing, f"Main 화면 요소 미노출: {', '.join(missing)}"
        logging.info("정상적으로 Main 화면에 진입 되었습니다.")

    def check_Event_Popup(self):
        """
        로그인 성공 후 메인 화면 진입 전 나타나는 팝업 확인
        """
        checks = {
            "close": self.common_page.check_element(self.common_page.qa_Common_Popup_Close_Button),
            "doNotShow": self.common_page.check_element(self.common_page.qa_Common_Popup_DoNotShowAgain_Button),
        }
        missing = [name for name, ok in checks.items() if not ok]
        assert not missing, f"로그인 성공 팝업 버튼 미노출: {', '.join(missing)}"
        logging.info("정상적으로 로그인 성공 팝업이 나타났습니다.")
    

    ############"""Control Functions"""############

    def click_Home_Button(self):
        """
        Main 화면의 하단 탭바에서 Home 버튼을 클릭 하는 기능
        """
        self.main_page.click(self.main_page.qa_Main_Home_Button)
        logging.info("정상적으로 Home 버튼을 클릭 하였습니다.")

    def click_Notification_Button(self):
        """
        Main 화면의 상단 우측 알림 버튼을 클릭 하는 기능
        """
        self.main_page.click(self.main_page.qa_Main_Notification_Button)
        logging.info("정상적으로 Notification 버튼을 클릭 하였습니다.")

    
   