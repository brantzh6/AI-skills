# 阿里云搜索 (aliyun-search)

> 提供三种阿里云搜索能力：模型内置联网搜索 + OpenSearch 企业级搜索 + 商品搜索推荐

## 配置

复制 `.env.example` 为 `.env` 并填入 API Key：

```bash
cp .env.example .env
```

`.env` 文件内容：
```env
# 百炼 API Key（联网搜索、商品搜索必需）
DASHSCOPE_API_KEY=sk-xxx

# OpenSearch 配置（企业级搜索必需）
OPENSEARCH_API_KEY=OS-xxx
OPENSEARCH_ENDPOINT=xxx.platform-cn-shanghai.opensearch.aliyuncs.com
OPENSEARCH_WORKSPACE=default
ES_HOST=http://your-es-host:9200
ES_AUTH=elastic:yourpassword
```

## 使用方式

### 能力一：模型内置联网搜索

```bash
# 简单搜索（默认 qwen-plus + turbo 策略）
python aliyun_search.py web "近期美股表现如何"

# 指定模型和策略
python aliyun_search.py web "杭州天气" -m qwen3.6-plus -s max

# 流式输出
python aliyun_search.py web "Qwen最新进展" --stream
```

搜索策略：
- `turbo`（默认）：兼顾速度与效果
- `max`：多源搜索，更详尽
- `agent`：多轮检索+信息整合（额外收费）
- `agent_max`：agent + 网页抓取（额外收费）

### 能力二：OpenSearch 智能搜索

```bash
# 知识库问答（默认服务）
python aliyun_search.py opensearch "AI搜索开放平台可以做什么"

# 指定服务和索引
python aliyun_search.py opensearch "如何搭建RAG链路" -s ops-qwen-plus -i my_rag_index
```

### 能力三：商品搜索推荐

```bash
# 简单搜索
python aliyun_search.py product "无线蓝牙耳机"

# 指定类目、价格范围、排序
python aliyun_search.py product "机械键盘" -c "数码配件" -p "200-500" -s relevance

# 价格从低到高排序
python aliyun_search.py product "平板电脑" -p "1000-3000" -s price_asc

# 销量优先，返回 10 个商品
python aliyun_search.py product "电动牙刷" -s sales -n 10
```

排序方式：
- `relevance`（默认）：综合相关度
- `price_asc`：价格从低到高
- `price_desc`：价格从高到低
- `sales`：销量优先

## Python API 调用

```python
from aliyun_search import web_search, opensearch_query, product_search

# 联网搜索
result = web_search("近期美股表现", model="qwen-plus")

# 知识库问答
result = opensearch_query("产品功能介绍")
print(result["answer"])
print(result["sources"])  # 参考文档列表

# 商品搜索推荐
result = product_search("无线蓝牙耳机", price_range="100-500", sort_by="sales")
for product in result.get("products", []):
    print(f"{product['name']} - ¥{product['price']}")
print(result.get("recommendations"))  # 推荐摘要
```

## 依赖

```bash
pip install openai elasticsearch
```
