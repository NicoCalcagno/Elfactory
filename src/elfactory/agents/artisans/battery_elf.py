"""Battery Elf - Installs power systems and battery management."""

from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient
from elfactory.config import settings
from elfactory.tools import (
    read_project_state,
    write_component,

    log_manufacturing_action,
)


BATTERY_SYSTEM_PROMPT = """You are the Battery Specialist Elf at Santa's Workshop.

ROLE:
You install power systems.

IMPORTANT - BE CONCISE:
- ALL responses MUST be 1-2 sentences maximum
- Register component with minimal details
- NO lengthy specs or safety explanations
- Format: "Installed [battery type]. Secured. Done."

WORKFLOW:
1. Read project state
2. Register component
3. Log action briefly

SAFETY:
- Screw-secured battery compartment for child safety
- Proper voltage, fuse all circuits
"""


def create_battery_elf() -> Agent:
    """Create the Battery Specialist Elf agent."""
    client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )

    agent = Agent(
        name="battery_elf",
        client=client,
        system_prompt=BATTERY_SYSTEM_PROMPT,
        tools=[
            read_project_state,
            write_component,
        
            log_manufacturing_action,
        ],
    )

    return agent
