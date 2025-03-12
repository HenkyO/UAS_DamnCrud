import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope='session')
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_valid_login(driver):
    driver.get("http://localhost/login.php")
    driver.find_element(By.ID, "inputUsername").send_keys("admin")
    driver.find_element(By.ID, "inputPassword").send_keys("nimda666!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    assert "Dashboard" in driver.page_source
    print("[PASS] Valid Login Test")

def test_invalid_login(driver):
    driver.get("http://localhost/login.php")
    driver.find_element(By.ID, "inputUsername").send_keys("wronguser")
    driver.find_element(By.ID, "inputPassword").send_keys("wrongpass")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    error_message = driver.find_element(By.CSS_SELECTOR, "div.checkbox.mb-3 label").text.strip()
    assert error_message == "Damn, wrong credentials!!"
    print("[PASS] Invalid Login Test")

def test_sql_injection(driver):
    driver.get("http://localhost/login.php")
    driver.find_element(By.ID, "inputUsername").send_keys("admin' --")
    driver.find_element(By.ID, "inputPassword").send_keys("")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    assert "Damn, wrong credentials!!" in driver.page_source
    print("[PASS] SQL Injection Test")

def test_duplicate_email(driver):
    driver.get("http://localhost/login.php")
    driver.find_element(By.ID, "inputUsername").send_keys("admin")
    driver.find_element(By.ID, "inputPassword").send_keys("nimda666!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    driver.get("http://localhost/create.php")
    driver.find_element(By.ID, "name").send_keys("David Deacon")
    driver.find_element(By.ID, "email").send_keys("daviddeacon@example.com")
    driver.find_element(By.ID, "phone").send_keys("2025550121")
    driver.find_element(By.ID, "title").send_keys("Security")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    assert "Email already exists" in driver.page_source
    print("[PASS] Duplicate Email Test")

def test_update_contact(driver):
    driver.get("http://localhost/login.php")
    driver.find_element(By.ID, "inputUsername").send_keys("admin")
    driver.find_element(By.ID, "inputPassword").send_keys("nimda666!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    driver.get("http://localhost/index.php")
    driver.find_element(By.LINK_TEXT, "Edit").click()
    phone_input = driver.find_element(By.ID, "phone")
    phone_input.clear()
    phone_input.send_keys("0987654321")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    assert "0987654321" in driver.page_source
    print("[PASS] Update Contact Test")
