# 阿里云百炼文档索引

> 最后更新：2026-04-12
> 文档来源：[阿里云百炼帮助中心](https://help.aliyun.com/zh/model-studio/)

---

## 文档总览

**总计：12 个类别，44 个文件**

| 类别 | 文件数 | 状态 | 来源 |
|------|--------|------|------|
| [语言模型](#language-models) | 7 | ✅ | text-generation, deep-thinking, context-cache, web-search |
| [视频生成](#video-generation) | 18 | ✅ | video-generation, Wan 2.7 API |
| [图像生成](#image-generation) | 2 | ✅ | text-to-image |
| [语音合成](#tts) | 2 | ✅ | qwen-tts |
| [语音识别](#asr) | 2 | ✅ | speech-recognition |
| [向量模型](#embedding) | 2 | ✅ | embedding |
| [视觉理解](#vision) | 2 | ✅ | vision |
| [工具调用](#tool-calls) | 2 | ✅ | tool-calls, function-calling |
| [Batch 批量](#batch) | 2 | ✅ | batch-interfaces |
| [限流](#rate-limit) | 2 | ✅ | rate-limit |
| [错误码](#error-codes) | 2 | ✅ | error-code |
| [微调/训练](#finetuning) | 0 | ⚠️ 待补充 | finetuning |

---

## 语言模型 (language-models/)

| 文件 | 内容 |
|------|------|
| SKILL.md | 总览：模型矩阵、高级特性速查 |
| docs/models.md | 完整模型选型：千问旗舰+第三方旗舰+决策树 |
| docs/deep-thinking.md | 深度思考：混合/仅思考模式 |
| docs/context-cache.md | 上下文缓存：显式/隐式缓存、计费 |
| docs/web-search.md | 联网搜索：四种方式（内置搜索/Responses API/MCP/OpenSearch）、搜索策略 |
| docs/opensearch.md | OpenSearch：企业级搜索引擎、全链路搜索能力 |

## 视频生成 (video-generation/)

| 文件 | 内容 |
|------|------|
| SKILL.md | 总览：Wan 2.6/2.7 对比 |
| docs/WAN_2_7_REVIEW.md | Wan 2.7 评测 |
| docs/WAN_2_6_REVIEW.md | Wan 2.6 评测 |
| docs/MULTI_CHARACTER_GUIDE.md | 多角色指南 |
| docs/LONG_FORM_VIDEO_DESIGN.md | 长视频设计 |
| ... 其他 13 篇 | 研究、示例、挑战等 |

## 图像生成 (image-generation/)

| 文件 | 内容 |
|------|------|
| SKILL.md | 千问/万相模型对比、异步/同步调用、关键参数 |

## 语音合成 (tts/)

| 文件 | 内容 |
|------|------|
| SKILL.md | 千问 TTS 模型矩阵、流式/非流式、声音复刻/设计、指令控制 |

## 语音识别 (asr/)

| 文件 | 内容 |
|------|------|
| SKILL.md | Paraformer 语音识别、录音文件识别 |

## 向量模型 (embedding/)

| 文件 | 内容 |
|------|------|
| SKILL.md | 文本向量+多模态向量、融合/独立向量、选型建议 |

## 视觉理解 (vision/)

| 文件 | 内容 |
|------|------|
| SKILL.md | Qwen3.6/3.5 VL 模型、图像问答、OCR、物体定位(2D/3D)、文档解析、视频理解 |

## 工具调用 (tool-calls/)

| 文件 | 内容 |
|------|------|
| SKILL.md | Chat Completions 工具调用、Assistant API、联网搜索工具 |

## Batch 批量 (batch/)

| 文件 | 内容 |
|------|------|
| SKILL.md | Batch API、成本降低 50%、输入格式、支持模型清单 |

## 限流 (rate-limit/)

| 文件 | 内容 |
|------|------|
| SKILL.md | RPM/TPM 限制、各模型限流条件、避免限流策略 |

## 错误码 (error-codes/)

| 文件 | 内容 |
|------|------|
| SKILL.md | 400/401/403/429/500 错误码：参数错误、认证、限流、多模态、文件等 |

---

## 通用信息

### Base URL

| 地域 | OpenAI 兼容 | DashScope 原生 |
|------|-------------|----------------|
| 北京 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `https://dashscope.aliyuncs.com/api/v1` |
| 新加坡 | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` | `https://dashscope-intl.aliyuncs.com/api/v1` |

### 关键文档链接

- [获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)
- [配置环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)
- [安装 SDK](https://help.aliyun.com/zh/model-studio/install-sdk)
- [模型列表](https://help.aliyun.com/zh/model-studio/models)
- [联网搜索](https://help.aliyun.com/zh/model-studio/web-search)
- [MCP 接入](https://help.aliyun.com/zh/model-studio/mcp)
- [MCP 服务市场](https://help.aliyun.com/zh/model-studio/official-and-third-party-mcp)
- [OpenSearch](https://help.aliyun.com/zh/open-search/)
- [计费说明](https://help.aliyun.com/zh/model-studio/billing-for-model-studio)
- [免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)
