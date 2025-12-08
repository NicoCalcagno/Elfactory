"""Image generation tools using DALL-E."""

from pathlib import Path
from datapizza.tools import tool
from openai import OpenAI
from elfactory.config import settings
from elfactory.tools.state_tools import active_gifts, current_gift_id


@tool
def generate_gift_image(image_prompt: str, save_path: str = None) -> str:
    """
    Generate an image of the completed gift using DALL-E.

    Args:
        image_prompt: Detailed description of the gift for image generation
        save_path: Optional custom path to save the image (defaults to logs/images/{gift_id}.png)

    Returns:
        Path to the generated image file
    """
    gift_id = current_gift_id.get()

    if not save_path:
        images_dir = Path("logs/images")
        images_dir.mkdir(parents=True, exist_ok=True)
        save_path = str(images_dir / f"{gift_id}.png")

    try:
        client = OpenAI(api_key=settings.openai_api_key)

        response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url

        import requests
        img_data = requests.get(image_url).content

        with open(save_path, 'wb') as f:
            f.write(img_data)

        state = active_gifts.get(gift_id)
        if state:
            state.log_action(
                agent="image_generator",
                action="image_generation",
                details=f"Generated gift image using DALL-E. Saved to: {save_path}"
            )

        return f"✓ Gift image generated successfully and saved to: {save_path}"

    except Exception as e:
        return f"✗ Error generating image: {str(e)}"
