---
layout: post  
title: "Requests Library Deep Dive - 10"  
author: Vikas Sharma  
date: 2025-01-16 22:15:00 +0800  
categories: [sticky-notes, requests-sticky-notes]  
show_preview: false  
---

Continuing the study of the `requests` module. Today, I am diving into `requests/status_codes.py`, a relatively small but useful module that deals with HTTP status codes. It maps numerical HTTP status codes to their textual representations, making the library more human-readable and user-friendly.

## Key Concepts in `requests/status_codes.py`
### Purpose
This module provides a dictionary and helper functions for working with HTTP status codes. It makes it easier to understand and handle status codes by providing textual descriptions.

### The `codes` Dictionary
Maps HTTP status codes (e.g., `200`, `404`) to their textual descriptions (e.g., `ok`, `not_found`).

```python
codes = LookupDict(name='status_codes')

# example entries
_codes = {
    200: 'ok',
    404: 'not_found',
    500: 'internal_server_error',
}

for code, phrase in _codes.items():
    codes[phrase] = code
    codes[code] = [phrase]
```

Two-way mapping:
You can look up either by number or by name:
```python
from requests.status_codes import codes
codes[200]
# 'ok'
codes['not_found']
# 404
```

### The `LookupDict` Class
A custom dictionary implmentation that provides case-insensitive lookup for textual representations of status codes.

Key methods:
- `__getitem__`: Enables standard dictionary access.
- `get`: Fetches a value while handling missing keys gracefully.

Example:
```python
class LookupDict(dict):
    def __init__(self, name=None):
        self.name = name

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def get(self, key, default=None):
        return self[key] if key in self else default
```

### Convenience in Code
Using this module makes it easier to write clear and readable code when dealing with status codes:

```python
import requests

response = requests.get('https://example.com')

if response.status_code == requests.codes.ok:
    print("The request was successful!")
elif response.status_code == requests.codes.not_found:
    print("The requested resource was not found.")
```