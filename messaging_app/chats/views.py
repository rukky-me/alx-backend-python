from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer


#       USER VIEWSET

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Filters here
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["is_active"]           # filter by active/inactive
    search_fields = ["username", "email"]      # search users



#   CONVERSATION VIEWSET
class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    # Filters here
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["user"]    # filter conversations by user id
    search_fields = ["title"]      # search conversations by title

    def get_queryset(self):
        # Only list conversations belonging to the authenticated user
        return Conversation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Auto-assign the authenticated user as the owner of the conversation
        serializer.save(user=self.request.user)


#       MESSAGE VIEWSET

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    # Filters here
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["conversation", "sender"]  # filter messages
    search_fields = ["content"]                    # search messages by text

    def get_queryset(self):
        # Only messages within conversations that belong to the user
        return Message.objects.filter(conversation__user=self.request.user)

    def perform_create(self, serializer):
        # Auto-set the sender to the authenticated user
        serializer.save(sender=self.request.user)
