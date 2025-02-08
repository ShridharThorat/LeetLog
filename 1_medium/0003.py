# Problem: 3. Longest Substring Without Repeating Characters
# Medium
# Topics: Hashtable, String, Sliding Window

"""
# Date : 06-02-25
# Total time: 40 minutes
# 11 ms, beats 95.04%
# NOTE: One way to do this is to use a queue. While `i` isn't at the end of the string, we can continue to add characters to the queue if the character isn't in the queue. Once we find a repeating character, updating our `max_len`, and then pop the first element in our queue. Once the while-loop is complete, we can update `max_len` once more in case the longest substring extends to the end of the array.<br><br>An alternate technique is to use 2 pointers, `l` and `r` that start off the same. Then while `r` hasn't reached the end, we check if `s[r]` is in the substring `s[l:r]`. If not, we just increment `r`, if it is, we update `max_len`, and move `l` forwards. Similarly in the `queue` technique, we update `max_len` at the end of the loop.

# Description: 

# NOTE

"""

import time
from typing import Optional, List
from collections import deque, Counter
import heapq


class Solution:
    # 49ms
    def lengthOfLongestSubstring(self, s: str) -> int:        
        i = 0
        max_len = 0
        substring = deque([])
        while i < len(s):
            # If our substring has a dupe, shift our window
            if s[i] in substring:
                max_len = max(max_len, len(substring))
                substring.popleft()
            else:
                # Otherwise increase our window size
                substring.append(s[i])
                i += 1
        max_len = max(max_len, len(substring))
        return max_len
    
    # 11ms, beats 95.40%
    def lengthOfLongestSubstring(self, s: str) -> int:
        if len(s) == len(set(s)):
            return len(s)

        l = 0 # Start of window
        r = 0 # end of window

        max_len = 0
        while r < len(s):
            # If our substring has a dupe, shift our window
            if s[r] in s[l:r]:
                max_len = max(max_len, len(s[l:r]))
                l += 1
                r -= 1  # Need to keep our window size the same as when no dupes existed
            # Otherwise increase our window size
            r += 1
        max_len = max(max_len, len(s[l:r]))
        return max_len
    
            

tic = time.perf_counter()
sol = Solution()
ret = sol.lengthOfLongestSubstring("pwwwkew")
print(ret)

toc = time.perf_counter()
print(f"Runtime: {(toc - tic)*1000:0.3f} ms")

