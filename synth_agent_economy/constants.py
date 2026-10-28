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

# ==============================================================================
# SYNTHETIC MACROECONOMIC CURRENCY & ASSET CLASSES
# ==============================================================================
BASE_CURRENCY = "SYNC"                   # Synthetic Yield-Bearing Network Credit

ASSET_CLASSES = {
    "SYNC": {
        "description": "Standard synthetic settlement unit across autonomous agents",
        "base_liquidity": 100_000_000.0,
        "is_collateral": True
    },
    "FLOP_HOUR": {
        "description": "Normalized petaFLOP compute hour (ExaFLOP cluster slice)",
        "base_price_sync": 42.50,
        "is_commodity": True
    },
    "INF_QUANTA": {
        "description": "One Million multi-modal reasoning & inference tokens",
        "base_price_sync": 18.20,
        "is_commodity": True
    },
    "SYNTH_DATA": {
        "description": "One Gigabyte of verified high-entropy synthetic training tokens",
        "base_price_sync": 85.00,
        "is_commodity": True
    }
}

# ==============================================================================
# MACROECONOMIC REGULATORY & SYSTEMIC CONSTANTS
# ==============================================================================
DEFAULT_TARGET_INFLATION_RATE = 0.015       # 1.5% target annual expansion for aGDP
CIRCUIT_BREAKER_VOLATILITY_THRESHOLD = 0.25 # 25% price deviation triggers trading halt
FLASH_CORP_MAX_LIFETIME_MS = 60000          # Maximum 60-second lifespan for flash corporations
COLLUSION_HERFINDAHL_THRESHOLD = 2500.0     # HHI index threshold for cartel detection
AGENT_CAPITAL_RESERVE_RATIO = 0.08          # 8% mandatory liquid collateral buffer
