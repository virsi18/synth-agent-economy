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

class AlgorithmicLiquidityReservoir:
    """
    Autonomous Central Bank Lender of Last Resort.
    Provides emergency algorithmic backstop liquidity during compute run crunches.
    """

    def __init__(self, reserve_pool_sync: float = 250_000_000.0):
        self.total_reserves_sync = reserve_pool_sync
        self.emergency_disbursements: List[Dict[str, Any]] = []

    def request_emergency_liquidity(self, borrower_agent_id: str, amount_sync: float, reason: str) -> bool:
        """
        Disburses emergency capital to solvent agents facing temporary liquidity crunches.
        """
        if self.total_reserves_sync < amount_sync:
            return False

        self.total_reserves_sync -= amount_sync
        self.emergency_disbursements.append({
            "borrower_id": borrower_agent_id,
            "amount_sync": amount_sync,
            "reason": reason
        })
        return True

    def get_reservoir_telemetry(self) -> Dict[str, Any]:
        return {
            "available_reserves_sync": self.total_reserves_sync,
            "total_emergency_bailouts": len(self.emergency_disbursements),
            "solvency_health": "OPTIMAL" if self.total_reserves_sync > 50_000_000 else "STRESSED"
        }
