"""Logistics Manager output model."""

from pydantic import BaseModel, Field


class LogisticsOutput(BaseModel):
    """Structured output for Logistics Manager."""

    packaging_design: str = Field(
        description="Description of how the gift will be packaged"
    )
    wrapping_style: str = Field(
        description="Gift wrapping style and colors chosen"
    )
    gift_card_message: str = Field(
        description="Personalized message for the gift card to the child"
    )
    special_instructions: str = Field(
        default="",
        description="Any special delivery or handling instructions"
    )
    ready_for_santa: bool = Field(
        description="Whether the gift is ready for Santa's final approval"
    )
