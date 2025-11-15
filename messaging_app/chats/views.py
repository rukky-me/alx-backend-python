from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer, ConversationCreateSerializer



# USER VIEWSET

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["is_active"]
    search_fields = ["email", "first_name", "last_name"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


# CONVERSATION VIEWSET

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["participants__user_id"]
    search_fields = ["conversation_id"]

    def get_queryset(self):
        # Conversations where user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = ConversationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)


# MESSAGE VIEW
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["conversation__conversation_id", "sender__user_id"]
    search_fields = ["message_body"]

    def get_queryset(self):
        # Messages in conversations where the user is a participant
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        sender_id = request.data.get("sender_id")
        conversation_id = request.data.get("conversation_id")
        message_body = request.data.get("message_body")

        # Validate sender
        try:
            sender = User.objects.get(user_id=sender_id)
        except User.DoesNotExist:
            return Response({"error": "Sender does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate conversation
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
