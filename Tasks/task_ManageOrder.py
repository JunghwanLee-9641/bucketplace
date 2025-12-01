import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import subprocess
import pytest,logging

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.ios import XCUITestOptions

import Config.config as config
from Pages.page_ManageOrder import ManageOrderPage, OrderSummaryPage


class Task_ManageOrder:
    def __init__(self, driver):
        self.driver = driver
        self.manageorder_page = ManageOrderPage(driver)
        self.ordersummary_page = OrderSummaryPage(driver)

    ############"""Check Functions"""############

    def check_ManageOrder_Page(self):
        """
        ManageOrder 화면에 정상적으로 진입 했는지를 확인 하기 위한 기능
        """
        ManageOrderTitle_Check = self.manageorder_page.check_element(self.manageorder_page.qa_ManageOrder_TitleName)
        ManageOrder_Overall_Check = self.manageorder_page.check_element(self.manageorder_page.qa_ManageOrder_Overall)
        ManageOrder_Search_Check = self.manageorder_page.check_element(self.manageorder_page.qa_ManageOrder_Search)

        if ManageOrderTitle_Check and ManageOrder_Overall_Check and ManageOrder_Search_Check:
            logging.info("정상적으로 ManageOrder 화면에 진입 되었습니다.")
        else:
            logging.error("정상적으로 ManageOrder 화면에 진입 하지 못했습니다.")
            assert ManageOrderTitle_Check and ManageOrder_Overall_Check and ManageOrder_Search_Check

    def check_OrderSummary_Page(self):
        """
        OrderSummary 화면에 정상적으로 진입 했는지를 확인 하기 위한 기능
        """
        OrderSummaryTitle_Check = self.ordersummary_page.check_element(self.ordersummary_page.qa_OrderSummary_TitleName)
        CancelOrder_Button_Check = self.ordersummary_page.check_element(self.ordersummary_page.qa_OrderSummary_CancelOrder_Button)

        if OrderSummaryTitle_Check and CancelOrder_Button_Check:
            logging.info("정상적으로 OrderSummary 화면에 진입 되었습니다.")
        else:
            logging.error("정상적으로 OrderSummary 화면에 진입 하지 못했습니다.")
            assert OrderSummaryTitle_Check and CancelOrder_Button_Check

    def get_OrderSummary_Info(self, timeout: int = 30) -> dict:
        """
        Order Summary 상단의 주요 필드 값을 dict로 반환한다.
        화면 표시가 늦어질 수 있어 기본 대기 시간을 30초로 길게 잡는다.
        """
        fields = ["Status", "Lab Name", "Patient Name", "Case Name", "Order No."]
        data = {}
        for label in fields:
            data[label] = self.ordersummary_page.get_info_value(label, timeout=timeout)
        logging.info("Order Summary 정보 수집 완료: %s", data)
        return data

    def check_OrderSummary_Info(self, expected_info: dict):
        """
        Order Summary 상단의 주요 필드 값이 기대한 값과 일치하는지 확인한다.
        """
        actual_info = self.get_OrderSummary_Info()
        for key, expected_value in expected_info.items():
            actual_value = actual_info.get(key)
            if actual_value == expected_value:
                logging.info("Order Summary 정보 '%s' 이(가) 기대한 값 '%s' 으로 확인 되었습니다.", key, expected_value)
            else:
                logging.error("Order Summary 정보 '%s' 이(가) 기대한 값 '%s' 으로 확인 되지 않았습니다. (실제 값: '%s')", key, expected_value, actual_value)
                assert False, f"Order Summary 정보 '{key}' 불일치"
    
    ############"""Control Functions"""############

    def click_ManageOrder_List(self, name: str | None = None, index: int = 0, timeout: int = 10):
        """Manage Order 리스트에서 항목을 탭. 기본은 이름 기준 StaticText 목록에서 index번째를 클릭."""
        locator = (
            self.manageorder_page.qa_ManageOrder_List_Item[0],
            self.manageorder_page.qa_ManageOrder_List_Item[1].format(name=name or config.orderpatientName)
        )
        clicked = self.manageorder_page.click(locator, timeout=timeout)

        if clicked:
            logging.info("Manage Order 리스트에서 '%s' (%d번째)를 선택했습니다.", name or "<first>", index)
        else:
            logging.error("Manage Order 리스트에서 '%s' (%d번째)를 선택하지 못했습니다.", name or "<first>", index)
            assert False

    def click_OrderSummary_CancelOrder_Button(self, timeout: int = 10):
        """Order Summary 화면에서 'Cancel Order' 버튼을 탭."""
        clicked = self.ordersummary_page.click(self.ordersummary_page.qa_OrderSummary_CancelOrder_Button, timeout=timeout)

        if clicked:
            logging.info("Order Summary 화면에서 'Cancel Order' 버튼을 선택했습니다.")
        else:
            logging.error("Order Summary 화면에서 'Cancel Order' 버튼을 선택하지 못했습니다.")
            assert False
    
    
