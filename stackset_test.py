from testify import *
from stackset import StackSet

"""
Test Suite for stackset.py
Intended for use with Testify ( https://github.com/Yelp/Testify )
"""

class TestStackSet(TestCase):

    def fill_stack(self, stk, n):
        for x in xrange(0, n):
            stk.push(x)
    
    def test_cons1(self):
        ss = StackSet()
        assert len(ss) == 0
        assert ss.peek() is None

    def test_cons2(self):
        ss = StackSet([])
        assert len(ss) == 0

    def test_cons3(self):
        ss = StackSet([1,2,3,4,5])
        assert len(ss) == 5
        assert ss.peek() == 5

    def test_push_into_empty(self):
        ss = StackSet()
        ss.push('hi')
        assert len(ss) == 1
        assert ss.peek() == 'hi'
        k = ss.pop()
        assert len(ss) == 0
        assert k == 'hi'
    
    def test_empty_str(self):
        ss = StackSet()
        assert str(ss) == '[]'

    def test_str(self):
        ss = StackSet()
        self.fill_stack(ss, 5)
        assert ss.peek() == 4
        assert str(ss) == '[0, 1, 2, 3, 4]'

    def test_empty_repr(self):
        ss = StackSet()
        assert ss.peek() is None
        assert repr(ss) == 'StackSet([])'

    def test_repr(self):
        ss = StackSet()
        self.fill_stack(ss, 5)
        assert repr(ss) == 'StackSet([0,1,2,3,4])'

    def test_push_two(self):
        ss = StackSet()
        ss.push('a')
        ss.push('b')
        assert len(ss) == 2
        k = ss.pop()
        assert k == 'b'
        assert len(ss) == 1
        k = ss.pop()
        assert k == 'a'
        assert len(ss) == 0

    def test_push_one_thing_twice(self):
        ss = StackSet()
        ss.push('pokey')
        ss.push('pokey')
        assert len(ss) == 1
        k = ss.pop()
        assert k == 'pokey'
        assert len(ss) == 0

    def test_push_multiple_replace_one(self):
        ss = StackSet()
        self.fill_stack(ss, 20)
        assert len(ss) == 20
        ss.push(15)
        assert len(ss) == 20
        k = ss.pop()
        assert k == 15
        assert len(ss) == 19

    def test_push_multiple_replace_multiple(self):
        ss = StackSet()
        self.fill_stack(ss, 100)
        ss.push(5)
        ss.push(50)
        ss.push(55)
        ss.push(105)
        assert 5 in ss
        assert 50 in ss
        assert 55 in ss
        assert 105 in ss
        assert len(ss) == 101
        assert ss.peek() == 105
        
    def test_huge_stack(self):
        ss = StackSet()
        self.fill_stack(ss, 100000)
        assert len(ss) ==   100000
        self.fill_stack(ss, 100001)
        assert len(ss) ==   100001

    def test_many_pops(self):
        ss = StackSet()
        self.fill_stack(ss, 10000)
        for i in xrange(0, 9000):
            ss.pop()
        assert len(ss) == 1000
        assert ss.peek() == 999

    def test_clear(self):
        ss = StackSet()
        ss.push(3)
        ss.push(5)
        ss.clear()
        assert len(ss) == 0
        ss.push(1)
        ss.push(9)
        assert len(ss) == 2
        ss.clear()
        assert len(ss) == 0
        assert not 3 in ss
        assert not 5 in ss
        assert not 1 in ss
        assert not 9 in ss

    def test_copy(self):
        ss = StackSet([1,3,5,7])
        ss2 = ss.copy()
        assert len(ss2) == 4
        ss.push(9)
        assert len(ss) == 5
        assert len(ss2) == 4

    def test_isdisjoint_yes(self):
        ss = StackSet([1,3,5,7,9])
        tt = StackSet([0,2,4,6,8])
        assert ss.isdisjoint(tt)

    def test_isdisjoint_no(self):
        ss = StackSet([2,3,4,5])
        tt = StackSet([9,7,4])
        assert not ss.isdisjoint(tt)

    def test_issubset_yes(self):
        ss = StackSet(xrange(1,7))
        tt = StackSet(xrange(0,7))
        assert ss.issubset(tt)

    def test_issubset_no(self):
        ss = StackSet(xrange(0,7))
        tt = StackSet(xrange(1,7))
        assert not ss.issubset(tt)

    def test_union(self):
        ss = StackSet(xrange(0,4))
        tt = StackSet(xrange(6,9))
        p = ss.union(tt)
        assert len(p) == 7

    def test_union_overlap(self):
        ss = StackSet(xrange(0, 10))
        tt = StackSet(xrange(5, 20))
        p = ss.union(tt)
        assert len(p) == 20
        q = tt.union(ss)
        assert len(q) == 20

    def test_intersection(self):
        ss = StackSet([1,3,5,6,7,8])
        tt = StackSet([0,1,4,6,8,9])
        p = ss.intersection(tt)
        assert len(p) == 3
        q = tt.intersection(ss)
        assert len(p) == 3

    def test_difference(self):
        ss = StackSet([9,3,6,2,4])
        tt = StackSet([3,4,5,6,88,21])
        p = ss.difference(tt)
        assert len(p) == 2
        q = tt.difference(ss)
        assert len(q) == 3

    def test_symmetric_difference(self):
        ss = StackSet([1,2,3,4,5,6])
        tt = StackSet([5,6,7,8,9])
        p = ss.symmetric_difference(tt)
        assert len(p) == 7
        q = tt.symmetric_difference(ss)
        assert len(q) == 7
