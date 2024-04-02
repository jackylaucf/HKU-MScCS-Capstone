import time

from bs4 import BeautifulSoup
from crawler.strategy.SourceStrategy import SourceStrategy
from model.market_data import DailyPrice, IntradayPrice
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class TradingViewSourceStrategy(SourceStrategy):

    def get_source_name(self) -> str:
        return 'Trading View'

    def get_daily_price(self, ticker: str) -> (str, [DailyPrice]):
        raise NotImplementedError()

    def get_intraday_price(self, ticker: str) -> (str, [IntradayPrice]):
        raise NotImplementedError()

    def get_constituents(self) -> [str]:
        url = 'https://www.tradingview.com/symbols/{ticker}/components'.format(ticker=self.index_ticker)
        browser_options = Options()
        browser_options.add_argument('--headless=new')
        browser = webdriver.Chrome(options=browser_options)
        browser.get(url)
        constituents = []
        try:
            while button_element := browser.find_element(By.CSS_SELECTOR, "div[class^='loadMoreWrapper']"):
                button_element.click()
                time.sleep(3)
        except NoSuchElementException:
            parsed_html = BeautifulSoup(browser.page_source, 'html.parser')
            for element in parsed_html.findAll('a', {'class': 'tickerName-GrtoTeat'}):
                constituents.append(element.text)
        finally:
            return constituents
