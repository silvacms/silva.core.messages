import unittest
from zope.component import getUtility, provideUtility
from Products.Silva.testing import SilvaLayer
from zope.publisher.browser import TestRequest
from silva.core.messages.service import MemoryMessageService
import silva.core.messages

class Session(object):

    def __init__(self, id):
        self.id = id


class ServiceTest(unittest.TestCase):

    def setUp(self):
        provideUtility(
            silva.core.messages.service.MemoryMessageService(),
            silva.core.messages.interfaces.IMessageService)

    def test_utility(self):
        service = getUtility(silva.core.messages.interfaces.IMessageService)
        request = TestRequest()
        request.SESSION = Session('asdfas')
        service.send(u"some unicode message", request)
        self.assertEquals(
            [u"some unicode message"],
            service.receive(request))


class ServiceMessagingTest(unittest.TestCase):

    def setUp(self):
        self.service = silva.core.messages.service.MemoryMessageService()
        self.request = TestRequest()
        self.request.SESSION = Session('asdf')

    def test_no_messages(self):
        self.assertEquals([], self.service.receive(self.request))

    def test_multiple_messages(self):
        self.service.send(u'message1', self.request)
        self.service.send(u'message2', self.request)
        self.assertEquals(
            [u'message1', u'message2'],
            self.service.receive(self.request))
        self.assertEquals([], self.service.receive(self.request))

    def test_multiple_messages_of_different_type(self):
        self.service.send(u'message_type1', self.request, type=u"type1")
        self.service.send(u'message_type2', self.request, type=u"type2")
        self.service.send(u'message_type1', self.request, type=u"type1")

        def receive(type):
            return self.service.receive(self.request, type=type)

        self.assertEquals(
            [u'message_type1', u'message_type1'],
            receive(u'type1'))
        self.assertEquals([], receive(u'type1'))

        self.assertEquals(
            [u'message_type2'], receive(u'type2'))
        self.assertEquals([], receive(u'type2'))


    def test_multiple_messages_of_different_type_fetch_all_at_once(self):
        self.service.send(u'message_type1', self.request, type=u"type1")
        self.service.send(u'message_type2', self.request, type=u"type2")
        self.service.send(u'message_type1', self.request, type=u"type1")

        self.assertEquals(
            [u'message_type1', u'message_type1', u'message_type2'],
            self.service.receive(self.request))
        self.assertEquals([], self.service.receive(self.request))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ServiceTest))
    suite.addTest(unittest.makeSuite(ServiceMessagingTest))    
    return suite
