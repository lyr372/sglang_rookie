# Lab 03 - Streaming Response 观察

## Goal

观察 streaming 模式下 token chunk 如何逐步返回，并理解 TTFT 与 inter-token latency。

## Run

```bash
python scripts/send_chat_request.py \
  --base-url http://127.0.0.1:30000/v1 \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --prompt "Write a short story about a scheduler and a KV cache." \
  --max-tokens 128 \
  --stream
```

## Observe

记录：

- first chunk latency
- 每个 chunk 的到达时间
- total latency
- 输出 token 是否连续

## Code Reading

```bash
cd ../sglang
rg "stream|chunk|delta|yield" python/sglang -n
```

回答：

1. streaming response 的 chunk 在哪里构造？
2. token id 在哪里变成 text？
3. non-streaming 和 streaming 分支在哪里分开？

## Summary

完成本 Lab 后，你应该能解释：为什么 first token latency 和后续 token latency 不是一回事。
