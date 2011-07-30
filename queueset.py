"""
Author: Seth Hoenig July 2011
This program is free software. It comes without any warranty, to
the extent permitted by applicable law. You can redistribute it
and/or modify it under the terms of the Do What The Fuck You Want
To Public License, Version 2, as published by Sam Hocevar. See
http://sam.zoy.org/wtfpl/COPYING for more details.
"""

class QueueSet(object):
    """
    A FIFO data structure that maintains the properties of a set.
    If an item does not exist in the queue, it is enqueued to the
    end of the list. If an item already exists in the queue, the
    queue does not change.
    """
    def __init__(self, data=None):
        self.data = {}
        self.bdata = {}
        self.next_num = 0
        self.low_num = 1
        if not data is None:
            for item in data:
                self.enqueue(item)

    def __contains__(self, item):
        return item in self.data

    def __repr__(self):
        if len(self) == 0:
            return 'QueueSet([])'
        r = 'QueueSet(['
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
        """Return the number of elements in the queue."""
        return len(self.data)

    def front(self):
        """Return the element at the front of the queue, or None
        if the queue is empty."""
        if len(self) == 0:
            return None
        else:
            return self.bdata[self.low_num]
        
    def enqueue(self, item, retval=True):
        """Return True if item is freshly added, False otherwise."""
        if not item in self.data:
            self.next_num += 1
            self.data[item] = self.next_num
            self.bdata[self.next_num] = item
            return retval
        else:
            return False
        

    def poll(self):
        """Returns the front element in the queue and removes it."""
        r = self.bdata[self.low_num]
        del self.bdata[self.low_num]
        del self.data[r]
        if self.low_num == self.next_num:
            self.low_num = 1
            self.next_num = 0
        else:
            while not self.low_num in self.bdata:
                self.low_num += 1
        return r

    def isdisjoint(self, other):
        """True is self is setwise disjoint with other, False otherwise."""
        for x in self.data:
            if x in other:
                return False
        return True

    def issubset(self, other):
        """True is self is a subset of other, False otherwise."""
        for x in self.data:
            if not x in other:
                return False
        return True

    def union(self, other):
        """Returns a QueueSet of the union of self and other."""
        a = self.data if len(self.data) > other.data else other.data
        b = self.data if len(self.data) <= other.data else other.data
        r = QueueSet(a)
        for x in b:
            r.enqueue(x)
        return r

    def intersection(self, other):
        """Returns a QueueSet of the intersection of self and other."""
        r = QueueSet()
        for x in self.data:
            if x in other:
                r.enqueue(x)
        return r

    def difference(self, other):
        """Returns a QueueSet of the difference of self and other."""
        r = QueueSet()
        for x in self.data:
            if not x in other:
                r.enqueue(x)
        return r

    def symmetric_difference(self, other):
        """Returns a QueueSet of the symmetric difference of self and other."""
        r = QueueSet()
        for x in self.data:
            if not x in other:
                r.enqueue(x)
        for x in other.data:
            if not x in self:
                r.enqueue(x)
        return r

    def clear(self):
        """Clear the QueueSet of all elements."""
        self.data = {}
        self.bdata = {}
        self.next_num = 0
        self.low_num = 1

    def copy(self):
        """Create and return a deep copy of the QueueSet."""
        return QueueSet(self.data.keys())
