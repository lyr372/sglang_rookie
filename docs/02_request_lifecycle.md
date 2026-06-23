# 02 - 请求生命周期：从 HTTP Request 到 Token

这一章的目标是建立代码阅读主线。你不需要一次看完所有文件，而是围绕“一次请求如何生成 token”来读。

## 生命周期总览

```text
1. client sends request
2. HTTP server receives request
3. OpenAI-compatible layer parses messages and sampling params
4. tokenizer converts prompt to token ids
5. scheduler enqueues request
6. model executor runs prefill
7. model executor runs decode loop
8. detokenizer converts token ids to text
9. server returns JSON or streaming chunks
```

## Prefill 和 Decode

### Prefill

Prefill 处理 prompt 的已有 token，通常计算量大，和 prompt length 强相关。

### Decode

Decode 每次生成一个或一小批新 token，依赖已有 KV cache，通常持续多轮。

理解这两个阶段，是理解首 token 延迟和持续 token throughput 的关键。

## 建议 trace 点

后续源码实验可以围绕这些 stage 加日志：

```text
[rookie-trace] stage=http_received request_id=...
[rookie-trace] stage=parse_openai_request request_id=...
[rookie-trace] stage=tokenized request_id=... input_tokens=...
[rookie-trace] stage=scheduler_enqueue request_id=...
[rookie-trace] stage=prefill_start request_id=...
[rookie-trace] stage=first_token request_id=... latency_ms=...
[rookie-trace] stage=decode_step request_id=... token_id=...
[rookie-trace] stage=stream_chunk request_id=... text=...
[rookie-trace] stage=finished request_id=... output_tokens=...
```

## 关键观察指标

| 指标 | 含义 |
| --- | --- |
| time to first token / TTFT | 从请求发出到第一个 token 返回的时间 |
| inter-token latency | 相邻 token chunk 的间隔 |
| end-to-end latency | 请求整体耗时 |
| output tokens | 生成 token 数 |
| throughput | 单位时间生成 token 数或完成请求数 |

## 推荐实验顺序

1. 非 streaming 请求：先看整体响应。
2. streaming 请求：观察每个 chunk。
3. 并发请求：观察排队和调度影响。
4. 共享 prefix 请求：观察 KV cache / prefix cache 相关行为。
