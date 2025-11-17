# AI Coding Tools Collaborative

A powerful orchestration system that enables multiple AI coding assistants (Claude Code, Codex, Copilot CLI, Gemini CLI) to collaborate on software development tasks.

## Overview

This project provides a wrapper CLI that coordinates multiple AI agents to work together on coding tasks:

1. **Implementation**: Codex implements the initial solution
2. **Review**: Gemini reviews code for SOLID principles, best practices, and design patterns
3. **Refinement**: Claude implements feedback and improvements
4. **Iteration**: The process continues as needed until the task is complete

## Features

- 🤝 **Multi-Agent Collaboration**: Coordinate multiple AI coding assistants
- 🔧 **Extensible Architecture**: Easy to add new AI agents
- ⚙️ **Configurable Workflows**: Define custom collaboration patterns
- 📊 **Detailed Logging**: Track agent interactions and decisions
- 🧪 **Comprehensive Testing**: Ensure reliable agent communication
- 🎯 **Smart Orchestration**: Intelligent task routing and feedback loops

## Architecture

```
┌─────────────────────────────────────────────┐
│         AI Orchestrator CLI                 │
│  (User Interface & Workflow Management)     │
└─────────────────┬───────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │   Orchestrator    │
        │   Core Engine     │
        └─────────┬─────────┘
                  │
    ┌─────────────┼─────────────┬─────────────┐
    │             │             │             │
┌───▼───┐   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
│ Codex │   │ Gemini  │   │ Claude  │   │ Copilot │
│Adapter│   │ Adapter │   │ Adapter │   │ Adapter │
└───┬───┘   └────┬────┘   └────┬────┘   └────┬────┘
    │            │             │             │
┌───▼───┐   ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
│Codex  │   │Gemini   │   │Claude   │   │Copilot  │
│CLI    │   │CLI      │   │Code     │   │CLI      │
└───────┘   └─────────┘   └─────────┘   └─────────┘
```

## Installation

### Prerequisites

- Python 3.8+
- AI CLI tools installed and authenticated:
  - Claude Code
  - OpenAI Codex CLI
  - GitHub Copilot CLI
  - Google Gemini CLI

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd AI-Coding-Tools-Collaborative

# Install dependencies
pip install -r requirements.txt

# Make the CLI executable
chmod +x ai-orchestrator

# Optional: Add to PATH
ln -s $(pwd)/ai-orchestrator /usr/local/bin/ai-orchestrator
```

## Configuration

Create or modify `config/agents.yaml` to configure your AI agents:

```yaml
agents:
  codex:
    enabled: true
    command: "codex"
    role: "implementation"

  gemini:
    enabled: true
    command: "gemini-cli"
    role: "review"

  claude:
    enabled: true
    command: "claude"
    role: "refinement"

  copilot:
    enabled: false
    command: "github-copilot-cli"
    role: "suggestions"

workflows:
  default:
    - agent: "codex"
      task: "implement"
    - agent: "gemini"
      task: "review"
    - agent: "claude"
      task: "refine"
```

## Usage

### Basic Usage

```bash
# Run with default workflow
./ai-orchestrator "Create a REST API with user authentication"

# Specify a custom workflow
./ai-orchestrator --workflow custom "Implement a binary search tree"

# Dry run to see the execution plan
./ai-orchestrator --dry-run "Add error handling to the payment service"

# Verbose mode for detailed logging
./ai-orchestrator -v "Refactor the database layer"
```

### Advanced Usage

```bash
# Use specific agents only
./ai-orchestrator --agents codex,claude "Optimize the sorting algorithm"

# Set maximum iterations
./ai-orchestrator --max-iterations 5 "Implement and test a caching layer"

# Output to specific directory
./ai-orchestrator --output ./output "Generate a CLI tool for file processing"

