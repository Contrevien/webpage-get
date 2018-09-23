import unittest
from main import HardMath
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


class TestMain(unittest.TestCase):

    def setUp(self):
        ch = os.getcwd() + '/tools/chromedriver'
        options = Options()
        options.set_headless(headless=True)
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options, executable_path=ch)
        self.test_url = "https://contrevien.github.io/test-scraping"
        self.driver.get(self.test_url)
        self.driver.implicitly_wait(10)
        self.obj = HardMath()

    def test_valid_link(self):
        self.assertTrue(self.obj.valid_link("google.com", "google"))
        self.assertTrue(self.obj.valid_link("https://google.com", "google"))
        self.assertTrue(self.obj.valid_link("http://google.com", "google"))
        self.assertTrue(self.obj.valid_link("http://www.google.com", "google"))
        self.assertTrue(self.obj.valid_link("www.google.com", "google"))
        self.assertFalse(self.obj.valid_link("abc.com", "google"))

    def test_get_links(self):

        links = [["https://contrevien.github.io/test-scraping"]]

        expected_links = [
            "https://contrevien.github.io/test-scraping/first",
            "https://contrevien.github.io/test-scraping/second",
            "https://contrevien.github.io/test-scraping/nested",
            "https://contrevien.github.io/test-scraping/wrongly"
        ]

        links = self.obj.get_links(self.driver, 0, links, "contrevien")

        for i in range(len(expected_links)):
            self.assertEqual(links[1][i], expected_links[i])

    def test_get_text(self):

        expected_words = ['tag', 'tag', 'tag', 'age', 'link', 'link', 'link', 'link', 'some', 'text', 'more', 'text', 'even', 'more', 'text', 'with', 'some', 'also', 'text', 'with', 'even', 'more', 'text', 'with', 'first', 'other', 'second', 'nested', 'nested', 'random', 'akhand', 'mishra', 'female', 'should', 'wrongly', 'lastname', 'firstname']
        fetched_words = self.obj.get_text(self.driver)

        for i in range(len(expected_words)):
            self.assertEqual(fetched_words[i], expected_words[i])
