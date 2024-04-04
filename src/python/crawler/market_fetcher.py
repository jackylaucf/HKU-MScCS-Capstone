import csv
import dataclasses
import os
import pathlib
import random
import time

from crawler.strategy import SourceStrategy
from enum import auto, StrEnum
from model.market_data import DailyPrice
from typing import List, NamedTuple


class FetcherStrategies(NamedTuple):
    index_price: SourceStrategy
    constituents: SourceStrategy
    constituents_price: SourceStrategy


class MarketDataType(StrEnum):
    ALL = auto()
    INDEX_DAILY = auto()
    INDEX_INTRADAY = auto()
    CONSTITUENTS_DAILY = auto()
    CONSTITUENTS_INTRADAY = auto()


class MarketFetcher:

    def __init__(self, index: str, strategies: FetcherStrategies):
        self.index = index
        self.strategies = strategies

    def get_constituents(self) -> [str]:
        constituents = self.strategies.constituents.get_constituents()
        print(f'Fetched {len(constituents)} ticker(s) from {self.strategies.constituents.get_source_name()}')
        return constituents

    def get_index_daily_price(self, save: bool = True, save_dir: str = None) -> [DailyPrice]:
        index_ticker = self.strategies.index_price.index_ticker
        _, daily_price = self.strategies.index_price.get_daily_price(index_ticker)
        print(f'Fetched {len(daily_price)} {index_ticker} daily price(s) from '
              f'{self.strategies.index_price.get_source_name()}')
        if save:
            self.export(daily_price, f'INDEX_DAILY_{self.index.upper()}.csv', file_dir=save_dir)
        return daily_price

    def get_index_intraday_price(self, save: bool = True, save_dir: str = None):
        pass

    def get_constituents_daily_price(self, ticker: str, save: bool = True, save_dir: str = None) -> [DailyPrice]:
        ticker, daily_price = self.strategies.constituents_price.get_daily_price(ticker)
        print(f'Fetched {len(daily_price)} {ticker} daily price(s) from '
              f'{self.strategies.constituents_price.get_source_name()}')
        if save:
            self.export(daily_price, f'CONSTITUENTS_DAILY_{ticker.upper()}.csv', file_dir=save_dir)
        return daily_price

    def get_constituents_intraday_price(self, ticker: str, save: bool = True, save_dir: str = None) -> [dict]:
        pass

    def export(self, data: List, file_name: str, file_dir: str = None):
        if data:
            file_path = pathlib.Path(file_dir or __file__).parents[1].joinpath(f'dataset/{self.index}/{file_name}')
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            headers = sorted(f.name for f in dataclasses.fields(data[0]))
            with open(file_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=headers)
                writer.writeheader()
                for row in data:
                    formatted_record = {k: ('null' if v is None else v) for k, v in dataclasses.asdict(row).items()}
                    writer.writerow(formatted_record)
        else:
            print("Skip file export due to empty data")

    def fetch(self, data_type: MarketDataType = MarketDataType.ALL, save: bool = True, save_dir: str = None):
        constituents_tickers = self.get_constituents()
        if data_type in (MarketDataType.ALL, MarketDataType.INDEX_DAILY):
            self.get_index_daily_price(save=save, save_dir=save_dir)
        if data_type in (MarketDataType.ALL, MarketDataType.CONSTITUENTS_DAILY):
            for ticker in constituents_tickers:
                self.get_constituents_daily_price(ticker, save=save, save_dir=save_dir)
                time.sleep(random.randint(1, 20))
