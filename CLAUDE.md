# Development Guidelines

## Build Commands
- Setup: `uv venv && uv pip install -r uv.lock`
- Run: `uv run --with mcp[cli] mcp run ./main.py`
- Lint: `uv run ruff check .`
- Format: `uv run black .`
- Type check: `uv run mypy .`

## Code Style
- **Formatting**: Follow PEP 8 guidelines with 100 char line length
- **Imports**: Group standard lib, third-party, and local imports
- **Types**: Use type hints for all function parameters and return values
- **Error Handling**: Use specific exceptions with descriptive messages
- **Naming**: Use snake_case for variables/functions, PascalCase for classes
- **Docstrings**: Include for all functions with param descriptions
- **Security**: Validate all inputs, especially file paths
- **MCP Tools**: Format each tool with async definitions and complete docstrings

## Structure
Keep all MCP tools in main.py and maintain security checks for file access.
