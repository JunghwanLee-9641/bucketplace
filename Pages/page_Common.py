from Pages.page_Base import BasePage
from appium.webdriver.common.appiumby import AppiumBy

""" Common의 Locator를 정의 """
class CommonACID(BasePage):
    #공용으로 쓸 수 있는 Accessibility ID

    #
    qa_Common_Close_Button = (AppiumBy.ID, 'qa_Common_Close_Button')
    #
    qa_Common_Back_Button = (AppiumBy.ID, 'qa_Common_Back_Button')
    #
    qa_Common_SidebarClose_Button = (AppiumBy.ID, 'qa_Common_SidebarClose_Button')
    
    # 아직 사용 되는 곳이 없음.
    # qa_Common_SidebarBack_Button = (AppiumBy.ID, 'qa_Common_SidebarBack_Button')
    #
    qa_Common_Cancel_Button = (AppiumBy.ID, 'Cancel')
    #
    qa_Common_Confirm_Button = (AppiumBy.ID, 'Confirm')
    #
    qa_Common_Delete_Button = (AppiumBy.ID, 'Delete')