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
from Pages.page_Login import LoginPage
from Pages.page_Home import HomePage
from Pages.page_Scan import ScanPage


class Task_Scan:
    def __init__(self, driver):
        self.driver = driver
        self.scan_page = ScanPage(driver)

    ############"""Check Functions"""############

    def check_Scan_Page(self):
        """
        Scan 화면에 정상적으로 진입 했는지를 확인 하기 위한 기능
        """
        ScanStart_Check = self.scan_page.check_element(self.scan_page.qa_Scan_StartScan_Button)
        ScanResume_Check = self.scan_page.check_element(self.scan_page.qa_Scan_ResumeScan_Button)
        NextButton_Check = self.scan_page.check_element(self.scan_page.qa_Scan_NextStage_Button)
        Toolbox_Check = self.scan_page.check_element(self.scan_page.qa_Scan_ToolBox_Button)
        
        if (ScanResume_Check or ScanStart_Check) and NextButton_Check and Toolbox_Check:
            logging.info("정상적으로 Scan 화면에 진입 되었습니다.")
        else:
            logging.error("정상적으로 Scan 화면에 진입 하지 못했습니다.")
            assert (ScanResume_Check or ScanStart_Check) and NextButton_Check and Toolbox_Check

    def check_Scan_Next_Button_Enabled(self, *, timeout: int = 10) -> None:
        """
        Scan 화면의 Next 버튼이 활성화되어 있는지 확인하고, 아니면 실패 처리한다.
        """
        if self.scan_page.is_element_enabled(
            self.scan_page.qa_Scan_NextStage_Button,
            timeout=timeout
        ):
            logging.info("정상적으로 Scan 화면의 Next 버튼이 활성화 되었습니다.")
            return
        logging.error("정상적으로 Scan 화면의 Next 버튼이 활성화 되지 않았습니다.")
        assert False, "Scan Next 버튼 비활성화"
    
    def check_Scan_Next_Button_Disabled(self, *, timeout: int = 10) -> None:
        """
        Scan 화면의 Next 버튼이 활성화되어 있는지 확인하고, 아니면 실패 처리한다.
        """
        if not self.scan_page.is_element_enabled(
            self.scan_page.qa_Scan_NextStage_Button,
            timeout=timeout
        ):
            logging.info("정상적으로 Scan 화면의 Next 버튼이 활성화 되었습니다.")
            return
        logging.error("정상적으로 Scan 화면의 Next 버튼이 활성화 되지 않았습니다.")
        assert False, "Scan Next 버튼 비활성화"


    def check_Scan_Order_Button_Disabled(self, *, timeout: int = 10) -> None:
        """
        Scan 화면의 Next 버튼이 활성화되어 있는지 확인하고, 아니면 실패 처리한다.
        """
        if not self.scan_page.is_element_enabled(
            self.scan_page.qa_Scan_Order_Button,
            timeout=timeout
        ):
            logging.info("정상적으로 Scan 화면의 Order 버튼이 비활성화 되었습니다.")
            return
        logging.error("정상적으로 Scan 화면의 Order 버튼이 비활성화 되지 않았습니다.")
        assert False, "Scan Order 버튼 비활성화"

    def check_Scan_Complete_Button_Disabled(self, *, timeout: int = 10) -> None:
        """
        Scan 화면의 Next 버튼이 활성화되어 있는지 확인하고, 아니면 실패 처리한다.
        """
        if not self.scan_page.is_element_enabled(
            self.scan_page.qa_Scan_Complete_Button,
            timeout=timeout
        ):
            logging.info("정상적으로 Scan 화면의 Complete 버튼이 비활성화 되었습니다.")
            return
        logging.error("정상적으로 Scan 화면의 Complete 버튼이 비활성화 되지 않았습니다.")
        assert False, "Scan Complete 버튼 비활성화"
        


    ############"""Control Functions"""############

    def click_Scan_Next_Button(self):
        """
        Scan 화면에서 Next 버튼 클릭
        """
        self.scan_page.click(self.scan_page.qa_Scan_NextStage_Button)
        logging.info("정상적으로 Scan 화면의 Next 버튼이 클릭 되었습니다.")
    
    def click_Scan_StartScan_Button(self):
        """
        Scan 화면에서 Start Scan 버튼 클릭
        """
        self.scan_page.click(self.scan_page.qa_Scan_StartScan_Button)
        logging.info("정상적으로 Scan 화면의 Start Scan 버튼이 클릭 되었습니다.")
    
    def click_Scan_Delete_Button(self):
        """
        Scan 화면에서 Delete 버튼 클릭
        """
        self.scan_page.click(self.scan_page.qa_Scan_Delete_Button)
        logging.info("정상적으로 Scan 화면의 Delete 버튼이 클릭 되었습니다.")

    def click_Scan_ToolBox_Button(self):
        """
        Scan 화면에서 ToolBox 버튼 클릭
        """
        self.scan_page.click(self.scan_page.qa_Scan_ToolBox_Button)
        logging.info("정상적으로 Scan 화면의 ToolBox 버튼이 클릭 되었습니다.")
    
    def input_Scan_CaseNameEdit(self, name: str):
        """
        Scan 화면에서 Case Name Edit 버튼 클릭 후 이름 입력
        """
        self.scan_page.click(self.scan_page.qa_Scan_CaseNameEdit_Button)
        self.scan_page.send_keys(self.scan_page.qa_Scan_CaseNameEdit_Input, name)
        self.scan_page.click(self.scan_page.qa_Scan_CaseNameEdit_Button)  #다시 Edit 버튼 클릭하여 입력 완료
        logging.info("정상적으로 Scan 화면의 Case Name이 '%s' 로 입력 되었습니다.", name)
    
    
