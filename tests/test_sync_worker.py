import unittest

from src.processor.sync_worker import SyncWorker


class TestSyncWorker(unittest.TestCase):
    def test_extract_prices_valid(self):
        kucoin_data = {"price": "30123.5"}
        wallex_data = {"bids": [["30000", "0.45"]]}

        prices = SyncWorker.extract_prices(kucoin_data, wallex_data)

        self.assertEqual(prices, (30123.5, 30000.0))

    def test_extract_prices_missing_data(self):
        self.assertIsNone(SyncWorker.extract_prices(None, {"bids": [["1", "1"]]}))
        self.assertIsNone(SyncWorker.extract_prices({"price": "1"}, {}))


if __name__ == "__main__":
    unittest.main()
