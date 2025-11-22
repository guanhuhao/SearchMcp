<div align="center">

# Grok Search MCP

**通过 MCP 协议将 Grok 搜索能力集成到 Claude，显著增强文档检索与事实核查能力**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-0.1.0+-green.svg)](https://github.com/jlowin/fastmcp)

</div>

---

## 概述

Grok Search MCP 是一个基于 [FastMCP](https://github.com/jlowin/fastmcp) 构建的 MCP（Model Context Protocol）服务器，通过转接第三方平台（如 Grok）的强大搜索能力，为 Claude、Claude Code 等 AI 模型提供实时网络搜索功能。

### 核心价值

- **突破知识截止限制**：让 Claude 访问最新的网络信息，不再受训练数据时间限制
- **增强事实核查**：实时搜索验证信息的准确性和时效性
- **结构化输出**：返回包含标题、链接、摘要的标准化 JSON，便于 AI 模型理解与引用
- **即插即用**：通过 MCP 协议无缝集成到 Claude Desktop、Claude Code 等客户端

### 工作原理

```
Claude/Claude Code → MCP 调用 → Search MCP 服务 → 转接 Grok API → 网络搜索 → 结构化结果返回
```

1. Claude 通过 MCP 协议调用 `web_search` 工具
2. Search MCP 将请求转发到 Grok 第三方平台（OpenAI 兼容接口）
3. Grok 执行实时网络搜索并返回结果
4. Search MCP 格式化为结构化 JSON：`{title, url, content}`
5. Claude 基于搜索结果生成更准确、更新的回答

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

- ✅ 通过 OpenAI 兼容格式调用 Grok 搜索能力
- ✅ 灵活的 TOML 配置文件管理
- ✅ 格式化搜索结果输出（标题 + 链接 + 摘要）
- ✅ 可扩展架构，支持添加其他搜索 Provider
- ✅ 完善的日志系统，便于调试和监控
- ✅ 调试模式开关，方便开发测试

## 快速开始

### 0. 前置要求

#### 安装必要工具（uv）

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

> **💡 重要提示**：我们**强烈推荐** Windows 用户在 WSL（Windows Subsystem for Linux）中运行本项目！

#### 获取 Grok API 访问权限

- 注册支持 Grok 的第三方平台账户
- 获取 API Endpoint 和 API Key

<!-- 如果您正在为订阅和配置而忧愁，我们非常欢迎您[积极联系我们](https://cc.guda.studio)。 -->

### 1. 安装

使用 `claude mcp add` 一键安装并配置：

```bash
claude mcp add search-mcp -s user --transport stdio -- uvx --from git+https://github.com/GuDaStudio/SearchMcp.git search-mcp
```

### 2. 配置

#### 配置文件说明

配置文件位置：
- **自动创建位置**：`~/.config/search-mcp/config.toml`
- **项目开发模式**：`./config.toml`（与 `config.toml.example` 同级）

首次运行时会自动创建配置文件模板。

编辑 `config.toml` 文件：

```toml
[debug]
enabled = false  # 生产环境设为 false，开发调试时设为 true

[grok]
api_url = "https://your-grok-api-endpoint.com/v1"  # 替换为实际的 Grok API 地址（目前支持Openai格式）
api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"    # 替换为您的实际 API Key

[logging]
level = "INFO"  # 日志级别：DEBUG, INFO, WARNING, ERROR
dir = "logs"    # 日志文件存储目录
```
欢迎使用我们的服务 https://cc.guda.studio/ 

⚠️ **安全提示**：
- 请勿将包含真实 API Key 的 `config.toml` 提交到 Git
- 项目已在 `.gitignore` 中排除此文件
- 用户目录配置（`~/.config/search-mcp/`）不会被 Git 追踪

### 3. 验证安装：

```bash
claude mcp list
```

应能看到 `search-mcp` 服务器已注册。

### 4. 使用示例

#### 实际对话场景

在 Claude 对话中直接询问需要实时搜索的问题：

**示例 1：技术文档查询**
```
用户：FastMCP 最新版本是什么？有哪些新功能？

Claude：[自动调用 web_search 工具]
根据最新搜索结果，FastMCP 当前版本是 0.2.1，主要新增了...
```

**示例 2：实时新闻**
```
用户：今天有哪些重要的 AI 行业新闻？

Claude：[自动调用 web_search 工具]
今天的重要 AI 新闻包括：
1. OpenAI 发布...
2. Google DeepMind...
```

**示例 3：事实核查**
```
用户：帮我验证一下"Python 3.13 已经发布"这个说法是否准确。

Claude：[自动调用 web_search 工具]
根据搜索结果，Python 3.13 确实已于...
```

#### 工具响应格式

`web_search` 工具返回的 JSON 结构：

```json
{
  "results": [
    {
      "title": "FastMCP - Python framework for MCP servers",
      "url": "https://github.com/jlowin/fastmcp",
      "content": "FastMCP is a Python framework that makes it easy to build Model Context Protocol (MCP) servers..."
    },
    {
      "title": "FastMCP Documentation",
      "url": "https://fastmcp.readthedocs.io/",
      "content": "Complete guide to building MCP servers with FastMCP..."
    }
  ],
  "provider": "grok",
  "query": "FastMCP latest version"
}
```

---

## 项目架构

```
search-mcp/
├── config.toml.example         # 配置文件模板
├── pyproject.toml              # 项目元数据与依赖
├── README.md                   # 项目文档
└── src/search_mcp/
    ├── __init__.py             # 包入口
    ├── config.py               # 配置管理（TOML 加载）
    ├── logger.py               # 日志系统
    ├── server.py               # MCP 服务器主程序
    ├── utils.py                # 结果格式化工具
    └── providers/              # 搜索 Provider 抽象层
        ├── __init__.py
        ├── base.py             # SearchProvider 基类
        └── grok.py             # Grok API 实现
```

### 核心模块说明

| 模块 | 职责 |
|------|------|
| `server.py` | FastMCP 服务入口，注册 `web_search` 工具 |
| `config.py` | 单例模式管理 TOML 配置 |
| `providers/base.py` | 定义 `SearchProvider` 抽象接口和 `SearchResult` 数据模型 |
| `providers/grok.py` | 实现 Grok API 调用与响应解析 |
| `utils.py` | 格式化搜索结果为 AI 友好的文本 |

## Others

### 提交 Issue

遇到问题或有建议？请[提交 Issue](https://github.com/yourusername/search-mcp/issues)。

## 常见问题

<details>
<summary><b>Q: 如何获取 Grok API 访问权限？</b></summary>

A: 本项目使用第三方平台转接 Grok API。您需要：
1. 注册支持 Grok 的第三方服务（如某些 AI Gateway）
2. 获取 API Endpoint 和 API Key
3. 在 `config.toml` 中配置相关信息
</details>

<details>
<summary><b>Q: 可以同时使用多个搜索 Provider 吗？</b></summary>

A: 当前版本仅支持单一 Provider。多 Provider 支持已在路线图中，将在未来版本实现。
</details>

<details>
<summary><b>Q: 搜索结果数量如何控制？</b></summary>

A: `web_search` 工具接受 `max_results` 参数（默认 5），Claude 会根据需要自动调整。
</details>

<details>
<summary><b>Q: 支持其他 AI 模型吗？</b></summary>

A: 支持！任何兼容 MCP 协议的客户端都可以使用，包括但不限于 Claude Desktop、Claude Code、其他 MCP 客户端。
</details>

## 许可证

本项目采用 [MIT License](LICENSE) 开源。

## 联系方式

- 作者：GuDa Studio
- 项目地址：https://github.com/yourusername/search-mcp

---

<div align="center">

**如果这个项目对您有帮助，请给个 ⭐ Star！**

</div>
