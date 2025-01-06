---
layout: post  
title: "Requests Library Deep Dive - 2"  
author: Vikas Sharma  
date: 2025-01-06 22:18:00 +0800  
categories: [sticky-notes, requests-sticky-notes]  
show_preview: false  
---

File reviewed: [api.py](https://github.com/psf/requests/blob/main/src/requests/api.py)  

### Key Points:
- The main function used is `request(method, url, **kwargs)`.
- All other methods internally call this function.
- The `request` function's implementation is straightforward:

```python
# By using the 'with' statement, we ensure the session is closed, 
# avoiding open sockets that could trigger a ResourceWarning or appear as a memory leak.
with sessions.Session() as session:
    return session.request(method=method, url=url, **kwargs)
```

- A session instance is created, and the request method is called on it.
- Next steps: Study the sessions module.
