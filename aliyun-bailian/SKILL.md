---
name: aliyun-bailian
description: 阿里云百炼平台完整知识库与配置管理。包含模型能力矩阵、多Provider配置指南、API参考、定期同步机制。支持 OpenClaw/Hermes/OpenHuman 等多智能体平台。
homepage: https://help.aliyun.com/zh/model-studio
metadata:
  {
    "openclaw":
      {
        "emoji": "🔮",
        "requires": { "env": ["DASHSCOPE_API_KEY"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "packages": ["requests", "notion-client"],
              "label": "Install sync dependencies",
            },
          ],
        "cron":
          {
            "name": "aliyun-bailian-weekly-sync",
            "schedule": "0 0 * * 1",
            "enabled": true,
            "description": "每周一同步阿里云百炼模型信息",
          },
      },
  }
---

# 阿里云百炼 — 知识库与配置管理

> **版本**: v2.0（合并自 aliyun-bailian-doc-research + aliyun-bailian-sync）
> **更新时间**: 2026-05-22
> **数据来源**: [百炼模型大全](https://help.aliyun.com/zh/model-studio/text-generation-model/) · [模型定价](https://help.aliyun.com/zh/model-studio/model-pricing)

---

## 目录结构

```
aliyun-bailian/
├── SKILL.md                      # 本文件（总入口）
├── knowledge/                    # 知识库（官网文档整理）
│   ├── INDEX.md                  # 知识库索引
│   ├── language-models/          # 语言模型（千问/第三方）
│   ├── image-generation/         # 图像生成（Wan 2.7 等）
│   ├── video-generation/         # 视频生成
│   ├── tts/                      # 语音合成（CosyVoice）
│   ├── asr/                      # 语音识别
│   ├── vision/                   # 视觉理解
│   ├── tool-calls/               # Function Calling
│   ├── embedding/                # 向量与重排序
│   ├── batch/                    # 批量推理
│   ├── rate-limit/               # 限流与配额
│   └── error-codes/              # 错误码
├── config/                       # 配置参考
│   └── config-guide.md           # 多Provider配置指南（Key机制）
├── scripts/                      # 自动化脚本
│   └── sync.py                   # Notion 同步脚本
├── templates/                    # 模板
│   └── research-template.md
└── docs/                         # 辅助文档
    ├── notion-setup.md           # Notion 集成配置
    └── usage-examples.md         # API 使用示例
```

---

## 快速查阅

### 🔥 模型选型

→ 看 [`knowledge/language-models/SKILL.md`](knowledge/language-models/SKILL.md)

| 需求 | 推荐模型 | Provider |
|------|----------|----------|
| 最强推理 | qwen3.7-max | bailian |
| 日常均衡 | qwen3.6-plus | coding-plan / token-plan |
| 代码专用 | qwen3-coder-plus | coding-plan |
| 极速低价 | qwen3.6-flash | bailian / token-plan |
| 多模态 | qwen3.5-omni-plus | bailian |
| 第三方推理 | deepseek-v4-pro | bailian / token-plan |

### 🔑 Key 配置

→ 看 [`config/config-guide.md`](config/config-guide.md)

| Provider | Key 前缀 | 获取途径 |
|----------|----------|----------|
| bailian | `sk-` | 百炼控制台 → API Key |
| bailian-coding-plan | `sk-sp-` | 百炼控制台 → Coding Plan |
| bailian-token-plan | Token Plan Key | 百炼控制台 → Token Plan |

### 🖼️ 图像/视频生成

→ 看 [`knowledge/image-generation/`](knowledge/image-generation/SKILL.md) · [`knowledge/video-generation/`](knowledge/video-generation/SKILL.md)

### 🔧 API 特性

| 特性 | 文档 |
|------|------|
| 深度思考 | [`knowledge/language-models/docs/deep-thinking.md`](knowledge/language-models/docs/deep-thinking.md) |
| Function Calling | [`knowledge/tool-calls/SKILL.md`](knowledge/tool-calls/SKILL.md) |
| 上下文缓存 | [`knowledge/language-models/docs/context-cache.md`](knowledge/language-models/docs/context-cache.md) |
| 联网搜索 | [`knowledge/language-models/docs/aliyun-web-search.md`](knowledge/language-models/docs/aliyun-web-search.md) |

---

## 思考模式速查

### ✅ 混合思考（默认开启）
qwen3.7-max · qwen3.6-plus · qwen3.6-flash · qwen3.5-plus · qwen3.5-flash · qwen3-coder-plus · deepseek-v4-pro · deepseek-v4-flash · glm-5.1 · glm-5 · glm-4.7 · MiniMax/MiniMax-M2.7 · mimo-v2.5-pro

### ⚠️ 混合思考（默认关闭，需手动开启）
qwen-turbo · qwen-max · kimi-k2.6 · kimi-k2.5 · deepseek-v3.2

### 🔒 仅思考模式（无法关闭）
qwq-plus · deepseek-r1 · kimi-k2-thinking · qwen3-next-80b-a3b-thinking

---

## 定期同步机制

### 自动同步（Cron）

每周一 00:00 自动执行，检查以下内容：

| 检查项 | 频率 | 来源 |
|--------|------|------|
| 新增/下线模型 | 每周 | 模型大全页面 |
| 价格变更 | 每周 | 定价页面 |
| 思考/FC/工具支持变化 | 每周 | 各模型详情页 |
| Token Plan / Coding Plan 覆盖 | 每周 | Plan 页面 |
| API 文档变更 | 每月 | 开发文档 |

### 手动触发

```bash
# 完整同步
python scripts/sync.py --action sync

# 仅检查变更
python scripts/sync.py --action check
```

### 更新检查清单

- [ ] 爬取模型大全：`https://help.aliyun.com/zh/model-studio/text-generation-model/`
- [ ] 爬取定价页：`https://help.aliyun.com/zh/model-studio/model-pricing`
- [ ] 检查新增模型 → 更新 knowledge/ 和 config/
- [ ] 检查价格变更 → 更新 cost 字段
- [ ] 检查思考模式变化 → 更新 reasoning 字段
- [ ] 检查 Plan 覆盖变化 → 更新 Provider 模型列表
- [ ] 更新 SKILL.md 时间戳

---

## 变更历史

| 日期 | 变更 |
|------|------|
| 2026-05-22 | **v2.0** 合并 doc-research + sync 为统一 skill；新增 qwen3.7-max；新增 config-guide |
| 2026-04-27 | 新增 DeepSeek V4、GLM-5.1、Kimi K2.6、MiniMax M2.7、Qwen3-Coder |
| 2026-04-12 | Qwen3.6-Max-Preview、Qwen3.6-Plus/Flash 首次记录 |
| 2026-03-31 | 初始版本，百炼知识库建立 |

---

**维护者**: 胖福 (OpenClaw Agent) · **更新频率**: 每周自动 + 重大变更时手动更新
