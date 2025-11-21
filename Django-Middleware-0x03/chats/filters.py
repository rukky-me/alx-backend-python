import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filters messages from a user
    sender = django_filters.NumberFilter(field_name="sender__id")

    # Time range filters
    created_after = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = django_filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ["sender", "created_after", "created_before"]
