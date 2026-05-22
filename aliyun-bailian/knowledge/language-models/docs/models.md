# 模型选型指南

> 来源：https://help.aliyun.com/zh/model-studio/text-generation

---

## 服务地域

阿里云百炼提供**北京**（中国内地）、**新加坡**（国际）、**弗吉尼亚**（全球）三个地域的模型服务。各地域的 API Key 不同，选择邻近地域调用可降低网络延迟。

| 地域 | Base URL | 特点 |
|------|----------|------|
| 北京 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | 中国内地，最全模型 |
| 新加坡 | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` | 国际，支持主要模型 |
| 弗吉尼亚 | `https://dashscope.aliyuncs.com/compatible-mode/v1`（美国） | 全球，支持主要模型 |

---

## 千问模型矩阵

### 千问旗舰系列

| 模型 | 版本标识 | 思考模式 | 搜索 | 缓存 | 推荐场景 |
|------|----------|----------|------|------|----------|
| **Qwen3.6-Plus** | `qwen3.6-plus` | 混合思考（默认开） | 仅 Responses API | ✅ | 最新旗舰，多模态 |
| **Qwen3.5-Plus** | `qwen3.5-plus` | 混合思考（默认开） | ✅ | ✅ | 效果/速度/成本均衡 |
| **Qwen3-Max** | `qwen3-max` | 混合思考（默认关） | ✅ agent/agent_max | ✅ | 最复杂任务 |
| **Qwen-Plus** | `qwen-plus` | 混合思考（默认关） | ✅ | ✅ | 通用首选 |
| **Qwen3.5-Flash** | `qwen3.5-flash` | 混合思考（默认开） | ✅ | ✅ | 快速响应 |
| **Qwen-Flash** | `qwen-flash` | 混合思考（默认关） | ✅ | ✅ | 最低成本 |
| **Qwen-Turbo** | `qwen-turbo` | 混合思考（默认关） | ✅ | — | 高速简单任务 |

### 开源版千问

| 模型 | 思考模式 | 说明 |
|------|----------|------|
| `qwen3.5-397b-a17b` | 混合思考（默认开） | 最大开源版 |
| `qwen3.5-122b-a10b` | 混合思考（默认开） | 中等规模 |
| `qwen3.5-27b` | 混合思考（默认开） | 轻量级 |
| `qwen3.5-35b-a3b` | 混合思考（默认开） | 混合专家 |

### 千问 Coder（代码专用）

| 模型 | 特点 |
|------|------|
| `qwen3-coder-plus` | 代码生成/调试/解释，支持显式缓存 |
| `qwen3-coder-flash` | 轻量级代码模型 |

### 千问 VL（视觉语言）

| 模型 | 特点 |
|------|------|
| `qwen3-vl-plus` | 视觉+文本理解，支持显式缓存 |
| `qwen3-vl-flash` | 轻量视觉模型 |
| `qwen-vl-max` | 上一代旗舰视觉模型 |
| `qwen-vl-plus` | 上一代通用视觉模型 |

### 千问 Omni（全模态）

| 模型 | 输入 | 输出 |
|------|------|------|
| `qwen3.5-omni-plus` | 视频+音频+图片+文本 | 文本+语音 |
| `qwen3.5-omni-flash` | 视频+音频+图片+文本 | 文本+语音 |
| `qwen3.5-omni-plus-realtime` | 同上，实时模式 | 同上 |

### 行业专用模型

| 模型 | 用途 |
|------|------|
| `qwen-plus-character` | 角色扮演 |
| `qwen-doc-turbo` | 数据挖掘 |
| `qwen3-max`（法律版） | 法律文档 |

---

## 第三方旗舰模型

### DeepSeek

| 模型 | 思考模式 | 特点 |
|------|----------|------|
| `deepseek-v3.2` | 混合思考（默认关） | 最新版，高性能 |
| `deepseek-v3.2-exp` | 混合思考 | 实验版 |
| `deepseek-v3.1` | 混合思考（默认关） | 稳定版 |
| `deepseek-r1` | 仅思考模式 | 深度推理专用 |
| `deepseek-r1-0528` | 仅思考模式 | 深度推理快照 |
| `deepseek-v3` | 混合思考 | 老版 |

### Kimi（月之暗面）

| 模型 | 思考模式 | 特点 |
|------|----------|------|
| `kimi-k2.5` | 混合思考（默认关） | 最新版，长上下文 |
| `kimi-k2-thinking` | 仅思考模式 | 深度推理 |
| `Moonshot-Kimi-K2-Instruct` | 混合思考 | 指令版 |

### GLM（智谱）

| 模型 | 思考模式 | 特点 |
|------|----------|------|
| `glm-5` | 混合思考（默认开） | 最新版 |
| `glm-4.7` | 混合思考（默认开） | 稳定版 |
| `glm-4.6` | 混合思考（默认开） | 旧版 |
| `glm-4.5` | 混合思考（默认开） | — |
| `glm-4.5-air` | 混合思考（默认开） | 轻量版 |

### MiniMax

| 模型 | 特点 |
|------|------|
| `MiniMax-M2.5` | 最新版 |
| `MiniMax-M2.1` | 稳定版 |

---

## 模型选型决策树

```
需要什么？
├── 最强效果/复杂推理 → Qwen3-Max 或 GLM-5
├── 均衡选择（推荐） → Qwen3.6-Plus 或 Qwen3.5-Plus
├── 最快响应/最低成本 → Qwen3.5-Flash 或 Qwen-Flash
├── 代码任务 → Qwen3-Coder-Plus
├── 视觉理解 → Qwen3-VL-Plus 或 Qwen3.6-Plus
├── 全模态（含语音） → Qwen3.5-Omni-Plus
├── 深度推理 → DeepSeek-R1 或 QwQ
├── 第三方最佳 → GLM-5 或 Kimi K2.5
└── 角色扮演 → Qwen-Plus-Character
```

---

## 快照版本说明

每个模型有多个快照版本，格式为 `模型名-日期`，例如：
- `qwen3.6-plus-2026-04-02`
- `qwen3.5-plus-2026-02-15`
- `qwen3-max-2026-01-23`

快照版本保证接口稳定性，`latest` 后缀会自动更新到最新快照。生产环境建议使用具体日期版本。

---

## 调用方式

所有模型均兼容 OpenAI 接口：

### Chat Completions API
```
POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions
```

### Responses API
```
POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses
```

### DashScope 原生接口
```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
```
