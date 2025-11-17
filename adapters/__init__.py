"""
AI Agent Adapters

This package contains adapters for different AI coding assistant CLI tools.
"""

from .base import BaseAdapter, AgentResponse, AgentCapability
from .claude_adapter import ClaudeAdapter
from .codex_adapter import CodexAdapter
from .gemini_adapter import GeminiAdapter
from .copilot_adapter import CopilotAdapter

__all__ = [
    'BaseAdapter',
    'AgentResponse',
    'AgentCapability',
    'ClaudeAdapter',
    'CodexAdapter',
    'GeminiAdapter',
    'CopilotAdapter',
]
