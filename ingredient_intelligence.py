"""
Local ingredient intelligence system for generating surprising recipe combinations.
Following @conventions.md: functions only, simple data structures, KISS principle.
"""
import random

# Local ingredient database by region/country
LOCAL_INGREDIENTS = {
    "italy": ["parmigiano-reggiano", "balsamic vinegar", "prosciutto", "basil", "pine nuts", "mascarpone", "pancetta", "romano cheese"],
    "mexico": ["lime", "cilantro", "jalapeños", "avocado", "queso fresco", "chipotle", "poblano peppers", "mexican crema"],
    "france": ["butter", "thyme", "shallots", "crème fraîche", "herbs de provence", "calvados", "roquefort", "tarragon"],
    "india": ["curry leaves", "tamarind", "cumin seeds", "coconut", "cardamom", "garam masala", "ghee", "mustard seeds"],
    "japan": ["miso paste", "nori", "mirin", "sesame oil", "shiitake", "dashi", "sake", "wasabi"],
    "thailand": ["fish sauce", "lemongrass", "coconut milk", "thai basil", "galangal", "palm sugar", "lime leaves", "bird's eye chili"],
    "greece": ["feta", "olive oil", "oregano", "olives", "lemon", "capers", "dill", "kasseri cheese"],
    "morocco": ["preserved lemons", "harissa", "ras el hanout", "dates", "almonds", "rose water", "orange blossom", "argan oil"],
    "china": ["soy sauce", "ginger", "star anise", "five-spice", "rice wine", "black vinegar", "scallions", "sesame seeds"],
    "spain": ["saffron", "sherry vinegar", "marcona almonds", "pimentón", "jamón ibérico", "manchego", "romesco", "membrillo"],
    "lebanon": ["sumac", "za'atar", "pomegranate molasses", "tahini", "arak", "rose petals", "pistachios", "labneh"],
    "peru": ["ají amarillo", "quinoa", "purple potatoes", "lucuma", "pisco", "huacatay", "rocoto peppers", "chicha morada"],
    "korea": ["gochujang", "kimchi", "sesame oil", "perilla", "doenjang", "rice wine", "napa cabbage", "korean pear"],
    "turkey": ["sumac", "pomegranate molasses", "bulgur", "turkish coffee", "raki", "pistachios", "dried apricots", "urfa biber"],
    "brazil": ["açaí", "cachaça", "dendê oil", "hearts of palm", "cashews", "coconut", "lime", "malagueta peppers"]
}

# Cultural cooking contexts for storytelling
CULTURAL_CONTEXTS = {
    "italy": "Ancient Roman spice routes meet Renaissance creativity",
    "mexico": "Aztec traditions meet Spanish conquistador influences", 
    "france": "Medieval guild techniques refined by royal chefs",
    "india": "Silk Road spices meet Mughal imperial kitchens",
    "japan": "Zen Buddhist simplicity meets samurai precision",
    "thailand": "Royal Thai court cuisine meets street vendor wisdom",
    "greece": "Ancient Mediterranean trading post flavors",
    "morocco": "Berber nomad traditions meet Arabic palace cuisine",
    "china": "Imperial Forbidden City meets regional diversity",
    "spain": "Moorish influences meet New World discoveries",
    "lebanon": "Phoenician traders meet Ottoman empire flavors",
    "peru": "Incan mountain wisdom meets coastal abundance", 
    "korea": "Royal court cuisine meets fermentation mastery",
    "turkey": "Ottoman sultan's kitchen meets nomadic traditions",
    "brazil": "Indigenous ingredients meet Portuguese colonial fusion"
}

def normalize_location(location: str) -> str:
    """Normalize location string for database lookup"""
    if not location:
        return ""
    
    location_lower = location.lower().strip()
    
    # Direct matches
    if location_lower in LOCAL_INGREDIENTS:
        return location_lower
    
    # Country name variations
    location_mappings = {
        "mexican": "mexico", "italia": "italy", "italian": "italy",
        "french": "france", "indian": "india", "japanese": "japan",
        "thai": "thailand", "greek": "greece", "moroccan": "morocco", 
        "chinese": "china", "spanish": "spain", "lebanese": "lebanon",
        "peruvian": "peru", "korean": "korea", "south korea": "korea",
        "turkish": "turkey", "brazilian": "brazil", "usa": "usa", 
        "america": "usa", "united states": "usa"
    }
    
    for key, value in location_mappings.items():
        if key in location_lower:
            return value if value in LOCAL_INGREDIENTS else ""
    
    return ""

def select_surprise_ingredients(user_location: str, user_ingredients: list, count: int = 2) -> list:
    """
    Select 1-2 local ingredients for surprise combination.
    Avoids ingredients user already mentioned.
    """
    normalized_location = normalize_location(user_location)
    
    if not normalized_location or normalized_location not in LOCAL_INGREDIENTS:
        return []
    
    available_ingredients = LOCAL_INGREDIENTS[normalized_location]
    
    # Convert user ingredients to lowercase for comparison
    user_ingredients_lower = [ing.lower().strip() for ing in user_ingredients if ing]
    
    # Filter out ingredients user already has (avoid duplicates)
    surprise_candidates = []
    for ingredient in available_ingredients:
        # Check if ingredient or part of it is already mentioned by user
        already_mentioned = False
        for user_ing in user_ingredients_lower:
            if (ingredient.lower() in user_ing or 
                user_ing in ingredient.lower() or
                any(word in ingredient.lower() for word in user_ing.split() if len(word) > 3)):
                already_mentioned = True
                break
        
        if not already_mentioned:
            surprise_candidates.append(ingredient)
    
    # Select random ingredients for surprise factor
    if len(surprise_candidates) >= count:
        return random.sample(surprise_candidates, count)
    else:
        return surprise_candidates

def get_cultural_context(location: str) -> str:
    """Get cultural cooking context for storytelling"""
    normalized_location = normalize_location(location)
    return CULTURAL_CONTEXTS.get(normalized_location, "Global fusion traditions meet local wisdom")

def get_available_locations() -> list:
    """Get list of supported locations for debugging/testing"""
    return list(LOCAL_INGREDIENTS.keys())

def has_local_ingredients(location: str) -> bool:
    """Check if we have local ingredient data for this location"""
    return normalize_location(location) in LOCAL_INGREDIENTS
