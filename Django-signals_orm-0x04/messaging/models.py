from django.db import models 
from django.conf import settings
from messaging.managers import UnreadMessagesManager


User = settings.AUTH_USER_MODEL

objects = models.Manager()
unread = UnreadMessagesManager()

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Returns unread messages for a specific user, optimized using .only()
        """
        return (
            super()
            .get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "content", "timestamp", "read")
        )


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )

    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_messages')

    # NEW FIELD FOR UNREAD FEATURE
    read = models.BooleanField(default=False)

    # MANAGERS
    objects = models.Manager()              # default manager
    unread = UnreadMessagesManager()        # custom unread manager

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} - Message ID {self.message.id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"
