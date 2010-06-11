import unittest
from Products.Silva.tests.layer import SilvaLayer

from silva.core.messages import PersistentLRUFolderTest


class PersistentLRUFolderTest(unittest.TestCase):

    layer = SilvaLayer()

    def setUp(self):
        self.root = self.layer.get_application()

    def test_creation(self):
        self.assertFalse(True)


def test_suite():
    suite = unittest.testSuite()
    suite.addTest(unittest.makeSuite(PersistentLRUFolderTest))
    return suite
