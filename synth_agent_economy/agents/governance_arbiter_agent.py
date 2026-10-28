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
from synth_agent_economy.constants import DEFAULT_TARGET_INFLATION_RATE

class GovernanceArbiterAgent(BaseEconomicAgent):
    """
    Autonomous Macroeconomic Stabilizer & Central Clearing Arbiter.
    Monitors inter-agent liquidity, evaluates systemic solvency,
    and calculates canonical Agentic Gross Domestic Product (aGDP).
    """

    def __init__(self, name: str = "Arbiter-Omega-Central"):
        super().__init__(name=name, role="MACRO_GOVERNANCE_ARBITER", initial_balance=50_000_000.0)
        self.target_inflation = DEFAULT_TARGET_INFLATION_RATE
        self.emergency_circuit_breaker_active: bool = False
        self.historical_agdp_snapshots: List[Dict[str, Any]] = []

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
