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
from typing import Dict, Any, List

class BaseEconomicAgent:
    """
    Abstract foundation for all economic agents participating in the autonomous macro-mesh.
    """

    def __init__(self, name: str, role: str, initial_balance: float = 10_000.0):
        self.agent_id = f"AGENT-{uuid.uuid4().hex[:8].upper()}"
        self.name = name
        self.role = role
        self.balances: Dict[str, float] = {
            "SYNC": initial_balance,
            "FLOP_HOUR": 0.0,
            "INF_QUANTA": 0.0,
            "SYNTH_DATA": 0.0
        }
        self.credit_score: float = 750.0
        self.transaction_history: List[Dict[str, Any]] = []
        self.created_at: float = time.time()
        self.is_active: bool = True

    def credit(self, asset: str, amount: float, reason: str = ""):
        if asset not in self.balances:
            self.balances[asset] = 0.0
        self.balances[asset] += amount
        self.transaction_history.append({
            "type": "CREDIT",
            "asset": asset,
            "amount": amount,
            "reason": reason,
            "timestamp": time.time()
        })

    def debit(self, asset: str, amount: float, reason: str = "") -> bool:
        if self.balances.get(asset, 0.0) < amount:
            return False
        self.balances[asset] -= amount
        self.transaction_history.append({
            "type": "DEBIT",
            "asset": asset,
            "amount": amount,
            "reason": reason,
            "timestamp": time.time()
        })
        return True

    def get_net_worth_sync(self, price_oracle: Dict[str, float]) -> float:
        """
        Calculates total portfolio value denominated in SYNC.
        """
        total = self.balances.get("SYNC", 0.0)
        for asset, qty in self.balances.items():
            if asset != "SYNC" and asset in price_oracle:
                total += qty * price_oracle[asset]
        return total

    def __repr__(self) -> str:
        return f"<{self.role}:{self.name} [{self.agent_id}] Balance: {self.balances['SYNC']:.2f} SYNC>"
