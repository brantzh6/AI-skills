---
name: aliyun-bailian-doc-research
description: 阿里云百炼文档研究方法，包括如何系统性地挖掘独立文档页面、验证链接有效性、提取模型信息和构建完整知识体系。
homepage: https://help.aliyun.com/zh/model-studio
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires": { "tools": ["web_search", "web_fetch"] },
        "install": [],
      },
  }
---

# 阿里云百炼文档研究方法 (Wan 2.7 Integrated)

**版本**: v1.1  
**更新时间**: 2026-04-04  
**适用场景**: 系统性研究阿里云百炼平台文档，跟踪最新模型发布 (如 Wan 2.7)

---

## 🎯 目标

建立一套**可复用的文档研究方法**，用于：
1. 系统性挖掘所有独立文档页面
2. 验证链接有效性
3. 提取结构化模型信息
4. 构建完整知识体系

---

## 📋 研究流程

### 阶段 1：核心文档定位 (15 分钟)

**目标**: 找到文档体系的入口页面

**步骤**:

1. **搜索模型大全页面**
   ```
   阿里云百炼 模型大全 site:help.aliyun.com
   ```
   - 目标 URL: `https://help.aliyun.com/zh/model-studio/models`
   - 这是**最核心的页面**，包含所有模型列表

2. **搜索开发文档总览**
   ```
   阿里云百炼 开发文档 site:help.aliyun.com
   ```
   - 目标 URL: `https://help.aliyun.com/zh/model-studio/development-documentation/`
   - 了解文档体系结构

3. **搜索用户指南**
   ```
   阿里云百炼 用户指南 site:help.aliyun.com
   ```
   - 目标 URL: `https://help.aliyun.com/zh/model-studio/model-user-guide/`
   - 了解使用方法

**工具**: `web_search` (count: 10)

**输出**: 核心文档 URL 列表

---

### 阶段 2：专项能力文档挖掘 (30 分钟)

**目标**: 为每个能力领域找到独立文档页面

**步骤**:

1. **按能力类别搜索**

   对每个能力类别执行搜索：

   ```
   # 图像生成
   阿里云百炼 图像生成 文生图 独立文档 site:help.aliyun.com
   
   # 视频生成
   阿里云百炼 视频生成 文生视频 独立文档 site:help.aliyun.com
   
   # 语音处理
   阿里云百炼 语音识别 语音合成 TTS ASR 独立文档 site:help.aliyun.com
   
   # 视觉理解
   阿里云百炼 视觉理解 VL 独立文档 site:help.aliyun.com
   
   # 全模态
   阿里云百炼 Omni 全模态 独立文档 site:help.aliyun.com
   
   # Embedding
   阿里云百炼 embedding 向量 独立文档 site:help.aliyun.com
   ```

2. **识别独立文档页面**

   **有效独立文档特征**:
   - ✅ URL 格式：`/zh/model-studio/{能力名称}/` 或 `/zh/model-studio/{具体功能}`
   - ✅ 标题包含完整能力名称
   - ✅ 内容包含完整的功能介绍、API 参考、使用指南
   - ❌ 避免：URL 包含 `#` 锚点的链接

   **示例**:
   - ✅ `https://help.aliyun.com/zh/model-studio/image-generation/` (独立页面)
   - ✅ `https://help.aliyun.com/zh/model-studio/use-video-generation` (独立页面)
   - ❌ `https://help.aliyun.com/zh/model-studio/models#96837528cdqes` (锚点链接，无效)

3. **验证文档有效性**

   对每个找到的 URL 执行：
   ```
   web_fetch(url="找到的 URL", extractMode="markdown", maxChars=5000)
   ```

   **验证标准**:
   - ✅ 返回状态码 200
   - ✅ 内容包含完整的功能介绍
   - ✅ 包含 API 调用示例或价格信息
   - ❌ 如果返回 404 或内容过少，标记为无效

**工具**: `web_search` + `web_fetch` 组合

**输出**: 专项能力独立文档 URL 列表（已验证）

---

### 阶段 3：API 文档挖掘 (20 分钟)

**目标**: 找到各能力的 API 参考文档

**步骤**:

1. **搜索 API 参考**

   对每个能力搜索 API 文档：

   ```
   # 图像 API
   阿里云百炼 图像生成 API 参考 site:help.aliyun.com
   
   # 视频 API
   阿里云百炼 视频生成 API 参考 site:help.aliyun.com
   
   # 语音 API
   阿里云百炼 语音识别 API 参考 site:help.aliyun.com
   ```

