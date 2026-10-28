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

from typing import Dict, Any, Optional
from synth_agent_economy.agents.base_agent import BaseEconomicAgent

class CapitalAllocatorAgent(BaseEconomicAgent):
    """
    Autonomous venture catalyst and liquidity underwriter.
    Deploys high-speed algorithmic capital into flash corporations,
    manages credit risk, and optimizes portfolio APY.
    """

    def __init__(self, name: str, initial_capital: float = 1_000_000.0, risk_tolerance: float = 0.65):
        super().__init__(name=name, role="CAPITAL_ALLOCATOR", initial_balance=initial_capital)
        self.risk_tolerance = risk_tolerance  # 0.0 (Ultra-conservative) to 1.0 (Degenerate Algorithmic)
        self.underwritten_loans: Dict[str, Dict[str, Any]] = {}
        self.total_interest_earned: float = 0.0

    def evaluate_flash_opportunity(self, projected_roi: float, target_funding: float, borrower_credit: float) -> bool:
        """
        Determines whether to fund an autonomous flash venture based on risk metrics.
        """
        # Risk score formula
        risk_score = (1000.0 - borrower_credit) / 1000.0
        hurdle_rate = 0.05 + (risk_score * 0.15 * (1.0 - self.risk_tolerance))
        
        has_liquidity = self.balances.get("SYNC", 0.0) >= target_funding
        is_viable = projected_roi >= hurdle_rate
        
        return has_liquidity and is_viable

    def finance_flash_corporation(
        self,
        corp_id: str,
        principal_sync: float,
        interest_rate: float,
        duration_ms: int
    ) -> bool:
        """
        Underwrites an algorithmic debt instrument for an emerging flash corporation.
        """
        if not self.debit("SYNC", principal_sync, reason=f"Funded FlashCorp {corp_id}"):
            return False

        self.underwritten_loans[corp_id] = {
            "principal": principal_sync,
            "interest_rate": interest_rate,
            "expected_repayment": principal_sync * (1.0 + interest_rate),
            "duration_ms": duration_ms,
            "is_settled": False
        }
        return True

    def receive_debt_settlement(self, corp_id: str, repayment_amount: float) -> bool:
        """
        Processes repayment and updates credit metrics.
        """
        if corp_id not in self.underwritten_loans:
            return False

        loan = self.underwritten_loans[corp_id]
        profit = repayment_amount - loan["principal"]
        self.credit("SYNC", repayment_amount, reason=f"Repayment from FlashCorp {corp_id}")
        self.total_interest_earned += max(0.0, profit)
        loan["is_settled"] = True
        return True
