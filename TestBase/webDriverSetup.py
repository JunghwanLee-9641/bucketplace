import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Config.config as config
from TestBase.DeviceSetup import DeviceSetup

class WebDriverSetup:
    def __init__(self, device_name=None, port=None, *, is_simulator=None, udid=None, os_version=None):
        self.device_name = device_name or os.environ.get("DEVICE_NAME")
        self.port = port or os.environ.get("PORT")
        if not self.device_name:
            raise ValueError("시뮬레이터 이름이 지정되지 않았습니다. DEVICE_NAME 환경 변수를 설정하거나 device_name을 전달하세요.")
        if not self.port:
            raise ValueError("Appium 포트가 지정되지 않았습니다.")

        # 물리/시뮬레이터 구분은 DeviceSetup.run_device_tests가 내려주는 env 값을 우선 사용
        if is_simulator is None:
            env_flag = os.environ.get("DEVICE_IS_SIMULATOR", "1").lower()
            is_simulator = env_flag not in ("0", "false", "no")
        self.is_simulator = is_simulator
        self.udid = udid or os.environ.get("UDID")
        self.os_version = os_version or os.environ.get("PLATFORM_VERSION")
        
    def get_driver(self):
        # DeviceSetup을 통해 드라이버를 초기화하고 반환합니다.
        device_setup = DeviceSetup(
            self.device_name,
            self.port,
            udid=self.udid,
            is_simulator=self.is_simulator,
            os_version=self.os_version
        )
        return device_setup.driver

# 예시 실행 코드 (직접 실행 시 드라이버가 생성되는지 확인)
if __name__ == "__main__":
    web_driver_setup = WebDriverSetup()
    driver = web_driver_setup.get_driver()
    print("드라이버 생성 완료:", driver)
    # 테스트 종료 후 드라이버 종료
    driver.quit()
