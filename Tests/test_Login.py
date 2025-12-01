import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest, time

import Config.config as config

VALID_ID = config.stage_clinics_ID
VALID_PW = config.stage_clinics_PW
INVALID_PW = "wrong_password!"

def test_login_success_shows_home_core_widgets(task_login, task_home):
    task_login.login_with_credentials(VALID_ID, VALID_PW)
    task_login.assert_login_success()
    task_home.assert_core_widgets_visible()

def test_login_fail_wrong_password_stays_on_login(task_login):
    task_login.login_with_credentials(VALID_ID, INVALID_PW)
    task_login.assert_login_failure_stays_on_login()
