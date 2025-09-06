# Zerodha-Trade-MCP

This project provides a **Model Context Protocol (MCP) server** built with [FastMCP](https://pypi.org/project/fastmcp/) that allows an LLM interface (e.g., Claude Desktop) to interact programmatically with your **Zerodha trading account**.  

It enables safe, structured access to Zerodha APIs for tasks like retrieving account information, fetching market data, and placing/cancelling orders.

---

## Features
-  MCP-compliant server (Python-only, via FastMCP)  
-  Secure login flow with environment-based API keys  
-  Access profile, holdings, positions, and LTP data  
-  Place and cancel orders programmatically  
-  Async-safe wrappers for blocking Zerodha API calls  


