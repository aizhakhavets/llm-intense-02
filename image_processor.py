import base64
import logging
from io import BytesIO

import openai
from PIL import Image

from config import OPENROUTER_API_KEY, OPENROUTER_VISION_MODEL

client = openai.AsyncClient(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

async def identify_ingredients_from_photo(chat_id: int, image_data: bytes) -> list[str]:
    """
    Identifies ingredients from a given photo using a vision model.
    Resizes the image for performance and encodes it to base64.
    Returns a list of identified ingredients.
    """
    try:
        # Resize image for faster processing
        image = Image.open(BytesIO(image_data))
        max_size = 512
        image.thumbnail((max_size, max_size))

        # Convert to BytesIO buffer
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        
        # Encode to base64
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        
        response = await client.chat.completions.create(
            model=OPENROUTER_VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Identify the food ingredients in this image. List them as a simple comma-separated string. For example: tomatoes, onions, garlic. If no food ingredients are visible, return an empty string."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        content = response.choices[0].message.content.strip()
        logging.info(f"Vision API identified ingredients for chat_id={chat_id}: {content}")

        if not content or "no ingredients found" in content.lower():
            return []
            
        # Split by comma and clean up whitespace
        ingredients = [item.strip() for item in content.split(',')]
        return ingredients

    except Exception as e:
        logging.error(f"Error identifying ingredients from photo for chat_id={chat_id}: {e}")
        return ["Error: Could not analyze the image."]
