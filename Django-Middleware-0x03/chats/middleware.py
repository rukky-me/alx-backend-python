import logging
from datetime import datetime, time
from django.http import JsonResponse

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