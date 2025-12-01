import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest, time

import Config.config as config

#################Test Case################
def test_Home0001(task_home, task_common):
    """
    테스트를 위한 임시 작성
    """    
    #
    task_home.check_Home_Page()
    task_home.click_ScanStart_Button()
    time.sleep(1)
    task_common.click_Close_Button()

def test_Home0002(task_home):
    """
    테스트를 위한 임시 작성
    """    
    #
    task_home.check_Home_Page()
    task_home.click_ManagePatient_Button()
    time.sleep(1)
    task_home.click_Home_Button()

def test_Home0003(task_home):
    """
    테스트를 위한 임시 작성
    """    
    #
    task_home.check_Home_Page()
    task_home.click_ViewOrder_Button()
    time.sleep(1)
    task_home.click_Home_Button()


def test_Home0004(task_home):
    """
    테스트를 위한 임시 작성
    """    
    #로그아웃
    task_home.check_Home_Page()
    task_home.click_Account_Info()
    task_home.click_Logout_Button()