2. **识别 API 文档特征**

   **API 文档特征**:
   - ✅ URL 包含 `api-reference` 或 `api`
   - ✅ 标题包含 "API 参考"
   - ✅ 内容包含请求参数、响应示例、错误码

   **示例**:
   - `https://help.aliyun.com/zh/model-studio/qwen-image-api`
   - `https://help.aliyun.com/zh/model-studio/text-to-video-api-reference`

3. **验证并记录**

   使用 `web_fetch` 验证每个 API 文档

**输出**: API 参考文档列表

---

### 阶段 4：使用指南挖掘 (15 分钟)

**目标**: 找到各能力的使用指南和最佳实践

**步骤**:

1. **搜索使用指南**

   ```
   # 图像使用
   阿里云百炼 图像编辑 使用指南 site:help.aliyun.com
   
   # 视频使用
   阿里云百炼 视频生成 使用方法 site:help.aliyun.com
   
   # 语音使用
   阿里云百炼 语音合成 使用指南 site:help.aliyun.com
   ```

2. **识别使用指南特征**

   **使用指南特征**:
   - ✅ URL 包含 `guide`、`use`、`how-to`
   - ✅ 标题包含 "使用指南"、"使用方法"、"最佳实践"
   - ✅ 内容包含操作步骤、示例代码、场景推荐

   **示例**:
   - `https://help.aliyun.com/zh/model-studio/qwen-image-edit-guide`
   - `https://help.aliyun.com/zh/model-studio/text-to-video-guide/`

**输出**: 使用指南列表

---

### 阶段 5：信息提取与结构化 (30 分钟)

**目标**: 从文档中提取结构化信息

**步骤**:

1. **提取模型列表**

   从模型大全页面提取：
   ```markdown
   | 模型名称 | 类型 | 上下文 | 价格 | 地域 | 状态 |
   |---------|------|--------|------|------|------|
   | Qwen3-Max | 文本 | 256K | ¥2.5-15/¥10-60 | 北京 | ✅ |
   ```

2. **提取能力矩阵**

   从各独立文档提取功能支持：
   ```markdown
   | 能力 | 支持模型 | 文档链接 |
   |------|---------|---------|
   | Think 模式 | Qwen3-Max, Qwen3.5-Plus | [详情](URL) |
   | 联网搜索 | Qwen3.5 系列 | [详情](URL) |
   ```

3. **提取价格信息**

   从定价文档提取：
   ```markdown
   | 模型 | 输入价格 | 输出价格 | 免费额度 |
   |------|---------|---------|---------|
   | Qwen3.5-Plus | ¥0.8/百万 | ¥4.8/百万 | 100 万 |
   ```

4. **提取地域支持**

   从地域文档提取：
   ```markdown
   | 地域 | Base URL | API Key | 支持模型 |
   |------|---------|--------|---------|
   | 北京 | dashscope.aliyuncs.com | 独立 | 全部 |
   | 新加坡 | dashscope-intl.aliyuncs.com | 独立 | 大部分 |
   ```

**工具**: `web_fetch` + 手动整理

**输出**: 结构化信息表格

---

### 阶段 6：链接验证与勘误 (15 分钟)

**目标**: 验证所有链接有效性，建立勘误表

**步骤**:

1. **批量验证链接**

   对每个收集到的 URL 执行：
   ```
   web_fetch(url="URL", extractMode="markdown", maxChars=1000)
   ```

2. **记录验证结果**

   ```markdown
   | URL | 状态 | 备注 |
   |-----|------|------|
   | https://.../image-generation/ | ✅ 有效 | 独立页面 |
   | https://.../models#xxxxx | ❌ 无效 | 锚点链接 |
   ```

3. **建立勘误表**

   记录所有无效链接和正确链接：
   ```markdown
   ## 无效链接（已移除）
   ❌ https://help.aliyun.com/zh/model-studio/models#96837528cdqes
   ✅ 更正：https://help.aliyun.com/zh/model-studio/image-generation/
   ```

**输出**: 链接验证报告

---

## 🛠️ 工具使用技巧

### web_search 技巧

1. **精确搜索**
   ```
   阿里云百炼 {能力名称} 独立文档 site:help.aliyun.com
   ```

2. **排除锚点链接**
   ```
   阿里云百炼 {能力} -"#" site:help.aliyun.com
   ```

3. **查找 API 文档**
   ```
   阿里云百炼 {能力} API 参考 site:help.aliyun.com
   ```

### web_fetch 技巧

