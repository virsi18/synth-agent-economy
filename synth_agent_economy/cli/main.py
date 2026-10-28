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

import sys
import time
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel

from synth_agent_economy.agents.capital_allocator_agent import CapitalAllocatorAgent
from synth_agent_economy.agents.compute_arbitrage_agent import ComputeArbitrageAgent
from synth_agent_economy.agents.synthetic_producer_agent import SyntheticProducerAgent
from synth_agent_economy.agents.governance_arbiter_agent import GovernanceArbiterAgent
from synth_agent_economy.market.flash_corporation import FlashCorporation
from synth_agent_economy.market.agentic_orderbook import AgenticOrderBook
from synth_agent_economy.market.agentic_gdp_tracker import AgenticGDPTracker
from synth_agent_economy.stabilizer.cartel_detector import CartelDetector
from synth_agent_economy.cli.dashboard import (
    BANNER,
    generate_header_panel,
    generate_agents_table,
    generate_flash_corp_panel,
    generate_hhi_panel
)

console = Console()

def run_simulation():
    console.print(BANNER, style="bold magenta")
    console.print("[bold yellow]Initializing Autonomous Agent World Economy Mesh...[/bold yellow]\n")

    # 1. Instantiate Autonomous Agents
    allocator = CapitalAllocatorAgent(name="Aethelgard-Capital-01", initial_capital=2_500_000.0)
    compute_broker = ComputeArbitrageAgent(name="Hyperion-ExaFLOP-Broker", cluster_capacity_flops=25_000.0)
    producer = SyntheticProducerAgent(name="Synthetix-Foundry-Nine", initial_sync=150_000.0)
    arbiter = GovernanceArbiterAgent(name="Arbiter-Omega-Central")
    gdp_tracker = AgenticGDPTracker(money_supply_sync=100_000_000.0)

    agents = [allocator, compute_broker, producer, arbiter]
    console.print(generate_agents_table(agents))
    console.print()

    # 2. Incorporate Flash Corporation
    console.print("[bold cyan]>>> OPPORTUNITY DETECTED: Synthesizing Multi-Modal Reasoning Quanta for European Autonomous Fleet <<<[/bold cyan]")
    flash_corp = FlashCorporation(
        mission_manifesto="Arbitrage high-density compute to synthesize 2,000 INF_QUANTA",
        founder_agent_id=producer.agent_id
    )
    console.print(f"[yellow]⚡ Flash Corporation created: {flash_corp.corp_id}[/yellow]")
    time.sleep(0.3)

    # 3. Capital Allocator Underwrites Flash Debt
    debt_amount = 75_000.0
    funded = flash_corp.raise_debt_capital(allocator, amount_sync=debt_amount, interest_rate=0.035)
    console.print(f"[green][OK] Flash Debt Underwritten: {debt_amount:,.2f} SYNC at 3.5% APY[/green]")
    gdp_tracker.record_economic_activity("INVESTMENT", debt_amount, "Flash Corporate Debt Financing")
    time.sleep(0.3)

    # 4. Procure Compute Hours
    flops_needed = 1000.0
    procured = flash_corp.procure_compute_resources(compute_broker, required_flops=flops_needed)
    console.print(f"[green][OK] Procured {flops_needed:,.0f} FLOP_HOURS from {compute_broker.name}[/green]")
    gdp_tracker.record_economic_activity("INVESTMENT", flops_needed * 38.0, "Hardware Compute Capacity Allocation")
    time.sleep(0.3)

    # 5. Synthesize Products
    quanta = flash_corp.execute_manufacturing_pipeline(producer)
    console.print(f"[green][OK] Manufactured {quanta:,.2f} INF_QUANTA via {producer.name}[/green]")
    time.sleep(0.3)

    # 6. Monetize & Dissolve
    market_price = 55.0  # SYNC per INF_QUANTA
    corp_result = flash_corp.monetize_and_dissolve(market_price, allocator)
    gdp_tracker.record_economic_activity("CONSUMPTION", corp_result["gross_revenue_sync"], "Autonomous Inference Quanta Market Absorption")
    gdp_tracker.record_economic_activity("EXPORTS", 15_000.0, "Net Cross-Cluster Compute Exports")

    console.print(f"[bold green]✔ Flash Corporation Dissolved in {corp_result['lifetime_ms']:.1f}ms[/bold green]")
    console.print()

    # 7. Render Telemetry
    agdp_stats = gdp_tracker.compute_current_agdp()
    console.print(generate_header_panel(agdp_stats))
    console.print()
    console.print(generate_flash_corp_panel(corp_result))
    console.print()

    # 8. Antitrust Cartel Audit
    audit_shares = {
        compute_broker.agent_id: 4200.0,
        allocator.agent_id: 3100.0,
        producer.agent_id: 2700.0
    }
    audit = CartelDetector.evaluate_market_collusion("FLOP_HOUR_COMPUTE_MARKET", audit_shares)
    console.print(generate_hhi_panel(audit))
    console.print("\n[bold green]>>> Autonomous Macro-Economic Engine In Nominal Equilibrium. <<<[/bold green]")

def run_agdp_report():
    gdp_tracker = AgenticGDPTracker()
    gdp_tracker.record_economic_activity("CONSUMPTION", 450_000.0)
    gdp_tracker.record_economic_activity("INVESTMENT", 1_200_000.0)
    gdp_tracker.record_economic_activity("SUBSIDIES", 100_000.0)
    gdp_tracker.record_economic_activity("EXPORTS", 350_000.0)
    stats = gdp_tracker.compute_current_agdp()
    console.print(generate_header_panel(stats))

def main():
    parser = argparse.ArgumentParser(description="NOOSPHERE Autonomous Agent Macro-Economy Engine")
    parser.add_argument("command", choices=["demo", "simulate", "agdp"], nargs="?", default="demo")
    args = parser.parse_args()

    if args.command in ("demo", "simulate"):
        run_simulation()
    elif args.command == "agdp":
        run_agdp_report()

if __name__ == "__main__":
    main()
