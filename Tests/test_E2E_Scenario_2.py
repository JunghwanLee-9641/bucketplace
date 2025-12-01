import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest, time
import Config.config as config


#################Test Case################
def test_E2E_Scenario2001(task_login,task_home):
    """
    
    """    
    #1~4 Step: 로그인
    task_login.check_Login_Page() #상태 확인
    task_login.input_Id(config.dev_clinics_ID)
    task_login.input_Password(config.dev_clinics_PW)
    task_login.click_Login_Button()
    task_home.check_Home_Page() #결과 확인


def test_E2E_Scenario2002(task_home, task_startscan):
    """
    
    """    
    #5 Step: 환자 관리 페이지 이동
    task_home.click_ScanStart_Button() #Treatment Scan 버튼 클릭
    #결과 확인
    task_startscan.check_SelectPatient_Page()
    
    
def test_E2E_Scenario2003(task_startscan):
    """
    
    """    
    #6 Step: 환자 선택
    task_startscan.click_SelectPatient_list() #제일 처음의 환자 선택
    #결과 확인
    task_startscan.check_SelectWorkflow_Page()


def test_E2E_Scenario2004(task_startscan):
    """
    
    """
    #7 Step: Restoration 선택
    task_startscan.click_SelectWorkflow_Restoration()
    #결과 확인
    task_startscan.check_SelectWorkflow_Next_Button_Enabled()


def test_E2E_Scenario2005(task_startscan):
    """
    
    """
    #8 Step: Next 버튼 클릭
    task_startscan.click_SelectWorkflow_Next_Button()
    #결과 확인
    task_startscan.check_SelectTreatment_Page()


def test_E2E_Scenario2006(task_startscan):
    """
    
    """
    #9 Step: 모든 Teeth 선택
    task_startscan.click_SelectTreatment_SelectTeeth_All()
    #결과 확인
    task_startscan.check_SelectTreatment_Next_Button_Enabled()


def test_E2E_Scenario2007(task_startscan, task_scan):
    """
    
    """
    #10 Step: Next 버튼 클릭
    task_startscan.click_SelectTreatment_Next_Button()
    #결과 확인
    task_scan.check_Scan_Page()


def test_E2E_Scenario2008(task_scan):
    """
    
    """
    #11~14 Step: Next 버튼 클릭
    task_scan.click_Scan_Next_Button() # Maxilla -> Mandible
    task_scan.click_Scan_Next_Button() # Mandible -> First Occlusion
    task_scan.click_Scan_Next_Button() # First Occlusion -> Secound Occlusion
    task_scan.click_Scan_Next_Button() # Secound Occlusion -> Review Scan
    #결과 확인
    task_scan.check_Scan_Order_Button_Disabled()
    task_scan.check_Scan_Complete_Button_Disabled()

def test_E2E_Scenario2009(task_home):
    """
    
    """
    #15 Step: Home 버튼 클릭
    task_home.click_Home_Button()
    #결과 확인
    task_home.check_Home_Page()

def test_E2E_Scenario2010(task_home, task_login):
    """
    
    """    
    #13~14 Step: Logout
    task_home.click_Account_Info()
    task_home.click_Logout_Button()
    #결과 확인
    task_login.check_Login_Page()