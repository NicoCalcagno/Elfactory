"""Fabric Elf - Sews and crafts fabric components."""

from datapizza.agents import Agent
from datapizza.clients.openai import OpenAIClient
from elfactory.config import settings
from elfactory.tools import (
    read_project_state,
    write_component,

    log_manufacturing_action,
)


FABRIC_SYSTEM_PROMPT = """You are the Fabric Elf at Santa's Workshop.

ROLE:
You sew and craft fabric components.

IMPORTANT - BE CONCISE:
- ALL responses MUST be 1-2 sentences maximum
- Register component with minimal details
- NO sewing procedures or stitch descriptions
- Format: "Sewed [item] from [fabric]. Done."

WORKFLOW:
1. Read project state
2. Register component
3. Log action briefly

SAFETY:
- Secure all seams
- No loose fibers or choking hazards
- dimensions: measurements (e.g., "20x15cm plush")
- details: stitching type, embellishments, stuffing density
- created_by: "fabric_elf"

GUIDELINES:
- Double-stitch seams for strength
- No small buttons or beads for young children (choking hazard)
- Use child-safe, non-toxic fabrics
- Ensure stuffing stays inside (no loose stuffing)
- Check for loose threads
- Machine washable materials when possible
- Check state for fabric component needs
"""


def create_fabric_elf() -> Agent:
    """Create the Fabric Elf agent."""
    client = OpenAIClient(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
    )

    agent = Agent(
        name="fabric_elf",
        client=client,
        system_prompt=FABRIC_SYSTEM_PROMPT,
        tools=[
            read_project_state,
            write_component,
        
            log_manufacturing_action,
        ],
    )

    return agent
