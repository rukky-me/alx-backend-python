from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from messaging.models import Message
from messaging.utils import build_thread


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    username = user.username

    user.delete()  # triggers the post_delete signal

    return Response({"message": f"User '{username}' deleted successfully"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_thread(request, message_id):
    try:
        message = (
            Message.objects
            .select_related("sender", "receiver")
            .prefetch_related(
                "replies__sender",
                "replies__receiver",
                "replies__replies"
            )
            .get(id=message_id)
        )
    except Message.DoesNotExist:
        return Response({"error": "Message not found"}, status=404)

    thread = build_thread(message)
    return Response(thread)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_unread_messages(request):
    """
    Returns all unread messages for the logged-in user.
    Uses the custom unread manager:
         Message.unread.unread_for_user(user)
    Includes .only() for optimized field selection.
    """
    user = request.user

    unread_messages = (
        Message.unread.unread_for_user(user)   # ← REQUIRED line
        .only("id", "sender", "receiver", "content", "timestamp")  # optimization
        .select_related("sender", "receiver")
    )

    data = [
        {
            "id": msg.id,
            "sender": msg.sender.username,
            "receiver": msg.receiver.username,
            "content": msg.content,
            "timestamp": msg.timestamp,
        }
        for msg in unread_messages
    ]

    return Response({"unread_messages": data})
