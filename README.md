# CI/CD Generator AI MCP Server

> By [MEOK AI Labs](https://meok.ai) — Generate CI/CD pipeline configurations for GitHub Actions, GitLab CI, and Jenkins

## Installation

```bash
pip install ci-cd-generator-ai-mcp
```

## Usage

```bash
python server.py
```

## Tools

### `generate_github_actions`
Generate a GitHub Actions workflow for a given language and test command.

**Parameters:**
- `language` (str): Programming language
- `test_command` (str): Test command to run

### `generate_gitlab_ci`
Generate a GitLab CI configuration file.

**Parameters:**
- `language` (str): Programming language

### `generate_jenkinsfile`
Generate a Jenkinsfile with configurable stages.

**Parameters:**
- `language` (str): Programming language
- `stages` (str): Comma-separated stages (default 'build,test,deploy')

### `lint_workflow`
Lint and validate a CI/CD workflow YAML file.

**Parameters:**
- `workflow_yaml` (str): Workflow YAML content

## Authentication

Free tier: 30 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT — MEOK AI Labs
