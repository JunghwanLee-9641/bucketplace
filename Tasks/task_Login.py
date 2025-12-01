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


class Task_Login:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)
        self.home_page = HomePage(driver)

    ############"""Check Functions"""############

    def check_Login_Page(self):
        """
        Login 화면에 정상적으로 진입 했는지를 확인 하기 위한 기능
        """
        input_Id_Check = self.home_page.check_element(self.login_page.qa_Login_EmailAddress)
        input_Password_Check = self.home_page.check_element(self.login_page.qa_Login_Password)
        Login_Button_Check = self.home_page.check_element(self.login_page.qa_Login_Login_Button)
        
        if input_Id_Check and input_Password_Check and Login_Button_Check:
            logging.info("정상적으로 Login 화면에 진입 되었습니다.")
        else:
            logging.error("정상적으로 Login 화면에 진입 하지 못했습니다.")
            assert input_Id_Check and input_Password_Check and Login_Button_Check

    def login_check(self):
        """ 로그인 정상 진행을 판단 """
        if self.home_page.check_element(self.home_page.qa_Home_GuideMe_Button, timeout=30):
            self.home_page.click(self.home_page.qa_Home_GuideMe_Button)

        if self.login_page.check_element(self.home_page.qa_Home_Setting_Button, timeout=30):
            logging.info("정상적으로 로그인 되었습니다.")
        else:
            logging.info("로그인 실패.")
            assert False

    ############"""Control Functions"""############

    def input_Id(self, email: str):
        """ 아이디 입력 """
        self.login_page.send_keys(self.login_page.qa_Login_EmailAddress, email)
        logging.info("정상적으로 id가 입력 되었습니다.")

    def input_Password(self, pw: str):
        """ 비밀번호 입력 """
        self.login_page.send_keys(self.login_page.qa_Login_Password, pw)
        logging.info("정상적으로 pw가 입력 되었습니다.")

    def click_Login_Button(self):
        """ 로그인 버튼 클릭 """
        self.login_page.click(self.login_page.qa_Login_Login_Button)
        logging.info("정상적으로 로그인 버튼이 클릭 되었습니다.")

    # def login(self, email: str, pw: str, keep_logged_in=False):
    #     """ 이메일 + 비밀번호 로그인 수행 (통합 메서드) """
    #     self.login_page.login(email, pw, keep_logged_in)
