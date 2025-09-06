"""
server.py - Windows-safe FastMCP server for Zerodha
"""

import sys
import asyncio
from pydantic import BaseModel, Field
from fastmcp import FastMCP
from zerodha_client import ZerodhaClient

# --- Windows async fix ---
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# --- Initialize Zerodha client ---
client = ZerodhaClient()

# --- Initialize FastMCP ---
mcp = FastMCP("Zerodha MCP")

# -------------------- Models --------------------
class Profile(BaseModel):
    user_id: str
    user_name: str
    email: str

class Holding(BaseModel):
    tradingsymbol: str
    quantity: float
    average_price: float
    last_price: float
    pnl: float

class OrderResult(BaseModel):
    order_id: str = Field(description="Zerodha order ID")

# -------------------- MCP Tools --------------------
@mcp.tool()
async def health_check() -> str:
    """Check if server is alive"""
    return "✅ Server is running"

@mcp.tool()
async def get_profile() -> Profile:
    """Fetch Zerodha account profile"""
    data = await asyncio.to_thread(client.profile)
    return Profile(
        user_id=data.get("user_id"),
        user_name=data.get("user_name"),
        email=data.get("email"),
    )

@mcp.tool()
async def get_holdings() -> list[Holding]:
    """Fetch current holdings"""
    holdings = await asyncio.to_thread(client.holdings)
    return [
        Holding(
            tradingsymbol=h["tradingsymbol"],
            quantity=h["quantity"],
            average_price=h["average_price"],
            last_price=h["last_price"],
            pnl=h["pnl"],
        )
        for h in holdings
    ]

@mcp.tool()
async def place_market_order(
    exchange: str,
    tradingsymbol: str,
    transaction_type: str,
    quantity: int,
    product: str = "CNC",
) -> OrderResult:
    """Place a market order"""
    resp = await asyncio.to_thread(
        client.place_market_order,
        exchange=exchange,
        tradingsymbol=tradingsymbol,
        transaction_type=transaction_type,
        quantity=quantity,
        product=product,
    )
    return OrderResult(order_id=resp["order_id"])

@mcp.tool()
async def cancel_order(order_id: str) -> dict:
    """Cancel an order by ID"""
    resp = await asyncio.to_thread(client.cancel_order, order_id)
    return {"status": "cancelled", "order_id": order_id, "resp": str(resp)}

# -------------------- Main --------------------
if __name__ == "__main__":
    print("Starting FastMCP Zerodha server on Windows...")
    mcp.run()
