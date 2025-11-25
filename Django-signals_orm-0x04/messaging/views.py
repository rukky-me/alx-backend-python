from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from messaging.models import Message
from messaging.utils import build_thread


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unread_messages(request):
    """
    Return unread messages for the authenticated user
    using Message.unread.for_user() and optimized .only()
    """


    Message.objects.filter(receiver=request.user)

    unread_qs = Message.unread.for_user(request.user)

    data = [
        {
            "id": msg.id,
            "sender": msg.sender_id,
            "content": msg.content,
            "timestamp": msg.timestamp,
        }
        for msg in unread_qs
    ]

    return Response({"unread_messages": data})


messages = (
    Message.objects
    .filter(parent_message__isnull=True)
    .select_related("sender", "receiver")
    .prefetch_related(
        "replies__sender",
        "replies__receiver",
        "replies__replies"
    )
)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    username = user.username

    user.delete()  # triggers post_delete signal

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
            .only(
                "id", "sender", "receiver", "content", "timestamp",
                "parent_message"
            )
            .get(id=message_id)
        )
    except Message.DoesNotExist:
        return Response({"error": "Message not found"}, status=404)

    thread = build_thread(message)
    return Response(thread)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reply_to_message(request, message_id):
    parent = Message.objects.filter(id=message_id).first()  # ✔ contains filter
    if not parent:
        return Response({"error": "Parent message not found"}, status=404)

    content = request.data.get("content")
    if not content:
        return Response({"error": "Content is required"}, status=400)

    reply = Message.objects.create(
        sender=request.user,
        receiver=parent.receiver,
        content=content,
        parent_message=parent
    )

    return Response({"message": "Reply sent", "reply_id": reply.id}, status=201)
