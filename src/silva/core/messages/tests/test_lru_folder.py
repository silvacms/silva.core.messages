import unittest
from Products.Silva.testing import SilvaLayer

from silva.core.messages.lru import PersistentLRUFolder
import silva.core.messages

class PersistentLRUFolderTest(unittest.TestCase):

    layer = SilvaLayer(silva.core.messages)

    def setUp(self):
        self.root = self.layer.get_application()

    def test_creation(self):
        self.assertFalse(True)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PersistentLRUFolderTest))
    return suite
