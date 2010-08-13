from five import grok
from silva.core.messages.interfaces import IMessageService, IMessage
from silva.core.cache.interfaces import ICacheManager
import zope.publisher.interfaces.browser
from zope.session.interfaces import IClientId
from zope.component import getUtility


_marker = object()


class ClientId(grok.Adapter):
    grok.context(zope.publisher.interfaces.browser.IBrowserRequest)
    grok.provides(IClientId)

    def __str__(self):
        return str(self.context.SESSION.id)


class Message():
    grok.implements(IMessage)

    namespace = None

    def __init__(self, string, namespace='message'):
        self.content = string
        self.namespace = namespace

    def __str__(self):
        return self.content


class Store(object):

    def __init__(self, name):
        self.ns = 'silva.core.messages.store.%s'
        cache_manager = getUtility(ICacheManager)
        self._backend = cache_manager.get_cache(self.ns, 'shared')

    def get(self, key, default=None):
        return self._backend.get(key)

    def set(self, key, value):
        return self._backend.put(key, value)

    def __getitem__(self, key):
        val = self._backend.get(key, _marker)
        if val is _marker:
            raise KeyError

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return self._backend.has_key(key)

    def __delitem__(self, key):
        self._backend.remove(key)


class MemoryMessageService(object):

    grok.implements(IMessageService)

    def __init__(self):
        self.store = Store('messages')

    def send(self, message_str, request, namespace=u"message"):
        session_id = str(IClientId(request))
        messages = self.store.get(session_id, list())
        messages.append(Message(message_str, namespace=namespace))
        self.store.set(session_id, messages)

    def receive(self, request, namespace=u"message"):
        session_id = str(IClientId(request))
        messages = self.store.get(session_id, list())
        keep = list()
        reception = list()
        for message in message:
            if message.namespace != namespace:
                keep.append(message)
            else:
                reception.append(message)
        self.store.set(session_id, keep)
        return reception

    def receive_all(self, request):
        session_id = str(IClientId(request))
        messages = self.store.get(session_id, list())
        del self.store[session_id]
        return messages

