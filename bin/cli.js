#!/usr/bin/env node
"use strict";

const { StockwaaleClient } = require("../index.js");

function printJson(value) {
  process.stdout.write(`${JSON.stringify(value, null, 2)}\n`);
}

function usage() {
  process.stderr.write([
    "Usage: stockwaale-mcp <command>",
    "",
    "Commands:",
    "  manifest              Fetch the hosted MCP manifest",
    "  mcp-config            Print a client config snippet for the hosted MCP endpoint",
    "  price <SYMBOL>        Fetch latest price context for a symbol",
    "",
    "Environment:",
    "  STOCKWAALE_API_KEY    API key for protected endpoints",
    "  STOCKWAALE_BASE_URL   Override hosted API base URL"
  ].join("\n"));
  process.stderr.write("\n");
}

async function main() {
  const [command, ...args] = process.argv.slice(2);
  const client = new StockwaaleClient();

  if (!command || command === "--help" || command === "-h") {
    usage();
    return;
  }

  if (command === "manifest") {
    printJson(await client.manifest());
    return;
  }

  if (command === "mcp-config") {
    printJson({
      mcpServers: {
        stockwaale: {
          http: {
            url: client.mcpUrl
          }
        }
      }
    });
    return;
  }

  if (command === "price") {
    const [symbol] = args;
    if (!symbol) {
      throw new Error("price requires a stock symbol");
    }
    printJson(await client.price(symbol));
    return;
  }

  throw new Error(`Unknown command: ${command}`);
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exit(1);
});
