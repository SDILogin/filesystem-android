# MCP Server Configuration
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)

## Overview
This project provides a Claude MCP server that enables secure access to Android project files. It allows AI assistants to browse and read source code from Android projects by checking for essential gradle configuration files that validate authentic Android projects.

Key features:
- **Project Validation**: Ensures directories are valid Android projects by checking for gradle files
- **File Browsing**: Lists all Kotlin, KTS, TOML files and AndroidManifest.xml grouped by directory
- **File Reading**: Provides secure access to read individual or multiple files with appropriate filtering
- **Security**: Prevents access to sensitive directories like .gradle, .git and build folders

This tool is ideal for developers who want to leverage Claude to help them understand, analyze, and work with Android codebases.

## Server Setup
Add this configuration to your Claude client's MCP settings:
```json
{
  "mcpServers": {
    "Android source code": {
      "command": "/path/to/uv", 
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "./filesystem_android/main.py"
      ]
    }
  }
}
```
Note: Replace `/path/to/uv` with your actual UV installation path

## Installation
```bash
# Install UV if missing
curl -LsSf https://astral.sh/uv/install.sh | sh

# Initialize project
uv venv
uv pip install -r uv.lock
```

## License
MIT License - See [LICENSE](LICENSE) for details