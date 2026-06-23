#!/usr/bin/env python3
"""Send concurrent OpenAI-compatible chat requests to an SGLang server."""

import argparse
import concurrent.futures
import json
import statistics
import time
import urllib.request


def send_one(index: int, args: argparse.Namespace) -> dict:
    url = f"{args.base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": args.model,
        "messages": [{"role": "user", "content": f"{args.prompt} Request #{index}"}],
        "temperature": args.temperature,
        "max_tokens": args.max_tokens,
        "stream": False,
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    start = time.perf_counter()
    with urllib.request.urlopen(request, timeout=300) as response:
        body = response.read().decode("utf-8")
    latency = time.perf_counter() - start
    data = json.loads(body)
    usage = data.get("usage") or {}
    return {
        "index": index,
        "latency_sec": latency,
        "completion_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:30000/v1")
    parser.add_argument("--model", required=True)
    parser.add_argument("--prompt", default="Explain the difference between prefill and decode.")
    parser.add_argument("--num-requests", type=int, default=8)
    parser.add_argument("--concurrency", type=int, default=4)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=128)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    start = time.perf_counter()
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = [executor.submit(send_one, index, args) for index in range(args.num_requests)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            print(json.dumps(result, ensure_ascii=False))
    total = time.perf_counter() - start
    latencies = [item["latency_sec"] for item in results]
    print("summary")
    print(f"requests={len(results)} concurrency={args.concurrency} total_sec={total:.3f}")
    print(f"latency_avg_sec={statistics.mean(latencies):.3f}")
    print(f"latency_min_sec={min(latencies):.3f}")
    print(f"latency_max_sec={max(latencies):.3f}")


if __name__ == "__main__":
    main()
