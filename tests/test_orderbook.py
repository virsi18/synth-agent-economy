import unittest
from synth_agent_economy.market.agentic_orderbook import AgenticOrderBook

class TestAgenticOrderBook(unittest.TestCase):
    def test_order_matching_execution(self):
        book = AgenticOrderBook("FLOP_HOUR")

        # Seller places ASK: 100 FLOP_HOURS at 45.0 SYNC
        trades1 = book.place_order("ORD-1", "Seller-Agent", "SELL", price=45.0, quantity=100.0)
        self.assertEqual(len(trades1), 0)
        self.assertEqual(len(book.asks), 1)

        # Buyer places matching BID: 40 FLOP_HOURS at 46.0 SYNC
        trades2 = book.place_order("ORD-2", "Buyer-Agent", "BUY", price=46.0, quantity=40.0)
        self.assertEqual(len(trades2), 1)
        self.assertEqual(trades2[0]["quantity"], 40.0)
        self.assertEqual(trades2[0]["price_sync"], 45.0)
        self.assertEqual(trades2[0]["volume_sync"], 1800.0)

        # 60 left in ask
        depth = book.get_orderbook_depth()
        self.assertEqual(depth["asks_count"], 1)
        self.assertEqual(book.asks[0].quantity, 60.0)

if __name__ == "__main__":
    unittest.main()

