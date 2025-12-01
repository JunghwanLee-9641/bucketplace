import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import subprocess
import pytest,logging

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.ios import XCUITestOptions

import Config.config as config
from Pages.page_OrderForm import OrderFormPage


class Task_OrderForm:
    def __init__(self, driver):
        self.driver = driver
        self.orderform_page = OrderFormPage(driver)

    ############"""Check Functions"""############

    def check_OrderForm_Page(self):
        """
        OrderForm 화면에 정상적으로 진입 했는지를 확인 하기 위한 기능
        """
        OrderFormTitle_Check = self.orderform_page.check_element(self.orderform_page.qa_OrderForm_TitleName)
        # selection_All_Check = self.orderform_page.check_element(self.orderform_page.qa_OrderForm_Selection_All_Check)
        
        if OrderFormTitle_Check: # and selection_All_Check:
            logging.info("정상적으로 OrderForm 화면에 진입 되었습니다.")
        else:
            logging.error("정상적으로 OrderForm 화면에 진입 하지 못했습니다.")
            assert OrderFormTitle_Check # and selection_All_Check
        
        
    def check_OrderForm_LabName(self, expected_name: str):
        """
        OrderForm 화면의 LabName 버튼이 기대한 이름인지 확인
        """
        locator = (
            self.orderform_page.qa_OrderForm_LabName[0],
            self.orderform_page.qa_OrderForm_LabName[1].format(name=expected_name)
        )
        if self.orderform_page.check_element(locator):
            logging.info("정상적으로 Lab 이름 '%s' 이 확인 되었습니다.", expected_name)
        else:
            logging.error("정상적으로 Lab 이름 '%s' 이 확인 되지 않았습니다.", expected_name)
            assert False

    def check_OrderForm_SubmitOrder_Button_Enabled(self, *, timeout: int = 10) -> None:
        """
        OrderForm 화면의 SubmitOrder 버튼이 활성화되어 있는지 확인하고, 아니면 실패 처리한다.
        """
        if self.orderform_page.is_element_enabled(
            self.orderform_page.qa_OrderForm_SubmitOrder_Button,
            timeout=timeout
        ):
            logging.info("정상적으로 OrderForm 화면의 SubmitOrder 버튼이 활성화 되었습니다.")
            return
        logging.error("정상적으로 OrderForm 화면의 SubmitOrder 버튼이 활성화 되지 않았습니다.")
        assert False, "OrderForm SubmitOrder 버튼 비활성화"
    

    ############"""Control Functions"""############

    def click_OrderForm_Select_All_Check(self):
        """ Select All checkbox 클릭 """
        self.orderform_page.click(self.orderform_page.qa_OrderForm_Selection_All_Check)
        logging.info("정상적으로 Select All checkbox가 클릭 되었습니다.")
    
    def click_OrderForm_SubmitOrder_Button(self):
        """ Submit Order 버튼 클릭 """
        self.orderform_page.click(self.orderform_page.qa_OrderForm_SubmitOrder_Button)
        logging.info("정상적으로 Submit Order 버튼이 클릭 되었습니다.")

    def click_OrderForm_Type(self, index: int = 1):
        """ Order Type 선택 (여러 개 중 index번째) """
        self.orderform_page.select_element(
            locator=self.orderform_page.qa_OrderForm_Type_List,
            index=index
        )
        logging.info("정상적으로 %d번째 Order Type이 클릭 되었습니다.", index)

    def click_OrderForm_Method(self, index: int = 1):
        """ Order Method 선택 (여러 개 중 index번째) """
        self.orderform_page.select_element(
            locator=self.orderform_page.qa_OrderForm_Method_List,
            index=index
        )
        logging.info("정상적으로 %d번째 Order Method가 클릭 되었습니다.", index)

    def click_OrderForm_Material(self, index: int = 1):
        """ Order Material 선택 (여러 개 중 index번째) """
        self.orderform_page.select_element(
            locator=self.orderform_page.qa_OrderForm_Material_List,
            index=index
        )
        logging.info("정상적으로 %d번째 Order Material이 클릭 되었습니다.", index)

    def select_OrderForm_Type_By_Name(self, name: str):
        """Order Type 리스트에서 전달한 accessibility id를 선택"""
        locator = self.orderform_page.locator_by_accessibility_id(name)
        self.orderform_page.click(locator)
        logging.info("정상적으로 Order Type '%s' 이 선택 되었습니다.", name)

    def select_OrderForm_Material_By_Name(self, name: str):
        """Order Material 리스트에서 전달한 텍스트가 포함된 셀을 클릭"""
        if self.orderform_page.click_cell_by_descendant_text(
            self.orderform_page.qa_OrderForm_Material_Options,
            name
        ):
            logging.info("정상적으로 Order Material '%s' 이 선택 되었습니다.", name)
        else:
            logging.error("Order Material '%s' 선택에 실패했습니다.", name)
            assert False

    def select_OrderForm_Method_By_Name(self, name: str):
        """Order Method 리스트에서 전달한 accessibility id를 선택"""
        locator = self.orderform_page.locator_by_accessibility_id(name)
        self.orderform_page.click(locator)
        logging.info("정상적으로 Order Method '%s' 이 선택 되었습니다.", name)

