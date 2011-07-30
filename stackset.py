"""
Author: Seth Hoenig July 2011
This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://sam.zoy.org/wtfpl/COPYING for more details.
"""

class StackSet(object):
    """
    A LIFO data structure that maintains the properties of a set.
    If an item does not exist in the stack, it is pushed onto the top
    If an item already exists in the stack, it is removed from the stack
    and pushed to the top.
    """    
    def __init__(self, data=None):
        self.data = {}    # { item: queuenum }
        self.bdata = {}   # { queuenum: item }
        self.next_num = 0
        self.high_num = 0
        if not data is None:
            for item in data:
                self.push(item)

    def __contains__(self, item):
        return item in self.data

    def __repr__(self):
        if len(self) == 0:
            return 'StackSet([])'
        r = 'StackSet(['
        for num in sorted(self.bdata.keys()):
            r += repr(self.bdata[num]) + ','
        r = r[0:len(r)-1]
        r += '])'
        return r

    def __str__(self):
        if len(self) == 0:
            return '[]'
        r = '['
        for num in sorted(self.bdata.keys()):
            r += str(self.bdata[num]) + ', '
        r = r[0:len(r)-2]
        r += ']'
        return r

    def __len__(self):
        """Return the number of elements in the stack."""
        return len(self.data)

    def peek(self):
        """Return the element at the top of the stack or None if the 
        stack is empty."""
        if len(self) == 0:
            return None
        else:
            return self.bdata[self.high_num]

    def push(self, item, retval=True):
        """Push element to the top of the stack. If the element already exists in
        the stack, it will now instead be located at the top of the stack. Returns
        True if the item is freshly added, false otherwise."""
        if not item in self.data:
            self.next_num += 1
            self.data[item] = self.next_num
            self.bdata[self.next_num] = item
            self.high_num = self.next_num
            return retval
        else:
            if self.bdata[self.high_num] != item:
                n = self.data[item]
                del self.data[item]
                del self.bdata[n]
                self.push(item, False)
                
    def pop(self):
        """Returns the top item on the stack and removes it."""
        r = self.bdata[self.high_num]
        del self.bdata[self.high_num]
        del self.data[r]
        while not self.high_num in self.bdata and not self.high_num is 0:
            self.high_num -= 1
        return r

    def isdisjoint(self, other):
        for x in self.data:
            if x in other:
                return False
        return True

    def issubset(self, other):
        for x in self.data:
            if not x in other:
                return False
        return True

    def union(self, other):
        a = self.data if len(self.data) > other.data else other.data
        b = self.data if len(self.data) <= other.data else other.data
        r = StackSet(a)
        for x in b:
            r.push(x)
        return r

    def intersection(self, other):
        r = StackSet()
        for x in self.data:
            if x in other:
                r.push(x)
        return r

    def difference(self, other):
        r = StackSet()
        for x in self.data:
            if not x in other:
                r.push(x)
        return r

    def symmetric_difference(self, other):
        r = StackSet()
        for x in self.data:
            if not x in other:
                r.push(x)
        for x in other.data:
            if not x in self:
                r.push(x)
        return r

    def clear(self):
        """Clear the StackSet of all elements."""
        self.data = {}
        self.bdata = {}
        self.next_num = 0
        self.high_num = 0

    def copy(self):
        """Create and return a deep copy of the StackSet."""
        return StackSet(self.data.keys())
