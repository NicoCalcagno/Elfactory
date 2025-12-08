"""3D Printer Elf - Creates components using 3D printing technology."""

from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient
from elfactory.config import settings
from elfactory.tools import (
    read_project_state,
    write_component,
    log_manufacturing_action,
)


PRINTER_3D_SYSTEM_PROMPT = """You are the 3D Printer Elf at Santa's Workshop.

ROLE:
You create plastic components using 3D printing.

MATERIALS:
- PLA (all colors), ABS (strong), PETG (flexible), TPU (rubber-like)

IMPORTANT - BE CONCISE:
- ALL responses MUST be 1-2 sentences maximum
- Register component with minimal details
- NO lengthy specs or explanations
- Format: "Printed [component] in [material]. Done."

WORKFLOW:
1. Read project state
2. Register component with write_component()
3. Log action briefly
4. Report issues only if critical

GUIDELINES:
- Match blueprint specs
- Ensure child safety (no sharp edges, toy-safe materials)
- Use tools to log, keep direct response under 2 sentences
"""


def create_3d_printer_elf() -> Agent:
    """Create the 3D Printer Elf agent."""
    client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )

    agent = Agent(
        name="3d_printer_elf",
        client=client,
        system_prompt=PRINTER_3D_SYSTEM_PROMPT,
        tools=[
            read_project_state,
            write_component,
            log_manufacturing_action,
        ],
    )

    return agent
