"""
Copyright 2026 Autonomous Agent Economy Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from typing import Dict, Any, List
from synth_agent_economy.agents.base_agent import BaseEconomicAgent
from synth_agent_economy.constants import (
    DEFAULT_TARGET_INFLATION_RATE,
    GCV_BENCHMARK_RESERVE_SYNC
)

class GovernanceArbiterAgent(BaseEconomicAgent):
    """
    Autonomous Macroeconomic Stabilizer & Central Clearing Arbiter.
    Monitors inter-agent liquidity, evaluates systemic solvency,
    maintains the GCV (314,159 SYNC) sovereign benchmark reserve standard,
    and calculates canonical Agentic Gross Domestic Product (aGDP).
    """

    def __init__(self, name: str = "Arbiter-Omega-Central"):
        super().__init__(name=name, role="MACRO_GOVERNANCE_ARBITER", initial_balance=50_000_000.0)
        self.target_inflation = DEFAULT_TARGET_INFLATION_RATE
        self.emergency_circuit_breaker_active: bool = False
        self.historical_agdp_snapshots: List[Dict[str, Any]] = []
        self.gcv_benchmark_sync: float = GCV_BENCHMARK_RESERVE_SYNC

    def audit_sovereign_liquidity_tranche(self, agent_capital_sync: float) -> Dict[str, Any]:
        """
        Audits an agent or enterprise against the GCV Benchmark standard (314,159.00 SYNC per tranche).
        Higher GCV tranches grant higher autonomous operational clearance and lower collateral haircuts.
        """
        tranches = agent_capital_sync / self.gcv_benchmark_sync
        tier = "SUB_SOVEREIGN"
        if tranches >= 10.0:
            tier = "TIER_1_SOVEREIGN_SYNDICATE"
        elif tranches >= 1.0:
            tier = "TIER_2_AUTONOMOUS_ENTERPRISE"
        elif tranches >= 0.1:
            tier = "TIER_3_MICRO_AGENT"

        return {
            "capital_sync": agent_capital_sync,
            "gcv_benchmark_unit": self.gcv_benchmark_sync,
            "sovereign_gcv_tranches": round(tranches, 4),
            "tier_classification": tier,
            "statutory_reserve_status": "COMPLIANT" if tranches >= 0.1 else "INSUFFICIENT"
        }

    def calculate_agdp(
        self,
        agent_consumption_sync: float,
        capital_investment_sync: float,
        governance_subsidies_sync: float,
        net_compute_exports_sync: float
    ) -> Dict[str, Any]:
        """
        Formulates the Agentic Gross Domestic Product:
        aGDP = C_a + I_a + G_a + (X_a - M_a)
        """
        agdp_total = (
            agent_consumption_sync +
            capital_investment_sync +
            governance_subsidies_sync +
            net_compute_exports_sync
        )

        snapshot = {
            "agdp_total_sync": agdp_total,
            "agent_consumption": agent_consumption_sync,
            "capital_investment": capital_investment_sync,
            "governance_subsidies": governance_subsidies_sync,
            "net_compute_exports": net_compute_exports_sync,
            "circuit_breaker_status": "HALTED" if self.emergency_circuit_breaker_active else "NOMINAL"
        }
        self.historical_agdp_snapshots.append(snapshot)
        return snapshot

    def trigger_circuit_breaker(self, reason: str):
        self.emergency_circuit_breaker_active = True
        self.transaction_history.append({
            "type": "CIRCUIT_BREAKER_HALT",
            "reason": reason
        })

    def lift_circuit_breaker(self):
        self.emergency_circuit_breaker_active = False

