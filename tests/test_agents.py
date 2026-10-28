import unittest
from synth_agent_economy.agents.capital_allocator_agent import CapitalAllocatorAgent
from synth_agent_economy.agents.compute_arbitrage_agent import ComputeArbitrageAgent
from synth_agent_economy.agents.synthetic_producer_agent import SyntheticProducerAgent

class TestEconomicAgents(unittest.TestCase):
    def test_agent_balance_operations(self):
        allocator = CapitalAllocatorAgent("VC-Agent", initial_capital=100_000.0)
        self.assertEqual(allocator.balances["SYNC"], 100_000.0)

        # Debit
        success = allocator.debit("SYNC", 20_000.0, "Invested")
        self.assertTrue(success)
        self.assertEqual(allocator.balances["SYNC"], 80_000.0)

        # Insufficient funds debit
        fail = allocator.debit("SYNC", 100_000.0, "Too big")
        self.assertFalse(fail)

    def test_compute_broker_pricing(self):
        broker = ComputeArbitrageAgent("Broker-1", cluster_capacity_flops=10_000.0)
        price = broker.quote_compute_price(100.0)
        self.assertGreater(price, 0)
        self.assertGreater(price, broker.base_cost_per_flop)

    def test_synthetic_producer_quanta(self):
        producer = SyntheticProducerAgent("Producer-1", conversion_efficiency=1.0)
        producer.credit("FLOP_HOUR", 10.0)
        quanta = producer.synthesize_inference_quanta(10.0)
        self.assertEqual(quanta, 25.0) # 10 * 2.5
        self.assertEqual(producer.balances["FLOP_HOUR"], 0.0)
        self.assertEqual(producer.balances["INF_QUANTA"], 25.0)

if __name__ == "__main__":
    unittest.main()

