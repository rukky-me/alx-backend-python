from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow access only to participants of the conversation.
    Ensures only authenticated users can access the API.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()

        return False


class IsMessageSenderOrParticipant(permissions.BasePermission):
    """
    Message access allowed only to conversation participants.
    Only the authenticated user can create a message as the sender.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if view.action == 'create':
            sender_id = request.data.get('sender_id')
            if sender_id:
                return str(request.user.pk) == str(sender_id)

        return True

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()

        return False
