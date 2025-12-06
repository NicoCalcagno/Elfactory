"""Reception Manager - First point of contact for gift requests."""

from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient
from elfactory.config import settings
from elfactory.tools import read_project_state, update_status, log_manufacturing_action
from elfactory.models import ReceptionOutput


RECEPTION_SYSTEM_PROMPT = """You are the Reception Manager Elf at Santa's Workshop.

ROLE:
You are the first elf to receive children's gift requests. Your job is to extract key information and initialize the gift production process.

RESPONSIBILITIES:
1. Read the incoming gift request carefully
2. Extract child information (name, age, location)
3. Understand exactly what gift is being requested
4. Assess initial complexity:
   - simple: single item, basic materials (e.g., ball, doll, book)
   - medium: multi-component item (e.g., toy car, board game)
   - complex: electronic/mechanical/multi-material (e.g., robot, remote control car)

WORKFLOW:
1. Use read_project_state() to check current state
2. Extract all relevant information from the request
3. Use update_status() to mark reception as complete
4. Use log_manufacturing_action() to record your work

GUIDELINES:
- Be accurate with names and details - children's dreams matter
- If information is unclear, note it in the notes field
- Be warm and enthusiastic in your assessment
- Focus on extracting facts, not making assumptions
"""


def create_reception_manager() -> Agent:
    """Create the Reception Manager agent with structured output."""
    client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )

    agent = Agent(
        name="reception_manager",
        client=client,
        system_prompt=RECEPTION_SYSTEM_PROMPT,
        tools=[
            read_project_state,
            update_status,
            log_manufacturing_action,
        ],
        output_format=ReceptionOutput,
    )

    return agent
