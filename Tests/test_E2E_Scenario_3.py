import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest, time
import Config.config as config


#################Test Case################
def test_E2E_Scenario3001(task_login,task_home):
    """
    
    """    
    #1~4 Step: 로그인
    task_login.check_Login_Page() #상태 확인
    task_login.input_Id(config.dev_clinics_ID)
    task_login.input_Password(config.dev_clinics_PW)
    task_login.click_Login_Button()
    task_home.check_Home_Page() #결과 확인


def test_E2E_Scenario3002(task_home, task_managepatient):
    """
    
    """    
    #5 Step: 환자 관리 페이지 이동
    task_home.click_ManagePatient_Button()
    #결과 확인
    task_managepatient.check_ManagePatient_Page()
    
    
def test_E2E_Scenario3003(task_casedetail, task_managepatient):
    """
    
    """    
    #6 Step: 환자 검색 후 선택
    task_managepatient.input_ManagePatient_Name(config.orderpatientName)
    task_managepatient.click_ManagePatient_list(config.orderpatientName)
    #결과 확인
    task_casedetail.check_CaseDetail_Page(config.orderpatientName)


def test_E2E_Scenario3004(task_casedetail):
    """
    
    """    
    #7 Step: Case Copy
    task_casedetail.longclick_CaseDetail_Case(config.caseName)
    task_casedetail.click_CaseDetail_Copy()
    #결과 확인
    task_casedetail.check_CaseDetail_CopyCase(config.caseName_Clone)


def test_E2E_Scenario3005(task_casedetail,task_orderform):
    """
    
    """
    # 현재 시간 정보를 config에 저장
    config.year = time.strftime("%Y", time.localtime())
    config.month = time.strftime("%B", time.localtime())
    config.day = time.strftime("%d", time.localtime())
    config.hour = time.strftime("%H", time.localtime())
    config.minute = time.strftime("%M", time.localtime())
    create_caseName = f"{config.year}_{config.month}_{config.day}_{config.hour}_{config.minute}"
    
    #8~9 Step: Copy Case 선택 후 order 버튼 클릭
    task_casedetail.click_CaseDetail_CaseList(index=0)
    task_casedetail.click_CaseDetail_Order_Button()
    
    """
    task_casedetail.click_CaseDetail_Open_Button()
    task_scan.check_Scan_Page()
    task_scan.input_Scan_CaseNameEdit(create_caseName)
    task_home.click_Home_Button()
    task_home.click_Home_SaveAndExit()
    task_home.check_Home_Page()
    """
    #결과 확인
    task_orderform.check_OrderForm_Page()

def test_E2E_Scenario3006(task_orderform, task_manageorder):
    """
    
    """    
    #10~11 Step: Submit Order
    task_orderform.check_OrderForm_LabName(config.labName)
    task_orderform.click_OrderForm_Select_All_Check()
    task_orderform.click_OrderForm_Type(index=0) #첫번째 선택
    task_orderform.select_OrderForm_Type_By_Name('Crown') #Crown 선택
    task_orderform.click_OrderForm_Method(index=0) #첫번째 선택
    task_orderform.select_OrderForm_Method_By_Name('Anatomic') #Anatomic 선택
    task_orderform.click_OrderForm_Material(index=0) #첫번째 선택
    task_orderform.select_OrderForm_Material_By_Name('Gold') #Gold 선택
    task_orderform.check_OrderForm_SubmitOrder_Button_Enabled()
    task_orderform.click_OrderForm_SubmitOrder_Button()
    #결과 확인
    task_manageorder.check_OrderSummary_Page()
    config.order_summary_info = task_manageorder.get_OrderSummary_Info()


def test_E2E_Scenario3007(task_home, task_manageorder):
    """
    
    """    
    #12~13 Step: Manage Order 진입
    task_home.click_Home_Button()
    task_home.check_Home_Page()
    task_home.click_ManageOrder_Button()
    #결과 확인
    task_manageorder.check_ManageOrder_Page()


def test_E2E_Scenario3008(task_manageorder):
    """
    
    """    
    #14~15 Step: Order 확인
    task_manageorder.click_ManageOrder_List() #order patient 첫번째 항목 선택
    #결과 확인
    task_manageorder.check_OrderSummary_Info(config.order_summary_info)


def test_E2E_Scenario3009(task_manageorder, task_common):
    """
    
    """    
    #16 Step: Cancel Order 
    task_manageorder.click_OrderSummary_CancelOrder_Button()
    task_common.click_Common_Confirm_Button()
    #결과 확인
    task_manageorder.check_ManageOrder_Page()


def test_E2E_Scenario3010(task_common, task_managepatient, task_home, task_casedetail):
    """
    
    """    
    #17~18 Step: Delete Case
    task_home.click_Home_Button()
    task_home.check_Home_Page()
    task_home.click_ManagePatient_Button()
    task_managepatient.input_ManagePatient_Name(config.orderpatientName)
    task_managepatient.click_ManagePatient_list(config.orderpatientName)
    task_casedetail.longclick_CaseDetail_Case(config.caseName_Clone)
    task_casedetail.click_CaseDetail_Delete()
    task_common.click_Common_Delete_Button()
    #결과 확인
    task_casedetail.check_CaseDetail_CopyCase_NotExists(config.caseName_Clone)


def test_E2E_Scenario3011(task_home, task_login):
    """
    
    """    
    #19~20 Step: Logout
    task_home.click_Account_Info()
    task_home.click_Logout_Button()
    #결과 확인
    task_login.check_Login_Page()
