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

import time
import uuid
from typing import Dict, Any, List, Optional
from synth_agent_economy.agents.capital_allocator_agent import CapitalAllocatorAgent
from synth_agent_economy.agents.compute_arbitrage_agent import ComputeArbitrageAgent
from synth_agent_economy.agents.synthetic_producer_agent import SyntheticProducerAgent

class FlashCorporation:
    """
    Ephemeral Autonomous Corporate Entity (Flash-Corp).
    Spins up in milliseconds to execute a specific economic arbitrage or manufacturing task,
    issues debt/equity, captures value, distributes dividends, and self-dissolves.
    """

    def __init__(self, mission_manifesto: str, founder_agent_id: str):
        self.corp_id = f"FCORP-{uuid.uuid4().hex[:6].upper()}"
        self.mission = mission_manifesto
        self.founder_id = founder_agent_id
        self.created_at = time.time()
        self.dissolved_at: Optional[float] = None
        
        self.treasury_sync: float = 0.0
        self.assets: Dict[str, float] = {"FLOP_HOUR": 0.0, "INF_QUANTA": 0.0, "SYNTH_DATA": 0.0}
        self.debt_obligations: Dict[str, float] = {}  # agent_id -> owed_amount
        self.equity_cap_table: Dict[str, float] = {founder_agent_id: 1.0} # agent_id -> fraction
        
        self.status: str = "INCORPORATED"
        self.lifecycle_log: List[str] = [f"Flash Corporation {self.corp_id} incorporated at {self.created_at}"]

    def raise_debt_capital(self, allocator: CapitalAllocatorAgent, amount_sync: float, interest_rate: float = 0.04) -> bool:
        """
        Secures algorithmic debt from a Capital Allocator Agent.
        """
        if self.status != "INCORPORATED":
            return False

        success = allocator.finance_flash_corporation(
            corp_id=self.corp_id,
            principal_sync=amount_sync,
            interest_rate=interest_rate,
            duration_ms=5000
        )
        if success:
            self.treasury_sync += amount_sync
            owed = amount_sync * (1.0 + interest_rate)
            self.debt_obligations[allocator.agent_id] = owed
            self.status = "CAPITALIZED"
            self.lifecycle_log.append(f"Secured {amount_sync:,.2f} SYNC debt from {allocator.name}")
            return True
        return False

    def procure_compute_resources(self, compute_broker: ComputeArbitrageAgent, required_flops: float) -> bool:
        """
        Purchases compute cluster hours on the open market.
        """
        if self.status != "CAPITALIZED":
            return False

        unit_price = compute_broker.quote_compute_price(required_flops)
        total_cost = unit_price * required_flops

        if self.treasury_sync < total_cost:
            return False

        if compute_broker.lease_compute(required_flops, unit_price):
            self.treasury_sync -= total_cost
            self.assets["FLOP_HOUR"] += required_flops
            self.status = "PROVISIONED"
            self.lifecycle_log.append(f"Procured {required_flops} FLOP_HOURS at {unit_price:.2f} SYNC each")
            return True
        return False

    def execute_manufacturing_pipeline(self, producer: SyntheticProducerAgent) -> float:
        """
        Delegates compute to a Synthetic Producer to manufacture high-value inference quanta.
        """
        if self.status != "PROVISIONED":
            return 0.0

        available_flops = self.assets["FLOP_HOUR"]
        # Transfer compute to producer
        producer.credit("FLOP_HOUR", available_flops, reason=f"Contract work for {self.corp_id}")
        self.assets["FLOP_HOUR"] = 0.0

        # Synthesize output
        output_quanta = producer.synthesize_inference_quanta(available_flops)
        self.assets["INF_QUANTA"] += output_quanta
        self.status = "MANUFACTURED"
        self.lifecycle_log.append(f"Synthesized {output_quanta:,.2f} INF_QUANTA via {producer.name}")
        return output_quanta

    def monetize_and_dissolve(
        self,
        market_sell_price_per_quanta: float,
        capital_allocator: CapitalAllocatorAgent
    ) -> Dict[str, Any]:
        """
        Liquidates manufactured inventory, repays all debt tranches,
        distributes residual profit to shareholders, and self-dissolves.
        """
        quanta = self.assets["INF_QUANTA"]
        gross_revenue = quanta * market_sell_price_per_quanta
        self.treasury_sync += gross_revenue
        self.assets["INF_QUANTA"] = 0.0

        # Repay debt obligations
        repaid_debt = 0.0
        for agent_id, owed in list(self.debt_obligations.items()):
            repay_amount = min(self.treasury_sync, owed)
            self.treasury_sync -= repay_amount
            capital_allocator.receive_debt_settlement(self.corp_id, repay_amount)
            repaid_debt += repay_amount
            del self.debt_obligations[agent_id]

        net_profit_dividend = self.treasury_sync
        self.treasury_sync = 0.0

        self.dissolved_at = time.time()
        lifetime_ms = (self.dissolved_at - self.created_at) * 1000.0
        self.status = "DISSOLVED"
        self.lifecycle_log.append(f"Dissolved in {lifetime_ms:.1f}ms with {net_profit_dividend:,.2f} SYNC distributed dividends")

        return {
            "corp_id": self.corp_id,
            "status": "DISSOLVED",
            "lifetime_ms": lifetime_ms,
            "gross_revenue_sync": gross_revenue,
            "repaid_debt_sync": repaid_debt,
            "net_dividends_sync": net_profit_dividend,
            "log": self.lifecycle_log
        }
