from Pages.page_Base import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class CaseDetailPage(BasePage):
    """ CaseDetail 페이지의 Locator를 정의 """

    # Case Detail
    #
    qa_CaseDetail_Open_Button = (AppiumBy.ID, 'Open')
    #
    qa_CaseDetail_Order_Button = (AppiumBy.ID, 'Order')
    #
    # qa_CaseHistory_UploadRawData = (AppiumBy.ID, 'qa_CaseHistory_UploadRawData')
    qa_CaseHistory_UploadRawData = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "square.and.arrow.up"`]')
    #
    qa_CaseHistory_Copy = (AppiumBy.ID, 'Copy')
    #
    qa_CaseHistory_GetHelp = (AppiumBy.ID, 'Get Help')
    #
    qa_CaseHistory_Delete = (AppiumBy.ID, 'Delete')
    #
    qa_CaseDetail_Chevron_List = (
        AppiumBy.IOS_CLASS_CHAIN,
        '**/XCUIElementTypeImage[`name == "chevronDownBold"`]'
    )
