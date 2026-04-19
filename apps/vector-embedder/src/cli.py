"""
CLI interface for the embedding pipeline.

Reads JSON from stdin, embeds structured items, and writes JSON to stdout.
"""

import json
import sys
from .pipeline import embed_items


def _error(message, details = None, code = 2):
    json.dump({"error": message, "details": details}, sys.stdout)
    raise SystemExit(code)


def main():
    try:
        items = json.load(sys.stdin)
        resp = embed_items(items)
        json.dump(resp, sys.stdout)
    except Exception as e:
        _error("Embedding failed", {"exception": str(e)})


if __name__ == "__main__":
    main()