from Pages.page_Base import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class StartScanPage(BasePage):
    """ Start Scan 페이지의 Locator를 정의 """
    
    # start scan page
    # qa_SelectPatient_Search = (AppiumBy.ID, 'qa_SelectPatient_Search')
    qa_SelectPatient_Search =(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeTextField[`name == "qa_SelectPatient_SearchBar"`]')
    #
    qa_SelectPatient_AddNewPatient_Button = (AppiumBy.ID, 'qa_SelectPatient_AddNewPatient_Button')


class SelectPatientPage(BasePage):
    """ Select Patient 페이지의 Locator를 정의 """
    #
    # qa_SelectPatient_Search = (AppiumBy.ID, 'qa_SelectPatient_Search')
    qa_SelectPatient_Search =(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeTextField[`name == "qa_SelectPatient_SearchBar"`]')
    #
    qa_SelectPatient_AddNewPatient_Button = (AppiumBy.ID, 'qa_SelectPatient_AddNewPatient_Button')
    #
    # 환자 리스트의 각 행에서 첫 번째 텍스트(환자 이름)를 가리킨다.
    qa_SelectPatient_PatientName_Cells = (
        AppiumBy.IOS_CLASS_CHAIN,
        '**/XCUIElementTypeTable/XCUIElementTypeCell/**/XCUIElementTypeStaticText[1]'
    )

class SelectWorkflowPage(BasePage):
    """ Select Workflow 페이지의 Locator를 정의 """
    #
    qa_SelectWorkflow_PreopMaxilla_Checkbox = (AppiumBy.ID, 'qa_SelectWorkflow_PreopMaxilla_Checkbox')
    #
    qa_SelectWorkflow_PreopMandible_Checkbox = (AppiumBy.ID, 'qa_SelectWorkflow_PreopMandible_Checkbox')
    #
    qa_SelectWorkflow_BasicProcedures = (AppiumBy.ID, 'Restoration')
    #
    qa_SelectWorkflow_ImplantRestoration = (AppiumBy.ID, 'Implant Scan')
    #
    qa_SelectWorkflow_Orthodontic = (AppiumBy.ID, 'Ortho Scan')
    #현재 스팩 제외
    qa_SelectWorkflow_Denture = (AppiumBy.ID, 'Denture')
    #
    qa_SelectWorkflow_Back_Button = (AppiumBy.ID, 'qa_SelectWorkflow_Back_Button')
    #
    qa_SelectWorkflow_Next_Button = (AppiumBy.ID, 'qa_SelectWorkflow_Next_Button')

class SelectTreatmentPage(BasePage):
    """ Select Treatment 페이지의 Locator를 정의 """
    #
    qa_SelectTreatment_Next_Button = (AppiumBy.ID, 'Next')
    #
    qa_SelectTreatment_Back_Button = (AppiumBy.ID, 'Back')
