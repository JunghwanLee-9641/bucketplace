from Pages.page_Base import BasePage
from appium.webdriver.common.appiumby import AppiumBy

""" OrderForm 페이지의 Locator를 정의 """
class OrderFormPage(BasePage):
    # OrderForm page

    #
    qa_OrderForm_TitleName = (AppiumBy.ID, 'Order Form')
    # qa_OrderForm_ShareWithLab_Toggle = (AppiumBy.ID, 'qa_OrderForm_ShareWithLab_Toggle')
    qa_OrderForm_ShareWithLab_Toggle = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeSwitch[`value == "0"`][1]')
    #
    # qa_OrderForm_CreateBridge_Button = (AppiumBy.ID, 'qa_OrderForm_CreateBridge_Button')
    qa_OrderForm_CreateBridge_Button = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "Create Bridge"`]')
    #
    # qa_OrderForm_Plus_Button = (AppiumBy.ID, 'qa_OrderForm_Plus_Button')
    qa_OrderForm_Plus_Button = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "plus"`][1]')
    #
    qa_OrderForm_Delete_Button = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "trashcan"`]')
    #
    qa_OrderForm_Selection_All_Check = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeSwitch[`name == "Square"`][1]')
    #
    qa_OrderForm_SubmitOrder_Button = (AppiumBy.ID, 'Submit Order')
    #
    qa_OrderForm_LabName = (
        AppiumBy.IOS_CLASS_CHAIN,
        '**/XCUIElementTypeButton[`name == "{name}"`]'
    )
    #
    qa_OrderForm_Type_List = (
        AppiumBy.IOS_CLASS_CHAIN,
        '**/XCUIElementTypeButton[`name == "Type"`]'
    )
    #
    qa_OrderForm_Method_List = (
        AppiumBy.IOS_CLASS_CHAIN,
        '**/XCUIElementTypeButton[`name == "Method"`]'
    )
    #
    qa_OrderForm_Material_List = (
        AppiumBy.IOS_CLASS_CHAIN,
        '**/XCUIElementTypeButton[`name == "Material"`]'
    )
    qa_OrderForm_Material_Options = (
        AppiumBy.IOS_CLASS_CHAIN,
        '**/XCUIElementTypeCollectionView/XCUIElementTypeCell'
    )
