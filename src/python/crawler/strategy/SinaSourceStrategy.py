import time

from bs4 import BeautifulSoup
from crawler.strategy.SourceStrategy import SourceStrategy
from model.market_data import DailyPrice, IntradayPrice
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class SinaSourceStrategy(SourceStrategy):

    def get_source_name(self) -> str:
        return 'Sina'

    def get_daily_price(self, ticker: str) -> (str, [DailyPrice]):
        raise NotImplementedError

    def get_intraday_price(self, ticker: str) -> (str, [IntradayPrice]):
        raise NotImplementedError()

    def get_constituents(self) -> [str]:
        url = ('http://vip.stock.finance.sina.com.cn/corp/go.php/vII_NewestComponent/indexid/{ticker}.phtml'
               .format(ticker=self.index_ticker))
        browser_options = Options()
        browser_options.add_argument('--headless=new')
        browser = webdriver.Chrome(options=browser_options)
        browser.get(url)
        constituents = []
        parsed_html = BeautifulSoup(browser.page_source, 'html.parser')
        table_element = parsed_html.find('table', {'id': 'NewStockTable'})
        while True:
            for table_row in table_element.find('tbody').findAll('tr')[1:]:
                href = table_row.find_all('td')[1].find('a')['href']
                sina_stock_code = href.split('/')[-2]
                exchange_code = sina_stock_code[:2].upper()
                if exchange_code == 'SH':
                    exchange_code = 'SS'
                constituents.append(f'{sina_stock_code[2:]}.{exchange_code}')
            try:
                next_button_element = browser.find_element(By.XPATH, '//a[text()="下一页"]')
                next_button_element.click()
                time.sleep(2)
            except NoSuchElementException:
                break
        return constituents


print(SinaSourceStrategy('399903').get_constituents())