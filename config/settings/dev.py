"""Development settings. This is the default when you run manage.py."""

from .base import *  # noqa: F401,F403

DEBUG = True

# Show debug toolbar if it is installed (it is in requirements/dev.txt)
try:
    import debug_toolbar  # noqa: F401

    INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405
    INTERNAL_IPS = ["127.0.0.1"]
except ImportError:
    pass

# Faster password hashing makes tests quicker (never use in production)
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
