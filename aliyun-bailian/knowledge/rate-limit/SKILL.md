# 限流（Rate Limit）

> 更新时间：2026-04-12
> 来源：https://help.aliyun.com/zh/model-studio/rate-limit

---

## 概述

百炼平台按**主账号维度**限流（所有 RAM 子账号、所有业务空间、所有 API Key 的调用总和计算）。不同模型独立限流。

限流指标：
- **RPM**：每分钟请求数（Requests Per Minute）
- **TPM**：每分钟消耗 Token 数（Tokens Per Minute，含输入与输出）
- 可能按秒级限制：RPS = RPM/60，TPS = TPM/60

---

## 常见限流错误

| 错误信息 | 含义 |
|----------|------|
| `Requests rate limit exceeded` / `You exceeded your current requests list` | 调用频率触发限流（RPM） |
| `Allocated quota exceeded` / `You exceeded your current quota` | Token 消耗触发限流（TPM） |
| `Request rate increased too quickly` | 调用频率短时间激增，触发系统稳定性保护 |

---

## 主要模型限流（中国内地）

| 模型 | RPM | TPM |
|------|-----|-----|
| **qwen3-max** | 30,000 | 5,000,000 |
| **qwen-max** | 1,200 | — |
| **qwen3.6-plus** | 30,000 | 5,000,000 |
| **qwen3.5-plus** | 30,000 | 5,000,000 |
| **qwen-plus** | 30,000 | 5,000,000 |
| **qwen-plus-latest** | 15,000 | 1,200,000 |
| **qwen3.5-flash** | 30,000 | 10,000,000 |
| **qwen-flash** | 30,000 | 10,000,000 |
| **qwen-turbo** | 1,200 | 5,000,000 |
| **qwen-long** | 1,200 | 3,000,000 |
| **qwq-plus** | 600 | 1,000,000 |
| **qwen3-coder-plus** | 5,000 | 5,000,000 |
| **qwen3-coder-flash** | 5,000 | 5,000,000 |
| **qwen3-vl-plus** | 3,000 | 5,000,000 |
| **qwen3-vl-flash** | 3,000 | 5,000,000 |
| **qwen-vl-max** | 1,200 | 1,000,000 |
| **qwen-vl-plus** | 1,200 | 1,000,000 |
| **qwen-vl-ocr** | 600 | 6,000,000 |
| **qwen3.5-omni-plus** | 60 | 100,000 |

### 快照版本限流更严格

| 模型 | RPM | TPM |
|------|-----|-----|
| qwen3-max-2026-01-23 | 600 | 1,000,000 |
| qwen3.6-plus-2026-04-02 | 600 | 1,000,000 |
| qwen3.5-plus-2026-02-15 | 600 | 1,000,000 |
| qwen-plus-2025-07-14 | 100,000 | 1,000,000 |
| qwen-plus-2025-04-28 | 1,000,000 | — |

**建议：使用稳定版或最新版（带 `-latest` 后缀），限流更宽松。**

---

## 如何避免限流

### 1. 选用高限流模型
优先使用 `qwen-plus`、`qwen3.5-plus`、`qwen3.6-plus` 等限流宽松的模型。

### 2. 稳定版比快照版限流更宽松
- `qwen-plus`：30,000 RPM
- `qwen-plus-2025-04-28`：1,000,000 RPM
- `qwen-plus-2025-07-14`：100,000 RPM

### 3. 平滑请求速率
收到 `Request rate increased too quickly` 时，采用匀速调度、指数退避策略，避免瞬时高峰。

### 4. 添加备选模型

```python
import asyncio
from openai import AsyncOpenAI, APIStatusError

client = AsyncOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

MODEL = "qwen-plus-2025-07-28"
BACKUP_MODEL = "qwen-plus-2025-07-14"

async def send_request(model):
    try:
        await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "你是谁？"}]
        )
        return True
    except APIStatusError as e:
        if e.status_code == 429:
            print(f"[限流触发] 模型 {model}")
            return False
        raise

async def task(i):
    if await send_request(MODEL):
        return True
    return await send_request(BACKUP_MODEL)

async def main():
    results = await asyncio.gather(*(task(i) for i in range(10)))
    print(f"成功: {sum(results)}, 失败: {len(results) - sum(results)}")

asyncio.run(main())
```

### 5. 使用 Batch API
批量推理（Batch API）不受实时限流约束。

### 6. 任务拆分
大批量任务拆分为小批次，在不同时间段提交。

---

## 查看模型调用量

模型调用完一小时后，在**模型监控**页面（[北京](https://bailian.console.aliyun.com/?tab=model#/model-telemetry) 或 [新加坡](https://modelstudio.console.aliyun.com/?tab=model#/model-telemetry)）查看调用统计。

---

## 恢复时间

通常在一分钟内恢复。
