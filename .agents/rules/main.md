---
trigger: always_on
---

# Code Style Rules

Імпорти завжди мають бути уверху файлу!

## Comments and Documentation

### Comment Format
- **Docstrings** (function/class descriptions): Use triple quotes `""" """`
- **Inline comments** (in code): Use `#` for single-line comments
- **English only**: All comments and docstrings must be written in English

### Minimize Unnecessary Comments
- **Keep code self-explanatory**: Write clean, readable code that doesn't need comments to explain what it does
- **Comment only when necessary**: Add comments ONLY for:
  - Complex algorithms or logic that isn't immediately obvious
  - Non-intuitive solutions or workarounds
  - Important business logic or edge cases
  - Confusing or tricky code that cannot be simplified
- **Avoid redundant comments**: Don't comment on obvious code (e.g., `# increment counter` for `counter += 1`)
- **No function/method descriptions for simple code**: Skip docstrings for straightforward functions where the name and parameters clearly indicate the purpose
- **Focus on "why", not "what"**: If you must comment, explain WHY the code does something, not WHAT it does (the code itself shows what)

### Examples

❌ **Bad** (unnecessary comments):
```python
def send_message(text: str):
    """This function sends a message."""
    # Send the message to the user
    await bot.send_message(chat_id, text)
```

✅ **Good** (no comments needed for simple functions):
```python
def send_message(text: str):
    await bot.send_message(chat_id, text)
```

✅ **Good** (docstring justified for complex logic):
```python
def calculate_priority(user_id: int) -> int:
    """
    Calculate user priority using XOR hash distribution.

    Uses XOR hash to distribute users evenly across priority buckets
    while maintaining deterministic assignment for the same user.
    """
    return (user_id ^ 0x5bd1e995) % MAX_PRIORITY
```

✅ **Good** (inline comment for non-obvious code):
```python
def process_data(data: list):
    # Skip first element as it's always the header row
    for item in data[1:]:
        process_item(item)
```
