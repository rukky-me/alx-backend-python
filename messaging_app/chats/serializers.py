from rest_framework import serializers
from .models import User, Conversation, Message


# USER SERIALIZER

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "password_hash",
            "created_at",
        ]
        read_only_fields = ["user_id", "created_at"]
        extra_kwargs = {
            "password_hash": {"write_only": True}
        }


# conversation serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "created_at",
        ]
        read_only_fields = ["conversation_id", "created_at"]



# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "conversation",
            "message_body",
            "sent_at",
        ]
        read_only_fields = [
            "message_id",
            "sent_at",
            "sender",
        ]