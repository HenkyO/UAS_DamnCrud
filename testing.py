import sys
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class CustomTestCase(unittest.TestCase):
    def setUp(self):
        options = FirefoxOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        server = 'http://localhost:4444'  # Adjust the Selenium endpoint if needed
        self.browser = webdriver.Remote(command_executor=server, options=options)

    def test_valid_login(self):
        self.browser.get("http://localhost/login.php")
        self.browser.find_element(By.NAME, "username").send_keys("admin")
        self.browser.find_element(By.NAME, "password").send_keys("nimda666!")
        self.browser.find_element(By.NAME, "login").click()
        time.sleep(2)
        # Check if the page title contains "Dashboard"
        self.assertIn("Dashboard", self.browser.title)
        print("[PASS] Valid Login Test")

    def test_invalid_login(self):
        self.browser.get("http://localhost/login.php")
        self.browser.find_element(By.NAME, "username").send_keys("admin1")
        self.browser.find_element(By.NAME, "password").send_keys("namdi666!")
        self.browser.find_element(By.NAME, "login").click()
        time.sleep(2)
        # Verify that an error message is displayed on the page
        self.assertIn("Username atau password salah", self.browser.page_source)
        print("[PASS] Invalid Login Test")

    def test_sql_injection(self):
        self.browser.get("http://localhost/login.php")
        self.browser.find_element(By.NAME, "username").send_keys("admin' --")
        self.browser.find_element(By.NAME, "password").send_keys("")
        self.browser.find_element(By.NAME, "login").click()
        time.sleep(2)
        # Assert that the error message is displayed
        self.assertIn("Username atau password salah", self.browser.page_source)
        print("[PASS] SQL Injection Test")

    def test_duplicate_email(self):
        # Login first
        self.browser.get("http://localhost/login.php")
        self.browser.find_element(By.NAME, "username").send_keys("admin")
        self.browser.find_element(By.NAME, "password").send_keys("nimda666!")
        self.browser.find_element(By.NAME, "login").click()
        time.sleep(2)
        # Navigate to the create contact page and submit a duplicate email
        self.browser.get("http://localhost/create.php")
        self.browser.find_element(By.NAME, "name").send_keys("David Deacon")
        self.browser.find_element(By.NAME, "email").send_keys("daviddeacon@example.com")
        self.browser.find_element(By.NAME, "phone").send_keys("2025550121")
        self.browser.find_element(By.NAME, "title").send_keys("Security")
        self.browser.find_element(By.NAME, "save").click()
        time.sleep(2)
        # Verify that the duplicate email error message appears
        self.assertIn("Email already exists", self.browser.page_source)
        print("[PASS] Duplicate Email Test")

    def test_update_contact(self):
        # Login first
        self.browser.get("http://localhost/login.php")
        self.browser.find_element(By.NAME, "username").send_keys("admin")
        self.browser.find_element(By.NAME, "password").send_keys("nimda666!")
        self.browser.find_element(By.NAME, "login").click()
        time.sleep(2)
        # Navigate to the dashboard and click on the "Edit" link for a contact
        self.browser.get("http://localhost/index.php")
        self.browser.find_element(By.LINK_TEXT, "Edit").click()
        time.sleep(2)
        # Update the phone number field
        phone_input = self.browser.find_element(By.NAME, "phone")
        phone_input.clear()
        phone_input.send_keys("0987654321")
        self.browser.find_element(By.NAME, "save").click()
        time.sleep(2)
        # Verify that the updated phone number appears on the page
        self.assertIn("0987654321", self.browser.page_source)
        print("[PASS] Update Contact Test")

    def tearDown(self):
        self.browser.quit()

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], verbosity=2, warnings='ignore')
