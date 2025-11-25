from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from messaging.models import Message
from messaging.serializers import MessageSerializer
from messaging.utils import build_thread


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

    user.delete()  # triggers post_delete cleanup

    return Response(
        {"message": f"User '{username}' deleted successfully"},
        status=status.HTTP_200_OK
    )


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


class MessageViewSet(viewsets.ModelViewSet):
    """
    Handles listing, creating, retrieving messages.
    Thread view remains separate because you requested
    to keep its original function name (get_thread).
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        # use your optimized queryset
        return messages

    # Preserve your sender=request.user requirement
    def perform_create(self, serializer):
        serializer.save(sender=request.user)
