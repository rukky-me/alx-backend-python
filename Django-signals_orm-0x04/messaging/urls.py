# messaging/urls.py
from rest_framework.routers import DefaultRouter
from messaging.views import MessageViewSet, UserAccountViewSet

router = DefaultRouter()
router.register("messages", MessageViewSet, basename="messages")
router.register("account", UserAccountViewSet, basename="account")

urlpatterns = router.urls
