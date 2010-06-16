from five import grok
from silva.core.messages.interfaces import IMessageService


class MemoryMessageService(object):

    grok.implements(IMessageService)

    def __init__(self):
        self._storage = {}

    def send(self, message, request, type=u"message"):
        session_id = request.SESSION.id
        if session_id in self._storage:
            store = self._storage[session_id]
        else:
            store = self._storage[session_id] = {}
        if type in store:
            message_list = store[type]
        else:
            message_list = store[type] = list()
        message_list.append(message)

    def receive(self, request, type=None):
        session_id = request.SESSION.id
        store = self._storage.get(session_id, {})
        if type is None:
            messages = list()
            for type, message_list in store.iteritems():
                messages += message_list
            store.clear()
            return messages
        messages = store.get(type, list())
        if store.has_key(type):
            del store[type]
        return messages

