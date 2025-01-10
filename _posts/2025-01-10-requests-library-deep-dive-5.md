---
layout: post  
title: "Requests Library Deep Dive - 5"  
author: Vikas Sharma  
date: 2025-01-10 23:27:00 +0800  
categories: [sticky-notes, requests-sticky-notes]  
show_preview: false  
---

Continuing the study of the `requests` module. Today, I am diving into `requests/sessions.py`, one of the most important modules in the library. It handles persistent settings and provides the reusable `Session` object.

## Key Concepts in `requests/sessions.py`
### The Session Class
A `Session` object allows you to:
- Persist settings like headers, cookies, and authentication across multiple requests.
- Maintain a pool of connections for better performance (connection reuse).

**Key Attributes of Session:**

- `headers`: A default dictionary of headers sent with every request.
- `cookies`: Manages cookies for the session.
- `auth`: Handles authentication (e.g., HTTP Basic Auth).
- `adapters`: Maps schemes (like http or https) to transport adapters (defined in `adapters.py`).

### Session.request Method
The core method that sends a prepared HTTP request.

Signature:
```python
def request(self, method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=None, ...):
    # Logic to send the request
```
**Key Steps Inside `Session.request`:**

- Merge Settings:
Combine session-level settings (like headers and cookies) with request-specific settings.
```python
merged_headers = self.headers.copy()
if headers:
    merged_headers.update(headers)
```
- Prepare the Request
Create a Request object and prepare it into a PreparedRequest using its prepare method.
```python
req = Request(
    method=method.upper(),
    url=url,
    headers=merged_headers,
    params=params,
    data=data,
    cookies=cookies,
    auth=auth,
    ...
)
prep = req.prepare()
```
- Send the Request
The prepared request is sent using the send method (delegates to an adapter).
```python
resp = self.send(prep, stream=stream, timeout=timeout, verify=verify, cert=cert, proxies=proxies)
```
- Handle Response
Hooks and redirects are processed if applicable.
Return the final Response object.

### Session.send Method
The `send` method sends a `PreparedRequest` and returns a `Response` object.

**Key Responsibilities:**

- Determines the appropriate transport adapter (e.g., HTTPAdapter) based on the request’s URL scheme (http or https).
- Calls the adapter’s send method to handle the actual I/O.
Example:

```python
def send(self, request, **kwargs):
    adapter = self.get_adapter(url=request.url)
    return adapter.send(request, **kwargs)
```

### Connection Pooling
The `Session` class uses transport adapters (from `adapters.py`) for connection pooling and reusing TCP connections, which improves performance for multiple requests to the same host.

Example of Using a Session:
```python
with requests.Session() as session:
    session.headers.update({'Authorization': 'Bearer TOKEN'})
    response = session.get('https://api.example.com/data')
    print(response.json())
```
The `Authorization` header is reused for all requests made with the session.
The same connection is reused for performance.
This is where the magic of persistent settings and efficient networking happens in `requests.sessions.py`!