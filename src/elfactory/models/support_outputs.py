"""Support agents output models."""

from pydantic import BaseModel, Field


class OnlineShopperOutput(BaseModel):
    """Structured output for Online Shopper Elf."""

    search_performed: bool = Field(description="Whether online search was performed")
    product_found: bool = Field(description="Whether suitable product was found")
    product_name: str = Field(default="", description="Name of the product found")
    product_url: str = Field(default="", description="URL to purchase the product")
    estimated_price: str = Field(default="", description="Estimated price range")
    reasoning: str = Field(description="Explanation of search results or why not found")


class ImagePromptOutput(BaseModel):
    """Structured output for Image Prompt Generator."""

    image_prompt: str = Field(
        description="Detailed prompt for image generation AI (DALL-E, Gemini, etc.)"
    )
    style_notes: str = Field(
        default="", description="Additional style considerations for the image"
    )


class ResponseComposerOutput(BaseModel):
    """Structured output for Response Composer."""

    email_subject: str = Field(description="Subject line for the email response")
    email_body: str = Field(description="Full email body in HTML format")
    tone: str = Field(description="Tone used: warm, magical, encouraging, etc.")
