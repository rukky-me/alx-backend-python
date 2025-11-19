from rest_framework.authentication import BasicAuthentication

class ChatBasicAuthentication(BasicAuthentication):
    """
    Custom BasicAuthentication class for the chats app.
    Currently extends DRF's BasicAuthentication without changes,
    but allows future customization (logging, role checks, etc.).
    """
    pass
