---
layout: post
title:  "How to solve Sliding Window Problems"
author: Vikas Sharma
date:   2023-10-25 13:12:00 +0530
image: assets/images/sliding-window-banner.jpeg
categories: [technical]
featured: true
---

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@i_vikassharma">
<meta name="twitter:creator" content="@i_vikassharma">
<meta name="twitter:title" content="How to solve Sliding Window Problems?">
<meta name="twitter:description" content="A comprehensive guide to solving problems with the Sliding Window Technique. Learn the fundamentals and real-world applications. #SlidingWindow #ProblemSolving">
<meta name="twitter:image" content="https://vikassharma.me/assets/images/sliding-window-banner.jpeg">

## Table of Contents

- [Introduction](#introduction)
- [How do you identify them?](#how-do-you-identify-them)
- [General Mental Model](#general-mental-model)
  - [1. Expand](#1-expand)
  - [2. Shrink](#2-shrink)
  - [3. Record the Candidate Result](#3-record-the-candidate-result)
- [Code Template](#code-template)
- [Problem Statement](#problem-statement)
- [Explanation and Solution](#explanation-and-solution)
- [Types](#types)
  - [Fixed Size Window](#fixed-size-window)
  - [Variable Size Window](#variable-size-window)
    - [1. Left Catches Up with Right](#1-left-catches-up-with-right)
    - [2. Multiple Possible Lefts](#2-multiple-possible-lefts)
- [Difference from Other General Optimizations](#difference-from-other-general-optimizations)
- [Where Not to Apply Sliding Window Technique](#where-not-to-apply-sliding-window-technique)
- [Conclusion](#conclusion)

## Introduction

**Sliding window** is a common technique/pattern used to solve many different problems in computer science. In fact, its one of the most frequently asked type of problem during software engineering interviews.

This blog post aims to provide clarity about these kind of questions and also aid the readers with necessary tools (mental model and coding templates) needed to efficiently solve the problems involving this technique.

## How do you identify them?

There are a few key things to look for when identifying problems where the sliding window technique can be applied:

1. The problem involves a **sequence of data points** such as arrays, list of elements or string.
2. Problem is specifically asking about finding some subrange in that array/string, like a longest, shortest or target value.
3. There is a constraint on the size of the window. Sometimes, its simple as being clearly mentioned as "k-sized window" or little more abstract in nature like "longest substring without repeating characters".

## General mental model

At the very fundamental level, sliding window technique involves: 

1. Dividing a sequence of data points into overlapping subsets of fixed size (or variable size based on certain constraint on the window size), and then performing some operation on each subset.
2. The window is then moved one position to the right, and the operation is performed on the new subset.
3. This process is repeated until the window reaches the end of the sequence.

Let's try to formalise these fundamental steps as follows:
### 1. Expand
As the name suggests, in this step we are just trying to expand the window being observed at the right end. While there are few different ways to do that, let's stick with good old `for` loop at the moment. We'll call our iterator as `right` to mimic the right end of our conceptual window (Sliding window: well it slides on the ends, so nothing fancy)

### 2. Shrink
As we discussed earlier, there would be some kind of constraint on the size of the window. This constraint can be simply a constraint of let's say "k-sized window" or little more abstract in nature like "longest substring without repeating characters". Essentially this constraint/condition will help us to evaluate the validity of the window being observed.
This particular step just refers to the action of shrinking the window from its left end towards right so that we can maintain the valid window (that satisfies the constraint on size)

### 3. Record the candidate result
Once we have a valid window, then all that is left for us is to record the candidate result from the window being observed. In most of the cases, we'll have no benefit of storing all the possible results in memory. Instead, we'll often store the best-result-so-far and keep on comparing this so called best-result-so-far with next candidate result of any future windows.

Following template captures the above idea at a high level
### Code template

```python
def fn(arr):
    left, result, cur_win = 0, 0, 0

    for right in range(len(arr)):
	    # 1. Expand
        # do logic here to add arr[right] to curr_win

		# 2. Shrink
        while WINDOW_CONDITION_BROKEN:
            # remove arr[left] from curr_win
            left += 1

		# 3. Record the candidate result
        # update result
    
    return result
```

Let's quickly solve a simple problem using sliding window pattern to reinforce our learning.

### Problem statement

You are given an array `prices` where `prices[i]` is the price of a given stock on the `ith` day.

You want to maximize your profit by choosing a **single day** to buy one stock and choosing a **different day in the future** to sell that stock.

Return _the maximum profit you can achieve from this transaction_. If you cannot achieve any profit, return `0`.

**Example 1:**

**Input:** prices = [7,1,5,3,6,4]
**Output:** 5

**Explanation:** Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

**Example 2:**

**Input:** prices = [7,6,4,3,1]
**Output:** 0

**Explanation:** In this case, no transactions are done and the max profit = 0.

### Explanation and Solution

- We fix a buy price, in this case index=0.
- We start with start expanding with the next possible selling price.
- For each potential selling price, we check if this window is still profitable i.e. `prices[sell] >= prices[buy]`. If that's not the case, then it means that we can do better in terms of selecting our buy price.
- Therefore, we move our buy price pointer to sell price directly (as we would have processed all intermediate cases already).
- This problem is of category <a href="#1-left-catches-up-with-right">Left catches up with right</a> explained later in this post.
- Following code implements this logic for more clarity.

```python
def maxProfit(prices: List[int]) -> int:
	buy, maxProfit = 0, 0
	for sell in range(len(prices)):
		# expand
		# no action needed - we are just expanding our observed window
		
		# shrink
		if prices[sell] < prices[buy]:
			buy = sell
		
		# record candidate result and compare it against best we got so far
		maxProfit = max(maxProfit, prices[sell]-prices[buy])

return maxProfit
```
## Types
### Fixed size window

**Example(s)**:
- <a href="https://leetcode.com/problems/sliding-window-maximum/description/" target="_blank">Sliding window maximum</a>

### Variable size window
#### 1. Left catches up with right

**Example(s)**:
- <a href="https://vikassharma.me/leetcode-121-best-time-to-buy-and-sell-stock/" target="_blank">Best time to buy and sell stock</a>
- <a href="https://leetcode.com/problems/longest-repeating-character-replacement" target="_blank">Longest repeating character replacement</a>
- <a href="https://leetcode.com/problems/permutation-in-string/" target="_blank">Permutation in string</a>

#### 2. Multiple possible lefts

**Example(s)**:
- <a href="https://leetcode.com/problems/longest-substring-without-repeating-characters/" target="_blank">Longest substring without repeating characters</a>
- <a href="https://leetcode.com/problems/minimum-window-substring/description/" target="_blank">Minimum window substring</a>

## Difference from other general optimizations

The sliding window technique offers a specific approach to problem-solving, distinct from other general optimization strategies. It excels in scenarios where you need to efficiently analyze a subset of data. While dynamic programming and other techniques have their strengths, sliding windows are particularly valuable when processing data sequentially.
Also, there has to be a constraint on window size. Otherwise, we won't be able to shrink or expand window linearly.

## Where not to apply Sliding Window technique 

While the sliding window technique is a versatile tool, it's not always the best choice. Avoid using it in situations where the problem's requirements do not align with the window concept or when alternative strategies, such as hash tables or prefix sums, are more efficient.

## Conclusion

In the realm of problem-solving, the sliding window technique stands as a versatile and efficient approach, particularly when dealing with sequences of data. This blog post has shed light on the fundamental principles behind this technique, from identifying suitable problems to constructing a code template for implementation.

The key takeaways are:

- The sliding window technique involves dividing a sequence into overlapping subsets and iteratively performing operations on these subsets.
- It excels in scenarios with constraints on window size, such as finding the longest substring without repeating characters or analyzing stock price trends.
- While sliding windows offer a powerful strategy, remember that it's not a one-size-fits-all solution. Be mindful of situations where alternative techniques like hash tables or dynamic programming might be more effective.

By mastering the sliding window technique and recognizing when to apply it, you'll add a valuable tool to your problem-solving toolkit, making those tricky software engineering interview questions a breeze. So go ahead, slide through those problems and unlock solutions with ease!