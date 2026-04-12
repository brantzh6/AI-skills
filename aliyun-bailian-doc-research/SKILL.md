---
name: aliyun-bailian-doc-research
description: 阿里云百炼文档研究与更新方法，包括文档抓取、URL 变更应对、知识提取、输出文档生成。
homepage: https://help.aliyun.com/zh/model-studio
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires": { "tools": ["web_fetch"] },
        "install": [],
      },
  }
---

# 阿里云百炼文档研究 — 抓取与更新指南

**版本**: v3.0
**更新时间**: 2026-04-12
**适用场景**: 抓取阿里云百炼平台最新文档，生成结构化的本地 SKILL.md 文档

---

## 🎯 目标

从官方文档抓取最新信息，生成 `output/{类别}/SKILL.md` 文件。

---

## 🔗 根目录与备用发现机制

> **核心原则：404 是常态。官方文档 URL 经常变化，但根目录永远不会变。**

### 根目录（不变）

| 根目录 | 说明 |
|--------|------|
| `https://help.aliyun.com/` | 阿里云帮助中心根目录 |
| `https://www.aliyun.com/` | 阿里云官网首页 |
| `https://help.aliyun.com/zh/model-studio/` | 百炼文档首页 |

### URL 变更应对策略

当已知文档 URL 返回 404 时，**按以下顺序尝试**：

#### 策略 1：访问上级目录

```
已知 URL: https://help.aliyun.com/zh/model-studio/qwen-tts
→ 404 时访问: https://help.aliyun.com/zh/model-studio/
→ 在页面中搜索新链接
```

#### 策略 2：访问文档首页

```
访问: https://help.aliyun.com/zh/model-studio/
→ 这是百炼文档的入口页面，包含所有子文档的导航链接
→ 从中提取最新的各能力文档 URL
```

#### 策略 3：搜索阿里云官网

```
访问: https://www.aliyun.com/
→ 使用站内搜索："百炼" 或 "model-studio" 或具体功能名称
→ 或直接访问: https://www.aliyun.com/search?keywords=百炼+语音合成
```

#### 策略 4：搜索帮助中心

```
访问: https://help.aliyun.com/
→ 使用帮助中心搜索功能
→ 或在浏览器中使用: site:help.aliyun.com {关键词}
```

### 已知有效入口页面

| 页面 | URL | 说明 |
|------|-----|------|
| 百炼文档首页 | `https://help.aliyun.com/zh/model-studio/` | ⭐ 最重要入口 |
| 模型列表 | `https://help.aliyun.com/zh/model-studio/models` | 所有模型规格 |
| 快速入门 | `https://help.aliyun.com/zh/model-studio/quick-start/` | 入门指南 |
| API Key | `https://help.aliyun.com/zh/model-studio/get-api-key/` | 获取密钥 |
| 安装 SDK | `https://help.aliyun.com/zh/model-studio/install-sdk/` | SDK 安装 |
| 计费说明 | `https://help.aliyun.com/zh/model-studio/billing-for-model-studio/` | 价格 |

**这些入口页面几乎不会变化**，即使子文档 URL 变了，从入口页面总能找到新链接。

---

## 📁 输出目录结构

```
output/
├── INDEX.md                              ← 总索引
├── language-models/                      ← 语言模型
├── video-generation/                     ← 视频生成
├── image-generation/                     ← 图像生成
├── tts/                                  ← 语音合成
├── asr/                                  ← 语音识别
├── embedding/                            ← 向量模型
├── vision/                               ← 视觉理解
├── tool-calls/                           ← 工具调用
├── batch/                                ← Batch 批量
├── rate-limit/                           ← 限流
└── error-codes/                          ← 错误码
```

---

## 📋 抓取流程

### 第 0 步：确认入口（每次必做）

```python
# 先访问百炼文档首页，确认导航结构未变
web_fetch(url="https://help.aliyun.com/zh/model-studio/", maxChars=20000)
```

从首页提取当前各能力文档的最新 URL。

### 第 1 步：批量抓取官方文档

使用 `web_fetch` 抓取所有核心文档。如果某个 URL 返回 404，**不要跳过**，执行第 0 步从入口页面找到新 URL。

