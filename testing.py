import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default="http://localhost", help="Base URL for tests")

@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url")

@pytest.fixture(scope="function")
def driver():
    options = FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # Enable headless mode if running in a CI environment (GitHub Actions sets CI=true)
    if os.environ.get("CI"):
        options.headless = True
    server = 'http://localhost:4444'  # Adjust Selenium endpoint if needed
    driver = webdriver.Remote(command_executor=server, options=options)
    yield driver
    driver.quit()

def test_successful_login(driver, base_url):
    login_url = base_url + "/login.php"
    driver.get(login_url)
    driver.find_element(By.ID, "inputUsername").send_keys("admin")
    driver.find_element(By.ID, "inputPassword").send_keys("nimda666!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    assert "Dashboard" in driver.page_source

def test_incorrect_username(driver, base_url):
    login_url = base_url + "/login.php"
    driver.get(login_url)
    driver.find_element(By.ID, "inputUsername").send_keys("invalid_user")
    driver.find_element(By.ID, "inputPassword").send_keys("namdi666!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    error_text = driver.find_element(By.CSS_SELECTOR, "div.checkbox.mb-3 label").text.strip()
    assert error_text == "Damn, wrong credentials!!"

def test_incorrect_password(driver, base_url):
    login_url = base_url + "/login.php"
    driver.get(login_url)
    driver.find_element(By.ID, "inputUsername").send_keys("admin")
    driver.find_element(By.ID, "inputPassword").send_keys("invalid_password")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    error_text = driver.find_element(By.CSS_SELECTOR, "div.checkbox.mb-3 label").text.strip()
    assert error_text == "Damn, wrong credentials!!"

def test_blank_credentials(driver, base_url):
    login_url = base_url + "/login.php"
    driver.get(login_url)
    driver.find_element(By.ID, "inputUsername").send_keys("")
    driver.find_element(By.ID, "inputPassword").send_keys("")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    error_text = driver.find_element(By.CSS_SELECTOR, "div.checkbox.mb-3 label").text.strip()
    assert error_text == "Damn, wrong credentials!!"

def test_xss_detection(driver, base_url):
    login_url = base_url + "/login.php"
    xss_url = base_url + "/vpage.php"
    # Log in first
    driver.get(login_url)
    driver.find_element(By.ID, "inputUsername").send_keys("admin")
    driver.find_element(By.ID, "inputPassword").send_keys("nimda666!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)
    # Navigate to the XSS page and submit payload
    driver.get(xss_url)
    xss_payload = '<script>alert("xss")</script>'
    driver.find_element(By.NAME, "thing").send_keys(xss_payload)
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    time.sleep(2)
    try:
        alert_box = driver.switch_to.alert
        assert alert_box.text == "xss"
        alert_box.accept()
    except Exception:
        pytest.fail("XSS alert not triggered.")

if __name__ == '__main__':
    import sys
    import pytest
    # Convert positional argument (if present) into the --base-url option.
    # E.g., running: python testing.py http://172.17.0.1
    # becomes: pytest testing.py --base-url=http://172.17.0.1
    new_args = sys.argv[1:]
    if new_args and not new_args[0].startswith("--"):
        new_args = [f"--base-url={new_args[0]}"] + new_args[1:]
    sys.exit(pytest.main(new_args))
