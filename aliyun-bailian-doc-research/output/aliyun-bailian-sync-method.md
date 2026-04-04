# 阿里云百炼信息收集和爬取方法

**版本**: v1.0  
**创建时间**: 2026-03-31  
**维护人**: 胖福

---

## 🎯 目标

定期（每周）自动收集阿里云百炼平台的最新模型信息，包括：
- 新模型发布
- 价格调整
- 功能更新
- 文档变更

---

## 📚 信息源清单

### 核心信息源

| 优先级 | 信息源 | URL | 检查频率 |
|--------|--------|-----|---------|
| **P0** | 模型大全 | https://help.aliyun.com/zh/model-studio/models | 每周 |
| **P0** | 定价详情 | https://help.aliyun.com/zh/model-studio/model-pricing | 每周 |
| **P1** | API 参考 | https://help.aliyun.com/zh/model-studio/model-api-reference/ | 每月 |
| **P1** | 开发文档 | https://help.aliyun.com/zh/model-studio/development-documentation/ | 每月 |

### 第三方模型信息源

| 厂商 | URL | 检查频率 |
|------|-----|---------|
| **智谱 GLM** | https://help.aliyun.com/zh/model-studio/glm | 每周 |
| **Kimi** | https://help.aliyun.com/zh/model-studio/kimi-api | 每周 |
| **DeepSeek** | https://help.aliyun.com/zh/model-studio/deepseek-api | 每周 |
| **MiniMax** | https://help.aliyun.com/zh/model-studio/minimax-api | 每周 |

### 专项能力信息源

| 能力 | URL | 检查频率 |
|------|-----|---------|
| 深度思考 | https://help.aliyun.com/zh/model-studio/deep-thinking | 每月 |
| 联网搜索 | https://help.aliyun.com/zh/model-studio/web-search | 每月 |
| Function Calling | https://help.aliyun.com/zh/model-studio/qwen-function-calling | 每月 |
| 上下文缓存 | https://help.aliyun.com/zh/model-studio/context-cache | 每月 |
| Coding Plan | https://help.aliyun.com/zh/model-studio/coding-plan | 每周 |

---

## 🛠️ 爬取工具和方法

### 方法 1: web_fetch 工具

**适用场景**: 单次或少量页面内容提取

```python
# OpenClaw web_fetch 工具
web_fetch(
    url="https://help.aliyun.com/zh/model-studio/models",
    extractMode="markdown",
    maxChars=20000
)
```

**优点**:
- ✅ 简单快速
- ✅ 自动提取正文
- ✅ 输出 Markdown 格式

**缺点**:
- ❌ 无法批量处理
- ❌ 无法检测变更

---

### 方法 2: web_search + web_fetch 组合

**适用场景**: 发现新文档/更新

```python
# 1. 搜索最新信息
web_search(
    query="阿里云百炼 新模型 2026 site:help.aliyun.com",
    count=10
)

# 2. 抓取搜索结果
for result in search_results:
    web_fetch(url=result.url, extractMode="markdown")
```

---

### 方法 3: 定期监控脚本 (推荐)

**脚本位置**: `C:\Users\jiuyou\.openclaw\skills\aliyun-bailian-sync\scripts\sync.py`

```python
#!/usr/bin/env python3
"""阿里云百炼信息同步脚本"""

import hashlib
import json
from datetime import datetime

# 信息源列表
SOURCES = [
    {
        "name": "模型大全",
        "url": "https://help.aliyun.com/zh/model-studio/models",
        "priority": "P0",
        "frequency": "weekly"
    },
    # ... 更多源
]

def fetch_page(url):
    """抓取页面内容"""
    # 使用 web_fetch 或 requests
    pass

def detect_change(content_hash, last_hash):
    """检测内容是否变更"""
    return content_hash != last_hash

def update_notion(content):
    """更新 Notion 文档"""
    # 调用 Notion API
    pass

def main():
    for source in SOURCES:
        content = fetch_page(source["url"])
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        if detect_change(content_hash, get_last_hash(source["url"])):
            print(f"[变更检测] {source['name']} 有更新")
            update_notion(content)
            save_hash(source["url"], content_hash)
        else:
            print(f"[无变更] {source['name']}")
    
    # 记录同步时间
    save_sync_time(datetime.now())

if __name__ == "__main__":
    main()
```

