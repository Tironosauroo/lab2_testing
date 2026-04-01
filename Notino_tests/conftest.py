import os
import winreg
import pytest
import undetected_chromedriver as uc

def get_chrome_major_version():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
        version, _ = winreg.QueryValueEx(key, "version")
        return int(version.split('.')[0])
    except Exception:
        return 146

os.makedirs("screenshots", exist_ok=True)

@pytest.fixture(scope="session")
def browser_driver():
    """
    Session-scoped fixture to initialize undetected-chromedriver.
    """
    options = uc.ChromeOptions()
    options.add_argument("--disable-popup-blocking")
    
    major_version = get_chrome_major_version()
    driver = uc.Chrome(options=options, version_main=major_version)
    driver.maximize_window()
    
    yield driver
    
    driver.quit()

@pytest.fixture(scope="function")
def driver(browser_driver):
    """
    Function-scoped fixture to provide the WebDriver.
    """
    yield browser_driver

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        if "driver" in item.fixturenames:
            driver = item.funcargs["driver"]
            screenshot_path = os.path.join("screenshots", f"{item.name}.png")
            try:
                driver.save_screenshot(screenshot_path)
                print(f"\nScreenshot saved to {screenshot_path}")
            except Exception as e:
                print(f"\nFailed to take screenshot: {e}")
