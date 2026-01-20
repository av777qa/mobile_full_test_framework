from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from core.devices import ANDROID, IOS

def get_android_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = ANDROID["device_name"]
    options.app = ANDROID["app_path"]
    options.allow_insecure = "adb_shell"
    options.auto_grant_permissions = True
    driver = webdriver.Remote("http://localhost:4723", options=options)
    return driver

def get_ios_driver():
    options = XCUITestOptions()
    options.platform_name = "iOS"
    options.automation_name = "XCUITest"
    options.device_name = IOS["device_name"]
    options.app = IOS["app_path"]
    options.allow_insecure = "adb_shell"
    options.auto_grant_permissions = True
    driver = webdriver.Remote("http://localhost:4723", options=options)
    return driver
