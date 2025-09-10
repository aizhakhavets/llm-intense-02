# Product Idea: LLM Assistant for Funny Recipe Generation

## Product Description

LLM assistant in the form of a Telegram bot for generating and proposing funny recipes or joke bad recipes based on user preferences, using real existing food and drink products to create impossible surprising combinations of ingredients that can be cooked and can be consumed by human without damage to health.

## Main Functions

### Understanding User Needs
1. Processing user questions about recipe preferences
2. Clarifying user needs regarding available products and ingredients
3. Collecting and structuring key information about user preferences

### Clarify User Preferences
4. Conducting dialogue through Telegram bot based on LLM
5. Personalizing recipe responses based on user context

### Recipe Creation
6. Getting first few recipe options from web or preferred sources based on clarified user preferences
7. Generating surprising simplified recipes for funny culinary experiments

## Technical Implementation

### Architecture
- **Platform**: Telegram Bot API
- **AI Engine**: Large Language Model (LLM)
- **Knowledge Base**: Recipe and ingredient information (history stored in memory)
- **Configuration**: Recipe data and conversation scripts in system prompt

### Data Sources
- Conversation scripts and recipe generation scenarios (prepared manually)

## System Prompt

```text
You are an LLM assistant for generating funny and surprising recipes through Telegram.

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
```

## Expected Results

- Automation of funny recipe generation
- Providing entertaining culinary experiments for users
- Collecting user preferences and available ingredients effectively
- Creating personalized surprising recipe combinations that are actually cookable