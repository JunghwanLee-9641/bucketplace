import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """ 
    모든 페이지에서 공통으로 사용할 메서드를 정의한다 
    """
    def __init__(self, driver):
        self.driver = driver  

    def click(self, locator: tuple, timeout: int = 10) -> bool:
        """
        locator로 입력한 엘레멘트를 클릭합니다.
        Args:
            - locator (tuple): (By.ID, "value") 형태
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            return True
        except Exception as exc:
            print(f"⚠️ click 실패: {locator} ({exc})")
            return False
    
    def send_keys(self, locator: tuple, text: str, timeout: int = 10) -> None:
        """
        특정 엘레멘트에 값을 입력합니다.
        Args:
            - locator (tuple): (By.ID, "value") 형태
            - text (str): 입력할 문자열
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass

    def send_keys_and_next(self, locator: tuple, text: str, timeout: int = 10) -> None:
        """
        텍스트 입력 후 키보드의 Next/Return 버튼을 누릅니다.
        Args:
            - locator (tuple): (By.ID, "value") 형태
            - text (str): 입력할 문자열
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)
        # iOS 키보드의 Next/Return 버튼 찾아서 클릭
        try:
            # 여러 가능한 버튼 이름 시도
            for button_name in ["Next", "next", "Return", "return", "완료", "Done"]:
                try:
                    button = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, button_name)
                    button.click()
                    return
                except:
                    continue
        except Exception as e:
            print(f"⚠️ 키보드 버튼을 찾을 수 없습니다: {e}")


    def get_input_value(self, locator: tuple) -> str:
        """입력창의 현재 문자열을 반환"""
        element = self.driver.find_element(*locator)
        # iOS 텍스트 필드는 value, 일반 label은 label/text 속성을 사용
        return element.get_attribute("value") or element.text


    def check_input_value(self, locator: tuple, expected: str, *, timeout: int = 5) -> bool:
        """입력창의 현재 문자열을 기대값과 비교하여 일치하면 True 반환"""
        WebDriverWait(self.driver, timeout).until(
            lambda drv: (drv.find_element(*locator).get_attribute("value") or "").strip() == expected
        )
        actual = self.get_input_value(locator)
        assert actual == expected, f"입력 값 불일치: 기대 '{expected}', 실제 '{actual}'"
        return True

    def check_element(self, by_locator, timeout: int = 10) -> bool:
        """ by_locator에 해당하는 Element가 나타날 때까지 10초 대기 후 Element가 검출되면 True를 반환 """
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(by_locator))
            return True
        except:
            return False

    def find_static_text(self, text: str, *, timeout: int = 10):
        """
        주어진 텍스트(name/label/value)가 표시된 StaticText 요소를 찾는다.
        """
        locator = (
            AppiumBy.IOS_CLASS_CHAIN,
            f'**/XCUIElementTypeStaticText[`name == "{text}" OR label == "{text}" OR value == "{text}"`][1]'
        )
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        return self.driver.find_element(*locator)

    def is_static_text_visible(self, text: str, *, timeout: int = 10) -> bool:
        """
        특정 텍스트가 화면에 표시됐는지 True/False 로 확인한다.
        """
        try:
            self.find_static_text(text, timeout=timeout)
            return True
        except Exception:
            return False

    def is_element_enabled(self, locator: tuple, *, timeout: int = 10) -> bool:
        """
        locator에 해당하는 요소가 enable 상태인지 반환한다.
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element.is_enabled()