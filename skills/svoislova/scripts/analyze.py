#!/usr/bin/env python3
"""Call the svoislova analyze endpoint and print only the JSON result."""

from __future__ import annotations

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request
from typing import Any

DEFAULT_URL = "https://svoislova.ru/analyze"
DEFAULT_CA_FILE = "/etc/ssl/cert.pem"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="POST text to the svoislova analyze endpoint."
    )
    parser.add_argument(
        "--text",
        help="Text to analyze. If omitted, the script reads from stdin.",
    )
    parser.add_argument(
        "--url",
        default=os.environ.get("SVOISLOVA_ANALYZE_URL", DEFAULT_URL),
        help="Analyze endpoint URL.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=20.0,
        help="HTTP timeout in seconds.",
    )
    parser.add_argument(
        "--ca-file",
        default=(
            os.environ.get("SVOISLOVA_CA_FILE")
            or (DEFAULT_CA_FILE if os.path.exists(DEFAULT_CA_FILE) else None)
        ),
        help="Path to a CA bundle file for TLS verification.",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Print compact JSON without indentation.",
    )
    return parser.parse_args()


def read_text(cli_text: str | None) -> str:
    if cli_text is not None:
        return cli_text
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise RuntimeError("Provide --text or pipe input via stdin.")


def build_ssl_context(ca_file: str | None) -> ssl.SSLContext | None:
    if not ca_file:
        return None
    try:
        return ssl.create_default_context(cafile=ca_file)
    except OSError as exc:
        raise RuntimeError(f"Failed to load CA file '{ca_file}': {exc}") from exc


def post_analyze(
    url: str, content: str, timeout: float, ca_file: str | None
) -> dict[str, Any]:
    payload = json.dumps({"content": content}, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    context = build_ssl_context(ca_file)

    try:
        with urllib.request.urlopen(
            request,
            timeout=timeout,
            context=context,
        ) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"API returned HTTP {exc.code}: {details}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"API request failed: {exc.reason}") from exc

    try:
        data = json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError("API returned invalid JSON.") from exc

    if not isinstance(data, dict):
        raise RuntimeError("API response is not a JSON object.")

    return data


def main() -> int:
    args = parse_args()

    try:
        text = read_text(args.text)
        result = post_analyze(args.url, text, args.timeout, args.ca_file)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.compact:
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
