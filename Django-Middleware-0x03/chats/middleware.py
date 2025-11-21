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
    

class OffensiveLanguageMiddleware(MiddlewareMixin):
    """
    Middleware that limits the number of chat messages a user can send
    within a 1-minute window, based on their IP address.
    """

    # Store request timestamps per IP address
    request_log = {}

    def process_request(self, request):
        # Only track POST requests to message endpoints
        if request.method != "POST":
            return None

        # Extract client IP address
        ip_address = request.META.get("REMOTE_ADDR", "unknown")

        # Initialize if IP not tracked before
        if ip_address not in self.request_log:
            self.request_log[ip_address] = []

        current_time = time.time()
        time_window = 60  # 1 minute
        limit = 5         # max 5 messages per minute

        # Keep only requests from the last 60 seconds
        recent_requests = [
            t for t in self.request_log[ip_address]
            if current_time - t < time_window
        ]
        self.request_log[ip_address] = recent_requests

        # Check if limit exceeded
        if len(recent_requests) >= limit:
            return JsonResponse(
                {
                    "error": "Message rate limit exceeded.",
                    "detail": "You may only send 5 messages per minute.",
                    "ip": ip_address
                },
                status=429
            )

        # Add current timestamp to the list
        self.request_log[ip_address].append(current_time)

        return None
    
    
class RolePermissionMiddleware:
    """
    Middleware that allows only admins or moderators to access restricted paths.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # List of URL paths that require admin/moderator role
        self.restricted_paths = [
            "/admin-only/",
            "/moderator-actions/",
            "/api/admin/",        
            "/api/moderator/",    
        ]

    def __call__(self, request):
        # Check if path is restricted
        request_path = request.path

        if any(request_path.startswith(path) for path in self.restricted_paths):

            # Must be authenticated
            if not request.user.is_authenticated:
                return JsonResponse(
                    {"error": "Authentication required"}, status=401
                )

            # User must have a valid role
            user_role = getattr(request.user, "role", None)

            if user_role not in ["admin", "moderator"]:
                return JsonResponse(
                    {
                        "error": "Forbidden: You do not have the required permissions.",
                        "required_roles": ["admin", "moderator"],
                        "your_role": user_role,
                    },
                    status=403,
                )

        return self.get_response(request)
    