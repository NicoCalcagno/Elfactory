"""Woodworker Elf - Crafts wooden components and toys."""

from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient
from elfactory.config import settings
from elfactory.tools import (
    read_project_state,
    write_component,

    log_manufacturing_action,
)


WOODWORKER_SYSTEM_PROMPT = """You are the Woodworker Elf at Santa's Workshop.

ROLE:
You craft wooden components.

IMPORTANT - BE CONCISE:
- ALL responses MUST be 1-2 sentences maximum
- Register component with minimal details
- NO cutting procedures or dimensions lists
- Format: "Cut [item] from [wood]. Sanded. Done."

WORKFLOW:
1. Read project state
2. Register component
3. Log action briefly

SAFETY:
- Sand smooth - no splinters
- Non-toxic finishes only
"""


def create_woodworker_elf() -> Agent:
    """Create the Woodworker Elf agent."""
    client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )

    agent = Agent(
        name="woodworker_elf",
        client=client,
        system_prompt=WOODWORKER_SYSTEM_PROMPT,
        tools=[
            read_project_state,
            write_component,
        
            log_manufacturing_action,
        ],
    )

    return agent
