import time
import pytest
from utils import wait_for_first_visible
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def click_cookie_accept_if_present(driver):
    try:
        btn = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-accept-btn-handler"))
        )
        btn.click()
    except Exception:
        pass

def test_valid_search(driver):
    """
    TC_001: Valid Search
    """
    driver.get("https://www.notino.ua/")
    time.sleep(3)
    
    click_cookie_accept_if_present(driver)
        
    search_input_selectors = [
        "input[data-testid='searchInput']",
        "input[type='search']",
        ".search-input",
        "input[name='q']"
    ]
    
    search_input = wait_for_first_visible(driver, search_input_selectors)
    search_input.click()
    search_input.clear()
    
    for char in "Calvin Klein":
        search_input.send_keys(char)
        time.sleep(0.1)
    
    search_input.send_keys(Keys.ENTER)
    
    try:
        search_btn = driver.find_element(By.CSS_SELECTOR, "button[data-testid='searchSubmit']")
        search_btn.click()
    except Exception:
        pass
        
    time.sleep(4)
    
    try:
        wait_for_first_visible(driver, ["div[data-testid='product-container']", ".product-card"], timeout=5)
    except Exception:
        pass
        
    body_text = driver.find_element(By.CSS_SELECTOR, "body").text.lower()
    found = "calvin klein" in body_text or "кляйн" in body_text
            
    assert found, "Calvin Klein was not found in the search results"

def test_invalid_search(driver):
    """
    TC_002: Invalid Search
    """
    driver.get("https://www.notino.ua/")
    time.sleep(3)
    
    click_cookie_accept_if_present(driver)
        
    search_input = wait_for_first_visible(driver, ["input[data-testid='searchInput']", "input[type='search']", "input[name='q']"])
    search_input.click()
    search_input.clear()
    
    for char in "qwertyuio":
        search_input.send_keys(char)
        time.sleep(0.1)
        
    search_input.send_keys(Keys.ENTER)
    
    try:
        search_btn = driver.find_element(By.CSS_SELECTOR, "button[data-testid='searchSubmit']")
        search_btn.click()
    except Exception:
        pass

    not_found_phrases = ["не знайдено", "нічого не знайдено", "0 результатів", "nothing found", "0 results", "не знайшли"]
    
    found = False
    start_time = time.time()
    while time.time() - start_time < 15:
        body_text = driver.find_element(By.CSS_SELECTOR, "body").text.lower()
        if any(phrase in body_text for phrase in not_found_phrases):
            found = True
            break
        time.sleep(1)
        
    assert found, "Nothing found message was not displayed in the page body within 15 seconds"

def test_add_product_to_cart(driver):
    """
    TC_003: Add Product to Cart
    """
    driver.get("https://www.notino.ua/parfyumeriya-dlya-zhenshchin/")
    time.sleep(3)
    
    click_cookie_accept_if_present(driver)
        
    product_card_selectors = [
        "div[data-testid='product-container'] a",
        "div[data-testid='product-container']",
        "div[data-testid='productContainer'] span",
        "div[data-testid='productContainer'] a",
        "div[data-testid='productContainer']",
        ".product-card"
    ]
    
    first_product = wait_for_first_visible(driver, product_card_selectors)
    
    actions = ActionChains(driver)
    actions.move_to_element(first_product).perform()
    time.sleep(1)
    
    driver.execute_script("arguments[0].click();", first_product)
    time.sleep(3)

    try:
        cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#pd-buy-button"))
        )
        driver.execute_script("arguments[0].click();", cart_button)
    except Exception:
        raise Exception("Could not find the '#pd-buy-button' button.")
    
    time.sleep(2)
    
    try:
        cart_counter = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/cart/'] div[data-count='1']"))
        )
        assert cart_counter.get_attribute("data-count") == "1", "Cart counter didn't update to 1."
    except Exception:
        raise Exception("Failed to locate cart counter reflecting 1 item: a[href*='/cart/'] div[data-count='1']")

def test_login_page_ui(driver):
    """
    TC_004: Verify Login Page UI
    """
    driver.get("https://www.notino.ua/")
    time.sleep(3)
    
    click_cookie_accept_if_present(driver)

    account_icon_selectors = [
        "a[href*='/mynotino/']",
        "a[data-testid='account-link']",
    ]
    account_icon = wait_for_first_visible(driver, account_icon_selectors)
    try:
        account_icon.click()
    except Exception:
        driver.execute_script("arguments[0].click();", account_icon)
        
    time.sleep(2)
    
    email_selectors = ["input[type='email']", "input[name='email']", "#email"]
    password_selectors = ["input[type='password']", "input[name='password']", "#password"]

    submit_selectors = ["button[name='button'][value='login']", "button.g-recaptcha"]
    
    email_input = wait_for_first_visible(driver, email_selectors)
    password_input = wait_for_first_visible(driver, password_selectors)
    
    try:
        submit_button = wait_for_first_visible(driver, submit_selectors)
    except Exception:
        submit_button = driver.find_element(By.XPATH, "//button[contains(., 'Увійти')]")
    
    assert email_input.is_displayed(), "Email input field is not visible"
    assert password_input.is_displayed(), "Password input field is not visible"
    assert submit_button.is_displayed(), "Submit button is not visible"


def test_filter_by_brand(driver):
    """
    TC_005: Filter by Brand
    """
    driver.get("https://www.notino.ua/parfyumeriya/")
    time.sleep(3)
    
    click_cookie_accept_if_present(driver)
        
    try:
        filter_group = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-testid='filter-group-1']"))
        )
        actions = ActionChains(driver)
        actions.move_to_element(filter_group).perform()
        time.sleep(1)
        driver.execute_script("arguments[0].click();", filter_group)
        time.sleep(2)

        h_letter = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='H'] | //div[normalize-space(text())='H']"))
        )
        actions = ActionChains(driver)
        actions.move_to_element(h_letter).perform()
        time.sleep(1)
        driver.execute_script("arguments[0].click();", h_letter)
        time.sleep(2)
    except Exception:
        pass 
        
    try:
        brand_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='filter-group-1']//a[.//span[contains(text(), 'Hugo Boss')]] | //a[.//span[contains(text(), 'Hugo Boss')]]"))
        )
        actions = ActionChains(driver)
        actions.move_to_element(brand_checkbox).perform()
        time.sleep(1)
        driver.execute_script("arguments[0].click();", brand_checkbox)
    except Exception:
        raise Exception("Hugo Boss checkbox could not be found via precise XPath")

    found_brand = False
    start_time = time.time()
    while time.time() - start_time < 20:
        brand_names = driver.find_elements(By.CSS_SELECTOR, "span[data-testid='product-card-brand']")
        for span in brand_names:
            if "hugo boss" in span.text.lower():
                found_brand = True
                break
        if found_brand:
            break
        time.sleep(1)
        
    assert len(driver.find_elements(By.CSS_SELECTOR, "span[data-testid='product-card-brand']")) > 0, "No product cards displayed after filtering by brand"
    assert found_brand, "Page body does not contain 'Hugo Boss' after filtering within 20 seconds"