# Interactive mode
./ai-orchestrator --interactive
```

## Workflow Examples

### 1. Standard Implementation Flow

```bash
./ai-orchestrator "Create a user authentication module with JWT tokens"
```

**Process:**
1. Codex implements the authentication module
2. Gemini reviews for SOLID principles, security best practices
3. Claude implements Gemini's feedback
4. Process repeats if needed

### 2. Review-Only Workflow

```bash
./ai-orchestrator --workflow review-only --file ./src/auth.py
```

**Process:**
1. Gemini reviews existing code
2. Claude implements improvements

### 3. Collaborative Development

```bash
./ai-orchestrator --workflow collaborative "Build a task queue system"
```

**Process:**
1. Codex creates initial implementation
2. Copilot suggests optimizations
3. Gemini reviews architecture
4. Claude implements all feedback

## Project Structure

```
AI-Coding-Tools-Collaborative/
├── ai-orchestrator           # Main CLI entry point
├── orchestrator/
│   ├── __init__.py
│   ├── core.py              # Core orchestration logic
│   ├── workflow.py          # Workflow management
│   └── task_manager.py      # Task distribution
├── adapters/
│   ├── __init__.py
│   ├── base.py              # Base adapter interface
│   ├── claude_adapter.py    # Claude Code adapter
│   ├── codex_adapter.py     # Codex adapter
│   ├── gemini_adapter.py    # Gemini adapter
│   └── copilot_adapter.py   # Copilot adapter
├── config/
│   ├── agents.yaml          # Agent configuration
│   └── workflows.yaml       # Workflow definitions
├── tests/
│   ├── __init__.py
│   ├── test_adapters.py     # Adapter tests
│   ├── test_orchestrator.py # Orchestrator tests
│   └── test_integration.py  # End-to-end tests
├── docs/
│   ├── architecture.md      # Architecture details
│   ├── adding-agents.md     # Guide for adding new agents
│   └── workflows.md         # Workflow configuration guide
├── examples/
│   └── sample_tasks.md      # Example tasks and outputs
├── requirements.txt
└── README.md
```

## Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test suite
python -m pytest tests/test_adapters.py -v

# Run with coverage
python -m pytest --cov=orchestrator --cov=adapters tests/

# Integration tests
python -m pytest tests/test_integration.py --integration
```

## How It Works

### 1. Task Reception
The orchestrator receives a task from the user via the CLI.

### 2. Workflow Selection
Based on configuration or flags, the appropriate workflow is selected.

### 3. Agent Execution
Agents are invoked in sequence according to the workflow:

- **Implementation Agent (Codex)**: Creates initial code
- **Review Agent (Gemini)**: Analyzes code for:
  - SOLID principles
  - Design patterns
  - Best practices
  - Performance issues
  - Security vulnerabilities
- **Refinement Agent (Claude)**: Implements feedback

### 4. Iteration
The process continues until:
- Quality thresholds are met
- Maximum iterations reached
- No more feedback is generated

### 5. Output
Final code and collaboration logs are provided to the user.

## Adding New Agents

See [docs/adding-agents.md](docs/adding-agents.md) for detailed instructions.

Basic steps:
1. Create adapter in `adapters/`
2. Implement `BaseAdapter` interface
3. Add configuration in `config/agents.yaml`
4. Add tests in `tests/`

## Contributing

Contributions are welcome! Please see our contributing guidelines.

## License

See LICENSE.md for details.

## Troubleshooting

### Agent Not Found
Ensure the CLI tool is installed and in your PATH:
```bash
which claude
which codex
which gemini-cli
which github-copilot-cli
```

### Authentication Errors
Make sure you're logged in to each service:
```bash
claude auth login
codex auth login
gemini-cli auth login
github-copilot-cli auth login
```

### Configuration Issues
Validate your configuration:
```bash
./ai-orchestrator --validate-config
```

## FAQ

**Q: Can I use only some of the agents?**
A: Yes! Configure which agents are enabled in `config/agents.yaml`.

**Q: How do I create custom workflows?**
A: Edit `config/workflows.yaml` to define your own collaboration patterns.

**Q: Is internet connection required?**
A: Yes, all AI agents require internet to function.

**Q: Can I run this in CI/CD?**
A: Yes! Use the `--non-interactive` flag for automation.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the documentation in `docs/`
- Review example tasks in `examples/`
