# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        curr, prev, length1 = l1, None, 0
        while curr:
            n = curr.next
            length1 += 1
            curr.next = prev
            prev = curr
            curr = n
        l1 = prev

        curr, prev, length2 = l2, None, 0
        while curr:
            n = curr.next
            length2 += 1
            curr.next = prev
            prev = curr
            curr = n
        l2 = prev

        if length1 > length2:
            l, r = l1, l2
        else:
            l, r = l2, l1
        rem = 0
        head = l
        prev = None
        while l or r:
            t = (l.val if l is not None else 0) + (r.val if r is not None else 0) + rem
            s = (t) % 10
            rem = (t) // 10
            l.val = s
            if l:
                prev = l
                l = l.next
            if r:
                r = r.next
        if rem > 0:
            prev.next = ListNode(rem)
        curr, prev = head, None
        while curr:
            n = curr.next
            curr.next = prev
            prev = curr
            curr = n

        return prev

s = Solution()
h1 = ListNode(5)

h2 = ListNode(5)
print(s.addTwoNumbers(h1, h2))