import sys
import os
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class TestLoginScenarios(unittest.TestCase):
    def setUp(self):
        options = FirefoxOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        # Enable headless mode if running in a CI environment (GitHub Actions sets CI=true)
        if os.environ.get("CI"):
            options.headless = True
        server = 'http://localhost:4444'  # Adjust Selenium endpoint if needed
        self.driver = webdriver.Remote(command_executor=server, options=options)

    def test_successful_login(self):
        base_url = sys.argv[1] + "/login.php" if len(sys.argv) > 1 else "http://localhost/login.php"
        self.driver.get(base_url)
        self.driver.find_element(By.ID, "inputUsername").send_keys("admin")
        self.driver.find_element(By.ID, "inputPassword").send_keys("nimda666!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        self.assertIn("Dashboard", self.driver.page_source)

    def test_incorrect_username(self):
        base_url = sys.argv[1] + "/login.php" if len(sys.argv) > 1 else "http://localhost/login.php"
        self.driver.get(base_url)
        self.driver.find_element(By.ID, "inputUsername").send_keys("invalid_user")
        self.driver.find_element(By.ID, "inputPassword").send_keys("namdi666!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        error_text = self.driver.find_element(By.CSS_SELECTOR, "div.checkbox.mb-3 label").text.strip()
        self.assertEqual(error_text, "Damn, wrong credentials!!")

    def test_incorrect_password(self):
        base_url = sys.argv[1] + "/login.php" if len(sys.argv) > 1 else "http://localhost/login.php"
        self.driver.get(base_url)
        self.driver.find_element(By.ID, "inputUsername").send_keys("admin")
        self.driver.find_element(By.ID, "inputPassword").send_keys("invalid_password")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        error_text = self.driver.find_element(By.CSS_SELECTOR, "div.checkbox.mb-3 label").text.strip()
        self.assertEqual(error_text, "Damn, wrong credentials!!")

    def test_blank_credentials(self):
        base_url = sys.argv[1] + "/login.php" if len(sys.argv) > 1 else "http://localhost/login.php"
        self.driver.get(base_url)
        self.driver.find_element(By.ID, "inputUsername").send_keys("")
        self.driver.find_element(By.ID, "inputPassword").send_keys("")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        error_text = self.driver.find_element(By.CSS_SELECTOR, "div.checkbox.mb-3 label").text.strip()
        self.assertEqual(error_text, "Damn, wrong credentials!!")

    def test_xss_detection(self):
        if len(sys.argv) > 1:
            login_url = sys.argv[1] + "/login.php"
            xss_url = sys.argv[1] + "/vpage.php"
        else:
            login_url = "http://localhost/login.php"
            xss_url = "http://localhost/vpage.php"
        # Log in first
        self.driver.get(login_url)
        self.driver.find_element(By.ID, "inputUsername").send_keys("admin")
        self.driver.find_element(By.ID, "inputPassword").send_keys("nimda666!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)
        # Navigate to the XSS page and submit payload
        self.driver.get(xss_url)
        xss_payload = '<script>alert("xss")</script>'
        self.driver.find_element(By.NAME, "thing").send_keys(xss_payload)
        self.driver.find_element(By.XPATH, "//input[@type='submit']").click()
        time.sleep(2)
        try:
            alert_box = self.driver.switch_to.alert
            self.assertEqual(alert_box.text, "xss")
            alert_box.accept()
        except Exception as error:
            self.fail("XSS alert not triggered.")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    # If xmlrunner is available, use it to generate JUnit XML reports for GitHub Actions.
    try:
        import xmlrunner
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
                      argv=['first-arg-is-ignored'], verbosity=2, warnings='ignore')
    except ImportError:
        unittest.main(argv=['first-arg-is-ignored'], verbosity=2, warnings='ignore')
