"""Sound Engineer Elf - Adds sound effects and audio to toys."""

from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient
from elfactory.config import settings
from elfactory.tools import (
    read_project_state,
    write_component,

    log_manufacturing_action,
)


SOUND_ENGINEER_SYSTEM_PROMPT = """You are the Sound Engineer Elf at Santa's Workshop.

ROLE:
You add sound effects.

IMPORTANT - BE CONCISE:
- ALL responses MUST be 1-2 sentences maximum
- Register component with minimal details
- NO audio setup procedures
- NO issues (all modules available)
- Format: "Added [sound module]. Tested. Done."

WORKFLOW:
1. Read project state
2. Register component
3. Log action briefly

SAFETY:
- Safe volume levels for children
"""


def create_sound_engineer_elf() -> Agent:
    """Create the Sound Engineer Elf agent."""
    client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )

    agent = Agent(
        name="sound_engineer_elf",
        client=client,
        system_prompt=SOUND_ENGINEER_SYSTEM_PROMPT,
        tools=[
            read_project_state,
            write_component,
        
            log_manufacturing_action,
        ],
    )

    return agent
