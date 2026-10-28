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
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

BANNER = r"""
  _   _  ____   ____   _____ _____  _    _ ______ _____  ______ 
 | \ | |/ __ \ / __ \ / ____|  __ \| |  | |  ____|  __ \|  ____|
 |  \| | |  | | |  | | (___ | |__) | |__| | |__  | |__) | |__   
 | . ` | |  | | |  | |\___ \|  ___/|  __  |  __| |  _  /|  __|  
 | |\  | |__| | |__| |____) | |    | |  | | |____| | \ \| |____ 
 |_| \_|\____/ \____/|_____/|_|    |_|  |_|______|_|  \_\______|
     >> AUTONOMOUS AGENT MACRO-ECONOMIC ENGINE (NOOSPHERE) <<
"""

def generate_header_panel(agdp_stats: dict) -> Panel:
    text = Text()
    text.append("NOOSPHERE-MACRO // AUTONOMOUS AGENT WORLD ECONOMY\n", style="bold magenta")
    text.append("Global Agentic GDP (aGDP): ", style="cyan")
    text.append(f"{agdp_stats['total_agdp_sync']:,.2f} SYNC\n", style="bold green")
    text.append("Capital Velocity (V_sc): ", style="cyan")
    text.append(f"{agdp_stats['synthetic_capital_velocity']:.4f}\n", style="bold yellow")
    text.append("Macro Paradigm: High-Frequency Machine-to-Machine Flash Commerce\n", style="italic blue")
    return Panel(text, title="[bold white]MACROECONOMIC TELEMETRY GRID[/bold white]", border_style="bright_blue")

def generate_agents_table(agents: list) -> Table:
    table = Table(title="ACTIVE AUTONOMOUS ECONOMIC AGENTS", border_style="cyan")
    table.add_column("Agent ID", style="bold white")
    table.add_column("Designation", style="dim")
    table.add_column("Archetype", style="magenta")
    table.add_column("SYNC Balance", justify="right", style="bold green")
    table.add_column("Credit Score", justify="right", style="yellow")

    for ag in agents:
        table.add_row(
            ag.agent_id,
            ag.name,
            ag.role,
            f"{ag.balances.get('SYNC', 0.0):,.2f}",
            f"{ag.credit_score:.0f}"
        )
    return table

def generate_flash_corp_panel(corp_data: dict) -> Panel:
    text = Text()
    text.append(f"FLASH CORPORATION: {corp_data['corp_id']}\n", style="bold yellow")
    text.append(f"  * Status:           {corp_data['status']}\n", style="bold green")
    text.append(f"  * Lifespan:         {corp_data['lifetime_ms']:.1f} milliseconds\n", style="white")
    text.append(f"  * Gross Revenue:    {corp_data['gross_revenue_sync']:,.2f} SYNC\n", style="cyan")
    text.append(f"  * Repaid Debt:      {corp_data['repaid_debt_sync']:,.2f} SYNC\n", style="yellow")
    text.append(f"  * Net Dividends:    {corp_data['net_dividends_sync']:,.2f} SYNC\n", style="bold green")
    return Panel(text, title="[bold yellow]EPHEMERAL CORPORATE LIFECYCLE[/bold yellow]", border_style="yellow")

def generate_hhi_panel(audit: dict) -> Panel:
    text = Text()
    text.append(f"Market Audited:       {audit['market']}\n", style="white")
    text.append(f"Herfindahl Index:     {audit['hhi_index']} / 10,000\n", style="bold cyan")
    text.append(f"Antitrust Status:     {audit['status']}\n", style="bold green" if not audit['is_cartel_risk'] else "bold red")
    text.append(f"Collusion Risk:       {'FLAGGED / INTERVENTION REQUIRED' if audit['is_cartel_risk'] else 'CLEAR / OPTIMAL'}\n", style="bold green" if not audit['is_cartel_risk'] else "bold red")
    return Panel(text, title="[bold red]ANTITRUST & CARTEL AUDIT[/bold red]", border_style="red")
