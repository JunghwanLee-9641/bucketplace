import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import subprocess
import pytest,logging
from typing import Optional

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.ios import XCUITestOptions
from selenium.common.exceptions import NoSuchElementException

import Config.config as config
import Pages.page_Base as BasePage
from Pages.page_Login import LoginPage
from Pages.page_Home import HomePage
from Pages.page_ManagePatient import ManagePatientPage, AddPatientPage
from Pages.page_StartScan import StartScanPage, SelectPatientPage, SelectWorkflowPage, SelectTreatmentPage

class Task_StartScan:
    FDI_SEQUENCE = tuple(
        [f"1{i}" for i in range(8, 0, -1)] +   # 18~11
        [f"2{i}" for i in range(1, 9)] +        # 21~28
        [f"3{i}" for i in range(8, 0, -1)] +      # 48~41
        [f"4{i}" for i in range(1, 9)]         # 31~38
        
    )

    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.home_page = HomePage(driver)
        self.managepatient_page = ManagePatientPage(driver)
        self.addpatient_page = AddPatientPage(driver)
        self.startscan_page = StartScanPage(driver)
        self.selectpatient_page = SelectPatientPage(driver)
        self.selectworkflow_page = SelectWorkflowPage(driver)
        self.selecttreatment_page = SelectTreatmentPage(driver)

    ############"""Check Functions"""############

    def check_SelectPatient_Page(self):
        """
        Select Treatment 화면에 정상적으로 진입 했는지를 확인 하기 위한 기능
        """
        ManagePatient_Search_Check = self.selectpatient_page.check_element(self.selectpatient_page.qa_SelectPatient_Search)
        AddNewPatient_Button_Check = self.selectpatient_page.check_element(self.selectpatient_page.qa_SelectPatient_AddNewPatient_Button)
        
        if ManagePatient_Search_Check and AddNewPatient_Button_Check:
            logging.info("정상적으로 Select Patient 화면에 진입 되었습니다.")
        else:
            logging.error("정상적으로 Select Patient 화면에 진입 하지 못했습니다.")
            assert ManagePatient_Search_Check and AddNewPatient_Button_Check
    
    def check_SelectWorkflow_Page(self):
        """
        SelectWorkflow 화면에 정상적으로 진입 했는지를 확인 하기 위한 기능
        """
        PreOp_Maxilla_Check = self.selectworkflow_page.check_element(self.selectworkflow_page.qa_SelectWorkflow_PreopMaxilla_Checkbox)
        PreOp_Mandible_Check = self.selectworkflow_page.check_element(self.selectworkflow_page.qa_SelectWorkflow_PreopMandible_Checkbox)
        Restoration_Check = self.selectworkflow_page.check_element(self.selectworkflow_page.qa_SelectWorkflow_BasicProcedures)
        Implant_Scan_Check = self.selectworkflow_page.check_element(self.selectworkflow_page.qa_SelectWorkflow_ImplantRestoration)
        Orthodontic_Check = self.selectworkflow_page.check_element(self.selectworkflow_page.qa_SelectWorkflow_Orthodontic)
        
        if PreOp_Maxilla_Check and PreOp_Mandible_Check and Restoration_Check and Implant_Scan_Check and Orthodontic_Check:
            logging.info("정상적으로 Select Workflow 화면에 진입 되었습니다.")
        else:
            logging.error("정상적으로 Select Workflow 화면에 진입 하지 못했습니다.")
            assert PreOp_Maxilla_Check and PreOp_Mandible_Check and Restoration_Check and Implant_Scan_Check and Orthodontic_Check

    def check_SelectTreatment_Page(self):
        """
        Select Treatment 화면에 정상적으로 진입 했는지를 확인 하기 위한 기능
        """
        SelectTreatment_Next_Button = self.selecttreatment_page.check_element(self.selecttreatment_page.qa_SelectTreatment_Next_Button)
        SelectTreatment_Back_Button = self.selecttreatment_page.check_element(self.selecttreatment_page.qa_SelectTreatment_Back_Button)
        
        if SelectTreatment_Next_Button and SelectTreatment_Back_Button:
            logging.info("정상적으로 Select Treatment 화면에 진입 되었습니다.")
        else:
            logging.error("정상적으로 Select Treatment 화면에 진입 하지 못했습니다.")
            assert SelectTreatment_Next_Button and SelectTreatment_Back_Button
        
    def check_SelectWorkflow_Next_Button_Enabled(self, *, timeout: int = 10) -> None:
        """
        Select Workflow 화면의 Next 버튼이 활성화되어 있는지 확인하고, 아니면 실패 처리한다.
        """
        if self.selectworkflow_page.is_element_enabled(
            self.selectworkflow_page.qa_SelectWorkflow_Next_Button,
            timeout=timeout
        ):
            logging.info("정상적으로 Select Workflow 화면의 Next 버튼이 활성화 되었습니다.")
            return
        logging.error("정상적으로 Select Workflow 화면의 Next 버튼이 활성화 되지 않았습니다.")
        assert False, "Select Workflow Next 버튼 비활성화"

    def check_SelectTreatment_Next_Button_Enabled(self, *, timeout: int = 10) -> None:
        """
        Select Treatment 화면의 Next 버튼이 활성화되어 있는지 확인하고, 아니면 실패 처리한다.
        """
        if self.selecttreatment_page.is_element_enabled(
            self.selecttreatment_page.qa_SelectTreatment_Next_Button,
            timeout=timeout
        ):
            logging.info("정상적으로 Select Treatment 화면의 Next 버튼이 활성화 되었습니다.")
            return
        logging.error("정상적으로 Select Treatment 화면의 Next 버튼이 활성화 되지 않았습니다.")
        assert False, "Select Treatment Next 버튼 비활성화"

    ############"""Control Functions"""############

    def click_SelectPatient_list(self, *, index: int = 0, name_filter: Optional[str] = config.test_patientName):
        """
        Start Scan > Select Patient 화면에서 index 번째 환자를 선택한다.
        기본 index=0은 목록의 첫 번째 항목을 의미한다.
        """
        candidate_locators = [
            getattr(self.selectpatient_page, "qa_SelectPatient_PatientName_Cells", None),
        ]

        for locator in candidate_locators:
            if not locator:
                continue
            if self.selectpatient_page.select_element(locator, index=index):
                logging.info("환자 목록에서 인덱스 %s 항목을 선택했습니다.", index)
                return

        if name_filter:
            name_locator = (
                AppiumBy.IOS_CLASS_CHAIN,
                f'**/XCUIElementTypeStaticText[`name CONTAINS "{name_filter}" OR label CONTAINS "{name_filter}"`]'
            )
            name_elements = self.driver.find_elements(*name_locator)
            if name_elements and self.selectpatient_page.select_element(elements=name_elements, index=index):
                logging.info("키워드 '%s'로 필터링된 환자 목록에서 인덱스 %s 항목을 선택했습니다.", name_filter, index)
                return

        logging.error("환자 목록에서 인덱스 %s 항목을 선택하지 못했습니다.", index)
        assert False, "환자 선택 실패"
   
    def click_SelectWorkflow_Restoration(self):
        """ Select Workflow 화면에서 Restoration 항목 선택 """
        self.selectworkflow_page.click(self.selectworkflow_page.qa_SelectWorkflow_BasicProcedures)
        logging.info("정상적으로 Select Workflow 화면의 Restoration 항목이 클릭 되었습니다.")

    def click_SelectWorkflow_Next_Button(self):
        """ Select Workflow 화면에서 Next 버튼 클릭 """
        self.selectworkflow_page.click(self.selectworkflow_page.qa_SelectWorkflow_Next_Button)
        logging.info("정상적으로 Select Workflow 화면의 Next 버튼이 클릭 되었습니다.")

    def click_SelectTreatment_Next_Button(self):
        """ Select Treatment 화면에서 Next 버튼 클릭 """
        self.selecttreatment_page.click(self.selecttreatment_page.qa_SelectTreatment_Next_Button)
        logging.info("정상적으로 Select Treatment 화면의 Next 버튼이 클릭 되었습니다.")

    def click_SelectTreatment_SelectTeeth(self, teeth_numbers: Optional[object] = None):
        """
        Select Treatment 화면에서 지정한 치아 번호만 선택한다.
        인자가 없으면 FDI 기본 시퀀스를 모두 선택한다.
        """
        targets = self._normalize_teeth_numbers(teeth_numbers)
        self._tap_teeth(targets)

    def click_SelectTreatment_SelectTeeth_All(self):
        """FDI 전체 번호를 순차적으로 선택"""
        self._tap_teeth(list(self.FDI_SEQUENCE))

    def _normalize_teeth_numbers(self, teeth_numbers: Optional[object]) -> list[str]:
        if teeth_numbers is None or teeth_numbers == []:
            iterable = self.FDI_SEQUENCE
        elif isinstance(teeth_numbers, (str, int)):
            iterable = [teeth_numbers]
        else:
            try:
                iter(teeth_numbers)
            except TypeError:
                iterable = [teeth_numbers]
            else:
                iterable = teeth_numbers

        normalized = []
        for number in iterable:
            if number is None:
                continue
            normalized.append(str(number).strip())
        return normalized

    def _tap_teeth(self, targets: list[str]) -> None:
        for tooth in targets:
            try:
                element = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, tooth)
            except NoSuchElementException:
                logging.warning("치아 번호 %s 요소를 찾지 못했습니다.", tooth)
                continue

            if element.is_enabled():
                element.click()
                logging.info("치아 번호 %s를 선택했습니다.", tooth)
            else:
                logging.warning("치아 번호 %s 요소가 비활성화되어 있습니다.", tooth)
