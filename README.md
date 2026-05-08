<div align="center">

# Ci Cd Generator Ai MCP

**MCP server for ci cd generator ai mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-ci-cd-generator-ai-mcp)](https://pypi.org/project/meok-ci-cd-generator-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Ci Cd Generator Ai MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `generate_pipeline` | Generate a CI/CD pipeline configuration for the specified language and platform  |
| `validate_config` | Validate a CI/CD configuration for common errors and best practices. |
| `list_templates` | List available CI/CD pipeline templates and supported languages. |
| `optimize_stages` | Suggest optimizations for a CI/CD pipeline: caching, parallelism, matrix builds. |

## Installation

```bash
pip install meok-ci-cd-generator-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ci-cd-generator-ai": {
      "command": "python",
      "args": ["-m", "meok_ci_cd_generator_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
