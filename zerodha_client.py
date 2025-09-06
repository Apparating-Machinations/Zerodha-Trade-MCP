import json
import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv
from kiteconnect import KiteConnect

# Where we persist the access token after login
TOKEN_PATH = os.path.join(os.path.dirname(__file__), "token.json")


class ZerodhaClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        access_token: Optional[str] = None,
    ):
        load_dotenv()
        self.api_key = api_key or os.getenv("API_KEY")
        self.api_secret = api_secret or os.getenv("API_SECRET")

        if not self.api_key or not self.api_secret:
            raise RuntimeError(
                "API_KEY and API_SECRET must be set in .env or passed explicitly."
            )

        self.kite = KiteConnect(api_key=self.api_key)

        # Try access_token (passed/env/file)
        token = access_token or os.getenv("ACCESS_TOKEN") or self._read_token_file()
        if token:
            self.kite.set_access_token(token)

    # --- token helpers ---
    def _read_token_file(self) -> Optional[str]:
        try:
            if os.path.exists(TOKEN_PATH):
                with open(TOKEN_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("access_token")
        except Exception:
            pass
        return None

    def _write_token_file(self, token: str) -> None:
        with open(TOKEN_PATH, "w", encoding="utf-8") as f:
            json.dump({"access_token": token}, f, indent=2)

    # --- auth/login flow ---
    def get_login_url(self) -> str:
        """Get the login URL for Zerodha where you authorize and get request_token."""
        return self.kite.login_url()

    def exchange_request_token(self, request_token: str) -> Dict[str, Any]:
        """Exchange request_token for access_token, persist it, and return session details."""
        data = self.kite.generate_session(request_token, api_secret=self.api_secret)
        token = data["access_token"]
        self.kite.set_access_token(token)
        self._write_token_file(token)
        return data

    def set_access_token(self, access_token: str) -> None:
        """Manually set (and persist) an existing access token."""
        self.kite.set_access_token(access_token)
        self._write_token_file(access_token)

        def _handle_call(self, func, *args, **kwargs):
            """Helper to wrap KiteConnect calls with nicer error messages."""
            try:
                return func(*args, **kwargs)
            except TokenException:
                raise RuntimeError(
                    "Access token has expired or is invalid. "
                    "Run 'login_flow.py' to refresh."
                )
            except KiteException as e:
                raise RuntimeError(f"Kite API error: {e}")

    # --- account/data methods ---
    def profile(self) -> Dict[str, Any]:
        return self.kite.profile()

    def holdings(self) -> List[Dict[str, Any]]:
        return self.kite.holdings()

    def positions(self) -> Dict[str, Any]:
        return self.kite.positions()

    def margins(self) -> Dict[str, Any]:
        return self.kite.margins(segment="equity")

    def ltp(self, instruments: List[str]) -> Dict[str, Any]:
        # instruments like ["NSE:INFY", "NSE:TCS"]
        return self.kite.ltp(instruments)

    # --- trading methods ---
    def place_market_order(
        self,
        *,
        exchange: str,
        tradingsymbol: str,
        transaction_type: str,
        quantity: int,
        product: str = "CNC",
    ) -> Dict[str, Any]:
        return self.kite.place_order(
            variety=KiteConnect.VARIETY_REGULAR,
            exchange=exchange,
            tradingsymbol=tradingsymbol,
            transaction_type=transaction_type,
            quantity=quantity,
            order_type=KiteConnect.ORDER_TYPE_MARKET,
            product=product,
        )

    def place_limit_order(
        self,
        *,
        exchange: str,
        tradingsymbol: str,
        transaction_type: str,
        quantity: int,
        price: float,
        product: str = "CNC",
    ) -> Dict[str, Any]:
        return self.kite.place_order(
            variety=KiteConnect.VARIETY_REGULAR,
            exchange=exchange,
            tradingsymbol=tradingsymbol,
            transaction_type=transaction_type,
            quantity=quantity,
            price=price,
            order_type=KiteConnect.ORDER_TYPE_LIMIT,
            product=product,
        )

    def cancel_order(self, order_id: str) -> Dict[str, Any]:
        return self.kite.cancel_order(
            variety=KiteConnect.VARIETY_REGULAR, order_id=order_id
        )
