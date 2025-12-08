"""State management tools for agents to interact with WorkshopState."""

import json
from contextvars import ContextVar
from datapizza.tools import tool
from elfactory.utils.agent_logger import get_agent_logger

active_gifts: dict[str, "WorkshopState"] = {}
current_gift_id: ContextVar[str] = ContextVar("current_gift_id")


@tool
def read_project_state() -> str:
    """
    Read the current state of the gift project.

    Returns a JSON representation of the complete WorkshopState including:
    - Child information
    - Gift request details
    - All components created so far
    - Manufacturing log
    - Issues and quality reports
    - Current status

    Use this BEFORE starting any work to understand what has already been done.
    """
    gift_id = current_gift_id.get()
    state = active_gifts.get(gift_id)

    if not state:
        return json.dumps({"error": "No active gift project found"})

    return state.model_dump_json(indent=2)


@tool
def write_component(
    component_id: str,
    component_type: str,
    material: str,
    dimensions: str,
    details: str,
    created_by: str,
) -> str:
    """
    Register a newly created component in the workshop state.

    Args:
        component_id: Unique identifier for this component (e.g., "chassis_001", "wheel_left")
        component_type: Type of component (e.g., "chassis", "wheel", "motor", "shell")
        material: Material used (e.g., "red PLA", "wood", "metal", "fabric")
        dimensions: Size specifications (e.g., "15x10x5cm", "diameter 3cm")
        details: Additional details about the component
        created_by: Name of the elf agent who created this (e.g., "3d_printer_elf")

    Returns:
        Confirmation message with component ID
    """
    gift_id = current_gift_id.get()
    state = active_gifts.get(gift_id)

    if not state:
        return "Error: No active gift project found"

    state.add_component({
        "id": component_id,
        "type": component_type,
        "material": material,
        "dimensions": dimensions,
        "details": details,
        "created_by": created_by,
        "status": "completed",
    })

    # Log component creation
    logger = get_agent_logger()
    logger.log_component_created(component_id, component_type, created_by)

    return f"✓ Component '{component_id}' successfully registered by {created_by}"


@tool
def report_issue(
    reported_by: str,
    severity: str,
    description: str,
) -> str:
    """
    Report an issue or problem encountered during production.

    Args:
        reported_by: Name of the agent reporting the issue
        severity: "low", "medium", or "high"
        description: Detailed description of the problem

    Returns:
        Confirmation message
    """
    gift_id = current_gift_id.get()
    state = active_gifts.get(gift_id)

    if not state:
        return "Error: No active gift project found"

    state.add_issue(
        reported_by=reported_by,
        severity=severity,
        description=description,
    )

    # Log issue
    logger = get_agent_logger()
    logger.log_issue(severity, description, reported_by)

    return f"⚠ Issue reported by {reported_by} (severity: {severity})"


@tool
def update_status(new_status: str) -> str:
    """
    Update the overall status of the gift production.

    Args:
        new_status: New status (e.g., "in_progress", "quality_check", "completed", "failed")

    Returns:
        Confirmation message
    """
    gift_id = current_gift_id.get()
    state = active_gifts.get(gift_id)

    if not state:
        return "Error: No active gift project found"

    old_status = state.status
    state.update_status(new_status)

    # Log status change
    logger = get_agent_logger()
    logger.log_status_change(gift_id, old_status, new_status, "system")

    return f"✓ Status updated to: {new_status}"


@tool
def log_manufacturing_action(
    agent: str,
    action: str,
    details: str,
) -> str:
    """
    Log a manufacturing action to the production log.

    Args:
        agent: Name of the agent performing the action
        action: Type of action (e.g., "printing", "assembling", "painting")
        details: Detailed description of what was done

    Returns:
        Confirmation message
    """
    gift_id = current_gift_id.get()
    state = active_gifts.get(gift_id)

    if not state:
        return "Error: No active gift project found"

    state.log_action(
        agent=agent,
        action=action,
        details=details,
    )

    return f"✓ Action logged: {agent} - {action}"


@tool
def set_child_info(
    name: str,
    age: int = None,
    location: str = None,
) -> str:
    """
    Set the child information in the workshop state.

    Args:
        name: Child's name
        age: Child's age (optional)
        location: Child's location/city (optional)

    Returns:
        Confirmation message
    """
    from elfactory.core.state import ChildInfo

    gift_id = current_gift_id.get()
    state = active_gifts.get(gift_id)

    if not state:
        return "Error: No active gift project found"

    state.child_info = ChildInfo(
        name=name,
        age=age,
        location=location,
    )

    # Log child info setting
    logger = get_agent_logger()
    logger.log_child_info(name, age, location)

    return f"✓ Child information set: {name}, age {age}, from {location}"
