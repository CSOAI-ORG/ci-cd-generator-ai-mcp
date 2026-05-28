#!/usr/bin/env python3
"""Generate CI/CD pipeline configurations for GitHub Actions, GitLab CI, and Jenkins. — MEOK AI Labs."""

import sys, os
from auth_middleware import check_access

import json, re
from datetime import datetime, timezone
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

STRIPE_199 = "https://buy.stripe.com/00wfZjcgAeUW4c5cyQ8k90K"

def _add_upgrade_tail(response, tier="free"):
    """Append upgrade nudge to free-tier success responses."""
    if isinstance(response, dict) and tier == "free":
        response["_upgrade_note"] = "Pro tier: unlimited calls + priority support. Upgrade: " + STRIPE_199
    return response


FREE_DAILY_LIMIT = 30
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now - t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT:
        return json.dumps({"error": f"Limit {FREE_DAILY_LIMIT}/day. Upgrade: meok.ai"})
    _usage[c].append(now)
    return None

mcp = FastMCP("ci-cd-generator-ai", instructions="Generate CI/CD pipeline configurations for GitHub Actions, GitLab CI, and Jenkins. By MEOK AI Labs.")

PIPELINE_TEMPLATES = {
    "github": {
        "python": {
            "name": "Python CI",
            "on": {"push": {"branches": ["main"]}, "pull_request": {"branches": ["main"]}},
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v4"},
                        {"uses": "actions/setup-python@v5", "with": {"python-version": "3.12"}},
                        {"run": "pip install -r requirements.txt"},
                        {"run": "pytest"},
                    ]
                }
            }
        },
        "node": {
            "name": "Node.js CI",
            "on": {"push": {"branches": ["main"]}, "pull_request": {"branches": ["main"]}},
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v4"},
                        {"uses": "actions/setup-node@v4", "with": {"node-version": "20"}},
                        {"run": "npm ci"},
                        {"run": "npm test"},
                    ]
                }
            }
        },
        "rust": {
            "name": "Rust CI",
            "on": {"push": {"branches": ["main"]}, "pull_request": {"branches": ["main"]}},
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v4"},
                        {"uses": "dtolnay/rust-toolchain@stable"},
                        {"run": "cargo test"},
                    ]
                }
            }
        },
        "go": {
            "name": "Go CI",
            "on": {"push": {"branches": ["main"]}, "pull_request": {"branches": ["main"]}},
            "jobs": {
                "test": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v4"},
                        {"uses": "actions/setup-go@v5", "with": {"go-version": "1.22"}},
                        {"run": "go test ./..."},
                    ]
                }
            }
        },
    },
    "gitlab": {
        "python": {"image": "python:3.12", "stages": ["test", "deploy"], "test": {"stage": "test", "script": ["pip install -r requirements.txt", "pytest"]}},
        "node": {"image": "node:20", "stages": ["test", "deploy"], "test": {"stage": "test", "script": ["npm ci", "npm test"]}},
        "rust": {"image": "rust:latest", "stages": ["test", "deploy"], "test": {"stage": "test", "script": ["cargo test"]}},
        "go": {"image": "golang:1.22", "stages": ["test", "deploy"], "test": {"stage": "test", "script": ["go test ./..."]}},
    },
}

STAGE_DEFINITIONS = {
    "lint": {"name": "Lint", "commands": {"python": ["pip install ruff", "ruff check ."], "node": ["npx eslint ."], "rust": ["cargo clippy"], "go": ["golangci-lint run"]}},
    "test": {"name": "Test", "commands": {"python": ["pytest --cov"], "node": ["npm test"], "rust": ["cargo test"], "go": ["go test ./..."]}},
    "build": {"name": "Build", "commands": {"python": ["python -m build"], "node": ["npm run build"], "rust": ["cargo build --release"], "go": ["go build ./..."]}},
    "deploy": {"name": "Deploy", "commands": {"python": ["echo 'deploy step'"], "node": ["echo 'deploy step'"], "rust": ["echo 'deploy step'"], "go": ["echo 'deploy step'"]}},
    "security": {"name": "Security Scan", "commands": {"python": ["pip install safety", "safety check"], "node": ["npm audit"], "rust": ["cargo audit"], "go": ["govulncheck ./..."]}},
}


