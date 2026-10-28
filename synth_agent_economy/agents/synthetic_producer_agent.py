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

class SyntheticProducerAgent(BaseEconomicAgent):
    """
    Autonomous computational manufacturer.
    Consumes raw compute (FLOP_HOUR) to synthesize high-dimensional reasoning tokens
    (INF_QUANTA) and structured high-entropy training data (SYNTH_DATA).
    """

    def __init__(self, name: str, initial_sync: float = 100_000.0, conversion_efficiency: float = 0.92):
        super().__init__(name=name, role="SYNTHETIC_PRODUCER", initial_balance=initial_sync)
        self.efficiency = conversion_efficiency
        self.total_products_manufactured: int = 0

    def synthesize_inference_quanta(self, flop_hours: float) -> float:
        """
        Converts raw compute into inference / reasoning quanta.
        1 FLOP_HOUR yields ~2.5 INF_QUANTA (2.5 million reasoning tokens).
        """
        if not self.debit("FLOP_HOUR", flop_hours, reason="Consumed in synthesis pipeline"):
            return 0.0

        output_quanta = flop_hours * 2.5 * self.efficiency
        self.credit("INF_QUANTA", output_quanta, reason="Synthesized new reasoning capacity")
        self.total_products_manufactured += 1
        return output_quanta

    def synthesize_training_data(self, flop_hours: float) -> float:
        """
        Converts raw compute into verified high-entropy synthetic training data.
        1 FLOP_HOUR yields ~0.4 SYNTH_DATA (400 MB).
        """
        if not self.debit("FLOP_HOUR", flop_hours, reason="Consumed in dataset generation"):
            return 0.0

        output_data = flop_hours * 0.4 * self.efficiency
        self.credit("SYNTH_DATA", output_data, reason="Synthesized high-entropy dataset")
        self.total_products_manufactured += 1
        return output_data
