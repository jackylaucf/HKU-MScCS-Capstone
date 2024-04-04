import csv
import operator
import pathlib

from crawler.strategy.SourceStrategy import SourceStrategy
from model.market_data import DailyPrice, IntradayPrice


class ImportCsvSourceStrategy(SourceStrategy):

    def __init__(self, index_ticker: [str, None], source_date_format: str):
        super().__init__(index_ticker)
        self.source_date_format = source_date_format

    def get_source_name(self) -> str:
        return 'Manual Import'

    def get_daily_price(self, ticker: str) -> (str, [DailyPrice]):
        csv_path = pathlib.Path(__file__).parents[2].joinpath(f'resources/crawler/csv_input/{ticker}.csv')
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file, skipinitialspace=True)
            results = []
            for row in reader:
                results.append(DailyPrice.build(row, self.source_date_format))
            return ticker, sorted(results, key=lambda x: x.date)

    def get_intraday_price(self, ticker: str) -> (str, [IntradayPrice]):
        raise NotImplementedError()

    def get_constituents(self) -> [str]:
        raise NotImplementedError()
