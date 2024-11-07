from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
from parameterized import parameterized

class TestWikipediaArticle(unittest.TestCase):

    def setUp(self):
        self.driver = None

    def initialize_driver(self, browser):
        if browser == 'edge':
            self.driver = webdriver.Edge()
        elif browser == 'chrome':
            self.driver = webdriver.Chrome()
        elif browser == 'firefox':
            self.driver = webdriver.Firefox()
        else:
            raise ValueError("Unsupported browser!")

    @parameterized.expand([
        ("edge",),
        ("chrome",),
        ("firefox",)
    ])
    def test_wikipedia_article_elements(self, browser):
        # Initialize WebDriver
        self.initialize_driver(browser)
        driver = self.driver
        driver.get("https://www.wikipedia.org")

        # Search for a term and navigate to an article page
        search_input = driver.find_element(By.NAME, "search")
        search_input.send_keys("Artificial Intelligence" + Keys.RETURN)

        # Wait for navigation to complete and check the title
        self.assertIn("Artificial Intelligence", driver.title)

        # Verify table of contents presence
        toc = driver.find_element(By.ID, "toc")
        print(f"Table of contents found: {toc is not None}")
        self.assertTrue(toc.is_displayed())

        # Check language links in sidebar
        sidebar_links = driver.find_elements(By.CSS_SELECTOR, "#p-lang .interlanguage-link-target")
        languages = ["en", "es", "de", "fr", "pl"]
        for lang in languages:
            lang_link = next((link for link in sidebar_links if lang in link.get_attribute("hreflang")), None)
            print(f"Language link for '{lang}' found: {lang_link is not None}")
            self.assertTrue(lang_link)

        # Verify search bar is present on article page
        search_input_article = driver.find_element(By.NAME, "search")
        print(f"Search bar found on article page: {search_input_article is not None}")
        self.assertTrue(search_input_article.is_displayed())

        # Verify content heading (first header) is present
        content_heading = driver.find_element(By.ID, "firstHeading")
        print(f"Content heading found: {content_heading is not None}")
        self.assertTrue(content_heading.is_displayed())

    def tearDown(self):
        # Close the browser after each test
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()
