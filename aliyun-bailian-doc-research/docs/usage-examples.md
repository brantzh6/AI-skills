# 阿里云百炼文档研究 - 使用示例

本文档演示如何使用 `aliyun-bailian-doc-research` skill 进行文档研究。

---

## 🎯 场景 1：快速查找某个能力的文档

**需求**: 找到视频生成的所有官方文档

**步骤**:

1. **搜索核心文档**
   ```
   搜索：阿里云百炼 视频生成 独立文档 site:help.aliyun.com
   ```

2. **验证找到的链接**
   ```python
   web_fetch(
       url="https://help.aliyun.com/zh/model-studio/use-video-generation",
       extractMode="markdown",
       maxChars=5000
   )
   ```

3. **记录结果**
   ```markdown
   | 文档 | URL | 状态 |
   |------|-----|------|
   | 视频生成使用指南 | https://help.aliyun.com/zh/model-studio/use-video-generation | ✅ 有效 |
   | 文生视频指南 | https://help.aliyun.com/zh/model-studio/text-to-video-guide/ | ✅ 有效 |
   ```

**预期结果**: 2-3 个有效文档链接

---

## 🎯 场景 2：系统性研究整个平台

**需求**: 完整研究阿里云百炼所有能力

**步骤**:

### 第 1 步：核心文档定位 (15 分钟)

```
搜索 1: 阿里云百炼 模型大全 site:help.aliyun.com
搜索 2: 阿里云百炼 开发文档 site:help.aliyun.com
搜索 3: 阿里云百炼 用户指南 site:help.aliyun.com
```

**输出**: 3-5 个核心文档 URL

### 第 2 步：专项能力挖掘 (30 分钟)

对每个能力执行搜索：

```
# 图像
阿里云百炼 图像生成 文生图 独立文档 site:help.aliyun.com

# 视频
阿里云百炼 视频生成 文生视频 独立文档 site:help.aliyun.com

# 语音
阿里云百炼 语音识别 语音合成 独立文档 site:help.aliyun.com

# 视觉
阿里云百炼 视觉理解 VL 独立文档 site:help.aliyun.com

# 全模态
阿里云百炼 Omni 全模态 独立文档 site:help.aliyun.com
```

**输出**: 每个能力 2-5 个独立文档 URL

### 第 3 步：验证链接 (20 分钟)

对每个找到的 URL 执行：

```python
web_fetch(url="URL", extractMode="markdown", maxChars=1000)
```

**输出**: 已验证的 URL 列表

### 第 4 步：提取信息 (30 分钟)

从模型大全页面提取：
- 模型列表
- 价格信息
- 地域支持
- 能力矩阵

**输出**: 结构化信息表格

### 第 5 步：创建文档 (20 分钟)

创建以下文档：
1. `aliyun-bailian-capabilities.md` - 主文档
2. `aliyun-bailian-document-index.md` - 索引文档
3. `link-verification.md` - 验证报告

**输出**: 3 个完整文档

**总耗时**: 约 2 小时

---

## 🎯 场景 3：验证现有链接

**需求**: 验证已有文档中的所有链接是否有效

**步骤**:

1. **读取现有文档**
   ```python
   read(path="aliyun-bailian-capabilities.md")
   ```

2. **提取所有链接**
   ```python
   # 使用正则表达式提取 markdown 链接
   import re
   links = re.findall(r'\[.*?\]\((https?://.*?)\)', content)
   ```

3. **批量验证**
   ```python
   for link in links:
       result = web_fetch(url=link, extractMode="markdown", maxChars=1000)
       # 记录验证结果
   ```

4. **生成验证报告**
   ```markdown
   | URL | 状态 | 最后验证 |
   |-----|------|---------|
   | https://... | ✅ 有效 | 2026-04-01 |
   | https://... | ❌ 无效 | 2026-04-01 |
   ```

**预期结果**: 验证报告，包含有效/无效链接列表

---

## 🎯 场景 4：定期更新信息

**需求**: 每周检查文档是否有更新

**步骤**:

1. **加载上次研究的哈希值**
   ```python
   last_hashes = load_json(".cache/content_hashes.json")
   ```

2. **重新抓取核心文档**
   ```python
   current_content = web_fetch(url="核心 URL", maxChars=20000)
   current_hash = hashlib.sha256(current_content.encode()).hexdigest()
   ```

3. **对比哈希值**
   ```python
   if current_hash != last_hashes[url]:
       print(f"[变更] {url}")
       # 更新文档
   ```

4. **记录更新**
   ```markdown
   ## 更新日志 - 2026-04-01
   
   - 模型大全：无变更
   - 视频生成：新增 wan2.6-t2v 模型
   - 价格页面：无变更
   ```

**预期结果**: 更新日志

---

## 🎯 场景 5：查找特定模型的详细信息

**需求**: 查找 Qwen3.5-Plus 的所有信息

**步骤**:

1. **搜索模型相关信息**
   ```
   搜索：阿里云百炼 Qwen3.5-Plus site:help.aliyun.com
   ```

2. **查找模型文档**
   - 模型大全页面 → 基础信息
   - 视觉理解文档 → 多模态能力
   - API 参考 → 调用方式

3. **提取信息**
   ```markdown
   ## Qwen3.5-Plus
   
   **类型**: 多模态大模型
   **上下文**: 1M tokens
   **价格**: ¥0.8/¥4.8 每百万 tokens
   **地域**: 北京/新加坡
   **能力**: 
   - ✅ Think 模式
   - ✅ 联网搜索
   - ✅ 视觉理解
   - ✅ 视频理解
   ```

**预期结果**: 模型详细信息卡片

---

## 📋 最佳实践

### 搜索技巧

1. **始终使用 `site:help.aliyun.com`** 限制范围
2. **添加 "独立文档" 关键词** 过滤锚点链接
3. **搜索 10 条结果** 确保覆盖全面

### 验证技巧

1. **先快速验证** (maxChars=1000)
2. **再完整提取** (maxChars=20000)
3. **记录验证状态** 便于维护

### 组织技巧

1. **按能力分类** 组织文档
2. **使用表格** 呈现对比信息
3. **提供直接链接** 方便查阅

---

## ⚠️ 常见错误

### 错误 1：使用锚点链接

❌ 错误:
```markdown
[文生图](https://help.aliyun.com/zh/model-studio/models#96837528cdqes)
```

✅ 正确:
```markdown
[文生图](https://help.aliyun.com/zh/model-studio/image-generation/)
```

### 错误 2：未验证链接

❌ 错误:
- 直接使用搜索结果的链接
- 不验证链接是否有效

✅ 正确:
- 使用 `web_fetch` 验证每个链接
- 记录验证状态

### 错误 3：信息不完整

❌ 错误:
- 只记录模型名称
- 缺少价格、地域等关键信息

✅ 正确:
- 使用结构化表格
- 包含所有关键信息

---

**最后更新**: 2026-04-01  
**维护人**: 胖福
