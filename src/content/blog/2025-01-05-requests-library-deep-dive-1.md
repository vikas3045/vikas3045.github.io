---
title:  "Requests Library Deep Dive - 1"
author: Vikas Sharma
date:   2025-01-05 21:28:00 +0800
categories: [sticky-notes, requests-sticky-notes]
show_preview: false
---

Continuing my exploration of the `requests` library, I thought it would be helpful to first review some of its most commonly used APIs before diving into the source code. Here's a quick overview:

### Core Methods
The library provides **7 main methods**, all of which return an instance of the `Response` object:

1. **`requests.request(method, url, **kwargs)`**  
   The most flexible method, allowing you to specify the HTTP method (`GET`, `POST`, `PUT`, `DELETE`, etc.) and additional parameters.

2. **`requests.get(url, params=None, **kwargs)`**  
   Sends a GET request to the specified URL. Query parameters can be passed as a dictionary to the `params` argument.

3. **`requests.post(url, data=None, json=None, **kwargs)`**  
   Sends a POST request. You can include form data or JSON in the request body.

4. **`requests.put(url, data=None, **kwargs)`**  
   Sends a PUT request, typically used for updating resources.

5. **`requests.patch(url, data=None, **kwargs)`**  
   Sends a PATCH request for partial updates to a resource.

6. **`requests.delete(url, **kwargs)`**  
   Sends a DELETE request to remove a resource.

7. **`requests.head(url, **kwargs)`**  
   Sends a HEAD request, retrieving only headers without the response body.

---

### Common Parameters
Across these methods, several parameters are frequently used:

- **`url`**: The target URL for the request.  
- **`params`**: Query parameters, passed as a dictionary (commonly used with GET requests).  
- **`data`**: The body of the request, typically used with POST or PUT.  
- **`json`**: A JSON-serializable object to include in the request body.  
- **`headers`**: Custom HTTP headers to send with the request.  
- **`cookies`**: Cookies to include with the request.  
- **`files`**: Files for multipart file uploads.  
- **`auth`**: Authentication credentials.  
- **`timeout`**: Specifies the maximum time to wait for a response before raising a timeout exception.  
- **`allow_redirects`**: Whether to follow HTTP redirects (defaults to `True`).  

---

This overview serves as a foundation for understanding the `requests` library before delving into its implementation details.

References: https://requests.readthedocs.io/en/latest/api/#main-interface
