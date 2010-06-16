from zope.interface import Interface


class IMessageService(Interface):
    """ Utility for registering messages it should receive only IMessages
    """
    def send(message, request, type=u"message"):
        """ send message
        """

    def receive(request, type=u"message"):
        """ receive message
        """

