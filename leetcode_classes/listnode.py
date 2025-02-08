# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
    def __str__(self):
        ptr = self
        str = f"{ptr.val}, "
        while ptr.next:
            ptr = ptr.next
            str += f"{ptr.val}, "
        return str
    @staticmethod
    def create_linkedList(arr):
        head = ListNode(-1)
        ptr = head
        for num in arr:
            ptr.next = ListNode(num)
            ptr = ptr.next
        return head.next
