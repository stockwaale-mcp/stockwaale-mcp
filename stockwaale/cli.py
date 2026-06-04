import argparse
import json
import sys

from .client import StockwaaleClient


def _print_json(value: object) -> None:
    print(json.dumps(value, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(prog="stockwaale-mcp")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("manifest", help="Fetch the hosted MCP manifest")
    subparsers.add_parser("mcp-config", help="Print a client config snippet for the hosted MCP endpoint")
    price_parser = subparsers.add_parser("price", help="Fetch latest price context for a symbol")
    price_parser.add_argument("symbol")

    args = parser.parse_args()
    client = StockwaaleClient()

    try:
        if args.command == "manifest":
            _print_json(client.manifest())
        elif args.command == "mcp-config":
            _print_json({"mcpServers": {"stockwaale": {"http": {"url": client.mcp_url}}}})
        elif args.command == "price":
            _print_json(client.price(args.symbol))
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
