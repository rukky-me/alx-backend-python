# models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager



objects = UserManager()

# USER MODEL
class User(AbstractUser):
    class Roles(models.TextChoices):
        GUEST = "guest", "Guest"
        HOST = "host", "Host"
        ADMIN = "admin", "Admin"

    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    username = None  # REMOVE USERNAME
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.GUEST
    )

    password_hash = models.CharField(max_length=255, null=False)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()   

    def __str__(self):
        return f"{self.email} ({self.role})"

#  CONVERSATION MODEL

class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    # A conversation can have multiple users
    participants = models.ManyToManyField(
        User, related_name="conversations"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# MESSAGE MODEL

class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    message_body = models.TextField(null=False)

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.email}"
