---
layout: post
title:  "217. Contains Duplicate"
author: Vikas Sharma
date:   2023-09-16 15:53:00 +0530
categories: [technical, leetcode, blind-75]
image: assets/images/l-contains-duplicate.jpeg
featured: true
show_preview: false
---

<p>
    <a href="https://leetcode.com/problems/contains-duplicate/" target="_blank">Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.</a>
</p>

```
Example 1:
Input: nums = [1,2,3,1]
Output: true

Example 2:
Input: nums = [1,2,3,4]
Output: false

Example 3:
Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true

Constraints:
1 <= nums.length <= 105
-109 <= nums[i] <= 109
```

## Intuition

### First thoughts
In order to solve this question in a brute-force manner, we'll have to:
- loop through all the elements and for each element
    - we need to check against all the remaining elements if that element is present or not.

This approach has:
- run time complexity of `O(n**2)` (as we have nested loops)
- space complextity of `O(1)` (since we don't need to allocate any extra storage)

### Further thoughts
Can we do better than `O(n**2)`?

- Well, if we use hash set to store all the elements of the given array, then we should be able to check the existence of any element in constant time.
- Thus, we can just loop through all the elements and then for each element we can check in constant time whether the element exists or not.

### Final approach
- Initialize an empty hashset by name `lookup`
- Loop through all the elements of given array
    - if that element is not present in `lookup`, then let's add it and move ahead
    - otherwise, (i.e. element already exists, ***duplicated spotted!***)
        - return `True`
- return `False`, as we exhausted the given array and didn't find any duplicate.
- Time complexity: `O(n)` (since we only process elements in a single loop)
- Space complexity: `O(n)` (since we create a new hashset to store all the elements of given array)


### Python code
```python
class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        lookup = set()
        for x in nums:
            if x in lookup:
                return True
            lookup.add(x)
        return False
```
    
