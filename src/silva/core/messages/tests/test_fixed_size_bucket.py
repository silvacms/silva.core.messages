import unittest
from silva.core.messages.service import FixedSizeBucket

B = FixedSizeBucket


class TestFixedSizeBucket(unittest.TestCase):

    def test_get_set_item(self):
        bucket = B(10)
        bucket['a'] = 'b'
        self.assertEquals('b', bucket['a'])

    def test_get(self):
        bucket = B(10)
        bucket['a'] = 'b'
        self.assertEquals('b', bucket.get('a'))
        self.assertEquals(None, bucket.get('c'))

    def test_set(self):
        bucket = B(10)
        bucket['a'] = 'b'
        self.assertEquals('c', bucket.set('c', 'd'))

    def test_size_exceeded(self):
        bu1 = B(10, tolerance=0)
        bu2 = B(9, tolerance=0)
        for i in range(1,11):
            bu1[i] = i
            bu2[i] = i
        self.assertEquals(1, bu1.get(1))
        self.assertEquals(None, bu2.get(1))

    def test_size_exceeded_with_tolerance(self):
        bu1 = B(10, tolerance=0.2)
        bu2 = B(10, tolerance=0)
        for i in range(1,13):
            bu1[i] = i
            bu2[i] = i
        self.assertEquals(1, bu1.get(1))
        self.assertEquals(2, bu1.get(2))
        self.assertEquals(None, bu2.get(1))
        self.assertEquals(None, bu2.get(2))

    def test_delete_when_eval_to_false(self):
        b = B(10)
        hash = {'b': 'b'}
        b['a'] = hash
        self.assertEquals({'b': 'b'}, b.get('a'))
        hash.clear()
        self.assertEquals(None, b.get('a'))
        self.assertFalse('a' in b)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFixedSizeBucket))
    return suite
