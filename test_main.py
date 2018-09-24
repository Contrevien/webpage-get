import unittest
import os
import sys
sys.path.append(os.path.abspath("./tests"))

from main import Webpage, valid_link, find_last_name

obj = Webpage("https://contrevien.github.io/test-scraping/", "github")

class TestMain(unittest.TestCase):

    def test_valid_link(self):
        self.assertTrue(valid_link("google.com", "google"))
        self.assertTrue(valid_link("https://google.com", "google"))
        self.assertTrue(valid_link("http://google.com", "google"))
        self.assertTrue(valid_link("http://www.google.com/", "google"))
        self.assertTrue(valid_link("www.google.com", "google"))
        self.assertFalse(valid_link("abc.com", "google"))

    def test_find_last_name(self):
        self.assertEqual(find_last_name("google.com/something/"), "something")
        self.assertEqual(find_last_name("https://google.com/something"), "something")
        self.assertEqual(find_last_name("http://google.com"), "google.com")
        self.assertEqual(find_last_name("http://www.google.com/"), "www.google.com")
        self.assertEqual(find_last_name("www.google.com"), "www.google.com")

    def test_get_links(self):
        
        global obj
        
        expected_links = [
            "https://contrevien.github.io/test-scraping/first",
            "https://contrevien.github.io/test-scraping/second",
            "https://contrevien.github.io/test-scraping/nested",
            "https://contrevien.github.io/test-scraping/wrongly"
        ]

        links = obj.get_links()

        for i in range(len(expected_links)):
            self.assertEqual(links[i], expected_links[i])

    def test_get_words(self):
        self.assertEqual(len(obj.get_words()), 53)

    def test_get_numbers(self):
        self.assertEqual(len(obj.get_numbers()), 10)
    
    def test_get_emails(self):
        self.assertEqual(len(obj.get_emails()), 2)

    def test_get_tables_as_list(self):
        self.assertEqual(len(obj.get_tables_as_list()), 3)
        self.assertEqual(len(obj.get_tables_as_list(1)), 3)
        self.assertEqual(len(obj.get_tables_as_list(2, 3)), 1)
    
    def test_get_tables_as_csv(self):
        obj.get_tables_as_csv()

    def test_get_images(self):
        obj.get_images()


if __name__ == "__main__":
    unittest.main()