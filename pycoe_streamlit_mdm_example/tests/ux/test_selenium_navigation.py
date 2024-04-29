import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class StreamlitAppTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()  # Change this to the appropriate webdriver for your browser

    def tearDown(self):
        self.driver.quit()

    def test_main_page(self):
        self.driver.get("http://localhost:8501")  # Replace this with the URL of your Streamlit app
        time.sleep(5)  # Wait for page to load (adjust as necessary)
        self.assertTrue("Welcome To The Kubrick MDM Training and Development Tool" in self.driver.page_source)

    def test_data_generation_page(self):
        self.driver.get("http://localhost:8501")  # Replace this with the URL of your Streamlit app
        time.sleep(5)  # Wait for page to load (adjust as necessary)
        # Navigate to the Data Creation/Upload page
        self.driver.find_element("link text", "Creation or Upload").click()
        time.sleep(5)  # Wait for page to load (adjust as necessary)
        self.assertTrue("Data Creation/Upload" in self.driver.page_source)

    def test_matching_process_page(self):
        self.driver.get("http://localhost:8501")  # Replace this with the URL of your Streamlit app
        time.sleep(5)  # Wait for page to load (adjust as necessary)
        # Navigate to the Matching Process page
        self.driver.find_element("link text", "Match").click()
        time.sleep(5)  # Wait for page to load (adjust as necessary)
        self.assertTrue("Matching Process" in self.driver.page_source)

    def test_merging_process_page(self):
        self.driver.get("http://localhost:8501")  # Replace this with the URL of your Streamlit app
        time.sleep(5)  # Wait for page to load (adjust as necessary)
        # Navigate to the Matching Process page
        self.driver.find_element("link text", "Merge").click()
        time.sleep(5)  # Wait for page to load (adjust as necessary)
        self.assertTrue("Merging Process" in self.driver.page_source)

if __name__ == "__main__":
    unittest.main()