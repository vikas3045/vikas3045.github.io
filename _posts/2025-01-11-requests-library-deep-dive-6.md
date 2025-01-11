---
layout: post  
title: "Requests Library Deep Dive - 6"  
author: Vikas Sharma  
date: 2025-01-11 23:07:00 +0800  
categories: [sticky-notes, requests-sticky-notes]  
show_preview: false  
---

Continuing the study of the `requests` module. Today, I am diving into `requests/adapters.py`, which implements the low-level connection management and is crucial for handling HTTP requests efficiently.

## Key Concepts in `requests/adapters.py`
### The HTTPAdapter Class
The `HTTPAdapter` class is responsible for:
- Handling connections (e.g., opening, reusing and closing).
- Managing retries and timeouts.
- Sending the actual http requests using `urllib3`, which is a dependency of `requests`.

**Key Attributes of Session:**

- `poolmanager`: Manages connection pools for reusing the connections to the same host.
- `max_retries`: Defines how many times to retry a failed request.
- `timeout`: Sets a default timeout for requests if not provided explicitly.
```python
def __init__(self, pool_connections=10, pool_maxsize=10, max_retries=3, pool_block=False):
    self.max_retries = max_retries
    self.poolmanager = PoolManager(
        num_pools=pool_connections,
        maxsize=pool_maxsize,
        block=pool_block,
    )
```
- `PoolManager` is a feature of `urllib3` that handles connection pooling.

### Sending a request
The `send` method is the core of the `HTTPAdapter` class. It sends a `PreparedRequest` and returns a `Response` object.

**Key Steps Inside `send`:**

- Get connection:
A connection from a pool is fetched using `PoolManager`.
```python
conn = self.poolmanager.connection_from_url(request.url)
```
- Make the request:
The actual HTTP request is made via `conn.urlopen`, which comes from `urllib3`.
```python
response = conn.urlopen(
    method=request.method,
    url=request.url,
    body=request.body,
    headers=request.headers,
    retries=self.max_retries,
    timeout=timeout,
)
```
- Wrap the response:
The raw `urllib3` response is wrapped in a `Response` object.
```python
response = self.build_response(request, response)
```

### Adapter lifecycle
- Each `Session` object has a dictionary mapping schemes (like `http` and `https`) to `HTTPAdapter` instances:

```python
self.adapters = {'http://': HTTPAdapter(), 'https://': HTTPAdapter()}
```
-  When a `Session` sends a request, it looks up the adapter for the request's URL scheme.
```python
def get_adapter(self, url):
    for prefix, adapter in self.adapters.items():
        if url.lower().startswith(prefix):
            return adapter
```

### Why Connection Pooling matters
- Without connection pooling, every HTTP request would require a new TCP connection, which is expensive.
- By reusing TCP connections for requests to the same host, the `HTTPAdapter` significantly improves performance, especially for APIs or websites with multiple requests.