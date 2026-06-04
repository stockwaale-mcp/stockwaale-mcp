import json
import os
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://api.stockwaale.com"
MCP_ENDPOINTS = {
    "streamable_http": "/mcp",
    "sse": "/mcp/sse",
}


class StockwaaleClient:
    """Small public client for the hosted Stockwaale API."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: float = 30.0,
        firebase_token: str | None = None,
    ) -> None:
        self.base_url = (base_url or os.getenv("STOCKWAALE_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.api_key = api_key or os.getenv("STOCKWAALE_API_KEY") or ""
        self.firebase_token = firebase_token or os.getenv("FIREBASE_ID_TOKEN") or ""
        self.timeout = timeout

    @property
    def mcp_url(self) -> str:
        return f"{self.base_url}/mcp"

    @property
    def sse_url(self) -> str:
        return f"{self.base_url}/mcp/sse"

    def request(
        self,
        method: str,
        path: str,
        *,
        query: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        auth_token: str | None = None,
    ) -> Any:
        url = urljoin(f"{self.base_url}/", path.lstrip("/"))
        if query:
            filtered = {key: value for key, value in query.items() if value not in (None, "")}
            if filtered:
                url = f"{url}?{urlencode(filtered)}"

        headers = {"Accept": "application/json"}
        data = None
        if body is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(body).encode("utf-8")
        token = auth_token if auth_token is not None else self.api_key
        if token:
            headers["Authorization"] = f"Bearer {token}"

        request = Request(url, data=data, headers=headers, method=method.upper())
        try:
            with urlopen(request, timeout=self.timeout) as response:
                payload = response.read().decode("utf-8")
                return json.loads(payload) if payload else None
        except HTTPError as exc:
            payload = exc.read().decode("utf-8")
            try:
                detail = json.loads(payload)
            except json.JSONDecodeError:
                detail = payload
            raise RuntimeError(f"Stockwaale API returned {exc.code}: {detail}") from exc

    def manifest(self) -> Any:
        return self.request("GET", "/.well-known/mcp.json")

    def stocks(self, **params: Any) -> Any:
        return self.request("GET", "/api/stocks", query=params)

    def price(self, symbol: str) -> Any:
        return self.request("GET", f"/api/stock/{symbol}/price")

    def features(self, symbol: str) -> Any:
        return self.request("GET", f"/api/stock/{symbol}/features")

    def signal_context(self, symbol: str) -> Any:
        return self.request("GET", f"/api/stock/{symbol}/signal-context")

    def screen(self, **filters: Any) -> Any:
        return self.request("POST", "/api/screen", body=filters)

    def compare(self, symbols: list[str], features: list[str] | None = None) -> Any:
        return self.request("POST", "/api/compare", body={"symbols": symbols, "features": features or []})

    def compliance_review(self, content: str) -> Any:
        return self.request("POST", "/api/compliance/review", body={"content": content})

    def create_api_key(self, name: str = "Default key", firebase_token: str | None = None) -> Any:
        return self.request(
            "POST",
            "/api/account/api-keys",
            body={"name": name},
            auth_token=firebase_token or self.firebase_token,
        )

    def list_api_keys(self, firebase_token: str | None = None) -> Any:
        return self.request("GET", "/api/account/api-keys", auth_token=firebase_token or self.firebase_token)

    def revoke_api_key(self, prefix: str, firebase_token: str | None = None) -> Any:
        return self.request(
            "DELETE",
            f"/api/account/api-keys/{prefix}",
            auth_token=firebase_token or self.firebase_token,
        )
