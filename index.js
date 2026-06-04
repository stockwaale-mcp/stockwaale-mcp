"use strict";

const DEFAULT_BASE_URL = "https://api.stockwaale.com";

class StockwaaleClient {
  constructor(options = {}) {
    this.baseUrl = (options.baseUrl || process.env.STOCKWAALE_BASE_URL || DEFAULT_BASE_URL).replace(/\/+$/, "");
    this.apiKey = options.apiKey || process.env.STOCKWAALE_API_KEY || "";
    this.firebaseToken = options.firebaseToken || process.env.FIREBASE_ID_TOKEN || "";
  }

  async request(method, path, options = {}) {
    const url = new URL(path, `${this.baseUrl}/`);
    const query = options.query || {};
    for (const [key, value] of Object.entries(query)) {
      if (value !== undefined && value !== null && value !== "") {
        url.searchParams.set(key, String(value));
      }
    }

    const headers = { Accept: "application/json" };
    const authToken = options.authToken || this.apiKey;
    if (authToken) {
      headers.Authorization = `Bearer ${authToken}`;
    }

    let body;
    if (options.body !== undefined) {
      headers["Content-Type"] = "application/json";
      body = JSON.stringify(options.body);
    }

    const response = await fetch(url, { method, headers, body });
    const text = await response.text();
    let payload = null;
    if (text) {
      try {
        payload = JSON.parse(text);
      } catch {
        payload = text;
      }
    }

    if (!response.ok) {
      const message = payload && payload.detail ? payload.detail : `Stockwaale API returned ${response.status}`;
      const error = new Error(message);
      error.status = response.status;
      error.payload = payload;
      throw error;
    }

    return payload;
  }

  manifest() {
    return this.request("GET", "/.well-known/mcp.json");
  }

  stocks(params = {}) {
    return this.request("GET", "/api/stocks", { query: params });
  }

  price(symbol) {
    return this.request("GET", `/api/stock/${encodeURIComponent(symbol)}/price`);
  }

  features(symbol) {
    return this.request("GET", `/api/stock/${encodeURIComponent(symbol)}/features`);
  }

  signalContext(symbol) {
    return this.request("GET", `/api/stock/${encodeURIComponent(symbol)}/signal-context`);
  }

  screen(filters = {}) {
    return this.request("POST", "/api/screen", { body: filters });
  }

  compare(symbols, features = []) {
    return this.request("POST", "/api/compare", { body: { symbols, features } });
  }

  complianceReview(content) {
    return this.request("POST", "/api/compliance/review", { body: { content } });
  }

  createApiKey(name = "Default key", firebaseToken = this.firebaseToken) {
    return this.request("POST", "/api/account/api-keys", { authToken: firebaseToken, body: { name } });
  }

  listApiKeys(firebaseToken = this.firebaseToken) {
    return this.request("GET", "/api/account/api-keys", { authToken: firebaseToken });
  }

  revokeApiKey(prefix, firebaseToken = this.firebaseToken) {
    return this.request("DELETE", `/api/account/api-keys/${encodeURIComponent(prefix)}`, { authToken: firebaseToken });
  }

  get mcpUrl() {
    return `${this.baseUrl}/mcp`;
  }

  get sseUrl() {
    return `${this.baseUrl}/mcp/sse`;
  }
}

const MCP_ENDPOINTS = {
  streamableHttp: "/mcp",
  sse: "/mcp/sse"
};

module.exports = {
  DEFAULT_BASE_URL,
  MCP_ENDPOINTS,
  StockwaaleClient
};