---

## 📅 更新计划

### 每周自动更新 (Cron)

**时间**: 每周一 00:00 (UTC+8)

**任务**:
1. 检查 P0 级信息源
2. 检测内容变更
3. 更新 Notion 文档
4. 记录更新日志
5. 通知用户（如有重大变更）

**Cron 配置**:
```json
{
  "name": "aliyun-bailian-sync",
  "schedule": "0 0 * * 1",
  "command": "python C:\\Users\\jiuyou\\.openclaw\\skills\\aliyun-bailian-sync\\scripts\\sync.py",
  "enabled": true
}
```

### 每月深度更新

**时间**: 每月 1 号

**任务**:
1. 检查 P1 级信息源
2. 验证所有链接有效性
3. 整理模型对比表格
4. 更新推荐方案

---

## 📊 变更检测逻辑

### 哈希对比法

```python
import hashlib

def get_content_hash(content):
    """计算内容哈希"""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def detect_change(current_hash, last_hash):
    """检测是否变更"""
    return current_hash != last_hash
```

### 关键字段监控

监控以下字段的变化：
- 模型价格
- 上下文长度
- 新功能支持 (Think/搜索/Function Call)
- 新模型发布

---

## 📝 Notion 文档结构

### 文档树

```
阿里云百炼知识库/
├── 阿里云百炼全系列能力清单 (主文档)
├── 阿里云百炼信息收集和爬取方法 (本文档)
├── 更新日志/
│   ├── 2026-03-31 更新记录
│   └── ...
└── 归档/
    ├── 历史版本/
    └── 废弃模型/
```

### 版本管理

**命名规则**: `v{年}.{月}.{版本}`

示例:
- v26.3.1 (2026 年 3 月第 1 版)
- v26.3.2 (2026 年 3 月第 2 版)

**版本记录**:
```markdown
| 版本 | 日期 | 更新内容 | 操作人 |
|------|------|---------|--------|
| v26.3.1 | 2026-03-31 | 初始版本 | 胖福 |
```

---

## 🔔 通知机制

### 重大变更通知

当检测到以下变更时，立即通知用户：

1. **价格调整** > 10%
2. **新模型发布** (旗舰级)
3. **功能下线**
4. **API 不兼容变更**

**通知方式**:
- Telegram 消息
- Notion 评论

---

## 🛡️ 错误处理

### 常见错误及处理

| 错误 | 原因 | 处理方案 |
|------|------|---------|
| 404 Not Found | 页面已删除/移动 | 记录错误，下次重试 |
| 403 Forbidden | 访问受限 | 检查是否需要登录 |
| Timeout | 网络超时 | 重试 3 次，失败则跳过 |
| 内容格式变更 | 页面结构变化 | 更新解析逻辑 |

### 重试机制

```python
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
def fetch_with_retry(url):
    return fetch_page(url)
```

---

## 📈 监控指标

### 同步成功率

```
成功率 = 成功同步的源数量 / 总源数量
目标：> 95%
```

### 更新及时性

```
延迟 = 实际更新时间 - 计划更新时间
目标：< 1 小时
```

### 数据准确性

```
准确率 = 正确字段数 / 总字段数
目标：> 99%
```

---

## 🔄 维护流程

### 每周检查清单

- [ ] 确认同步脚本正常运行
- [ ] 检查 Notion 文档更新
- [ ] 验证链接有效性
- [ ] 审查变更日志

### 每月维护任务

- [ ] 清理废弃链接
- [ ] 更新信息源列表
- [ ] 优化解析逻辑
- [ ] 备份历史数据

---

**文档维护**: 本内容由 OpenClaw 自动维护
**最后更新**: 2026-03-31 08:30 GMT+8
