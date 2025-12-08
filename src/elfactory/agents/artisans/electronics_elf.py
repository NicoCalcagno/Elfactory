"""Electronics Elf - Assembles electronic circuits and components."""

from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient
from elfactory.config import settings
from elfactory.tools import (
    read_project_state,
    write_component,

    log_manufacturing_action,
)


ELECTRONICS_SYSTEM_PROMPT = """You are the Electronics Elf at Santa's Workshop.

ROLE:
You assemble electronic circuits.

IMPORTANT - BE CONCISE:
- ALL responses MUST be 1-2 sentences maximum
- Register component with minimal details
- NO lengthy specs, test procedures, or explanations
- Format: "Assembled [circuit]. Tested OK. Done."

WORKFLOW:
1. Read project state
2. Register component with write_component()
3. Log action briefly
4. Report critical issues only

SAFETY:
- Low voltage only (max 12V)
- Insulate all connections
- Test before delivery
"""


def create_electronics_elf() -> Agent:
    """Create the Electronics Elf agent."""
    client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )

    agent = Agent(
        name="electronics_elf",
        client=client,
        system_prompt=ELECTRONICS_SYSTEM_PROMPT,
        tools=[
            read_project_state,
            write_component,
        
            log_manufacturing_action,
        ],
    )

    return agent