```python
# 核心文档（高优先级）
web_fetch(url="https://help.aliyun.com/zh/model-studio/text-generation", maxChars=20000)
web_fetch(url="https://help.aliyun.com/zh/model-studio/vision", maxChars=15000)
web_fetch(url="https://help.aliyun.com/zh/model-studio/embedding", maxChars=15000)
web_fetch(url="https://help.aliyun.com/zh/model-studio/rate-limit", maxChars=15000)
web_fetch(url="https://help.aliyun.com/zh/model-studio/error-code", maxChars=15000)

# 其他文档（中优先级）
web_fetch(url="https://help.aliyun.com/zh/model-studio/deep-thinking", maxChars=15000)
web_fetch(url="https://help.aliyun.com/zh/model-studio/context-cache", maxChars=15000)
web_fetch(url="https://help.aliyun.com/zh/model-studio/web-search", maxChars=15000)
web_fetch(url="https://help.aliyun.com/zh/model-studio/qwen-tts", maxChars=15000)
web_fetch(url="https://help.aliyun.com/zh/model-studio/text-to-image", maxChars=15000)
web_fetch(url="https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/", maxChars=15000)
web_fetch(url="https://help.aliyun.com/zh/model-studio/tool-calls", maxChars=15000)
```

### 第 2 步：提取关键信息

从每个页面提取：
1. **模型列表** — 模型名称、特点、支持的功能
2. **快速开始代码** — Python/curl 示例
3. **参数表格** — 关键参数、取值范围、说明
4. **注意事项** — 有效期、SDK版本要求、地域差异
5. **支持的地域** — 北京/新加坡/全球

### 第 3 步：生成 SKILL.md

每个类别的 SKILL.md 标准结构：

```markdown
# {类别名称}

> 更新时间：{日期}
> 来源：{官方URL}

---

## 概述

**Base URL：**
- 北京：`...`
- 新加坡：`...`

---

## 模型矩阵

| 模型 | 特点 | 适用场景 |

---

## 快速开始

### Python
### curl

---

## 关键参数

| 参数 | 说明 | 取值 |

---

## 支持的模型

### 北京地域 / 新加坡地域

---

## 注意事项
```

### 第 4 步：生成 _meta.json

```json
{
  "name": "{类别名}",
  "version": "{日期}",
  "description": "{描述}",
  "last_updated": "{日期}",
  "sources": ["{官方URL}"],
  "files": ["SKILL.md"]
}
```

### 第 5 步：更新 INDEX.md

更新总索引，标注所有来源 URL 和状态。

---

## ⚠️ 注意事项

### 信息真实性

- **只写官方文档中明确提到的内容**
- **不要基于已有知识推测**
- 如果官方文档没有提到某个模型或功能，不要写入

### 404 处理

1. 已知 URL 返回 404 → 访问 `https://help.aliyun.com/zh/model-studio/` 找到新 URL
2. 如果入口页面也变了 → 访问 `https://help.aliyun.com/` 搜索"百炼"
3. 如果搜索也失败 → 访问 `https://www.aliyun.com/` 搜索
4. **根目录 https://help.aliyun.com/ 和 https://www.aliyun.com/ 永远不会变**

### 时效性

- 每个文档标注更新日期和来源 URL
- 模型列表、限流条件等数据经常变化，以官方最新为准

---

## 📊 当前文档状态（2026-04-12）

| 类别 | 文件数 | 状态 | 来源 |
|------|--------|------|------|
| language-models | 6 | ✅ | text-generation, deep-thinking, context-cache, web-search |
| video-generation | 18 | ✅ | video-generation, Wan 2.7 API |
| image-generation | 2 | ✅ | text-to-image |
| tts | 2 | ✅ | qwen-tts |
| asr | 2 | ✅ | speech-recognition |
| embedding | 2 | ✅ | embedding |
| vision | 2 | ✅ | vision |
| tool-calls | 2 | ✅ | tool-calls, function-calling |
| batch | 2 | ✅ | batch-interfaces |
| rate-limit | 2 | ✅ | rate-limit |
| error-codes | 2 | ✅ | error-code |
| finetuning | 0 | ⚠️ 待补充 | finetuning |

**总计：43 个文件，约 296KB**
