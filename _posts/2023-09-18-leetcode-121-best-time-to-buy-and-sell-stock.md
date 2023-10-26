---
layout: post
title:  "121. Best Time to Buy and Sell Stock"
author: Vikas Sharma
date:   2023-09-18 13:01:00 +0530
image: assets/images/l-buy-and-sell.jpeg
categories: [technical, leetcode, blind-75, sliding-window]
featured: true
show_preview: false
---

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@i_vikassharma">
<meta name="twitter:creator" content="@i_vikassharma">
<meta name="twitter:title" content="121. Best Time to Buy and Sell Stock">
<meta name="twitter:description" content="How to solve leetcode problem no. 121 best-time-to-buy-and-sell-stock">
<meta name="twitter:image" content="https://vikassharma.me/assets/images/l-buy-and-sell.jpeg">

<p>
    <a href="https://leetcode.com/problems/best-time-to-buy-and-sell-stock/" target="_blank">
        You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.
    </a>
</p>

```
Example 1:

Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.
Example 2:

Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.
 

Constraints:

1 <= prices.length <= 105
0 <= prices[i] <= 104
```

## Intuition

### First thoughts
In order to solve this question in a brute-force way, we'll have to:
- loop through all the elements and for each element (i.e. selecting the current element as our buying price):
    - we need to check against all the possible selling points (i.e. all the prices after our chosen buying price).
        - calculate if we are going to make any profit with the pair of chosen `buy price` and `sell price`. Record that in higher level variable (let's call it `max_profit` - only need to store the maximum obtained so far)
- by end of the first loop, we'll have our answer recorded in the higher level variable `max_profit`.

This approach has:
- run time complexity of O(n<sup>2</sup>) (as we have nested loops).
- space complextity of O(1) (since our storage needs doesn't grow with input size i.e. size of the allocated variable `max_profit` is going to be same for any input size).

### Further thoughts
Can we do better than O(n<sup>2</sup>)?

- In our brute-force approach, for each potential buying price, we are eventually looking for the best possible selling price. The inefficiency in this approach is that it keeps looking for the selling price, `even if our current profit becomes 0 or -ve at certain point`. We know for sure that for such cases, our chosen buying price can't really be the solution to our problem as a better buying price exists at later stage due to which the profit becomes either 0 or -ve.
- Let's consider an example `prices = [7,2,5,1,3,6,4]`. Assume that we are at `day 2 (price=2, index=1)`. Now, while looking for potential selling prices, at some point in time, we would consider `selling at day 4 (price=1, index=3)`. At that point the current profit would have been become -1. Which essentially means that there is no point in considering our current buying price (index=1) because either same or better buying price exists at later stage. So, we can safely ignore the intermediate buying prices and directly move to index=3.
- From there on, we can keep looking for the optimal selling price:
    - till we run out of all potential prices.
- At each valid selling point, we record the candidate result in the higher level variable `max_profit` (only if we find any better result from the previously computed candidates).
- If we stumble upon a situation where we encounter `-ve profit`, we ignore looking any further and we move to next possible buying price.

### Final approach
- Initialize a varible namely `max_profit` with current value as `0`.
- Loop through all the elements of given array.
    - keep looking for potential selling prices, till the computed profit so far is `>= 0`.
    - otherwise, (i.e. current profit gets -ve):
        - Move to the current selling price being considered.
    - while we keep getting +ve result store the max of `max_profit` and `current profit` in the variable `max_profit`.
- By end of the main loop we would have gotten our result in the variable `max_profit`. Time to just return it.
- Time complexity: O(n) (since we only process all the elements at max 2 times).
- Space complexity: O(1) (since our auxiliary storage `max_profit` doesn't grow with input size).


### Python code
```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit, buy_price_idx, sell_price_idx = 0, 0, 0
        while sell_price_idx < len(prices):
            current_profit = prices[sell_price_idx] - prices[buy_price_idx]
            if current_profit >= 0:
                max_profit = max(max_profit, current_profit)
                sell_price_idx += 1
            else:
                buy_price_idx = sell_price_idx
        return max_profit

# Alternative thinking model in terms of sliding window
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        buy, maxProfit = 0, 0        
        for sell in range(len(prices)):
            # expand

            # record candidate result if window is valid
            if prices[buy] <= prices[sell]:
                maxProfit = max(maxProfit, prices[sell]-prices[buy])                
            
            # shrink
            if prices[sell] < prices[buy]:
                buy = sell
        return maxProfit
```


    
