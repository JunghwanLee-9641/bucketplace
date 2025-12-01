from Pages.page_Base import BasePage
from appium.webdriver.common.appiumby import AppiumBy

""" Main 페이지의 Locator를 정의 """
class MainPage(BasePage):
    # home page

    #
    qa_Main_Menu_Button = (AppiumBy.ID, 'qa_Home_Menu_Button')
    #
    qa_Main_Notification_Button = (AppiumBy.ID, 'qa_Home_Notification_Button')
    #
    qa_Main_Scrapbook_Button = (AppiumBy.ID, 'qa_Home_Scrapbook_Button')
    #
    # qa_Main_Home_Button = (AppiumBy.ID, 'qa_Main_Home_Button')
    qa_Main_Home_Button = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeImage[`name == "qa_Main_Home_Button"`]')
    #
    qa_Main_Community_Button = (AppiumBy.ID, 'qa_Home_Community_Button')
    #
    qa_Main_Shopping_Button = (AppiumBy.ID, 'qa_Home_Shoppingbasket_Button')
    #
    qa_Main_Interior_Button = (AppiumBy.ID, 'qa_Home_Interior_Button')
    #
    qa_Main_Mypage_Button = (AppiumBy.ID, 'qa_Home_Mypage_Button')
    #
    qa_Home_ScannerStatus_Button = (AppiumBy.ID, 'qa_Home_ScannerStatus_Button')

class MainPage_MessageBox(BasePage):
    """ Main 페이지의 출력되는 메시지를 정의"""
    #
    qa_Main_EventPopup_Text = (AppiumBy.ID, '초특가 오늘 시작')
    