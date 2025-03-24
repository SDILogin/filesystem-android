# MCP Server Configuration
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)

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