# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
)


# CONVERSATION VIEWSET
class ConversationViewSet(viewsets.ModelViewSet):
    """
    Handles:
    - List all conversations
    - Retrieve single conversation with nested messages
    - Create a new conversation
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return ConversationCreateSerializer
        return ConversationSerializer

    def create(self, request, *args, **kwargs):
        serializer = ConversationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation = serializer.save()

        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )


#  MESSAGE VIEWSET

class MessageViewSet(viewsets.ModelViewSet):
    """
    Handles:
    - List messages
    - Retrieve message
    - Send message to existing conversation
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a message to a conversation.
        Required fields:
        - sender_id
        - conversation_id
        - message_body
        """
        sender_id = request.data.get("sender_id")
        conversation_id = request.data.get("conversation_id")
        message_body = request.data.get("message_body")

        # Validate sender
        try:
            sender = User.objects.get(user_id=sender_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Sender does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate conversation
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create message
        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )
