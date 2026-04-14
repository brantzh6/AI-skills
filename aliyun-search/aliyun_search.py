#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云搜索工具
支持三种搜索能力：
1. 模型内置联网搜索（enable_search）
2. OpenSearch 智能搜索（企业级搜索引擎/RAG）
3. 商品搜索推荐（基于联网搜索的结构化商品对比）

API Key 从 .env 文件读取
"""

import os
import sys
import json
import io
from pathlib import Path
from urllib.parse import quote_plus

# Fix Windows console encoding for Chinese
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 加载 .env 文件
def load_dotenv():
    """从 .env 文件加载环境变量"""
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

load_dotenv()

# ============================================================
# 能力一：模型内置联网搜索
# ============================================================

def web_search(query, model="qwen-plus", strategy="turbo", stream=False):
    """
    通过百炼模型内置联网搜索能力获取实时信息

    Args:
        query (str): 搜索查询
        model (str): 模型名称，默认 qwen-plus
        strategy (str): 搜索策略 - turbo(默认)/max/agent/agent_max
        stream (bool): 是否流式输出

    Returns:
        str: 搜索结果
    """
    try:
        from openai import OpenAI
    except ImportError:
        print("错误：请先安装 openai 库: pip install openai")
        sys.exit(1)

    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("错误：未找到 DASHSCOPE_API_KEY，请在 .env 文件中配置")
        sys.exit(1)

    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    extra_body = {
        "enable_search": True,
        "search_options": {
            "search_strategy": strategy
        }
    }

    if stream:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": query}],
            extra_body=extra_body,
            stream=True
        )
        result = ""
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                result += content
        print()
        return result
    else:
        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": query}],
            extra_body=extra_body
        )
        return completion.choices[0].message.content


# ============================================================
# 能力二：OpenSearch 智能搜索（通过 API 调用）
# ============================================================

def opensearch_query(query, service_id="ops-qwen-turbo", es_index="dense_vertex_index"):
    """
    通过 OpenSearch AI搜索开放平台进行知识库问答

    Args:
        query (str): 查询内容
        service_id (str): 大模型服务ID，默认 ops-qwen-turbo
        es_index (str): Elasticsearch 索引名称

    Returns:
        dict: 包含答案和相关文档的字典
    """
    try:
        from openai import OpenAI
        from elasticsearch import Elasticsearch
    except ImportError:
        print("错误：请先安装 openai 和 elasticsearch 库: pip install openai elasticsearch")
        sys.exit(1)

    api_key = os.getenv("OPENSEARCH_API_KEY")
    endpoint = os.getenv("OPENSEARCH_ENDPOINT")
    workspace = os.getenv("OPENSEARCH_WORKSPACE", "default")
    es_host = os.getenv("ES_HOST", "http://localhost:9200")
    es_auth = os.getenv("ES_AUTH", "elastic:changeme").split(":", 1)

    if not api_key or not endpoint:
        print("错误：未找到 OPENSEARCH_API_KEY 或 OPENSEARCH_ENDPOINT，请在 .env 文件中配置")
        sys.exit(1)

    # Step 1: 查询向量化
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 文本向量化
    embedding_url = f"http://{endpoint}/api/v1/workspaces/{workspace}/services/ops-text-embedding-002/queries/text-embedding"
    embedding_payload = {
        "texts": [query]
    }

    # Step 2: ES 向量检索
    es = Elasticsearch(
        [es_host],
        basic_auth=(es_auth[0], es_auth[1]),
        verify_certs=False
    )

    # 这里使用简化的直接 ES 文本搜索作为示例
    search_result = es.search(
        index=es_index,
        query={
            "multi_match": {
                "query": query,
                "fields": ["content", "title"]
            }
        },
        size=5
    )

    docs = []
    for hit in search_result["hits"]["hits"]:
        docs.append({
            "score": hit["_score"],
            "content": hit["_source"].get("content", "")
        })

    # Step 3: 使用大模型生成答案
    context = "\n\n".join([d["content"] for d in docs])

    client = OpenAI(
        api_key=api_key,
        base_url=f"http://{endpoint}/compatible-mode/v1"
    )

    prompt = f"""你是一个知识库问答助手。请根据以下参考资料回答问题。

