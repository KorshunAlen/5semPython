import unittest
from LR5 import CurrencyFetcher

class TestCurrencyFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = CurrencyFetcher(min_request_interval=0)

    def test_invalid_id(self):
        currencies = self.fetcher.fetch_currencies(['R9999'])
        self.assertEqual(currencies, [])

    def test_valid_id(self):
        currencies = self.fetcher.fetch_currencies(['R01035'])  # ID для GBP
        self.assertTrue(currencies)
        for currency in currencies:
            self.assertIn('GBP', currency)
            self.assertTrue(0 <= float(".".join(currency['GBP'][1])) < 1000)

if __name__ == '__main__':
    unittest.main()
