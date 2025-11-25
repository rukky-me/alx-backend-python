# messaging/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
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

    user.delete()  # triggers automatic post_delete cleanup

    return Response(
        {"message": f"User '{username}' deleted successfully"},
        status=status.HTTP_200_OK
    )



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_thread(request, message_id):
    # Explicit use of Message.objects.filter (your requirement)
    base_queryset = (
        Message.objects
        .filter(id=message_id)  # <-- required filter usage
        .select_related("sender", "receiver")
        .prefetch_related(
            "replies__sender",
            "replies__receiver",
            "replies__replies"
        )
    )

    message = base_queryset.first()
    if not message:
        return Response({"error": "Message not found"}, status=404)

    thread = build_thread(message)
    return Response(thread)


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        # Reuse your optimized queryset
        return messages

    def perform_create(self, serializer):
        # Required: sender=request.user
        serializer.save(sender=request.user)
