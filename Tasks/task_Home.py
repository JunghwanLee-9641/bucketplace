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
from Pages.page_Login import LoginPage
from Pages.page_Home import HomePage, AccountInfoPage, SaveExitPage



class Task_Home:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.home_page = HomePage(driver)
        self.account_page = AccountInfoPage(driver)

    ############"""Check Functions"""############

    def check_Home_Page(self):
        """
        Home 화면에 정상적으로 진입 했는지를 확인 하기 위한 기능
        """
        Scan_Button_Check = self.home_page.check_element(self.home_page.qa_Home_StartScan_Button)
        ManagePatient_Button_Check = self.home_page.check_element(self.home_page.qa_Home_ManagePatient_Button)
        ManageOrder_Button_Check = self.home_page.check_element(self.home_page.qa_Home_ManageOrder_Button)
        
        if Scan_Button_Check and ManagePatient_Button_Check and ManageOrder_Button_Check:
            logging.info("정상적으로 Home 화면에 진입 되었습니다.")
        else:
            logging.error("정상적으로 Home 화면에 진입 하지 못했습니다.")
            assert Scan_Button_Check and ManagePatient_Button_Check and ManageOrder_Button_Check
    
    ############"""Control Functions"""############

    def click_Home_Button(self):
        self.home_page.click(self.home_page.qa_Home_Home_Button)
        logging.info("정상적으로 Home 버튼이 클릭 되었습니다.")

    #Treatment Scan 버튼 클릭
    def click_ScanStart_Button(self):
        self.home_page.click(self.home_page.qa_Home_StartScan_Button)
        logging.info("정상적으로 Treatment Scan 버튼이 클릭 되었습니다.")

    def click_ManagePatient_Button(self):
        self.home_page.click(self.home_page.qa_Home_ManagePatient_Button)
        logging.info("정상적으로 Manage Patient 버튼이 클릭 되었습니다.")

    def click_ManageOrder_Button(self):
        self.home_page.click(self.home_page.qa_Home_ManageOrder_Button)
        logging.info("정상적으로 Manage Order 버튼이 클릭 되었습니다.")

    def click_Account_Info(self):
        self.account_page.click(self.account_page.qa_Home_AccountInfo_ManageAccount)
        logging.info("정상적으로 Account 버튼이 클릭 되었습니다.")

    def click_Logout_Button(self):
        self.account_page.click(self.account_page.qa_Home_AccountInfo_Logout)
        logging.info("정상적으로 로그아웃 버튼이 클릭 되었습니다.")

    def click_Home_SaveAndExit(self):
        self.home_page.click(self.home_page.qa_Home_SaveAndExit)
        logging.info("정상적으로 Home Save And Exit 버튼이 클릭 되었습니다.")