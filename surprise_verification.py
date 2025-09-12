"""
Surprise verification system for ensuring recipes meet surprise criteria and include humor.
Following @conventions.md: functions only, simple data structures, KISS principle.
"""
import re
import logging
import openai
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
import time

# Surprise scoring constants
COMMON_INGREDIENT_PAIRS = {
    ("chicken", "rice"), ("beef", "potatoes"), ("pasta", "tomato"), 
    ("fish", "lemon"), ("pork", "apple"), ("lamb", "mint"),
    ("bread", "butter"), ("eggs", "cheese"), ("potato", "onion"),
    ("tomato", "basil"), ("garlic", "olive oil"), ("chocolate", "vanilla")
}

SURPRISING_INGREDIENT_PAIRS = {
    ("chocolate", "chicken"), ("coffee", "beef"), ("strawberry", "fish"),
    ("vanilla", "garlic"), ("cinnamon", "salmon"), ("honey", "pizza"),
    ("peanut butter", "curry"), ("banana", "bacon"), ("watermelon", "cheese"),
    ("cola", "chicken"), ("lavender", "potato"), ("blueberry", "steak")
}

def extract_ingredients(recipe_text: str) -> list:
    """Extract ingredients from recipe text"""
    # Look for ingredients section
    ingredients_section = re.search(r"\*\*Ingredients:\*\*(.*?)(?:\*\*Steps|\*\*Result|\*\*The Story|\Z)", 
                                  recipe_text, re.DOTALL)
    
    if not ingredients_section:
        return []
    
    # Extract individual ingredients
    ingredients_text = ingredients_section.group(1)
    ingredients = []
    
    # Extract from bullet points
    for line in ingredients_text.split('\n'):
        line = line.strip()
        if line.startswith('-'):
            ingredient = line[1:].strip()
            ingredients.append(ingredient)
    
    return ingredients

def extract_joke(recipe_text: str) -> str:
    """Extract joke or humorous content from recipe"""
    # Look for humor in various sections
    humor_patterns = [
        r"Plot twist.*?(?:\n\n|\Z)",  # Plot twist section
        r"\*\*Result:\*\*.*?(?:\n\n|\Z)",  # Result section often has humor
        r"🌊.*?(?:\n\n|\Z)",  # Regional version jokes
        r"🌮.*?(?:\n\n|\Z)",  # Culture revenge jokes
        r"🍷.*?(?:\n\n|\Z)"   # Culture rebellion jokes
    ]
    
    jokes = []
    for pattern in humor_patterns:
        matches = re.finditer(pattern, recipe_text, re.DOTALL)
        for match in matches:
            jokes.append(match.group(0).strip())
    
    return "\n".join(jokes) if jokes else ""

def calculate_surprise_score(ingredients: list, user_profile: dict) -> float:
    """
    Calculate surprise score based on ingredient combinations.
    Higher score = more surprising.
    """
    if not ingredients or len(ingredients) < 2:
        return 0.0
    
    score = 0.0
    total_pairs = 0
    
    # Convert ingredients to lowercase for comparison
    normalized_ingredients = []
    for item in ingredients:
        # Extract main ingredient name from descriptions
        main_ingredient = item.split(',')[0].split('(')[0].lower().strip()
        # Extract key words from ingredient descriptions
        words = main_ingredient.split()
        if words:
            normalized_ingredients.append(words[0])  # Take first word as main ingredient
    
    if len(normalized_ingredients) < 2:
        return 0.0
    
    # Define food categories for better matching
    food_categories = {
        "meats": ["chicken", "beef", "pork", "meat", "steak", "lamb", "turkey", "duck", "jerky"],
        "seafood": ["fish", "shrimp", "seafood", "salmon", "tuna", "cod", "lobster"],
        "dairy": ["milk", "cheese", "yogurt", "cream", "butter", "mozzarella", "cheddar", "ice"],
        "sweets": ["chocolate", "sugar", "candy", "dessert", "sweet", "cake", "vanilla", "honey", "cream"],
        "fruits": ["apple", "banana", "orange", "berry", "fruit", "mango", "peach", "strawberry", "strawberries"],
        "vegetables": ["carrot", "broccoli", "spinach", "vegetable", "lettuce", "tomato", "onion"],
        "grains": ["rice", "bread", "pasta", "wheat", "quinoa", "oats"],
        "spices": ["cumin", "paprika", "cinnamon", "garlic", "ginger", "basil", "oregano"],
        "sauces": ["sauce", "ketchup", "mustard", "mayo", "soy"]
    }
    
    # Check all ingredient pairs
    for i in range(len(normalized_ingredients)):
        for j in range(i+1, len(normalized_ingredients)):
            ing1 = normalized_ingredients[i]
            ing2 = normalized_ingredients[j]
            
            # Find categories for each ingredient
            ing1_category = None
            ing2_category = None
            
            for category, keywords in food_categories.items():
                if any(keyword in ing1 for keyword in keywords):
                    ing1_category = category
                if any(keyword in ing2 for keyword in keywords):
                    ing2_category = category
            
            # Score based on category combinations
            if ing1_category and ing2_category:
                if ing1_category == ing2_category:
                    # Same category = less surprising
                    score += 0.2
                elif (ing1_category == "sweets" and ing2_category in ["meats", "seafood"]) or \
                     (ing2_category == "sweets" and ing1_category in ["meats", "seafood"]):
                    # Sweet + savory protein = very surprising
                    score += 1.5
                elif ing1_category != ing2_category:
                    # Different categories = moderately surprising
                    score += 0.8
            else:
                # Unknown ingredients = assume neutral
                score += 0.5
            
            total_pairs += 1
    
    # Normalize score based on number of pairs and return
    final_score = score / max(1, total_pairs)
    return min(final_score, 2.0)  # Cap at 2.0 for very surprising combinations

