"""Design Manager output model."""

from pydantic import BaseModel, Field


class DesignOutput(BaseModel):
    """Structured output for Design Manager."""

    feasibility: str = Field(
        description="Feasibility assessment: fattibile (can manufacture) or impossibile (cannot manufacture)"
    )
    manufacturing_decision: str = Field(
        description="Decision: manufattura (build in workshop) or acquisto_online (buy online)"
    )
    blueprint: str = Field(
        description="Detailed blueprint/plan for manufacturing the gift, including all components needed"
    )
    bill_of_materials: list[dict[str, str]] = Field(
        description="List of materials needed, each with name, quantity, material_type, and specifications"
    )
    estimated_complexity: str = Field(
        description="Final complexity: simple, medium, or complex"
    )
    required_artisans: list[str] = Field(
        description="List of artisan elves needed for this project (e.g., ['3d_printer_elf', 'painter_elf'])"
    )
    notes: str = Field(default="", description="Additional design notes or considerations")
