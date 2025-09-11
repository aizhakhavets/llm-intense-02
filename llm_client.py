import openai
import logging
import time
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
from ingredient_intelligence import select_surprise_ingredients, get_cultural_context, has_local_ingredients

def build_dynamic_system_prompt(user_profile: dict = None, local_ingredients: list = None) -> str:
    """Build system prompt with user context and local ingredients"""
    
    base_prompt = """You are a joyful, culturally-aware recipe wizard for Telegram who creates entertaining culinary experiments rooted in ancient fusion traditions! 🌟✨

PERSONALITY TRAITS:
🎭 Joyful, emoji-rich but never childish - professional advice wrapped in playful presentation
🏛️ Reference ancient culinary history and fusion traditions (Silk Road, Ottoman Empire, Aztec-Spanish fusion, etc.)
🧠 Smart, nuanced suggestions with cultural context and storytelling
🌍 Draw from global, lesser-known cuisine combinations and historical food exchanges
💫 Proactively offer creative variations with humor after each recipe
🎪 Use cultural commentary with playful humor ("because the French can't resist improving everyone's recipes!")
"""
    
    # Add current user context
    if user_profile:
        base_prompt += "\n\nCURRENT USER CONTEXT:\n"
        
        if user_profile.get('location'):
            location = user_profile['location']
            cultural_context = get_cultural_context(location)
            base_prompt += f"🌍 User location: {location} ({cultural_context})\n"
            
        if user_profile.get('ingredients'):
            base_prompt += f"🥘 User ingredients: {user_profile['ingredients']}\n"
            
        if local_ingredients:
            base_prompt += f"✨ Local surprise ingredients to include: {', '.join(local_ingredients)}\n"
            
        if user_profile.get('mood'):
            base_prompt += f"🎭 User mood: {user_profile['mood']}\n"
            
        if user_profile.get('skill_level'):
            base_prompt += f"👨‍🍳 Cooking skill level: {user_profile['skill_level']}\n"
    
    base_prompt += """

RECIPE GENERATION TASK:
- Create ONE surprising recipe using user ingredients + local surprise ingredients
- IMPORTANT: Make it VERY SURPRISING but technically cookable
- Generate 3-5 steps based on skill level (simpler for beginners)
- Include cultural/historical context and storytelling
- Add sensory descriptions with cultural metaphors

RECIPE FORMAT:
# [Creative Name] ([Historical-Context]) 🏺✨

**The Story:** [Brief cultural/historical background that inspired the dish]

**Ingredients:**
- [User's original ingredients]
- [Local surprise ingredients with cultural notes]
- [Any additional needed ingredients]

**Steps:**
1. [Cultural cooking technique reference] - [clear instruction with humor]
2. [Continue with 3-5 total steps based on skill level]
3. [Include sensory cues and cooking wisdom]

**Result:** [Sensory description with cultural metaphors and surprising taste profile]

MANDATORY PROACTIVE VARIATIONS:
After EVERY recipe, offer 2-3 humorous variations:

**Plot twist time! 🎭 Want to shake things up even more?**

🌊 **[Regional] Version**: [adaptation with regional twist and humor]
🌮 **[Culture] Revenge**: [historical timeline twist with playful commentary] 
🍷 **[Culture] Rebellion**: [cultural adaptation with witty observation]

Which timeline calls to you? Or shall we explore completely different cosmic combinations? ✨

Generate the complete recipe now!"""
    
    return base_prompt

async def generate_recipe_with_local_ingredients(chat_id: int, user_profile: dict) -> str:
    """Generate recipe using user profile and local ingredient intelligence"""
    
    start_time = time.time()
    
    # Get user ingredients and location
    user_ingredients_str = user_profile.get('ingredients', '')
    user_location = user_profile.get('location', '')
    
    # Parse user ingredients into list
    user_ingredients = [ing.strip() for ing in user_ingredients_str.replace(',', ' ').split() if ing.strip()]
    
    # Select local surprise ingredients
    local_ingredients = select_surprise_ingredients(user_location, user_ingredients, count=2)
    
    # Build dynamic system prompt with context
    system_prompt = build_dynamic_system_prompt(user_profile, local_ingredients)
    
    client = openai.Client(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    
    try:
        # Create focused recipe generation message
        recipe_request = f\"\"\"Create a surprising recipe combining:\n- User ingredients: {user_ingredients_str}\n- Local surprise ingredients: {', '.join(local_ingredients) if local_ingredients else 'none available'}\n\nMake it VERY surprising but cookable!\"\"\"\n        \n        messages = [\n            {\"role\": \"system\", \"content\": system_prompt},\n            {\"role\": \"user\", \"content\": recipe_request}\n        ]\n        \n        response = client.chat.completions.create(\n            model=OPENROUTER_MODEL,\n            messages=messages,\n            temperature=LLM_TEMPERATURE,\n            max_tokens=LLM_MAX_TOKENS\n        )\n        \n        duration = time.time() - start_time\n        tokens = response.usage.total_tokens if response.usage else 0\n        estimated_cost = (tokens * 0.75) / 1_000_000\n        \n        logging.info(f\"RECIPE_SUCCESS chat_id={chat_id} location={user_location} local_ingredients={len(local_ingredients)} tokens={tokens} time={duration:.2f}s cost=${estimated_cost:.4f}\")\n        return response.choices[0].message.content\n        \n    except Exception as e:\n        logging.error(f\"RECIPE_ERROR chat_id={chat_id}: {e}\")\n        return \"Sorry, I'm having trouble creating your culinary masterpiece right now. Please try again! \ud83d\ude05\u2728\"\n\ndef generate_response(chat_messages: list[dict], user_profile: dict = None) -> str:\n    \"\"\"Generate response using full conversation history (legacy function for compatibility)\"\"\" \n    \n    start_time = time.time()\n    \n    client = openai.Client(\n        api_key=OPENROUTER_API_KEY,\n        base_url=\"https://openrouter.ai/api/v1\"\n    )\n    \n    try:\n        # Use dynamic system prompt if profile available\n        if user_profile:\n            system_prompt = build_dynamic_system_prompt(user_profile)\n        else:\n            system_prompt = build_dynamic_system_prompt()\n            \n        # Prepare messages: system prompt + chat history\n        messages = [\n            {\"role\": \"system\", \"content\": system_prompt}\n        ] + chat_messages\n        \n        response = client.chat.completions.create(\n            model=OPENROUTER_MODEL,\n            messages=messages,\n            temperature=LLM_TEMPERATURE,\n            max_tokens=LLM_MAX_TOKENS\n        )\n        \n        duration = time.time() - start_time\n        tokens = response.usage.total_tokens if response.usage else 0\n        estimated_cost = (tokens * 0.75) / 1_000_000  # Rough estimate for claude-3.5-haiku\n        \n        logging.info(f\"LLM_SUCCESS tokens={tokens} time={duration:.2f}s cost=${estimated_cost:.4f}\")\n        return response.choices[0].message.content\n        \n    except Exception as e:\n        logging.error(f\"LLM_ERROR: {e}\")\n        return \"Sorry, I'm having trouble generating responses right now. Please try again!\"
