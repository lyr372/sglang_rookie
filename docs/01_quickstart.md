# 01 - Quickstart：使用真实 SGLang 跑通服务

本项目要求使用真实 SGLang，而不是 mock server。你可以使用 pip 安装版本，也可以 clone SGLang 源码后 editable install。源码导读阶段推荐使用源码安装。

## 方案 A：pip 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install "sglang[all]"
```

## 方案 B：源码安装，推荐用于源码导读

```bash
git clone https://github.com/sgl-project/sglang.git ../sglang
cd ../sglang
pip install -e "python[all]"
cd ../sglang_rookie
```

> 如果你的机器没有合适 GPU，可以先阅读文档和脚本；真正启动 server 建议在 CUDA 环境执行。

## 启动 SGLang Server

选择一个可用模型。下面示例使用 Hugging Face model id，你也可以替换成本地模型路径。

```bash
python -m sglang.launch_server \
  --model-path meta-llama/Llama-3.1-8B-Instruct \
  --host 127.0.0.1 \
  --port 30000
```

如果模型需要 Hugging Face 权限：

```bash
export HF_TOKEN=your_huggingface_token
```

## 发送一次 Chat Completion 请求

```bash
python scripts/send_chat_request.py \
  --base-url http://127.0.0.1:30000/v1 \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --prompt "用三句话解释 SGLang 是什么。"
```

## 使用 curl 验证 server

```bash
curl http://127.0.0.1:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.1-8B-Instruct",
    "messages": [{"role": "user", "content": "hello"}],
    "max_tokens": 32
  }'
```

## 常见问题

### ModuleNotFoundError: No module named sglang

确认你激活了正确的 Python environment，并安装了 SGLang：

```bash
python -c "import sglang; print(sglang.__file__)"
```

### CUDA / torch 版本错误

SGLang 依赖底层 GPU runtime、PyTorch、attention backend。先用下面命令确认 GPU 可见：

```bash
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no cuda')"
```

### gated model 无权限

更换公开小模型，或者设置 `HF_TOKEN`。
