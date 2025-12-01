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
from Pages.page_ManagePatient import ManagePatientPage, AddPatientPage
from Pages.page_CaseDetail import CaseDetailPage


class Task_CaseDetail:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.home_page = HomePage(driver)
        self.managepatient_page = ManagePatientPage(driver)
        self.addpatient_page = AddPatientPage(driver)
        self.casedetail_page = CaseDetailPage(driver)

    ############"""Check Functions"""############

    def check_CaseDetail_Page(self, name: str):
        """
        CaseDetail 화면에 정상적으로 진입 했는지를 확인 하기 위한 기능
        """
        Open_Button_Check = self.casedetail_page.check_element(self.casedetail_page.qa_CaseDetail_Open_Button)
        Order_Button_Check = self.casedetail_page.check_element(self.casedetail_page.qa_CaseDetail_Order_Button)
        PatientName_Check = self.casedetail_page.is_static_text_visible(name)

        if Open_Button_Check and Order_Button_Check and PatientName_Check:
            logging.info(f"정상적으로 {name} Case Detail에 진입 되었습니다.")
        else:
            logging.error(f"정상적으로 {name} Case Detail에 진입 하지 못했습니다.")
            assert Open_Button_Check and Order_Button_Check and PatientName_Check

    def check_CaseDetail_CopyCase(self, name: str):
        """
        CaseDetail 화면의 Copy 버튼이 정상적으로 동작하는지 확인 하기 위한 기능
        """
        Copy_Button_Check = self.casedetail_page.is_static_text_visible(name)
        if Copy_Button_Check:
            logging.info(f"정상적으로 {Copy_Button_Check} Case Detail의 Copy Case가 확인 되었습니다.")
        else:
            logging.error(f"정상적으로 {Copy_Button_Check} Case Detail의 Copy Case가 확인 되지 않았습니다.")
            assert Copy_Button_Check

    def check_CaseDetail_CopyCase_NotExists(self, name: str):
        """
        주어진 이름의 Case가 리스트에 존재하지 않는지 확인
        """
        if self.managepatient_page.is_static_text_visible(name):
            logging.error("'%s' Case가 이미 존재합니다.", name)
            assert False, f"'{name}' Case가 존재함"
        logging.info("'%s' Case가 존재하지 않음을 확인했습니다.", name)


    ############"""Control Functions"""############

    def longclick_CaseDetail_Case(self, name: str):
        CaseName = self.casedetail_page.find_static_text(name)
        self.casedetail_page.long_press(element=CaseName, duration=2)
        logging.info("정상적으로 Case Detail 화면의 Case가 롱클릭 되었습니다.")
    
    def click_CaseDetail_UploadRawData(self):
        self.casedetail_page.click(self.casedetail_page.qa_CaseHistory_UploadRawData)
        logging.info("정상적으로 Case Detail 화면의 Upload Raw Data 버튼이 클릭 되었습니다.")
    
    def click_CaseDetail_Copy(self):
        self.casedetail_page.click(self.casedetail_page.qa_CaseHistory_Copy)
        logging.info("정상적으로 Case Detail 화면의 Copy 버튼이 클릭 되었습니다.")
    
    def click_CaseDetail_GetHelp(self):
        self.casedetail_page.click(self.casedetail_page.qa_CaseHistory_GetHelp)
        logging.info("정상적으로 Case Detail 화면의 Get Help 버튼이 클릭 되었습니다.")

    def click_CaseDetail_Delete(self):
        self.casedetail_page.click(self.casedetail_page.qa_CaseHistory_Delete)
        logging.info("정상적으로 Case Detail 화면의 Delete 버튼이 클릭 되었습니다.")
    
    def click_CaseDetail_CaseList(self, index: int = 0):
        """
        CaseDetail 화면에 있는 chevronDownBold 이미지 리스트 중 index번째를 클릭한다.
        """
        self.casedetail_page.select_element(
            locator=self.casedetail_page.qa_CaseDetail_Chevron_List,
            index=index
        )
        logging.info("정상적으로 Case Detail 화면의 %d번째 chevron이 클릭 되었습니다.", index)

    def click_CaseDetail_list(self, name: str):
        """환자 리스트에서 특정 이름을 찾아 탭"""
        element = self.managepatient_page.find_static_text(name)
        element.click()
        logging.info("환자 리스트에서 '%s' 를 선택했습니다.", name)

    def click_CaseDetail_Open_Button(self):
        self.casedetail_page.click(self.casedetail_page.qa_CaseDetail_Open_Button)
        logging.info("정상적으로 Case Detail 화면의 Open 버튼이 클릭 되었습니다.")

    def click_CaseDetail_Order_Button(self):
        self.casedetail_page.click(self.casedetail_page.qa_CaseDetail_Order_Button)
        logging.info("정상적으로 Case Detail 화면의 Order 버튼이 클릭 되었습니다.")
