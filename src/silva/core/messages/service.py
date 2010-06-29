from five import grok
from threading import Lock
from silva.core.messages.interfaces import IMessageService
import zope.publisher.interfaces.browser
from zope.session.interfaces import IClientId
import uuid

_marker = object()


# class ClientId(grok.Adapter):
#     grok.context(zope.publisher.interfaces.browser.IBrowserRequest)
#     grok.provides(IClientId)

#     def __str__(self):
#         return str(self.context.SESSION.id)


class Message(object):

    def __init__(self, content):
        self.uuid = str(uuid.uuid4())
        self.content = content

    def __str__(self):
        return self.content


class FixedSizeBucket(object):
    """ The bucket keep track of its size and delete some items if it grows
    too much.
    """
    def __init__(self, size, tolerance=0.2):
        self.tolerance = float(tolerance)
        self.__size = size
        self._item_index = list()
        self._items = {}
        self.__clear_lock = Lock()

    def __getitem__(self, key):
        return self._items[key]

    def __contains__(self, key):
        return key in self._item_index

    def get(self, key, default=None, autocleanup=True):
        if autocleanup:
            value = self._items.get(key, _marker)
            if value is _marker:
                return default
            if not value:
                del self[key]
                return default
            return value
        return self._items.get(key, default)

    def __setitem__(self, key, value):
        self._item_index.append(key)
        self._items[key] = value
        self.cleanup()
        return key

    set = __setitem__

    def __delitem__(self, key):
        if self.__clear_lock.acquire(False):
            try:
                del self._items[key]
                self._item_index.remove(key)
            finally:
                self.__clear_lock.release()

    def __recall(self):
        if self.__clear_lock.acquire(False):
            try:
                del_count = len(self) - self.__size
                if del_count < 1:
                    return
                items_to_delete = self._item_index[:del_count]
                for key in items_to_delete:
                    del self._items[key]
                del self._item_index[:del_count]
            finally:
                self.__clear_lock.release()

    def exceed_ratio(self):
        return ((len(self) - self.__size) / float(self.__size))

    def should_cleanup(self):
        ratio = self.exceed_ratio()
        if self.tolerance < ratio:
            return True
        return False

    def cleanup(self):
        if self.should_cleanup():
            self.__recall()

    def __len__(self):
        return len(self._item_index)


class MemoryMessageService(object):

    grok.implements(IMessageService)

    def __init__(self):
        self._session_bucket = FixedSizeBucket(100)
        self._message_bucket = FixedSizeBucket(1000)

    def send(self, message, request, namespace=u""):
        session_id = str(IClientId(request))
        if session_id in self._session_bucket:
            store = self._session_bucket[session_id]
        else:
            store = {}
            self._session_bucket[session_id] = store
        if namespace in store:
            message_list = store[namespace]
        else:
            message_list = list()
            store[namespace] = message_list
        message = Message(message)
        message_list.append(
            self._message_bucket.set(message.uuid, message))
        return message

    def receive(self, request, namespace=u''):
        messages = []
        session_id = str(IClientId(request))
        session_store = self._session_bucket.get(session_id)
        if not session_store:
            return messages
        message_ids = session_store.get(namespace, list())
        for id in message_ids:
            message = self._message_bucket.get(id)
            if message:
                del self._message_bucket[id]
                messages.append(message)
        return messages

    def receive_all(self, request):
        messages = []
        session_id = str(IClientId(request))
        session_store = self._session_bucket.get(session_id)
        if not session_store:
            return messages
        for namespace in session_store:
            messages += [(namespace, message,)
                         for message in self.receive(request, namespace)]
        return messages

