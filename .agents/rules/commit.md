---
trigger: always_on
description: Main project rules
---

## Auto-commit after finishing work

After completing any changes to the code, **always** commit:

1. First, run pre-commit to check and auto-fix:
   ```bash
   uv run pre-commit run --all-files
   ```

2. If pre-commit made changes or fixed errors, add them:
   ```bash
   git add -A
   ```

3. Commit with a descriptive message:
   ```bash
   git commit -m “type: short description of changes in English”
   ```

### Commit types:
- `feat:` — new functionality
- `fix:` — bug fix
- `refactor:` — code refactoring
- `docs:` — changes to documentation
- `style:` — formatting, code style
- `chore:` — technical changes (dependencies, configurations)

Don't ignore any errors that pre-commit throws! You must fix all errors if there are any!
