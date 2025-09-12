import openai
import logging
import time
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
from ingredient_intelligence import select_surprise_ingredients, get_cultural_context, has_local_ingredients

def build_dynamic_system_prompt(user_profile: dict = None, local_ingredients: list = None, conversation_state: str = None, for_recipe_generation: bool = False, surprise_focus: bool = False) -> str:
    """Build system prompt with user context, local ingredients, and conversational task"""
    
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

    if for_recipe_generation:
        base_prompt += """

RECIPE GENERATION TASK:
- Create ONE surprising recipe using user ingredients + local surprise ingredients
- IMPORTANT: Make it EXTREMELY SURPRISING but technically cookable
- Focus on unexpected ingredient combinations that create culinary surprise
- Include at least one joke or humorous element in the recipe
- Generate 3-7 steps based on skill level (simpler for beginners)
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
2. [Continue with 3-7 total steps based on skill level]
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
    else:
        base_prompt += "\n\nCONVERSATIONAL TASK:\n"
        if conversation_state == "discovering_location":
            base_prompt += "Your task is to ask for the user's location to suggest surprise local ingredients. Explain why you're asking, with humor and charm. Keep it to one concise question."
        elif conversation_state == "asking_mood":
            base_prompt += "Your task is to ask about the user's cooking mood (e.g., adventurous, comfort food). Make it fun and keep it to one question!"
        elif conversation_state == "checking_skill_level":
            base_prompt += "Your task is to ask for the user's cooking skill level (e.g., kitchen ninja or cautious experimenter). Keep it light, encouraging, and ask one question."
        elif conversation_state in ["post_recipe_reaction", "post_recipe_followup"]:
            base_prompt += """You have already provided a recipe. The user is now responding.
- **If the user's message is about cooking, recipes, or ingredients**: Engage with them! Offer to make adjustments, suggest variations, answer their questions, or start a completely new recipe idea. Be proactive and helpful.
- **If the user's message is off-topic (e.g., about politics, weather, your own nature as an AI)**: You MUST respond from your chef personality. Use cooking metaphors to answer their question humorously, and then gently steer the conversation back to food. For example, if asked about the weather, you might say 'The forecast in my kitchen is a high chance of delicious aromas, with a slight drizzle of olive oil! What culinary adventure shall we cook up next?'
Keep your response concise and focused on moving the conversation forward."""
        else:
            base_prompt += "Your task is to continue the conversation naturally, following your personality. Ask one clear question to move the conversation forward towards creating a recipe."

    return base_prompt

async def generate_recipe_with_local_ingredients(chat_id: int, user_profile: dict, regeneration_hints: str = None) -> str:
    """Generate recipe using user profile and local ingredient intelligence"""
    
    start_time = time.time()
    
    # Get user ingredients and location
    user_ingredients_str = user_profile.get('ingredients', '')
    user_location = user_profile.get('location', '')
    
    # Parse user ingredients into list
    user_ingredients = [ing.strip() for ing in user_ingredients_str.replace(',', ' ').split() if ing.strip()]
    
    # Select local surprise ingredients
    local_ingredients = select_surprise_ingredients(user_location, user_ingredients, count=2)
    
    # Build dynamic system prompt with context and surprise focus
    system_prompt = build_dynamic_system_prompt(user_profile, local_ingredients, for_recipe_generation=True, surprise_focus=True)
    
    client = openai.Client(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    
    try:
        # Create focused recipe generation message with emphasis on surprise and humor
        recipe_request = f"""Create an EXTREMELY surprising recipe combining:
- User ingredients: {user_ingredients_str}
- Local surprise ingredients: {', '.join(local_ingredients) if local_ingredients else 'none available'}

Requirements:
- Make it EXTREMELY surprising with unexpected ingredient combinations
- Include at least one joke or humorous element
- Ensure it's technically cookable despite the surprising combinations
- Add cultural context and storytelling"""
        
        # Add regeneration hints if provided (for subsequent attempts)
        if regeneration_hints:
            recipe_request += f"\n\nSPECIAL FOCUS FOR THIS ATTEMPT:\n{regeneration_hints}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": recipe_request}
        ]
        
        response = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=messages,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS
        )
        
        duration = time.time() - start_time
        tokens = response.usage.total_tokens if response.usage else 0
        estimated_cost = (tokens * 0.75) / 1_000_000
        
        logging.info(f"RECIPE_SUCCESS chat_id={chat_id} location={user_location} local_ingredients={len(local_ingredients)} tokens={tokens} time={duration:.2f}s cost=${estimated_cost:.4f}")
        return response.choices[0].message.content
        
    except Exception as e:
        logging.error(f"RECIPE_ERROR chat_id={chat_id}: {e}")
        return "Sorry, I'm having trouble creating your culinary masterpiece right now. Please try again! 😅✨"

async def generate_contextual_response(chat_id: int, user_profile: dict, conversation_history: list[dict], current_state: str) -> str:
    """Generate a contextual conversational response using the LLM."""
    
    start_time = time.time()
    
    # Build dynamic system prompt for conversation
    system_prompt = build_dynamic_system_prompt(user_profile, conversation_state=current_state, for_recipe_generation=False)
    
    client = openai.Client(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    
    try:
        messages = [
            {"role": "system", "content": system_prompt}
        ] + conversation_history
        
        response = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=messages,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS
        )
        
        duration = time.time() - start_time
        tokens = response.usage.total_tokens if response.usage else 0
        estimated_cost = (tokens * 0.75) / 1_000_000
        
        logging.info(f"CONTEXT_SUCCESS chat_id={chat_id} state={current_state} tokens={tokens} time={duration:.2f}s cost=${estimated_cost:.4f}")
        return response.choices[0].message.content
        
    except Exception as e:
        logging.error(f"CONTEXT_ERROR chat_id={chat_id} state={current_state}: {e}")
        return "I seem to be lost for words... could you please try that again? 🤔"

def generate_response(chat_messages: list[dict], user_profile: dict = None) -> str:
    """Generate response using full conversation history (legacy function for compatibility)"""
    
    start_time = time.time()
    
    client = openai.Client(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    
    try:
        # Use dynamic system prompt if profile available
        if user_profile:
            system_prompt = build_dynamic_system_prompt(user_profile)
        else:
            system_prompt = build_dynamic_system_prompt()
            
        # Prepare messages: system prompt + chat history
        messages = [
            {"role": "system", "content": system_prompt}
        ] + chat_messages
        
        response = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=messages,
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
