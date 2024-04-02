from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

from crawler import http_utils

url = 'https://www.tradingview.com/symbols/{ticker}/components'.format(ticker='KRX-KOSDAQ')
browser_options = Options()
browser_options.add_argument('--headless=new')
browser = webdriver.Chrome() #options=browser_options
browser.get(url)
try:
    while button_element := browser.find_element(By.CSS_SELECTOR, "div[class^='loadMoreWrapper']"):
        button_element.click()
        time.sleep(3)
except NoSuchElementException:
    parsed_html = BeautifulSoup(browser.page_source, 'html.parser')
    constituents = []
    for element in parsed_html.findAll('a', {'class': 'tickerName-GrtoTeat'}):
        constituents.append(element.text)
    print(constituents)
browser.close()
