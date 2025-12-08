"""Agent logging utilities to capture agent interactions in log files."""

import logging
from typing import Any, Optional
from contextlib import contextmanager


class AgentLogger:
    """Logger for agent interactions and delegations."""

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize agent logger.

        Args:
            logger: Logger instance to use. If None, uses 'elfactory.agents' logger.
        """
        self.logger = logger or logging.getLogger("elfactory.agents")

    def log_agent_call(self, agent_name: str, input_task: str, truncate: int = 200):
        """
        Log when an agent is called.

        Args:
            agent_name: Name of the agent being called
            input_task: The task/input given to the agent
            truncate: Maximum length of task to log
        """
        task_preview = input_task[:truncate] + "..." if len(input_task) > truncate else input_task
        self.logger.info(f"[{agent_name}] Called with task: {task_preview}")

    def log_agent_response(self, agent_name: str, response: Any, truncate: int = 500):
        """
        Log agent response.

        Args:
            agent_name: Name of the agent
            response: The agent's response
            truncate: Maximum length of response to log
        """
        response_str = str(response)
        response_preview = response_str[:truncate] + "..." if len(response_str) > truncate else response_str
        self.logger.info(f"[{agent_name}] Response: {response_preview}")

    def log_delegation(self, from_agent: str, to_agent: str, reason: str = ""):
        """
        Log when one agent delegates to another.

        Args:
            from_agent: Agent delegating
            to_agent: Agent being called
            reason: Reason for delegation
        """
        msg = f"[DELEGATION] {from_agent} → {to_agent}"
        if reason:
            msg += f" | Reason: {reason}"
        self.logger.info(msg)

    def log_status_change(self, gift_id: str, old_status: str, new_status: str, agent: str):
        """
        Log status changes.

        Args:
            gift_id: Gift ID
            old_status: Previous status
            new_status: New status
            agent: Agent that changed the status
        """
        self.logger.info(f"[STATUS] {gift_id}: {old_status} → {new_status} (by {agent})")

    def log_component_created(self, component_id: str, component_type: str, created_by: str):
        """
        Log component creation.

        Args:
            component_id: Component ID
            component_type: Type of component
            created_by: Agent that created it
        """
        self.logger.info(f"[COMPONENT] {component_id} ({component_type}) created by {created_by}")

    def log_issue(self, severity: str, description: str, reported_by: str):
        """
        Log an issue.

        Args:
            severity: Issue severity
            description: Issue description
            reported_by: Agent reporting the issue
        """
        self.logger.warning(f"[ISSUE-{severity.upper()}] {reported_by}: {description}")

    def log_error(self, agent_name: str, error: Exception):
        """
        Log an error from an agent.

        Args:
            agent_name: Agent that encountered the error
            error: The exception
        """
        self.logger.error(f"[ERROR] {agent_name}: {type(error).__name__}: {str(error)}")


# Global agent logger instance
_agent_logger: Optional[AgentLogger] = None


def get_agent_logger() -> AgentLogger:
    """Get or create the global agent logger."""
    global _agent_logger
    if _agent_logger is None:
        _agent_logger = AgentLogger()
    return _agent_logger


@contextmanager
def log_agent_execution(agent_name: str, task: str):
    """
    Context manager to log agent execution.

    Usage:
        with log_agent_execution("quality_manager", "Inspect gift"):
            result = agent.run(task)

    Args:
        agent_name: Name of the agent
        task: Task being executed
    """
    logger = get_agent_logger()
    logger.log_agent_call(agent_name, task)
    try:
        yield
    except Exception as e:
        logger.log_error(agent_name, e)
        raise
