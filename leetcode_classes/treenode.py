class TreeNode(object):
    # root = TreeNode.level_order_insertion([3,9,20,'null','null',15,7])
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
    def __repr__(self):
        if self.left:
            l = self.left.val
        else:
            l = None
        if self.right:
            r = self.right.val
        else:
            r = None
        return f"{self.val}: L:{l}, R:{r}"
    
    @staticmethod
    def level_order_insertion(array, i):
        root = None
        
        if i < len(array):
            root = TreeNode(array[i])
            
            root.left = TreeNode.level_order_insertion(array, 2*i + 1)
            root.right = TreeNode.level_order_insertion(array, 2*i + 2)
        
        return root
    
    @staticmethod
    def level_order_insertion(array):
        if not array:
            return None
        
        root = TreeNode(array[0])
        
        queue = [root]  # Add each node once connected to a parent
        i = 0
        while 2*i+1 < len(array):
            this_node = queue.pop(0)
            if 2*i+1 < len(array) and array[2*i+1] != 'null':
                this_node.left = TreeNode(array[2*i+1])
                queue.append(this_node.left)
            if 2*i+2 < len(array) and array[2*i+2] != 'null':
                this_node.right = TreeNode(array[2*i+2])
                queue.append(this_node.right)
                
            i += 1
        return root
