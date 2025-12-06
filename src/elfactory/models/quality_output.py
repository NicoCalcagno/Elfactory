"""Quality Manager output model."""

from pydantic import BaseModel, Field


class QualityOutput(BaseModel):
    """Structured output for Quality Manager."""

    overall_status: str = Field(
        description="Overall quality assessment: PASS or FAIL"
    )
    components_checked: int = Field(
        description="Number of components inspected"
    )
    safety_approved: bool = Field(
        description="Whether the gift meets safety standards for children"
    )
    issues_found: list[str] = Field(
        default_factory=list,
        description="List of quality issues or defects found"
    )
    inspection_notes: str = Field(
        description="Detailed notes from the quality inspection"
    )
    recommendation: str = Field(
        description="Recommendation: approve, reject, or rework"
    )
