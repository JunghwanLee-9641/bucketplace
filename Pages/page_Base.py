import sys, os, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import Config.config as config

import unittest
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.common.exceptions import NoSuchElementException


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

    @staticmethod
    def locator_by_accessibility_id(name: str) -> tuple:
        """
        주어진 문자열을 accessibility id로 사용하는 locator를 반환한다.
        """
        return (AppiumBy.ACCESSIBILITY_ID, name)

    def click_accessibility_ancestor(
        self,
        name: str,
        *,
        ancestor_type: str = "XCUIElementTypeCell",
        timeout: int = 10,
    ) -> bool:
        """
        accessibility id가 name인 요소의 상위 ancestor_type 요소를 찾아 클릭한다.
        """
        locator = self.locator_by_accessibility_id(name)
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            parent = element.find_element(
                AppiumBy.XPATH,
                f"./ancestor::{ancestor_type}[1]"
            )
            parent.click()
            return True
        except Exception as exc:
            print(f"⚠️ click_accessibility_ancestor 실패: {name}, {ancestor_type} ({exc})")
            return False

    def get_value_next_to_label(
        self,
        label_locator: tuple,
        *,
        timeout: int = 10,
    ) -> str:
        """
        주어진 라벨 locator를 기준으로 동일 부모 내 첫 번째 StaticText 값을 반환한다.
        """
        label_el = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(label_locator)
        )
        parent = label_el.find_element(AppiumBy.XPATH, "..")
        texts = parent.find_elements(AppiumBy.CLASS_NAME, "XCUIElementTypeStaticText")

        target_idx = None
        for idx, el in enumerate(texts):
            if el.id == label_el.id:
                target_idx = idx
                break
        if target_idx is None:
            label_name = label_el.get_attribute("name") or label_el.text
            for idx, el in enumerate(texts):
                if (el.get_attribute("name") or el.text) == label_name:
                    target_idx = idx
                    break

        if target_idx is not None and target_idx + 1 < len(texts):
            next_el = texts[target_idx + 1]
            return next_el.get_attribute("value") or next_el.text

        # 마지막 fallback: 형제 탐색
        value_el = label_el.find_element(
            AppiumBy.XPATH,
            "./following-sibling::XCUIElementTypeStaticText[1]"
        )
        return value_el.get_attribute("value") or value_el.text

    def click_text_ancestor(
        self,
        text: str,
        *,
        ancestor_type: str = "XCUIElementTypeCell",
        timeout: int = 10,
    ) -> bool:
        """
        화면에 표시된 StaticText(text/label/value) 요소의 상위 ancestor_type 요소를 찾아 클릭한다.
        """
        try:
            element = self.find_static_text(text, timeout=timeout)
            parent = element.find_element(
                AppiumBy.XPATH,
                f"./ancestor::{ancestor_type}[1]"
            )
            parent.click()
            return True
        except Exception as exc:
            print(f"⚠️ click_text_ancestor 실패: {text}, {ancestor_type} ({exc})")
            return False

    def click_cell_by_descendant_text(
        self,
        cell_locator: tuple,
        text: str,
        *,
        match_index: int = 0,
        timeout: int = 10,
    ) -> bool:
        """
        cell_locator로 찾은 각 Cell 내에서 특정 텍스트(name/label/value)를 가진 자손이 있는 셀을 클릭한다.
        동일 텍스트가 여러 셀에 있을 경우 match_index(0기반)번째를 클릭한다.
        """
        try:
            def cells_ready(drv):
                cells = drv.find_elements(*cell_locator)
                return cells if cells else False

            cells = WebDriverWait(self.driver, timeout).until(cells_ready)
            found_count = 0
            for cell in cells:
                try:
                    cell.find_element(
                        AppiumBy.IOS_PREDICATE,
                        f'name == "{text}" OR label == "{text}" OR value == "{text}"'
                    )
                    if found_count == match_index:
                        cell.click()
                        return True
                    found_count += 1
                except NoSuchElementException:
                    continue
            raise NoSuchElementException(f"텍스트 '{text}' 를 포함한 셀을 찾지 못했습니다.")
        except Exception as exc:
            print(f"⚠️ click_cell_by_descendant_text 실패: {text} ({exc})")
            return False
        

    def send_keys(self, locator: tuple, text: str) -> None:
        """
        특정 엘레멘트에 값을 입력합니다.
        Args:
            - locator (tuple): (By.ID, "value") 형태
            - text (str): 입력할 문자열
        """
        element = self.driver.find_element(*locator)
        element.clear()
        element.send_keys(text)
        self.driver.hide_keyboard()

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

    def select_element(
        self,
        locator: tuple | None = None,
        *,
        elements=None,
        index: int = 0,
        timeout: int = 10,
        sort_key=None,
    ) -> bool:
        """
        locator로 찾은 요소 리스트나 이미 구해둔 elements 리스트에서 원하는 항목을 탭한다.
        기본 index=0은 첫 번째 항목을 의미하며, sort_key를 넘기면 해당 기준으로 내림차순 정렬 후
        index번째 항목을 탭한다(예: 최신 항목 선택).
        """
        if index < 0:
            raise ValueError("index는 0 이상의 정수여야 합니다.")
        if locator is None and elements is None:
            raise ValueError("locator 또는 elements 중 하나는 반드시 전달해야 합니다.")

        try:
            if elements is None:
                def elements_ready(drv):
                    found = drv.find_elements(*locator)
                    return found if len(found) > index else False

                elements = WebDriverWait(self.driver, timeout).until(elements_ready)
            elif len(elements) <= index:
                raise IndexError("index가 요소 개수보다 큽니다.")

            if sort_key:
                elements = sorted(elements, key=sort_key, reverse=True)

            elements[index].click()
            return True
        except Exception as exc:
            print(f"⚠️ select_element 실패: {exc}")
            return False

    def is_element_enabled(self, locator: tuple, *, timeout: int = 10) -> bool:
        """
        locator에 해당하는 요소가 enable 상태인지 반환한다.
        """
        element = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        return element.is_enabled()

    def long_press(
        self,
        locator: tuple | None = None,
        *,
        element=None,
        duration: float = 2.0,
        timeout: int = 10,
    ) -> bool:
        """
        locator 또는 element로 지정한 대상 위에서 롱 탭 제스처를 수행한다.
        duration은 초 단위이며 기본값은 1초이다.
        """
        if element is None:
            if locator is None:
                raise ValueError("locator 또는 element 중 하나는 반드시 전달해야 합니다.")
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )

        try:
            actions = ActionChains(self.driver)
            finger = PointerInput(interaction.POINTER_TOUCH, "finger")
            actions.w3c_actions = ActionBuilder(self.driver, mouse=finger)
            actions.w3c_actions.pointer_action.move_to(element)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(duration)
            actions.w3c_actions.pointer_action.release()
            actions.perform()
            return True
        except Exception as exc:
            print(f"⚠️ long_press 실패: {exc}")
            return False
    
    def swipe_down_to_close(self, start_ratio: float = 0.4, end_ratio: float = 0.9, duration: float = 0.3) -> None:
        """
        화면 상단에서 하단으로 스와이프하여 모달/시트를 닫습니다.
        start_ratio와 end_ratio는 화면 높이를 0~1 범위로 본 상대 좌표입니다.
        """
        window_size = self.driver.get_window_size()
        start_x = window_size["width"] // 2
        start_y = int(window_size["height"] * start_ratio)
        end_y = int(window_size["height"] * end_ratio)

        # iOS drag 제스처
        self.driver.execute_script(
            "mobile: dragFromToForDuration",
            {
                "duration": duration,
                "fromX": start_x,
                "fromY": start_y,
                "toX": start_x,
                "toY": end_y,
            },
        )
