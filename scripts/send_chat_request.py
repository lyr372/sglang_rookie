#!/usr/bin/env python3
"""Send one OpenAI-compatible chat completion request to an SGLang server."""

import argparse
import json
import time
import urllib.error
import urllib.request


def build_payload(args: argparse.Namespace) -> dict:
    return {
        "model": args.model,
        "messages": [{"role": "user", "content": args.prompt}],
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "stream": args.stream,
    }


def post_json(url: str, payload: dict) -> urllib.response.addinfourl:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    return urllib.request.urlopen(request, timeout=300)


def run_non_stream(args: argparse.Namespace) -> None:
    url = f"{args.base_url.rstrip('/')}/chat/completions"
    payload = build_payload(args)
    start = time.perf_counter()
    try:
        with post_json(url, payload) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        print(exc.read().decode("utf-8"))
        raise
    latency = time.perf_counter() - start
    data = json.loads(body)
    print(f"latency_sec={latency:.3f}")
    print(json.dumps(data, ensure_ascii=False, indent=2))


def run_stream(args: argparse.Namespace) -> None:
    url = f"{args.base_url.rstrip('/')}/chat/completions"
    payload = build_payload(args)
    start = time.perf_counter()
    first_chunk_at = None
    try:
        with post_json(url, payload) as response:
            for raw_line in response:
                line = raw_line.decode("utf-8").strip()
                if not line:
                    continue
                now = time.perf_counter()
                if first_chunk_at is None:
                    first_chunk_at = now
                    print(f"ttft_sec={first_chunk_at - start:.3f}")
                print(f"chunk_at_sec={now - start:.3f} {line}")
    except urllib.error.HTTPError as exc:
        print(exc.read().decode("utf-8"))
        raise
    print(f"total_latency_sec={time.perf_counter() - start:.3f}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:30000/v1")
    parser.add_argument("--model", required=True)
    parser.add_argument("--prompt", default="Explain SGLang in three short sentences.")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=128)
    parser.add_argument("--stream", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.stream:
        run_stream(args)
    else:
        run_non_stream(args)


if __name__ == "__main__":
    main()
