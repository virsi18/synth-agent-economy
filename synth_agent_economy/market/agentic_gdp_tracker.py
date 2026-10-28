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

from typing import List, Dict, Any

class AgenticGDPTracker:
    """
    Computes real-time macroeconomic indicators for the autonomous agent society.
    Tracks Agentic Gross Domestic Product (aGDP), Velocity of Synthetic Capital (V_sc),
    and autonomous employment capacity.
    """

    def __init__(self, money_supply_sync: float = 100_000_000.0):
        self.money_supply = money_supply_sync
        self.total_consumption: float = 0.0
        self.total_investment: float = 0.0
        self.total_subsidies: float = 0.0
        self.total_net_exports: float = 0.0
        self.all_recorded_transactions: List[Dict[str, Any]] = []

    def record_economic_activity(self, category: str, amount_sync: float, details: str = ""):
        """
        Records an economic event into one of the four macroeconomic quadrants:
        C (Consumption), I (Investment), G (Governance/Subsidies), NX (Net Exports).
        """
        if category == "CONSUMPTION":
            self.total_consumption += amount_sync
        elif category == "INVESTMENT":
            self.total_investment += amount_sync
        elif category == "SUBSIDIES":
            self.total_subsidies += amount_sync
        elif category == "EXPORTS":
            self.total_net_exports += amount_sync
        elif category == "IMPORTS":
            self.total_net_exports -= amount_sync

        self.all_recorded_transactions.append({
            "category": category,
            "amount_sync": amount_sync,
            "details": details
        })

    def compute_current_agdp(self) -> Dict[str, Any]:
        """
        Formulates the standard autonomous macro equation:
        aGDP = C_a + I_a + G_a + NX_a
        """
        total_agdp = (
            self.total_consumption +
            self.total_investment +
            self.total_subsidies +
            self.total_net_exports
        )

        # Velocity of synthetic capital V = aGDP / M
        velocity = total_agdp / self.money_supply if self.money_supply > 0 else 0.0

        return {
            "total_agdp_sync": total_agdp,
            "consumption_c": self.total_consumption,
            "investment_i": self.total_investment,
            "subsidies_g": self.total_subsidies,
            "net_exports_nx": self.total_net_exports,
            "synthetic_capital_velocity": velocity,
            "total_recorded_events": len(self.all_recorded_transactions)
        }
