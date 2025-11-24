from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        # Create a notification for the receiver
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
        print(f"Notification created for {instance.receiver} for message {instance.id}")
        

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # Only run if the message already exists (i.e., an update)
    if instance.pk:
        old_message = Message.objects.get(pk=instance.pk)

        # Detect content change
        if old_message.content != instance.content:
            instance.edited = True

            # Create history record
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content,
                edited_by=instance.edited_by  # The last editor
            )
            
@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    user = instance

    # Delete any MessageHistory entries related to messages the user sent or received
    MessageHistory.objects.filter(message__sender=user).delete()
    MessageHistory.objects.filter(message__receiver=user).delete()

    # Delete Notifications belonging to user
    Notification.objects.filter(user=user).delete()

    # Delete messages sent or received by the user
    Message.objects.filter(sender=user).delete()
    Message.objects.filter(receiver=user).delete()

    # Optional: clean up edits they made
    MessageHistory.objects.filter(edited_by=user).delete()

    # Optional: clean up messages they edited
    Message.objects.filter(edited_by=user).update(edited_by=None)

    print(f"Cleanup completed for deleted user: {user.username}")