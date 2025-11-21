import logging
from datetime import datetime, time
from django.http import JsonResponse
from collections import defaultdict

# Configure logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('request_logs.log')   # Log file will appear in project root
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else "Anonymous"

        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # Allowed access window: 6 AM – 9 PM
        self.start_time = time(6, 0)   # 06:00 AM
        self.end_time = time(21, 0)    # 09:00 PM

    def __call__(self, request):
        current_time = datetime.now().time()

        # If outside allowed range → block
        if not (self.start_time <= current_time <= self.end_time):
            return JsonResponse(
                {
                    "detail": "Access to the messaging app is restricted at this time.",
                    "allowed_hours": "06:00 - 21:00"
                },
                status=403
            )

        return self.get_response(request)
    

class MessageRateLimitMiddleware:
    """
    Limit number of chat messages sent per IP within a 1-minute window.
    Max allowed = 5 POST requests per minute.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Store data as: ip_address -> list_of_timestamps
        self.ip_message_log = defaultdict(list)

        # Rate limit settings
        self.max_messages = 5       # 5 messages allowed
        self.time_window = 60       # 60 seconds = 1 minute

    def __call__(self, request):
        # Only limit POST requests — because messages are created using POST
        if request.method == "POST" and "/messages" in request.path:
            
            # Get user IP address
            ip_address = self.get_client_ip(request)
            current_time = time.time()

            # Clean logs: keep only timestamps within the last minute
            recent_timestamps = [
                t for t in self.ip_message_log[ip_address]
                if current_time - t < self.time_window
            ]
            self.ip_message_log[ip_address] = recent_timestamps

            # Check if the limit is exceeded
            if len(recent_timestamps) >= self.max_messages:
                return JsonResponse(
                    {
                        "error": "Rate limit exceeded. You can only send 5 messages per minute.",
                        "ip": ip_address,
                        "limit": self.max_messages,
                        "time_window_seconds": self.time_window
                    },
                    status=429  # Too Many Requests
                )

            # Otherwise, log new request timestamp
            self.ip_message_log[ip_address].append(current_time)

        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        """
        Safely returns the user's IP address.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]  # first IP in list
        return request.META.get("REMOTE_ADDR")