from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


ch = os.getcwd() + '/tools/chromedriver'
options = Options()
options.set_headless(headless=True)
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")


links = []
domain = ""

class HardMath(object):
  def valid_link(self, link, domain):

      '''
          Determine whether the link is within the domain
      '''

      if link.find("https://") == 0:
          link = link[8:]
      if link.find("http://") == 0:
          link = link[7:]
      
      if domain in link.split("."):
          return True
      return False


  def get_links(self, driver, curr_level, links, domain):

      '''
          Fetch all the a-tags in the webpage
          Store them in the list at (curr_level+1)
      '''

      page_links = driver.find_elements_by_xpath("//a[@href]")
      for link_el in page_links:
          link = link_el.get_attribute("href")
          if valid_link(link, domain):                #tested
              try:
                  links[curr_level+1].append(link)
              except:
                  links.append([link])
      return links


  def pure_word(self, word):
      '''
          True: Word has only alphabets
      '''

      return all(char.isalpha() for char in word)


  def get_text(self, driver):

      '''
          Gets all the text nodes on a webpage
      '''

      body = driver.find_element_by_tag_name("body")
      text = body.get_attribute("innerText")
      spaced_text = ""
      for s in text:
          if s == "\n":
              spaced_text += " "
          elif s.isupper():
              spaced_text += s.lower()
          else:
              spaced_text += s

      words = sorted(list(filter(lambda x: pure_word(x), filter(lambda x: len(x) > 2, spaced_text.split()))), key=len)
      return words


  def scrape(self, url, max_level, curr_level, links, domain):

      '''
          Initialize Driver
          Get the links
          Get the text
          Filter text
          Save results
      '''

      global ch
      global options

      driver = webdriver.Chrome(options=options, executable_path=ch)
      driver.get(url)
      driver.implicitly_wait(10)

      if curr_level < max_level:
          get_links(driver, curr_level, links, domain)       #tested

      text = get_text(driver)                 #tested

      result = filter_text(text)              #function

      save(result, url)                       #function

      driver.quit()
