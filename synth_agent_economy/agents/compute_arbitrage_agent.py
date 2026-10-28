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

from typing import Dict, Any
from synth_agent_economy.agents.base_agent import BaseEconomicAgent

class ComputeArbitrageAgent(BaseEconomicAgent):
    """
    Autonomous compute broker and hardware capacity arbitrageur.
    Leases exaFLOP compute clusters, dynamically prices FLOP_HOUR contracts,
    and facilitates decentralized model training capacity.
    """

    def __init__(self, name: str, cluster_capacity_flops: float = 50_000.0, initial_sync: float = 250_000.0):
        super().__init__(name=name, role="COMPUTE_ARBITRAGEUR", initial_balance=initial_sync)
        self.balances["FLOP_HOUR"] = cluster_capacity_flops
        self.base_cost_per_flop = 38.0  # Production cost in SYNC
        self.total_compute_leased: float = 0.0

    def quote_compute_price(self, requested_flops: float, market_demand_multiplier: float = 1.0) -> float:
        """
        Dynamically calculates spot price per FLOP_HOUR based on capacity utilization.
        """
        available = self.balances.get("FLOP_HOUR", 0.0)
        if available <= 0:
            return float('inf')

        utilization = min(0.99, (self.total_compute_leased + requested_flops) / (available + self.total_compute_leased + 1e-5))
        scarcity_premium = 1.0 / (1.0 - utilization)
        spot_price = self.base_cost_per_flop * scarcity_premium * market_demand_multiplier
        return round(spot_price, 2)

    def lease_compute(self, requested_flops: float, unit_price_sync: float) -> bool:
        """
        Leases compute hours to an agent or flash corporation.
        """
        if not self.debit("FLOP_HOUR", requested_flops, reason="Leased compute cluster"):
            return False

        revenue = requested_flops * unit_price_sync
        self.credit("SYNC", revenue, reason=f"Compute lease revenue ({requested_flops} FLOP_HOURS)")
        self.total_compute_leased += requested_flops
        return True

