# Kanban CLI

A powerful command-line interface for interacting with the [kan.bn](https://kan.bn) API.

## Features

- 🔐 **Authentication management** - Securely store and manage API credentials
- 📋 **Workspace operations** - Create, list, update, and delete workspaces
- 📊 **Board management** - Manage boards within workspaces
- 📝 **List operations** - Create and organize lists
- 🎯 **Card management** - Full CRUD operations for cards, including comments and labels
- 🏷️ **Label management** - Create and apply labels to cards
- 🎨 **Rich output** - Beautiful terminal output with colors and tables
- 🔍 **Search functionality** - Search across boards and cards

## Quick Start

### Quick Try (No Installation Required) ⚡

Try the CLI instantly with uvx:

```bash
uvx kanbn-cli auth login
uvx kanbn-cli workspace list
```

> **Note**: First run downloads dependencies (~1-3 seconds), subsequent runs are instant.

### Install Globally (Recommended)

**Using uv** (Fast - recommended):

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install kanbn-cli
uv tool install kanbn-cli

# Use it anywhere
kanbn workspace list
```

**Using pip** (Traditional):

```bash
pip install kanbn-cli
kanbn workspace list
```

### Development Setup

**Using uv** (recommended):

```bash
# Clone the repository
cd kanbn-cli

# Sync dependencies (creates .venv automatically)
uv sync

# Run CLI in development
uv run kanbn --help

# Run with auto-reload during development
uv run kanbn workspace list
```

**Using pip**:

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode
pip install -e .

# Run CLI
kanbn --help
```

### 1. Authenticate

```bash
# Interactive login
kanbn auth login

# Or provide token directly
kanbn auth login --token YOUR_API_TOKEN

# Check authentication status
kanbn auth status
```

### 2. Manage Workspaces

```bash
# List all workspaces
kanbn workspace list

# Create a new workspace
kanbn workspace create "My Workspace" --slug my-workspace

# Get workspace details
kanbn workspace get WORKSPACE_ID

# Search within a workspace
kanbn workspace search WORKSPACE_ID "search query"
```

### 3. Manage Boards

```bash
# List boards in a workspace
kanbn board list WORKSPACE_ID

# Create a new board
kanbn board create WORKSPACE_ID "My Board" --slug my-board

# Get board details
kanbn board get BOARD_ID
```

### 4. Manage Lists

```bash
# Create a list
kanbn list create BOARD_ID "To Do"

# Update list
kanbn list update LIST_ID --name "In Progress"

# Delete list
kanbn list delete LIST_ID --yes
```

### 5. Manage Cards

```bash
# Create a card
kanbn card create LIST_ID "My Task" --description "Task description"

# Get card details
kanbn card get CARD_ID

# Update card
kanbn card update CARD_ID --title "Updated Title"

# Move card to another list
kanbn card update CARD_ID --list NEW_LIST_ID

# Add comment
kanbn card comment CARD_ID "This is a comment"

# Delete card
kanbn card delete CARD_ID
```

### 6. Manage Labels

```bash
# Create a label
kanbn label create BOARD_ID "Bug" "#ff0000"

# Add label to card
kanbn card label CARD_ID LABEL_ID

# Remove label from card
kanbn card label CARD_ID LABEL_ID --remove
```

## Configuration

The CLI stores configuration in `~/.kanbnrc` as JSON. You can also use environment variables:

```bash
export KANBN_API_URL="https://api.your-instance.com"
export KANBN_API_TOKEN="your_token_here"
export KANBN_DEFAULT_WORKSPACE="workspace_id"
```

Or create a `.env` file in your project:

```env
KANBN_API_URL=https://api.your-instance.com
KANBN_API_TOKEN=your_token_here
```

## Command Reference

### Global Options

- `--version, -v` - Show version and exit
- `--help` - Show help message

### Commands

- `auth` - Authentication management
  - `login` - Store API credentials
  - `logout` - Clear stored credentials
  - `status` - Show authentication status

- `workspace` - Workspace management
  - `list` - List all workspaces
  - `create` - Create a new workspace
  - `get` - Get workspace details
  - `update` - Update a workspace
  - `delete` - Delete a workspace
  - `search` - Search boards and cards

- `board` - Board management
  - `list` - List boards in a workspace
  - `create` - Create a new board
  - `get` - Get board details
  - `update` - Update a board
  - `delete` - Delete a board

- `list` - List management
  - `create` - Create a new list
  - `update` - Update a list
  - `delete` - Delete a list

- `card` - Card management
  - `create` - Create a new card
  - `get` - Get card details
  - `update` - Update a card
  - `delete` - Delete a card
  - `comment` - Add a comment
  - `label` - Add or remove labels

- `label` - Label management
  - `create` - Create a new label
  - `get` - Get label details
  - `update` - Update a label
  - `delete` - Delete a label

## Development

### Setup Development Environment

**Using uv** (recommended):

```bash
# Clone repository
git clone git@github.com:mikkelkrogsholm/kanbn_cli.git
cd kanbn_cli

# Install dependencies
uv sync

# Run tests (when implemented)
uv run pytest

# Format code
uv run black .

# Lint code
uv run ruff check .

# Run CLI in development
uv run kanbn workspace list
```

**Using pip**:

```bash
# Install dependencies including dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .

# Lint code
ruff check .
```

### Adding Dependencies

**With uv**:
```bash
# Add runtime dependency
uv add httpx

# Add dev dependency  
uv add --dev pytest
```

**With pip**:
```bash
# Edit pyproject.toml manually, then:
pip install -e ".[dev]"
```

### Project Structure

```
kanbn-cli/
├── kanbn_cli/
│   ├── __init__.py
│   ├── main.py           # Main CLI entry point
│   ├── config.py         # Configuration management
│   ├── api/
│   │   ├── client.py     # HTTP client
│   │   └── models.py     # Pydantic models
│   ├── commands/         # Command modules
│   │   ├── auth.py
│   │   ├── workspace.py
│   │   ├── board.py
│   │   ├── list.py
│   │   ├── card.py
│   │   └── label.py
│   └── utils/
│       ├── display.py    # Display utilities
│       └── errors.py     # Custom errors
├── pyproject.toml
└── README.md
```

## License

[Add your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- Open an issue on GitHub
- Check the [kan.bn documentation](https://docs.kan.bn)
