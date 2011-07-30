from testify import *
from queueset import QueueSet

"""
Test Suite for queueset.py
Intended for use with Testify ( https://github.com/Yelp/Testify )
"""

class TestQueueSet(TestCase):

    def fill_queue(self, que, n):
        for x in xrange(0, n):
            que.enqueue(x)

    def test_cons1(self):
        qs = QueueSet()
        assert len(qs) == 0
        assert qs.front() is None

    def test_cons2(self):
        qs = QueueSet([])
        assert len(qs) == 0

    def test_cons3(self):
        qs = QueueSet([1,2,3,4,5])
        assert len(qs) == 5
        assert qs.front() == 1

    def test_poll(self):
        qs = QueueSet(['one','two','three'])
        assert len(qs) == 3
        assert qs.front() == 'one'
        k = qs.poll()
        assert k == 'one'
        assert len(qs) == 2
        assert qs.front() == 'two'

    def test_one_poll(self):
        qs = QueueSet(['a'])
        assert len(qs) == 1
        assert qs.front() == 'a'
        k = qs.poll()
        assert k == 'a'
        assert len(qs) == 0
        assert qs.front() is None

    def test_empty_str(self):
        qs = QueueSet()
        assert str(qs) == '[]'

    def test_empty_repr(self):
        qs = QueueSet()
        assert repr(qs) == 'QueueSet([])'

    def test_str(self):
        qs = QueueSet([1,2,3,4,5])
        assert str(qs) == '[1, 2, 3, 4, 5]'

    def test_repr(self):
        qs = QueueSet([1,3,4])
        assert repr(qs) == 'QueueSet([1,3,4])'
        
    def test_enqueue_two(self):
        qs = QueueSet()
        qs.enqueue('a')
        qs.enqueue('b')
        assert len(qs) == 2
        assert qs.front() == 'a'
        k = qs.poll()
        assert k == 'a'
        assert len(qs) == 1
        assert qs.front() == 'b'
        k = qs.poll()
        assert k == 'b'
        assert len(qs) == 0
        assert qs.front() is None

    def test_enqueue_one_thing_twice(self):
        qs = QueueSet()
        qs.enqueue('home')
        qs.enqueue('home')
        assert len(qs) == 1
        assert qs.front() == 'home'
        k = qs.poll()
        assert k == 'home'
        assert len(qs) == 0
        assert qs.front() is None

    def test_enqueue_multiple_replace_one(self):
        qs = QueueSet()
        qs.enqueue('a')
        qs.enqueue('b')
        qs.enqueue('c')
        qs.enqueue('d')
        qs.enqueue('b')
        assert len(qs) == 4
        assert qs.front() == 'a'
        qs.poll()
        k = qs.poll()
        assert k == 'b'
        assert len(qs) == 2

    def test_enq_multi_replace_multi(self):
        qs = QueueSet()
        self.fill_queue(qs, 100)
        qs.enqueue(23)
        qs.enqueue(47)
        qs.enqueue(34)
        qs.enqueue(194)
        assert 23 in qs
        assert 47 in qs
        assert 34 in qs
        assert 194 in qs
        assert len(qs) == 101
        assert qs.front() == 0

    def test_huge_queue(self):
        qs = QueueSet()
        self.fill_queue(qs, 100000)
        assert len(qs) ==   100000
        self.fill_queue(qs, 100001)
        assert len(qs) ==   100001

    def test_many_polls(self):
        qs = QueueSet()
        self.fill_queue(qs, 10000)
        for i in xrange(0, 9000):
            qs.poll()
        assert len(qs) == 1000
        assert qs.front() == 9000

    def test_clear(self):
        qs = QueueSet()
        self.fill_queue(qs, 100)
        qs.clear()
        assert len(qs) == 0
        qs.enqueue('a')
        qs.enqueue('b')
        qs.clear()
        assert len(qs) == 0
        assert not 'a' in qs
        assert not 'b' in qs

    def test_copy(self):
        qs = QueueSet([1,3,5,7])
        qs2 = qs.copy()
        assert len(qs) == 4
        assert len(qs2) == 4
        qs.enqueue(9)
        assert len(qs) == 5
        assert len(qs2) == 4

    def test_isdisjoint_yes(self):
        qs = QueueSet([1,3,5,7,9])
        tt = QueueSet([0,2,4,6,8])
        assert qs.isdisjoint(tt)

    def test_isdisjoint_no(self):
        qs = QueueSet([2,3,4,5])
        tt = QueueSet([9,7,4])
        assert not qs.isdisjoint(tt)

    def test_iqsubset_yes(self):
        qs = QueueSet(xrange(1,7))
        tt = QueueSet(xrange(0,7))
        assert qs.issubset(tt)

    def test_iqsubset_no(self):
        qs = QueueSet(xrange(0,7))
        tt = QueueSet(xrange(1,7))
        assert not qs.issubset(tt)

    def test_union(self):
        qs = QueueSet(xrange(0,4))
        tt = QueueSet(xrange(6,9))
        p = qs.union(tt)
        assert len(p) == 7

    def test_union_overlap(self):
        qs = QueueSet(xrange(0, 10))
        tt = QueueSet(xrange(5, 20))
        p = qs.union(tt)
        assert len(p) == 20
        q = tt.union(qs)
        assert len(q) == 20

    def test_intersection(self):
        qs = QueueSet([1,3,5,6,7,8])
        tt = QueueSet([0,1,4,6,8,9])
        p = qs.intersection(tt)
        assert len(p) == 3
        q = tt.intersection(qs)
        assert len(p) == 3

    def test_difference(self):
        qs = QueueSet([9,3,6,2,4])
        tt = QueueSet([3,4,5,6,88,21])
        p = qs.difference(tt)
        assert len(p) == 2
        q = tt.difference(qs)
        assert len(q) == 3

    def test_symmetric_difference(self):
        qs = QueueSet([1,2,3,4,5,6])
        tt = QueueSet([5,6,7,8,9])
        p = qs.symmetric_difference(tt)
        assert len(p) == 7
        q = tt.symmetric_difference(qs)
        assert len(q) == 7
