"""Production Manager output model."""

from pydantic import BaseModel, Field


class ProductionOutput(BaseModel):
    """Structured output for Production Manager."""

    production_status: str = Field(
        description="Overall production status: in_progress, completed, or failed"
    )
    components_completed: int = Field(
        description="Number of components successfully created"
    )
    artisans_used: list[str] = Field(
        description="List of artisan elves that worked on this project"
    )
    issues_encountered: list[str] = Field(
        default_factory=list,
        description="List of issues encountered during production"
    )
    production_summary: str = Field(
        description="Summary of the production process and what was built"
    )
    ready_for_quality_check: bool = Field(
        description="Whether the gift is ready for quality inspection"
    )
