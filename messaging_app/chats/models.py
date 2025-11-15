# users/models.py
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.models import User

class User(AbstractUser):
    class Roles(models.TextChoices):
        GUEST = "guest", "Guest"
        HOST = "host", "Host"
        ADMIN = "admin", "Admin"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None  # Remove username from AbstractUser
    email = models.EmailField(unique=True, null=False)

    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.GUEST
    )

    # AbstractUser includes password, so no need for password_hash separately

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.email} ({self.role})"


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} in {self.conversation.id}"
    
class User(AbstractUser):
    ...
    class Meta:
        indexes = [
            models.Index(fields=["email"]),
        ]
