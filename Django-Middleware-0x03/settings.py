from messaging_app.settings import *

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'chats.middleware.RequestLoggingMiddleware',
    'chats.middleware.RolepermissionMiddleware',
    'chats.middleware.RestrictAccessByTimeMiddleware',
    'chats.middleware.OffensiveLanguageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]