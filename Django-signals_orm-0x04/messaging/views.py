from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from messaging.models import Message
from messaging.utils import build_thread


from messaging.models import Message

messages = (
    Message.objects
    .filter(parent_message__isnull=True)  # top-level messages
    .select_related("sender", "receiver")
    .prefetch_related(
        "replies__sender",
        "replies__receiver",
        "replies__replies"  # nested replies
    )
)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    username = user.username

    user.delete()  # triggers the post_delete signal below

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
