from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_messages')


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


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reply_to_message(request, message_id):
    parent = Message.objects.filter(id=message_id).first()
    if not parent:
        return Response({"error": "Parent message not found"}, status=404)

    content = request.data.get("content")
    if not content:
        return Response({"error": "Content is required"}, status=400)

    reply = Message.objects.create(
        sender=request.user,
        receiver=parent.receiver,  # or logic depending on chat system
        content=content,
        parent_message=parent
    )

    return Response({"message": "Reply sent", "reply_id": reply.id}, status=201)    