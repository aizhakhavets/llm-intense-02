# Coding Conventions

*Development rules based on @vision.md principles*

## Code Style

**Functions Only**
- No classes or OOP - pure functional approach
- One function = one responsibility
- Pass data as parameters, avoid global state

**Naming**
- Clear names: `generate_funny_recipe()` not `gen_rec()`
- Self-documenting through naming
- Use verbs for functions, nouns for data

**Data Structures** 
- Simple types only: `dict`, `list`, `str`, `int`, `float`
- No complex data classes or objects

## Architecture

**Layer Organization** (per @vision.md structure)
- `main.py` - entry point only
- `config.py` - environment variables only  
- `handlers.py` - message processing layer
- `llm_client.py` - LLM integration layer
- Each module has single responsibility

## Implementation Rules

**KISS Principle** = Keep It Simple, Stupid:
- Simple solutions are better than complex ones
- Minimum code to achieve the goal
- Clarity is more important than "smartness"
- Direct approach over clever solutions
- If a function can be avoided - don't write it
- Minimum abstractions needed
- Solve only current problem

**Code Quality**
- Comments only for complex logic
- Pure functions where possible (easier to test)
- No global variables or state
- Function parameters for all data flow

## Testing

**Simple Unit Tests**
- Test core functions only
- Focus on business logic (recipe generation)
- No complex test frameworks beyond pytest

---

*For architecture details, system design, and deployment - see @vision.md*