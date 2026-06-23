# Lab 01 - 最小 Server 与一次请求

## Goal

使用真实 SGLang 启动一个 OpenAI-compatible server，并完成一次 chat completion 请求。

## Run

启动 server：

```bash
python -m sglang.launch_server \
  --model-path meta-llama/Llama-3.1-8B-Instruct \
  --host 127.0.0.1 \
  --port 30000
```

发送请求：

```bash
python scripts/send_chat_request.py \
  --base-url http://127.0.0.1:30000/v1 \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --prompt "Explain SGLang in three short sentences."
```

## Observe

记录：

- server 启动日志
- 模型加载时间
- 第一次请求耗时
- 输出文本

## Code Reading

在真实 SGLang 源码中执行：

```bash
cd ../sglang
rg "launch_server|chat/completions|OpenAI" python -n
```

回答：

1. server 启动入口在哪里？
2. `/v1/chat/completions` 路由在哪里？
3. 请求参数如何进入内部对象？

## Summary

完成本 Lab 后，你应该知道 SGLang server 如何启动，以及 OpenAI-compatible API 如何被调用。
