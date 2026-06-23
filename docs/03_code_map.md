# 03 - 源码地图：第一次读 SGLang 代码看哪里

本文件是源码导读入口。由于 SGLang 版本演进很快，具体文件名和类名请以你本地 clone 的真实 SGLang 仓库为准。本项目先提供阅读顺序和定位方法。

## 推荐准备

```bash
git clone https://github.com/sgl-project/sglang.git ../sglang
cd ../sglang
rg "launch_server|OpenAI|chat/completions|Scheduler|KVCache|stream" python -n
```

## 阅读顺序

### 1. Server 启动入口

先找：

```bash
rg "launch_server" python -n
```

目标问题：

- `python -m sglang.launch_server` 最终进入哪个函数？
- server args 在哪里定义？
- host、port、model-path 如何传递？

### 2. OpenAI-compatible API 层

查找：

```bash
rg "chat/completions|completions|OpenAI" python -n
```

目标问题：

- `/v1/chat/completions` 路由在哪里？
- request body 如何变成内部 request？
- streaming 和 non-streaming 分支在哪里分开？

### 3. Sampling Params

查找：

```bash
rg "temperature|top_p|max_tokens|sampling" python/sglang -n
```

目标问题：

- OpenAI 参数如何映射到 SGLang 内部参数？
- 默认值在哪里设置？
- 非法参数在哪里报错？

### 4. Scheduler

查找：

```bash
rg "class .*Scheduler|schedule|prefill|decode" python/sglang -n
```

目标问题：

- 请求什么时候进入队列？
- prefill batch 和 decode batch 如何组织？
- 哪些条件会影响调度？

### 5. Model Executor

查找：

```bash
rg "forward|ModelRunner|Executor|model_runner" python/sglang -n
```

目标问题：

- 真正调用模型 forward 的位置在哪里？
- input ids、positions、KV cache metadata 如何传入？
- logits 如何进入 sampling？

### 6. KV Cache / Prefix Cache

查找：

```bash
rg "KV|cache|prefix|Radix" python/sglang -n
```

目标问题：

- KV cache block 如何分配？
- prefix cache 如何命中？
- cache miss 和 cache hit 对 TTFT 有什么影响？

### 7. Streaming Response

查找：

```bash
rg "stream|yield|ServerSentEvent|chunk" python/sglang -n
```

目标问题：

- token chunk 从哪里 yield 出来？
- client 看到的 delta content 是在哪里构造的？
- client 断开连接时如何处理？

## Rookie 读源码原则

1. 不要从 repo 根目录随机读。
2. 每次只追一个请求对象。
3. 先画图，再读细节。
4. 优先理解数据结构流动，而不是每个优化细节。
5. 看到复杂 CUDA / Triton backend 可以先跳过，只记录接口。