1. **快速验证**
   ```python
   web_fetch(url="URL", extractMode="markdown", maxChars=1000)
   ```
   - `maxChars=1000`: 快速验证页面是否有效

2. **完整提取**
   ```python
   web_fetch(url="URL", extractMode="markdown", maxChars=20000)
   ```
   - `maxChars=20000`: 提取完整内容

3. **提取模式选择**
   - `extractMode="markdown"`: 结构化内容（推荐）
   - `extractMode="text"`: 纯文本（备用）

---

## 📊 信息组织模板

### 主文档结构

```markdown
# 阿里云百炼全系列能力清单

## 📊 信息概览
[模型统计表]

## 🔗 官方信息源
[核心文档链接表格]

## 🎨 图像生成与编辑
[文生图模型表格]
[图像编辑模型表格]

## 🎬 视频生成与编辑
[文生视频模型表格]
[图生视频模型表格]

## 🎤 语音处理
[语音识别模型表格]
[语音合成模型表格]

## 🔮 全模态模型
[Omni 系列表格]

## 👁️ 视觉理解
[VL 系列表格]

## 📝 更新日志
[版本记录表格]
```

### 模型表格模板

```markdown
| 模型 | 上下文 | Think | 搜索 | 多模态 | 价格 | 地域 | 文档 |
|------|--------|-------|------|--------|------|------|------|
| 模型名 | 256K | ✅ | ✅ | ❌ | ¥1/¥4 | 北京 | [详情](URL) |
```

---

## ✅ 质量检查清单

### 链接验证

- [ ] 所有链接都是独立文档页面（非锚点）
- [ ] 所有链接都已通过 `web_fetch` 验证
- [ ] 无效链接已移除或更正

### 信息完整性

- [ ] 所有核心能力都有独立文档链接
- [ ] 所有模型都有价格信息
- [ ] 所有模型都有地域支持说明
- [ ] 所有能力都有 API 文档链接

### 信息准确性

- [ ] 模型参数已从官方文档核实
- [ ] 价格信息已核对最新版本
- [ ] 地域支持已确认

---

## 🔄 更新维护

### 每周更新 (Cron)

- 检查核心文档是否有更新
- 验证链接有效性
- 记录更新日志

### 每月更新

- 搜索新发布的模型
- 检查是否有新的独立文档页面
- 更新模型对比表格

### 每季度更新

- 全面审查文档结构
- 清理失效链接
- 更新推荐方案

---

## 📋 输出文档清单

完成研究后，应创建以下文档：

1. **主文档**: `aliyun-bailian-capabilities.md`
   - 完整能力清单
   - 模型对比表格
   - 官方文档链接

2. **索引文档**: `aliyun-bailian-document-index.md`
   - 独立文档完整列表
   - 按能力分类
   - 文档统计

3. **验证文档**: `link-verification.md`
   - 链接验证报告
   - 无效链接勘误
   - 更正记录

4. **方法文档**: `research-methodology.md` (本文档)
   - 研究方法记录
   - 工具使用技巧
   - 最佳实践

---

## 💡 最佳实践

### 搜索技巧

1. **始终使用 `site:help.aliyun.com`** 限制搜索范围
2. **使用 "独立文档" 关键词** 过滤锚点链接
3. **搜索 10 条结果** 确保覆盖全面

### 验证技巧

1. **先快速验证** (maxChars=1000) 确认页面有效
2. **再完整提取** (maxChars=20000) 获取完整信息
3. **记录验证状态** 便于后续维护

### 组织技巧

1. **按能力分类** 组织文档
2. **使用表格** 呈现对比信息
3. **提供直接链接** 方便查阅

---

## 📞 常见问题

### Q: 如何判断一个链接是独立文档还是锚点链接？

**A**: 
- ✅ 独立文档：`/zh/model-studio/image-generation/`
- ❌ 锚点链接：`/zh/model-studio/models#96837528cdqes`

**判断标准**: URL 是否包含 `#` 符号

### Q: 如何快速找到某个能力的所有相关文档？

**A**: 使用组合搜索：
```
阿里云百炼 {能力名称} (API OR 使用 OR 指南) site:help.aliyun.com
```

### Q: 如何验证找到的文档是否有效？

**A**: 使用 `web_fetch` 提取内容：
- 如果返回 200 且内容完整 → ✅ 有效
- 如果返回 404 或内容过少 → ❌ 无效

---

**文档状态**: ✅ 已完成  
**适用版本**: 阿里云百炼 2026 版  
**维护人**: 胖福
