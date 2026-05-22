# 阿里云百炼（DashScope）多 Provider 配置指南

> **更新时间**：2026-05-22  
> **适用范围**：OpenClaw / Hermes / Claude Code / OpenHuman 等 AI Agent 平台  
> **数据来源**：[百炼模型大全](https://help.aliyun.com/zh/model-studio/text-generation-model/) · [百炼定价](https://help.aliyun.com/zh/model-studio/model-pricing)

---

## 1. Provider 架构

百炼提供三种独立 Provider，**每种需要不同的 API Key**，不可混用。

| Provider | Base URL | 计费方式 | 专属模型 |
|----------|----------|----------|----------|
| **bailian** | `dashscope.aliyuncs.com/compatible-mode/v1` | API Key 按量计费 | qwen3.7-max、qwen3.5-omni-plus 等旗舰模型 |
| **bailian-coding-plan** | `coding.dashscope.aliyuncs.com/v1` | Coding Plan 订阅制 | qwen3-coder-plus/next、MiniMax-M2.5 |
| **bailian-token-plan** | `dashscope.aliyuncs.com/compatible-mode/v1` | Token Plan 预付费额度 | MiniMax/MiniMax-M2.7、mimo-v2.5-pro |

> ⚠️ **注意**：Token Plan 和 bailian API 虽然 Base URL 相同，但 Key 不同、计费逻辑不同。

---

## 2. Key 配置机制

### 2.1 OpenClaw Key 配置

OpenClaw 采用两层 Key 管理：

**第一层：`openclaw.json` 声明 auth profile**
```json
{
  "auth": {
    "profiles": {
      "bailian:default": { "provider": "bailian", "mode": "api_key" },
      "bailian-coding-plan:default": { "provider": "bailian-coding-plan", "mode": "api_key" },
      "bailian-token-plan:default": { "provider": "bailian-token-plan", "mode": "api_key" }
    }
  }
}
```

**第二层：每个 Agent 的 `auth-profiles.json` 存储实际 Key**

路径：`~/.openclaw/agents/{agent-id}/agent/auth-profiles.json`

```json
{
  "version": 1,
  "profiles": {
    "bailian:default": {
      "type": "api_key",
      "provider": "bailian",
      "key": "sk-***（bailian 专属 Key）"
    },
    "bailian-coding-plan:default": {
      "type": "api_key",
      "provider": "bailian-coding-plan",
      "key": "sk-sp-***（Coding Plan 专属 Key）"
    },
    "bailian-token-plan:default": {
      "type": "api_key",
      "provider": "bailian-token-plan",
      "key": "sk-tp-***（Token Plan 专属 Key）"
    }
  },
  "lastGood": {
    "bailian": "bailian:default",
    "bailian-coding-plan": "bailian-coding-plan:default",
    "bailian-token-plan": "bailian-token-plan:default"
  }
}
```

**Key 获取方式**：
| Provider | 获取途径 | Key 前缀 |
|----------|----------|----------|
| bailian | [百炼控制台 → API Key](https://bailian.console.aliyun.com/#/api-key) | `sk-` |
| bailian-coding-plan | [百炼控制台 → Coding Plan](https://bailian.console.aliyun.com/#/coding-plan) | `sk-sp-` |
| bailian-token-plan | [百炼控制台 → Token Plan](https://bailian.console.aliyun.com/#/token-plan) | Token Plan 专属 Key |

**CLI 快速配置**：
```bash
# 交互式添加
openclaw models auth add --provider bailian-token-plan

# 或直接粘贴 Key
openclaw models auth paste-token --provider bailian-token-plan --profile-id bailian-token-plan:default
```

### 2.2 Hermes / Claude Code Key 配置

Hermes 和 Claude Code 通过环境变量配置：

```bash
# bailian provider
export DASHSCOPE_API_KEY="sk-***"

# bailian-coding-plan
export DASHSCOPE_CODING_PLAN_API_KEY="sk-sp-***"

# bailian-token-plan
export DASHSCOPE_TOKEN_PLAN_API_KEY="sk-tp-***"
```

在配置文件中指定 base URL：
```yaml
# hermes.yaml / claude-code-config.yaml
providers:
  bailian:
    base_url: https://dashscope.aliyuncs.com/compatible-mode/v1
    api_key: ${DASHSCOPE_API_KEY}
  bailian-coding-plan:
    base_url: https://coding.dashscope.aliyuncs.com/v1
    api_key: ${DASHSCOPE_CODING_PLAN_API_KEY}
  bailian-token-plan:
    base_url: https://dashscope.aliyuncs.com/compatible-mode/v1
    api_key: ${DASHSCOPE_TOKEN_PLAN_API_KEY}
```

### 2.3 OpenHuman Key 配置

OpenHuman 通过 Web UI 或配置文件管理多 Provider Key：

```json
{
  "providers": {
    "bailian": {
      "type": "openai-compatible",
      "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
      "apiKey": "***"
    },
    "bailian-coding-plan": {
      "type": "openai-compatible",
      "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
      "apiKey": "***"
    },
    "bailian-token-plan": {
      "type": "openai-compatible",
      "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
      "apiKey": "***"
    }
  }
}
```

---

## 3. 模型 × Provider 完整矩阵

### 3.1 思考模式支持（2026-05-22 更新）

| 模型 | 思考模式 | 默认状态 | bailian | coding-plan | token-plan |
|------|----------|----------|---------|-------------|------------|
| **qwen3.7-max** | 混合 | ✅ 默认开 | ✅ | ❌ | ❌ |
| **qwen3.6-max-preview** | 混合 | ✅ 默认开 | ✅ | ❌ | ❌ |
| **qwen3.6-plus** | 混合 | ✅ 默认开 | ✅ | ✅ | ✅ |
| **qwen3.6-flash** | 混合 | ✅ 默认开 | ✅ | ✅ | ✅ |
| **qwen3.5-plus** | 混合 | ✅ 默认开 | ✅ | ✅ | ✅ |
| **qwen3.5-flash** | 混合 | ✅ 默认开 | ✅ | ❌ | ✅ |
| **qwen3.5-omni-plus** | 混合 | ✅ 默认开 | ✅ | ❌ | ❌ |
| **qwen3-coder-plus** | 混合 | ✅ 默认开 | ✅ | ✅ | ❌ |
| **qwen3-coder-next** | 混合 | ✅ 默认开 | ❌ | ✅ | ❌ |
| **deepseek-v4-pro** | 混合 | ✅ 默认开 | ✅ | ❌ | ✅ |
| **deepseek-v4-flash** | 混合 | ✅ 默认开 | ✅ | ❌ | ✅ |
| **glm-5.1** | 混合 | ✅ 默认开 | ✅ | ✅ | ✅ |
| **glm-5** | 混合 | ✅ 默认开 | ❌ | ✅ | ❌ |
| **glm-4.7** | 混合 | ✅ 默认开 | ❌ | ✅ | ❌ |
| **kimi-k2.6** | 混合 | ⚠️ 默认关 | ✅ | ✅ | ❌ |
| **kimi-k2.5** | 混合 | ⚠️ 默认关 | ❌ | ✅ | ❌ |
| **MiniMax-M2.5** | 仅思考 | ✅ 始终开 | ❌ | ✅ | ❌ |
| **MiniMax/MiniMax-M2.7** | 混合 | ✅ 默认开 | ❌ | ❌ | ✅ |
| **mimo-v2.5-pro** | 混合 | ✅ 默认开 | ✅ | ❌ | ✅ |
| **qwen-turbo**（主线） | 混合 | ⚠️ 默认关 | ✅ | ❌ | ❌ |
| **qwq-plus** | 仅思考 | ✅ 始终开 | ✅ | ❌ | ❌ |
| **deepseek-r1** | 仅思考 | ✅ 始终开 | ✅ | ❌ | ❌ |

### 3.2 价格速查（元/百万Token）

| 模型 | 输入 | 输出 | 上下文 |
|------|------|------|--------|
| qwen3.7-max | ¥12 | ¥36 | 1M |
| qwen3.6-plus | ¥2 | ¥12 | 1M |
| qwen3.6-flash | ¥1.2 | ¥7.2 | 1M |
| qwen3.5-plus | ¥0.8 | ¥4.8 | 1M |
| qwen3.5-flash | ¥0.2 | ¥2 | 1M |
| deepseek-v4-pro | ¥2 | ¥8 | 1M |
| deepseek-v4-flash | ¥0.5 | ¥2.5 | 1M |
| glm-5.1 | ¥4 | ¥18 | 198K |
| kimi-k2.6 | ¥4 | ¥21 | 256K |
| MiniMax-M2.7 | ¥2.1 | ¥8.4 | 192K |
| mimo-v2.5-pro | ¥3 | ¥12 | 1M |

---

## 4. Agent 配置参考

### 4.1 openclaw.json 完整 Provider 配置

```json
{
  "models": {
    "providers": {
      "bailian": {
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api": "openai-completions",
        "models": [
          {"id": "qwen3.7-max", "reasoning": true, "contextWindow": 1000000, "maxTokens": 65536, "input": ["text","image"], "cost": {"input":12,"output":36}},
          {"id": "qwen3.6-plus", "reasoning": true, "contextWindow": 1000000, "maxTokens": 65536, "input": ["text","image"], "cost": {"input":2,"output":12}},
          {"id": "qwen3.6-flash", "reasoning": true, "contextWindow": 1000000, "maxTokens": 65536, "input": ["text","image"], "cost": {"input":1.2,"output":7.2}},
          {"id": "qwen3.5-plus", "reasoning": true, "contextWindow": 1000000, "maxTokens": 65536, "input": ["text","image"], "cost": {"input":0.8,"output":4.8}},
          {"id": "qwen3.5-flash", "reasoning": true, "contextWindow": 1000000, "maxTokens": 65536, "input": ["text"], "cost": {"input":0.2,"output":2}},
          {"id": "qwen3.5-omni-plus", "reasoning": true, "contextWindow": 262144, "maxTokens": 65536, "input": ["text","image","video","audio"], "cost": {"input":7,"output":40}},
          {"id": "deepseek-v4-pro", "reasoning": true, "contextWindow": 1000000, "maxTokens": 65536, "input": ["text"], "cost": {"input":2,"output":8}},
          {"id": "deepseek-v4-flash", "reasoning": true, "contextWindow": 1000000, "maxTokens": 65536, "input": ["text"], "cost": {"input":0.5,"output":2.5}},
          {"id": "glm-5.1", "reasoning": true, "contextWindow": 202752, "maxTokens": 131072, "input": ["text"], "cost": {"input":4,"output":18}},
          {"id": "kimi-k2.6", "reasoning": true, "contextWindow": 262144, "maxTokens": 98304, "input": ["text","image"], "cost": {"input":4,"output":21}},
          {"id": "MiniMax-M2.7", "reasoning": true, "contextWindow": 200000, "maxTokens": 32768, "input": ["text"], "cost": {"input":2.1,"output":8.4}},
          {"id": "mimo-v2.5-pro", "reasoning": true, "contextWindow": 1000000, "maxTokens": 131072, "input": ["text"], "cost": {"input":3,"output":12}}
        ]
      },
      "bailian-coding-plan": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "api": "openai-completions",
        "models": [
          {"id": "qwen3.6-plus", "reasoning": true, "contextWindow": 1000000, "maxTokens": 65536, "input": ["text","image"]},
          {"id": "qwen3.5-plus", "reasoning": true, "contextWindow": 1000000, "maxTokens": 65536, "input": ["text","image"]},
          {"id": "qwen3-coder-plus", "reasoning": true, "contextWindow": 1000000, "maxTokens": 65536, "input": ["text"]},
          {"id": "qwen3-coder-next", "reasoning": true, "contextWindow": 262144, "maxTokens": 65536, "input": ["text"]},
          {"id": "kimi-k2.5", "reasoning": true, "contextWindow": 262144, "maxTokens": 262144, "input": ["text","image"]},
          {"id": "MiniMax-M2.5", "reasoning": true, "contextWindow": 196608, "maxTokens": 32768, "input": ["text"]},
          {"id": "glm-5", "reasoning": true, "contextWindow": 202752, "maxTokens": 16384, "input": ["text"]},
          {"id": "glm-4.7", "reasoning": true, "contextWindow": 169984, "maxTokens": 16384, "input": ["text"]}
        ]
      },
      "bailian-token-plan": {
        "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api": "openai-completions",
        "models": [
          {"id": "qwen3.6-plus", "reasoning": true, "contextWindow": 1000000, "maxTokens": 65536, "input": ["text","image"]},
          {"id": "qwen3.6-flash", "reasoning": true, "contextWindow": 1000000, "maxTokens": 65536, "input": ["text","image"]},
          {"id": "qwen3.5-plus", "reasoning": true, "contextWindow": 1000000, "maxTokens": 65536, "input": ["text","image"]},
          {"id": "qwen3.5-flash", "reasoning": true, "contextWindow": 1000000, "maxTokens": 65536, "input": ["text"]},
          {"id": "deepseek-v4-pro", "reasoning": true, "contextWindow": 1000000, "maxTokens": 65536, "input": ["text"]},
          {"id": "deepseek-v4-flash", "reasoning": true, "contextWindow": 1000000, "maxTokens": 65536, "input": ["text"]},
          {"id": "glm-5.1", "reasoning": true, "contextWindow": 202752, "maxTokens": 131072, "input": ["text"]},
          {"id": "MiniMax/MiniMax-M2.7", "reasoning": true, "contextWindow": 200000, "maxTokens": 32768, "input": ["text"]},
          {"id": "mimo-v2.5-pro", "reasoning": true, "contextWindow": 1000000, "maxTokens": 131072, "input": ["text"]}
        ]
      }
    }
  }
}
```

### 4.2 Agent 推荐模型选择

| 场景 | 推荐模型 | Provider | 理由 |
|------|----------|----------|------|
| **最强推理** | qwen3.7-max | bailian | 最新旗舰，256K 思考预算 |
| **日常均衡** | qwen3.6-plus | coding-plan | 性价比高，支持 Token Plan |
| **代码专用** | qwen3-coder-plus | coding-plan | 代码优化，1M 上下文 |
| **极速低成本** | qwen3.6-flash | bailian/token-plan | ¥1.2/¥7.2 |
| **长文档审查** | kimi-k2.5/k2.6 | coding-plan/bailian | 256K 上下文 |
| **第三方推理** | deepseek-v4-pro | token-plan | 1M 上下文，强推理 |
| **多模态** | qwen3.5-omni-plus | bailian | 全模态支持 |
| **智能体优化** | glm-5.1 | token-plan | 上下文缓存，Agent 友好 |

### 4.3 thinkingDefault 配置

所有 Agent 建议统一设置：
```json
{
  "thinkingDefault": "high"
}
```

支持思考的模型会自动启用深度推理；不支持的模型（如 qwen-turbo）会忽略此设置。

---

## 5. 定期更新机制

### 5.1 自动同步 Cron

OpenClaw cron job `bailian-model-sync-weekly` 每周五 10:00 自动执行：
- 爬取百炼官网模型列表和定价
- 对比上次同步记录
- 更新 SKILL.md 和配置参考文档
- 有变更时通知 Discord

### 5.2 手动更新检查清单

```
□ 1. 爬取模型大全：https://help.aliyun.com/zh/model-studio/text-generation-model/
□ 2. 爬取定价页：https://help.aliyun.com/zh/model-studio/model-pricing
□ 3. 检查新增模型 → 更新 Provider models 配置
□ 4. 检查价格变更 → 更新 cost 字段
□ 5. 检查思考模式变化 → 更新 reasoning 字段
□ 6. 检查 Token Plan / Coding Plan 覆盖 → 更新可用模型列表
□ 7. 更新 SKILL.md 的更新时间戳
□ 8. 推送到 GitHub: brantzh6/AI-skills
```

### 5.3 变更历史

| 日期 | 变更 |
|------|------|
| 2026-05-22 | 新增 qwen3.7-max；新增 bailian-token-plan provider；新增 MiniMax-M2.7、mimo-v2.5-pro；确认思考模式矩阵 |

---

## 6. 常见问题

**Q: 为什么 bailian 和 bailian-token-plan 的 Base URL 相同但 Key 不同？**  
A: bailian 是按量计费 Key，token-plan 是预付费额度 Key。百炼后台根据 Key 类型决定计费逻辑。

**Q: 同一个模型在多个 Provider 下有什么区别？**  
A: 模型本身相同，区别在于计费方式。例如 qwen3.6-plus 在 bailian 按量计费，在 coding-plan 走订阅额度，在 token-plan 扣预付费额度。

**Q: 如何选择用哪个 Provider？**  
A:
- **高频使用** → coding-plan（订阅制，成本可控）
- **低频偶尔调用** → bailian（按量，不用不花钱）
- **需要特定模型（如 MiniMax-M2.7）** → token-plan

**Q: Agent 怎么指定 Provider？**  
A: 模型 ID 格式为 `{provider}/{model}`，例如 `bailian/qwen3.7-max`、`bailian-coding-plan/qwen3.6-plus`。
