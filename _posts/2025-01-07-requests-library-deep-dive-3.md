---
layout: post  
title: "Requests Library Deep Dive - 3"  
author: Vikas Sharma  
date: 2025-01-07 22:07:00 +0800  
categories: [sticky-notes, requests-sticky-notes]  
show_preview: false  
---
### Key Points:
#### High-Level Structure
The requests library is organized into several core modules that handle different parts of HTTP functionality. Here's a quick overview:

1. `requests/__init__.py`
This file defines the user-facing API of the library, such as requests.get, requests.post, etc.
It imports functionality from other internal modules and exposes them as a unified interface.
2. `requests/models.py`
Defines classes like Request and Response, which represent HTTP requests and responses respectively.
Handles data serialization, headers, and response content.
3. `requests/sessions.py`
Manages Session objects, which allow for persistent settings (e.g., headers, cookies) across multiple requests. Provides methods like Session.get and Session.post.
4. `requests/adapters.py`
Implements the HTTPAdapter class, which handles the low-level connection pooling and transports.
5. `requests/api.py`
A thin wrapper around Session methods to provide the requests.get, requests.post, etc., functions.
6. `requests/utils.py`
Contains helper functions used across the library (e.g., URL manipulation, encoding detection).
7. `requests/exceptions.py`
Defines custom exception classes used by the library (e.g., RequestException, HTTPError).
8. `requests/status_codes.py`
mapping of HTTP status codes to their textual representation (e.g., 200: 'OK').
9. `requests/cookies.py`
Manages cookies for HTTP requests.
10. `requests/hooks.py`
Implements hooks, allowing users to customize behavior (e.g., modifying a response object before it’s returned).