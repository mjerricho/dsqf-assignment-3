"""
This module is responsible for testing the functions that validate
and organise user input.
"""

import sys
from src.input_data import InputData, get_args, DATE_TODAY
import unittest
from unittest.mock import patch
from datetime import datetime
from typing import List, Tuple
import os.path

sys.path.append("/.../src")


class TestInputData(unittest.TestCase):
  """
  Defines the TestInputData class which tests the functions that validate
  and organise user input.
  """

  def setUp(self):
    self.sample_tickers = "AAPL,GOOGL,MSFT"
    self.sample_b = 20200101
    self.sample_e = 20201231
    self.sample_initial_aum = 10000
    self.sample_strategy1_type = "M"
    self.sample_strategy2_type = "R"
    self.sample_days1 = 30
    self.sample_days2 = 60
    self.sample_top_pct = 10

    self.input_data = InputData(
        tickers=self.sample_tickers,
        b=self.sample_b,
        e=self.sample_e,
        initial_aum=self.sample_initial_aum,
        strategy1_type=self.sample_strategy1_type,
        strategy2_type=self.sample_strategy2_type,
        days1=self.sample_days1,
        days2=self.sample_days2,
        top_pct=self.sample_top_pct
    )

  def test_get_tickers(self):
    result = self.input_data.get_tickers()
    expected = ["AAPL", "GOOGL", "MSFT"]
    self.assertEqual(result, expected)

    self.input_data.tickers = "AAPL ,GOOGL, MSFT"
    result = self.input_data.get_tickers()
    self.assertEqual(result, expected)

    with self.assertRaises(ValueError):
      self.input_data.tickers = None
      self.input_data.get_tickers()

    with self.assertRaises(ValueError):
      self.input_data.tickers = 123
      self.input_data.get_tickers()

    with self.assertRaises(ValueError):
      self.input_data.tickers = "AAPL,GOOGL,MSFT#"
      self.input_data.get_tickers()

    with self.assertRaises(ValueError):
      self.input_data.tickers = "AAPL,GOOGL,MSFTTT"
      self.input_data.get_tickers()

  def test_get_beginning_date(self):
    result = self.input_data.get_beginning_date()
    expected = "20200101"
    self.assertEqual(result, expected)

    with self.assertRaises(ValueError):
      self.input_data.b = None
      self.input_data.get_beginning_date()

    with self.assertRaises(ValueError):
      self.input_data.b = "20200101"
      self.input_data.get_beginning_date()

    with self.assertRaises(ValueError):
      self.input_data.b = 202001
      self.input_data.get_beginning_date()

    with self.assertRaises(ValueError):
      self.input_data.b = int(DATE_TODAY) + 1
      self.input_data.get_beginning_date()

  def test_get_ending_date(self):
    result = self.input_data.get_ending_date()
    expected = "20201231"
    self.assertEqual(result, expected)

    self.input_data.e = None
    result = self.input_data.get_ending_date()
    self.assertEqual(result, DATE_TODAY)

    with self.assertRaises(ValueError):
      self.input_data.e = "20201231"
      self.input_data.get_ending_date()

    with self.assertRaises(ValueError):
      self.input_data.e = 202012
      self.input_data.get_ending_date()

    with self.assertRaises(ValueError):
      self.input_data.e = self.sample_b - 1
      self.input_data.get_ending_date()

    with self.assertRaises(ValueError):
      self.input_data.e = int(DATE_TODAY) + 1
      self.input_data.get_ending_date()

  def test_get_initial_aum(self):
    result = self.input_data.get_initial_aum()
    expected = 10000
    self.assertEqual(result, expected)

    with self.assertRaises(ValueError):
      self.input_data.initial_aum = None
      self.input_data.get_initial_aum()

    with self.assertRaises(ValueError):
      self.input_data.initial_aum = "10000"
      self.input_data.get_initial_aum()

    with self.assertRaises(ValueError):
      self.input_data.initial_aum = -10000
      self.input_data.get_initial_aum()

  def test_get_top_pct(self):
    result = self.input_data.get_top_pct()
    expected = 10
    self.assertEqual(result, expected)

    with self.assertRaises(ValueError):
      self.input_data.top_pct = None
      self.input_data.get_top_pct()

    with self.assertRaises(ValueError):
      self.input_data.top_pct = "10"
      self.input_data.get_top_pct()

    with self.assertRaises(ValueError):
      self.input_data.top_pct = 0
      self.input_data.get_top_pct()

    with self.assertRaises(ValueError):
      self.input_data.top_pct = 101
      self.input_data.get_top_pct()

  def test_get_strategy_and_days(self):
    result1 = self.input_data.get_strategy_and_days(1)
    expected1 = ("M", 30)
    self.assertEqual(result1, expected1)

    result2 = self.input_data.get_strategy_and_days(2)
    expected2 = ("R", 60)
    self.assertEqual(result2, expected2)

    with self.assertRaises(ValueError):
      self.input_data.get_strategy_and_days(3)

    with self.assertRaises(ValueError):
      self.input_data.strategy1_type = None
      self.input_data.get_strategy_and_days(1)

    with self.assertRaises(ValueError):
      self.input_data.strategy1_type = "X"
      self.input_data.get_strategy_and_days(1)

    with self.assertRaises(ValueError):
      self.input_data.days1 = None
      self.input_data.get_strategy_and_days(1)

    with self.assertRaises(ValueError):
      self.input_data.days1 = "30"
      self.input_data.get_strategy_and_days(1)

    with self.assertRaises(ValueError):
      self.input_data.days1 = 0
      self.input_data.get_strategy_and_days(1)

    with self.assertRaises(ValueError):
      self.input_data.days1 = 251
      self.input_data.get_strategy_and_days(1)

  def test_get_normal_args(self):
    """
    Tests the get_args method with normal input.
    """
    test_args = [
        "--tickers", "AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,META,WMT,MCD",
        "--b", "20220101",
        "--e", "20230318",
        "--initial_aum", "10000",
        "--strategy_type", "M",
        "--days", "100",
        "--top_pct", "20"
    ]

    with patch.object(sys, "argv", [""] + test_args):
      args = get_args()
      self.assertEqual(args.tickers,
       "AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,META,WMT,MCD")
      self.assertEqual(args.b, 20220101)
      self.assertEqual(args.e, 20230318)
      self.assertEqual(args.initial_aum, 10000)
      self.assertEqual(args.strategy_type, "M")
      self.assertEqual(args.days, 100)
      self.assertEqual(args.top_pct, 20)

  def test_missing_args(self):
    """
    Tests the get_args method with missing input.
    """
    test_args = []

    with patch.object(sys, "argv", [""] + test_args):
      with self.assertRaises(SystemExit):
        get_args()

  def test_wrong_args(self):
    """
    Tests the get_args method with wrong input.
    """
    test_args = [
        "--tickers", "AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,HAHAHHAAH,WMT,MCD",
        "--b", "jjj222",
        "--e", "82j23i2",
        "--initial_aum", "alsms12",
        "--strategy_type", "A",
        "--days", "aslkdmamdkj123311",
        "--top_pct", "l12i2s",
        "--wrong-stuff"
    ]

    with patch.object(sys, "argv", [""] + test_args):
      with self.assertRaises(SystemExit):
        get_args()
