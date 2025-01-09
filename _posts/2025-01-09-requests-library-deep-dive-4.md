---
layout: post  
title: "Requests Library Deep Dive - 4"  
author: Vikas Sharma  
date: 2025-01-09 23:04:00 +0800  
categories: [sticky-notes, requests-sticky-notes]  
show_preview: false  
---
Continuing to study the `requests` module. Today, trying to go through `requests/models.py`, which defines the foundational classes for representing HTTP requests and responses.

## Key Concepts in `requests/models.py`
### Core Classes
Two critical classes in this module are:
`Request`: Represents an HTTP request.
`Response`: Represents an HTTP response.
1. **Request Class**
The Request class encapsulates all the data needed to prepare and send an HTTP request.

## Key Attributes:

- method: The HTTP method (e.g., 'GET', 'POST').
- url: The URL to which the request is made.
- headers: A dictionary of HTTP headers.
- params: Query parameters for the URL.
- data / json: The request payload (body).
Example Constructor:

```python
def __init__(self, method, url, headers=None, files=None, data=None, params=None, json=None, ...):
    self.method = method.upper()
    self.url = url
    self.headers = headers or {}
    self.params = params or {}
    self.data = data
    self.json = json
    ...
```
Preparing a Request:

The prepare method converts the Request into a PreparedRequest object, which is a fully-formed request ready to be sent.
```python
def prepare(self):
    return PreparedRequest().prepare(
        method=self.method,
        url=self.url,
        headers=self.headers,
        files=self.files,
        data=self.data,
        params=self.params,
        json=self.json,
    )
```
2. **Response Class**
The Response class holds the result of an HTTP request.

Key Attributes:

- status_code: The HTTP status code (e.g., 200, 404).
- headers: Response headers.
- text: The response body as a string (decoded).
- content: The raw response body as bytes.
- json: Decodes the response body as JSON (if applicable).
Example Constructor:

```python
def __init__(self):
    self._content = False
    self.status_code = None
    self.headers = CaseInsensitiveDict()
    self.url = None
    self.reason = None
    self.elapsed = None
    self.history = []
```
Methods:

- `raise_for_status`: Raises an exception for HTTP error responses:
```python
def raise_for_status(self):
    if 400 <= self.status_code < 600:
        raise HTTPError(f'{self.status_code} Error: {self.reason}')
```
- `json`: Parses the body as JSON:
```python
def json(self, **kwargs):
    return json.loads(self.text, **kwargs)
```
Interaction Between Request and Response

A Request object is prepared using prepare, resulting in a PreparedRequest.
The Session sends the PreparedRequest and receives a Response object.
The Response contains all the information about the server’s reply to the request.
This module is where a lot of abstraction occurs, making HTTP requests intuitive for end users.