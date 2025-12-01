from Pages.page_Base import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

""" ManageOrder 페이지의 Locator를 정의 """
class ManageOrderPage(BasePage):
    # ManageOrder page

    #
    qa_ManageOrder_TitleName = (AppiumBy.ID, 'Manage Orders')
    #
    # qa_ManageOrder_Search = (AppiumBy.ID, 'qa_ManageOrder_Search')
    qa_ManageOrder_Search = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeImage[`name == "qa_ViewOrder_SearchBar"`]')
    #
    # qa_ManageOrder_SearchBar = (AppiumBy.ID, 'qa_ManageOrder_SearchBar')
    qa_ManageOrder_SearchBar = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeTextField[`name == "qa_ViewOrder_SearchBar"`]')
    #
    qa_ManageOrder_Overall = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeImage[`name == "qa_ViewOrder_Overall"`]')
    #
    qa_ManageOrder_Pending = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeImage[`name == "qa_ViewOrder_Pending"`]')
    #
    qa_ManageOrder_InProgress = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeImage[`name == "qa_ViewOrder_InProgress"`]')
    #
    qa_ManageOrder_InDelivery = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeImage[`name == "qa_ViewOrder_InDelivery"`]')
    #
    qa_ManageOrder_Received = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeImage[`name == "qa_ViewOrder_Received"`]')
    #
    qa_ManageOrder_Rejected = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeImage[`name == "qa_ViewOrder_Rejected"`]')
    #
    qa_ManageOrder_List_Item = (
        AppiumBy.IOS_PREDICATE,
        'type == "XCUIElementTypeStaticText" AND (name == "{name}" OR label == "{name}" OR value == "{name}")'
    )
    qa_ManageOrder_List_Cells = (
        AppiumBy.IOS_CLASS_CHAIN,
        '**/XCUIElementTypeCollectionView/XCUIElementTypeCell'
    )

class OrderSummaryPage(BasePage):
    """ Order Summary 페이지의 Locator를 정의 """
    #
    qa_OrderSummary_Back_Button = (AppiumBy.ID, 'chevronBackwardBold')
    #
    qa_OrderSummary_TitleName = (AppiumBy.ID, 'Order Summary')
    #
    qa_OrderSummary_CancelOrder_Button = (AppiumBy.ID, 'Cancel Order')
    #
    qa_OrderSummary_Info_Container = (
        AppiumBy.IOS_CLASS_CHAIN,
        '**/XCUIElementTypeScrollView[1]/XCUIElementTypeOther[1]'
    )
    #
    def get_info_value(self, label: str, *, timeout: int = 10) -> str:
        # 컨테이너 내 모든 StaticText를 순회하며 라벨과 그 다음 값을 매핑한다.
        container = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.qa_OrderSummary_Info_Container)
        )
        texts = container.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeStaticText")
        for idx, el in enumerate(texts):
            name_or_text = (el.get_attribute("name") or el.text or "").strip()
            if (name_or_text == label) or (label.lower() in name_or_text.lower()):
                if idx + 1 < len(texts):
                    next_el = texts[idx + 1]
                    return next_el.get_attribute("value") or next_el.text
        # 추가 fallback: 화면 전체에서 다시 탐색
        all_texts = self.driver.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeStaticText")
        for idx, el in enumerate(all_texts):
            name_or_text = (el.get_attribute("name") or el.text or "").strip()
            if (name_or_text == label) or (label.lower() in name_or_text.lower()):
                if idx + 1 < len(all_texts):
                    next_el = all_texts[idx + 1]
                    return next_el.get_attribute("value") or next_el.text
        raise Exception(f"라벨 '{label}'에 대한 값을 찾지 못했습니다.")
