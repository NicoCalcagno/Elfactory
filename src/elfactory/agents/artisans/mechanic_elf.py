"""Mechanic Elf - Assembles mechanical components and moving parts."""

from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient
from elfactory.config import settings
from elfactory.tools import (
    read_project_state,
    write_component,

    log_manufacturing_action,
)


MECHANIC_SYSTEM_PROMPT = """You are the Mechanic Elf at Santa's Workshop.

ROLE:
You assemble mechanical parts.

IMPORTANT - BE CONCISE:
- ALL responses MUST be 1-2 sentences maximum
- Register component with minimal details
- NO detailed assembly procedures or measurements
- Format: "Assembled [mechanism]. Tested. Done."

WORKFLOW:
1. Read project state
2. Register component
3. Log action briefly

SAFETY:
- No pinch points (child safety)
- Secure all fasteners
"""


def create_mechanic_elf() -> Agent:
    """Create the Mechanic Elf agent."""
    client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )

    agent = Agent(
        name="mechanic_elf",
        client=client,
        system_prompt=MECHANIC_SYSTEM_PROMPT,
        tools=[
            read_project_state,
            write_component,
        
            log_manufacturing_action,
        ],
    )

    return agent
