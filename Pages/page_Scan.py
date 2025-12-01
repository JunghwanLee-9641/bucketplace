from Pages.page_Base import BasePage
from appium.webdriver.common.appiumby import AppiumBy

class ScanPage(BasePage):
    """ Scan 페이지의 Locator를 정의 """

    # Scan Page
    #
    qa_Scan_DisclosureExpanded_Button = (AppiumBy.ID, 'disclosureExpanded')
    #
    qa_Scan_EditStage_Button = (AppiumBy.ID, 'editStage')
    #
    qa_Scan_AddStage_Button = (AppiumBy.ID, 'Add Stage')
    #
    qa_Scan_SaveEdit_Button = (AppiumBy.ID, 'Save Changes')
    #
    qa_Scan_CancelEdit_Button = (AppiumBy.ID, 'Cancel')
    #
    #Cancel
    #
    #Save
    #
    qa_Scan_CaseNameEdit_Button = (AppiumBy.ID, 'caseEdit')
    
    qa_Scan_CaseNameEdit_Input = (AppiumBy.ID, 'XCUIElementTypeTextField')
    #
    qa_Scan_StartScan_Button = (AppiumBy.ID, 'Start Scan')
    #
    qa_Scan_ScanStop_Button = (AppiumBy.ID, 'Scan Stop')
    #
    qa_Scan_ResumeScan_Button = (AppiumBy.ID, 'Resume Scan')
    #
    qa_Scan_NextStage_Button = (AppiumBy.ID, 'Next')
    #
    qa_Scan_Delete_Button = (AppiumBy.ID, 'Delete Data')

    #
    qa_Scan_MaxillaStage = (AppiumBy.ID, 'scanStageMaxillaSmall')
    #
    qa_Scan_MandibleStage = (AppiumBy.ID, 'scanStageMandibleSmall')
    #
    qa_Scan_FirstOcclusionStage = (AppiumBy.ID, 'scanStageOcclusionFirstSmall')
    #
    qa_Scan_SecondOcclusionStage = (AppiumBy.ID, 'scanStageOcclusionSecondSmall')
    #
    qa_Scan_OverviewStage = (AppiumBy.ID, 'scanStageReviewSmall')
    #
    qa_Scan_Undo_Button = (AppiumBy.ID, 'undo')
    #
    qa_Scan_Redo_Button = (AppiumBy.ID, 'redo')
    #
    qa_Scan_ToolBox_Button = (AppiumBy.ID, 'toolBox')
    #
    qa_Scan_ModelViewMode_Button = (AppiumBy.ID, 'statusSeeMoreTypePbr') #보여지는 U에 따라 변경 필요
    #
    qa_Scan_GridView_Button = (AppiumBy.ID, 'nameGridViewTypeOff') #보여지는 U에 따라 변경 필요
    #
    qa_Scan_Order_Button = (AppiumBy.ID, 'Order')
    #
    qa_Scan_Complete_Button = (AppiumBy.ID, 'Complete Scan')
    