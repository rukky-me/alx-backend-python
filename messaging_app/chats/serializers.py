from rest_framework import serializers
from .models import User, Conversation, Message


# USER SERIALIZER (uses CharField & ValidationError)

class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    password_hash = serializers.CharField(write_only=True)

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

    def validate_email(self, value):
        """Ensure email is unique (manual validation example)."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_password_hash(self, value):
        """Simple validation example."""
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value


# CONVERSATION SERIALIZERS
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    # Fields you required:
    participant_count = serializers.SerializerMethodField()
    message_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "participant_count",
            "messages",
            "message_count",
            "created_at",
        ]
        read_only_fields = ["conversation_id", "created_at"]

    def get_participant_count(self, obj):
        return obj.participants.count()

    def get_message_count(self, obj):
        return obj.messages.count()



# MESSAGE SERIALIZERS
class MessageSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField()
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
