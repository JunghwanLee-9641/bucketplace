from Pages.page_Base import BasePage
from appium.webdriver.common.appiumby import AppiumBy

""" Home 페이지의 Locator를 정의 """
class HomePage(BasePage):
    # home page

    #
    # qa_Home_Home_Button = (AppiumBy.ID, 'qa_Home_Home_Button')
    qa_Home_Home_Button = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeImage[`name == "qa_Home_Home_Button"`]')
    #
    qa_Home_ScannerStatus_Button = (AppiumBy.ID, 'qa_Home_ScannerStatus_Button')
    #
    qa_Home_AccountInfo_Button = (AppiumBy.ID, 'qa_Home_AccountInfo_Button')
    #
    qa_Home_Notification_Button = (AppiumBy.ID, 'qa_Home_Notification_Button')
    #
    qa_Home_Setting_Button = (AppiumBy.ID, 'qa_Home_Setting_Button')
    #
    qa_Home_SetUpNow_Button = (AppiumBy.ID, 'qa_Home_SetUpNow_Button')
    #
    qa_Home_Search = (AppiumBy.ID, 'qa_Home_Search')
    #
    qa_Home_StartScan_Button = (AppiumBy.ID, 'qa_Home_StartScan_Button')
    #
    qa_Home_ManagePatient_Button = (AppiumBy.ID, 'qa_Home_ManagePatient_Button')
    #
    qa_Home_ManageOrder_Button = (AppiumBy.ID, 'qa_Home_ViewOrder_Button')
    #임시
    GuideMe_Button = str("Let’s Get Started!")
    qa_Home_GuideMe_Button = (AppiumBy.ID, GuideMe_Button)

class AccountInfoPage(BasePage):
    # AccountInfo page
    
    #
    qa_Home_AccountInfo_Logout = (AppiumBy.ID, 'qa_Home_AccountInfo_Logout')
    #
    qa_Home_AccountInfo_ManageAccount = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "qa_Home_AccountInfo_Button"`]')
    #

class SaveExitPage(BasePage):
    # SaveExit page

    #
    qa_Home_SaveAndExit = (AppiumBy.ID, 'Save and Exit')
    #
    qa_Home_ExitWithoutSaving_Button = (AppiumBy.ID, 'Exit without Saving')
    #
    qa_Home_Cancel = (AppiumBy.ID, 'Cancel')