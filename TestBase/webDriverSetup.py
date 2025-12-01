import os
import Config.config as config
from TestBase.DeviceSetup import DeviceSetup


class WebDriverSetup:
    """Thin wrapper to return an Appium driver using DeviceSetup."""

    def __init__(self, device_name=None, port=None, *, is_simulator=False, udid=None, os_version=None):
        self.device_name = (
            device_name
            or os.environ.get("DEVICE_NAME")
            or config.REAL_DEVICE_CAPABILITIES.get("appium:deviceName")
            or "iOS Device"
        )
        self.port = int(port or os.environ.get("PORT", config.APPIUM_BASE_PORT))
        self.is_simulator = is_simulator
        self.udid = udid or os.environ.get("UDID")
        self.os_version = os_version or os.environ.get("PLATFORM_VERSION")

    def get_driver(self):
        setup = DeviceSetup(
            self.device_name,
            self.port,
            udid=self.udid,
            is_simulator=self.is_simulator,
            os_version=self.os_version,
        )
        return setup.driver


if __name__ == "__main__":
    # Quick manual check (will require a connected real device and running Appium)
    driver = WebDriverSetup().get_driver()
    print("Driver created:", driver)
    driver.quit()
