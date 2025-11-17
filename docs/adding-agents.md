# Adding New AI Agents

This guide explains how to add support for new AI coding assistant CLI tools to the orchestrator.

## Overview

Adding a new agent involves:
1. Creating an adapter class
2. Registering the CLI communication pattern
3. Updating configuration
4. Writing tests

## Step-by-Step Guide

### Step 1: Create the Adapter Class

Create a new file in `adapters/` directory (e.g., `adapters/my_agent_adapter.py`):

```python
"""
Adapter for My Custom AI Agent CLI.
"""

from typing import Dict, List, Any
from .base import BaseAdapter, AgentResponse, AgentCapability


class MyAgentAdapter(BaseAdapter):
    """Adapter for interacting with My AI Agent CLI."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.command = config.get('command', 'my-agent-cli')

    def get_capabilities(self) -> List[AgentCapability]:
        """Define what this agent is good at."""
        return [
            AgentCapability.IMPLEMENTATION,
            AgentCapability.CODE_REVIEW,
            # Add other capabilities as appropriate
        ]

    def execute_task(self, task: str, context: Dict[str, Any]) -> AgentResponse:
        """
        Execute a task using this agent.

        Args:
            task: The task description
            context: Additional context (files, feedback, etc.)

        Returns:
            AgentResponse with results
        """
        # Build a prompt for your agent
        prompt = self._build_prompt(task, context)

        # Get working directory from context
        working_dir = context.get('working_dir', './workspace')

        # Use the enhanced communication method
        # Set use_workspace=True if your agent modifies files
        response = self._run_command_with_prompt(
            prompt=prompt,
            working_dir=working_dir,
            use_workspace=True  # or False if agent only provides suggestions
        )

        # Parse agent-specific output
        if response.success:
            suggestions = self._extract_suggestions(response.output)
            response.suggestions = suggestions

        return response

    def _build_prompt(self, task: str, context: Dict[str, Any]) -> str:
        """Build a prompt tailored to your agent."""
        parts = [task]

        # Add context as needed
        if context.get('feedback'):
            parts.append(f"\n\nFeedback to address:\n{context['feedback']}")

        # Add any agent-specific instructions
        parts.append("\n\nPlease provide detailed, production-ready code.")

        return '\n'.join(parts)

    def _extract_suggestions(self, output: str) -> List[str]:
        """Parse suggestions from agent output."""
        suggestions = []

        # Implement parsing logic specific to your agent's output format
        for line in output.split('\n'):
            if line.strip().startswith('-') or line.strip().startswith('•'):
                suggestions.append(line.strip()[1:].strip())

        return suggestions
```

### Step 2: Register the CLI Communication Pattern

Add your agent's CLI communication pattern to `adapters/cli_communicator.py`:

```python
# In AgentCLIRegistry.PATTERNS dictionary:
PATTERNS = {
    # ... existing patterns ...

    'my-agent': {
        'command': 'my-agent-cli',
        'method': 'stdin',  # or 'arg', 'file', 'heredoc'
        'prompt_flag': '--prompt',  # if using 'arg' method
        'supports_workspace': True,  # Does it work with files?
        'output_format': 'text'  # or 'json'
    },
}
```

**Communication Methods:**

- `stdin`: Agent reads from standard input
  ```bash
  echo "prompt" | my-agent-cli
  ```

- `arg`: Agent accepts prompt as argument
  ```bash
  my-agent-cli --prompt "prompt text"
  ```

- `file`: Agent reads from file
  ```bash
  my-agent-cli --input input.txt --output output.txt
  ```

- `heredoc`: Using bash heredoc
  ```bash
  my-agent-cli << EOF
  prompt text
  EOF
  ```

### Step 3: Update Adapter Registry

Add your adapter to `adapters/__init__.py`:

```python
from .my_agent_adapter import MyAgentAdapter

__all__ = [
    # ... existing exports ...
    'MyAgentAdapter',
]
```

### Step 4: Register in Orchestrator

Update `orchestrator/core.py` to include your adapter:

```python
def _initialize_adapters(self):
    """Initialize all configured adapters."""
    adapter_classes = {
        'codex': CodexAdapter,
        'gemini': GeminiAdapter,
        'claude': ClaudeAdapter,
        'copilot': CopilotAdapter,
        'my-agent': MyAgentAdapter,  # Add your adapter
    }
    # ... rest of method ...
```

### Step 5: Add Configuration

Add your agent to `config/agents.yaml`:

```yaml
agents:
  # ... existing agents ...

  my-agent:
    enabled: true
    command: "my-agent-cli"
    role: "implementation"  # or "review", "refinement", etc.
    timeout: 300  # seconds
    description: "Description of what this agent does"

# Add to workflows as needed
workflows:
  my-custom-workflow:
    - agent: "codex"
      task: "implement"

    - agent: "my-agent"
      task: "review"

    - agent: "claude"
      task: "refine"
```

### Step 6: Write Tests

Create tests in `tests/test_adapters.py`:

