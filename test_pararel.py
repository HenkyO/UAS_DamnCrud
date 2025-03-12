import sys
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

@pytest.fixture(scope="function")
def browser():
    firefox_options = FirefoxOptions()
    firefox_options.add_argument('--ignore-certificate-errors')
    firefox_options.add_argument('--ignore-ssl-errors')
    selenium_server = 'http://localhost:4444'  # Adjust Selenium endpoint if needed
    driver = webdriver.Remote(command_executor=selenium_server, options=firefox_options)
    yield driver
    driver.quit()

def test_successful_login(browser):
    base_url = sys.argv[1] + "/login.php" if len(sys.argv) > 1 else "http://localhost/login.php"
    browser.get(base_url)
    browser.find_element(By.ID, "inputUsername").send_keys("admin")
    browser.find_element(By.ID, "inputPassword").send_keys("nimda666!")
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    assert "Dashboard" in browser.page_source

def test_incorrect_username(browser):
    base_url = sys.argv[1] + "/login.php" if len(sys.argv) > 1 else "http://localhost/login.php"
    browser.get(base_url)
    browser.find_element(By.ID, "inputUsername").send_keys("invalid_user")
    browser.find_element(By.ID, "inputPassword").send_keys("namdi666!")
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    error_text = browser.find_element(By.CSS_SELECTOR, "div.checkbox.mb-3 label").text.strip()
    assert error_text == "Damn, wrong credentials!!"

def test_incorrect_password(browser):
    base_url = sys.argv[1] + "/login.php" if len(sys.argv) > 1 else "http://localhost/login.php"
    browser.get(base_url)
    browser.find_element(By.ID, "inputUsername").send_keys("admin")
    browser.find_element(By.ID, "inputPassword").send_keys("invalid_password")
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    error_text = browser.find_element(By.CSS_SELECTOR, "div.checkbox.mb-3 label").text.strip()
    assert error_text == "Damn, wrong credentials!!"

def test_blank_credentials(browser):
    base_url = sys.argv[1] + "/login.php" if len(sys.argv) > 1 else "http://localhost/login.php"
    browser.get(base_url)
    browser.find_element(By.ID, "inputUsername").send_keys("")
    browser.find_element(By.ID, "inputPassword").send_keys("")
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    error_text = browser.find_element(By.CSS_SELECTOR, "div.checkbox.mb-3 label").text.strip()
    assert error_text == "Damn, wrong credentials!!"

def test_xss_detection(browser):
    if len(sys.argv) > 1:
        login_url = sys.argv[1] + "/login.php"
        xss_url = sys.argv[1] + "/vpage.php"
    else:
        login_url = "http://localhost/login.php"
        xss_url = "http://localhost/vpage.php"
    # Log in first
    browser.get(login_url)
    browser.find_element(By.ID, "inputUsername").send_keys("admin")
    browser.find_element(By.ID, "inputPassword").send_keys("nimda666!")
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    # Navigate to XSS page and submit payload
    browser.get(xss_url)
    xss_payload = '<script>alert("xss")</script>'
    browser.find_element(By.NAME, "thing").send_keys(xss_payload)
    browser.find_element(By.XPATH, "//input[@type='submit']").click()
    time.sleep(2)
    try:
        alert_box = browser.switch_to.alert
        assert alert_box.text == "xss"
        alert_box.accept()
    except Exception as error:
        pytest.fail("XSS alert not triggered.")
