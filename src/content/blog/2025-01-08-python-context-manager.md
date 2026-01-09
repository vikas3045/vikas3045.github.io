---
title: "TIL: Python context manager"  
author: Vikas Sharma  
date: 2025-01-08 17:26:00 +0800  
categories: [sticky-notes, til]
show_preview: false  
---

While reviewing the `requests` library's codebase, I found myself diving into yet another rabbit hole. A couple of internet searches later, I had gained some foundational understanding of the concept I encountered, which I decided to capture under my `TIL` (Things I Learned Today) series.

### Discovery: `__enter__` and `__exit__`
During my code-reading exercise, I came across two dunder (double underscore) methods: `__enter__` and `__exit__`. These were new to me, but I quickly learned their importance in Python's built-in [Context Manager](https://docs.python.org/3/reference/datamodel.html#context-managers) mechanism.

### What is a Context Manager?
Context managers in Python are used to manage resources efficiently. They handle the setup and teardown logic required when working with resources such as files, network connections, or database cursors. The `with` statement is the idiomatic way to use context managers.

For example, consider file operations in Python:

```python
with open('filename') as file:
    file.read()
```

Under the hood, the `with` statement ensures that the file object is properly allocated and released, even if an exception occurs during execution. The equivalent code using try and finally would look like this:

```python
file = open('filename')
try:
    file.read()
finally:
    file.close()
```
Really amazing to see the amount of boilerplate this reduces.

### Custom Context Managers

The magic behind context managers lies in the `__enter__` and `__exit__` methods. By defining these methods in a class, you can create custom context managers. Here's an example from the requests library, specifically in the [sessions.py](https://github.com/psf/requests/blob/23540c93cac97c763fe59e843a08fa2825aa80fd/src/requests/sessions.py#L451-L455) file:

```python
class Session:
    '''
    Omitting other sections for brevity. Refer to the link above
    to view the complete code.
    '''
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
```

This implementation allows the Session class to be used with the `with` keyword, like so:

```python
with Session() as session:
    return session.request(method=method, url=url, **kwargs)
```

In this example, the `__enter__` method initializes the context and returns the Session instance, while the `__exit__` method ensures that the session is properly closed, even if an exception occurs.


### Handling exceptions in `__exit__`
The `__exit__` method can also handle exceptions raised within the context block. Its signature includes three arguments:

`exc_type`: The exception type.<br/>
`exc_value`: The exception instance.<br/>
`traceback`: The traceback object.<br/>

If the __exit__ method returns `True`, it suppresses the exception. Here's an example:

```python
class MyContextManager:
    def __enter__(self):
        print("Entering context")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"Exception caught: {exc_value}")
            return True  # Suppress the exception
        print("Exiting context")

# Usage
with MyContextManager() as cm:
    print("Inside context")
    raise ValueError("Something went wrong!")
print("Outside context")
```
```zsh
# Output
Entering context
Inside context
Exception caught: Something went wrong!
Outside context
```