```python
class TestMyAgentAdapter:
    """Test My Agent adapter."""

    def test_capabilities(self):
        """Test agent capabilities."""
        config = {'name': 'my-agent', 'command': 'my-agent-cli', 'enabled': True}
        adapter = MyAgentAdapter(config)

        capabilities = adapter.get_capabilities()

        assert AgentCapability.IMPLEMENTATION in capabilities

    def test_build_prompt(self):
        """Test prompt building."""
        config = {'name': 'my-agent', 'command': 'my-agent-cli', 'enabled': True}
        adapter = MyAgentAdapter(config)

        task = "Create a function"
        context = {'feedback': 'Add error handling'}

        prompt = adapter._build_prompt(task, context)

        assert 'Create a function' in prompt
        assert 'Add error handling' in prompt

    def test_extract_suggestions(self):
        """Test suggestion extraction."""
        config = {'name': 'my-agent', 'command': 'my-agent-cli', 'enabled': True}
        adapter = MyAgentAdapter(config)

        output = """
        Here are suggestions:
        - Improve error handling
        - Add type hints
        - Optimize performance
        """

        suggestions = adapter._extract_suggestions(output)

        assert len(suggestions) == 3
        assert 'Improve error handling' in suggestions
```

## Advanced Features

### Custom Context Handling

If your agent needs special context:

```python
def execute_task(self, task: str, context: Dict[str, Any]) -> AgentResponse:
    # Extract agent-specific context
    language = context.get('language', 'python')
    framework = context.get('framework')

    # Build custom prompt
    prompt = f"Task: {task}\nLanguage: {language}"
    if framework:
        prompt += f"\nFramework: {framework}"

    # ... execute task
```

### Structured Output Parsing

If your agent outputs JSON or structured data:

```python
import json

def _parse_json_response(self, output: str) -> AgentResponse:
    """Parse JSON response from agent."""
    try:
        data = json.loads(output)

        return AgentResponse(
            success=True,
            output=data.get('code', ''),
            files_modified=data.get('files', []),
            suggestions=data.get('suggestions', []),
            metadata=data.get('metadata', {})
        )
    except json.JSONDecodeError as e:
        return AgentResponse(
            success=False,
            output="",
            error=f"Failed to parse JSON: {e}"
        )
```

### Multiple Commands

If your agent requires multiple commands:

```python
def execute_task(self, task: str, context: Dict[str, Any]) -> AgentResponse:
    # First command: analyze
    analyze_response = self._run_command(['my-agent', 'analyze', task])

    if not analyze_response.success:
        return analyze_response

    # Second command: implement
    implement_response = self._run_command([
        'my-agent', 'implement',
        '--analysis', analyze_response.output
    ])

    return implement_response
```

## Testing Your Adapter

### 1. Unit Tests

```bash
pytest tests/test_adapters.py::TestMyAgentAdapter -v
```

### 2. Integration Test

```bash
# Add integration test
pytest tests/test_integration.py -v -k my_agent
```

### 3. Manual Test

```bash
# Validate configuration
./ai-orchestrator validate

# Check agent availability
./ai-orchestrator agents

# Test with a simple task
./ai-orchestrator run "Create a hello world function" --workflow quick
```

## Common Issues

### Agent Not Found

**Problem:** `Agent my-agent not available`

**Solutions:**
1. Ensure CLI tool is installed: `which my-agent-cli`
2. Check configuration enabled: `enabled: true`
3. Verify command name matches

### Communication Failures

**Problem:** Agent doesn't receive prompt or returns empty output

**Solutions:**
1. Try different communication method ('stdin' vs 'arg')
2. Check if agent requires specific flags
3. Test command manually: `echo "test" | my-agent-cli`
4. Review agent documentation for correct invocation

### Timeout Errors

**Problem:** Agent execution times out

**Solutions:**
1. Increase timeout in config: `timeout: 600`
2. Check if agent is hanging on input
3. Verify agent doesn't require interactive confirmation

## Best Practices

1. **Error Handling**: Always handle potential errors in parsing
2. **Logging**: Use `self.logger` for debugging
3. **Documentation**: Document expected input/output formats
4. **Testing**: Write comprehensive tests before deployment
5. **Configuration**: Provide sensible defaults
6. **Capabilities**: Accurately declare agent capabilities

## Example: Adding Aider

Here's a complete example for adding Aider (an AI pair programming tool):

```python
# adapters/aider_adapter.py
from typing import Dict, List, Any
from .base import BaseAdapter, AgentResponse, AgentCapability


class AiderAdapter(BaseAdapter):
    """Adapter for Aider AI pair programming tool."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.command = config.get('command', 'aider')

    def get_capabilities(self) -> List[AgentCapability]:
        return [
            AgentCapability.IMPLEMENTATION,
            AgentCapability.REFACTORING,
            AgentCapability.DEBUGGING,
        ]

    def execute_task(self, task: str, context: Dict[str, Any]) -> AgentResponse:
        prompt = f"/ask {task}"
        working_dir = context.get('working_dir', './workspace')

        # Aider works with files, so use workspace mode
        response = self._run_command_with_prompt(
            prompt=prompt,
            working_dir=working_dir,
            use_workspace=True
        )

        return response
```

Then update configuration:

```yaml
agents:
  aider:
    enabled: true
    command: "aider"
    role: "implementation"
    timeout: 300
```

## Support

If you encounter issues adding a new agent:
1. Check agent's CLI documentation
2. Test the CLI tool independently
3. Review existing adapters for examples
4. Check logs in `ai-orchestrator.log`
