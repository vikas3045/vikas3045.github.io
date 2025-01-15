---
layout: post  
title: "Requests Library Deep Dive - 9"  
author: Vikas Sharma  
date: 2025-01-15 21:19:00 +0800  
categories: [sticky-notes, requests-sticky-notes]  
show_preview: false  
---

Continuing the study of the `requests` module. Today, I am diving into `requests/exceptions.py`, which defines custom exception classes. These exceptions improve error handling and debugging by providing meaningful messages specific to HTTP requests and responses.

## Key Concepts in `requests/exceptions.py`
### Purpose
`requests` uses its own set of exceptions to clearly indicate different types of errors, rather than relying on generic Python exceptions like `ValueError` or `OSError`.

### Hierarchy of Exceptions
All exceptions in `requests` inherit from `RequestException`. This allows users to catch all exceptions with a single base class if needed.

## The Base Class: `RequestException`
- This is the parent class for all exceptions in requests.
- It accepts a custom message and optionally a request or response object for additional context.

Example:
```python
class RequestException(IOError):
    def __init__(self, message, request=None, response=None):
        super().__init__(message)
        self.request = request
        self.response = response
```

## Common Exceptions
`HTTPError`
Raised when an HTTP request fails due to client-side (4xx) or server-side (5xx) errors. It’s often triggered by Response.raise_for_status().
```python
class HTTPError(RequestException):
    pass
```

`ConnectionError`
Raised when a connection to the server cannot be established.

```python
class ConnectionError(RequestException):
    pass
```

`Timeout`
Raised when a request exceeds the specified timeout.

```python
class Timeout(RequestException):
    pass
```

`URLRequired`
Raised when a URL is not provided to a request.

```python
class URLRequired(RequestException):
    pass
```

`TooManyRedirects`
Raised when the maximum number of allowed redirects is exceeded.

```python
class TooManyRedirects(RequestException):
    pass
```

`InvalidURL`
Raised when a URL is improperly formatted.

```python
class InvalidURL(RequestException):
    pass
```

## Less Common Exceptions

`ProxyError`
Raised when a request fails due to issues with a proxy server.

```python
class ProxyError(ConnectionError):
    pass
```

`SSLError`
Raised for SSL/TLS-related errors, such as certificate validation failures.

```python
class SSLError(ConnectionError):
    pass
```

`ChunkedEncodingError`
Raised when the server provides malformed chunked encoding data.

```python
class ChunkedEncodingError(RequestException):
    pass
```

`ContentDecodingError`
Raised when the response body cannot be decoded.

```python
class ContentDecodingError(RequestException):
    pass
```

## Usage in Code

Exception handling is simplified because of this module. For example:
```python
import requests

try:
    response = requests.get('https://example.com', timeout=1)
    response.raise_for_status()  # Raises HTTPError for 4xx/5xx responses
except requests.exceptions.Timeout:
    print("Request timed out.")
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
except requests.exceptions.RequestException as err:
    print(f"An error occurred: {err}")

```