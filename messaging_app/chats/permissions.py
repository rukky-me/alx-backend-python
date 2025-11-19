# chat/permissions.py
from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow access only to participants of the conversation.
    Ensures only authenticated users can access the API.
    """
    def has_permission(self, request, view):
        # Require authentication for any action
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Object-level check: user must be participant
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        return False


class IsMessageSenderOrParticipant(permissions.BasePermission):
    """
    Allow message access only to conversation participants.
    Creation allowed only if sender is the authenticated user.
    """
    def has_permission(self, request, view):
        # Require authentication
        if not request.user or not request.user.is_authenticated:
            return False

        # Creation check: sender must be request.user if sender_id is provided
        if view.action == 'create':
            sender_id = request.data.get('sender_id')
            if sender_id:
                return str(request.user.pk) == str(sender_id)
            # if sender auto-assigned from request.user, allow
            return True
        return True

    def has_object_permission(self, request, view, obj):
        # Object-level check: user must be a participant of the conversation
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        return False
