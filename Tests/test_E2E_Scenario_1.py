import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest, time
import Config.config as config


#################Test Case################
def test_E2E_Scenario1001(task_login,task_home):
    """
    
    """    
    #1~4 Step: 로그인
    task_login.check_Login_Page() #상태 확인
    task_login.input_Id(config.dev_clinics_ID)
    task_login.input_Password(config.dev_clinics_PW)
    task_login.click_Login_Button()
    task_home.check_Home_Page() #결과 확인



def test_E2E_Scenario1002(task_home,task_managepatient):
    """
    
    """    
    #5 Step: 환자 관리 페이지 이동
    task_home.click_ManagePatient_Button()
    #결과 확인
    task_managepatient.check_ManagePatient_Page()
    

def test_E2E_Scenario1003(task_managepatient):
    """
    
    """    
    #6 Step: 환자 생성 버튼 클릭
    task_managepatient.click_ManagePatient_AddNewPatient_Button()
    #결과 확인
    task_managepatient.check_AddNewPatient_Name()


def test_E2E_Scenario1004(task_managepatient):
    """
    
    """
    # 현재 시간 정보를 config에 저장
    config.year = time.strftime("%Y", time.localtime())
    config.month = time.strftime("%B", time.localtime())
    config.day = time.strftime("%d", time.localtime())
    config.hour = time.strftime("%H", time.localtime())
    config.minute = time.strftime("%M", time.localtime())
    config.second = time.strftime("%S", time.localtime())    
    
    #7 Step: Name 입력
    config.patientName = (
    f"{config.test_patientName}_{config.year}_{config.month}_{config.day}_{config.hour}_{config.minute}"
    )
    task_managepatient.input_AddNewPatient_Name(config.patientName)
    #결과 확인
    task_managepatient.check_input_AddNewPatient_Name(config.patientName)


def test_E2E_Scenario1005(task_managepatient):
    """
    
    """    
    #8~11 Step: Date 입력, 환자 생성
    #DatePicker 열기
    task_managepatient.click_AddNewPatient_DatePicker()
    task_managepatient.input_AddNewPatient_Day(config.day)
    # task_managepatient.click_ManagePatient_YearMonth_Button() DataPicker에서 Roller 선택으로 변경되어 불필요
    task_managepatient.input_AddNewPatient_Year(config.year)
    task_managepatient.input_AddNewPatient_Month(config.month)
    #DatePicker 닫기
    task_managepatient.click_AddNewPatient_DatePicker_Done()
    
    task_managepatient.click_AddNewPatient_Male_Button()
    task_managepatient.input_AddNewPatient_ID(config.patientName)
    task_managepatient.click_RegisterOnly_Button()

    #결과 확인
    task_managepatient.check_AddNewPatient_List(config.patientName)


def test_E2E_Scenario1006(task_managepatient,task_casedetail):
    """
    
    """    
    #12 Step: 환자 선택
    task_managepatient.click_ManagePatient_list(config.patientName)
    #결과 확인
    task_casedetail.check_CaseDetail_Page(config.patientName)


def test_E2E_Scenario1007(task_home,task_login):
    """
    
    """    
    #13~14 Step: Logout
    task_home.click_Account_Info()
    task_home.click_Logout_Button()
    #결과 확인
    task_login.check_Login_Page()