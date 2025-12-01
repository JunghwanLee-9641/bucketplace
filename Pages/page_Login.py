from Pages.page_Base import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class LoginPage(BasePage):
    """ Login 페이지의 Locator를 정의 """
    
    # login page

    #
    qa_Login_EmailAddress = (AppiumBy.ID, 'qa_Login_EmailAddress')
    #
    qa_Login_Password = (AppiumBy.ID, 'qa_Login_Password')
    #
    qa_Login_Password_ShowHide = (AppiumBy.ID, 'qa_Login_Password_ShowHide')
    #
    qa_Login_KeepMeLoggedIn_Check = (AppiumBy.ID, 'qa_Login_KeepMeLoggedIn_Check')
    #
    qa_Login_KeepMeLoggedIn = (AppiumBy.ID, 'qa_Login_KeepMeLoggedIn')
    #
    qa_Login_Login_Button = (AppiumBy.ID, 'qa_Login_Login_Button')
    #
    qa_Login_ForgotPassword = (AppiumBy.ID, 'qa_Login_ForgotPassword')
    #
    qa_Login_CreateNewAccount = (AppiumBy.ID, 'qa_Login_CreateNewAccount')