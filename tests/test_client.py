from stockwaale import StockwaaleClient


def test_endpoint_urls_are_stable():
    client = StockwaaleClient(base_url="https://api.stockwaale.com/")

    assert client.mcp_url == "https://api.stockwaale.com/mcp"
    assert client.sse_url == "https://api.stockwaale.com/mcp/sse"
