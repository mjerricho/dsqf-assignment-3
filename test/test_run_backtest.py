"""
This module is responsible for testing the functions that simulate
the backtest
"""
import sys
import unittest
from src.stocks_fetcher import StocksFetcher, DATE_FORMAT
from backtest import RunBacktest, MOMENTUM, REVERSAL, CLOSE_PRICE
from random import randint

sys.path.append("/.../src")

class TestRunBacktest(unittest.TestCase):
  """
  Defines the TestRunBacktest class which tests the RunBacktest class.
  """
  # StockFetcher parameters
  start_str = "20230117"
  end_str = "20230302"
  ticker_1 = "AAPL"
  ticker_2 = "GOOGL"
  ticker_3 = "MSFT"
  ticker_4 = "NFLX"
  ticker_5 = "META"
  tickers_str = [ticker_1, ticker_2, ticker_3, ticker_4, ticker_5]
  ticker_obj = StocksFetcher()
  stocks_data = ticker_obj.fetch_stocks_data(tickers_str, start_str, end_str)

  # RunBacktest parameters
  initial_aum = 10000
  days = 20
  top_pct = 40

  def init_run_backtest(self, strategy: str):
    """
    Tests the RunBacktest class instantiation.
    """
    return RunBacktest(
      self.stocks_data,
      self.initial_aum,
      self.start_str,
      self.days,
      strategy,
      self.top_pct)

  def test_month_end_indexes_in_range(self):
    """
    Tests the get_month_end_indexes_from_b method.
    """
    run_backtest = self.init_run_backtest(MOMENTUM)
    month_end_indexes = run_backtest.get_month_end_indexes_from_b()
    self.assertEqual(len(month_end_indexes), 2)
    date_indexes = self.stocks_data[self.ticker_1].index
    first_month_end = date_indexes[month_end_indexes[0]].strftime(DATE_FORMAT)
    self.assertEqual(first_month_end, "20230131")
    second_month_end = date_indexes[month_end_indexes[1]].strftime(DATE_FORMAT)
    self.assertEqual(second_month_end, "20230228")

  def test_calc_stocks_to_buy_m(self):
    """
    Tests the calc_stocks_to_buy method for momentum.
    """
    run_backtest = self.init_run_backtest(MOMENTUM)
    first_month_end_index = run_backtest.get_month_end_indexes_from_b()[0]
    num_stocks_to_buy = int(len(self.tickers_str) * self.top_pct / 100)
    stocks_to_buy_m = run_backtest.calc_stocks_to_buy(first_month_end_index)
    self.assertEqual(len(stocks_to_buy_m), num_stocks_to_buy)
    self.assertTrue(self.ticker_3 in stocks_to_buy_m \
                    and self.ticker_5 in stocks_to_buy_m)

  def test_calc_stocks_to_buy_r(self):
    """
    Tests the calc_stocks_to_buy method for reversal.
    """
    run_backtest = self.init_run_backtest(REVERSAL)
    first_month_end_index = run_backtest.get_month_end_indexes_from_b()[0]
    num_stocks_to_buy = int(len(self.tickers_str) * self.top_pct / 100)
    stocks_to_buy_r = run_backtest.calc_stocks_to_buy(first_month_end_index)
    self.assertEqual(len(stocks_to_buy_r), num_stocks_to_buy)
    self.assertTrue(self.ticker_1 in stocks_to_buy_r \
                    and self.ticker_3 in stocks_to_buy_r)

  def test_calc_portfolio_first_positioning_m(self):
    """
    Tests the calc_stocks_to_buy and calc_portfolio methods for momentum.
    """
    run_backtest = self.init_run_backtest(MOMENTUM)
    first_month_end_index = run_backtest.get_month_end_indexes_from_b()[0]
    stocks_to_buy_m = run_backtest.calc_stocks_to_buy(first_month_end_index)
    new_portfolio = run_backtest.calc_portfolio(stocks_to_buy_m,
                                                self.initial_aum,
                                                first_month_end_index)
    total_aum = 0
    for stock, amount in new_portfolio:
      total_aum += \
        self.stocks_data[stock].iloc[first_month_end_index][CLOSE_PRICE] \
          * amount
    self.assertEqual(int(total_aum), self.initial_aum)

  def test_calc_portfolio_first_positioning_r(self):
    """
    Tests the calc_stocks_to_buy and calc_portfolio methods for reversal.
    """
    run_backtest = self.init_run_backtest(REVERSAL)
    first_month_end_index = run_backtest.get_month_end_indexes_from_b()[0]
    stocks_to_buy_r = run_backtest.calc_stocks_to_buy(first_month_end_index)
    new_portfolio = run_backtest.calc_portfolio(stocks_to_buy_r,
                                                self.initial_aum,
                                                first_month_end_index)
    total_aum = 0
    for stock, amount in new_portfolio:
      total_aum += \
        self.stocks_data[stock].iloc[first_month_end_index][CLOSE_PRICE] \
          * amount
    self.assertEqual(int(total_aum), self.initial_aum)

  def test_init_portfolio_performance(self):
    """
    Tests the init_portfolio_performance and portfolio_performance methods.
    """
    run_backtest = self.init_run_backtest(MOMENTUM)
    run_backtest.init_portfolio_performance()
    portfolio_performance_len = len(run_backtest.portfolio_performance)
    self.assertEqual(portfolio_performance_len, \
                     len(self.stocks_data[self.ticker_1]))
    self.assertEqual(\
      run_backtest.portfolio_performance.at[\
      randint(0, portfolio_performance_len - 1), "aum"], self.initial_aum)

  def test_calc_aum_first_positioning(self):
    """
    Tests the calc_aum method.
    """
    run_backtest = self.init_run_backtest(MOMENTUM)
    first_month_end_index = run_backtest.get_month_end_indexes_from_b()[0]
    stocks_to_buy_m = run_backtest.calc_stocks_to_buy(first_month_end_index)
    run_backtest.portfolio = run_backtest.calc_portfolio(stocks_to_buy_m,
                                                         self.initial_aum,
                                                         first_month_end_index)
    self.assertEqual(run_backtest.calc_aum(first_month_end_index),
                     self.initial_aum)

  def test_calc_aum_day_after_first_positioning(self):
    """
    Tests the calc_aum method.
    """
    run_backtest = self.init_run_backtest(MOMENTUM)
    first_month_end_index = run_backtest.get_month_end_indexes_from_b()[0]
    stocks_to_buy_m = run_backtest.calc_stocks_to_buy(first_month_end_index)
    run_backtest.portfolio = run_backtest.calc_portfolio(stocks_to_buy_m,
                                                         self.initial_aum,
                                                         first_month_end_index)
    self.assertAlmostEqual(run_backtest.calc_aum(first_month_end_index + 1),
                           10238.9627300)

  def test_calc_dividends_0(self):
    """
    Tests the calc_dividends method.
    """
    run_backtest = self.init_run_backtest(MOMENTUM)
    first_month_end_index = run_backtest.get_month_end_indexes_from_b()[0]
    stocks_to_buy_m = run_backtest.calc_stocks_to_buy(first_month_end_index)
    run_backtest.portfolio = run_backtest.calc_portfolio(stocks_to_buy_m,
                                                         self.initial_aum,
                                                         first_month_end_index)
    self.assertEqual(run_backtest.calc_dividends(first_month_end_index), 0)

  def test_calc_dividends_not_0(self):
    """
    Tests the calc_dividends method.
    """
    run_backtest = self.init_run_backtest(MOMENTUM)
    msft_stocks_owned = 20
    run_backtest.portfolio = [(self.ticker_3, msft_stocks_owned)]
    # based on dividend earned on 2023-02-15 00:00:00-05:00
    self.assertEqual(run_backtest.calc_dividends(314), msft_stocks_owned * 0.68)

  def test_fill_up_portfolio_performance_on_second_position_dates_m(self):
    """
    Tests the fill_up_portfolio_performance method.
    """
    run_backtest_auto = self.init_run_backtest(MOMENTUM)
    run_backtest_auto.fill_up_portfolio_performance()

    run_backtest_manual = self.init_run_backtest(MOMENTUM)
    month_end_indexes = run_backtest_manual.get_month_end_indexes_from_b()
    first_month_end_index = month_end_indexes[0]
    first_pos_stocks_to_buy_m = \
      run_backtest_manual.calc_stocks_to_buy(first_month_end_index)
    run_backtest_manual.portfolio = \
      run_backtest_manual.calc_portfolio(first_pos_stocks_to_buy_m,
                                         self.initial_aum,
                                         first_month_end_index)

    second_month_end_index = month_end_indexes[1]
    previous_aum = run_backtest_manual.calc_aum(second_month_end_index - 1)
    second_pos_stocks_to_buy_m = \
      run_backtest_manual.calc_stocks_to_buy(second_month_end_index)
    run_backtest_manual.portfolio = \
      run_backtest_manual.calc_portfolio(second_pos_stocks_to_buy_m,
                                         previous_aum,
                                         second_month_end_index)
    res_second_month_end_index_aum = \
      run_backtest_manual.calc_aum(second_month_end_index)
    # comparing aum
    res_auto = run_backtest_auto.portfolio_performance.at[29, "aum"]
    self.assertAlmostEqual(res_auto, res_second_month_end_index_aum)
    self.assertAlmostEqual(res_auto, 10750.4649708)

  def test_fill_up_portfolio_performance_end_m(self):
    """
    Tests the fill_up_portfolio_performance method for momentum.
    """
    run_backtest = self.init_run_backtest(MOMENTUM)
    run_backtest.fill_up_portfolio_performance()
    last_index = len(run_backtest.portfolio_performance) - 1
    self.assertAlmostEqual(\
      run_backtest.portfolio_performance.at[last_index, "aum"], 10566.8301891)

  def test_fill_up_portfolio_performance_end_r(self):
    """
    Tests the fill_up_portfolio_performance method for reversal.
    """
    run_backtest = self.init_run_backtest(REVERSAL)
    run_backtest.fill_up_portfolio_performance()
    last_index = len(run_backtest.portfolio_performance) - 1
    self.assertAlmostEqual(\
      run_backtest.portfolio_performance.at[last_index, "aum"], 10141.2860640)

  start_str_calc_ic = "20221217"
  stocks_data_calc_ic = ticker_obj.fetch_stocks_data(tickers_str,
                                                     start_str_calc_ic,
                                                     end_str)
  top_pct_calc_ic = 80

  def init_run_backtest_calc_ic(self, strategy: str):
    """
    Tests the RunBacktest class instantiation.
    """
    return RunBacktest(
      self.stocks_data,
      self.initial_aum,
      self.start_str_calc_ic,
      self.days,
      strategy,
      self.top_pct_calc_ic)

  def test_calc_ic_m(self):
    """
    Tests the calc_ic method for momentum.
    """
    run_backtest = self.init_run_backtest_calc_ic(MOMENTUM)
    run_backtest.fill_up_portfolio_performance()
    run_backtest.calc_ic()
    self.assertEqual(run_backtest.monthly_ic.at[0, "ic"], 1)
    self.assertEqual(run_backtest.monthly_ic.at[1, "ic"], 1.5)

  def test_calc_ic_r(self):
    """
    Tests the calc_ic method for reversal.
    """
    run_backtest = self.init_run_backtest_calc_ic(REVERSAL)
    run_backtest.fill_up_portfolio_performance()
    run_backtest.calc_ic()
    self.assertEqual(run_backtest.monthly_ic.at[0, "ic"], 1)
    self.assertEqual(run_backtest.monthly_ic.at[1, "ic"], 1)


