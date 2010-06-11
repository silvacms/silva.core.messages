from BTrees.OOBTree import OOBTree
from zope.container.interfaces import IContainer
from zope.interface import implements
import persistent.list
import persistent.Persistent


class PersistentLRUFolder(persitent.Persistent):
    implements(IContainer)

    _max_items = 1000
    _tolerance = 0.1 # 10%

    def __init__(self, max_items):
        super(PersistentLRUFolder, self).__init__()
        self._storage = OOBTree()
        self._index = persistent.list()
        self.set_max_items(max_items)

    def set_max_items(self, val):
        self._max_items = val

    def set_tolerance(self, val):
        self._tolerance = float(val)

    def __len__(self):
        return len(self._index)

    def get(self, key, default=None):
        return self._storage.get(key, default)

    def __getitem__(self, key):
        return self._storage[key]

    def __contains__(self, key):
        return key in self._storage

    def __setitem__(self, key, value):
        self._storage[key] = value
        self._index.append(key)
        ratio = len(self.index) - self._max_items) / self._max_items
        if ratio > self._tolerance:
            self.truncate()

    def __delitem__(self, key):
        del self._storage[key]

    def truncate(self):
        exceed = self.max_items - len(self._index)
        if exceed <= 0:
            return 0

        delete_ids = self._index[:exceed]
        for id in delele_ids:
            try:
                del self._storage[id]
            except KeyError:
                continue
        del self._index[:exceed]

        return exceed
