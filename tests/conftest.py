import pytest
from core.appium_driver import get_android_driver, get_ios_driver

@pytest.fixture(scope="function")
def android_driver():
    driver = get_android_driver()
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def ios_driver():
    driver = get_ios_driver()
    yield driver
    driver.quit()
