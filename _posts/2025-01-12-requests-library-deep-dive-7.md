---
layout: post  
title: "Requests Library Deep Dive - 7"  
author: Vikas Sharma  
date: 2025-01-12 22:03:00 +0800  
categories: [sticky-notes, requests-sticky-notes]  
show_preview: false  
---

Continuing the study of the `requests` module. Today, I am diving into `requests/utils.py`, which contains common utility functions that are used throughout the library.

## Key Concepts in `requests/utils.py`
### Purpose
This module provides helper functions for various tasks, such as:
- Parsing and formatting urls.
- Encoding/Decoding data.
- Inspecting request/reponse content.

### Url related utilities
`to_native_string`: Ensures that strings are in the correct format for URLs (unicode for Python 3 and bytes for Python 2).

```python
def to_native_string(string, encoding='ascii'):
    if isinstance(string, bytes):
        return string.decode(encoding)
    return string
```

`get_environ_proxies`: Fetches proxy settings from environment variables like `HTTP_PROXY` and `HTTPS_PROXY`.

```python
def get_environ_proxies(url, no_proxy=None):
    proxies = {}
    if should_bypass_proxies(url, no_proxy=no_proxy):
        return proxies
    ...
    return proxies
```
This function ensures that requests respects system-wide proxy configurations.

`parse_url`: Parses a URL into its components (scheme, host, path etc.) using `urlparse` from python's `urllib.parse`.

### Encoding Utilities
`get_encoding_from_headers`: Detect encoding of a response from its `Content-Type` headers.

```python
def get_encoding_from_headers(headers):
    content_type = headers.get('content-type')
    if not content_type:
        return None
    match = _charset_from_content_type(content_type)
    return match.lower() if match else None
```

`get_json_utf`: Attempts to guess the encoding of a JSON response if not explicitly specified.

### Content-Type Utilities
`get_content_type`: Determines the MIME type of a file based on its extension (e.g., `.html` -> `text/html`).

### Request/Response Inspection Utilities
`check_header_validity`: Validates the format of HTTP headers to ensure they conform to RFC standards.

```python
def check_header_validity(header):
    if not isinstance(header, str) or '\n' in header or '\r' in header:
        raise InvalidHeader("Header value must be a string and must not contain newlines.")
```

`parse_header_links`: Parses `Link` headers (commonly used in APIs for pagination)
```python
def parse_header_links(value):
    links = []
    replace_chars = ' \'"'
    for val in value.split(","):
        ...
        links.append({"url": url, "rel": rel})
    return links
```