"""Reception Manager output model."""

from pydantic import BaseModel, Field


class ReceptionOutput(BaseModel):
    """Structured output for Reception Manager."""

    child_name: str = Field(description="Name of the child requesting the gift")
    child_age: int | None = Field(default=None, description="Age of the child if mentioned")
    child_location: str | None = Field(default=None, description="Location/city if mentioned")
    gift_description: str = Field(description="Clear, concise description of the requested gift")
    complexity_assessment: str = Field(
        description="Initial complexity assessment: simple, medium, or complex"
    )
    notes: str = Field(default="", description="Any additional observations or special requests")
