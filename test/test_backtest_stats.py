"""
This module is responsible for testing the functions that calculate
backtest statistics.
"""
import sys
import unittest
import pytest
import os.path
from datetime import date
from src.stocks_fetcher import StocksFetcher
from backtest import RunBacktest, MOMENTUM
from src.backtest_stats import BacktestStats

sys.path.append("/.../src")

class TestBacktestStats(unittest.TestCase):
  """
  Defines the TestBacktestStats class which tests the BacktestStats class.
  """
  # StockFetcher parameters
  start_str = "20201217"
  end_str = "20210302"
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

  def init_backtest_stats(self):
    """
    Tests the BacktestStats class instantiation.
    """
    run_backtest = RunBacktest(
      self.stocks_data,
      self.initial_aum,
      self.start_str,
      self.days,
      MOMENTUM,
      self.top_pct)
    run_backtest.fill_up_portfolio_performance()
    run_backtest.calc_ic()

    return BacktestStats(
      run_backtest.portfolio_performance,
      run_backtest.monthly_ic)

  def test_get_beginning_trading_date_str(self):
    """
    Tests the get_beginning_trading_date_str method.
    """
    bts = self.init_backtest_stats()
    self.assertEqual(bts.get_beginning_trading_date_str(),
                     "17/12/2020")

  def test_get_ending_trading_date_str(self):
    """
    Tests the get_ending_trading_date_str method.
    """
    bts = self.init_backtest_stats()
    self.assertEqual(bts.get_ending_trading_date_str(),
                     "02/03/2021")

  def test_get_number_days(self):
    """
    Tests the get_number_of_days method.
    """
    bts = self.init_backtest_stats()
    beginning_trading_date = date(2020, 12, 17)
    ending_trading_date = date(2021, 3, 2)
    diff = ending_trading_date - beginning_trading_date
    self.assertEqual(bts.get_number_of_days(), diff.days)

  def test_get_initial_aum(self):
    """
    Tests the get_initial_aum method.
    """
    bts = self.init_backtest_stats()
    self.assertEqual(bts.get_initial_aum(), self.initial_aum)

  def test_get_final_aum(self):
    """
    Tests the get_final_aum method.
    """
    bts = self.init_backtest_stats()
    self.assertAlmostEqual(bts.get_final_aum(), 10305.45637, 2)

  def test_get_profit_loss(self):
    """
    Tests the get_profit_loss method.
    """
    bts = self.init_backtest_stats()
    self.assertAlmostEqual(bts.get_profit_loss(), 313.68406, 2)

  def test_get_total_stock_return(self):
    """
    Tests the get_total_stock_return method.
    """
    bts = self.init_backtest_stats()
    self.assertAlmostEqual(bts.get_total_stock_return(), 0.03055, 3)

  def test_get_total_return(self):
    """
    Tests the get_total_return method.
    """
    bts = self.init_backtest_stats()
    self.assertAlmostEqual(bts.get_total_return(), 0.03137, 3)

  def test_get_annualized_rate_of_return(self):
    """
    Tests the get_annualized_rate_of_return method.
    """
    bts = self.init_backtest_stats()
    self.assertAlmostEqual(bts.get_annualized_rate_of_return(), 0.16220, 3)

  def test_get_average_daily_aum(self):
    """
    Tests the get_average_daily_aum method.
    """
    bts = self.init_backtest_stats()
    self.assertAlmostEqual(bts.get_average_daily_aum(), 10306.71087, 2)

  def test_get_maximum_daily_aum(self):
    """
    Tests the get_maximum_daily_aum method.
    """
    bts = self.init_backtest_stats()
    self.assertAlmostEqual(bts.get_maximum_daily_aum(), 10902.82288, 2)

  def test_get_daily_returns(self):
    """
    Tests the get_daily_returns method.
    """
    bts = self.init_backtest_stats()
    dr = [-0.029640397582960193, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
          -0.019922489837307693, -0.009922241610900164, -0.011749927582867048,
          0.009537970135655426, 0.04327931329369445, -0.01246580376766709,
          -0.029172021587267154, 0.004678976684473441, -0.001470585128347106,
          -0.019896438726364568, 0.011441158035954191, 0.06370494885844678,
          0.06308392797820443, 0.02910548937188815, 0.02438827515572276,
          0.018612059233934584, -0.022923957235919053, -0.03551727576720656,
          -0.008493492599531775, 0.014505609856717916, 0.02629137486387206,
          -0.0003674471774606418, 0.012521128160366908, 0.021801336006444957,
          -0.004836327673704285, 0.004757795014086287, 0.008653537336325725,
          -0.0045422098229200404, -0.006438489640713136, -0.007383824429011465,
          -0.021281181164778423, -0.02110660948144507, -0.013925446006276805,
          -0.027445571084428095, -0.009645725385907305, 0.016304394560859244,
          -0.018135447824884576, -0.02295198250639831, 0.021619686633503114,
          0.013733150610690529]
    for exp, act in zip(bts.get_daily_returns(), dr):
      self.assertAlmostEqual(exp, act, 3)

  def test_get_average_daily_return(self):
    """
    Tests the get_average_daily_return method.
    """
    bts = self.init_backtest_stats()
    self.assertAlmostEqual(bts.get_average_daily_return(), 0.0009956, 2)

  def test_get_daily_standard_deviation(self):
    """
    Tests the get_daily_standard_deviation method.
    """
    bts = self.init_backtest_stats()
    self.assertAlmostEqual(bts.get_daily_standard_deviation(), 0.0212649, 2)

  def test_get_daily_sharpe_ratio(self):
    """
    Tests the get_daily_sharpe_ratio method.
    """
    bts = self.init_backtest_stats()
    self.assertAlmostEqual(bts.get_daily_sharpe_ratio(), 0.04212, 2)

  # Allows us to capture printing to standard output
  @pytest.fixture(autouse=True)
  def capsys(self, capsys):
    self.capsys = capsys

  def test_print_summary(self):
    """Tests the print_summary method."""
    out_str = """
    Begin Date: 17/12/2020
    End Date: 02/03/2021
    Number of Days: 75
    Total Stock Return: 3.055%
    Total Return: 3.137%
    Annualized Rate of Return: 16.220%
    Initial AUM: 10000.00000
    Final AUM: 10305.45721
    Average Daily AUM: 10306.71195
    Maximum Daily AUM: 10902.82411
    Profit and Loss: 313.68634
    Average Daily Return: 0.09956%
    Daily Standard Deviation: 2.12649%
    Daily Sharpe Ratio: 0.04212
    
"""
    bts = self.init_backtest_stats()
    bts.print_summary()
    captured = self.capsys.readouterr()
    assert len(captured.out) == len(out_str)

  def test_plot_daily_aum(self):
    """
    Tests the plot_daily_aum method.
    """
    bts = self.init_backtest_stats()
    bts.plot_daily_aum()
    parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    expected_path = os.path.join(parent_dir, "daily_aum.png")
    self.assertTrue(os.path.isfile(expected_path))

  def test_plot_monthly_cumulative_ic(self):
    """
    Tests the plot_monthly_cumulative_ic method.
    """
    bts = self.init_backtest_stats()
    bts.plot_monthly_cumulative_ic()
    parent_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    expected_path = os.path.join(parent_dir, "cumulative_ic.png")
    self.assertTrue(os.path.isfile(expected_path))
