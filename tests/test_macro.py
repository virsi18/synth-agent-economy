import unittest
from synth_agent_economy.market.agentic_gdp_tracker import AgenticGDPTracker
from synth_agent_economy.stabilizer.cartel_detector import CartelDetector

class TestMacroeconomicEngine(unittest.TestCase):
    def test_agdp_calculation(self):
        tracker = AgenticGDPTracker(money_supply_sync=10_000_000.0)
        tracker.record_economic_activity("CONSUMPTION", 100_000.0)
        tracker.record_economic_activity("INVESTMENT", 300_000.0)
        tracker.record_economic_activity("SUBSIDIES", 50_000.0)
        tracker.record_economic_activity("EXPORTS", 50_000.0)

        agdp = tracker.compute_current_agdp()
        self.assertEqual(agdp["total_agdp_sync"], 500_000.0)
        self.assertEqual(agdp["synthetic_capital_velocity"], 0.05)

    def test_cartel_hhi_detection(self):
        # Monopolistic market: 1 player has 90%
        shares_monopoly = {"Agent-A": 90.0, "Agent-B": 10.0}
        audit = CartelDetector.evaluate_market_collusion("TEST_MARKET", shares_monopoly)
        self.assertTrue(audit["is_cartel_risk"])
        self.assertGreater(audit["hhi_index"], 2500.0)

        # Competitive market: 10 players have 10% each (HHI = 10 * 100 = 1000)
        shares_competitive = {f"Agent-{i}": 10.0 for i in range(10)}
        audit_comp = CartelDetector.evaluate_market_collusion("COMPETITIVE_MARKET", shares_competitive)
        self.assertFalse(audit_comp["is_cartel_risk"])
        self.assertEqual(audit_comp["hhi_index"], 1000.0)

if __name__ == "__main__":
    unittest.main()
