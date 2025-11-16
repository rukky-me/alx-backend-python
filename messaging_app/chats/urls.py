# chats/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chats.views import ConversationViewSet, MessageViewSet, UserViewSet

# Create router
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
   
    path('', include(router.urls)),
]
