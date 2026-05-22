#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云百炼信息同步脚本
每周自动同步最新模型信息到 Notion
"""

import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

# 配置
CONFIG = {
    "sources": {
        "P0": [
            {
                "name": "模型大全",
                "url": "https://help.aliyun.com/zh/model-studio/models",
                "check_frequency": "weekly"
            },
            {
                "name": "智谱 GLM",
                "url": "https://help.aliyun.com/zh/model-studio/glm",
                "check_frequency": "weekly"
            },
            {
                "name": "Kimi",
                "url": "https://help.aliyun.com/zh/model-studio/kimi-api",
                "check_frequency": "weekly"
            },
            {
                "name": "DeepSeek",
                "url": "https://help.aliyun.com/zh/model-studio/deepseek-api",
                "check_frequency": "weekly"
            },
            {
                "name": "MiniMax",
                "url": "https://help.aliyun.com/zh/model-studio/minimax-api",
                "check_frequency": "weekly"
            },
            {
                "name": "Coding Plan",
                "url": "https://help.aliyun.com/zh/model-studio/coding-plan",
                "check_frequency": "weekly"
            }
        ],
        "P1": [
            {
                "name": "API 参考",
                "url": "https://help.aliyun.com/zh/model-studio/model-api-reference/",
                "check_frequency": "monthly"
            },
            {
                "name": "深度思考",
                "url": "https://help.aliyun.com/zh/model-studio/deep-thinking",
                "check_frequency": "monthly"
            }
        ]
    },
    "notion": {
        "database_id": os.getenv("NOTION_BAILIAN_DB_ID", ""),
        "api_key": os.getenv("NOTION_API_KEY", "")
    },
    "storage": {
        "hash_file": Path(__file__).parent.parent / ".cache" / "content_hashes.json",
        "log_file": Path(__file__).parent.parent / ".cache" / "sync.log",
        "last_sync_file": Path(__file__).parent.parent / ".cache" / "last_sync.json"
    }
}


def log(message, level="INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] [{level}] {message}"
    print(log_msg)
    
    # 写入日志文件
    CONFIG["storage"]["log_file"].parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG["storage"]["log_file"], "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")


def get_content_hash(content):
    """计算内容哈希"""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def load_hashes():
    """加载历史哈希值"""
    if CONFIG["storage"]["hash_file"].exists():
        with open(CONFIG["storage"]["hash_file"], "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_hashes(hashes):
    """保存哈希值"""
    CONFIG["storage"]["hash_file"].parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG["storage"]["hash_file"], "w", encoding="utf-8") as f:
        json.dump(hashes, f, ensure_ascii=False, indent=2)


def fetch_page(url):
    """
    抓取页面内容
    实际实现中应该调用 OpenClaw 的 web_fetch 工具
    """
    log(f"抓取：{url}")
    
    # TODO: 实现实际的页面抓取逻辑
    # 可以使用 requests 或调用 OpenClaw 工具
    # 这里返回模拟内容
    
    return f"模拟内容 from {url}"


def detect_change(url, current_content):
    """检测内容是否变更"""
    hashes = load_hashes()
    current_hash = get_content_hash(current_content)
    last_hash = hashes.get(url, "")
    
    if current_hash != last_hash:
        log(f"检测到变更：{url}", "WARN")
        hashes[url] = current_hash
        save_hashes(hashes)
        return True
    else:
        log(f"无变更：{url}")
        return False


def update_notion(content, source_name):
    """
    更新 Notion 文档
    实际实现中应该调用 Notion API
    """
    log(f"更新 Notion: {source_name}")
    
    # TODO: 实现 Notion API 调用
    # 可以使用 notion-client 库
    
    return True


def save_sync_record(source_name, changed, timestamp):
    """保存同步记录"""
    records = []
    
    if CONFIG["storage"]["last_sync_file"].exists():
        with open(CONFIG["storage"]["last_sync_file"], "r", encoding="utf-8") as f:
            records = json.load(f)
    
    records.append({
        "source": source_name,
        "changed": changed,
        "timestamp": timestamp,
        "date": timestamp.strftime("%Y-%m-%d")
    })
    
    # 只保留最近 100 条记录
    records = records[-100:]
    
    CONFIG["storage"]["last_sync_file"].parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG["storage"]["last_sync_file"], "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def sync_source(source):
    """同步单个信息源"""
    log(f"开始同步：{source['name']}")
    
    try:
        # 抓取内容
        content = fetch_page(source["url"])
        
        # 检测变更
        changed = detect_change(source["url"], content)
        
        # 如果有变更，更新 Notion
        if changed:
            update_notion(content, source["name"])
            log(f"✓ {source['name']} 已更新", "SUCCESS")
        else:
            log(f"✓ {source['name']} 无变更")
        
        # 保存记录
        save_sync_record(source["name"], changed, datetime.now())
        
        return True
        
    except Exception as e:
        log(f"✗ {source['name']} 同步失败：{e}", "ERROR")
        return False


def sync_all(priority="P0"):
    """同步所有信息源"""
    log(f"=" * 50)
    log(f"开始同步 - 优先级：{priority}")
    log(f"=" * 50)
    
    sources = CONFIG["sources"].get(priority, [])
    
    if not sources:
        log(f"未找到 {priority} 级信息源", "WARN")
        return
    
    success_count = 0
    changed_count = 0
    
    for source in sources:
        if sync_source(source):
            success_count += 1
    
    # 统计结果
    log(f"=" * 50)
    log(f"同步完成")
    log(f"总计：{len(sources)} | 成功：{success_count} | 失败：{len(sources) - success_count}")
    log(f"=" * 50)


def check_status():
    """检查同步状态"""
    log("同步状态检查")
    
    if CONFIG["storage"]["last_sync_file"].exists():
        with open(CONFIG["storage"]["last_sync_file"], "r", encoding="utf-8") as f:
            records = json.load(f)
        
        if records:
            last_sync = records[-1]
            log(f"最后同步：{last_sync['date']}")
            log(f"最后同步源：{last_sync['source']}")
            log(f"是否有变更：{'是' if last_sync['changed'] else '否'}")
        else:
            log("暂无同步记录", "WARN")
    else:
        log("未找到同步记录文件", "WARN")


def main():
    """主函数"""
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == "sync":
            sync_all("P0")
        elif action == "sync-p1":
            sync_all("P1")
        elif action == "check":
            check_status()
        elif action == "force-sync":
            # 强制同步，不检查变更
            log("强制同步模式", "WARN")
            sync_all("P0")
        else:
            print(f"未知命令：{action}")
            print("可用命令：sync, sync-p1, check, force-sync")
            sys.exit(1)
    else:
        # 默认执行 P0 同步
        sync_all("P0")


if __name__ == "__main__":
    main()
