from bs4 import BeautifulSoup
from crawler.strategy.SourceStrategy import SourceStrategy
from enum import auto, StrEnum
from model.market_data import DailyPrice, IntradayPrice
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from typing import Callable


class InvestingDotComDataType(StrEnum):
    indices = auto()
    equities = auto()


class InvestingDotComSourceStrategy(SourceStrategy):

    def __init__(self, index_ticker: [str, None], ticker_formatter: Callable[[str], str] = None,
                 source_type: InvestingDotComDataType = InvestingDotComDataType.equities):
        super().__init__(index_ticker, ticker_formatter)
        self.source_type = source_type

    def get_source_name(self) -> str:
        return 'Investing.com'

    def get_daily_price(self, ticker: str) -> (str, [DailyPrice]):
        url = f'https://www.investing.com/{self.source_type}/{ticker}-historical-data'
        browser_options = Options()
        # browser_options.add_argument('--headless=new')
        browser = webdriver.Chrome(options=browser_options)
        browser.get(url)
        data_selector_element = (browser.find_element(By.CLASS_NAME, 'min-w-0')
                                 .find_elements(By.CLASS_NAME, 'shadow-select')[-1])
        data_selector_element.click()
        input_elements = browser.find_element(By.CLASS_NAME, 'min-w-0').find_elements(By.TAG_NAME, 'input')
        input_elements[0].send_keys('01/01/2001')
        # for date_picker in browser.find_elements(By.CSS_SELECTOR, 'div[class^="NativeDateInputV2"]'):
        #     date_picker.click()
        print('hi')

    def get_intraday_price(self, ticker: str) -> (str, [IntradayPrice]):
        raise NotImplementedError()

    def get_constituents(self) -> [str]:
        raise NotImplementedError()

InvestingDotComSourceStrategy('nikkei-mid-and-small-cap', source_type=InvestingDotComDataType.indices).get_daily_price('nikkei-mid-and-small-cap')