from crawler.market_fetcher import FetcherStrategies, MarketFetcher, MarketDataType
from crawler.strategy.TradingViewSourceStrategy import TradingViewSourceStrategy
from crawler.strategy.YahooSourceStrategy import YahooSourceStrategy


# Hong Kong
def hsi():
    strategies = FetcherStrategies(index_price=YahooSourceStrategy('^HSI'),
                                   constituents=TradingViewSourceStrategy('HSI-HSI'),
                                   constituents_price=YahooSourceStrategy('^HSI',
                                                                          YahooSourceStrategy.get_ticker_formatter(
                                                                              suffix='.HK', zfill=4)))
    return MarketFetcher('hsi', strategies)


# India
def nifty_50():
    strategies = FetcherStrategies(index_price=YahooSourceStrategy('^NSEI'),
                                   constituents=TradingViewSourceStrategy('NSE-NIFTY'),
                                   constituents_price=YahooSourceStrategy('^NSEI',
                                                                          YahooSourceStrategy.get_ticker_formatter(
                                                                              suffix='.NS')))
    return MarketFetcher('nifty_50', strategies)


# KOREA
def kosdaq_composite():
    strategies = FetcherStrategies(index_price=YahooSourceStrategy('^KQ11'),
                                   constituents=TradingViewSourceStrategy('KRX-KOSDAQ'),
                                   constituents_price=YahooSourceStrategy('^KQ11',
                                                                          YahooSourceStrategy.get_ticker_formatter(
                                                                              suffix='.KQ', zfill=6)))
    return MarketFetcher('kosdaq_composite', strategies)


def kosdaq_150():
    strategies = FetcherStrategies(index_price=YahooSourceStrategy('229200.KS'),
                                   constituents=TradingViewSourceStrategy('KRX-KOSDAQ150'),
                                   constituents_price=YahooSourceStrategy('229200.KS',
                                                                          YahooSourceStrategy.get_ticker_formatter(
                                                                              suffix='.KQ', zfill=6)))
    return MarketFetcher('kosdaq_150', strategies)


# Japan
def nikkei_225():
    strategies = FetcherStrategies(index_price=YahooSourceStrategy('^N225'),
                                   constituents=TradingViewSourceStrategy('INDEX-NKY'),
                                   constituents_price=YahooSourceStrategy('^N225',
                                                                          YahooSourceStrategy.get_ticker_formatter(
                                                                              suffix='.T')))
    return MarketFetcher('nikkei_225', strategies)


# China
def sse_composite():
    strategies = FetcherStrategies(index_price=YahooSourceStrategy('000001.SS'),
                                   constituents=TradingViewSourceStrategy('SSE-000001'),
                                   constituents_price=YahooSourceStrategy('000001.SS',
                                                                          YahooSourceStrategy.get_ticker_formatter(
                                                                              suffix='.SS')))
    return MarketFetcher('sse_composite', strategies)


def szse_component():
    strategies = FetcherStrategies(index_price=YahooSourceStrategy('399001.SZ'),
                                   constituents=TradingViewSourceStrategy('SZSE-399001'),
                                   constituents_price=YahooSourceStrategy('399001.SZ',
                                                                          YahooSourceStrategy.get_ticker_formatter(
                                                                              suffix='.SZ', zfill=6)))
    return MarketFetcher('szse_component', strategies)


# Singapore
def ftse_sti():
    strategies = FetcherStrategies(index_price=YahooSourceStrategy('^STI'),
                                   constituents=TradingViewSourceStrategy('FTSEST-STI'),
                                   constituents_price=YahooSourceStrategy('^STI',
                                                                          YahooSourceStrategy.get_ticker_formatter(
                                                                              suffix='.SI')))
    return MarketFetcher('ftse_sti', strategies)


# Taiwan
# def tsec_weighted():
#     strategies = FetcherStrategies(index_price=YahooSourceStrategy('^TWII'),
#                                    constituents=TradingViewSourceStrategy('INDEX-NKY'),
#                                    constituents_price=YahooSourceStrategy('^TWII',
#                                                                           YahooSourceStrategy.get_ticker_formatter(
#                                                                               suffix='.T')))

if __name__ == '__main__':
    ftse_sti().fetch()
