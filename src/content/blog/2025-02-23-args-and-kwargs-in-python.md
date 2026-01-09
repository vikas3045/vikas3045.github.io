---
title: "Use of `args` and `kwargs` in Python"  
author: Vikas Sharma  
date: 2025-02-23 15:12:00 +0800  
categories: [sticky-notes]  
show_preview: false  
---

`*args` and `**kwargs` allows us to pass *multiple arguments* and *keyword arguments* to a function.

## args
The use of `*` in front of a collection will unpack it. This interesting behaviour can be used to make your function accept any arbitrary number of parameters.

For example, let's consider a function that concatenates the words passed into a complete sentence separated by space.

1. First case, where you want to support two words

```python
def change_words_to_sentence(word_1, word_2):
    return f'{word_1} {word_2}'

# change_words_to_sentence('Hi', 'there')
# output: 'Hi there'
```

2. Now let's say you to support more than two words,

```python
def change_words_to_sentence(words):
    return ' '.join(words)

# change_words_to_sentence(['Hi', 'there', 'I', 'am', 'learning', 'python'])

# output: 'Hi there I am learning python'
```

3. One another possible way could be,

```python
def change_words_to_sentence(*args):
    return ' '.join(args)

# change_words_to_sentence('Hi', 'there', 'I', 'am', 'learning', 'python')

# output: 'Hi there I am learning python'
```

Point to note is the name `*args` is not important, you can use for example `*words` as well. It basically unpacks the arguments. **Unpacking operator** `*`

## kwargs
It's very similar to `args` only main difference being that it can be applied only to dictionaries.

For example,

```python
def change_words_to_sentence(*kwargs):
    return ' '.join(kwargs.values())

# change_words_to_sentence(a='Hi', b='there', c='!')

# output: 'Hi there !'
```

- Notice the use of `kwargs.values()`, it gives the list of values in the dictionary. Basically, any dictionary methods can be used on `kwargs`.
- Again, `kwargs` can be replaced by any other name of your choice. Main thing is the operator `**`.

