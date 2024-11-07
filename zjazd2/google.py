import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

class GoogleTest(unittest.TestCase):

    def setUp(self):
        # Setup Chrome WebDriver
        options = Options()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)

    def test_google_search_and_shop(self):
        driver = self.driver
        driver.get("https://www.google.com")

        # Assertion 1 - Checks if the reject cookies button is available
        reject_button = driver.find_element(By.ID, "W0wltc")
        self.assertTrue(reject_button.is_displayed())

        # Step 2 - Click the reject cookies button
        reject_button.click()

        # Assertion 2 - Check if the title is "Google"
        home_title = driver.title
        self.assertEqual("Google", home_title)

        # Assertion 3 - Check if the link with text "Google Store" is displayed
        store_link = driver.find_element(By.LINK_TEXT, "Google Store")
        self.assertTrue(store_link.is_displayed())

        # Step 3 - Navigate to Google Store
        store_link.click()

        # Assertion 4 - Check if there is a link that partially contains the text "Telefony"
        phones = driver.find_element(By.PARTIAL_LINK_TEXT, "Telefony")
        self.assertTrue(phones.is_displayed())

        # Step 4 - Go back to the previous page
        driver.back()

        # Assertion 5 - Verify title is still "Google" after navigating back
        home_title_2 = driver.title
        self.assertEqual("Google", home_title_2)

        # Step 5 - Search for "pjatk" in the search box and submit
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("pjatk")
        search_box.submit()

        # Wait until the URL contains "pjatk"
        wait = WebDriverWait(driver, 5)
        wait.until(EC.url_contains("pjatk"))

        # Assertion 6 - Check if "Grafika" link is available
        photos_link = driver.find_element(By.LINK_TEXT, "Grafika")
        self.assertTrue(photos_link.is_displayed())

        # Step 6 - Navigate to the images section
        photos_link.click()

        # Assertion 7 - Check if "Log in" button is present
        login_button = driver.find_element(By.LINK_TEXT, "Zaloguj się")
        self.assertTrue(login_button.is_displayed())

        # Assertion 8 - Check if the element with class name "BA0zte" is displayed
        similar_searches_section = driver.find_element(By.CLASS_NAME, "BA0zte")
        self.assertTrue(similar_searches_section.is_displayed())

    def tearDown(self):
        # Close the browser after each test
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()