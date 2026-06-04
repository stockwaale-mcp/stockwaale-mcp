# Stockwaale MCP

[![PyPI Version](https://img.shields.io/pypi/v/stockwaale-mcp?color=blue)](https://pypi.org/project/stockwaale-mcp/)
[![npm Scoped Version](https://img.shields.io/npm/v/@stockwaale/stockwaale-mcp?color=green)](https://www.npmjs.com/package/@stockwaale/stockwaale-mcp)

Stockwaale is a hosted intelligence layer for Indian equities. It exposes verified market context through REST APIs and a remote Model Context Protocol endpoint for AI agents, builders, and research workflows.

The public PyPI and npm packages are thin clients. They do not contain the private FastAPI server, Lambda handler, MongoDB code, database credentials, or business deployment logic.

## Hosted Endpoints

- MCP Streamable HTTP: `https://api.stockwaale.com/mcp`
- MCP SSE: `https://api.stockwaale.com/mcp/sse`
- Discovery manifest: `https://api.stockwaale.com/.well-known/mcp.json`
- Product site: `https://stockwaale.com`

## Install

Python:

```bash
pip install stockwaale-mcp
```

Node.js:

```bash
npm install @stockwaale/stockwaale-mcp
```

## Python Usage

```python
from stockwaale import StockwaaleClient

client = StockwaaleClient(api_key="sk_live_xxx")
print(client.price("RELIANCE"))
print(client.screen(regime="Bullish Expansion", min_rsi=55))
```

The client also reads:

```bash
export STOCKWAALE_API_KEY=sk_live_xxx
export STOCKWAALE_BASE_URL=https://api.stockwaale.com
```

CLI:

```bash
stockwaale-mcp manifest
stockwaale-mcp mcp-config
stockwaale-mcp price RELIANCE
```

## Node.js Usage

```js
const { StockwaaleClient } = require("@stockwaale/stockwaale-mcp");

const client = new StockwaaleClient({ apiKey: "sk_live_xxx" });

async function main() {
  console.log(await client.price("RELIANCE"));
  console.log(await client.screen({ regime: "Bullish Expansion", min_rsi: 55 }));
}

main();
```

CLI:

```bash
npx @stockwaale/stockwaale-mcp manifest
npx @stockwaale/stockwaale-mcp mcp-config
npx @stockwaale/stockwaale-mcp price RELIANCE
```

## MCP Client Config

Use the hosted remote endpoint from Claude Desktop, Cursor, VS Code extensions, or any MCP client that supports Streamable HTTP:

```json
{
  "mcpServers": {
    "stockwaale": {
      "http": {
        "url": "https://api.stockwaale.com/mcp"
      }
    }
  }
}
```

For protected plans, send the API key as `Authorization: Bearer <key>` or `X-API-Key: <key>` where the client supports custom headers.

## API Keys

Do not publish fixed API keys in package code, README examples, GitHub, PyPI, or npm.

Production API keys are created per user or organization in the hosted backend after Firebase login. The free plan defaults to 50 API calls per day. Keys are stored hashed in the database and shown only once at creation time.

Fixed keys in `STOCKWAALE_API_KEYS` are only for admin/test bootstrap access and private smoke checks. They should not be customer keys.

Lambda environment variables or AWS Secrets Manager should hold platform secrets such as MongoDB credentials, Firebase service-account configuration, JWT signing secrets, webhook secrets, and bootstrap admin credentials.

## Private Deployment Boundary

The private Lambda deployment can include:

- `lambda_handler.py`
- FastAPI application code
- MCP server implementation
- MongoDB integration
- AWS Secrets Manager integration
- CloudFront and Lambda deployment templates

Those files should stay in a private repository or private deployment artifact. PyPI and npm package artifacts should ship only the public clients and documentation needed by customers.

## Compliance

Stockwaale provides market data context, derived indicators, and research infrastructure. It does not provide investment advice, guaranteed returns, financial planning, stock tips, or SEBI-registered advisory services.
