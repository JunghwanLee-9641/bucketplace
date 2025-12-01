from Pages.page_Base import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class ManagePatientPage(BasePage):
    """ ManagePatient 페이지의 Locator를 정의 """

    # Manage Patient
    #
    # qa_ManagePatient_Search = (AppiumBy.ID, 'qa_ManagePatient_Search')
    qa_ManagePatient_Search = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeTextField[`name == "qa_ManagePatient_Search"`]')
    #
    qa_ManagePatient_PatientName = (AppiumBy.ID, 'Patient Name')
    #
    qa_ManagePatient_DateOfBirth = (AppiumBy.ID, 'Date of Birth')
    #
    qa_ManagePatient_PatientID = (AppiumBy.ID, 'Patient ID')
    #
    qa_ManagePatient_AddNewPatient_Button = (AppiumBy.ID, 'qa_ManagePatient_AddNewPatient_Button')

class AddPatientPage(BasePage):
    """ Add a New Patient 페이지의 Locator를 정의 """
    
    # Add a New Patient
    #
    qa_AddNewPatient_Name  = (AppiumBy.ID, 'qa_AddNewPatient_Name')
    #
    qa_AddNewPatient_PatientID = (AppiumBy.ID, 'qa_AddNewPatient_PatientID')
    #
    qa_AddNewPatient_RegisterOnly_Button = (AppiumBy.ID, 'qa_AddNewPatient_RegisterOnly_Button')
    #
    qa_AddNewPatient_RegisterStartScan_Button = (AppiumBy.ID, 'qa_AddNewPatient_RegisterStartScan_Button')
    #이이디가 별도로 부여 되지 않아 임시로 초기값을 지정
    qa_AddNewPatient_DatePicker = (AppiumBy.ID, 'MM/DD/YYYY')
    #DatePicker를 닫기위해 외부의 스트링 터치
    # qa_AddNewPatient_DatePicker_Done = (AppiumBy.ID, 'Date of Birth*') 
    qa_AddNewPatient_DatePicker_Done =(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeWindow[3]/XCUIElementTypeOther')

    #아이디가 별도로 부여 되지 않아 임시로 초기값을 지정
    qa_AddNewPatient_YearMonth = (AppiumBy.ID, 'January 1970')
    #
    # qa_AddNewPatient_Year = (AppiumBy.ID, '1970')
    qa_AddNewPatient_Year = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypePickerWheel[`value == "1970"`]')
    #
    # qa_AddNewPatient_Month = (AppiumBy.ID, 'January')
    qa_AddNewPatient_Month = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypePickerWheel[`value == "January"`]')
    #
    qa_AddNewPatient_Day = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypePickerWheel[`value == "1"`]')

    qa_AddNewPatient_Female = (AppiumBy.ID, 'Female')
    #
    qa_AddNewPatient_Male = (AppiumBy.ID, 'Male')