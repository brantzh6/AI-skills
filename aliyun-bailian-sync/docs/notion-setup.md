# Notion 集成配置

## 目标文档

### 主文档
- **名称**: 阿里云百炼全系列能力清单
- **路径**: `C:\Users\jiuyou\.openclaw\workspace\notion\aliyun-bailian-capabilities.md`
- **Notion 链接**: [待创建]

### 方法文档
- **名称**: 阿里云百炼信息收集和爬取方法
- **路径**: `C:\Users\jiuyou\.openclaw\workspace\notion\aliyun-bailian-sync-method.md`
- **Notion 链接**: [待创建]

---

## Notion API 配置

### 1. 创建 Integration

1. 访问 https://www.notion.so/my-integrations
2. 点击 **New integration**
3. 填写信息:
   - **Name**: OpenClaw Bailian Sync
   - **Logo**: (可选)
   - **Associated workspace**: 选择你的 workspace
4. 点击 **Submit**
5. 复制 **Internal Integration Token** (`ntn_xxx`)

### 2. 共享页面给 Integration

1. 打开要同步的 Notion 页面
2. 点击右上角 **···** → **Connect to**
3. 选择 **OpenClaw Bailian Sync**
4. 确认授权

### 3. 获取 Database/Page ID

**Page ID 获取方法**:
1. 打开 Notion 页面
2. 点击 **···** → **Copy link**
3. 链接格式：`https://www.notion.so/xxx/Page-Name-{page_id}`
4. `{page_id}` 即为所求

**Database ID 获取方法**:
1. 打开 Database 页面
2. 链接格式：`https://www.notion.so/{workspace_id}/{database_id}?v={view_id}`
3. `{database_id}` 即为所求

---

## 环境变量配置

在 OpenClaw 配置中添加：

```bash
# Notion API Key
export NOTION_API_KEY="ntn_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Notion Database ID (如果使用 Database)
export NOTION_BAILIAN_DB_ID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 或者在 openclaw.json 中配置
{
  "env": {
    "NOTION_API_KEY": "ntn_xxx",
    "NOTION_BAILIAN_DB_ID": "xxx"
  }
}
```

---

## Notion 页面结构

### 主页面模板

```
# 阿里云百炼全系列能力清单

## 📊 信息概览
[表格：模型数量统计]

## 🔗 官方信息源
[表格：信息源列表和链接]

## 📝 更新日志
[表格：版本更新记录]

## 🎯 千问 (Qwen) 系列
[表格：千问系列模型详情]

## 🌐 第三方模型
[表格：各厂商模型详情]

## 💼 Coding Plan
[套餐详情]

## 📊 能力矩阵
[表格：功能支持对比]

## 🔄 更新方法
[[阿里云百炼信息收集和爬取方法]]
```

---

## 同步逻辑

### 内容更新流程

```
1. 抓取阿里云百炼页面
   ↓
2. 计算内容哈希
   ↓
3. 对比历史哈希
   ↓
4. 如有变更 → 更新 Notion
   ↓
5. 记录更新日志
   ↓
6. 保存新哈希值
```

### Notion API 调用示例

```python
from notion_client import Client

notion = Client(auth=os.getenv("NOTION_API_KEY"))

# 更新页面内容
notion.pages.update(
    page_id=page_id,
    properties={
        "标题": {"title": [{"text": {"content": "新标题"}}]},
        "更新时间": {"date": {"start": datetime.now().isoformat()}}
    }
)

# 添加子页面
notion.pages.create(
    parent={"database_id": database_id},
    properties={
        "名称": {"title": [{"text": {"content": "新页面"}}]}
    }
)

# 追加内容到页面
notion.blocks.children.append(
    block_id=block_id,
    children=[
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": "新内容"}
                    }
                ]
            }
        }
    ]
)
```

---

## 版本管理

### Notion 页面属性

| 属性 | 类型 | 说明 |
|------|------|------|
| **版本** | Text | v26.3.1 |
| **更新时间** | Date | 2026-03-31 |
| **状态** | Select | ✅ 已同步 / ⚠️ 部分失败 / ❌ 失败 |
| **变更数** | Number | 本次更新的模型数量 |
| **操作人** | Text | 胖福 / OpenClaw |

### 版本命名规则

```
v{年}.{月}.{版本}

示例:
v26.3.1 - 2026 年 3 月第 1 版
v26.3.2 - 2026 年 3 月第 2 版
v26.4.1 - 2026 年 4 月第 1 版
```

---

## 更新日志格式

```markdown
## 更新日志

| 版本 | 日期 | 更新内容 | 操作人 |
|------|------|---------|--------|
| v26.3.1 | 2026-03-31 | 初始版本，完成全量信息收集 | 胖福 |
| | | | |
```

**更新内容示例**:
- 新增 DeepSeek-V3.2 模型
- 更新 GLM-4.7 价格：¥0.5 → ¥0.45
- 修复 Kimi-K2.5 上下文长度错误
- 新增 Coding Plan 套餐说明

---

## 故障排除

### 常见问题

**Q: 403 Forbidden**
A: 确认页面已共享给 Integration

**Q: 404 Not Found**
A: 检查 Page ID / Database ID 是否正确

**Q: 速率限制**
A: Notion API 限制 3 次/秒，添加延迟

**Q: 内容格式错误**
A: 检查 Markdown 转 Notion Block 的逻辑

---

## 相关资源

- [Notion API 文档](https://developers.notion.com/)
- [Notion Python SDK](https://github.com/ramnes/notion-sdk-py)
- [OpenClaw Notion Skill](../skills/notion/SKILL.md)

---

**最后更新**: 2026-03-31
