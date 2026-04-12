# 阿里云搜索产品体系

> 更新时间：2026-04-12
> 来源：https://help.aliyun.com/zh/model-studio/web-search、https://help.aliyun.com/zh/open-search/

---

## 概述

阿里云提供多种搜索相关的产品和服务，覆盖从模型内置联网搜索到企业级搜索引擎的全场景需求。

---

## 一、模型内置联网搜索

让大语言模型能够获取互联网实时信息。

### 启用方式

```python
# Chat Completions API
client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "近期美股表现"}],
    extra_body={"enable_search": True}
)

# Responses API（推荐，支持多工具组合）
client.responses.create(
    model="qwen3.6-plus",
    input="杭州天气",
    tools=[
        {"type": "web_search"},       # 联网搜索
        {"type": "web_extractor"},    # 网页内容抓取
        {"type": "code_interpreter"}  # 代码解释器
    ]
)
```

### 搜索策略

| 策略 | 说明 | 额外收费 |
|------|------|----------|
| `turbo`（默认） | 兼顾速度与效果 | 无 |
| `max` | 多源搜索，更详尽 | 无 |
| `agent` | 多轮检索+整合 | 有 |
| `agent_max` | agent + 网页抓取 | 有 |

### 支持模型

qwen3.6-plus、qwen3.5-plus、qwen-plus、qwen3.5-flash、qwen-flash、qwen-turbo、qwen3-max 等

**文档来源：** [web-search](https://help.aliyun.com/zh/model-studio/web-search)

---

## 二、MCP Server 调用

通过 MCP（Model Context Protocol）协议调用外部工具服务。

### 调用方式

```python
mcp_tool = {
    "type": "mcp",
    "server_protocol": "sse",
    "server_label": "amap-maps",
    "server_description": "高德地图MCP Server，提供地图、导航、天气查询等能力。",
    "server_url": "https://dashscope.aliyuncs.com/api/v1/mcps/amap-maps/sse",
    "headers": {"Authorization": "Bearer " + os.getenv("DASHSCOPE_API_KEY")}
}

response = client.responses.create(
    model="qwen3.6-plus",
    input="从北京到上海怎么走",
    tools=[mcp_tool]
)
```

### 百炼官方 MCP 服务

| 服务 | 功能 | 费用 |
|------|------|------|
| Amap Maps | 地图、导航、天气查询 | 限时免费 |
| Sequential Thinking | 逐步推理 | 免费 |
| QuickChart | 图表绘制 | 免费 |

**文档来源：** [mcp](https://help.aliyun.com/zh/model-studio/mcp)、[official-and-third-party-mcp](https://help.aliyun.com/zh/model-studio/official-and-third-party-mcp)

---

## 三、OpenSearch 智能搜索

企业级搜索引擎，提供从数据解析、向量化、检索到 LLM 生成的全链路搜索能力。适用于 RAG、智能客服、企业知识库等场景。

### 产品系列

| 产品 | 说明 | 适用场景 |
|------|------|----------|
| **AI搜索开放平台** | 组件化服务（文档解析、向量化、联网搜索、LLM 等），自由组合 | RAG、多模态搜索 |
| **LLM 智能问答版** | 内置向量模型+LLM，一站式开箱即用 RAG | 对话式搜索、智能客服 |
| **向量检索版** | 高性能在线向量检索 | 图片/文本检索、推荐 |
| **召回引擎版** | 大规模文本召回检索 | 高性能低成本搜索 |
| **行业算法版** | 行业智能搜索系统 | 电商零售、游戏、内容社区、教育 |

### 核心能力

| 能力 | 服务 | 说明 |
|------|------|------|
| 数据解析 | 文档解析、图片解析、语音识别、视频截帧/切割/总结 | 非结构化数据转结构化 |
| 向量化 | 文本向量（稠密/稀疏）、多模态向量（Qwen2-VL） | 文本/图像转向量 |
| 搜索排序 | 向量检索、文本检索、相关性排序、多模态排序 | 检索+排序全链路 |
| 大模型 | Qwen3、QwQ、DeepSeek 全系、OpenSearch-千问-Turbo（RAG 微调版） | LLM 生成 |
| 联网搜索 | 当私有知识库无法回答时，联网补充信息 | 知识库+互联网 |

### 免费额度

开通后提供 **10 次免费服务调用额度**。

### RAG 链路示例

```
文档解析 → 图片解析 → 文档切片 → 文本向量化 → 写入ES索引
                                                    ↓
用户查询 → 查询向量化 → ES检索 → 排序 → 大模型生成回答
```

### 支持的搜索引擎

| 引擎 | 说明 |
|------|------|
| 阿里云 Elasticsearch | 开源兼容，100%兼容开源功能 |
| OpenSearch-向量检索版 | 阿里自研，高精度高性能 |

### 开发框架

支持 Java SDK、Python SDK、LangChain、LlamaIndex 四种开发框架。

**文档来源：** [open-search](https://help.aliyun.com/zh/open-search/)、[search-platform](https://help.aliyun.com/zh/open-search/search-platform/product-overview/introduction-to-search-platform)

---

## 四、搜索产品对比

| 产品 | 类型 | 特点 | 适用场景 | 费用 |
|------|------|------|----------|------|
| 模型内置搜索 | 模型内置 | 一行代码开启 | 简单问答、天气查询 | 按模型调用计费 |
| MCP Server | 协议集成 | 灵活配置外部工具 | 地图/天气/图表等 | 部分免费 |
| OpenSearch | 企业搜索引擎 | 全链路、组件化 | RAG/企业搜索/知识库 | 按量计费+免费额度 |

---

## 五、选型建议

| 场景 | 推荐方案 |
|------|----------|
| 简单实时问答（天气、新闻） | 模型内置 `enable_search: true` |
| 复杂研究（多源交叉验证） | Responses API + `search_strategy: "agent"` |
| 需要外部工具（地图、天气API） | MCP Server |
| 企业知识库/文档问答 | OpenSearch LLM 智能问答版 |
| 自定义 RAG 链路 | OpenSearch AI搜索开放平台 |
| 大规模向量检索 | OpenSearch 向量检索版 |
| 电商/内容社区搜索 | OpenSearch 行业算法版 |
