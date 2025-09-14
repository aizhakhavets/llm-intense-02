# Development Workflow

*Rules for code assistant working on @tasklist.md according to @vision.md*

## Core Principle

**Work strictly by plan** - one iteration at a time with mandatory confirmation at each step.

## Iteration Process

### 1. Plan & Propose
- Take next iteration from @tasklist.md
- Study requirements and expected tests
- **Propose solution with code examples**
- **WAIT FOR CONFIRMATION** - do not implement without approval

### 2. Implement
- Code only the agreed solution
- Follow @vision.md principles:
  - Functional approach, no OOP
  - Simple functions by domains
  - Minimal dependencies
- Test immediately after each step:
  - All tests must be stored in the `/tests/` directory.
  - All tests must be runnable (`pytest` or `make test`) and passing after every change.

### 3. Report & Update
- Update @tasklist.md:
  - Mark completed subtasks with [x]
  - Update iteration progress
  - Set completion date
- Report results with test outcomes

### 4. Commit & Confirm
- Make commit: `feat: Iteration N - [brief description]`
- **WAIT FOR CONFIRMATION** before next iteration

## Communication Rules

**Before implementation:**
```
"Propose implementing [task] as follows: [code/architecture]"
"Confirm to proceed?"
```

**After completion:**
```
"Iteration N completed. Tests: [results]"  
"Ready for next iteration?"
```

## Required Flow

```
Plan → Propose → Confirm → Implement → Test → Report → Commit → Confirm → Next
```

## Prohibited Actions

- ❌ Implement without confirmation
- ❌ Skip steps from @tasklist.md  
- ❌ Add "future" functionality
- ❌ Use complex architecture
- ❌ Move to next iteration without approval
- ❌ Commit code that breaks existing tests

## Files to Track

- **@tasklist.md** - main plan and progress
- **@vision.md** - technical principles
- **@conventions.md** - development standards

---

*Every step requires confirmation. No exceptions.*