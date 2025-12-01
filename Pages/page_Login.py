from Pages.page_Base import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class LoginPage(BasePage):
    """ Login 페이지의 Locator를 정의 """
    
    # login page
    qa_Login_Lookaround_Button = (AppiumBy.ID, 'qa_Login_Lookaround_Button')
    #
    qa_Login_KakaoLogin_Button = (AppiumBy.ID, 'qa_Login_KakaoLogin_Button')
    #
    qa_Login_AppleLogin_Button = (AppiumBy.ID, 'qa_Login_AppleLogin_Button')
    #
    qa_Login_NaverLogin_Button = (AppiumBy.ID, 'qa_Login_NaverLogin_Button')
    #
    qa_Login_FacebookLogin_Button = (AppiumBy.ID, 'qa_Login_FacebookLogin_Button')
    #ID 부여가 정상적으로 되어 있지 않으면 IOS_CLASS_CHAIN 값을 사용하고 이후 ID가 정상적으로 부여 된다면 수정
    # qa_Login_EmailLogin_Button = (AppiumBy.ID, 'qa_Login_EmailLogin_Button')
    qa_Login_EmailLogin_Button = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeImage[`name == "qa_Login_EmailLogin_Button"`]')
    #
    qa_Login_CreateNewAccount_Button = (AppiumBy.ID, 'qa_Login_CreateNewAccount_Button')
    #
    qa_Login_EmailAddress = (AppiumBy.ID, 'qa_Login_EmailAddress')
    #
    qa_Login_Password = (AppiumBy.ID, 'qa_Login_Password')
    #
    qa_Login_KeepMeLoggedIn_Check = (AppiumBy.ID, 'qa_Login_KeepMeLoggedIn_Check')
    #
    qa_Login_KeepMeLoggedIn = (AppiumBy.ID, 'qa_Login_KeepMeLoggedIn')
    #
    qa_Login_Complete_Button = (AppiumBy.ID, 'qa_Login_Complete_Button')
    #
    qa_Login_ForgotPassword = (AppiumBy.ID, 'qa_Login_ForgotPassword')
    #
    qa_Login_CreateNewAccount = (AppiumBy.ID, 'qa_Login_CreateNewAccount')
    #
    qa_Login_Help_Button = (AppiumBy.ID, 'qa_Login_Help_Button')

class LoginPage_MessageBox(BasePage):
    """ Login 페이지의 출력되는 메시지를 정의"""
    #
    qa_Login_RequiredFieldMessage_Text = (AppiumBy.ID, '꼭 입력해야 해요.')
    #
    qa_Login_InvalidEmailFormatMessage_Text = (AppiumBy.ID, '이메일 형식에 맞는지 확인해주세요.')
    #
    qa_Login_UnregisteredEmailMessage_Text = (AppiumBy.ID, '가입되지 않은 이메일이에요.')
    #
    qa_Login_IncorrectPasswordMessage_Text = (AppiumBy.ID, '비밀번호가 올바르지 않습니다.')
    #
    qa_Login_LoginAttemptLimitMessage_Text = (AppiumBy.ID, '10번 실패하면 10분간 로그인이 제한돼요.')