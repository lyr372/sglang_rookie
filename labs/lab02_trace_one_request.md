# Lab 02 - Trace 一次请求

## Goal

从 client 侧观察一次请求的 latency，并为后续源码 trace 建立 stage 模型。

## Run

```bash
python scripts/send_chat_request.py \
  --base-url http://127.0.0.1:30000/v1 \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --prompt "用 bullet points 解释 prefill 和 decode 的区别。" \
  --max-tokens 128
```

## Observe

脚本会打印：

- response latency
- response content
- usage 信息，如果 server 返回 usage

## Code Reading

在真实 SGLang 源码中查找这些 stage：

```bash
cd ../sglang
rg "chat/completions|tokenizer|prefill|decode|stream" python/sglang -n
```

把你找到的位置填入下面表格：

| Stage | File / Function | Notes |
| --- | --- | --- |
| HTTP received |  |  |
| Parse request |  |  |
| Tokenize |  |  |
| Scheduler enqueue |  |  |
| Prefill |  |  |
| Decode |  |  |
| Response |  |  |

## Exercise

不要一开始大范围改代码。先只加一条日志，例如：

```text
[rookie-trace] stage=parse_openai_request
```

然后重新跑本实验，确认日志出现。
