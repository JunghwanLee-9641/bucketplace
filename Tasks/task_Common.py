import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import subprocess
import pytest,logging

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.ios import XCUITestOptions

import Config.config as config
import Pages.page_Base as BasePage
from Pages.page_Common import CommonACID

class Task_Common:
    def __init__(self, driver):
        self.driver = driver
        self.common_page = CommonACID(driver)

    ############"""Check Functions"""############

    def click_Common_Close_Button(self):
        self.common_page.click(self.common_page.qa_Common_Close_Button)
        logging.info("정상적으로 X 버튼이 클릭 되었습니다.")

    def click_Common_Back_Button(self):
        self.common_page.click(self.common_page.qa_Common_Back_Button)
        logging.info("정상적으로 X 버튼이 클릭 되었습니다.")
    
    def click_Common_Cancel_Button(self, timeout: int = 10):
        """공용 'Cancel' 버튼을 탭."""
        clicked = self.common_page.click(self.common_page.qa_Common_Cancel_Button, timeout=timeout)

        if clicked:
            logging.info("공용 'Cancel' 버튼을 선택했습니다.")
        else:
            logging.error("공용 'Cancel' 버튼을 선택하지 못했습니다.")
            assert False
        
    def click_Common_Confirm_Button(self, timeout: int = 10):
        """공용 'Confirm' 버튼을 탭."""
        clicked = self.common_page.click(self.common_page.qa_Common_Confirm_Button, timeout=timeout)

        if clicked:
            logging.info("공용 'Confirm' 버튼을 선택했습니다.")
        else:
            logging.error("공용 'Confirm' 버튼을 선택하지 못했습니다.")
            assert False
    
    def click_Common_Delete_Button(self, timeout: int = 10):
        """공용 'Delete' 버튼을 탭."""
        clicked = self.common_page.click(self.common_page.qa_Common_Delete_Button, timeout=timeout)

        if clicked:
            logging.info("공용 'Delete' 버튼을 선택했습니다.")
        else:
            logging.error("공용 'Delete' 버튼을 선택하지 못했습니다.")
            assert False
