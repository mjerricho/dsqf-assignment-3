"""
This module is responsible for testing the functions that fetch stock data.
"""
import sys
import unittest
from datetime import datetime
from src.stocks_fetcher import StocksFetcher, DATE_FORMAT

sys.path.append("/.../src")

class TestStocksFetcher(unittest.TestCase):
  """
  Defines the TestStocksFetcher class which tests the StocksFetcher class.
  """
  def test_fetch_stock_data(self):
    """
    Tests the fetch_stock_data method.
    """
    start = datetime.strptime("20230306", DATE_FORMAT)
    end = datetime.strptime("20230310", DATE_FORMAT)
    ticker_str = "MSFT"
    stocks_fetcher = StocksFetcher()
    res = stocks_fetcher.fetch_stock_data(ticker_str, start, end)
    self.assertTrue(len(res) == 4)

  def test_fetch_stocks_data_single_ticker(self):
    """
    Tests the fetch_stocks_data method with a single ticker.
    """
    start_str = "20230301"
    end_str = "20230302"
    ticker = "AAPL"
    tickers_str = [ticker]
    stocks_fetcher = StocksFetcher()
    res = stocks_fetcher.fetch_stocks_data(tickers_str, start_str, end_str)
    self.assertFalse(res[ticker].empty)
    self.assertTrue(len(res[ticker].index) > 250)
    self.assertEqual(res[ticker].index[-1].strftime(DATE_FORMAT), end_str)

  def test_fetch_stocks_data_multiple_tickers(self):
    """
    Tests the fetch_stocks_data method with multiple tickers.
    """
    start_str = "20230202"
    end_str = "20230302"
    ticker_1 = "AAPL"
    ticker_2 = "GOOGL"
    tickers_str = [ticker_1, ticker_2]
    stocks_fetcher = StocksFetcher()
    res = stocks_fetcher.fetch_stocks_data(tickers_str, start_str, end_str)
    self.assertFalse(res[ticker_1].empty)
    self.assertFalse(res[ticker_2].empty)
    self.assertEqual(len(res), 2)
