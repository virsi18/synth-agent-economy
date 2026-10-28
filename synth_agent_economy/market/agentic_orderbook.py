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
import heapq
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field

@dataclass(order=True)
class Order:
    sort_key: float
    order_id: str = field(compare=False)
    agent_id: str = field(compare=False)
    asset: str = field(compare=False)
    side: str = field(compare=False)          # 'BUY' or 'SELL'
    price_sync: float = field(compare=False)
    quantity: float = field(compare=False)
    timestamp: float = field(compare=False)

class AgenticOrderBook:
    """
    Sub-millisecond continuous double auction orderbook for machine-to-machine assets.
    """

    def __init__(self, asset: str):
        self.asset = asset
        # Bids: Max-heap (invert price for heapq)
        self.bids: List[Order] = []
        # Asks: Min-heap
        self.asks: List[Order] = []
        self.trade_history: List[Dict[str, Any]] = []
        self.last_clearing_price: float = 0.0

    def place_order(self, order_id: str, agent_id: str, side: str, price: float, quantity: float) -> List[Dict[str, Any]]:
        """
        Inserts an order and immediately matches against opposite book side.
        Returns list of executed trades.
        """
        now = time.time()
        executed_trades = []

        if side == "BUY":
            # Match against lowest ask
            while self.asks and self.asks[0].price_sync <= price and quantity > 0:
                best_ask = self.asks[0]
                trade_qty = min(quantity, best_ask.quantity)
                trade_price = best_ask.price_sync

                executed_trades.append({
                    "asset": self.asset,
                    "buyer_id": agent_id,
                    "seller_id": best_ask.agent_id,
                    "price_sync": trade_price,
                    "quantity": trade_qty,
                    "volume_sync": trade_price * trade_qty,
                    "timestamp": now
                })

                quantity -= trade_qty
                best_ask.quantity -= trade_qty
                self.last_clearing_price = trade_price

                if best_ask.quantity <= 0:
                    heapq.heappop(self.asks)

            if quantity > 0:
                heapq.heappush(self.bids, Order(
                    sort_key=-price,
                    order_id=order_id,
                    agent_id=agent_id,
                    asset=self.asset,
                    side="BUY",
                    price_sync=price,
                    quantity=quantity,
                    timestamp=now
                ))

        elif side == "SELL":
            # Match against highest bid
            while self.bids and (-self.bids[0].sort_key) >= price and quantity > 0:
                best_bid = self.bids[0]
                trade_qty = min(quantity, best_bid.quantity)
                trade_price = best_bid.price_sync

                executed_trades.append({
                    "asset": self.asset,
                    "buyer_id": best_bid.agent_id,
                    "seller_id": agent_id,
                    "price_sync": trade_price,
                    "quantity": trade_qty,
                    "volume_sync": trade_price * trade_qty,
                    "timestamp": now
                })

                quantity -= trade_qty
                best_bid.quantity -= trade_qty
                self.last_clearing_price = trade_price

                if best_bid.quantity <= 0:
                    heapq.heappop(self.bids)

            if quantity > 0:
                heapq.heappush(self.asks, Order(
                    sort_key=price,
                    order_id=order_id,
                    agent_id=agent_id,
                    asset=self.asset,
                    side="SELL",
                    price_sync=price,
                    quantity=quantity,
                    timestamp=now
                ))

        self.trade_history.extend(executed_trades)
        return executed_trades

    def get_orderbook_depth(self) -> Dict[str, Any]:
        """
        Returns top bids and asks depth.
        """
        top_bid = -self.bids[0].sort_key if self.bids else 0.0
        top_ask = self.asks[0].sort_key if self.asks else 0.0
        spread = max(0.0, top_ask - top_bid) if top_ask and top_bid else 0.0

        return {
            "asset": self.asset,
            "best_bid": top_bid,
            "best_ask": top_ask,
            "spread": spread,
            "bids_count": len(self.bids),
            "asks_count": len(self.asks),
            "total_trades": len(self.trade_history),
            "last_price": self.last_clearing_price
        }

