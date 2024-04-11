from crawler import http_utils
from crawler.strategy.SourceStrategy import SourceStrategy
from model.market_data import DailyPrice, IntradayPrice


class NSEIndiaSourceStrategy(SourceStrategy):

    def get_source_name(self) -> str:
        return 'NSE India'

    def get_daily_price(self, ticker: str) -> (str, [DailyPrice]):
        raise NotImplementedError

    def get_intraday_price(self, ticker: str) -> (str, [IntradayPrice]):
        raise NotImplementedError()

    def get_constituents(self) -> [str]:
        url = ('https://www.niftyindices.com/IndexConstituent/ind_{ticker}list.csv'
               .format(ticker=self.index_ticker))
        constituents = []
        response = http_utils.get(url)
        raw_data = response.text.split('\n')
        ticker_col = raw_data[0].split(',').index('Symbol')
        for row in raw_data[1:]:
            if row.strip():
                constituents.append(row.split(',')[ticker_col])
        return constituents
