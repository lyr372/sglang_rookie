# sglang_rookie

一个面向 rookie 的 SGLang 实战导读项目：先用真实 SGLang 跑通 LLM inference，再从源码入口、请求链路、Scheduler、Streaming、KV Cache 等关键路径建立整体认知。

> 目标：不是替代 SGLang 官方文档，而是提供一条“能跑起来、能看懂链路、能做关键实验、能继续读源码”的最小学习路径。

## MVP 学习路径

1. [全局认知：SGLang 是什么](docs/00_overview.md)
2. [Quickstart：使用真实 SGLang 跑通服务](docs/01_quickstart.md)
3. [请求生命周期：从 HTTP Request 到 Token](docs/02_request_lifecycle.md)
4. [源码地图：第一次读 SGLang 代码看哪里](docs/03_code_map.md)
5. [Lab 01：最小 Server 与一次请求](labs/lab01_minimal_server.md)
6. [Lab 02：Trace 一次请求](labs/lab02_trace_one_request.md)
7. [Lab 03：Streaming Response 观察](labs/lab03_streaming_response.md)

## 项目定位

- **rookie guide**：用中文解释核心概念，命令和代码保持英文。
- **源码导读**：围绕真实 SGLang 的源码模块建立 code map。
- **关键实验**：每个实验都对应一个核心问题，例如请求链路、首 token 延迟、streaming chunk。
- **MVP 优先**：第一版只覆盖单机单模型、OpenAI-compatible API、请求追踪和 streaming。

## 预期环境

- Python 3.10+
- CUDA GPU 环境优先
- 已安装或准备安装真实 SGLang
- 可访问 Hugging Face 模型仓库，或已有本地模型路径

## 脚本

- `scripts/send_chat_request.py`：调用 OpenAI-compatible `/v1/chat/completions`。
- `scripts/send_batch_requests.py`：并发发送请求，观察 latency 和 throughput。

## 官方资料入口

- SGLang 官方文档：https://docs.sglang.ai/
- SGLang GitHub：https://github.com/sgl-project/sglang
