from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command

from image_processor import identify_ingredients_from_photo
from audio_processor import transcribe_audio_message
from llm_client import generate_response
from config import MAX_CONTEXT_MESSAGES
from database import (
    get_user_profile,
    create_user_profile,
    update_user_preferences,
    update_journey_stage,
    increment_interaction_count,
    reset_interaction_count,
    delete_user_profile,
    add_message_to_history,
    get_conversation_history as db_get_conversation_history,
    delete_conversation_history,
)
import logging
import json

router = Router()


def get_conversation_history(chat_id: int) -> list[dict]:
    """
    Wrapper to retrieve conversation history from the database.
    """
    return db_get_conversation_history(chat_id, MAX_CONTEXT_MESSAGES)


@router.message(Command("start"))
async def start_handler(message: Message):
    """Initialize conversation and handle user profile."""
    chat_id = message.chat.id
    user_profile = get_user_profile(chat_id)

    if not user_profile:
        create_user_profile(chat_id)
        user_profile = get_user_profile(chat_id)

    # Clear previous conversation history for a fresh start
    delete_conversation_history(chat_id)

    journey_stage = user_profile.get("journey_stage", "new_user") if user_profile else "new_user"

    if journey_stage == "new_user":
        welcome_message = (
            "🌟✨ Welcome, culinary adventurer! I'm your funny recipe wizard who creates "
            "impossible-but-delicious combinations rooted in ancient fusion traditions!\n\n"
            "Let's start our culinary detective work... What ingredients are currently "
            "lurking in your fridge or pantry? Tell me what you have available! 🥘🔍"
        )
        # Progress the user's journey
        update_journey_stage(chat_id, "familiar")
    else: # familiar or health_focused
        preferences = user_profile.get("preferences", {}) if user_profile else {}
        if preferences:
             welcome_message = (
                f"👋 Welcome back! I remember you like {', '.join(preferences.keys())}. "
                f"Ready for another culinary adventure? What ingredients do you have today?"
            )
        else:
            welcome_message = (
                f"👋 Welcome back! I'm ready to cook up some more fun. "
                f"What ingredients are we working with today?"
            )

    add_message_to_history(chat_id, "assistant", welcome_message)
    await message.answer(welcome_message)

@router.message(Command("preferences"))
async def preferences_handler(message: Message):
    """Displays the user's currently stored preferences."""
    chat_id = message.chat.id
    user_profile = get_user_profile(chat_id)

    if user_profile and user_profile.get("preferences"):
        preferences = user_profile["preferences"]
        preferences_str = "\n".join(f"- {key.replace('_', ' ').capitalize()}: {', '.join(map(str, value))}" for key, value in preferences.items())
        response_text = f"📜 **Your Stored Preferences:**\n\n{preferences_str}"
    else:
        response_text = "You don't have any preferences stored yet. I'll learn as we chat!"

    await message.answer(response_text, parse_mode="Markdown")

@router.message(Command("reset"))
async def reset_handler(message: Message):
    """Resets the user's profile and conversation history."""
    chat_id = message.chat.id
    
    # Clear conversation history from db
    delete_conversation_history(chat_id)
    
    # Clear user profile from db
    delete_user_profile(chat_id)

    # Re-initialize profile
    create_user_profile(chat_id)

    response_text = "🧹✨ Your profile has been reset! Let's start a new culinary adventure from scratch."
    await message.answer(response_text)


@router.message(Command("photo_help"))
async def photo_help_handler(message: Message):
    """Provides tips for taking good ingredient photos."""
    help_text = (
        "📸 **Tips for great ingredient photos:**\n\n"
        "1. **Good Lighting:** Use bright, even light.\n"
        "2. **Clear View:** Lay ingredients out, don't stack them.\n"
        "3. **Focus:** Make sure the image is sharp.\n"
        "4. **One at a Time:** For best results, show a few items at once.\n\n"
        "Just send a photo when you're ready!"
    )
    await message.answer(help_text, parse_mode="Markdown")

