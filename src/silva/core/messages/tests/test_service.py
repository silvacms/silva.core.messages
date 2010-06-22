import unittest
from zope.component import getUtility, provideUtility
from Products.Silva.testing import SilvaLayer
from zope.publisher.browser import TestRequest
from silva.core.messages.service import MemoryMessageService
import silva.core.messages


def messages_to_string(message_list):
    return [(type, str(msg),) for (type, msg,) in message_list] 

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
            [(u'', u"some unicode message",)],
            messages_to_string(service.receive_all(request)))


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
            [(u'', u'message1',),
             (u'', u'message2',)],
            messages_to_string(self.service.receive_all(self.request)))
        self.assertEquals([], self.service.receive(self.request))

    def test_multiple_messages_of_different_type(self):
        self.service.send(u'message_type1', self.request, namespace=u"type1")
        self.service.send(u'message_type2', self.request, namespace=u"type2")
        self.service.send(u'message_type1', self.request, namespace=u"type1")

        def receive(type):
            return self.service.receive(self.request, type)

        self.assertEquals(
            [u'message_type1',
             u'message_type1',],
            map(str, receive(u'type1')))
        self.assertEquals([], receive(u'type1'))

        self.assertEquals(
            [u'message_type2',], map(str, receive(u'type2')))
        self.assertEquals([], receive(u'type2'))


    def test_multiple_messages_of_different_type_fetch_all_at_once(self):
        self.service.send(u'message_type1', self.request, namespace=u"type1")
        self.service.send(u'message_type2', self.request, namespace=u"type2")
        self.service.send(u'message_type1', self.request, namespace=u"type1")

        self.assertEquals(
            [(u'type1', u'message_type1',),
             (u'type1', u'message_type1',),
             (u'type2', u'message_type2',)],
            messages_to_string(self.service.receive_all(self.request)))
        self.assertEquals([], self.service.receive(self.request))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ServiceTest))
    suite.addTest(unittest.makeSuite(ServiceMessagingTest))
    return suite
