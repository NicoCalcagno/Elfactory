"""Santa Claus output model."""

from pydantic import BaseModel, Field


class SantaOutput(BaseModel):
    """Structured output for Santa Claus final approval."""

    approved: bool = Field(description="Whether Santa approves the gift")
    decision: str = Field(
        description="Final decision: APPROVED, REJECTED, or NEEDS_REVISION"
    )
    santa_blessing: str = Field(
        description="Santa's personal blessing and magical touch for the gift"
    )
    feedback: str = Field(
        description="Santa's feedback on the work done by the elves"
    )
    special_notes: str = Field(
        default="",
        description="Any special instructions or magical enhancements Santa wants to add"
    )