def has_sufficient_humor(joke_text: str) -> bool:
    """Check if recipe has sufficient humor content"""
    if not joke_text:
        return False
    
    # Simple checks for humor indicators
    humor_indicators = ["twist", "revenge", "rebellion", "plot", "joke", "humor", 
                       "funny", "laugh", "surprise", "unexpected", "because", "would've"]
    
    # Count humor indicators
    humor_count = sum(1 for indicator in humor_indicators if indicator in joke_text.lower())
    
    # Check for emoji presence (often indicates humor in our format)
    has_emoji = any(char in joke_text for char in "🌊🌮🍷🎭✨🔥")
    
    return humor_count >= 2 or has_emoji

async def verify_recipe_surprise(recipe_text: str, user_profile: dict) -> dict:
    """
    Verify if recipe meets surprise criteria and includes humor.
    Returns dict with verification results and enhancement suggestions.
    """
    verification_result = {
        "original_recipe": recipe_text,
        "ingredients": [],
        "joke_text": "",
        "surprise_score": 0.0,
        "has_humor": False,
        "needs_enhancement": False,
        "enhancement_suggestions": []
    }
    
    # Extract ingredients and jokes
    verification_result["ingredients"] = extract_ingredients(recipe_text)
    verification_result["joke_text"] = extract_joke(recipe_text)
    
    # Calculate surprise score
    verification_result["surprise_score"] = calculate_surprise_score(
        verification_result["ingredients"], 
        user_profile
    )
    
    # Check humor content
    verification_result["has_humor"] = has_sufficient_humor(verification_result["joke_text"])
    
    # Determine if enhancement needed
    verification_result["needs_enhancement"] = (
        verification_result["surprise_score"] < 0.5 or 
        not verification_result["has_humor"]
    )
    
    # Generate enhancement suggestions if needed
    if verification_result["needs_enhancement"]:
        if verification_result["surprise_score"] < 0.5:
            verification_result["enhancement_suggestions"].append(
                "Increase surprise factor by adding more unexpected ingredient combinations"
            )
        if not verification_result["has_humor"]:
            verification_result["enhancement_suggestions"].append(
                "Add more humor and jokes, especially in the variations section"
            )
    
    return verification_result

def get_regeneration_hints(verification_result: dict, attempt_number: int) -> str:
    """
    Generate hints for recipe regeneration based on verification failures.
    Returns string with specific guidance for improving surprise factor.
    """
    hints = []
    
    if verification_result["surprise_score"] < 0.5:
        hints.append("Focus on more unexpected ingredient combinations")
        hints.append("Mix ingredients from different culinary traditions")
        hints.append("Combine sweet and savory elements in surprising ways")
        
        # More aggressive hints for later attempts
        if attempt_number >= 2:
            hints.append("Use ingredients that would never normally go together")
            hints.append("Create fusion between completely different cuisines")
    
    if not verification_result["has_humor"]:
        hints.append("Include at least one clear joke or humorous observation")
        hints.append("Add funny cultural commentary in the variations section")
        hints.append("Use playful language and cultural references")
        
        # More specific humor hints for later attempts
        if attempt_number >= 2:
            hints.append("Add witty observations about cultural cooking traditions")
            hints.append("Include humorous historical anecdotes about the ingredients")
    
    return " | ".join(hints) if hints else "Create maximum surprise with unexpected combinations"

async def enhance_recipe(recipe_text: str, verification_result: dict) -> str:
    """
    Enhance recipe based on verification results to increase surprise and humor.
    Returns enhanced recipe text.
    """
    if not verification_result["needs_enhancement"]:
        return recipe_text  # No enhancement needed
    
    start_time = time.time()
    
    client = openai.Client(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
    
    try:
        # Build system prompt for enhancement
        system_prompt = """You are an expert recipe enhancer focusing on SURPRISE and HUMOR.
        
Your task is to enhance a recipe to make it more surprising and humorous while maintaining its cookability.

ENHANCEMENT RULES:
- Preserve the overall structure and format of the recipe
- Keep the same recipe name and basic concept
- Make ingredient combinations more surprising (mix sweet/savory, unexpected pairings)
- Add more humor and jokes throughout, especially in the variations section
- Ensure there's at least one clear joke in the recipe
- Add emoji for emphasis in appropriate places
- Keep the recipe cookable despite surprising combinations

DO NOT:
- Change the recipe format or structure
- Remove any existing sections
- Make the recipe impossible to cook

Return the COMPLETE enhanced recipe with all original sections."""

        # Create enhancement request message
        enhancement_request = f"""Enhance this recipe to make it more surprising and humorous:

{recipe_text}

Enhancement needed:
{"- Increase surprise factor with more unexpected ingredient combinations" if verification_result["surprise_score"] < 0.5 else ""}
{"- Add more humor and jokes, especially in the variations section" if not verification_result["has_humor"] else ""}

Make the recipe more SURPRISING and FUNNY while keeping it cookable!"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": enhancement_request}
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
        
        logging.info(f"ENHANCE_SUCCESS surprise_score={verification_result['surprise_score']} has_humor={verification_result['has_humor']} tokens={tokens} time={duration:.2f}s cost=${estimated_cost:.4f}")
        return response.choices[0].message.content
        
    except Exception as e:
        logging.error(f"ENHANCE_ERROR: {e}")
        return recipe_text  # Return original if enhancement fails
