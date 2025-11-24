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
    # Only run if message already exists (edit)
    if instance.pk:
        old_message = Message.objects.get(pk=instance.pk)

        # Content changed?
        if old_message.content != instance.content:
            # Mark edited
            instance.edited = True

            # Save old version in history table
            MessageHistory.objects.create(
                message=instance,
                old_content=old_message.content
            )