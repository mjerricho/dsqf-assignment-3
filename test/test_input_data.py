"""
This module is responsible for testing the functions that validate
and organise user input.
"""
import sys
import unittest
from src.input_data import InputData, get_args, DATE_TODAY

sys.path.append("/.../src")

class TestInputData(unittest.TestCase):
  """ 
  Defines the TestInputData class which tests the InputData class.
  """
  def test_get_normal_args(self) -> None:
    """
    Tests the get_args method with normal input.
    """
    parser = get_args()
    args = parser.parse_args(["--tickers",
      "AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,META,WMT,MCD", "--b", "20220101",
      "--e", "20230318", "--initial_aum", "10000", "--strategy_type", "M",
      "--days", "100", "--top_pct", "20"])
    self.assertEqual(args.tickers,
      "AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,META,WMT,MCD")
    self.assertEqual(args.b, 20220101)
    self.assertEqual(args.e, 20230318)
    self.assertEqual(args.initial_aum, 10000)
    self.assertEqual(args.strategy_type, "M")
    self.assertEqual(args.days, 100)
    self.assertEqual(args.top_pct, 20)

  def test_missing_args(self) -> None:
    """
    Tests the get_args method with missing input.
    """
    parser = get_args()
    self.assertRaises(SystemExit, parser.parse_args, [])

  def test_wrong_args(self) -> None:
    """
    Tests the get_args method with wrong input.
    """
    parser = get_args()
    self.assertRaises(SystemExit, parser.parse_args, ["--tickers",
      "AAPL,TSLA,LMT,BA,GOOG,AMZN,NVDA,HAHAHHAAH,WMT,MCD", "--b", "jjj222",
      "--e", "82j23i2", "--initial_aum", "alsms12", "--strategy_type", "A",
      "--days", "aslkdmamdkj123311", "--top_pct", "l12i2s", "--wrong-stuff"])

  def test_get_tickers_valid(self):
    """
    Tests the get_tickers method with valid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    expected_tickers = ["MSFT", "AMZN", "WMT"]
    self.assertEqual(input_data.get_tickers(), expected_tickers)

  def test_get_tickers_invalid_empty(self):
    """
    Tests the get_tickers method with missing input.
    """
    input_data = InputData(
      tickers="",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_tickers()
    self.assertEqual(str(cm.exception),
      "Ticker must be a string of alphanumeric characters.")

  def test_get_tickers_invalid_non_alphanumeric(self):
    """
    Tests the get_tickers method with invalid characters.
    """
    input_data = InputData(
      tickers="MSFT,AM@N,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_tickers()
    self.assertEqual(str(cm.exception),
      "Ticker must be a string of alphanumeric characters.")

  def test_get_tickers_invalid_length(self):
    """
    Tests the get_tickers method with invalid length.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT,VERYLONG",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_tickers()
    self.assertEqual(str(cm.exception),
      "Ticker must be between 1 to 5 characters long.")

  def test_get_beginning_date_valid(self):
    """
    Tests the get_beginning_date method with valid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    self.assertEqual(input_data.get_beginning_date(), "20220101")

  def test_get_beginning_date_invalid(self):
    """
    Tests the get_beginning_date method with invalid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b="jkqheiuh21231",
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_beginning_date()
    self.assertEqual(str(cm.exception), "Beginning date must be an integer.")

  def test_get_beginning_date_must_be_specified(self):
    """
    Tests the get_beginning_date method with missing input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=None,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_beginning_date()
    self.assertEqual(str(cm.exception),
      "Beginning date must be specified")

  def test_get_beginning_date_invalid_integer(self):
    """
    Tests the get_beginning_date method with invalid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b="haha",
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_beginning_date()
    self.assertEqual(str(cm.exception),
      "Beginning date must be an integer.")

  def test_get_beginning_date_invalid_length(self):
    """
    Tests the get_beginning_date method with invalid length.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=202201011,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_beginning_date()
    self.assertEqual(str(cm.exception),
      "Beginning date must be in format YYYYMMDD.")

  def test_ending_date_before_beginning_date(self):
    """
    Tests the get_ending_date method being before beginningn date.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20230301,
      e=20220101,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_ending_date()
    self.assertEqual(str(cm.exception),
      "Ending date must be greater than or equal to the beginning date.")

  def test_get_ending_date_default(self) -> None:
    """
    Tests the get_ending_date method when it is not provided.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=None,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    self.assertEqual(input_data.get_ending_date(), DATE_TODAY)

  def test_get_ending_date_valid(self):
    """
    Tests the get_ending_date method with valid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20230301,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    self.assertEqual(input_data.get_ending_date(), "20230318")

  def test_get_ending_date_invalid(self):
    """
    Tests the get_ending_date method with invalid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e="alsjdajdjadjq2313123213",
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_ending_date()
    self.assertEqual(str(cm.exception),
      "Ending date must be in format YYYYMMDD.")

  def test_get_initial_aum_valid(self):
    """
    Tests the get_initial_aum method with valid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    self.assertEqual(input_data.get_initial_aum(), 10000)

  def test_get_initial_aum_invalid(self):
    """
    Tests the get_initial_aum method with invalid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=-100,
      strategy_type="M",
      days=100,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_initial_aum()
    self.assertEqual(str(cm.exception),
      "Initial AUM must be a positive integer.")

  def test_get_initial_aum_invalid_2(self):
    """
    Tests the get_initial_aum method with invalid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum="ahah",
      strategy_type="M",
      days=100,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_initial_aum()
    self.assertEqual(str(cm.exception),
      "Initial AUM must be an integer.")

  def test_get_initial_aum_invalid_3(self):
    """
    Tests the get_initial_aum method with invalid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=None,
      strategy_type="M",
      days=100,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_initial_aum()
    self.assertEqual(str(cm.exception),
      "Initial AUM must be specified.")

  def test_get_strategy_type_valid(self):
    """
    Tests the get_strategy_type method with valid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    self.assertEqual(input_data.get_strategy_type(), "M")

  def test_get_strategy_type_invalid(self):
    """
    Tests the get_strategy_type method with invalid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="A",
      days=100,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_strategy_type()
    self.assertEqual(str(cm.exception),
      "Strategy type must be 'M' (momentum) or 'R' (reversal).")

  def test_get_strategy_type_invalid_2(self):
    """
    Tests the get_strategy_type method with invalid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type=None,
      days=100,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_strategy_type()
    self.assertEqual(str(cm.exception),
      "Strategy type must be a string.")

  def test_get_strategy_type_invalid_3(self):
    """
    Tests the get_strategy_type method with invalid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type=1,
      days=100,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_strategy_type()
    self.assertEqual(str(cm.exception),
      "Strategy type must be a string.")

  def test_get_days_valid(self):
    """
    Tests the get_days method with valid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    self.assertEqual(input_data.get_days(), 100)

  def test_get_days_invalid(self):
    """
    Tests the get_days method with invalid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=251,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_days()
    self.assertEqual(str(cm.exception),
      "Number of trading days must be between 1 to 250.")

  def test_get_days_invalid_2(self):
    """
    Tests the get_days method with invalid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=0,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_days()
    self.assertEqual(str(cm.exception),
      "Number of trading days must be between 1 to 250.")

  def test_get_days_invalid_3(self):
    """
    Tests the get_days method with invalid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days="haha",
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_days()
    self.assertEqual(str(cm.exception),
      "Number of trading days must be an integer.")

  def test_get_days_invalid_4(self):
    """
    Tests the get_days method with invalid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=None,
      top_pct=20)
    with self.assertRaises(ValueError) as cm:
      input_data.get_days()
    self.assertEqual(str(cm.exception),
      "Number of trading days must be specified.")

  def test_get_top_pct_valid(self):
    """
    Tests the get_top_pct method with valid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=20)
    self.assertEqual(input_data.get_top_pct(), 20)

  def test_get_top_pct_invalid(self):
    """
    Tests the get_top_pct method with invalid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=-100)
    with self.assertRaises(ValueError) as cm:
      input_data.get_top_pct()
    self.assertEqual(str(cm.exception),
      "Top percentage must be between 1 to 100.")

  def test_get_top_pct_invalid_3(self):
    """
    Tests the get_top_pct method with invalid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct="haha")
    with self.assertRaises(ValueError) as cm:
      input_data.get_top_pct()
    self.assertEqual(str(cm.exception),
      "Top percentage must be an integer.")

  def test_get_top_pct_invalid_4(self):
    """
    Tests the get_top_pct method with invalid input.
    """
    input_data = InputData(
      tickers="MSFT,AMZN,WMT",
      b=20220101,
      e=20230318,
      initial_aum=10000,
      strategy_type="M",
      days=100,
      top_pct=None)
    with self.assertRaises(ValueError) as cm:
      input_data.get_top_pct()
    self.assertEqual(str(cm.exception),
      "Top percentage must be specified.")
