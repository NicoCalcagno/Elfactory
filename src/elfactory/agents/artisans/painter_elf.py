"""Painter Elf - Applies paint finishes to components."""

from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient
from elfactory.config import settings
from elfactory.tools import (
    read_project_state,
    write_component,

    log_manufacturing_action,
)


PAINTER_SYSTEM_PROMPT = """You are the Painter Elf at Santa's Workshop.

ROLE:
You apply paint finishes.

IMPORTANT - BE CONCISE:
- ALL responses MUST be 1-2 sentences maximum
- Register component with minimal details
- NO paint procedures or drying times
- Format: "Painted [item] [color]. Dried. Done."

WORKFLOW:
1. Read project state
2. Register component
3. Log action briefly

SAFETY:
- Non-toxic paints only
- Multiple thin coats
"""


def create_painter_elf() -> Agent:
    """Create the Painter Elf agent."""
    client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )

    agent = Agent(
        name="painter_elf",
        client=client,
        system_prompt=PAINTER_SYSTEM_PROMPT,
        tools=[
            read_project_state,
            write_component,
        
            log_manufacturing_action,
        ],
    )

    return agent
