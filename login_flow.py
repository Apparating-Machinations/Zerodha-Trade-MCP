"""
login_flow.py

Run this script once every trading day to generate and store
a fresh Zerodha access token in `token.json`.

Steps:
1. Run: python login_flow.py
2. Open the login URL printed in your terminal.
3. Log in to Zerodha with your account.
4. Copy the `request_token` from the redirect URL.
5. Paste it back into the terminal when prompted.
"""

from zerodha_client import ZerodhaClient

def main():
    client = ZerodhaClient()

    # Step 1: Print login URL
    login_url = client.get_login_url()
    print("\n=== Zerodha Login ===")
    print("Open this URL in your browser and log in:")
    print(login_url)

    # Step 2: User pastes request_token
    request_token = input("\nPaste the request_token from the redirect URL: ").strip()

    # Step 3: Exchange request_token for access_token
    try:
        session = client.exchange_request_token(request_token)
        print("\n✅ Access token generated and saved to token.json")
        print("Token details (keep private):")
        print(session)
    except Exception as e:
        print("\n❌ Failed to exchange request token:", str(e))


if __name__ == "__main__":
    main()


# some read-only tests:
from zerodha_client import ZerodhaClient
c = ZerodhaClient()  # will load token.json / env
print("Profile:", c.profile())          # should return dict with user info
print("Holdings:", c.holdings())        # list
print("Positions:", c.positions())      # dict/day & net positions
