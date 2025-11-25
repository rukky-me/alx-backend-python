from django.db import models


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
