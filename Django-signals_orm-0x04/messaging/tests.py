from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Message, Notification

User = get_user_model()

class NotificationSignalTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="sender", password="password123"
        )
        self.user2 = User.objects.create_user(
            username="receiver", password="password123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)

    def test_notification_created_on_message(self):
        """
        Test that a notification is automatically created
        when a new Message is saved.
        """

        # Create a message
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello!"
        )

        # Check that ONE notification was created
        notifications = Notification.objects.filter(user=self.user2)
        self.assertEqual(notifications.count(), 1)

        # Check that notification is linked to the right message
        notification = notifications.first()
        self.assertEqual(notification.message, message)

        # Check that notification is unread initially
        self.assertFalse(notification.is_read)

    def test_no_duplicate_notifications(self):
        """Ensure only one notification is created per message."""

        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Another message"
        )

        # Ensure only 1 notification is created for 1 message
        notif_count = Notification.objects.filter(message=message).count()
        self.assertEqual(notif_count, 1)