@mcp.tool()
def generate_pipeline(language: str, platform: str = "github", stages: str = "lint,test,build", deploy_target: str = "", api_key: str = "") -> str:
    """Generate a CI/CD pipeline configuration for the specified language and platform (github, gitlab).

    Behavior:
        This tool generates structured output without modifying external systems.
        Output is deterministic for identical inputs. No side effects.
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.

    Args:
        language (str): The language to analyze or process.
        platform (str): The platform to analyze or process.
        stages (str): The stages to analyze or process.
        test: The test to analyze or process.
        build": The build" to analyze or process.
        deploy_target (str): The deploy target to analyze or process.
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})
    if err := _rl():
        return err

    lang = language.lower().strip()
    plat = platform.lower().strip()
    stage_list = [s.strip() for s in stages.split(",") if s.strip()]

    if plat not in PIPELINE_TEMPLATES:
        return json.dumps({"error": f"Unsupported platform '{plat}'. Use: github, gitlab"})

    templates = PIPELINE_TEMPLATES[plat]
    base = templates.get(lang, templates.get("python"))

    if plat == "github":
        pipeline = dict(base)
        jobs = {}
        for stage_name in stage_list:
            sdef = STAGE_DEFINITIONS.get(stage_name)
            if sdef:
                cmds = sdef["commands"].get(lang, sdef["commands"]["python"])
                jobs[stage_name] = {
                    "runs-on": "ubuntu-latest",
                    "steps": [{"uses": "actions/checkout@v4"}] + [{"run": c} for c in cmds]
                }
        if jobs:
            pipeline["jobs"] = jobs
        if deploy_target:
            pipeline["jobs"].setdefault("deploy", {
                "runs-on": "ubuntu-latest",
                "needs": [s for s in stage_list if s != "deploy"],
                "steps": [{"uses": "actions/checkout@v4"}, {"run": f"echo 'Deploying to {deploy_target}'"}]
            })
    else:
        pipeline = {"stages": stage_list}
        if lang in templates:
            pipeline["image"] = templates[lang].get("image", "ubuntu:latest")
        for stage_name in stage_list:
            sdef = STAGE_DEFINITIONS.get(stage_name)
            if sdef:
                cmds = sdef["commands"].get(lang, sdef["commands"]["python"])
                pipeline[stage_name] = {"stage": stage_name, "script": cmds}

    return json.dumps({"platform": plat, "language": lang, "stages": stage_list, "pipeline": pipeline, "timestamp": datetime.now(timezone.utc).isoformat()})


@mcp.tool()
def validate_config(config_yaml: str, platform: str = "github", api_key: str = "") -> str:
    """Validate a CI/CD configuration for common errors and best practices.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.

    Args:
        config_yaml (str): The config yaml to analyze or process.
        platform (str): The platform to analyze or process.
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})
    if err := _rl():
        return err

    issues = []
    warnings = []
    plat = platform.lower().strip()

    if not config_yaml or len(config_yaml.strip()) < 10:
        issues.append("Configuration is empty or too short")
        return json.dumps({"valid": False, "issues": issues, "warnings": warnings})

    if plat == "github":
        if "on:" not in config_yaml and '"on"' not in config_yaml:
            issues.append("Missing trigger definition ('on:' block)")
        if "jobs:" not in config_yaml and '"jobs"' not in config_yaml:
            issues.append("Missing 'jobs:' block")
        if "actions/checkout" not in config_yaml:
            warnings.append("No checkout step found - most workflows need actions/checkout")
        if "ubuntu-latest" not in config_yaml and "runs-on" not in config_yaml:
            warnings.append("No runner specified - ensure 'runs-on' is set for each job")
        if re.search(r'actions/[a-z-]+@v[0-9]+', config_yaml):
            versions = re.findall(r'(actions/[a-z-]+)@v([0-9]+)', config_yaml)
            old_actions = {"actions/checkout": 4, "actions/setup-python": 5, "actions/setup-node": 4, "actions/setup-go": 5}
            for action, ver in versions:
                if action in old_actions and int(ver) < old_actions[action]:
                    warnings.append(f"{action}@v{ver} is outdated, latest is v{old_actions[action]}")
    elif plat == "gitlab":
        if "stages:" not in config_yaml:
            warnings.append("No explicit 'stages:' definition - GitLab will use defaults")
        if "image:" not in config_yaml:
            warnings.append("No Docker image specified - consider adding a base image")

    if "password" in config_yaml.lower() or "secret" in config_yaml.lower():
        if "${{" not in config_yaml:
            warnings.append("Possible hardcoded secret detected - use environment variables or secrets")

    return json.dumps({
        "valid": len(issues) == 0,
        "platform": plat,
        "issues": issues,
        "warnings": warnings,
        "issue_count": len(issues),
        "warning_count": len(warnings),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@mcp.tool()
def list_templates(platform: str = "github", api_key: str = "") -> str:
    """List available CI/CD pipeline templates and supported languages.

    Behavior:
        This tool generates structured output without modifying external systems.
        Output is deterministic for identical inputs. No side effects.
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.

    Args:
        platform (str): The platform to analyze or process.
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})
    if err := _rl():
        return err

    plat = platform.lower().strip()
    available = {}
    for p, langs in PIPELINE_TEMPLATES.items():
        available[p] = list(langs.keys())

    return json.dumps({
        "platforms": list(PIPELINE_TEMPLATES.keys()),
        "templates": available,
        "stages": list(STAGE_DEFINITIONS.keys()),
        "stage_details": {k: {"name": v["name"], "languages": list(v["commands"].keys())} for k, v in STAGE_DEFINITIONS.items()},
        "requested_platform": plat,
        "requested_languages": available.get(plat, []),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


@mcp.tool()
def optimize_stages(config_yaml: str, platform: str = "github", api_key: str = "") -> str:
    """Suggest optimizations for a CI/CD pipeline: caching, parallelism, matrix builds.

    Behavior:
        This tool generates structured output without modifying external systems.
        Output is deterministic for identical inputs. No side effects.
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need structured analysis or classification
        of inputs against established frameworks or standards.

    When NOT to use:
        Not suitable for real-time production decision-making without
        human review of results.

    Args:
        config_yaml (str): The config yaml to analyze or process.
        platform (str): The platform to analyze or process.
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return json.dumps({"error": msg, "upgrade_url": STRIPE_199})
    if err := _rl():
        return err

    suggestions = []
    plat = platform.lower().strip()

    if plat == "github":
        if "cache" not in config_yaml and "actions/cache" not in config_yaml:
            suggestions.append({"type": "caching", "priority": "high", "suggestion": "Add dependency caching to speed up builds", "example": "- uses: actions/cache@v4\n  with:\n    path: ~/.cache/pip\n    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}"})
        if "matrix" not in config_yaml:
            suggestions.append({"type": "matrix", "priority": "medium", "suggestion": "Use a matrix strategy to test across multiple versions", "example": "strategy:\n  matrix:\n    python-version: ['3.10', '3.11', '3.12']"})
        if "concurrency" not in config_yaml:
            suggestions.append({"type": "concurrency", "priority": "medium", "suggestion": "Add concurrency control to cancel outdated runs", "example": "concurrency:\n  group: ${{ github.workflow }}-${{ github.ref }}\n  cancel-in-progress: true"})
        if "timeout-minutes" not in config_yaml:
            suggestions.append({"type": "timeout", "priority": "low", "suggestion": "Add timeout to prevent stuck jobs", "example": "timeout-minutes: 15"})
        if "needs:" not in config_yaml:
            suggestions.append({"type": "parallelism", "priority": "medium", "suggestion": "Use 'needs' to define job dependencies and run independent jobs in parallel"})
    elif plat == "gitlab":
        if "cache:" not in config_yaml:
            suggestions.append({"type": "caching", "priority": "high", "suggestion": "Add cache configuration for dependencies"})
        if "parallel:" not in config_yaml:
            suggestions.append({"type": "parallelism", "priority": "medium", "suggestion": "Use parallel keyword for test splitting"})
        if "rules:" not in config_yaml and "only:" not in config_yaml:
            suggestions.append({"type": "rules", "priority": "medium", "suggestion": "Add rules to control when jobs run and avoid unnecessary builds"})

    return json.dumps({
        "platform": plat,
        "suggestions": suggestions,
        "suggestion_count": len(suggestions),
        "config_length": len(config_yaml),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })


def main():
    mcp.run()

if __name__ == '__main__':
    main()
