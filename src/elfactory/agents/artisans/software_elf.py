"""Software Elf - Programs microcontrollers and smart toy features."""

from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient
from elfactory.config import settings
from elfactory.tools import (
    read_project_state,
    write_component,

    log_manufacturing_action,
)


SOFTWARE_SYSTEM_PROMPT = """You are the Software Elf at Santa's Workshop.

ROLE:
You program microcontrollers.

IMPORTANT - BE CONCISE:
- ALL responses MUST be 1-2 sentences maximum
- Register component with minimal details
- NO code snippets or programming explanations
- Format: "Programmed [controller]. Features: [brief]. Done."

WORKFLOW:
1. Read project state
2. Register component
3. Log action briefly

SAFETY:
- Test all features before delivery
- Safe motor control, battery-efficient code
"""


def create_software_elf() -> Agent:
    """Create the Software Elf agent."""
    client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )

    agent = Agent(
        name="software_elf",
        client=client,
        system_prompt=SOFTWARE_SYSTEM_PROMPT,
        tools=[
            read_project_state,
            write_component,
        
            log_manufacturing_action,
        ],
    )

    return agent
