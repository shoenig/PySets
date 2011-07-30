from testify import *
from queueset import QueueSet

"""
Test Suite for queueset.py
Intended for use with Testify ( https://github.com/Yelp/Testify )
"""

class TestQueueSet(TestCase):

    def fill_queue(self, que, n):
        for x in xrange(0, n):
            que.enqueue(n)

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
        assert qs.front() == None
