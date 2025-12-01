import pytest, logging
import os
from TestBase.DeviceSetup import DeviceSetup
import Config.config as config
from Tasks.task_Login import Task_Login
from TestBase.webDriverSetup import WebDriverSetup
from Tasks.task_Login import Task_Login
from Tasks.task_Home import Task_Home
from Tasks.task_Common import Task_Common
from Tasks.task_ManagePatient import Task_ManagePatient
from Tasks.task_CaseDetail import Task_CaseDetail
from Tasks.task_StartScan import Task_StartScan
from Tasks.task_Scan import Task_Scan
from Tasks.task_CaseDetail import Task_CaseDetail
from Tasks.task_OrderForm import Task_OrderForm
from Tasks.task_ManageOrder import Task_ManageOrder
from pytest_html import extras
# Accumulate setup-phase logs to display in summary
setup_extras = []


# Filter pytest-HTML extra items to only include stderr and log messages during test execution
@pytest.hookimpl(optionalhook=True)
def pytest_html_results_extra(report, extra):
    # Capture setup-phase stderr/ansi items for summary, then clear
    if report.when == "setup":
        for item in extra:
            if getattr(item, "format", None) in ("stderr", "ansi"):
                setup_extras.append(item)
        extra.clear()
        return

    # For call phase, keep only stderr/ansi items under each test
    if report.when == "call":
        extra[:] = [
            item for item in extra
            if getattr(item, "format", None) in ("stderr", "ansi")
        ]
    else:
        extra.clear()

def pytest_addoption(parser):
    parser.addoption("--device", action="store", default=None, help="Device under test")
    parser.addoption("--port", action="store", default=None, help="Appium server port")
    

class CompositeTasks:
    def __init__(self, driver):
        self.login = Task_Login(driver)

def get_device_info(pytest_config):
    device_name = pytest_config.getoption("--device")
    port = pytest_config.getoption("--port")
    if device_name is None:
        device_name = os.environ.get('DEVICE_NAME', config.iPad_Pro_M4_13_16G)
    if port is None:
        port = os.environ.get('PORT', 4723)
    return device_name, int(port)

@pytest.fixture(scope="session")
def set_driver(request):
    device_name, port = get_device_info(request.config)
    device_setup = DeviceSetup(device_name, port)
    device_setup.driver = device_setup.start_appium_with_simulator(device_name)
    driver = device_setup.driver
    yield driver
    # driver.quit()
    # DeviceSetup.stop_simulator(device_name)
    # DeviceSetup.stop_appium(port)

@pytest.fixture(scope="session")
def Tasks(set_driver):
    return CompositeTasks(set_driver)

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

@pytest.hookimpl(optionalhook=True)
def pytest_html_results_summary(prefix, summary, postfix):
    if setup_extras:
        prefix.append(extras.html("<h2>Setup Logs</h2>"))
        for item in setup_extras:
            # Render each captured log block in a <pre> for readability
            prefix.append(extras.html(f"<pre>{item.content}</pre>"))

@pytest.fixture(scope='session')
def driver():
    drv = WebDriverSetup().get_driver()
    try:
        yield drv
    finally:
        try:
            drv.quit()
        except Exception:
            pass

@pytest.fixture(scope='session')
def task_login(driver):
    return Task_Login(driver)

@pytest.fixture(scope='session')
def task_home(driver):
    return Task_Home(driver)

@pytest.fixture(scope='session')
def task_common(driver):
    return Task_Common(driver)

@pytest.fixture(scope='session')
def task_managepatient(driver):
    return Task_ManagePatient(driver)

@pytest.fixture(scope='session')
def task_casedetail(driver):
    return Task_CaseDetail(driver)

@pytest.fixture(scope='session')
def task_startscan(driver):
    return Task_StartScan(driver)

@pytest.fixture(scope='session')
def task_scan(driver):
    return Task_Scan(driver)

@pytest.fixture(scope='session')
def task_casedetail(driver):
    return Task_CaseDetail(driver)

@pytest.fixture(scope='session')
def task_orderform(driver):
    return Task_OrderForm(driver)

@pytest.fixture(scope='session')
def task_manageorder(driver):
    return Task_ManageOrder(driver)
