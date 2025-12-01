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


class Task_ManagePatient:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.home_page = HomePage(driver)
        self.managepatient_page = ManagePatientPage(driver)
        self.addpatient_page = AddPatientPage(driver)

    ############"""Check Functions"""############

    def check_ManagePatient_Page(self):
        """
        ManagePatient 화면에 정상적으로 진입 했는지를 확인 하기 위한 기능
        """
        ManagePatient_Search_Check = self.managepatient_page.check_element(self.managepatient_page.qa_ManagePatient_Search)
        AddNewPatient_Button_Check = self.managepatient_page.check_element(self.managepatient_page.qa_ManagePatient_AddNewPatient_Button)
        
        if ManagePatient_Search_Check and AddNewPatient_Button_Check:
            logging.info("정상적으로 Manage Patient 화면에 진입 되었습니다.")
        else:
            logging.error("정상적으로 Manage Patient 화면에 진입 하지 못했습니다.")
            assert ManagePatient_Search_Check and AddNewPatient_Button_Check
    
    def check_AddPatient_Page(self):
        """
        ManagePatient 화면에 정상적으로 진입 했는지를 확인 하기 위한 기능
        """
        AddNewPatient_Name_Check = self.addpatient_page.check_element(self.addpatient_page.qa_AddNewPatient_Name)
        RegisterOnly_Button_Check = self.addpatient_page.check_element(self.addpatient_page.qa_AddNewPatient_RegisterOnly_Button)
        
        if AddNewPatient_Name_Check and RegisterOnly_Button_Check:
            logging.info("정상적으로 Add Patient 화면에 진입 되었습니다.")
        else:
            logging.error("정상적으로 Add Patient 화면에 진입 하지 못했습니다.")
            assert AddNewPatient_Name_Check and RegisterOnly_Button_Check

    def check_ManagePatient_AddNewPatient_Button(self):
        if self.addpatient_page.check_element(self.managepatient_page.qa_ManagePatient_AddNewPatient_Button):
            logging.info("정상적으로 ManagePatient 화면의 AddNewPatient 버튼이 확인 되었습니다.")
        else:
            logging.error("정상적으로 ManagePatient 화면의 AddNewPatient 버튼이 확인 되지 않았습니다.")
            assert False

    def check_ManagePatient_Search(self):
        if self.managepatient_page.check_element(self.managepatient_page.qa_ManagePatient_Search):
            logging.info("정상적으로 ManagePatient 화면의 Search 입력 필드가 확인 되었습니다.")
        else:
            logging.error("정상적으로 ManagePatient 화면의 Search 입력 필드가 확인 되지 않았습니다.")
            assert False      

    def check_AddNewPatient_Name(self):
        if self.addpatient_page.check_element(self.addpatient_page.qa_AddNewPatient_Name):
            logging.info("정상적으로 AddPatient 화면의 Name 입력 필드가 확인 되었습니다.")
        else:
            logging.error("정상적으로 AddPatient 화면의 Name 입력 필드가 확인 되지 않았습니다.")
            assert False

    def check_AddNewPatient_ID(self):
        if self.addpatient_page.check_element(self.addpatient_page.qa_AddNewPatient_PatientID):
            logging.info("정상적으로 AddPatient 화면의 Patient ID 입력 필드가 확인 되었습니다.")
        else:
            logging.error("정상적으로 AddPatient 화면의 Patient ID 입력 필드가 확인 되지 않았습니다.")
            assert False
    
    def check_input_AddNewPatient_Name(self, name: str):
        """ Patient Name 입력 값 확인 """
        self.addpatient_page.check_input_value(self.addpatient_page.qa_AddNewPatient_Name, name)
        logging.info("정상적으로 Name가 입력 되었습니다.")

    def check_input_AddNewPatient_ID(self, patient_id: str):
        """ Patient ID 입력 값 확인 """
        self.addpatient_page.check_input_value(self.addpatient_page.qa_AddNewPatient_PatientID, patient_id)
        logging.info("정상적으로 Patient ID가 입력 되었습니다.")

    def check_AddNewPatient_List(self, name: str):
        """ 환자 리스트에 생성한 환자가 있는지 확인 """
        if self.managepatient_page.is_static_text_visible(name, timeout=10):
            logging.info("정상적으로 환자 리스트에 생성한 환자가 확인 되었습니다.")
        else:
            logging.error("정상적으로 환자 리스트에 생성한 환자가 확인 되지 않았습니다.")
            assert False

    
    ############"""Control Functions"""############

    def input_AddNewPatient_Name(self, name: str):
        """ Patient Name 입력 """
        self.check_AddNewPatient_Name()
        self.addpatient_page.send_keys(self.addpatient_page.qa_AddNewPatient_Name, name)
        logging.info("정상적으로 Name가 입력 되었습니다.")
    
    def input_ManagePatient_Name(self, name: str):
        """ Patient Name 입력 """
        # self.check_AddNewPatient_Name()
        self.managepatient_page.send_keys(self.managepatient_page.qa_ManagePatient_Search, name)
        logging.info("정상적으로 Name가 입력 되었습니다.")

    def click_ManagePatient_AddNewPatient_Button(self):
        """ AddNewPatient 버튼 클릭 """
        self.check_ManagePatient_AddNewPatient_Button()
        self.addpatient_page.click(self.managepatient_page.qa_ManagePatient_AddNewPatient_Button)
        logging.info("정상적으로 AddNewPatient 버튼이 클릭 되었습니다.")

    def click_AddNewPatient_DatePicker(self):
        """ DatePicker 버튼 클릭 """
        self.addpatient_page.click(self.addpatient_page.qa_AddNewPatient_DatePicker)
        logging.info("정상적으로 DatePicker 버튼이 클릭 되었습니다.")
    
    def click_AddNewPatient_DatePicker_Done(self):
        """ DatePicker 모달을 스와이프로 닫습니다. """
        self.addpatient_page.swipe_down_to_close()
        logging.info("스와이프로 Date 모달을 닫았습니다.")

    def click_ManagePatient_Day_Button(self, label: str):
        day_locator = (AppiumBy.ACCESSIBILITY_ID, label)
        self.addpatient_page.click(day_locator)
        logging.info("정상적으로 Day 버튼이 클릭 되었습니다.")
    
    def click_ManagePatient_YearMonth_Button(self):
        self.addpatient_page.click(self.addpatient_page.qa_AddNewPatient_YearMonth)
        logging.info("정상적으로 YearMonth 버튼이 클릭 되었습니다.")

    def input_AddNewPatient_Year(self, year: str):
        """ Patient Year 입력 """
        self.addpatient_page.send_keys(self.addpatient_page.qa_AddNewPatient_Year, year)
        logging.info("정상적으로 Year가 입력 되었습니다.")

    def input_AddNewPatient_Month(self, month: str):
        """ Patient Month 입력 """
        self.addpatient_page.send_keys(self.addpatient_page.qa_AddNewPatient_Month, month)
        logging.info("정상적으로 Month가 입력 되었습니다.")
    
    def input_AddNewPatient_Day(self, day: str):
        """ Patient Day 입력 """
        self.addpatient_page.send_keys(self.addpatient_page.qa_AddNewPatient_Day, day)
        logging.info("정상적으로 Day가 입력 되었습니다.")

    def click_AddNewPatient_Female_Button(self):
        """ Female 버튼 클릭 """
        self.addpatient_page.click(self.addpatient_page.qa_AddNewPatient_Female)
        logging.info("정상적으로 Female 버튼이 클릭 되었습니다.")

    def click_AddNewPatient_Male_Button(self):
        """ Male 버튼 클릭 """
        self.addpatient_page.click(self.addpatient_page.qa_AddNewPatient_Male)
        logging.info("정상적으로 Male 버튼이 클릭 되었습니다.")

    def input_AddNewPatient_ID(self, patient_id: str):
        """ Patient ID 입력 """
        self.check_AddNewPatient_ID()
        self.addpatient_page.send_keys(self.addpatient_page.qa_AddNewPatient_PatientID, patient_id)
        logging.info("정상적으로 Patient ID 가 입력 되었습니다.")
    
    def click_RegisterOnly_Button(self):
        """ RegisterOnly 버튼 클릭 """
        self.addpatient_page.click(self.addpatient_page.qa_AddNewPatient_RegisterOnly_Button)
        logging.info("정상적으로 RegisterOnly 버튼이 클릭 되었습니다.")

    def click_AddNewPatient_RegisterOnly_Button(self):
        """ RegisterOnly 버튼 클릭 """
        self.addpatient_page.click(self.addpatient_page.qa_AddNewPatient_RegisterOnly_Button)
        logging.info("정상적으로 RegisterOnly 버튼이 클릭 되었습니다.")

    def click_ManagePatient_list(self, name: str):
        """환자 리스트에서 특정 이름을 찾아 탭"""
        element = self.managepatient_page.find_static_text(name)
        element.click()
        logging.info("환자 리스트에서 '%s' 를 선택했습니다.", name)