参考资料：
{context}

问题：{query}

请根据参考资料给出准确、简洁的回答。如果参考资料中没有相关信息，请如实告知。"""

    response = client.chat.completions.create(
        model=service_id.replace("ops-", ""),
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": docs
    }


# ============================================================
# 能力三：商品搜索推荐
# ============================================================

def product_search(query, category=None, price_range=None, sort_by="relevance", limit=10):
    """
    商品搜索推荐：通过模型联网搜索获取商品信息，结构化输出
    
    基于阿里云 OpenSearch 行业算法版的商品搜索推荐能力，
    结合百炼模型联网搜索，提供商品检索、对比、推荐。
    
    Args:
        query (str): 搜索关键词（如 "无线蓝牙耳机"）
        category (str): 商品类目（可选，如 "数码配件"）
        price_range (str): 价格范围（可选，如 "100-500"）
        sort_by (str): 排序方式 - relevance(默认)/price_asc/price_desc/sales
        limit (int): 返回商品数量，默认 10
    
    Returns:
        dict: 结构化商品搜索结果
    """
    try:
        from openai import OpenAI
    except ImportError:
        print("错误：请先安装 openai 库: pip install openai")
        sys.exit(1)

    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("错误：未找到 DASHSCOPE_API_KEY，请在 .env 文件中配置")
        sys.exit(1)

    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # 构建搜索提示词
    prompt_parts = [f"请搜索并推荐以下商品：{query}"]
    
    if category:
        prompt_parts.append(f"类目：{category}")
    if price_range:
        prompt_parts.append(f"价格范围：{price_range} 元")
    
    sort_map = {
        "relevance": "综合相关度",
        "price_asc": "价格从低到高",
        "price_desc": "价格从高到低",
        "sales": "销量优先"
    }
    prompt_parts.append(f"排序方式：{sort_map.get(sort_by, '综合相关度')}")
    prompt_parts.append(f"请返回 {limit} 个商品的详细信息。")
    
    prompt_parts.append("""\n请严格按照以下 JSON 格式返回结果（不要包含 markdown 代码块标记）：
{
  "search_query": "搜索关键词",
  "total_results": 估计总数,
  "products": [
    {
      "name": "商品名称",
      "brand": "品牌",
      "price": 价格数字,
      "currency": "CNY",
      "category": "类目",
      "rating": 评分(1-5),
      "sales_count": "销量描述",
      "features": ["特点1", "特点2"],
      "pros": ["优点1"],
      "cons": ["缺点1"],
      "recommendation_reason": "推荐理由"
    }
  ],
  "recommendations": {
    "best_value": "性价比最高的商品名",
    "best_quality": "品质最好的商品名",
    "budget_pick": "最实惠的选择"
  }
}""")
    
    prompt = "\n".join(prompt_parts)
    
    extra_body = {
        "enable_search": True,
        "search_options": {
            "search_strategy": "max"
        }
    }
    
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[{"role": "user", "content": prompt}],
        extra_body=extra_body,
        temperature=0.3  # 降低随机性，确保 JSON 格式稳定
    )
    
    content = response.choices[0].message.content.strip()
    
    # 尝试解析 JSON
    try:
        # 移除可能的 markdown 代码块标记
        if content.startswith("```"):
            content = content.split("\n", 1)[1]
        if content.endswith("```"):
            content = content.rsplit("\n", 1)[0]
        content = content.strip()
        
        result = json.loads(content)
        return result
    except json.JSONDecodeError:
        # 如果 JSON 解析失败，返回原始文本
        return {"raw_response": content}


# ============================================================
# 命令行入口
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="阿里云搜索工具")
    subparsers = parser.add_subparsers(dest="command", help="选择搜索能力")

    # 子命令 1: web_search
    web_parser = subparsers.add_parser("web", help="模型内置联网搜索")
    web_parser.add_argument("query", help="搜索查询")
    web_parser.add_argument("-m", "--model", default="qwen-plus", help="模型名称")
    web_parser.add_argument("-s", "--strategy", default="turbo", choices=["turbo", "max", "agent", "agent_max"], help="搜索策略")
    web_parser.add_argument("--stream", action="store_true", help="流式输出")

    # 子命令 2: opensearch
    es_parser = subparsers.add_parser("opensearch", help="OpenSearch 智能搜索")
    es_parser.add_argument("query", help="查询内容")
    es_parser.add_argument("-s", "--service", default="ops-qwen-turbo", help="大模型服务ID")
    es_parser.add_argument("-i", "--index", default="dense_vertex_index", help="ES索引名称")

    # 子命令 3: product_search
    product_parser = subparsers.add_parser("product", help="商品搜索推荐")
    product_parser.add_argument("query", help="搜索关键词")
    product_parser.add_argument("-c", "--category", help="商品类目")
    product_parser.add_argument("-p", "--price", help="价格范围，如 100-500")
    product_parser.add_argument("-s", "--sort", default="relevance",
                               choices=["relevance", "price_asc", "price_desc", "sales"],
                               help="排序方式")
    product_parser.add_argument("-n", "--limit", type=int, default=5, help="返回商品数量")

    args = parser.parse_args()

    if args.command == "web":
        result = web_search(args.query, model=args.model, strategy=args.strategy, stream=args.stream)
        if not args.stream:
            print(f"\n搜索结果:\n{result}")

    elif args.command == "opensearch":
        result = opensearch_query(args.query, service_id=args.service, es_index=args.index)
        print(f"\n答案:\n{result['answer']}")
        print(f"\n参考文档 ({len(result['sources'])} 篇):")
        for i, doc in enumerate(result["sources"], 1):
            print(f"  {i}. [score: {doc['score']:.2f}] {doc['content'][:100]}...")

    elif args.command == "product":
        result = product_search(
            args.query,
            category=args.category,
            price_range=args.price,
            sort_by=args.sort,
            limit=args.limit
        )
        
        if "raw_response" in result:
            print(f"\n搜索结果:\n{result['raw_response']}")
        else:
            print(f"\n{'='*60}")
            print(f"🔍 搜索结果: {result.get('search_query', args.query)}")
            print(f"📊 估计总数: {result.get('total_results', 'N/A')}")
            print(f"{'='*60}")
            
            products = result.get("products", [])
            for i, p in enumerate(products, 1):
                print(f"\n{'─'*50}")
                print(f"  {i}. {p.get('name', '未知')}")
                print(f"     品牌: {p.get('brand', 'N/A')}")
                print(f"     价格: ¥{p.get('price', '?')}")
                print(f"     评分: {'⭐' * int(p.get('rating', 0))} ({p.get('rating', '?')})")
                print(f"     销量: {p.get('sales_count', 'N/A')}")
                if p.get('features'):
                    print(f"     特点: {', '.join(p['features'][:3])}")
                if p.get('recommendation_reason'):
                    print(f"     推荐: {p['recommendation_reason']}")
            
            recs = result.get("recommendations", {})
            if recs:
                print(f"\n{'='*60}")
                print("💡 推荐摘要:")
                if recs.get('best_value'):
                    print(f"  🏆 性价比之选: {recs['best_value']}")
                if recs.get('best_quality'):
                    print(f"  💎 品质之选: {recs['best_quality']}")
                if recs.get('budget_pick'):
                    print(f"  💰 实惠之选: {recs['budget_pick']}")
                print(f"{'='*60}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
