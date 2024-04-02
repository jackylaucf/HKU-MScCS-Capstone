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
              f'{self.strategies.index_price.get_source_name()}')
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
                    writer.writerow(dataclasses.asdict(row))
        else:
            print("Skip file export due to empty data")

    def fetch(self, data_type: MarketDataType = MarketDataType.ALL, save: bool = True, save_dir: str = None):
        constituents_tickers = self.get_constituents()
        if data_type in (MarketDataType.ALL, MarketDataType.INDEX_DAILY):
            self.get_index_daily_price(save=save, save_dir=save_dir)
        if data_type in (MarketDataType.ALL, MarketDataType.CONSTITUENTS_DAILY):
            for ticker in constituents_tickers:
                if ticker not in ('000250','000440','001000','001540','001810','001840','002230','002290','002680','002800','003100','003310','003380','003800','004590','004650','004780','005160','005290','005670','005710','005860','005990','006050','006140','006580','006620','006730','006910','006920','007330','007370','007390','007530','007680','007720','007770','007820','008290','008370','008470','008830','009300','009520','009620','009730','009780','010170','010240','010280','010470','011040','011080','011320','011370','011560','012340','012620','012700','012790','012860','013030','013120','013310','013720','013810','013990','014100','014190','014200','014470','014570','014620','014940','014970','015710','015750','016100','016250','016600','016670','016790','016920','017000','017250','017480','017510','017650','017890','018000','018120','018290','018310','018620','018680','018700','019010','019210','019540','019550'):
                    self.get_constituents_daily_price(ticker, save=save, save_dir=save_dir)
                    time.sleep(random.randint(1, 20))
