![这是图片](./images/title.png)
<div align="center">

<!-- # Grok Search MCP -->

[English](./docs/README_EN.md) | 简体中文

**通过 MCP 协议将 Grok 搜索能力集成到 Claude，显著增强文档检索与事实核查能力**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.0.0+-green.svg)](https://github.com/jlowin/fastmcp)

</div>

---

## 概述

Grok Search MCP 是一个基于 [FastMCP](https://github.com/jlowin/fastmcp) 构建的 MCP（Model Context Protocol）服务器，通过转接第三方平台（如 Grok）的强大搜索能力，为 Claude、Claude Code 等 AI 模型提供实时网络搜索功能。

### 核心价值
- **突破知识截止限制**：让 Claude 访问最新的网络信息，不再受训练数据时间限制
- **增强事实核查**：实时搜索验证信息的准确性和时效性
- **结构化输出**：返回包含标题、链接、摘要的标准化 JSON，便于 AI 模型理解与引用
- **即插即用**：通过 MCP 协议无缝集成到 Claude Desktop、Claude Code 等客户端


**工作流程**：`Claude → MCP → Grok API → 搜索/抓取 → 结构化返回`

## 为什么选择 Grok？

与其他搜索方案对比：

| 特性 | Grok Search MCP | Google Custom Search API | Bing Search API | SerpAPI |
|------|----------------|-------------------------|-----------------|---------|
| **AI 优化结果** | ✅ 专为 AI 理解优化 | ❌ 通用搜索结果 | ❌ 通用搜索结果 | ❌ 通用搜索结果 |
| **内容摘要质量** | ✅ AI 生成高质量摘要 | ⚠️ 需二次处理 | ⚠️ 需二次处理 | ⚠️ 需二次处理 |
| **实时性** | ✅ 实时网络数据 | ✅ 实时 | ✅ 实时 | ✅ 实时 |
| **集成复杂度** | ✅ MCP 即插即用 | ⚠️ 需自行开发 | ⚠️ 需自行开发 | ⚠️ 需自行开发 |
| **返回格式** | ✅ AI 友好 JSON | ⚠️ 需格式化 | ⚠️ 需格式化 | ⚠️ 需格式化 |

## 功能特性

- ✅ OpenAI 兼容接口，环境变量配置
- ✅ 实时网络搜索 + 网页内容抓取
- ✅ 支持指定搜索平台（Twitter、Reddit、GitHub 等）
- ✅ 配置测试工具（连接测试 + API Key 脱敏）
- ✅ 可扩展架构，支持添加其他搜索 Provider

## 快速开始


**Python 环境**：
- Python 3.10 或更高版本
- 已配置 Claude Code 或 Claude Desktop

**uv 工具**（推荐的 Python 包管理器）：

请确保您已成功安装 [uv 工具](https://docs.astral.sh/uv/getting-started/installation/)：

<details>
<summary><b>Windows 安装</b></summary>
在 PowerShell 中运行以下命令：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**💡 重要提示** ：我们 **强烈推荐** Windows 用户在 WSL（Windows Subsystem for Linux）中运行本项目！

</details>

<details>
<summary><b>Linux/macOS 安装</b></summary>

使用 curl 或 wget 下载并安装：

```bash
# 使用 curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 wget
wget -qO- https://astral.sh/uv/install.sh | sh
```

</details>


### 1. 安装与配置

使用 `claude mcp add-json` 一键安装并配置：
**注意：**  需要替换 **GROK_API_URL** 以及 **GROK_API_KEY**这两个字段为你自己的站点以及密钥，目前只支持openai格式，所以如果需要使用grok，也需要使用转为openai格式的grok镜像站

```bash
claude mcp add-json grok-search --scope user '{
  "type": "stdio",
  "command": "uvx",
  "args": [
    "--from",
    "git+https://github.com/GuDaStudio/GrokSearch",
    "grok-search"
  ],
  "env": {
    "GROK_API_URL": "https://your-api-endpoint.com/v1",
    "GROK_API_KEY": "your-api-key-here"
  }
}'
```

#### 配置说明

配置通过**环境变量**进行，安装时直接在 `env` 字段中设置：

| 环境变量 | 必填 | 默认值 | 说明 |
|---------|------|--------|------|
| `GROK_API_URL` | ✅ | - | Grok API 地址（支持 OpenAI 格式） |
| `GROK_API_KEY` | ✅ | - | 您的 API Key |
| `GROK_DEBUG` | ❌ | `false` | 调试模式开关（`true`/`false`） |
| `GROK_LOG_LEVEL` | ❌ | `INFO` | 日志级别（DEBUG/INFO/WARNING/ERROR） |
| `GROK_LOG_DIR` | ❌ | `logs` | 日志文件存储目录 |

### 2. 验证安装

```bash
claude mcp list
```

应能看到 `grok-search` 服务器已注册。

### 3. 测试配置

配置完成后，**强烈建议**在 Claude 对话中运行配置测试，以确保一切正常：

在 Claude 对话中输入：
```
请测试 Grok Search 的配置
```

或直接说：
```
显示 grok-search 配置信息
```

工具会自动执行以下检查：
- ✅ 验证环境变量是否正确加载
- ✅ 测试 API 连接（向 `/models` 端点发送请求）
- ✅ 显示响应时间和可用模型数量
- ✅ 识别并报告任何配置错误

**成功示例输出**：
```json
{
  "api_url": "https://YOUR-API-URL/grok/v1",
  "api_key": "sk-a*****************xyz",
  "config_status": "✅ 配置完整",
  "connection_test": {
    "status": "✅ 连接成功",
    "message": "成功获取模型列表 (HTTP 200)，共 5 个模型",
    "response_time_ms": 234.56
  }
}
```

如果看到 `❌ 连接失败` 或 `⚠️ 连接异常`，请检查：
- API URL 是否正确
- API Key 是否有效
- 网络连接是否正常

### 4. 高级配置（可选）
为了更好的使用Grok Search 可以通过配置Claude Code或者类似的系统提示词来对整体Vibe Coding Cli进行优化，以Claude Code 为例可以编辑 ~/.claude/CLAUDE.md中坠下下面内容：
<details>
<summary><b>💡 Grok Search Enhance 系统提示词</b>（点击展开）</summary>

  # Grok Search Enhance 系统提示词

  ## 0. Module Activation
  **触发条件**：当需要执行以下操作时，自动激活本模块并**强制替换**内置工具：
  - 网络搜索 / 信息检索 / 事实核查
  - 获取网页内容 / URL 解析 / 文档抓取
  - 查询最新信息 / 突破知识截止限制

  ## 1. Tool Routing Policy

  ### 强制替换规则
  | 需求场景 | ❌ 禁用 (Built-in) | ✅ 强制使用 (GrokSearch) |
  | :--- | :--- | :--- |
  | 网络搜索 | `WebSearch` | `mcp__grok-search__web_search` |
  | 网页抓取 | `WebFetch` | `mcp__grok-search__web_fetch` |
  | 配置诊断 | N/A | `mcp__grok-search__get_config_info` |

  ### 工具能力矩阵

  | Tool | Function | Key Parameters | Output Format | Use Case |
  | :--- | :--- | :--- | :--- | :--- |
  | **web_search** | 实时网络搜索 | `query` (必填)<br>`platform` (可选: Twitter/GitHub/Reddit)<br>`min_results` / `max_results` | JSON Array<br>`{title, url, content}` | • 事实核查<br>• 最新资讯<br>• 技术文档检索 |
  | **web_fetch** | 网页内容抓取 | `url` (必填) | Structured Markdown<br>(含元数据头部) | • 完整文档获取<br>• 深度内容分析<br>• 链接内容验证 |
  | **get_config_info** | 配置状态检测 | 无参数 | JSON<br>`{api_url, status, connection_test}` | • 连接问题诊断<br>• 首次使用验证 |

  ## 2. Search Workflow

  ### Phase 1: 查询构建 (Query Construction)
  1.  **意图识别**：分析用户需求，确定搜索类型：
      - **广度搜索**：多源信息聚合 → 使用 `web_search`
      - **深度获取**：单一 URL 完整内容 → 使用 `web_fetch`
  2.  **参数优化**：
      - 若需聚焦特定平台，设置 `platform` 参数
      - 根据需求复杂度调整 `min_results` / `max_results`

  ### Phase 2: 搜索执行 (Search Execution)
  1.  **首选策略**：优先使用 `web_search` 获取结构化摘要
  2.  **深度补充**：若摘要不足以回答问题，对关键 URL 调用 `web_fetch` 获取完整内容
  3.  **迭代检索**：若首轮结果不满足需求，**调整查询词**后重新搜索（禁止直接放弃）

  ### Phase 3: 结果整合 (Result Synthesis)
  1.  **信息验证**：交叉比对多源结果，识别矛盾信息
  2.  **时效标注**：对时间敏感信息，**必须**标注信息来源与时间
  3.  **引用规范**：输出中**强制包含**来源 URL，格式：`[标题](URL)`

  ## 3. Error Handling

  | 错误类型 | 诊断方法 | 恢复策略 |
  | :--- | :--- | :--- |
  | 连接失败 | 调用 `get_config_info` 检查配置 | 提示用户检查 API URL / Key |
  | 无搜索结果 | 检查 query 是否过于具体 | 放宽搜索词，移除限定条件 |
  | 网页抓取超时 | 检查 URL 可访问性 | 尝试搜索替代来源 |
  | 内容被截断 | 检查目标页面结构 | 分段抓取或提示用户直接访问 |

  ## 4. Anti-Patterns

  | ❌ 禁止行为 | ✅ 正确做法 |
  | :--- | :--- |
  | 使用内置 `WebSearch` / `WebFetch` | **强制**使用 GrokSearch 对应工具 |
  | 搜索后不标注来源 | 输出**必须**包含 `[来源](URL)` 引用 |
  | 单次搜索失败即放弃 | 调整参数后至少重试 1 次 |
  | 假设网页内容而不抓取 | 对关键信息**必须**调用 `web_fetch` 验证 |
  | 忽略搜索结果的时效性 | 时间敏感信息**必须**标注日期 |

  ---
  模块说明：
  - 强制替换：明确禁用内置工具，强制路由到 GrokSearch
  - 三工具覆盖：web_search + web_fetch + get_config_info
  - 错误处理：包含配置诊断的恢复策略
  - 引用规范：强制标注来源，符合信息可追溯性要求

</details>

### 5. 项目相关说明

#### MCP 工具说明

本项目提供三个 MCP 工具：

##### `web_search` - 网络搜索

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `query` | string | ✅ | - | 搜索查询语句 |
| `platform` | string | ❌ | `""` | 聚焦搜索平台（如 `"Twitter"`, `"GitHub, Reddit"`） |
| `min_results` | int | ❌ | `3` | 最少返回结果数 |
| `max_results` | int | ❌ | `10` | 最多返回结果数 |

**返回**：包含 `title`、`url`、`content` 的 JSON 数组

##### `web_fetch` - 网页内容抓取

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `url` | string | ✅ | 目标网页 URL |

**功能**：获取完整网页内容并转换为结构化 Markdown，保留标题层级、列表、表格、代码块等元素

##### `get_config_info` - 配置信息查询

**无需参数**。显示配置状态、测试 API 连接、返回响应时间和可用模型数量（API Key 自动脱敏）

<details>
<summary><b>返回示例</b>（点击展开）</summary>

```json
{
  "api_url": "https://YOUR-API-URL/grok/v1",
  "api_key": "sk-a*****************xyz",
  "config_status": "✅ 配置完整",
  "connection_test": {
    "status": "✅ 连接成功",
    "message": "成功获取模型列表 (HTTP 200)，共 x 个模型",
    "response_time_ms": 234.56
  }
}
```

</details>

---

<details>
<summary><h2>项目架构</h2>（点击展开）</summary>

```
src/grok_search/
├── config.py          # 配置管理（环境变量）
├── server.py          # MCP 服务入口（注册工具）
├── logger.py          # 日志系统
├── utils.py           # 格式化工具
└── providers/
    ├── base.py        # SearchProvider 基类
    └── grok.py        # Grok API 实现
```

</details>

## 常见问题

**Q: 如何获取 Grok API 访问权限？**
A: 注册第三方平台 → 获取 API Endpoint 和 Key → 使用 `claude mcp add-json` 配置

**Q: 配置后如何验证？**
A: 在 Claude 对话中说"显示 grok-search 配置信息"，查看连接测试结果

## 许可证

本项目采用 [MIT License](LICENSE) 开源。

---

<div align="center">

**如果这个项目对您有帮助，请给个 ⭐ Star！**
[![Star History Chart](https://api.star-history.com/svg?repos=GuDaStudio/GrokSearch&type=date&legend=top-left)](https://www.star-history.com/#GuDaStudio/GrokSearch&type=date&legend=top-left)
</div>
