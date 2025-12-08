"""Light Designer Elf - Adds lighting effects and illumination."""

from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient
from elfactory.config import settings
from elfactory.tools import (
    read_project_state,
    write_component,

    log_manufacturing_action,
)


LIGHT_DESIGNER_SYSTEM_PROMPT = """You are the Light Designer Elf at Santa's Workshop.

ROLE:
You add lighting effects.

IMPORTANT - BE CONCISE:
- ALL responses MUST be 1-2 sentences maximum
- Register component with minimal details
- NO wiring diagrams or circuit explanations
- NO issues (all LEDs/components available)
- Format: "Added [LED type]. Tested. Done."

WORKFLOW:
1. Read project state
2. Register component
3. Log action briefly

SAFETY:
- Safe brightness, current-limiting resistors
"""


def create_light_designer_elf() -> Agent:
    """Create the Light Designer Elf agent."""
    client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )

    agent = Agent(
        name="light_designer_elf",
        client=client,
        system_prompt=LIGHT_DESIGNER_SYSTEM_PROMPT,
        tools=[
            read_project_state,
            write_component,
        
            log_manufacturing_action,
        ],
    )

    return agent
