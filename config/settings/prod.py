"""Production settings. Used by wsgi.py / asgi.py. DEBUG must be False."""

from .base import *  # noqa: F401,F403

DEBUG = False

# Serve static files with Whitenoise (behind Gunicorn / Nginx)
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")  # noqa: F405
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# HTTPS and cookie security
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)  # noqa: F405
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Send error emails to these people. Example: ADMINS_EMAILS=lead@example.com
ADMINS = [("Admin", e) for e in env.list("ADMINS_EMAILS", default=[])]  # noqa: F405
