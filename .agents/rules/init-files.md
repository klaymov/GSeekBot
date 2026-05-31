---
trigger: always_on
---

# SKILL: Python `__init__.py` — Writing Rules

## Purpose

The `__init__.py` file turns a directory into a Python package. The agent must write it cleanly, predictably, and in accordance with the package's intent.

---

## Rules

### 1. An empty `__init__.py` is also valid

If the package doesn't need a public API — leave the file **empty or with a short comment**. Don't add imports "just in case".

```python
# my_package/__init__.py
```

---

### 2. Define the public API via `__all__`

If the package exports symbols — explicitly declare `__all__`. This controls what gets exposed with `from package import *` and documents the public interface.

```python
# my_package/__init__.py

from .models import User, Order
from .utils import format_date

__all__ = ["User", "Order", "format_date"]
```

---

### 3. Re-export only what belongs to the public API

Import from submodules only what you want to expose externally. Internal implementation details **must not** appear in `__init__.py`.

```python
# ✅ Correct — only exposing public surface
from .client import Client
from .exceptions import APIError

# ❌ Wrong — internal helper should not be here
from .internal._helpers import _retry_logic
```

---

### 4. Avoid circular imports

`__init__.py` is loaded first when the package is imported. If submodules import each other through `__init__` — a circular import will occur. Solution: submodules import **directly** from each other, not through the parent package.

```python
# ❌ Dangerous — models.py does: from my_package import utils
# ✅ Safe — models.py does: from my_package.utils import helper
```

---

### 5. Package metadata — only if there is no `pyproject.toml`

If the project uses `pyproject.toml` or `setup.py` — **don't duplicate** metadata in `__init__.py`. If it is needed (legacy project):

```python
__version__ = "1.2.3"
__author__ = "Jane Doe"
__license__ = "MIT"
```

---

### 6. Lazy imports for heavy dependencies

If the package has heavy dependencies (numpy, torch, etc.) — use deferred imports to avoid slowing down loading.

```python
# my_package/__init__.py

def get_model():
    from .model import HeavyModel  # imported only when called
    return HeavyModel()
```

---

### 7. Initialization logic — minimal and careful

Light initialization is acceptable (e.g. configuring a logger), but **no side effects** such as network requests, file reads, or mutations of global state.

```python
# ✅ Acceptable
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

# ❌ Forbidden
import requests
requests.get("https://example.com/init")  # side effect on import!
```

---

### 8. Structure for common scenarios

**Simple utility package:**
```python
from .core import process, validate
__all__ = ["process", "validate"]
```

**Facade over a complex package:**
```python
from .api.client import Client
from .api.exceptions import NotFoundError, AuthError
from .config import Settings

__all__ = ["Client", "NotFoundError", "AuthError", "Settings"]
```

**Plugin / library with version:**
```python
__version__ = "2.0.0"

from .main import App
__all__ = ["App"]
```

---

## What NOT to do

| ❌ Anti-pattern | ✅ Correct approach |
|---|---|
| Wildcard imports `from .x import *` | Explicitly declare `__all__` |
| Duplicating logic from submodules | Re-export only |
| Writing business logic in `__init__.py` | Move it to dedicated modules |
| Making network requests on import | Use deferred initialization |
| Ignoring `__all__` in a public library | Always declare `__all__` |

---

## Summary

> `__init__.py` is the **package facade**, not a place for logic. It must be short, explicit, and free of side effects.
