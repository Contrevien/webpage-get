from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import re
import csv
import urllib.request


def valid_link(link, domain):

    '''
        Utility
        Determine whether the link is within the domain
    '''

    if link.find("https://") == 0:
        link = link[8:]
    if link.find("http://") == 0:
        link = link[7:]
    
    if domain in link.split("."):
        return True
    return False


def find_last_name(url):

    '''
        Returns string between last and second-last '/'
    '''

    if url[-1] == '/':
        url = url[:-1]

    return url.split('/')[-1]


class Webpage(object):

    def __init__(self, url, domain):
        ch = os.getcwd() + '/tools/chromedriver'
        options = Options()
        options.set_headless(headless=True)
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=options, executable_path=ch)
        self.domain = domain
        self.url = url
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        body = self.driver.find_element_by_tag_name("body")
        text = body.get_attribute("innerText")
        spaced_text = ""
        for s in text:
            if s == "\n":
                spaced_text += " "
            elif s.isupper():
                spaced_text += s.lower()
            else:
                spaced_text += s
        self.words = spaced_text.split()


    def get_links(self):

        '''
            Fetch all the a-tags in the webpage
        '''

        page_links = self.driver.find_elements_by_xpath("//a[@href]")

        if len(page_links) == 0:
            print("No links found!")
            return

        links = []
        for link_el in page_links:
            link = link_el.get_attribute("href")
            if valid_link(link, self.domain):                #tested
                links.append(link)
        return links


    def get_words(self):

        '''
            Get all the words from the webpage
        '''

        return list(filter(lambda x: len(x) > 2 and all(char.isalpha() for char in x), self.words))


    def get_numbers(self):
        
        '''
            Get all the numbers from the webpage
        '''

        return list(filter(lambda x: all(char.isdigit() for char in x), self.words))


    def get_emails(self):
        
        '''
            Get all the emails from the webpage
        '''

        return list(filter(lambda x: re.match("[^@]+@[^@]+\.[^@]+", x), self.words))


    def get_tables_as_list(self, start=None, end=None):
        
        '''
            Fetch all tables
            Return content from tables no. "start" to table no. "end" as lists
            [
                [
                    [col1, col2, col3],
                    [val1, val2, val3],
                    [val4, val5, val6],
                ],
                [
                    [col1, col2, col3],
                    [val1, val2, val3],
                    [val4, val5, val6],                    
                ]
            ]
        '''

        tables = self.driver.find_elements_by_tag_name("table")
        if len(tables) == 0:
            print("No tables found!")
            return

        if end != None:
            tables = tables[start:end]
        
        content = []

        for table in tables:
            table_content = []

            rows = table.find_elements_by_tag_name("tr")
            for row in rows:
                row_content = []
                cols = row.find_elements_by_css_selector("*")
                for col in cols:
                    row_content.append(col.text)
                table_content.append(row_content)
            content.append(table_content)
        
        return content

    
    def get_tables_as_csv(self, start=None, end=None):

        '''
            Get Tables and save as csv file
        '''

        content = self.get_tables_as_list(start, end)

        if len(content) == 0:
            print("No tables found!")
            return

        with open(self.domain + "-tables.csv", "w", newline="") as new_file:
            csv_writer = csv.writer(new_file)

            for table in content:
                empty = ""
                for row in table:
                    csv_writer.writerow(row)
                csv_writer.writerow(empty)

    
    def get_images(self):
        
        '''
            Get all images from the website
        '''

        images = self.driver.find_elements_by_tag_name("img")

        if len(images) == 0:
            print("No images found!")
            return

        try:
            os.mkdir(find_last_name(self.url) + "-images")
        except:
            pass
        index = 1
        for img in images:
            src = img.get_attribute('src')
            urllib.request.urlretrieve(src, "./" + find_last_name(self.url) + "-images/" + find_last_name(src))
            index += 1
        


