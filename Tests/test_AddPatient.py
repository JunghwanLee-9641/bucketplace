import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest, time

import Config.config as config

id = config.stage_addPatient_clinics_ID
pw = config.stage_addPatient_clinics_PW


#################Test Case################
def test_ManagePatient0001(task_login,task_home):
    """
    테스트를 위한 임시 작성
    """    
    #ID 입력
    task_login.input_Id(id)
    #PW 입력
    task_login.input_Password(pw)
    task_login.click_Login_Button()
    task_login.login_check()
    #결과 확인
    task_home.check_Home_Page()

def test_ManagePatient0002(task_home,task_managepatient):
    """
    테스트를 위한 임시 작성
    """
    task_home.click_ManagePatient_Button()
    #결과 확인
    task_managepatient.check_ManagePatient_Page()
    

def test_ManagePatient0003(task_managepatient):
    """
    테스트를 위한 임시 작성
    """
    for i in range(1, 2):
        # Add New Patient 버튼 클릭
        task_managepatient.click_ManagePatient_AddNewPatient_Button()
        task_managepatient.check_AddPatient_Page()

        # 환자 이름에 타임스탬프와 인덱스를 추가
        timestep = time.strftime("%y%m%d%H%M%S", time.localtime())
        patientName = f"환자_{timestep}_{i}"

        # 이름 입력 및 등록 버튼 클릭
        task_managepatient.input_AddNewPatient_Name(patientName)
        task_managepatient.click_AddNewPatient_RegisterOnly_Button()
        print(str(i) + '/200 생성 완료')