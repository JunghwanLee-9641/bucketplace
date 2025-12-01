import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging

from Pages.page_Common import CommonACID

class Task_Common:
    def __init__(self, driver):
        self.driver = driver
        self.common_page = CommonACID(driver)

    ############"""Check Functions"""############
    def check_Allow_Notification(self):
        """
        공용 알림 허용 팝업이 정상적으로 진입 했는지를 확인 하기 위한 기능
        """
        checks = {
            "allow": self.common_page.check_element(self.common_page.qa_Common_Allow_Button),
            "notTrack": self.common_page.check_element(self.common_page.qa_Common_NotTrack_Button),
        }
        missing = [name for name, ok in checks.items() if not ok]
        assert not missing, f"알림 허용 팝업 요소 미노출: {', '.join(missing)}"
        logging.info("정상적으로 알림 허용 팝업이 나타났습니다.")


    ############"""Control Functions"""############

    def click_Common_Back_Button(self):
        ok = self.common_page.click(self.common_page.qa_Common_Back_Button)
        assert ok, "둘러보기 버튼이 표시되지 않아 클릭할 수 없습니다."
        logging.info("정상적으로 <- 버튼이 클릭 되었습니다.")

    def click_Common_Allow_Button(self):
        ok = self.common_page.click(self.common_page.qa_Common_Allow_Button)
        assert ok, "허용 버튼이 표시되지 않아 클릭할 수 없습니다."
        logging.info("정상적으로 허용 버튼이 클릭 되었습니다.")

    def click_Common_NotTrack_Button(self):
        ok = self.common_page.click(self.common_page.qa_Common_NotTrack_Button)
        assert ok, "허용 버튼이 표시되지 않아 클릭할 수 없습니다."
        logging.info("정상적으로 허용 버튼이 클릭 되었습니다.")

    def click_Common_Close_Button(self):
        ok = self.common_page.click(self.common_page.qa_Common_Close_Button)
        assert ok, "닫기 버튼이 표시되지 않아 클릭할 수 없습니다."
        logging.info("정상적으로 닫기 버튼이 클릭 되었습니다.")
    
    def click_Common_DoNotShowAgain_Button(self):
        ok = self.common_page.click(self.common_page.qa_Common_DoNotShowAgain_Button)
        assert ok, "다시보지않기 버튼이 표시되지 않아 클릭할 수 없습니다."
        logging.info("정상적으로 다시보지않기 버튼이 클릭 되었습니다.")