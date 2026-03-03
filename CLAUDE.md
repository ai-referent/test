# CLAUDE.md

This file provides guidance for AI assistants working in this repository.

## Repository Overview

This is a minimal Python test repository. It currently contains a single Python script and an MCP server configuration.

## Repository Structure

```
/
├── hello.py        # Simple Python "Hello world" script
├── README.md       # Project README (minimal)
├── .mcp.json       # MCP server configuration
└── CLAUDE.md       # This file
```

## Files

### `hello.py`
A minimal Python script that prints "Hello world". This is the primary (and currently only) Python source file.

### `.mcp.json`
Configures the [data.gouv.fr MCP server](https://mcp.data.gouv.fr/mcp), which provides access to French open data resources via the Model Context Protocol (HTTP transport).

```json
{
  "mcpServers": {
    "datagouv": {
      "type": "http",
      "url": "https://mcp.data.gouv.fr/mcp"
    }
  }
}
```

## Development Conventions

- **Language**: Python
- **No build system** or package manager is currently configured (no `requirements.txt`, `pyproject.toml`, or `setup.py`)
- **No test framework** is currently set up
- Keep changes minimal and focused given the simplicity of the project

## Git Workflow

- The default branch is `master`
- Feature branches follow the pattern `claude/<description>-<session-id>`
- Commit messages are short and descriptive (e.g., "first python file", "Adding mcp json file for data gouv")

## Running the Code

```bash
python hello.py
# Output: Hello world
```

## MCP Integration

The repository includes a `.mcp.json` that connects to the `data.gouv.fr` MCP server. This server provides tools for querying French government open data. When working with Claude Code, this MCP server is available as `datagouv`.
