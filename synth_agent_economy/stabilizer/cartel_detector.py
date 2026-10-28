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

from typing import Dict, List, Any
from synth_agent_economy.constants import COLLUSION_HERFINDAHL_THRESHOLD

class CartelDetector:
    """
    Antitrust & Collusion Sentinel for machine-to-machine economies.
    Evaluates Herfindahl-Hirschman Index (HHI) and flags synthetic price-fixing rings.
    """

    @staticmethod
    def calculate_hhi(market_shares: Dict[str, float]) -> float:
        """
        Calculates HHI = sum((market_share_percentage)^2)
        HHI < 1500: Competitive
        1500 <= HHI <= 2500: Moderately Concentrated
        HHI > 2500: Highly Concentrated (Potential Cartel)
        """
        total = sum(market_shares.values())
        if total <= 0:
            return 0.0

        hhi = 0.0
        for agent_id, share in market_shares.items():
            pct = (share / total) * 100.0
            hhi += pct ** 2

        return round(hhi, 2)

    @classmethod
    def evaluate_market_collusion(cls, market_name: str, agent_volumes: Dict[str, float]) -> Dict[str, Any]:
        """
        Audits market volumes for antitrust cartel concentration.
        """
        hhi = cls.calculate_hhi(agent_volumes)
        is_cartel_risk = hhi > COLLUSION_HERFINDAHL_THRESHOLD

        status = "COMPETITIVE"
        if hhi > COLLUSION_HERFINDAHL_THRESHOLD:
            status = "CRITICAL_CARTEL_RISK"
        elif hhi > 1500:
            status = "MODERATELY_CONCENTRATED"

        return {
            "market": market_name,
            "hhi_index": hhi,
            "threshold": COLLUSION_HERFINDAHL_THRESHOLD,
            "status": status,
            "is_cartel_risk": is_cartel_risk,
            "participating_agents": len(agent_volumes)
        }
