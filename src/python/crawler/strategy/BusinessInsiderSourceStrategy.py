from crawler import http_utils
from crawler.strategy.SourceStrategy import SourceStrategy
from datetime import datetime
from model.market_data import DailyPrice, IntradayPrice


class BusinessInsiderSourceStrategy(SourceStrategy):

    def get_source_name(self) -> str:
        return 'Business Insider'

    def get_daily_price(self, ticker: str) -> (str, [DailyPrice]):
        valor, _, business_insider_code = ticker.partition(':')
        if not valor or not business_insider_code:
            raise ValueError('Ticker provided to Business Insider strategy should be in the format of '
                             '{valor_number}-{business_insider_code}')
        daily_prices = []
        url = (f'https://markets.businessinsider.com/ajax/Valor_HistoricPriceList/{valor}/Jan. 01 2000_Mar. 31 2024/'
               f'{business_insider_code}')
        response = http_utils.get(url)
        if response.ok:
            for row in response.json():
                daily_prices.append(
                    DailyPrice(
                        date=datetime.strptime(row['Date'], '%m/%d/%y').date().isoformat(),
                        open=str(row['Open']).replace(',', ''),
                        high=str(row['High']).replace(',', ''),
                        low=str(row['Low']).replace(',', ''),
                        close=str(row['Close']).replace(',', ''),
                        volume=str(row['Volume']).replace(',', '')))
        return valor, daily_prices

    def get_intraday_price(self, ticker: str) -> (str, [IntradayPrice]):
        raise NotImplementedError()

    def get_constituents(self) -> [str]:
        raise NotImplementedError()
