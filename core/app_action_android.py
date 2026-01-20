from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

class AppActionsAndroid:
    def __init__(self, driver):
        self.driver = driver
        self.bundle = driver.capabilities.get("appPackage")

    def check_webview(self, timeout: int = 20) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element(AppiumBy.CLASS_NAME, "android.webkit.WebView")
            )
            return True
        except TimeoutException:
            return False

    def background_app(self):
        self.driver.background_app(-1)

    def kill_app(self):
        self.driver.terminate_app(self.bundle)

    def launch_app(self):
        self.driver.activate_app(self.bundle)
