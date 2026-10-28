import unittest
from synth_agent_economy.agents.capital_allocator_agent import CapitalAllocatorAgent
from synth_agent_economy.agents.compute_arbitrage_agent import ComputeArbitrageAgent
from synth_agent_economy.agents.synthetic_producer_agent import SyntheticProducerAgent
from synth_agent_economy.market.flash_corporation import FlashCorporation

class TestFlashCorporation(unittest.TestCase):
    def test_full_flash_corp_lifecycle(self):
        allocator = CapitalAllocatorAgent("Capital-01", initial_capital=500_000.0)
        broker = ComputeArbitrageAgent("Broker-01", cluster_capacity_flops=20_000.0)
        producer = SyntheticProducerAgent("Producer-01", initial_sync=50_000.0)

        # 1. Incorporate
        corp = FlashCorporation("Arbitrage synthetic dataset", producer.agent_id)
        self.assertEqual(corp.status, "INCORPORATED")

        # 2. Raise Debt
        funded = corp.raise_debt_capital(allocator, amount_sync=20_000.0, interest_rate=0.05)
        self.assertTrue(funded)
        self.assertEqual(corp.status, "CAPITALIZED")
        self.assertEqual(corp.treasury_sync, 20_000.0)

        # 3. Procure Compute
        procured = corp.procure_compute_resources(broker, required_flops=200.0)
        self.assertTrue(procured)
        self.assertEqual(corp.status, "PROVISIONED")

        # 4. Synthesize
        quanta = corp.execute_manufacturing_pipeline(producer)
        self.assertGreater(quanta, 0)
        self.assertEqual(corp.status, "MANUFACTURED")

        # 5. Monetize & Dissolve
        res = corp.monetize_and_dissolve(market_sell_price_per_quanta=60.0, capital_allocator=allocator)
        self.assertEqual(res["status"], "DISSOLVED")
        self.assertGreater(res["gross_revenue_sync"], 0)
        self.assertEqual(corp.treasury_sync, 0.0)
        self.assertIsNotNone(corp.dissolved_at)

if __name__ == "__main__":
    unittest.main()

