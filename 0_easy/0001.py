# Problem: 1. Two Sum
# Easy
# Topics: Array, Hashtable

"""
# Date: 19-01-25
# Total time: 20 min
# 1313 ms, beats 43.96%
# NOTE: Iterate through the array and for each number, add `value, index` pair-since we don't care about which `4` we look at in [1,2,4,4,4]. Also check if the complement exists already, and if so, return the current index and the complement's index. Otherwise return [0,0].

# Description: 
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

# NOTE
return ndex of 2 numbers
always one answer

# Technique 1: 1313 ms, beats 43.96%, 12.76mb, beats 81.73%
in O(n) time, you could loop through once, and find the complement if it exists
for num in nums:
    try:
        indices = [nums.index(nums), nums.index(complement,nums.index(num)+1)]
        return indices
    except ValueError:
        continue

return [0,0]

# Technique 2: 0ms, beats 100%, 13.22mb, beats 30.58%
using a hash map, add the value and its index to the hash map. if the complement exists in the hash, return it's value and the current
number's index
"""

import time

class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        map = {}
        for i,v in enumerate(nums):
            complement = target - v
            if complement in map:
                return [i, map[complement]]
            map[v] = i

        return [0,0]
        
        
        

tic = time.perf_counter()
sol = Solution()
nums = [3,2,4]

target = 6
ret = sol.twoSum(nums, target)
print(ret)

toc = time.perf_counter()
print(f"Runtime: {(toc - tic)*1000:0.3f} ms")

