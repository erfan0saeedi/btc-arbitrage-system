import unittest

from src.collectors.wallex import WallexCollector


class TestWallexCollector(unittest.TestCase):
    def test_parse_orderbook_valid_payload(self):
        payload = {
            "result": {
                "ask": [{"price": "100", "quantity": "0.1"}],
                "bid": [{"price": "99", "quantity": "0.2"}],
            }
        }

        asks, bids = WallexCollector.parse_orderbook(payload)

        self.assertEqual(asks, [["100", "0.1"]])
        self.assertEqual(bids, [["99", "0.2"]])

    def test_parse_orderbook_missing_result(self):
        asks, bids = WallexCollector.parse_orderbook({})

        self.assertEqual(asks, [])
        self.assertEqual(bids, [])


if __name__ == "__main__":
    unittest.main()
