# Installation Guide

## Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- pip package manager
- At least one AI CLI tool installed (Claude Code, Codex, Gemini CLI, or Copilot CLI)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install click pyyaml colorama rich pydantic
```

### 3. Verify Installation

```bash
# Make the CLI executable
chmod +x ai-orchestrator

# Verify it works
./ai-orchestrator --help

# Check version
./ai-orchestrator version

# Validate configuration
./ai-orchestrator validate

# Check available agents
./ai-orchestrator agents
```

### 4. Install AI CLI Tools

You need at least one of the following AI CLI tools installed and authenticated:

#### Claude Code
```bash
# Follow Claude Code installation instructions
# Authenticate with your account
claude auth login
```

#### OpenAI Codex
```bash
# Install Codex CLI
pip install openai-codex

# Set API key
export OPENAI_API_KEY="your-api-key"
```

#### Google Gemini CLI
```bash
# Install Gemini CLI
pip install google-generativeai

# Authenticate
gemini-cli auth login
```

#### GitHub Copilot CLI
```bash
# Install GitHub CLI with Copilot extension
gh extension install github/gh-copilot

# Authenticate
gh auth login
```

### 5. Run Your First Task

```bash
./ai-orchestrator run "Create a function to validate email addresses" --workflow quick
```

## Development Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd AI-Coding-Tools-Collaborative
```

### 2. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Production dependencies
pip install -r requirements.txt

# Development dependencies
pip install pytest pytest-cov
```

### 4. Run Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_adapters.py -v

# With coverage
pytest --cov=orchestrator --cov=adapters tests/
```

### 5. Install in Development Mode

```bash
pip install -e .
```

This allows you to edit the code and see changes immediately without reinstalling.

## Configuration

### Default Configuration

The default configuration is located at `config/agents.yaml`.

### Custom Configuration

Create your own configuration file:

```bash
cp config/agents.yaml config/my-config.yaml
```

Edit `config/my-config.yaml` to customize agents and workflows.

Use it with:

```bash
./ai-orchestrator run "task" --config config/my-config.yaml
```

### Environment Variables

You can set these environment variables:

- `AI_ORCHESTRATOR_CONFIG`: Path to default config file
- `AI_ORCHESTRATOR_LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `AI_ORCHESTRATOR_OUTPUT_DIR`: Default output directory

## Adding to PATH

### Linux/macOS

```bash
# Create symlink
sudo ln -s $(pwd)/ai-orchestrator /usr/local/bin/ai-orchestrator

# Or add to PATH in ~/.bashrc or ~/.zshrc
export PATH=$PATH:/path/to/AI-Coding-Tools-Collaborative
```

### Windows

```powershell
# Add to PATH using PowerShell
$env:Path += ";C:\path\to\AI-Coding-Tools-Collaborative"

# Make permanent
[Environment]::SetEnvironmentVariable("Path", $env:Path, [System.EnvironmentVariableTarget]::User)
```

## Troubleshooting

### Command Not Found

If you get "command not found" errors:

1. Ensure the script is executable:
   ```bash
   chmod +x ai-orchestrator
   ```

2. Use Python explicitly:
   ```bash
   python3 ai-orchestrator --help
   ```

### Import Errors

If you get import errors:

1. Ensure you're in the project directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Agent Not Available

If agents show as "Not available":

1. Install the CLI tool
2. Authenticate with the service
3. Verify with `which <command>` (e.g., `which claude`)
4. Check configuration in `config/agents.yaml`

### Permission Errors

If you get permission errors:

```bash
# Fix file permissions
chmod +x ai-orchestrator

# Or run with Python
python3 ./ai-orchestrator --help
```

## Docker Installation (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ai-orchestrator

ENTRYPOINT ["./ai-orchestrator"]
```

Build and run:

```bash
docker build -t ai-orchestrator .
docker run -it ai-orchestrator --help
```

## Verification

Run the verification checklist:

```bash
# 1. Check Python version
python3 --version  # Should be 3.8+

# 2. Install dependencies
pip install -r requirements.txt

# 3. Validate configuration
./ai-orchestrator validate

# 4. Check agents
./ai-orchestrator agents

# 5. List workflows
./ai-orchestrator workflows

# 6. Run tests
pytest tests/ -v

# 7. Try a simple task (if agents available)
./ai-orchestrator run "Create a hello world function" --dry-run
```

## Next Steps

After installation:

1. Read the [README.md](README.md) for usage examples
2. Check [docs/architecture.md](docs/architecture.md) to understand the system
3. See [examples/sample_tasks.md](examples/sample_tasks.md) for task examples
4. Read [docs/adding-agents.md](docs/adding-agents.md) to add custom agents

## Support

For issues:
1. Check logs in `ai-orchestrator.log`
2. Run with `--verbose` flag for detailed output
3. Validate configuration with `./ai-orchestrator validate`
4. Check GitHub issues for known problems
