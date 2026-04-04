---
name: aliyun-bailian-sync
description: 定期同步阿里云百炼平台最新模型信息到 Notion，包括价格、功能、新模型发布等。支持每周自动更新和变更检测。
homepage: https://help.aliyun.com/zh/model-studio
metadata:
  {
    "openclaw":
      {
        "emoji": "🔄",
        "requires": { "env": ["DASHSCOPE_API_KEY", "NOTION_API_KEY"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "packages": ["requests", "hashlib", "notion-client"],
              "label": "Install sync dependencies",
            },
          ],
        "cron":
          {
            "name": "aliyun-bailian-weekly-sync",
            "schedule": "0 0 * * 1",
            "enabled": true,
            "description": "每周同步阿里云百炼信息",
          },
      },
  }
---

# 阿里云百炼信息同步 Skill

每周自动同步阿里云百炼平台的最新模型信息到 Notion 知识库。

## 功能特性

- ✅ **每周自动同步**: 每周一 00:00 自动执行
- ✅ **变更检测**: 智能检测价格、功能、新模型变更
- ✅ **Notion 集成**: 自动更新 Notion 文档
- ✅ **版本管理**: 自动记录版本和更新时间
- ✅ **变更通知**: 重大变更时通知用户

## 配置

### 环境变量

```bash
# 阿里云百炼 API Key (用于验证)
export DASHSCOPE_API_KEY="sk-xxx"

# Notion API Key
export NOTION_API_KEY="ntn_xxx"

# Notion 数据库 ID
export NOTION_BAILIAN_DB_ID="xxx"
```

### Cron 配置

```json5
{
  "cron": {
    "aliyun-bailian-weekly-sync": {
      "enabled": true,
      "schedule": "0 0 * * 1",  // 每周一 00:00
      "command": "python scripts/sync.py",
      "timeout": 300,
    }
  }
}
```

## 使用方法

### 手动触发同步

```bash
# 完整同步
openclaw skill run aliyun-bailian-sync --action sync

# 仅检查变更
openclaw skill run aliyun-bailian-sync --action check

# 强制更新 (不检查变更)
openclaw skill run aliyun-bailian-sync --action force-sync
```

### 查看同步状态

```bash
openclaw skill run aliyun-bailian-sync --action status
```

### 查看更新历史

```bash
openclaw skill run aliyun-bailian-sync --action history
```

## 信息源

### P0 级 (每周检查)

| 信息源 | URL |
|--------|-----|
| 模型大全 | https://help.aliyun.com/zh/model-studio/models |
| 定价详情 | https://help.aliyun.com/zh/model-studio/model-pricing |
| 智谱 GLM | https://help.aliyun.com/zh/model-studio/glm |
| Kimi | https://help.aliyun.com/zh/model-studio/kimi-api |
| DeepSeek | https://help.aliyun.com/zh/model-studio/deepseek-api |
| MiniMax | https://help.aliyun.com/zh/model-studio/minimax-api |
| Coding Plan | https://help.aliyun.com/zh/model-studio/coding-plan |

### P1 级 (每月检查)

| 信息源 | URL |
|--------|-----|
| API 参考 | https://help.aliyun.com/zh/model-studio/model-api-reference/ |
| 开发文档 | https://help.aliyun.com/zh/model-studio/development-documentation/ |
| 深度思考 | https://help.aliyun.com/zh/model-studio/deep-thinking |
| 联网搜索 | https://help.aliyun.com/zh/model-studio/web-search |
| Function Calling | https://help.aliyun.com/zh/model-studio/qwen-function-calling |

## 变更检测

### 检测内容

1. **价格变更**: 输入/输出价格变化 > 5%
2. **功能变更**: Think/搜索/Function Call 支持变化
3. **新模型**: 新增模型型号
4. **模型下线**: 模型状态变为不可用
5. **文档更新**: 关键文档内容变更

### 通知阈值

| 变更类型 | 通知方式 |
|---------|---------|
| 价格调整 > 10% | 立即通知 |
| 新旗舰模型发布 | 立即通知 |
| 功能下线 | 立即通知 |
| 一般更新 | 周报汇总 |

## Notion 文档结构

```
阿里云百炼知识库/
├── 阿里云百炼全系列能力清单 (主文档)
│   ├── 信息概览
│   ├── 官方信息源
│   ├── 千问系列
│   ├── 第三方模型
│   ├── Coding Plan
│   ├── 能力矩阵
│   └── 更新日志
├── 阿里云百炼信息收集和爬取方法
├── 更新日志/
│   └── 2026-03-31 更新记录
└── 归档/
    └── 历史版本/
```

## 输出示例

### 同步报告

```markdown
## 同步报告 - 2026-03-31

### 检查结果
- ✅ 模型大全 (无变更)
- ✅ 定价详情 (无变更)
- ⚠️  智谱 GLM (有变更)
  - GLM-4.7 价格调整：¥0.5 → ¥0.45
- ✅ Kimi (无变更)
- ✅ DeepSeek (无变更)
- ✅ MiniMax (无变更)

### 更新内容
1. 更新 GLM-4.7 价格信息
2. 记录变更到更新日志
3. 版本号：v26.3.1 → v26.3.2

### 下次同步
2026-04-07 00:00 (UTC+8)
```

## 故障排除

### 常见问题

**Q: 同步失败，提示 403**
A: 检查 Notion API Key 是否有效，确认页面已共享给集成

**Q: 内容解析失败**
A: 阿里云可能更新了页面结构，需要更新解析逻辑

**Q: Cron 未执行**
A: 检查 Gateway 日志，确认 Cron 配置正确

### 日志位置

```
C:\Users\jiuyou\.openclaw\logs\aliyun-bailian-sync.log
```

## 维护

### 每周检查

- [ ] 确认同步成功
- [ ] 检查 Notion 文档更新
- [ ] 审查变更日志

### 每月维护

- [ ] 验证所有链接
- [ ] 更新信息源列表
- [ ] 清理历史数据

## 相关文档

- [[阿里云百炼全系列能力清单]] - 主文档
- [[阿里云百炼信息收集和爬取方法]] - 详细方法

---

**版本**: v1.0  
**创建**: 2026-03-31  
**维护**: OpenClaw 自动维护