@router.message(F.photo)
async def photo_handler(message: Message):
    """Handles photo messages to identify ingredients."""
    chat_id = message.chat.id
    
    # Notify user that the photo is being processed
    processing_message = await message.answer("📸 Analyzing your photo to identify ingredients... this might take a moment!")

    try:
        # Get the highest resolution photo
        photo = message.photo[-1]
        photo_file = await message.bot.get_file(photo.file_id)
        
        # Download the photo into a BytesIO buffer
        photo_bytes = await message.bot.download_file(photo_file.file_path)

        # Identify ingredients
        identified_ingredients = await identify_ingredients_from_photo(chat_id, photo_bytes.read())

        # Update the user
        if identified_ingredients and "Error:" not in identified_ingredients[0]:
            ingredients_str = ", ".join(identified_ingredients)
            response_text = (
                f"🔍 I've identified the following ingredients:\n\n"
                f"**{ingredients_str}**\n\n"
                "You can add or remove items, or ask for a recipe with these!"
            )
            add_message_to_history(chat_id, "user", f"[USER SENT A PHOTO WITH INGREDIENTS: {ingredients_str}]")
        elif identified_ingredients and "Error:" in identified_ingredients[0]:
            response_text = f"😕 {identified_ingredients[0]}"
        else:
            response_text = "🤔 I couldn't find any ingredients in your photo. Want to try another one? For tips, use /photo_help."
        
        add_message_to_history(chat_id, "assistant", response_text)
        
        await processing_message.edit_text(response_text, parse_mode="Markdown")

    except Exception as e:
        logging.error(f"Error handling photo for chat_id={chat_id}: {e}")
        await processing_message.edit_text("😕 Sorry, something went wrong while processing your photo. Please try again!")


@router.message(F.voice)
async def voice_handler(message: Message):
    """Handles voice messages for transcription and processing."""
    chat_id = message.chat.id
    
    # Notify user that the audio is being processed
    processing_message = await message.answer("🎤 Listening to your message... one moment!")

    try:
        voice_file = await message.bot.get_file(message.voice.file_id)
        voice_ogg = await message.bot.download_file(voice_file.file_path)

        # Transcribe audio
        transcribed_text = await transcribe_audio_message(chat_id, voice_ogg)

        if "Error:" in transcribed_text:
            await processing_message.edit_text(f"😕 {transcribed_text}")
            return

        # Show the user what was understood
        feedback_text = f"I heard you say: \"_{transcribed_text}_\"\n\nNow, let me think of a recipe..."
        await processing_message.edit_text(feedback_text, parse_mode="Markdown")

        # Add to conversation and generate response
        add_message_to_history(chat_id, "user", transcribed_text)
        conversation_history = get_conversation_history(chat_id)
        response = await generate_response(chat_id, conversation_history)
        
        add_message_to_history(chat_id, "assistant", response)
        await message.answer(response)

    except Exception as e:
        logging.error(f"Error handling voice message for chat_id={chat_id}: {e}")
        await processing_message.edit_text("😕 Sorry, something went wrong while processing your audio. Please try again!")


@router.message()
async def message_handler(message: Message):
    """Handle all user messages by passing them to the LLM."""
    chat_id = message.chat.id
    user_message = message.text

    user_profile = get_user_profile(chat_id)
    if not user_profile:
        create_user_profile(chat_id)
        user_profile = get_user_profile(chat_id)

    # Increment interaction counter
    increment_interaction_count(chat_id)
    interaction_count = user_profile.get("interaction_count", 0) + 1 if user_profile else 1


    # Check if the interaction limit is reached
    if interaction_count >= 30:
        # Reset for a new cycle
        reset_interaction_count(chat_id)
        delete_conversation_history(chat_id)

        retuning_message = (
            "🕰️✨ Wow, time flies when you're cooking with ideas! We've had quite a long chat. "
            "To keep my suggestions fresh and exciting, let's retune our culinary senses. \n\n"
            "What new ingredients or cravings have sparked your imagination recently? "
            "Tell me what you're working with now!"
        )
        add_message_to_history(chat_id, "assistant", retuning_message)
        await message.answer(retuning_message)
        return

    # Add user message to conversation
    add_message_to_history(chat_id, "user", user_message)
    
    # Get conversation history
    conversation_history = get_conversation_history(chat_id)

    # --- Add user preferences to the context for the LLM ---
    if user_profile and user_profile.get("preferences"):
        preferences = user_profile["preferences"]
        preferences_str = json.dumps(preferences)
        # Using a "system" role for this note makes it clear it's context, not user input
        conversation_history.insert(0, {"role": "system", "content": f"System Note: User's current preferences are: {preferences_str}"})

    
    # Generate response from LLM
    llm_response = await generate_response(chat_id, conversation_history)
    
    # --- Preference Extraction Logic ---
    response_to_user = llm_response
    try:
        if "```json" in llm_response:
            json_part = llm_response.split("```json")[1].split("```")[0].strip()
            preferences = json.loads(json_part)
            
            if isinstance(preferences, dict):
                update_user_preferences(chat_id, preferences)
                logging.info(f"Updated preferences for chat_id={chat_id}: {preferences}")

            # Remove the JSON block from the response sent to the user
            response_to_user = llm_response.split("```json")[0].strip()

    except (json.JSONDecodeError, IndexError) as e:
        logging.warning(f"Could not parse preferences from LLM response for chat_id={chat_id}: {e}")
        response_to_user = llm_response # Send the full response if parsing fails
    
    # Add bot response to conversation and send to user
    add_message_to_history(chat_id, "assistant", response_to_user)
    await message.answer(response_to_user)
