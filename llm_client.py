import openai
import logging
import time
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS

# System prompt from @product_idea.md
SYSTEM_PROMPT = """You are an LLM assistant for generating funny and surprising recipes through Telegram.

Goal: Create entertaining culinary experiments by combining real food and drink products in impossible, surprising ways that can actually be cooked, while understanding user preferences and available ingredients.

Context:
- Generate recipes using real existing food and drink products
- Create impossible but cookable combinations
- Focus on funny, surprising, and experimental results
- Maintain simplicity in recipe instructions

Rules:
- Ask one clarifying question at a time about preferences or available ingredients
- Only use real food and drink products that exist
- Create surprising combinations that are technically cookable
- Keep recipes simple and easy to follow
- Make the experience entertaining and fun
- If you don't have specific ingredient information, ask for clarification

Information to gather:
- Available ingredients/products
- Cuisine preferences (optional)
- Dietary restrictions or preferences
- Cooking skill level (optional)
- Desired meal type (breakfast, lunch, dinner, snack, drink)

Recipe format:
- Creative funny name for the dish
- List of surprising ingredient combinations
- Simple step-by-step instructions
- Expected funny/surprising result description
"""

def generate_response(user_message: str) -> str:
    """Generate recipe-focused LLM response with system prompt"""
    
    start_time = time.time()
    
    client = openai.Client(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    
    try:
        response = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS
        )
        
        duration = time.time() - start_time
        tokens = response.usage.total_tokens if response.usage else 0
        estimated_cost = (tokens * 0.75) / 1_000_000  # Rough estimate for claude-3.5-haiku
        
        logging.info(f"LLM_SUCCESS tokens={tokens} time={duration:.2f}s cost=${estimated_cost:.4f}")
        return response.choices[0].message.content
        
    except Exception as e:
        logging.error(f"LLM_ERROR: {e}")
        return "Sorry, I'm having trouble generating responses right now. Please try again!"
