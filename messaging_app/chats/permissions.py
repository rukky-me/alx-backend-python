from rest_framework import permissions
from .models import Conversation, Message


class IsConversationParticipant(permissions.BasePermission):
    """
    Allow access only to participants of the conversation.
    Assumes view has `get_object()` that returns a Conversation or that the object is passed directly.
    """
    def has_object_permission(self, request, view, obj):
        # obj is a Conversation instance or view.get_object() result
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        # if obj is Message, check its conversation
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        return False


class IsMessageSenderOrParticipant(permissions.BasePermission):
    """
    Allow message retrieval by conversation participants, allow message creation if sender is the request.user.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a Message
        if isinstance(obj, Message):
            # allow if user is a conversation participant
            return request.user in obj.conversation.participants.all()
        return False

    def has_permission(self, request, view):
        # For create: ensure sender_id (if provided) matches request.user, or if using authenticated user, allow.
        if view.action == 'create':
            # if you require sender to be authenticated user, enforce it:
            sender_id = request.data.get('sender_id')
            if sender_id:
                try:
                    return str(request.user.pk) == str(sender_id)
                except Exception:
                    return False
            # if you auto-assign sender from request.user (recommended), allow
            return True
        return True
