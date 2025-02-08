# Problem: 104. Maximum Depth of Binary Tree
# easy
# Topics: tree, Depth-First-Search, Breadth-First-Search, binary tree

"""
# Date: 27-01-25
# Total time: 5 minutes
# 0 ms, beats 100%, 15.06mb, beats 56.55%
# NOTE:

# Description: 

# NOTE
same as finding the min depth, just no quick exit - we have to traverse the entire tree
"""

import time
from collections import deque
from leetcode_classes.treenode import TreeNode

class Solution(object):
    def maxDepth(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """
        if not root:
            return 0
        
        queue = deque([(root,1)])
        while queue:
            node, level = queue.popleft()
            if node.left:
                queue.append((node.left, level +1))
            if node.right:
                queue.append((node.right, level +1))
        return level
    
    
    # Recursive solution - internet
    def maxDepth(self, root):
        """
        :type root: Optional[TreeNode]
        :rtype: int
        """
        if not root:
            return 0  # Base case: If the tree is empty, the depth is 0

        # Recursively find the depth of the left and right subtrees
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)

        # Return the maximum of the two depths plus 1 (for the current node)
        return max(left_depth, right_depth) + 1
    
        
        

tic = time.perf_counter()
sol = Solution()
root = TreeNode.level_order_insertion([3,9,20,'null','null',15,7])
ret = sol.maxDepth(root)
print(ret)

toc = time.perf_counter()
print(f"Runtime: {(toc - tic)*1000:0.3f} ms")

