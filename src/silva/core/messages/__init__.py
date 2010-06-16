from zope.component import provideUtility
from silva.core.messages.service import MemoryMessageService
from silva.core.messages.interfaces import IMessageService

# XXX : fix this to use configuration to load the service
provideUtility(MemoryMessageService(), IMessageService)

