from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Ensures:
    - Only authenticated users access the API
    - Only participants of a conversation can view/update/delete it
    """

    def has_permission(self, request, view):
        # Global check: must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Conversation object
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # Message object
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()

        return False
        


class IsMessageSenderOrParticipant(permissions.BasePermission):
    """
    Rules:
    - Conversation participants can view messages
    - Conversation participants can send messages
    - Only the message sender can update or delete a message
    """

    def has_permission(self, request, view):
        # Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # When creating a message, ensure the user is the sender (if sender_id provided)
        if view.action == "create":
            sender_id = request.data.get("sender_id")

            if sender_id:
                # Only allow if sender_id matches request.user
                return str(request.user.pk) == str(sender_id)

            # If you auto-assign sender = request.user in view, allow
            return True

        return True

    def has_object_permission(self, request, view, obj):
        # obj is a Message instance
        if isinstance(obj, Message):

            # Check if user is participant in conversation
            is_participant = request.user in obj.conversation.participants.all()

            # SAFE METHODS (GET, HEAD, OPTIONS)
            if request.method in permissions.SAFE_METHODS:
                return is_participant

            # UPDATE or DELETE → Only sender can modify
            if request.method in ["PUT", "PATCH", "DELETE"]:
                return request.user == obj.sender

            # POST handled in has_permission()
            return is_participant

        return False
