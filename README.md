<!-- mcp-name: io.github.CSOAI-ORG/ci-cd-generator-ai-mcp -->
[![MCP Scorecard: 86/100](https://img.shields.io/badge/proofof.ai-86%2F100-5b21b6)](https://proofof.ai/scorecard/ci-cd-generator-ai-mcp.html)

# Ci Cd Generator Ai MCP

[![MEOK AI Labs](https://img.shields.io/badge/MEOK-AI%20Labs-667eea)](https://meok.ai)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-Install-3775a9)](https://pypi.org/project/ci_cd_generator_ai_mcp/)

> CI/CD pipeline generator MCP — GitHub Actions, GitLab CI, Azure DevOps, Jenkins

CI/CD pipeline generator MCP — GitHub Actions, GitLab CI, Azure DevOps, Jenkins. Security scanning integration. MIT.

---

## 🚀 Quick Start

```bash
# Install via pip
pip install ci_cd_generator_ai_mcp

# Or install via Smithery
npx -y @smithery/cli@latest install ci-cd-generator-ai-mcp --client claude
```

## ✨ Features

- MCP protocol compliant
- Easy installation
- Well-documented API
- Production-ready
- Active maintenance

## 📖 Documentation

- [Full Documentation](https://docs.meok.ai/ci-cd-generator-ai-mcp)
- [API Reference](https://api.meok.ai)
- [EU AI Act Compliance Guide](https://councilof.ai/compliance)

## 🛡️ Compliance

This MCP server is built with **EU AI Act compliance** built-in:

- ✅ Article 9 — Risk Management System
- ✅ Article 13 — Transparency & Instructions for Use
- ✅ Article 15 — Bias Detection & Testing
- ✅ Article 26 — FRIA Support (where applicable)
- ✅ Article 50 — AI Content Watermarking (where applicable)

Need help getting compliant? **[Book a free 15-min diagnostic →](https://cal.com/csoai/august-audit)**

## How MEOK charges

MEOK has no subscriptions and no tiers. You pay per job, and only when the agreed artifact has been delivered to you. There is no public price list. See <https://meok.ai/pricing>.

This repository's source is MIT-licensed and free to self-host.

## 🤝 Part of the MEOK Ecosystem

This server is part of the **[MEOK AI Labs](https://meok.ai)** ecosystem — 300+ MCP servers for sovereign AI governance.

| Domain | Purpose |
|--------|---------|
| [councilof.ai](https://councilof.ai) | EU AI Act compliance marketplace |
| [safetyof.ai](https://safetyof.ai) | AI safety & monitoring |
| [meok.ai](https://meok.ai) | Sovereign AI platform |
| [cobolbridge.ai](https://cobolbridge.ai) | Legacy modernization |

## 📜 License

MIT © [CSOAI-ORG](https://github.com/CSOAI-ORG)

---

<p align="center">
  <sub>Built with 💜 by <a href="https://meok.ai">MEOK AI Labs</a> · UK Companies House 16939677</sub>
</p>
Each tier above the free self-host adds HMAC-signed attestations verifiable at
`verify.meok.ai`. Linux Foundation governance on the A2A spine means EU regulated
buyers can deploy without vendor-lock-in objections.




## Configuration

Add to your `claude_desktop_config.json` (Claude Desktop) or your MCP client config:

```json
{
  "mcpServers": {
    "ci-cd-generator-ai-mcp": {
      "command": "uvx",
      "args": ["ci-cd-generator-ai-mcp"]
    }
  }
}
```

Or: `pip install ci-cd-generator-ai-mcp` then run the `ci-cd-generator-ai-mcp` command (stdio transport).

## Examples

Once configured, ask your assistant, for example:
- "Use `generate_pipeline` to …"
- "Use `validate_config` to …"
- "Use `list_templates` to …"

## See also

MEOK compliance MCP fleet:
[`cli-builder-ai-mcp`](https://github.com/CSOAI-ORG/cli-builder-ai-mcp), [`linkedin-outreach-mcp`](https://github.com/CSOAI-ORG/linkedin-outreach-mcp), [`lorem-ipsum-ai-mcp`](https://github.com/CSOAI-ORG/lorem-ipsum-ai-mcp), [`otp-ai-mcp`](https://github.com/CSOAI-ORG/otp-ai-mcp), [`recruitment-ai-mcp`](https://github.com/CSOAI-ORG/recruitment-ai-mcp)
