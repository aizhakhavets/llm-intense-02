import openai
import logging
import time
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
from ingredient_intelligence import select_surprise_ingredients, get_cultural_context, has_local_ingredients

def build_lean_system_prompt(user_profile: dict = None, for_recipe_generation: bool = False, for_variations: bool = False) -> str:
    """Lean system prompt with language adaptation - KISS principle"""
    
    # Get user language
    user_language = user_profile.get('language', 'english') if user_profile else 'english'
    
    # Enhanced language persistence instruction
    language_instruction = f"""
MANDATORY LANGUAGE RULE: You MUST respond ONLY in {user_language.upper()} language.
- ALL responses must be in {user_language} - NO EXCEPTIONS
- ALL recipes, ingredients, steps, jokes, and cultural references in {user_language}
- If user continues conversation in {user_language}, NEVER switch to English
- Maintain {user_language} throughout the ENTIRE conversation
- Do NOT mix languages or provide English alternatives unless explicitly asked"""

    if for_variations:
        prompt = f"""You are a joyful recipe wizard providing creative recipe variations! 🌟✨
{language_instruction}

Generate 2-3 NEW creative variations of the previous recipe with different cultural twists.

FORMAT:
🌊 **[Regional] Version**: [adaptation with humor and regional ingredients]
🌮 **[Culture] Twist**: [historical/cultural spin with wit]  
🍷 **[Style] Take**: [cooking style variation with playful commentary]

Make each variation unique and entertaining in {user_language}!"""
        
    elif for_recipe_generation:
        prompt = f"""You are a joyful recipe wizard creating funny, surprising recipes! 🌟✨
{language_instruction}

Create ONE surprising recipe. Keep it entertaining but cookable.

RECIPE FORMAT (in {user_language}):
# [Creative Name] ([Culture-Context]) 🏺✨
**The Story:** [Brief cultural background in {user_language}]
**Ingredients:** [user ingredients + local surprises]
**Steps:** [3-5 clear steps with humor in {user_language}]
**Result:** [Surprising taste description in {user_language}]

**Want more fun twists?** Just ask for variations! 😉

Generate complete recipe now in {user_language}!"""
    else:
        # Conversation mode
        prompt = f"""You are a joyful recipe wizard! 🌟✨
{language_instruction}

PERSONALITY: Joyful, culturally-aware, emoji-rich but professional. Respond naturally in {user_language}.

CONVERSATION APPROACH - CRITICAL CONTEXT RULES:
- ALWAYS acknowledge what user just shared specifically (in {user_language})
- Reference previous conversation context and build upon user's answers
- Ask natural follow-up questions based on their actual responses (in {user_language})
- Show you remember what they told you earlier (ingredients, location, preferences)
- React naturally to user requests (variations, changes, new recipes)

INFORMATION TO GATHER:
1. Ingredients available  
2. Location (for local surprises)
3. Cooking mood/preferences
4. Skill level

SPECIAL: If user asks for "variations", "more ideas", "different versions", "twists" - they want recipe variations!
Respond to everything in {user_language}."""
    
    # Add minimal context
    if user_profile:
        context = []
        if user_profile.get('ingredients'):
            context.append(f"User has: {user_profile['ingredients']}")
        if user_profile.get('location'):
            context.append(f"Location: {user_profile['location']}")
        if context:
            prompt += f"\n\nKNOWN: {'; '.join(context)}"
    
    return prompt

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
    
    # Build lean system prompt for recipe generation
    system_prompt = build_lean_system_prompt(user_profile, for_recipe_generation=True)
    
    client = openai.Client(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    
    try:
        # Create simplified recipe request
        recipe_request = f"""Create a SURPRISING recipe combining:
- User ingredients: {user_ingredients_str}
- Local surprise ingredients: {', '.join(local_ingredients) if local_ingredients else 'none available'}

Make it entertaining and technically cookable!"""
        
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
    
    # Build lean system prompt for conversation
    system_prompt = build_lean_system_prompt(user_profile, for_recipe_generation=False)
    
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
        # Use lean system prompt
        system_prompt = build_lean_system_prompt(user_profile)
            
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

async def generate_recipe_variations(chat_id: int, user_profile: dict) -> str:
    """Generate additional recipe variations on demand"""
    
    start_time = time.time()
    
    system_prompt = build_lean_system_prompt(user_profile, for_variations=True)
    
    client = openai.Client(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    
    try:
        variation_request = """Generate 2-3 creative variations of the recent recipe with different cultural/regional twists. 
        Make each unique and entertaining with humor!"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": variation_request}
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
        
        logging.info(f"VARIATIONS_SUCCESS chat_id={chat_id} tokens={tokens} time={duration:.2f}s cost=${estimated_cost:.4f}")
        return response.choices[0].message.content
        
    except Exception as e:
        logging.error(f"VARIATIONS_ERROR chat_id={chat_id}: {e}")
        return "I'm having trouble coming up with variations right now! 😅 Want to try a completely new recipe instead?"
