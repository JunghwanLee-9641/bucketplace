from Pages.page_Base import BasePage
from appium.webdriver.common.appiumby import AppiumBy

""" Common의 Locator를 정의 """
class CommonACID(BasePage):
    #공용으로 쓸 수 있는 Accessibility ID

    #
    qa_Common_Back_Button = (AppiumBy.ID, 'qa_Common_Back_Button')
    #
    qa_Common_Confirm_Button = (AppiumBy.ID, 'Confirm')
    #
    qa_Common_Shoppingbasket_Button = (AppiumBy.ID, 'qa_Common_Shoppingbasket_Button')
    #
    qa_Common_Allow_Button = (AppiumBy.ID, 'Allow') #apple system의 allow button
    #
    qa_Common_NotTrack_Button = (AppiumBy.ID, 'Ask App Not to Track') #apple system의 don't allow button
    #
    qa_Common_Close_Button = (AppiumBy.ID, 'qa_Common_Close_Button')
    #
    qa_Common_DoNotShowAgain_Button = (AppiumBy.ID, 'qa_Common_DoNotShowAgain_Button')
    