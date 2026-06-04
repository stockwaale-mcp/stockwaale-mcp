# Stockwaale MCP Client SDK

[![PyPI Version](https://img.shields.io/pypi/v/stockwaale-mcp?color=blue&logo=python&logoColor=white)](https://pypi.org/project/stockwaale-mcp/)
[![npm Scoped Version](https://img.shields.io/npm/v/@stockwaale/stockwaale-mcp?color=green&logo=npm&logoColor=white)](https://www.npmjs.com/package/@stockwaale/stockwaale-mcp)

**Stockwaale** is a hosted intelligence and analytics layer for Indian equities. It exposes verified real-time and historical market context, technical indicators, news analysis, and regulatory checks through standard REST APIs and a remote **Model Context Protocol (MCP)** endpoint.

This SDK provides lightweight Python and Node.js clients to interact with the Stockwaale platform.

---

## 🌐 Hosted Endpoints
- **Product & Dashboard**: [https://stockwaale.com](https://stockwaale.com)
- **MCP Streamable HTTP Endpoint**: `https://api.stockwaale.com/mcp`
- **MCP Server-Sent Events (SSE)**: `https://api.stockwaale.com/mcp/sse`
- **Discovery Manifest**: `https://api.stockwaale.com/.well-known/mcp.json`

---

## 📦 Installation

### Python Client
```bash
pip install stockwaale-mcp
```

### Node.js Client
```bash
npm install @stockwaale/stockwaale-mcp
```

---

## 🛠️ Features & Available Capabilities

The Stockwaale client provides access to the following operations:
1. **Price Retrieval**: Latest daily closing price, exchange, and token metadata.
2. **OHLCV Data**: Historical daily and hourly candles.
3. **Intraday Candles**: Real-time and historical intraday candles (1m to 1h timeframes).
4. **Technical Indicators**: Precomputed and on-demand indicators (RSI, ATR, EMAs, SMAs, Volatility Z-Scores).
5. **Market Regime Classification**: Volatility and trend categorization (e.g. Bullish Expansion, Consolidation).
6. **Market News & Sentiment**: Aggregated headlines, sentiment scoring, and market impact analysis.
7. **Adviser/Analyst Registry**: Search SEBI registered investment advisers and research analysts.
8. **Compliance Checks**: Deterministic screening checks for financial publications/UI copy.

---

## 🐍 Python SDK Usage

### Programmatic Client
```python
from stockwaale import StockwaaleClient

# Initialize client (uses STOCKWAALE_API_KEY env var by default if api_key parameter is omitted)
client = StockwaaleClient(api_key="sk_live_your_api_key_here")

# 1. Fetch latest price
price_info = client.price("RELIANCE")
print(f"Reliance Price: {price_info['price']} ({price_info['exchange']})")

# 2. Get technical indicators
indicators = client.features("TCS")
print(f"TCS RSI-14: {indicators['rsi14']}")

# 3. Screen stocks based on technical criteria
bullish_stocks = client.screen(regime="Bullish Expansion", min_rsi=55)
print("Bullish Expansion Stocks:", [s['symbol'] for s in bullish_stocks])

# 4. Compare multiple stocks side-by-side
comparison = client.compare(symbols=["RELIANCE", "TCS", "INFY"])
print("Comparison Matrix:", comparison)
```

### Environment Variables
You can customize the client using environment variables:
```bash
export STOCKWAALE_API_KEY="sk_live_your_api_key_here"
export STOCKWAALE_BASE_URL="https://api.stockwaale.com"
```

### Command Line Interface (CLI)
```bash
# Display server manifest
stockwaale-mcp manifest

# Fetch a stock price
stockwaale-mcp price RELIANCE
```

---

## ☕ Node.js SDK Usage

### Programmatic Client
```javascript
const { StockwaaleClient } = require("@stockwaale/stockwaale-mcp");

// Initialize client
const client = new StockwaaleClient({ apiKey: "sk_live_your_api_key_here" });

async function run() {
  try {
    // 1. Fetch latest price
    const priceInfo = await client.price("RELIANCE");
    console.log(`Reliance Price: ${priceInfo.price}`);

    // 2. Query technical indicators
    const indicators = await client.features("TCS");
    console.log(`TCS RSI-14: ${indicators.rsi14}`);

    // 3. Screen stocks
    const bullishStocks = await client.screen({ regime: "Bullish Expansion", minRsi: 55 });
    console.log("Bullish Stocks:", bullishStocks.map(s => s.symbol));
  } catch (error) {
    console.error("Error communicating with Stockwaale:", error);
  }
}

run();
```

### Command Line Interface (CLI)
```bash
# Print server manifest
npx @stockwaale/stockwaale-mcp manifest

# Fetch a stock price
npx @stockwaale/stockwaale-mcp price RELIANCE
```

---

## 🤖 Model Context Protocol (MCP) Setup

You can connect Stockwaale's intelligence layer directly to AI assistants like Claude Desktop, Cursor, or VS Code Extensions.

### Claude Desktop Configuration
Add the server configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "stockwaale": {
      "http": {
        "url": "https://api.stockwaale.com/mcp",
        "headers": {
          "Authorization": "Bearer sk_live_your_api_key_here"
        }
      }
    }
  }
}
```

*Note: For platforms or LLM clients that do not support custom request headers, you can pass your API key via query parameter (if supported by your client proxy) or configure client-side environment variables.*

---

## 🛡️ Terms & Compliance

Stockwaale provides market data context, statistical analyses, and regulatory registry lookups for educational and research purposes.

> [!WARNING]
> Stockwaale does **not** provide investment advice, buy/sell recommendations, financial planning, or SEBI-registered portfolio advisory services. All research and data are provided "as-is" without warranty.
