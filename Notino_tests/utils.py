from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def wait_for_first_visible(driver, selectors, timeout=10):
    """
    Iterates through a list of fallback CSS selectors and waits 
    for the first one to become visible using Selenium.
    
    Returns:
        The WebElement of the first visible locator found.
    """
    for selector in selectors:
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
            )
            return element
        except TimeoutException:
            continue
            
    raise Exception(f"None of the selectors became visible within {timeout}s: {selectors}")
