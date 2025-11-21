from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Conversation, Message
from .serializers import (
    UserSerializer,
    ConversationSerializer,
    MessageSerializer,
)
from .permissions import (IsParticipantOfConversation)
from .filters import MessageFilter
from .pagination import MessagePagination



# USER VIEWSET

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        "role": ["exact"],
        "is_active": ["exact"],
    }
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def create(self, request, *args, **kwargs):
        """Prevent overriding hashed password logic — UserSerializer handles hashing."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )



# CONVERSATION VIEWSET

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    permission_classes = [IsParticipantOfConversation]

    def get_serializer_class(self):
        if self.action == "create":
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conv = serializer.save()

        # Ensure logged-in user is included
        if self.request.user not in conv.participants.all():
            conv.participants.add(self.request.user)




# MESSAGE VIEWSET

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        "conversation__conversation_id": ["exact"],
        "sender__id": ["exact"],
    }
    ordering_fields = ["sent_at"]
    ordering = ["sent_at"]

    def get_queryset(self):
        # restrict messages to conversations where user is a participant
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """Sender is always request.user — secure and safe."""
        conversation_id = request.data.get("conversation_id")
        message_body = request.data.get("message_body")

        # Validate conversation
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        # Ensure user is a participant
        if request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Create message
        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=message_body,
        )

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
