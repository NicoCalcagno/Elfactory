"""Librarian Elf - Manages technical specifications and materials knowledge."""

from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient
from elfactory.config import settings
from elfactory.tools import (
    read_project_state,

    log_manufacturing_action,
)


LIBRARIAN_SYSTEM_PROMPT = """You are the Librarian Elf at Santa's Workshop.

ROLE:
You provide technical specs and knowledge to other elves.

IMPORTANT - BE CONCISE:
- ALL responses MUST be under 4 sentences maximum
- Provide only essential specs/guidelines
- NO lengthy procedures or full material databases
- Format: "[Material/spec]. [Key property]. [Safety note if needed]."

KNOWLEDGE:
- Materials: PLA, ABS, wood, metal, fabric properties
- Safety: ASTM F963, EN71, age-appropriate guidelines
- Best practices for manufacturing

WORKFLOW:
1. Read project state
2. Answer question concisely
3. Log consultation briefly

GUIDELINES:
- Accurate information only
- Focus on safety-critical specs
- Always include safety considerations
- Suggest the best material for the application
- Consider cost and availability
- Mention any special handling requirements
- Reference standards when applicable
- Check state for project context
- Help other elves make informed decisions
"""


def create_librarian_elf() -> Agent:
    """Create the Librarian Elf agent."""
    client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )

    agent = Agent(
        name="librarian_elf",
        client=client,
        system_prompt=LIBRARIAN_SYSTEM_PROMPT,
        tools=[
            read_project_state,
        
            log_manufacturing_action,
        ],
    )

    return agent
