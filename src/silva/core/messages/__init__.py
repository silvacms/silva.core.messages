from zope.component import provideUtility
from silva.core.messages.service import MemoryMessageService
from silva.core.messages.interfaces import IMessageService
from zope.testing import cleanup


# XXX : fix this to use configuration to load the service

def register_utility():
    provideUtility(MemoryMessageService(), IMessageService)

register_utility()
cleanup.addCleanUp(register_utility)
