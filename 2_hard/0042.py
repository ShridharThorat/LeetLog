# Problem: 42. Trapping Rain Water
# Hard
# Topics: Array, Two Pointers, Dynamic Programming, Stack, Monotonic Stack

"""
# Date : 05-02-25
# Total time: 2 hr 16 minutes
#  ms, beats %
# NOTE: For every block, we know the amount of water that could be stored is the minimum of it's left and right walls. We also know that the left-most block has no left-wall and vice versa for the right-most block.<br>First we can set the <b>current</b> `l_wall` and `r_wall` to `0`, and the loop through our heights. The `maxL[i]` is then our previous wall, which is `l_wall`. Then `l_wall` becomes the maximum of itself, or the current height. The same would go for the `r_wall`, but we'd add values to it in reverse (`j=-i-1`).<br>Finally, the amount of water at each block is the min of it's left and right walls, minus its height -- if this is negative, 0 water is stored.<br><br>A Two pointer approach is possible since we really just need to know the minimum of the left or right--not both. If our `maxL<maxR` then we want to move our left-pointer `l` as well as update our next `maxL` to be the max of itself, and the height at `l`. Then the amt of water here is just the `maxL - height[l]`. If not true, then we do the same thing but for `r` (and `r-=1`).

# Description: 

# NOTE

"""

import time
from typing import Optional, List
from collections import deque

class Solution(object):
    # WRONG
    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        l = 0

        water = 0
        while l < len(height):
            if height[l] == 0:
                l+= 1
                continue
                        
            r = l+1
            while r < len(height) and height[r] < height[l]:
                r += 1

            if r==len(height):
                if l+2 != r-1:  # only 3 heights at most left
                    l += 1
                    continue
                else:
                    r -=1
           
            max_water = min(height[r], height[l])*(r-l-1)
            for i in range(l+1,r): # Subtract heights between l and l+d
                max_water -= height[i]
            
            if max_water > 0:
                water += max_water
                
            l = r  # Same as l = l + d
            
        return water
    
    # Greg Hogg - https://www.youtube.com/watch?v=KFdHpOlz8hs
    # 32ms, beats 25.60%
    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        l_wall = r_wall = 0
        n = len(height)
        
        maxL = [0]*n
        maxR = [0]*n
        
        # Determine the biggest walls on the left and right for every single block
        for i in range(n):
            j = -i-1  # quick way to traverse maxR in reverse
            
            maxL[i] = l_wall
            maxR[j] = r_wall
            
            l_wall = max(l_wall, height[i])
            r_wall = max(r_wall, height[j])

        water = 0
        for i in range(n):
            pot = min(maxL[i], maxR[i])
            water += max( 0, pot-height[i])  # Adds 0 if impossible, and pot - height[i] if it is 
        
        return water
    
    # neetcode
    # 11ms, beats 73.20%, 13.56mb, beats 60.51%
    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        if not height:
            return 0
        
        l, r = 0, len(height)-1
        maxL, maxR = height[l], height[r]
        
        res = 0
        while l < r:
            if maxL < maxR:
                l += 1
                maxL = max(maxL, height[l])
                res += maxL - height[l]
            else:
                r -= 1
                maxR = max(maxR, height[r])
                res += maxR - height[r]
        
        return res
            
            
        

tic = time.perf_counter()
sol = Solution()
ret = sol.trap([0,7,1,4,6])
print(ret)

toc = time.perf_counter()
print(f"Runtime: {(toc - tic)*1000:0.3f} ms")

