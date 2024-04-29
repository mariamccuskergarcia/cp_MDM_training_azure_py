import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class StreamlitAppScreenshotTests(unittest.TestCase):
    def setUp(self):
        # Configure Selenium WebDriver to run headlessly and capture screenshots
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run headlessly (without opening a browser window)
        self.driver = webdriver.Chrome(options=chrome_options)  # Change this to the appropriate webdriver for your browser

    def tearDown(self):
        self.driver.quit()

    def test_take_screenshot_main_page(self):
        self.driver.get("http://localhost:8501")  # Replace this with the URL of your Streamlit app
        time.sleep(5)  # Wait for page to load (adjust as necessary)
        self.take_screenshot("main_page")

    def test_take_screenshot_Creation_or_Upload(self):
        self.driver.get("http://localhost:8501/Creation_or_Upload")  # Replace this with the URL of the data generation page
        time.sleep(5)  # Wait for page to load (adjust as necessary)
        self.take_screenshot("Creation_or_Upload")

    def test_take_screenshot_Match(self):
        self.driver.get("http://localhost:8501/Match")  # Replace this with the URL of the matching process page
        time.sleep(5)  # Wait for page to load (adjust as necessary)
        self.take_screenshot("Match")

    def test_take_screenshot_Merge(self):
        self.driver.get("http://localhost:8501/Merge")  # Replace this with the URL of the merging process page
        time.sleep(5)  # Wait for page to load (adjust as necessary)
        self.take_screenshot("Merge")

    def take_screenshot(self, page_name):
        # Capture screenshot
        screenshot_filename = f"{page_name}_screenshot.png"
        self.driver.save_screenshot(screenshot_filename)
        print(f"Screenshot captured: {screenshot_filename}")

if __name__ == "__main__":
    unittest.main()